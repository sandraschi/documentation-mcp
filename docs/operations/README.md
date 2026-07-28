# Fleet Operations

**Prerequisites:** `docs/core/`, familiarity with at least one fleet MCP server

Operational reference for the 136+ repo fleet: ports, control plane, deployment infrastructure, and runbooks.

## Files

| File | Purpose |
|------|---------|
| `WEBAPP_PORTS.md` | **Port registry** — every repo's frontend and backend ports (10700-11500 range) |
| `VIBE_OPERATIONS.md` | Live infrastructure status and operational notes |
| `MCP_SERVER_SAGA_INDEX.md` | Fleet migration war stories — upgrades, bugs, lessons learned |
| `DOCS_MCP_MAAS.md` | Using this server as a shared RAG service for other repos |
| `DEVELOPER_LINGO.md` | Shared dev shorthand used across the fleet |
| `FLEET_EXECUTION.md` | Fleet-wide execution and orchestration patterns |
| `A2A_FLEET_ROLLOUT.md` | Agent-to-Agent protocol rollout status |
| `HERE_NOW_STATIC_PUBLISHING.md` | Static URL publishing for agent-built pages |

## Key operations

- **Find a port:** `WEBAPP_PORTS.md` — search by repo name
- **Check if a server is alive:** `http://localhost:{port}/health`
- **Start a webapp:** Use fleet `starts/*-start.bat` launchers (private MCD) or each repo's `web_sota/start.ps1` / `start.ps1`
