# 06 - Operations and Security

Source: upstream `README.md` connections/auth sections, `.env.example`,
`docker-compose.yml`, `DEPLOYMENT.md`, `docs/mcp.md`, `SECURITY.md`.

## 1. RBAC and tokens

* SSO supported; IdP redirect URI = `APP_URL/api/auth/sso/callback`.
* API tokens: UI user menu -> API Tokens -> New (name + optional expiry, shown
  once, SHA-256 stored). Send as `x-api-key` (or `Authorization: Bearer` for
  `auto_ontology_...` tokens). Acts as its owner - viewer token cannot do admin
  things. Whole `/api/...` surface accepts it (resolved in
  `frontend/auth/resolve-user.ts`). Revocation immediate (delete token or
  ban user -> 401). Tokens cannot create/revoke tokens (needs session).
* MCP OAuth: app is the authorization server, clients auto-register, grants in
  DB (replica-shared, restart-safe). Per-call permission check. `openid` scope
  required (Better Auth UserInfo). Check per call: expiry, revocation, client,
  session state.
* Write perms to know: `connection:manage` (add connection), `catalog:read`
  (list DBs), `catalog:edit` (glossary writes), `modelInterchange:export/import`,
  `semanticCompilation:manage` (reset), `chat:use` + `conversation:write` (chat
  with thread). 403 = role lacks perm, not wrong URL.

## 2. Connection secrets (sharp edge)

Two sources, only one active: UI-managed connections win when ANY exist,
`CONNECTION_STRINGS` (comma-separated, deploy-time) is fallback only
(`GET /api/connections/source` reports set-ness, carries no schema/table filters).

* Without Vault: full connection object incl. password JSON-serialized UNENCRYPTED
  on the catalog DB row.
* With Vault: creds in Vault keyed by DB name (no separate ref field), row holds
  none. Enabled ONLY when `VAULT_ADDR` + `VAULT_NAMESPACE` + `VAULT_ROLE_ID` +
  `VAULT_SECRET_ID` are ALL set (`VAULT_AUTH_MOUNT`, `VAULT_KV_MOUNT` optional
  overrides). Partial = warning + plaintext fallback. Off by default.

Fleet rule: never run a trial with real creds and Vault off. Use scratch DBs or
refuse.

## 3. Network boundaries

* Public: Next.js `:3000` (UI + `/api/...` gateway + OAuth discovery). This is
  what `AUTO_ONTOLOGY_API_URL` and clients point at. MCP public origin
  `AUTO_ONTOLOGY_MCP_PUBLIC_URL` (default :3003) must EXACTLY match the
  client-used URL incl. `/mcp` suffix (`127.0.0.1` vs `localhost` mismatch is a
  known login killer).
* Internal only: FastAPI `:3001` (trusts `x-auto-ontology-user-id`, no independent
  verification - direct `conversation_id` use requires that header), ingestion
  `:3002`, Postgres `:5432`. Firewall :3001 from other machines, especially in
  `--ds` dev mode (binds 0.0.0.0 for container reachability).
* Secrets hygiene: values file / `.env` in an editor, `chmod 600`, out of git and
  shell history. Never paste into chat. Required secrets: `AUTH_SECRET`,
  `APP_URL`/`appUrl` (exact browsed origin), `POSTGRES_PASSWORD`,
  `DEFAULT_MODELS_API_KEY`, admin email/password. `authSecret` persists across
  Helm upgrades once generated.

## 4. Artifacts and maintenance

* Releases: NGC `nvidia` org - images `nvcr.io/nvidia/auto-ontology`,
  `-frontend`, `-mcp`; Helm chart at `helm.ngc.nvidia.com/nvidia`. Chart pins
  images to chart version. `helm uninstall` deletes the postgres-data PVC too.
* Vendored clone: shallow `--depth 1` at `external/nvidia/auto-ontology`.
  Refresh with `git pull` + record new HEAD. No fleet commits inside. Port code
  out only after `LICENSE` / `THIRD_PARTY_NOTICES.md` /
  `CONTAINER_THIRD_PARTY_NOTICES.md` check (bundled/linked OSS enumerated there).
* Upstream accepts no external contributions; do not open PRs. Security issues
  follow `SECURITY.md`. Maintainer workflow is `CONTRIBUTING.md` (informational
  for fleet - do not follow it with fleet changes).
* Runtime notices: external materials (hosted NIM APIs, configured
  OpenAI-compatible endpoints, KumoRFM when keyed, source DBs) governed solely
  by their own terms. Verify security/suitability per use case. Software AS IS.
