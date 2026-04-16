# Multi Backup MCP Server

[![Python](https://img.shields.io/badge/python-3.8+-blue)](#requirements)
[![MCP](https://img.shields.io/badge/MCP-2.1-brightgreen)](#mcp-client-integration)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

**âš ï¸ STATUS: ALPHA / BASIC FUNCTIONALITY** - This server starts and runs, but backup operations have not been tested. FastMCP 3.1.1++ compliant implementation.

A **multi-method backup MCP server** providing comprehensive system protection and development repository archival. Supports three core backup methods:

1. **Hasleo Backup Suite** - Professional disk imaging and partition management.
2. **Repository Archival (SOTA)** - Intelligent, pruned zipping of development repositories.
3. **Git/GitHub Tools** - Version control integration for project snapshots.

All methods are accessible through the Model Context Protocol, enabling AI-assisted backup management.

## ðŸš€ MCP Client Integration

This server implements the MCP 2.1 protocol over STDIO, making it compatible with any MCP-compliant client. The primary purpose is to enable AI-assisted backup management through the Model Control Protocol.

### Key MCP Features

- Full MCP 2.1 protocol support
- STDIO transport for maximum compatibility
- Asynchronous message handling
- Structured logging and error reporting
- WebSocket support for real-time updates

### Quick Start with MCP Client

```python
# Example MCP client usage
import asyncio
import json

async def mcp_client():
    proc = await asyncio.create_subprocess_exec(
        'python', '-m', 'multi_backup_mcp',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    # Send MCP message
    message = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'backup.list',
        'params': {}
    }
    proc.stdin.write((json.dumps(message) + '\n').encode())
    await proc.stdin.drain()
    
    # Read response
    response = await proc.stdout.readline()
    print('MCP Response:', response.decode().strip())

asyncio.run(mcp_client())
```

## ðŸ“‹ Table of Contents

- [Web Interface](#-web-interface)
- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [License](#-license)

## âœ¨ Features

### Backup Methods

#### 1. System Backup Suite
- **System & Disk Backups** - Full system image backups, disk/partition backups
- **Backup Management** - Create, list, and manage backup jobs
- **Scheduling** - Flexible scheduling with cron-like expressions
- **Progress Monitoring** - Real-time backup progress tracking
- **Restore Operations** - Restore from existing backups

#### 2. Repository Archival (Native Python)
- **SOTA Pruning**: Intelligent directory walking that automatically excludes `node_modules`, `target` (Rust), `venv`, and build artifacts while preserving project structure.
- **Nuclear Backup**: Batch archival of all repositories in `D:/Dev/repos` with a single trigger.
- **MCP Signature Detection**: Automatic identification of MCP servers via `pyproject.toml` markers.
- **Multi-Destination**: Synchronized distribution to Desktop and N: drive storage.
- **Perfect for**: Secure, portable snapshots of development environments.

#### 3. Git/GitHub Tools
- **Version Control as Backup** - Initialize git repos, create GitHub repositories
- **Quick Setup** - Auto-create .gitignore and README.md
- **GitHub Integration** - Create repos and push via GitHub CLI
- **Perfect for** - Project initialization, version control backup

### Additional Features

- **Web Interface**
  - Modern, responsive FastAPI-based dashboard
  - Real-time status monitoring
  - Interactive backup management
  - System resource usage
  - Interactive API documentation with Swagger UI
  - Health check endpoints

- **Security**
  - API key authentication
  - Role-based access control
  - Encrypted communication

## ðŸš€ Requirements

### Core Requirements
- Claude Desktop with DXT support (or Python 3.10+ for development)
- Windows 10/11 or Windows Server 2016+ (for Hasleo Backup Suite)
- 4GB RAM minimum (8GB recommended)
#### **MCPB CLI** (Required for packaging distribution bundles)
```bash
npm install -g @anthropic-ai/mcpb
```

### Method-Specific Requirements

**System Backup Suite:**
- Compatible system backup software (recommended: Hasleo Backup Suite)

**Archive Tools:**
- No additional requirements (uses Python's built-in `zipfile` module)

**Git/GitHub Tools:**
- [Git](https://git-scm.com/) installed
- [GitHub CLI](https://cli.github.com/) (for `make_github` tool)
- GitHub CLI authenticated: `gh auth login`

## ðŸ“¦ Packaging & Distribution

This repository is SOTA 2026 compliant and uses the officially validated `@anthropic-ai/mcpb` workflow for distribution.

### Pack Extension
To generate a `.mcpb` distribution bundle with complete source code and automated build exclusions:
```bash
# SOTA 2026 standard pack command
mcpb pack . dist/multi-backup-mcp.mcpb
```

## ðŸ”§ Development Setup

### Prerequisites

1. Install [Python 3.8+](https://www.python.org/downloads/)
2. Install compatible backup software (optional, depending on backup method)

### Setup

```bash
# Clone the repository
git clone https://github.com/sandraschi/multi-backup-mcp.git
cd multi-backup-mcp

# Install dependencies
uv pip install -r requirements.txt

# Set up pre-commit hooks (recommended)
# Option 1: Use the setup script (Windows PowerShell)
.\scripts\setup-pre-commit.ps1

# Option 2: Manual setup
pip install pre-commit
pre-commit install

# Copy example config
cp config.example.yaml config.yaml

# Edit config file with your settings
# (See Configuration Reference for details)
```

## ðŸš€ Quick Start

1. Start the MCP server:

   ```bash
   # Install dependencies
   uv pip install -r requirements.txt
   
   # Start the server
   python -m multi_backup_mcp
   ```

2. Access the web interface:
   - **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
   - **API Documentation**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

3. Use any of the backup methods:
   - **Hasleo Backup**: Create system/disk backups
   - **Archive Tools**: Create ZIP archives of folders
   - **Git/GitHub**: Initialize version control

### Quick Examples

**Hasleo Backup:**
```python
create_backup(
    name="System Backup",
    source="C:\\",
    destination="D:\\Backups"
)
```

**Archive Tool:**
```python
create_archive(
    source="D:\\Dev\\repos\\my-project",
    destination="D:\\Backups"
)
```

**Git/GitHub:**
```python
# Initialize git repo
make_git(directory="D:\\Dev\\repos\\my-project")

# Create GitHub repo
make_github(directory="D:\\Dev\\repos\\my-project")
```

## ðŸŒ Web Interface

The FastAPI web interface provides several key endpoints:

- `/` - Main web dashboard
- `/api/docs` - Interactive API documentation (Swagger UI)
- `/api/redoc` - Alternative API documentation (ReDoc)
- `/health` - Health check endpoint
- `/api/v1/backups` - Manage backup jobs
- `/api/v1/schedules` - Manage backup schedules
- `/api/v1/system` - System information and metrics

### API Authentication

The API supports the following authentication methods:

1. **API Key**: Include `X-API-Key` header in your requests
2. **OAuth2**: Use the `/token` endpoint to get an access token
3. **Session Cookies**: For browser-based access

### Example API Requests

```bash
# Get system information
curl -X 'GET' \
  'http://localhost:8000/api/v1/system/info' \
  -H 'accept: application/json'

# Create a new backup job
curl -X 'POST' \
  'http://localhost:8000/api/v1/backups' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Full System Backup",
    "source": "C:\\",
    "destination": "D:\\Backups",
    "type": "full"
  }'

# Check server health
curl -X 'GET' \
  'http://localhost:8000/health' \
  -H 'accept: application/json'
```

## ðŸ“š Documentation

### User Guides

- [User Guide](docs/USER_GUIDE.md) - Getting started and basic usage
- [Configuration Reference](docs/CONFIGURATION.md) - All available configuration options
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [API Reference](docs/API.md) - Complete API documentation

### Developer Resources

- [Development Guide](docs/DEVELOPMENT.md) - Setting up a development environment
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Changelog](CHANGELOG.md) - Release history and changes

## ðŸ¤ Contributing

Contributions are welcome! Please read our [Contributing Guidelines](docs/CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest new features.

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks (recommended)
pip install pre-commit
pre-commit install

# Run tests
pytest

# Run linting
ruff check .
ruff format .

# Run with hot reload for development
uvicorn multi_backup_mcp.main:app --reload
```

## ðŸ“„ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ“ Notes

- Always test backups before relying on them in production.
- Keep your API keys and credentials secure.
- Different backup methods may require specific software installation.

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx multi-backup-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "multi-backup-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/multi-backup-mcp", "run", "multi-backup-mcp"]
  }
}
```

