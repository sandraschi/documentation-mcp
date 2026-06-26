# Docker MCP — fleet status

**Last reviewed**: 2026-06-02  
**Upstream version**: 3.3.0  
**Repo**: `D:\Dev\repos\docker-mcp`

## Compliance snapshot

| Standard | Status |
|----------|--------|
| FastMCP 3.3 | OK (`3.3.1` resolved) |
| WEBAPP_STANDARDS (`/logs`, settings LLM glom) | OK |
| MCPB root `manifest.json` v0.2 | OK (~229 KB pack) |
| Tauri native build (Windows) | OK (NSIS + MSI 3.3.0) |
| README fleet shape (~100 lines upstream) | OK |
| Legacy `mcpb/` folder | Removed |

## Ports

| Role | Port |
|------|------|
| Frontend (Vite) | 10806 |
| API bridge (uvicorn) | 10807 |

## Build artifacts (local)

- MCPB: `dist/docker-mcp-v3.3.0.mcpb`
- Tauri: `native/target/release/bundle/nsis/Docker MCP_3.3.0_x64-setup.exe`
- Sidecar: `native/binaries/docker-mcp-backend-x86_64-pc-windows-msvc.exe`

## Open items

- README Preview screenshots (WEBAPP_STANDARDS) — optional
- `DOCKER_MCP_PREFAB_APPS` env documented in CONFIGURATION; wire when needed
