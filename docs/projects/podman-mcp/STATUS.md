# Podman MCP — Fleet Status

**Last reviewed**: 2026-07-26
**Version**: 3.5.0
**Repo**: `D:\Dev\repos\podman-mcp`

## Compliance Snapshot

| Standard | Status |
|----------|--------|
| FastMCP 3.5 | OK |
| Portmanteau tool pattern (9 tools, 70+ ops) | OK |
| Dual transport (stdio + HTTP) | OK |
| WEBAPP_SOTA (13 pages, AppLayout, dark theme) | OK |
| Local LLM glom-on (Ollama/LM Studio) | OK |
| Connection health store (Zustand) | OK |
| Ctrl+Scroll zoom (useZoom) | OK |
| data-testid on connection status | Partial (backend-dot exists, KPI cards missing testids) |
| Tauri native build (Windows NSIS) | Not yet (native/ directory not present) |
| CUA smoke test | Not yet (scripts/cua-smoke.py missing) |
| Diagnostics endpoint (`GET /api/v1/diagnostics`) | OK |
| Rootless mode detection | OK |
| 4 categorized error states | OK |
| MCPB packaging | OK (manifest.json at root) |
| CORS per fleet standard | OK |
| README fleet shape | OK |
| Port table in README | OK |
| llms.txt + llms-full.txt | OK |
| glama.json | OK |
| CHANGELOG.md | OK |
| AGENTS.md | OK |
| PRD.md | OK |
| .env.example | OK |
| Prefab UI (prefab-ui dependency) | Check (prefab-ui not in pyproject.toml) |
| Session context injection (.cursorrules) | Missing |

## Ports

| Role | Port |
|------|------|
| Frontend (Vite React SPA) | 11112 |
| Backend (FastAPI + MCP HTTP /mcp) | 11113 |

## Tools (9 portmanteau, 70+ operations)

| Tool | Ops | Notable |
|------|-----|---------|
| `manage_containers` | 12 | exec, files (in-container I/O), CPU/memory limits |
| `manage_pods` | 6 | Podman-unique, no Docker equivalent |
| `manage_images` | 6 | Pull, build, search, delete |
| `manage_system` | 14 | Machine lifecycle, generate_systemd, volumes, networks |
| `manage_compose` | 7 | Up/down/ps/logs/build/config/debug |
| `manage_backup` | 8 | Image/container/volume/compose save+restore |
| `manage_migrate` | 7 | Docker↔Podman porting — compose conversion, image migration |
| `manage_agentic` | 5 | Multi-step workflows with dry-run safety |
| `manage_health` | 3 | Restart loops, OOM, log analysis, recommendations |

## Webapp Pages (13)

Dashboard, Containers, Pods, Images, Volumes, Networks, Compose, Migrate (Docker↔Podman), AI Command, MCP Tools, Event Logs, Help, Settings

## Open Items

- Version tag needs bump to v3.5.0 in git (pyproject.toml already has 3.5.0)
- Tauri native directory not present — no NSIS build pipeline
- CUA smoke test not configured
- `prefab-ui` dependency not in pyproject.toml (Prefab UI not in use yet)
- `.cursorrules` missing — no session context injection for IDE agents
- `data-testid` on KPI cards not present (only backend-dot exists)
- `native/` directory not scaffolded
- GitHub release not created for v3.5.0
- `ventoy-mcp` duplicate ADN file in docs/adn-notes (SEP-1577-in-Docker-MCP...)
