# Docker MCP — fleet status

**Last reviewed**: 2026-10-03  
**Upstream version**: 3.5.0  
**Repo**: `D:\Dev\repos\docker-mcp`

## Compliance snapshot

| Standard | Status |
|----------|--------|
| FastMCP 3.5 | OK |
| WEBAPP_STANDARDS (/logs, settings LLM glom, help tabs) | OK |
| Tools hub (`/tools` + schema runner) | OK |
| Dashboard hero CTA + quick actions | OK |
| MCPB root manifest.json v0.2 | OK |
| Tauri native build (Windows NSIS) | OK (3.3.1-beta, CUA-certified) |
| README fleet shape | OK |
| CSP explicit with backend port | OK (pitfall #13 fixed) |
| Connection health store (zustand) | OK |
| Ctrl+Scroll zoom | OK |
| CUA smoke test (9 phases) | OK (pywinauto + OCR + nav click-through) |
| Docker triple kill recovery | OK (POST /api/docker/recover; dashboard Recover Docker) |
| Diagnostics endpoint | OK (GET /api/v1/diagnostics) |
| data-testid on connection status | OK |
| MCP Streamable HTTP live (`POST /mcp`, 43 tools) | OK 2026-10-03 |
| Reports page + junk endpoint (MD/JSON export) | OK 2026-10-03 |
| Compose files preload + fleet-root setting | OK 2026-10-03 |
| List/card + export on all list pages | OK 2026-10-03 |

## Ports

| Role | Port |
|------|------|
| Frontend (Vite) | 10806 |
| API bridge (uvicorn) | 10807 |

## Build artifacts (local)

- NSIS: `native/target/release/bundle/nsis/Docker MCP_3.3.1_x64-setup.exe`
- Backend: `dist/docker-mcp-backend.exe` (28.6 MB, PyInstaller onefile)

## Open items

- Version tag needs bump from 3.3.0 → 3.3.1 in pyproject.toml, tauri.conf.json
- GitHub release: `gh release create v3.3.1-beta dist/*.exe --title "Docker MCP 3.3.1-beta" --notes "See CHANGELOG.md"`
- CUA cert on remaining 13 built repos (CSP fix applied, need rebuild + test)
