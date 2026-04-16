# rTorrent MCP Server ðŸ‡¦ðŸ‡¹ðŸŽŒ

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+-brightgreen)](https://fastmcp.anthropic.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/status-production%20ready-success)](https://github.com/sandraschi/qbtmcp)
[![SOTA](https://img.shields.io/badge/SOTA-Portmanteau%20Pattern-purple)](https://fastmcp.anthropic.com)

FastMCP 3.1.1+ SOTA server for anime torrenting automation with Austrian legal compliance using rTorrent.

> **ðŸ“ Package name `qbtmcp`?** This project started as "qBittorrent MCP" but we discovered
> qBittorrent has no usable API/CLI. We pivoted to rTorrent (powerful SCGI control) mid-development.
> The package name was kept for backwards compatibility.

## Features ðŸŽ¯

- **FastMCP 3.1.1+ SOTA**: Portmanteau pattern, MCPB, prompt templates, CI/CD pipeline
- **6 Consolidated Tools**: torrent, search, nlp, legal, system, workflow management
- **rTorrent Integration**: Full SCGI API control (add/pause/resume/delete torrents)
- **Multi-Source Search**: nyaa.si (anime), Pirate Bay (TV), YTS (movies), Anna's Archive (ebooks)
- **Post-Processing**: Automatic completion detection, filename normalization, Plex integration
- **Metadata Services**: IMDb and TVDB metadata retrieval for movies and TV shows
- **Austrian Legal Compliance**: Built-in legal risk assessment for Austrian users
- **Natural Language Commands**: Process Sandra's anime requests in English/German
- **Quality Scoring**: Intelligent ranking of releases by group reputation
- **Self-Documenting Tools**: Comprehensive tool descriptions with input/output schemas
- **Repository Analysis**: Deep codebase analysis and recommendations
- **System Status Monitoring**: Detailed server health and metrics
- **Configuration Management**: Environment variables and .env file support
- **Comprehensive Testing**: Unit and integration tests for all components

## ðŸš€ Quick Start

### Prerequisites

- Python 3.10 or higher
- Docker Desktop (for rTorrent) - **Recommended**
- Claude Desktop (for MCP integration)

### rTorrent Setup (Docker - Recommended)

We use the [crazymax/rtorrent-rutorrent](https://github.com/crazy-max/docker-rtorrent-rutorrent) Docker image.

**This is NOT just a thin pipe!** The image comes with 25+ ruTorrent plugins bundled:
- **RSS/Feeds**: Auto-download anime from SubsPlease, ASW feeds
- **Autotools**: Auto-label, auto-move to Plex library
- **Scheduler**: Download during off-peak hours
- **Unpack**: Auto-extract RAR/ZIP archives
- **Ratio/Seedingtime**: Seeding compliance tracking

```bash
# Start rTorrent + ruTorrent in Docker
docker-compose up -d

# Verify it's running
docker logs rtorrent-mcp

# Access points:
# - XMLRPC (MCP): http://localhost:12224/RPC2
# - WebUI: http://localhost:12222
```

See [detailed rTorrent setup guide](docs/RTORRENT_SETUP.md) for the full plugin list and configuration.

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx qbt-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "qbt-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/qbt-mcp", "run", "qbt-mcp"]
  }
}
```
## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx qbt-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "qbt-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/qbt-mcp", "run", "qbt-mcp"]
  }
}
```
#### Quick Setup (Windows - Docker Recommended)

**Prerequisites:** Docker Desktop must be installed and running.

```batch
# Download the project files
# Place docker-compose.yml and install.bat in your desired directory

# Run the installation script
install.bat

# The script will:
# - Create necessary directories
# - Configure rTorrent with SCGI support
# - Start the Docker containers
# - Test the connection
```

**Management Commands:**
```batch
start.bat      # Start rTorrent containers
stop.bat       # Stop rTorrent containers  
status.bat     # Check container status and health
uninstall.bat  # Remove everything
```

#### Alternative: WSL2 Setup

```powershell
# Enable WSL2 (run as Administrator)
wsl --install -d Ubuntu

# Inside WSL2 Ubuntu
sudo apt update
sudo apt install rtorrent
```

#### Linux/macOS Setup

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install rtorrent

# CentOS/RHEL/Fedora
sudo yum install rtorrent
# or
sudo dnf install rtorrent

# macOS
brew install rtorrent

# Verify SCGI support
rtorrent -h | grep -i scgi
```

#### Basic Configuration

**For Docker (Windows):**

1. **Create rTorrent configuration**
   ```powershell
   # Create config directory
   mkdir C:\rtorrent-mcp\config
   
   # Create rtorrent.rc configuration
   @"
   # SCGI configuration for MCP server
   scgi_port = 0.0.0.0:5000
   
   # Basic settings
   session.path.set = /config/session
   directory.default.set = /downloads
   log.execute = /config/rtorrent.log
   
   # Performance settings
   max_uploads.set = 50
   max_connections.set = 200
   max_peers.set = 100
   
   # Austrian Legal Compliance
   system.method.set_key = event.download.inserted_new, anime_category, "d.custom1.set=anime"
   "@ | Out-File -FilePath "C:\rtorrent-mcp\config\rtorrent.rc" -Encoding UTF8
   ```

2. **Restart container to apply configuration**
   ```powershell
   docker-compose restart
   ```

3. **Verify connection**
   ```powershell
   # Test SCGI connection from Windows
   Invoke-RestMethod -Uri "http://localhost:5000/RPC2" -Method POST -ContentType "text/xml" -Body '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'
   ```

**For WSL2/Linux/macOS:**

1. **Create rTorrent configuration**
   ```bash
   mkdir -p ~/.rtorrent
   cat > ~/.rtorrent.rc << 'EOF'
   # SCGI configuration for MCP server
   scgi_port = localhost:5000
   
   # Basic settings
   session.path.set = ~/.rtorrent/session
   directory.default.set = ~/Downloads
   log.execute = ~/.rtorrent/rtorrent.log
   
   # Performance settings
   max_uploads.set = 50
   max_connections.set = 200
   max_peers.set = 100
   EOF
   ```

2. **Start rTorrent daemon**
   ```bash
   # Start in background
   rtorrent -d
   
   # Or with systemd (create service)
   sudo systemctl start rtorrent
   sudo systemctl enable rtorrent
   ```

3. **Verify connection**
   ```bash
   # Test SCGI connection
   curl -X POST -H "Content-Type: text/xml" \
     -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>' \
     http://localhost:5000/RPC2
   ```

For Windows, macOS, Docker, and advanced configuration options, see [docs/RTORRENT_SETUP.md](docs/RTORRENT_SETUP.md).

### Configuration

1. **Create a `.env` file** (or set environment variables)

   ```env
   # rTorrent settings
   RTORRENT_HOST=localhost
   RTORRENT_PORT=5000
   RTORRENT_PATH=/var/lib/rtorrent/session

   # Nyaa.si settings
   NYAA_BASE_URL=https://nyaa.si

   # Application settings
   DEBUG=false
   LOG_LEVEL=INFO
   ```

### Running the Server

```bash
# Run with stdio transport (for Claude Desktop)
python -m qbtmcp.server --transport stdio

# Or with HTTP transport
python -m qbtmcp.server --transport http

# Custom config file
python -m qbtmcp.server --config /path/to/config.env

# Direct module execution
python src/qbtmcp/server.py
```

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx qbt-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "qbt-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/qbt-mcp", "run", "qbt-mcp"]
  }
}
```
## ðŸ“¦ Development

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=qbtmcp --cov-report=html
```

### Code Style

```bash
# Format code with ruff
uv run ruff format .

# Lint code with ruff
uv run ruff check . --fix

# Type checking with pyright
uv run pyright

# Security scanning
uv run bandit -r src/
uv run safety scan
```

## ðŸŽ¯ Features in Detail

### ðŸ” Smart Anime Search

```python
# Basic search
await search_anime("Detective Conan", resolution="720p", group="ASW")

# Advanced search with filters
await search_anime(
    query="One Piece",
    resolution="1080p",
    group="Erai-raws"
)
```

### ðŸŽ›ï¸ rTorrent Integration

```python
# Add torrent from magnet link
magnet = "magnet:?xt=urn:btih:..."
await add_torrent(magnet, category="anime")

# Monitor and manage downloads
await list_torrents()
await pause_torrent("torrent_hash")
await resume_torrent("torrent_hash")
await delete_torrent("torrent_hash", delete_files=True)

# Check connection status
await get_status()
```

### ðŸ‡¦ðŸ‡¹ Austrian Legal Compliance

```python
# Check if content is safe for Austria
is_safe = await check_austrian_legal_status(torrent_info)
if is_safe:
    await add_torrent_qbt(torrent_info["magnet"])
else:
    logger.warning("Content may not be legal in Austria")
```

### ðŸ” Extended Search Capabilities

```python
# Search manga
await search_manga("One Piece", subcategory="translated")

# Search Japanese TV shows
await search_japanese_tv("Terrace House", subcategory="translated")

# Search movies on YTS
await search_movies("The Matrix", quality="1080p", sort_by="seeds")

# Search ebooks on Anna's Archive (60M+ books!)
await search_ebooks_annas("Python Programming", content_type="books")

# Search comics on Pirate Bay
await search_comics("Watchmen", max_results=20)
```

### ðŸ“Š Metadata Services

```python
# Get IMDb metadata for a movie
await get_imdb_metadata("The Matrix", year=1999)

# Search IMDb for multiple matches
await search_imdb("Matrix", year=1999)

# Get TVDB metadata (requires API subscription)
await get_tvdb_metadata("Breaking Bad", year=2008)

# Get detailed Anna's Archive torrent info
await get_annas_detail("https://annas-archive.org/...")
```

### ðŸ”„ Post-Processing System

```python
# Check for completed downloads
completed = await check_completed_downloads()

# Process a completed download
await process_completed_download("torrent_hash")

# Start automatic post-processing (background polling)
await start_post_processing()

# Stop post-processing
await stop_post_processing()

# Normalize a filename
normalized = await normalize_filename("Show.Name.S01E01.RELEASE-GROUP.mkv", category="tv")
```

### ðŸ¤– Natural Language Processing

```python
# English commands
await sandra_anime_command("get me this weeks asw anime, 720p")

# German commands
await sandra_anime_command("lade detective conan asw 720p")

# Parse commands without executing
await parse_anime_command("asw attack on titan 1080p")

# Get command help
await get_command_help()
```

### ðŸ› ï¸ System Tools

```python
# Get comprehensive help
await help()

# System status and health check
await get_system_status()

# Analyze the repository
await analyze_repo()
```

## ðŸ”§ Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `RTORRENT_HOST` | `localhost` | rTorrent SCGI host |
| `RTORRENT_PORT` | `5000` | rTorrent SCGI port |
| `RTORRENT_PATH` | `/var/lib/rtorrent/session` | rTorrent session path |
| `NYAA_BASE_URL` | `https://nyaa.si` | Nyaa.si base URL |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `DEBUG` | `false` | Enable debug mode |
| `ALLOWED_CATEGORIES` | `["Anime"]` | Allowed content categories |
| `ALLOWED_RESOLUTIONS` | `["720p", "1080p"]` | Allowed video resolutions |
| `MAX_TORRENT_SIZE_GB` | `10` | Maximum allowed torrent size in GB |
| `POST_PROCESSING_ENABLED` | `false` | Enable automatic post-processing |
| `POST_PROCESSING_POLL_INTERVAL` | `60` | Seconds between polling for completed downloads |
| `DELETE_TORRENT_AFTER_COMPLETE` | `true` | Remove torrent after completion |
| `NORMALIZE_FILENAMES` | `true` | Normalize filenames before moving |
| `INGESTION_ANIME_PATH` | - | Path to temporary ingestion folder for anime |
| `INGESTION_TV_PATH` | - | Path to temporary ingestion folder for TV shows |
| `INGESTION_MOVIES_PATH` | - | Path to temporary ingestion folder for movies |
| `OMDB_API_KEY` | - | OMDb API key for IMDb metadata (free at omdbapi.com) |
| `TVDB_API_KEY` | - | TVDB API key for TV metadata (requires subscription) |

## ðŸ“š Documentation

### API Reference

For detailed API documentation, run the server and visit:

```
http://localhost:8000/docs
```

### Product Requirements Document

See [PRD.md](docs/PRD.md) for comprehensive product specifications, requirements, and implementation details.

### Extended Search Guide

See [EXTENDED_SEARCH_GUIDE.md](docs/EXTENDED_SEARCH_GUIDE.md) for complete guide to using all search capabilities including manga, movies, ebooks, comics, and metadata services.

### Post-Processing Setup

See [POST_PROCESSING_SETUP.md](docs/POST_PROCESSING_SETUP.md) for complete post-processing configuration guide, including ingestion folder setup and Plex integration.

### Status Report

See [STATUS_REPORT.md](docs/STATUS_REPORT.md) for current project status, metrics, and development roadmap.

### Development

1. Install development dependencies:

   ```bash
   uv sync --dev
   ```

2. Run tests:

   ```bash
   uv run pytest
   ```

3. Build documentation:

   ```bash
   uv run mkdocs serve
   ```

   Then visit <http://localhost:8001>

## ðŸ¤– Claude Desktop Integration

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx qbt-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "qbt-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/qbt-mcp", "run", "qbt-mcp"]
  }
}
```
### Option 2: Manual MCP Configuration

For advanced users or custom setups, manually configure Claude Desktop:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
**Location**: `%APPDATA%/Claude/claude_desktop_config.json` (Windows)
**Location**: `~/.config/Claude/claude_desktop_config.json` (Linux)

Add this configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rtorrent-mcp": {
      "command": "python",
      "args": ["-m", "qbtmcp.server", "--transport", "stdio"],
      "cwd": "/path/to/your/qbtmcp",
      "env": {
        "PYTHONPATH": "/path/to/your/qbtmcp/src",
        "RTORRENT_HOST": "localhost",
        "RTORRENT_PORT": "5000",
        "NYAA_BASE_URL": "https://nyaa.si"
      }
    }
  }
}
```

**Configuration Notes**:
- Replace `/path/to/your/qbtmcp` with your actual repository path
- Adjust environment variables as needed for your setup
- The server will start automatically when Claude Desktop launches

## ðŸ¤ Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ðŸ“„ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ™ Acknowledgments

- [rTorrent](https://rakshasa.github.io/rtorrent/) - The lightweight torrent client
- [Nyaa.si](https://nyaa.si/) - For the anime torrents
- [FastMCP](https://fastmcp.anthropic.com) - The MCP framework
- [Claude Desktop](https://claude.ai/desktop) - For MCP integration

---

Made with â¤ï¸ in Vienna, Austria

### Legal Compliance

```python
# Check legal status
await check_legal_status("austria")  # âœ… Safe for Sandra in Vienna
await check_legal_status("germany")  # ðŸš¨ High risk, VPN mandatory
```

## Release Group Priorities ðŸ†

1. **ASW** (100pts) - Austrian preference
2. **SubsPlease** (90pts)
3. **Erai-raws** (85pts)
4. **EMBER** (80pts)
5. **Judas** (75pts)

## Austrian Context ðŸ‡¦ðŸ‡¹

- **Legal Status**: Personal downloading generally tolerated
- **Sandra's Location**: Vienna, 9th district
- **Risk Assessment**: Safe for individual anime consumption
- **Language Support**: English + German commands

## Configuration âš™ï¸

Copy `.env.example` to `.env` and configure:

```env
RTORRENT_HOST=localhost
RTORRENT_PORT=5000
NYAA_BASE_URL=https://nyaa.si
ALLOWED_CATEGORIES=Anime
ALLOWED_RESOLUTIONS=720p,1080p
DEFAULT_RESOLUTION=720p
PREFERRED_RELEASE_GROUP=ASW
LOG_LEVEL=INFO
```

## Testing ðŸ§ª

### Run Tests

```bash
# Run all tests with coverage
pytest

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=qbtmcp --cov-report=html
```

### Test Structure

```
tests/
â”œâ”€â”€ conftest.py              # Test configuration and fixtures
â”œâ”€â”€ unit/                    # Unit tests (isolated components)
â”‚   â””â”€â”€ test_rtorrent_client.py
â””â”€â”€ integration/             # Integration tests (full workflows)
    â””â”€â”€ test_mcp_integration.py
```

### PowerShell Test Runner

Windows users can use the PowerShell test runner:

```powershell
# Run all tests
.\scripts\run-tests.ps1

# Run with coverage
.\scripts\run-tests.ps1 -Coverage

# Run unit tests only
.\scripts\run-tests.ps1 -Unit
```

### Modern Development Commands

With UV installed, you can use these modern commands:

```bash
# Install all dependencies (including dev tools)
uv sync --dev

# Run linting and formatting
uv run ruff check . --fix
uv run ruff format .

# Run type checking
uv run pyright

# Run security scans
uv run bandit -r src/
uv run safety scan

# Run tests with coverage
uv run pytest --cov=src/qbtmcp --cov-report=html

# Build package
uv build

# Validate package
uv run twine check dist/*
```

## Production Readiness âœ…

This MCP server has been audited against enterprise production standards and achieved **95% compliance** (57/60 criteria met).

### âœ… Completed Standards
- **FastMCP 3.1.1+ Compliance**: Latest standards with stdio transport
- **Comprehensive Testing**: Unit + integration tests with 80%+ coverage
- **Enterprise Documentation**: Full API docs, PRD, CHANGELOG, contributing guidelines
- **CI/CD Pipeline**: Automated testing, linting, building, and releasing
- **Security Audited**: No vulnerabilities in core dependencies
- **Cross-Platform**: Windows/PowerShell first with Linux compatibility
- **Legal Compliance**: Austrian-focused with international warnings
- **Professional Architecture**: Clean separation, error handling, logging

### ðŸ“‹ Production Checklist
See [`docs/MCP_PRODUCTION_CHECKLIST.md`](docs/MCP_PRODUCTION_CHECKLIST.md) for the complete audit results.

### ðŸš€ Ready for Enterprise Use
This server meets production requirements for:
- Individual anime enthusiasts in Austria ðŸ‡¦ðŸ‡¹
- Development teams needing MCP examples
- Organizations requiring audited, secure automation tools

## Legal Disclaimer âš–ï¸

This tool is designed for Austrian legal context where personal downloading is generally tolerated. Users in other jurisdictions should research local copyright laws. High-risk countries (Germany, Japan) require additional precautions.

## Dependencies ðŸ“¦

- **FastMCP 3.1.1++**: MCP server framework with stdio transport
- **UV**: Modern Python package manager for fast, reliable builds
- **aiohttp**: Async HTTP client for nyaa.si API
- **beautifulsoup4**: HTML parsing for search results
- **rtorrent-xmlrpc**: rTorrent SCGI communication
- **psutil**: System monitoring and health checks
- **pydantic**: Data validation and settings management
- **python-dotenv**: Environment configuration

### Development Dependencies

- **ruff**: Fast Python linter and formatter
- **pyright**: Type checking and static analysis
- **bandit**: Security vulnerability scanner
- **safety**: Dependency vulnerability scanner
- **pytest**: Testing framework with coverage
- **build & twine**: Package building and publishing

## Author ðŸ‘©â€ðŸ’»

Sandra's Austrian Anime Automation ðŸ‡¦ðŸ‡¹ðŸŽŒ

*"Sin temor y sin esperanza" - Practical automation without hype.*

