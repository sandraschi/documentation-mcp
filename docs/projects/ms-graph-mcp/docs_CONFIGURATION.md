# Configuration

All settings are environment variables with the `MSG_` prefix, read via
`Settings.from_env()` (src/ms_graph_mcp/config.py). Copy `.env.example` to
`.env` and adjust. The `.env` file is loaded automatically when running via
the fleet start script; for bare `uv run`, export the vars in your shell.

| Variable | Default | Meaning |
|----------|---------|---------|
| `MSG_HOST` | `127.0.0.1` | Bind address for the HTTP backend |
| `MSG_PORT` | `11149` | Backend port (FastAPI + MCP at `/mcp`) |
| `MSG_CLIENT_ID` | *(empty)* | Azure app registration client id. Empty = Microsoft's public **Graph Explorer** client (zero setup, consent shows "Graph Explorer"). Set for a private revocable consent. |
| `MSG_SCOPES` | `User.Read,Calendars.ReadWrite,Tasks.ReadWrite,Contacts.ReadWrite,Files.ReadWrite,offline_access` | Delegated permissions requested at consent (comma separated). Keep `offline_access` for token refresh. |
| `MSG_TOKEN_PATH` | `%LOCALAPPDATA%\ms-graph-mcp\tokens.json` | Where the MSAL token cache persists |
| `MSG_GRAPH_BASE` | `https://graph.microsoft.com/v1.0` | Graph REST base URL (override for test fixtures) |
| `MSG_TIMEOUT_SECONDS` | `30` | HTTP timeout for Graph calls |
| `MSG_LOG_LEVEL` | `INFO` | Logging level |

## Auth modes

| Mode | `MSG_CLIENT_ID` | Consent screen | Revocable per-app | Setup |
|------|-----------------|----------------|-------------------|-------|
| **Graph Explorer** (default) | *(empty)* | "Graph Explorer" | No | None |
| **Private app** | your client id | your app name | Yes | ~5 min, free |

### Creating a private app registration

1. https://portal.azure.com > **Microsoft Entra ID** > **App registrations**
2. **New registration**: name `ms-graph-mcp`, supported account types
   **Personal Microsoft accounts only**, no redirect URI.
3. **Authentication** > Advanced settings > **Allow public client flows:
   Yes** (required for the device-code flow).
4. **API permissions** > Add permission > Microsoft Graph > Delegated:
   `User.Read`, `Calendars.ReadWrite`, `Tasks.ReadWrite`,
   `Contacts.ReadWrite`, `Files.ReadWrite`.
5. Copy the **Application (client) ID** into `MSG_CLIENT_ID`.

Personal accounts consent interactively during the device flow (the user is
their own admin). No admin approval, no billing.

## Why these scopes

| Scope | Unlocks |
|-------|---------|
| `User.Read` | profile card, photo |
| `Calendars.ReadWrite` | calendar list/create/update/cancel, free-slot search |
| `Tasks.ReadWrite` | To-Do lists and tasks |
| `Contacts.ReadWrite` | contacts CRUD |
| `Files.ReadWrite` | OneDrive list/read/upload/download/share |
| `offline_access` | refresh token - the server re-authenticates silently |

## Ports

| Port | Service |
|------|---------|
| 11148 | Webapp (Vite dev server) |
| 11149 | Backend (FastAPI REST + MCP streamable HTTP `/mcp`) |

Registered in `mcp-central-docs/operations/WEBAPP_PORTS.md`. Both are in the
fleet reservoir (10700-11500) and are cleared of zombies by `start.ps1`.
