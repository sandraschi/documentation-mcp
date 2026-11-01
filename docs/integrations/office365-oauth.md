# Office 365 & Microsoft Account Authentication (OAuth2 / Azure / Graph)

**Established**: 2026-07-31
**Reference implementations**: `email-mcp` (Exchange IMAP/SMTP XOAUTH2 + Microsoft Graph service), `onenote-mcp` (Graph via MSAL device-code)
**Category**: integrations

## 1. The Problem: Microsoft killed basic auth

Since September 2024, Microsoft disables **basic authentication** (username +
password, including **app passwords**) for personal Outlook.com / Hotmail / Live
accounts:

| Symptom | Meaning |
|---------|---------|
| SMTP `535 5.7.139 Authentication unsuccessful, basic authentication is disabled` | SMTP AUTH disabled for the mailbox — personal accounts permanently, M365 until admin re-enables |
| IMAP `AUTHENTICATE failed` | Same policy on IMAP |
| App password accepted nowhere | App passwords ARE basic auth — they do not help personal accounts |

Consequences for fleet servers:

- **Password-based SMTP/IMAP clients cannot talk to personal Microsoft accounts.**
- **Microsoft 365 business** mailboxes work only if the admin enables SMTP AUTH
  (`Set-CASMailbox -Identity user@domain -SmtpClientAuthenticationDisabled $false`)
  or the tenant exempts legacy auth — app passwords then work.
- The durable path for **both** personal and business accounts is **OAuth2** with
  **XOAUTH2** (SASL) for IMAP/SMTP, or the **Microsoft Graph REST API**.

## 2. The Azure App Registration (free)

An **app registration** in Microsoft Entra ID is free — no subscription, no
billing, no credit card. It is the identity the consent screen shows.

### 2.1 Create one

1. https://portal.azure.com → **Microsoft Entra ID** → **App registrations** →
   **New registration**.
2. Name: `email-mcp` (or the product name).
3. Supported account types: **Personal Microsoft accounts only** (or *...and
   organizational directory* for M365 support).
4. Redirect URI: **none** — we use the device-code flow, which needs no redirect.
5. Copy the **Application (client) ID** (`xxxxxxxx-xxxx-...`).

### 2.2 Required settings

| Setting | Where | Value |
|---------|-------|-------|
| **Allow public client flows** | Authentication → Advanced settings | **Yes** (mandatory for device code) |
| **IMAP.AccessAsUser.All** | API permissions → Office 365 Exchange Online → Delegated | consent at first login |
| **SMTP.Send** | same | consent at first login |
| **Mail.Read / Mail.Send** | API permissions → Microsoft Graph → Delegated | consent at first login (Graph path) |

For personal accounts the user consents interactively during the device flow
(they are their own "admin"); M365 tenants may require an admin to grant consent.

### 2.3 Public alternative: Graph Explorer client ID

`onenote-mcp` uses Microsoft's shared **Graph Explorer** client ID
(`14d82eec-204b-4c2f-b7e8-296a70dab67e`) with the MSAL device-code flow — no app
registration needed at all. Trade-off: the consent screen says "Graph Explorer",
and the token is not revocable per-app. Fine for personal use; a private
registration is cleaner for distribution.

## 3. The Device-Code Flow

No web server / redirect listener is required — ideal for headless MCP servers.

```
Server                    User                     Microsoft
  | POST /devicecode       |                          |
  |  <- user_code, URI     |                          |
  |                        |-- open microsoft.com/devicelogin -->|
  |                        |-- enter user_code -------------->|
  |                        |-- approve scopes --------------->|
  | POST /token (poll) ----|---------------------------------->|
  |  <- access_token + refresh_token                          |
```

- Endpoints: `https://login.microsoftonline.com/common/oauth2/v2.0/devicecode`
  and `/token` (`grant_type=urn:ietf:params:oauth:grant-type:device_code`).
- Errors while polling: `authorization_pending` (keep waiting),
  `authorization_declined`, `expired_token`.
- The account email is parsed from the `id_token` JWT payload
  (`preferred_username`).
- Refresh tokens for personal accounts are long-lived; access tokens last
  ~1 hour → **always refresh transparently before expiry**.

## 4. Two Token Families (Exchange vs Graph)

An access token is audience-bound. `outlook.office.com` scopes (IMAP/SMTP
XOAUTH2) and `graph.microsoft.com` scopes (REST) produce **different tokens**.
Fleet servers store both, keyed per family:

| Family | Scopes | Used for |
|--------|--------|----------|
| `exchange` | `https://outlook.office.com/IMAP.AccessAsUser.All https://outlook.office.com/SMTP.Send offline_access` | imaplib/smtplib XOAUTH2 |
| `graph` | `https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.Send offline_access` | Microsoft Graph REST (`/me/...`) |

Token store (email-mcp): `data/oauth_tokens.json` (gitignored), key
`account|family`, refresh-on-read, thread-safe (RLock).

## 5. XOAUTH2 SASL (Exchange path)

```
user=<email>\x01auth=Bearer <access_token>\x01\x01
```

- IMAP: `imaplib.IMAP4_SSL(...).authenticate("XOAUTH2", lambda _: auth_bytes)`
- SMTP: `smtplib.SMTP(...).starttls(); server.auth("XOAUTH2", lambda _: auth_str)`
- Fallback chain in email-mcp: XOAUTH2 if a token exists → password login
  otherwise → clear error. Services report "not ready" when neither is available.

## 6. Microsoft Graph Path (recommended)

Graph is more robust than IMAP for Microsoft mail: no protocol quirks, richer
metadata, simpler auth (plain Bearer header).

| Operation | Graph endpoint |
|-----------|----------------|
| Send | `POST /v1.0/me/sendMail` (`saveToSentItems: true`) |
| List inbox | `GET /v1.0/me/mailFolders/{folder}/messages?$top=N&$orderby=receivedDateTime desc&$filter=isRead eq false` |
| Read | `GET /v1.0/me/messages/{id}` |
| Search | `GET /v1.0/me/messages?$search="query"` |
| Move | `POST /v1.0/me/messages/{id}/move {"destinationId": "folder"}` |
| Delete | `DELETE /v1.0/me/messages/{id}` (soft → deleteditems) |
| Mark read | `PATCH /v1.0/me/messages/{id} {"isRead": true}` |
| Folders | `GET/POST/DELETE/PATCH /v1.0/me/mailFolders` |

Well-known folder ids: `inbox`, `sentitems`, `drafts`, `deleteditems`,
`junkemail`, `archive`. Auth header: `Authorization: Bearer <token>`; on 401/403
the client must say "reconnect OAuth", not retry.

## 7. Fleet Integration (email-mcp)

- `src/email_mcp/oauth.py` — device flow, token store, XOAUTH2 strings,
  per-family tokens.
- `src/email_mcp/services/graph_service.py` — GraphEmailService implementing the
  standard EmailService interface (all 39 MCP tools work with `service="graph"`).
- REST: `POST /api/oauth/device` (body `{"scope": "exchange"|"graph"}`),
  `POST /api/oauth/poll`, `GET /api/oauth/status` (per-family state).
- Webapp: **Settings → Outlook OAuth** card — scope selector, Connect button,
  live user code + verification link, per-family authorized chips.
- Env: `EMAIL_MCP_OAUTH_CLIENT_ID`, optional `EMAIL_MCP_OAUTH_SCOPE`,
  `EMAIL_MCP_OAUTH_TOKEN_FILE`, `GRAPH_USER` (defaults to IMAP_USER/SMTP_USER).
- A `graph` service auto-registers when the client ID is set.

`onenote-mcp` shows the alternative: pure MSAL (`msal>=1.24`), Graph Explorer
client ID, same device-code UX, token file, Graph `notes.readwrite` scopes.

## 8. What Costs What

| Item | Cost |
|------|------|
| Entra app registration | **Free** (free tier) |
| Device-code OAuth + token refresh | **Free** |
| Microsoft Graph API (mail, calendar, OneNote, contacts, tasks) | **Free** (within limits) |
| Azure OpenAI / storage / compute | Paid (separate subscription, never required for auth) |
| Entra P1/P2 (some admin features) | Paid license, not needed for app registrations |

## 9. Troubleshooting

| Symptom | Fix |
|---------|-----|
| `5.7.139` on send | Personal account: basic auth gone — use OAuth (exchange or graph family). M365: admin must enable SMTP AUTH |
| IMAP `AUTHENTICATE failed` | Same policy; or "Let devices and apps use IMAP" toggle; or use Graph family |
| Device flow polls forever | User must complete consent at microsoft.com/devicelogin before the code expires (15 min) |
| `AADSTS70011` / invalid scope | Scope string typo — copy the exact URLs from §4 |
| Graph 401 after a while | Refresh token expired/revoked — re-run the device flow (clear the stored token) |
| Consent screen not appearing | "Allow public client flows" off, or wrong account type in the registration |
| `authorization_declined` | User declined — restart the flow |

## 10. Future

- Shared fleet `office365-auth` module (extract oauth.py + graph_service.py into
  a reusable package) so every Microsoft-facing server (email, onenote, calendar,
  contacts, tasks) uses one consent + one token store.
- Webhook-style Graph change notifications (`/me/messages` delta) as a
  replacement for IMAP polling watchers.
