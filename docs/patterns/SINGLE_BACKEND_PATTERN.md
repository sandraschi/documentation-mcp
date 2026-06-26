# Single-Backend Pattern (FastMCP 3.1 Webapps)

**Pattern:** One app serves both REST (for the UI) and MCP at `/mcp`. No separate bridge process.

## When to use

- Any MCP server that has a webapp (Webapp, webapp, or similar).
- You want the frontend to call tools and resources without running a separate bridge or proxy.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Frontend (Vite/React, port e.g. 10796)                         │
│  - Calls REST: GET /api/v1/tools, POST /api/v1/tools/call       │
│  - Optional: MCP-native client to /mcp (streamable HTTP)        │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP (REST or MCP)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Single Backend (FastAPI/Starlette, port e.g. 10797)             │
│  - REST routes: /health, /api/v1/* (list tools, call tool, …)   │
│  - MCP mount:   app.mount("/mcp", mcp.http_app())                │
│  - One process, one MCP instance: REST handlers use same `mcp`  │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation

1. **One FastAPI (or Starlette) app**
   - Define custom routes: `/health`, `/api/v1/tools`, `/api/v1/tools/call`, or whatever the UI needs.
   - Use a single `FastMCP` instance (e.g. in `mcp_app.py` or `server.py`).

2. **Mount MCP at `/mcp`**
   - `app.mount("/mcp", mcp.http_app())` so native MCP clients (IDE, CLI) can connect via streamable HTTP.

3. **REST handlers use the same MCP instance**
   - List tools: `await mcp.list_tools()`.
   - Call tool: `await mcp.run_tool(name, arguments)` (or equivalent 3.1 API).
   - No separate process; no bridge.

4. **Frontend**
   - Targets the backend base URL (e.g. `http://localhost:10797`).
   - Uses REST for the web UI (simple fetch/axios to `/api/v1/...`).
   - Does not need to speak MCP protocol unless you build an in-browser MCP client to `/mcp`.

## Benefits

- **No bridge:** One backend process; no extra Node/Python bridge to run or debug.
- **Single MCP instance:** REST and MCP share the same tools, prompts, and state.
- **3.1 compliant:** MCP is exposed via `mcp.http_app()` at `/mcp`; REST is just another way to invoke the same server.

## References

- [FASTMCP_3.1_ALIGNMENT.md](../operations/FASTMCP_3.1_ALIGNMENT.md) — “Use a single FastAPI app for custom HTTP routes; mount the MCP HTTP app at the required path.”
- [FLEET_RULE_FIX_EVERYWHERE.md](../operations/FLEET_RULE_FIX_EVERYWHERE.md) — Apply patterns across the fleet.
- Example: reaper-mcp (FastAPI + mount at `/mcp`, REST at `/api/v1/tools`).
