# FastSearch MCP

âš¡ Lightning-fast file search for Claude Desktop via direct NTFS Master File Table access â€” no indexing, no caching, no compromises.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+%2B-brightgreen)](https://docs.anthropic.com/claude/docs/mcp)

> **Core Principle:** FastSearch MCP follows the WizFile philosophy. Every request reads straight from the NTFS MFT. We never build background indexes, caches, or persistent file databases.

## ðŸš€ Why FastSearch MCP

- **Direct NTFS MFT reads** for sub-second search across millions of files.
- **Zero indexing & zero persistence** keeps startup instant and memory under 50 MB.
- **Claude-first integration** through the MCP protocol and schema-driven tools.
- **Privilege separation**: elevated C++ service handles filesystem duties, Python bridge stays in user space.
- **Fast service checks** - <1ms overhead per search (optimized from 5 seconds).
- **Clear error messages** - Actionable guidance when service is unavailable.

## ðŸ— Architecture Overview

```
Claude Desktop
      â”‚ JSON-RPC (stdin/stdout)
Python MCP Bridge (user privileges)
      â”‚ Named pipe (`\\.\pipe\FastSearchMCP`)
C++ Windows Service (LocalSystem)
      â”‚
NTFS Master File Table (live)
```

- **C++ Windows Service (`service/`)**
  - Runs as `LocalSystem`.
  - Opens NTFS volumes directly and answers search requests on demand.
  - Emits structured logging to the Windows Event Log for diagnostics.
  - No background threads, no file caches, no startup scans.

- **Python MCP Bridge (`src/fastsearch_mcp/`)**
  - Implements FastMCP 3.1.1+ tools (`fastsearch_search`, `disk_analyzer`, `service_status`, etc.).
  - Marshals requests to the service via named pipes and reformats results for Claude.
  - Fast service availability checks (<1ms) before each search.
  - Clear error messages when service is unavailable (no silent fallbacks).

## ðŸš¨ Architecture Guardrails (Non-Negotiable)

- **Never add indexing, background scanning, or persistent metadata stores.**
- **Never introduce in-memory caches of file lists or search results.**
- **Always query NTFS live and stop once `max_results` is reached.**
- **Always maintain instant startup, real-time accuracy, and minimal memory usage.**

See `docs/WIZFILE_COMPARISON.md` for the rationale.

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx fastsearch-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "fastsearch-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/fastsearch-mcp", "run", "fastsearch-mcp"]
  }
}
```
### Quick Start

#### For IDE Users (Cursor, Windsurf, Zed) â­ **Recommended**

1. Install service: Download `fastsearch-mcp-setup.msi` â†’ Run as Administrator
2. Install Python package: `pip install fastsearch-mcp`
3. Configure IDE: `npx -y fastsearch-mcp`

#### For Claude Desktop Users

1. Install service: Download `fastsearch-mcp-setup.msi` â†’ Run as Administrator
2. Install extension: Drag `fastsearch-mcp-0.4.0.mcpb` into Claude Desktop
   - **Note**: MCPB format is Claude Desktop specific. The "drag-and-drop into settings UI" UX is unconventional.
   - **Benefit**: MCPB includes prompt templates (system prompts, user guides) that help Claude understand capabilities.
   - **Alternative**: Use NPX installation above for standard MCP config (works with Claude Desktop too).
   - **See**: [`docs/MCPB_STATUS.md`](docs/MCPB_STATUS.md) for detailed explanation of MCPB limitations and prompt template alternatives.

#### For Developers

See [Local Installation](docs/INSTALLATION_METHODS.md#1-local-installation-development) for full setup.

## â–¶ï¸ Running the MCP Server Locally

```powershell
.venv\Scripts\Activate.ps1
python scripts/start_server.py
```

Add `fastsearch-mcp` to Claude Desktop's MCP configuration (see `mcp.config.json`) to auto-launch with Claude.

## ðŸ§ª Development Notes

- `pytest` runs the Python test suite (18/18 tests passing).
- `scripts/check-repo-standards.ps1` enforces logging + doc standards.
- **Search functionality fully operational** - All search tools working with direct NTFS MFT access.
- **Service running** - FastSearch Windows service operational and responding to requests.
- **Performance optimized** - Service checks optimized to <1ms (from 5 seconds).

See `docs/RECENT_IMPROVEMENTS.md` for details on recent improvements.

## ðŸ“š Key Documentation

- `docs/RECENT_IMPROVEMENTS.md` â€“ **NEW** - Recent improvements and search functionality status.
- `docs/STATUS_REPORT.md` â€“ Current project status and what's working.
- `docs/TECHNICAL_ARCHITECTURE.md` â€“ deep dive into the C++ + MCP bridge design.
- `docs/PRODUCT_REQUIREMENTS.md` â€“ product goals and non-negotiable principles.
- `docs/SERVICE_AVAILABILITY_CHECKS.md` â€“ How service availability is checked and error handling.
- `docs/WIZFILE_COMPARISON.md` â€“ why direct MFT access beats indexing.

## ðŸ¤ Contributing

We welcome contributions that preserve the direct-MFT architecture.

1. Open an issue describing the change.
2. Confirm it does **not** add indexing, caching, or background scanning.
3. Create a feature branch and add tests where applicable.
4. Run `pytest` and the markdown linter (`scripts/lint-markdown.ps1`).
5. Submit a PR referencing the relevant docs.

## ðŸ“„ License

MIT â€“ see [LICENSE](LICENSE).


## ðŸŒ Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10844**.
*(Assigned ports: **10844** (Web dashboard frontend), **10845** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10844` in your browser.

