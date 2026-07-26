# fleetwatcher-mcp

Internal fleet pulse — monitor repos, builds, sessions, and topology.

## Tools

| Tool | What it does |
|------|-------------|
| `fleet_pulse` | Monitor repo activity (recent commits, dirty state, sentinels) |
| `build_watch` | Parse BUILD_LOG.md across the fleet for NSIS build outcomes |
| `session_scan` | Search and browse agent session documentation |
| `fleet_graph` | MCP server dependencies and live port mapping |
| `fleetwatcher_help` / `fleetwatcher_status` | Help and health |

## Quick Start

```powershell
.\start.ps1
```

Starts backend on port 10947 and Fleet Pulse dashboard on port 10948.

## Config

Environment variables: see `llms-full.txt`.

## Ports

- 10918: backend (FastMCP HTTP + REST)
- 10919: Fleet Pulse dashboard (Vite + React)
