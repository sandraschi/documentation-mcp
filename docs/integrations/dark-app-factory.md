# Dark App Factory

**Software factory for the rest of us.** Vibe -> Foreman -> Council of 19 Specialists -> generated app. Local-first (Ollama, DeepSeek). Inspired by StrongDM Factory; free tier.

## Integration points

| Aspect | Detail |
|--------|--------|
| **Repo** | `D:/Dev/repos/dark-app-factory` |
| **Dashboard** | http://localhost:8002 (SOTA build progress, specialist status) |
| **DTU** | http://localhost:8001 (Digital Twin mocks: Stripe, Auth, Email, etc.) |
| **Foreman MCP** | Claude Desktop: `uv --directory D:/Dev/repos/dark-app-factory run foreman` |

## Fleet

- **Fleet registry**: Listed as `dark-app-factory` (category Dev, port 8002). Installable/launchable from robofang hub.
- **meta-mcp**: See `dark-app-factory/docs/META_MCP_INTEGRATION.md` for agent lifecycle (start factory, foreman, worker, judge) and DTU-as-MCP ideas.

## Ports

- 8002: Web dashboard (outside 10700–10800; factory default).
- 8001: DTU mock server.

## Quick start

```powershell
cd D:\Dev\repos\dark-app-factory
.\start_factory.ps1
```

Then open http://localhost:8002. Define a vibe in `vibe.md`, enrich with `python foreman.py enrich --vibe vibe.md`, then run the factory from the dashboard or `python factory.py run`.
