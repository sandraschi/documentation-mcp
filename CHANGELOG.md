# Changelog

## 1.1.0 (2026-07-05)

### Added
- Zustand store (`src/lib/store.ts`) for shared app state (sidebar, backend health)
- Playwright E2E tests (`web_sota/e2e/`) — backend health, diagnostics, frontend load, console errors, dashboard KPIs, tools hub
- CI workflow (`.github/workflows/ci.yml`) — ruff lint, tsc typecheck, pytest
- `.pre-commit-config.yaml` — ruff + biome pre-commit hooks
- `.claude-plugin/plugin.json` + `hooks/hooks.json` — SessionStart context injection for Claude Code
- `GET /api/v1/diagnostics` endpoint (required by CUA-NSIS smoke test)
- `.cursorrules` for Cursor session context

### Fixed
- LLM model discovery: wrong API URL paths in frontend (`/api/ollama/models` → `/api/models/ollama`), tuple unpacking bug in LM Studio endpoint
- start.ps1: backend crash detection (stderr capture to log, `$proc.Refresh()`, TIME_WAIT drain, abort on failure instead of silent continue)
- start.ps1: `Resolve-FleetPortConflict` called before `FleetStartMode.ps1` was sourced (ordering bug)
- start.ps1: npm is a `.ps1` script, not an exe — `Start-Process` now uses `powershell.exe` as `FilePath`
- cua-nsis-config.json: backend port (10795 → 11033), health path, diagnostics path
- Backend spec: `.dist-info` preservation for fastmcp/prefab_ui (was using broken `copy_metadata` workaround)
- `api/tools` endpoint: used `mcp._tool_manager` (removed in FastMCP 3.4) — now uses `mcp.list_tools()`
- Persistence page: replaced technobabble ("long-horizon context retention", "policy-based guardrails") with honest factual description
- B904 lint errors across all API modules (raise from e)
