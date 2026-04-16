# Browser Bookmarks Tools (MCP)

FastMCP 3.1.1+ compliant MCP server providing a unified `bookmarks` portmanteau tool for CRUD operations, organization, sync, and AI-powered helpers.

## Features

- **Primary Browser:** Firefox (SQLite-based bookmarks)
- **Secondary Browsers:** Chrome, Edge, Brave (JSON-based bookmarks)
- **Optional:** Safari (plist-based bookmarks)
- **AI Features:** Smart tagging, summarization, and content analysis
- **Cross-browser Sync:** Import/export between different browsers
- **Organization:** Automatic categorization and duplicate detection

## Quick Start

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx bookmarks-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "bookmarks-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/bookmarks-mcp", "run", "bookmarks-mcp"]
  }
}
```
### Running the Server

#### As a Python Module (Recommended for MCP clients)
```bash
python -m browser_bookmarks_tools
```

#### As a Direct Script (Development)
```bash
python src/browser_bookmarks_tools/mcp_server.py
```

#### With uv
```bash
uv run python -m browser_bookmarks_tools
```

## MCP Client Configuration

### Cursor IDE (mcp.json)
```json
{
  "mcpServers": {
    "bookmarks-mcp": {
      "command": "python",
      "args": ["-m", "browser_bookmarks_tools"],
      "env": {
        "PYTHONPATH": "D:/Dev/repos/bookmarks-mcp/src",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Claude Desktop (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "bookmarks-mcp": {
      "command": "python",
      "args": ["-m", "browser_bookmarks_tools"],
      "env": {
        "PYTHONPATH": "/path/to/bookmarks-mcp/src"
      }
    }
  }
}
```

## Available Operations

The `bookmarks` tool supports the following operations:

- **`create`** - Add new bookmarks with metadata
- **`read`** - Retrieve bookmarks by URL, title, or tags
- **`update`** - Modify existing bookmarks
- **`delete`** - Remove bookmarks
- **`organize`** - Auto-categorize and clean up bookmarks
- **`sync`** - Import/export between browsers
- **`analyze`** - AI-powered content analysis and tagging
- **`tag`** - Smart tag generation and management
- **`summarize`** - Create bookmark summaries

## Browser Support Details

### Firefox (Primary)
- **Storage:** `places.sqlite` database
- **Features:** Full history, tags, folders, favicons
- **Path:** `~/.mozilla/firefox/*/places.sqlite`

### Chrome/Edge/Brave
- **Storage:** JSON bookmark files
- **Features:** Basic bookmarks with folders
- **Path:** `~/Library/Application Support/Google/Chrome/Default/Bookmarks`

### Safari (macOS only)
- **Storage:** Binary plist files
- **Features:** Basic bookmarks
- **Path:** `~/Library/Safari/Bookmarks.plist`

## Development

### Project Structure
```
bookmarks-mcp/
â”œâ”€â”€ src/browser_bookmarks_tools/
â”‚   â”œâ”€â”€ __init__.py          # Package initialization
â”‚   â”œâ”€â”€ __main__.py          # Module entry point for `python -m`
â”‚   â”œâ”€â”€ mcp_server.py       # FastMCP server implementation
â”‚   â”œâ”€â”€ bookmarks/           # Core bookmark operations
â”‚   â”‚   â”œâ”€â”€ manager.py       # CRUD operations
â”‚   â”‚   â”œâ”€â”€ organizer.py     # Organization features
â”‚   â”‚   â”œâ”€â”€ portmanteau.py   # Main tool interface
â”‚   â”‚   â””â”€â”€ sync.py          # Cross-browser sync
â”‚   â”œâ”€â”€ ai/                  # AI-powered features
â”‚   â”‚   â”œâ”€â”€ analyzer.py      # Content analysis
â”‚   â”‚   â”œâ”€â”€ summarizer.py    # Summary generation
â”‚   â”‚   â””â”€â”€ tagger.py        # Smart tagging
â”‚   â””â”€â”€ browsers/            # Browser-specific implementations
â”œâ”€â”€ tests/
â””â”€â”€ pyproject.toml
```

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint code
ruff check src/

# Type checking
mypy src/
```

## Troubleshooting

### "Module not found" errors
Ensure `PYTHONPATH` includes the `src` directory:
```bash
export PYTHONPATH="/path/to/bookmarks-mcp/src:$PYTHONPATH"
```

### Browser permission issues
- **Firefox:** Ensure Firefox is not running when accessing `places.sqlite`
- **Chrome/Edge:** No special permissions needed for reading bookmark files
- **Safari:** Requires macOS and appropriate file permissions

### MCP connection issues
- Verify the server starts without errors when run manually
- Check that `PYTHONPATH` is correctly set in your MCP client configuration
- Ensure no firewall/antivirus is blocking the connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[Add appropriate license information]

## Changelog

### v0.1.0
- Initial FastMCP 3.1.1+ compliant implementation
- Firefox, Chrome, Edge, Brave, and Safari support
- Unified portmanteau tool interface
- AI-powered bookmark analysis and tagging
- Cross-browser synchronization


## ðŸŒ Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10802**.
*(Assigned ports: **10802** (Web dashboard frontend), **10803** (Web dashboard backend))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10802` in your browser.

