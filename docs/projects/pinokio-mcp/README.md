# pinokio-mcp

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+.1-green.svg)](https://github.com/jlowin/fastmcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for controlling [Pinokio](https://pinokio.co) - the 1-click localhost cloud for AI apps.

## Status: ðŸŸ¢ PRODUCTION READY - Full Feature Set

MCP server for Pinokio with production-grade error handling, portmanteau tools, and LAN Wide Web support.

**Key Features:**
- âœ… **Portmanteau Tools**: Consolidated operations for better UX (60+ operations â†’ 3 tools)
- âœ… **LAN Wide Web**: Zeroconf-based device discovery and cross-device app management
- âœ… **Production Error Handling**: Retry logic, validation, and comprehensive error messages
- âœ… **FastMCP 3.1.1++**: SOTA compliance with modern MCP standards
- âœ… **Comprehensive Testing**: Full test coverage with proper mocking

**API Integration:**
- API reverse-engineered from `pinokiod` source (github.com/pinokiocomputer/pinokiod)
- Core endpoints confirmed working: `/pinokio/info`, `/check`, `/pinokio/launch/:name`, `/pinokio/delete`, `/env/*`
- LAN Wide Web with zeroconf/mDNS discovery
- Cross-device app orchestration

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx pinokio-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "pinokio-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/pinokio-mcp", "run", "pinokio-mcp"]
  }
}
```
## Configuration

### Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json` (Linux/Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "pinokio": {
      "command": "uvx",
      "args": ["pinokio-mcp"],
      "env": {
        "PINOKIO_HOST": "localhost"
      }
    }
  }
}
```

PINOKIO_HOME is optional; the client auto-discovers from Pinokio's config when not set.

### Cursor

Add to Cursor's MCP settings with the same configuration.

## Tools

### Portmanteau Tools (Recommended)

| Tool | Description | Operations |
|------|-------------|------------|
| `app_management(action, ...)` | Manage Pinokio apps | list, status, start, stop, delete |
| `system_management(action)` | System operations | ping, info, localhost_search |
| `lww_management(action, ...)` | LAN Wide Web operations | devices, start_remote |

**Error Handling Features:**
- ðŸ”„ **Automatic Retry**: Exponential backoff for transient failures
- âœ… **Input Validation**: Comprehensive parameter validation with helpful error messages
- ðŸ“ **Structured Errors**: Consistent error format with suggestions for resolution
- ðŸ›¡ï¸ **Graceful Degradation**: Handles partial failures and provides actionable feedback

### Legacy Individual Tools (Testing/Development)

| Tool | Description |
|------|-------------|
| `pinokio_ping()` | Check if Pinokio is running |
| `pinokio_info()` | Get comprehensive system state |
| `pinokio_list_apps()` | List all installed apps |
| `pinokio_app_status(app)` | Check if app is running |
| `pinokio_start(app, script?)` | Launch an app |
| `pinokio_stop(app)` | Stop a running app (limited) |
| `pinokio_delete(app)` | Delete an installed app |
| `pinokio_localhost_search()` | List proxied services |
| `pinokio_lww_devices()` | List Pinokio instances on LAN |
| `pinokio_lww_start(device, app)` | Start app on remote device |

## Resources

| URI | Description |
|-----|-------------|
| `pinokio://apps` | Installed apps (JSON) |
| `pinokio://running` | Running apps (JSON) |
| `pinokio://localhost` | Local services (JSON) |
| `pinokio://lww/devices` | LAN devices (JSON) |

## Prompts

| Prompt | Description |
|--------|-------------|
| `prompt_start_workflow` | Guide for starting AI workflows |
| `prompt_cross_device` | LAN Wide Web orchestration guide |
| `prompt_troubleshooting` | Common issues and solutions |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PINOKIO_HOST` | `localhost` | Pinokio host address |
| `PINOKIO_PORT` | (auto) | Pinokio port (auto-discovers 42000-42059 if not set) |
| `PINOKIO_HOME` | see below | Pinokio home directory |

**PINOKIO_HOME resolution order:** (1) env var, (2) Windows: `%APPDATA%\Pinokio\config.json` `home` key, (3) default `~/pinokio`.

## API Discovery

API was discovered by analyzing `pinokiod` source code. See [DISCOVERY.md](DISCOVERY.md) for full endpoint documentation.

Key insight: The Electron app (`pinokio`) is a thin shell around `pinokiod` npm package which contains the Express server.

### Pinokio 5.x / 6.x Compatibility

Pinokio 5.0+ reintroduced the app; 6.x continues the pinokiod HTTP API. This MCP server targets `/pinokio/info`, `/check`, etc.

- **Port**: Auto-discovers by scanning 42000-42059. Set `PINOKIO_PORT` if you know it (port no longer shown in title bar in recent versions).
- **Home**: Auto-discovers from `%APPDATA%\Pinokio\config.json` on Windows. Override with `PINOKIO_HOME` if needed.
- **Offline mode**: Pinokio 5.3+ "Network Sharing Off by default" does not affect localhost API access.

If tools fail, run `scripts/test_tools.py` or `scripts/discover-api.ps1` to verify.

## Development

```bash
# Clone and install dev dependencies
git clone https://github.com/YOUR_USERNAME/pinokio-mcp
cd pinokio-mcp
pip install -e ".[dev]"

# Run linting
ruff check src/

# Run type checking
mypy src/

# Run tests (once implemented)
pytest
```

## Architecture

```
pinokio-mcp/
â”œâ”€â”€ src/pinokio_mcp/
â”‚   â”œâ”€â”€ __init__.py     # Package exports
â”‚   â”œâ”€â”€ server.py       # FastMCP server with tools/resources/prompts
â”‚   â”œâ”€â”€ client.py       # Pinokio API client (scaffold)
â”‚   â””â”€â”€ models.py       # Pydantic models
â”œâ”€â”€ scripts/
â”‚   â””â”€â”€ discover-api.ps1  # API discovery script
â”œâ”€â”€ pyproject.toml      # Package config + mcpb
â”œâ”€â”€ DISCOVERY.md        # API discovery notes
â””â”€â”€ README.md
```

## Related

- [Pinokio](https://github.com/pinokiocomputer/pinokio) - The main project
- [Pinokio Docs](https://github.com/pinokiocomputer/program.pinokio.computer) - Official documentation
- [FastMCP](https://github.com/jlowin/fastmcp) - Modern Python MCP framework
- [MCP Specification](https://modelcontextprotocol.io) - Model Context Protocol

## Contributing

This is a scaffold waiting for API discovery. Contributions welcome:

1. Run Pinokio and discover API endpoints
2. Update DISCOVERY.md with findings
3. Implement client methods
4. Add tests

## License

MIT

---

*Built with [FastMCP](https://github.com/jlowin/fastmcp) 3.1.1+.1*


## ðŸŒ Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10816**.
*(Assigned ports: **10816** (Web dashboard frontend), **10817** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10816` in your browser.

