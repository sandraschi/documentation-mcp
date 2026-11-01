# Troubleshooting

## "Not signed in" everywhere

Run the device-code flow again: Settings > Sign in with Microsoft, enter the
code, approve all scopes. If it still fails, delete the stale token file:

```powershell
Remove-Item "$env:LOCALAPPDATA\ms-graph-mcp\tokens.json"
```

## Device flow: "authorization_declined" or code does not complete

The user denied consent or used the wrong account. Re-run
`auth_ops(operation="login")` and approve **all** requested permissions.

## Calendar/Tasks/Contacts/Drive pages load but are empty

- Not signed in yet -> do the sign-in (pages legitimately show empty/MOCK
  state until then).
- Signed in but empty: the account has no data in that surface, or a scope
  was denied at consent. Re-consent with the full `MSG_SCOPES` list.

## Backend health OK but the frontend shows Offline / CORS errors

- Check the frontend port: the webapp must be on 11148 and the backend on
  11149 (see docs/CONFIGURATION.md). The Vite dev proxy forwards `/api` and
  `/mcp` to 11149.
- `start.ps1` clears zombie listeners on both ports first; if something else
  grabbed 11149, `Get-NetTCPConnection -LocalPort 11149` shows the owner.

## rate_limit errors

Graph throttles ~10,000 requests per 10 minutes per app. Wait ~60s, then
retry with a smaller range (`limit`/date window). The webapp polls every
10-30s which is well within limits.

## 401 / "auth" errors from a tool that just worked

The refresh token may have been rotated out from under the process (e.g. the
webapp refreshed while stdio was connected). The client retries once with a
forced refresh; if it still fails, run login again.

## "MCP tool not found" in the client

FastMCP registers tools at import time. If `uv run python -m
ms_graph_mcp.server` prints errors or the client shows fewer than 8 tools,
check the server log; `GET /api/v1/diagnostics` lists what is registered.

## Chat page: "No local LLM detected"

The chat uses a local Ollama at 127.0.0.1:11434 (fleet default). Install
Ollama and pull a model (e.g. `ollama pull qwen2.5:7b`), then reload the
page. Chat is optional - the rest of the app works without it.

## Work/school account sign-in fails

This server targets personal accounts (consumers authority). M365 work
tenants are rejected by design - Teams/SharePoint/Entra admin are out of
scope. If you need Teams, see PARKING_LOT.md ("teams-mcp (business accounts
only)").

## Still stuck

```powershell
uv run python -m ms_graph_mcp.server   # watch stderr for the real error
```

Full stack logs go to stderr (and the Tauri log dir in packaged builds).
