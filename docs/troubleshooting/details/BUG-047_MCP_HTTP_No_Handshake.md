# BUG-047: Hand-rolled MCP HTTP clients skip the `initialize` handshake

**Severity:** P1
**Date:** 2026-09-25
**Component:** Fleet-wide — any code that POSTs raw `{"jsonrpc":"2.0","method":"tools/call",...}` to an MCP server's `/mcp` HTTP endpoint instead of using a real MCP client library.

## Symptom

A hand-rolled `httpx`/`aiohttp`/`requests` POST straight to `http://host:port/mcp` with `method: "tools/call"` gets rejected by live FastMCP 3.x servers: HTTP 307 redirect to `/mcp/`, 404, or 405. The call silently never works — no exception surfaces the real cause unless the caller inspects the status code, and many of these connectors swallow the failure (log-and-continue, or a fallback path that masks it, e.g. calibre-mcp's client falling back to an in-process function call).

## Root cause

The MCP Streamable HTTP transport requires a session handshake before any `tools/call`:
1. POST an `initialize` request first.
2. Capture the `Mcp-Session-Id` response header and send it back on every subsequent request.
3. Send `Accept: application/json, text/event-stream` on every request (not just `Content-Type: application/json`).
4. (Recommended) POST a `notifications/initialized` notification after `initialize` succeeds.

Code that skips straight to `tools/call` with none of the above is not speaking the protocol — it happens to look like JSON-RPC but the server has no session context and rejects it outright.

## First found in

`robofang`'s `MCPBridgeConnector` (`src/robofang/core/tool_router.py`). Fixed by switching to `fastmcp.Client`, which performs the full handshake internally (commits `ebd75c1`, `2dff03f`).

## Fleet audit (2026-09-25)

Grepped `D:\Dev\repos` for `"method": "tools/call"` / `jsonrpc` construction (~78 matches incl. `mcpb/` packaged duplicates). Confirmed-broken production files (no `initialize`, no session id, and/or missing `Accept` header):

- `meta_mcp/src/meta_mcp/services/dynamic_router.py`
- `meta_mcp/src/meta_mcp/services/capability_router.py`
- `meta_mcp/src/meta_mcp/services/dynamic_router_service.py`
- `fleet-agent-mcp/src/fleet_agent/coworker/surveillance_watch.py`
- `fleet-agent-mcp/src/fleet_agent/mcp/tools/github.py`
- `fleet-public-relations-mcp/src/fleet_public_relations_mcp/publish_handoff.py` (`notify_discord`)
- `mcp-federation-hub/bridge/app/main.py`
- `dark-app-factory/blocks/mcp_client/backend/client.py`
- `speech-mcp/src/speech_mcp/providers/voicestudio.py`
- `veogen/backend/app/services/mcp_media_service.py` (also wrong endpoint path: `/jsonrpc` instead of `/mcp`)
- `nekomimi-mcp/src/nekomimi_mcp/renderers/boomy.py`
- `calibre-mcp/webapp/backend/app/mcp/client.py` — broken but currently masked by an in-process fallback, so it "works" by bypassing MCP entirely, not by speaking the protocol correctly. Lower urgency (dead-code correctness, not a live outage) but still worth fixing.

Files confirmed to already do the handshake correctly (reference examples for any future fix):
- `vienna-life-assistant/web_sota/vienna_life_assistant/fleet_mcp.py` — manual handshake, caches `mcp-session-id` per server in a `_SESSIONS` dict.
- `qcad-mcp/src/qcad_mcp/server.py` (`_blender_rpc`) — manual handshake, session captured and replayed.
- `obsidian-mcp/plugin-fleet-hub/main.ts` — TS client, `initialize()` method with re-init retry on missing session.
- `devices-mcp/src/devices_mcp/mcp_client.py`, `ednaficator/ednaficator/mcp/stdio_client.py`, `myai/core/shared/mcp_client/connection.py` — stdio transports, explicit `initialize()` before use.
- `meta_mcp/src/meta_mcp/tools/smoke_test.py` (+ mcp-studio copies) — stdio subprocess, correct manual sequence.

`fleet-agent-mcp`'s self-referential calls (`coworker/tasks.py`, `mcp/tools/contribute.py`, and its `scripts/*.py` dev tools) target its own server, which is `stateless_http=True` — these may work without a formal handshake against that specific server and were left unmodified pending a live test rather than assumed broken.

## Fix pattern

Prefer `fastmcp.Client(url)` (handles handshake, session, and Accept header automatically) over hand-rolled HTTP. Where a dependency on `fastmcp` isn't wanted, the manual pattern used correctly in `vienna-life-assistant/fleet_mcp.py` is the fleet reference: send `initialize`, capture `Mcp-Session-Id`, send `notifications/initialized`, then attach the session id and `Accept: application/json, text/event-stream` header to every later request.

## SOTA impact

New MCP HTTP clients must not be hand-rolled without the initialize/session/Accept sequence — see `standards/AGENT_PROTOCOLS.md` (client-side MCP guidance to be cross-linked here once added). Repo-by-repo fixes tracked in this file; do not blind-sweep — each repo committed and verified separately, max 5 files per commit per `GIT_REPOSITORY_SAFETY.md` / global Batch Size Limit rule.

## Status

🔧 Root-caused, confirmed-broken list above; fixes applied repo-by-repo (see commit hashes added here as each lands). Not pushed without explicit approval per session instructions.
