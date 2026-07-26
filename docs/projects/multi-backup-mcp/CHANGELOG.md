# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2026-06-15

### Added
- **Python repo archiver upgrade to SOTA parity**: `git ls-files` file selection (source & docs only), SHA256 deduplication, 3 destinations (Desktop, N:, OneDrive), per-repo subdirectories, retry logic with exponential backoff, dry-run mode
- **CI pipeline**: `.github/workflows/ci.yml` — Windows-only, ruff lint + format + pytest
- **Smoke tests**: `tests/test_smoke.py` — import, git-tracked fallback, walk excludes, ZIP creation
- Repos router registered in server (`/api/repos/*` endpoints now live)
- `scan_repositories` excludes junk/external/hidden folders (mirrors `backup-all-repos.ps1` logic)
- `run_nuclear_backup` reports `skipped_count` for dedup'd repos

### Changed
- **Single code path**: MCP tools and webapp REST both use the same Python archiver (no PowerShell subprocess)
- `sota_tools.py` deprecated — stub pointing to `repo_tools`
- `DEFAULT_LOCATIONS` expanded from 2 to 3 destinations with OneDrive
- `list_repo_backups` now scans per-repo subdirectories at each destination
- Ruff config updated: security false-positives suppressed (S603/S104/S607/S108/S110/S112, RUF006)

### Fixed
- **Hasleo CLI confirmed working**: `BackupCmdUI.exe` v5.6.2.0 is installed and responds; 2 tasks configured (System Backup, File Backup). Integration was never broken — mocks were hiding a functional system.
- **Gaslighting removed**: `backup_tools.py` no longer returns mock data when Hasleo CLI is missing (returns empty list)
- **Gaslighting removed**: `backup_service._simulate_backup` replaced with honest `_mark_not_implemented` (fails immediately, no fake progress)
- **Gaslighting removed**: `integrations.py` Claude endpoints now return HTTP 501 instead of hardcoded fakes
- **Hardcode removed**: `/tmp/claude_backups` Linux path eliminated
- Circular import risk: `sota_tools.py` imported from `mcp_instance` not `fastmcp_server`
- `backup-all-repos.ps1` was passed `-WhatIf` (wrong flag) — fixed to `-DryRun`
- Ruff green: 85 auto-fixed, 28 unsafe-fixed, remaining suppressed via config

## [0.5.0] - 2026-06-14

### Added
- Tauri 2.0 native wrapper with `bundle.resources` + `std::process::Command`
- PyInstaller frozen backend embedded in NSIS installer
- CUA-NSIS smoke test (`scripts/cua-smoke.py`, `scripts/cua-nsis-config.json`)
- `just cua-nsis-test` recipe
- Tauri CORS: `tauri://localhost` origins for WebView API access
- `GET /api/v1/diagnostics` endpoint for CUA verification

## [0.4.0] - 2026-03-09

### Added
- **FastMCP 3.1 upgrade**: single-backend pattern with MCP at `/mcp` via `mcp.http_app()`
- **Agentic workflow tool** `backup_workflow`: Multi-step orchestration

### Changed
- Single FastAPI app; MCP at `/mcp` (no separate bridge)
- STDIO entrypoint uses `server.run(transport="stdio")` (3.1 API)

### Fixed
- datetime.utcnow() deprecation replaced with `datetime.now(timezone.utc)`
- ASGI app loading

## [0.3.0]

### Added
- Initial project setup
- Basic FastAPI server structure
- MCP 2.1 protocol support
- Backup job management endpoints
- Scheduling functionality

## [0.1.0] - 2025-07-25

### Added
- Initial release of Hasleo Backup MCP Server
- Basic backup operations
- Simple scheduling
- Status monitoring
