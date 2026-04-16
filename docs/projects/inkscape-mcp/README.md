# Inkscape MCP Server

Professional vector graphics and SVG operations for AI agents through the Model Context Protocol.

[![CI/CD](https://img.shields.io/github/actions/workflow/status/sandraschi/inkscape-mcp/ci.yml)](https://github.com/sandraschi/inkscape-mcp/actions)
[![PyPI](https://img.shields.io/pypi/v/inkscape-mcp)](https://pypi.org/project/inkscape-mcp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

Provides AI agents with comprehensive vector graphics capabilities including AI-powered SVG generation, professional vector operations, and Inkscape extension ecosystem access.

## Key Features

- **AI SVG Generation**: Natural language to professional vector graphics
- **27 Vector Operations**: Complete suite across 6 categories
- **Extension Ecosystem**: Access to 200+ Inkscape extensions
- **Cross-platform**: Windows, macOS, Linux support
- **Production Ready**: Comprehensive error handling and validation

## Quick Start

```bash
# Install
pip install inkscape-mcp

# Run
inkscape-mcp --help
```

## Documentation

- [Installation](INSTALL.md) - Setup and configuration
- [Usage](docs/USAGE.md) - Getting started guide
- [Features](docs/FEATURES.md) - Complete feature overview
- [API Reference](docs/API.md) - Tool specifications
- [Architecture](docs/ARCHITECTURE.md) - Technical details
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## MCP Integration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "inkscape-mcp": {
      "command": "inkscape-mcp",
      "args": []
    }
  }
}
```

### Windsurf

Add to your `windsurf_config.json`:

```json
{
  "mcpServers": {
    "inkscape-mcp": {
      "command": "uvx",
      "args": ["inkscape-mcp"]
    }
  }
}
```

## Development

```bash
# Clone repository
git clone https://github.com/sandraschi/inkscape-mcp.git
cd inkscape-mcp

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build package
python -m build
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx inkscape-mcp
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "inkscape-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/inkscape-mcp", "run", "inkscape-mcp"]
  }
}
```


## 🌐 Webapp Dashboard

This MCP server includes a free, premium web interface for monitoring and control.
By default, the web dashboard runs on port **10846**.
*(Assigned ports: **10846** (Web dashboard frontend), **10847** (Web dashboard backend (API)))*

To start the webapp:
1. Navigate to the `webapp` (or `web`, `frontend`) directory.
2. Run `start.bat` (Windows) or `./start.ps1` (PowerShell).
3. Open `http://localhost:10846` in your browser.
