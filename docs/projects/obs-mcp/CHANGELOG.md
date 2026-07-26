# Changelog

All notable changes to the OBS Studio MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - Unreleased

### Added
- Tauri 2.0 native wrapper with `bundle.resources` + `std::process::Command`
- PyInstaller frozen backend embedded in NSIS installer
- CUA-NSIS smoke test (`scripts/cua-smoke.py`, `scripts/cua-nsis-config.json`) and `just cua-nsis-test` recipe
- Tauri CORS: `tauri://localhost` origins for WebView API access
- `GET /api/v1/diagnostics` endpoint for CUA verification
- `CHANGELOG_LATEST.md` (fleet convention: latest release notes only)

### Changed
- **Truth pass across all metadata**: single version (1.6.0) in pyproject, manifest.json, glama.json, FastMCP app, and webapp; all repository URLs corrected to the actual remote (`sandraschi/obsmcp`)
- `manifest.json` tool list regenerated from the actual 36 registered tools (was 18 stale/wrong names)
- `glama.json` corrected: 36 tools, stdio/http/sse transports (was 12 tools, stdio-only)
- `obs_help` now introspects the live FastMCP tool registry instead of a hardcoded (and wrong) 17-entry table
- Server `instructions` corrected to reference real tool names (`obs_agentic_workflow`, `obs_production_assistant`)
- README rewritten from code: accurate tool tables, Python 3.12+ everywhere, MCPB packaging via `bunx` (fleet Bun standard), webapp section points at `web_sota`; removed fictional PyPI install path and nonexistent `requirements.txt` reference
- INSTALL.md: fixed broken module paths (`obs_mcp` → `obs_studio_mcp`), corrected ports
- pyproject: `ruff` moved out of runtime dependencies; dead setuptools block removed; mypy targets 3.12
- CI: runs on push/PR (was tags-only), Python 3.12/3.13 matrix (3.10/3.11 could not install under `requires-python >=3.12`), uv-based, Biome CI job for web_sota

### Removed
- Legacy `mcpb/` duplicate source tree (full second copy of the package **with committed .pyc bytecode**) — packaging now stages from the real `src/` via mcpb CLI + `.mcpbignore`
- ~40 generic fleet-template docs (Glama/Serena/MCPB/debugging guides) — canonical home is mcp-central-docs
- Committed `.bak` backup files (13), `web_sota/package-lock.json` (Bun is the fleet package manager), `eslint.config.js` (Biome migration completed)

## [1.5.0] - 2026-04-14

### 🚀 Industrialization & Stage Automation
- ✨ **FastMCP 3.2.0**: Full protocol modernization and conversational logic stabilization
- ✨ **OSC Orchestration**: Added multi-target OSC sending and listening capabilities
- ✨ **Connection Targets**: New management system for OBS and OSC destination nodes
- 🎨 **web_sota Evolution**: Migrated toolchain from ESLint/Prettier to Biome; added Connection Targets page; optimized glassmorphism UI for multi-node control
- 🛡️ **Protocol Hardening**: Purged legacy `print()` statements for RPC integrity; standardized error handling with `contextlib.suppress` and `B904` chaining

### 🔧 Technical Improvements
- ✅ **OSC Manager**: Asynchronous OSC dispatcher with multi-target support
- ✅ **Tool Expansion**: Added `obs_send_osc` and `obs_list_targets`
- ✅ **Port Standardization**: Fleet ports locked to **10818** (Web) and **10819** (API)
- ✅ **Test Scaffold**: pytest suite for OSC logic verification

## [0.2.0] - 2025-12-21

### 🛠️ Code Quality & Maintenance
- ✅ **Ruff Linting**: Fixed all 44 linting issues (unused imports, variable shadowing, unused variables)
- ✅ **Pydantic V2 Migration**: `json_schema_extra`, `@field_validator`, `ConfigDict`, `update_forward_refs()` fixes
- ✅ **Code Formatting**: Consistent formatting across all files
- ✅ **Import Organization**: `status` import fixed (`fastapi` → `starlette`), redundant imports removed

## [0.1.0] - 2025-10-15

### ✨ Initial Release
- **FastMCP 2.13.0 Integration**: Full MCP protocol compliance
- **OBS WebSocket Support**: Streaming, recording, scene, audio, replay buffer, and virtual camera control
- **DXT Packaging**: Ready for MCP deployment environments
- **Docker Support**: Containerized deployment with multi-architecture builds
- **Configuration Management**: Flexible settings via Pydantic models
