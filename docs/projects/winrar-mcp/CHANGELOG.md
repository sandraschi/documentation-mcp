# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed (2026-07-18, assfix pass)
- **CORS**: `allow_origin_regex` was gated behind `WINRAR_TAURI` env var, silently
  breaking LAN/Tailscale access to the webapp for anyone not running the Tauri
  shell. Now unconditional, covers `tauri.localhost` plus private LAN and
  Tailscale CGNAT ranges.
- **justfile**: added `build-native`, `mcpb-pack`, `cua-nsis-test`, and
  `gates-green` targets — previously only reachable via the all-in-one `release`
  target, which meant a build-only or test-only pass required manual flag-juggling.
- **Tracked `.bak` dross**: removed 4 tracked `start.ps1.bak.*` files (already
  covered by `.gitignore`, just never untracked).
- **Webapp**: added the mandatory `useZoom()` hook (Ctrl+Scroll to zoom, Ctrl+0 to
  reset, persisted to `localStorage`, CSS `zoom` fallback for dev-browser use) —
  was completely absent.

### Known issue (not fixed this pass, needs manual disambiguation)
- The NSIS-installed build's app process exits within ~1s of launch when started
  from a non-interactive automation session (winops), with no crash event logged
  and no write to its own `backend-spawn.log`. Resource path structure was
  verified correct. Root cause not confirmed — may be a genuine bug, or may be an
  artifact of launching without an interactive desktop session (see
  `docs/assess-reports/2026-07-18.md`). Needs a manual launch from a real desktop
  session to confirm before further investigation.

### Fixed
- **start.ps1**: Fixed broken references (`web_sota/` → `webapp/`, `winrar_mcp` → `winrarmcp`)
- **CLAUDE.md**: Replaced 10 stale tool names with actual 17-tool surface
- **llms.txt**: Removed stale `winrar_archive` portmanteau reference, replaced with individual tool list
- **CORS**: Replaced `["*"]` with fleet-standard origins + regex in both `webapp/api.py` and `transport.py`
- **Default port**: Changed default from 8000 to 10762 in `config.py` and `.env.example`
- **Docstrings**: Removed deprecated `Args:` blocks from `status.py`, `help.py`
- **E501**: 43 line-length violations expedited with noqa annotations

### Added
- `.opencode/skills/session-context/SKILL.md` — opencode session context injection

### Security
- **CRITICAL: .env leak fixed** — `tauri.conf.json` now bundles `.env.example`, not `.env`. `build.ps1` copies `.env.example` only. Personal API keys no longer shipped in NSIS installer.

### Added (prior)
- `/api/v1/diagnostics` endpoint with tool count, version, uptime (CUA smoke test support)
- `/health` endpoint upgraded with `server`, `version`, `uptime_seconds`, `tool_count` fields
- `CLAUDE.md` at repo root with session context injection
- `@tauri-apps/api` dependency in webapp for Tauri event listening
- `tauri.conf.json` now has `beforeDevCommand` and `beforeBuildCommand`
- Dual transport in `run_server.py`: `WINRAR_PORT` env → HTTP, fallback → stdio
- Tool annotations (`READ_ONLY`/`MUTATING`) on all 17 MCP tools
- All tool docstrings migrated from `Args:` to `Annotated[T, Field(description=...)]` pattern
- Tauri CORS origins in `main.py` (`tauri://localhost`, etc.)

### Fixed
- `build.ps1` orphaned `-ForegroundColor` syntax error
- `backend.rs` upgraded to fleet standard: image-name kill, UAC elevation fallback at 15s, 240s port-free poll, piped stderr capture
- `main.py` CORS now includes Tauri-specific origins
- `glama.json`: FastMCP 2.10 → 3.4.2, tools 6 → 20
- `mcpb.json`: corrected entry point and dep constraint
- `llms-full.txt`: portmanteau docs → actual individual tool signatures
- `Cargo.toml`: added `features = ["tray-icon"]`
- `justfile lint`: targets `webapp/` instead of retired `web_sota/`

### Removed
- 10 stale `.bak` files across repo
- Dead `web/` and `web_sota/` frontend scaffolds (3 → 1 frontend directory)

## [0.3.1] - 2026-04-09

### Added
- **Industrial Testing Scaffold** — migrated from ad-hoc scripts to professional `pytest` suite with shared fixtures (`conftest.py`)
- **Tool Verification Suite** — added `tests/test_mcp_tools.py` for direct verification of FastMCP tool handlers and pydantic input validation
- **Testing Justfile Recipes** — added `test`, `test-cov`, and `test-failed` recipes to the industrial dashboard
- **Coverage Config** — added industrial-grade coverage standards to `pyproject.toml`

### Fixed
- **RUF006 (Async Safety)** — implemented `_background_tasks` set in `webapp/api.py` to prevent premature garbage collection of background archive processes
- **B006 (Mutable Defaults)** — resolved mutable default arguments in `ArchiveService` constructor
- **B904 (Exception Chaining)** — enforced explicit exception chaining in `archive.py` for improved debuggability
- **E501 (Format)** — applied surgical line breaks in `mcp_server.py` to comply with SOTA v13.1 linting standards

## [0.3.0] - 2026-04-09

### Added
- **Webapp dashboard** — full SOTA React/Vite frontend (port 10763) with Starlette backend (port 10762)
- **Repo Archiver page** — scans `D:\Dev\repos`, reads `.gitignore` per repo, translates patterns to WinRAR `-x` exclusion flags, async job runner with live progress polling
- **Archive Browser page** — path input → list files, full info (`UnRAR l -v`), integrity test, extract-to with job polling
- **Compression Lab page** — runs RAR5 m1/m3/m5 analysis in temp dir, renders bar chart + table with ★ best recommendation
- **Jobs page** — auto-refreshing 3 s poll, running/completed split, JSON result detail panel
- **Status page** — live backend health, env var reference
- **gitignore → WinRAR exclusion translator** (`webapp/api.py`) — handles directory-only patterns, path-relative patterns, simple globs; skips negation lines with explanation
- **Async job store** — in-memory job tracking with start/finish timestamps and error capture
- **`start.ps1` / `start.bat`** — kills port zombies, creates venv, installs deps, waits for backend readiness, opens browser
- **Design** — dark ink+amber palette, DM Mono / IBM Plex Sans / JetBrains Mono typography, collapsible sidebar, Framer Motion transitions, toast notification stack

### Changed
- Replaced placeholder `web_sota/` scaffold (mock data, no API calls) with functional `webapp/` directory
- Ports clarified: backend **10762**, frontend **10763** (were reversed in old README)

### Technical
- Backend: Starlette + uvicorn, no FastAPI dependency
- Frontend: React 18 + Vite 5 + Tailwind CSS 3 + Zustand + Framer Motion + Lucide React
- All archive operations delegate to `Rar.exe` / `UnRAR.exe` subprocesses via `asyncio.create_subprocess_exec`

### Changed
- **FastMCP 3.1**: Upgraded from FastMCP 2.x to 3.1. Separate FastAPI app with MCP mounted at `/mcp` via `mcp.http_app()`. Constructor uses identity/instructions only; transport (host, port, log_level) passed to `run()`/`http_app()`. Lifespan replaces deprecated `on_event` startup/shutdown.
- **Platform Support**: Marked as Windows-only due to WinRAR dependency
- **Development Status**: Updated to Beta classification
- **Documentation**: Added Windows-specific badges and requirements; README and docs/mcp-technical updated for FastMCP 3.1

### Added
- **CI/CD Pipeline**: Comprehensive GitHub Actions workflow with:
  - Code quality checks (ruff formatting, linting, mypy)
  - Multi-platform testing (Python 3.10, 3.11, 3.12)
  - Security scanning (bandit, safety)
  - Automated releases on version tags
- **Pre-commit Hooks**: Automated code quality checks with:
  - Ruff linting and formatting
  - MyPy type checking
  - Security scanning
  - Import sorting and file checks
- **Development Scripts**: Setup scripts for easy development environment configuration
- **Advanced Archive Tools**: 6 new intelligent tools for archive management:
  - `analyze_compression_efficiency`: Compression analysis and optimization
  - `batch_archive_operations`: Parallel batch processing
  - `compare_archives`: Archive comparison and diff analysis
  - `smart_archive_backup`: Intelligent backup with versioning
  - `archive_health_monitor`: Health monitoring and repair
  - `secure_file_operations`: Secure deletion and compliance
- **FastMCP 3.1**: Full alignment with FastMCP 3.1 (conversational tool returns, sampling; HTTP at `/mcp`)
- **Enhanced Documentation**: CONTRIBUTING.md with development guidelines

### Changed
- **Code Quality**: Major improvements with ruff formatting and linting
- **Tool Documentation**: Updated to FastMCP 3.1 conversational standards
- **README**: Enhanced with development setup and CI/CD information

### Fixed
- **Syntax Errors**: Fixed f-string parsing issues and code formatting
- **Import Organization**: Sorted and cleaned up import statements
- **Type Hints**: Improved type annotations throughout codebase

### Technical Improvements
- **Test Coverage**: Added comprehensive test suite structure
- **Security**: Implemented security scanning and vulnerability checks
- **Performance**: Optimized archive operations with parallel processing
- **Maintainability**: Improved code organization and documentation

## [0.1.0] - 2025-01-19

### Added
- Initial release of WinRAR MCP server
- Basic archive creation, extraction, and management tools
- FastMCP 2.13+ compliant implementation
- Windows-specific WinRAR integration
- Core MCP functionality with help and status tools

### Features
- Create archives with compression and encryption
- Extract archives with various options
- Add/remove files from existing archives
- Archive information and content listing
- Basic archive testing and integrity checks
- Repository archiving with automatic exclusions