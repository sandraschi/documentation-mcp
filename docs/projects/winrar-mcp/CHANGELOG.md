# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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