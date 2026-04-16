# Windows Operations MCP

[![FastMCP](https://img.shields.io/badge/FastMCP-3.1.1+.3-blue)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![MCPB](https://img.shields.io/badge/MCPB-v0.2-green)](https://modelcontextprotocol.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green)](REPOSITORY_STATUS_REPORT.md)

A comprehensive Windows system operations MCP server implementing the FastMCP 3.1.1+.3 protocol with full MCPB (MCP Bundle) packaging support.

## âœ¨ Core Features (January 2026 SOTA)

- **ðŸŽ¯ Portmanteau Logic**: Surgical tool reduction (9 specialized interface tools)
- **ðŸš€ Integrated SOTA Dashboard**: Specialized multi-page Vite dashboard with real-time telemetry
- **ðŸ¤– AI Command Center**: Integrated AI Router for natural language system orchestration
- **âš¡ FastAPI Bridge**: SOTA integrated bridge on port 10748
- **âœ… MCPB v1.18.1**: Full MCP Bundle compliance for zero-friction distribution
- **âœ… Secure Sampling**: SEP-1577 compliant autonomous tool invocation

## ðŸš€ Key Features

### âœ… MCPB Packaging & Distribution
- **Full MCPB compliance** with proper manifest structure (v0.2 format)
- **Automated AI-generated manifests** for optimal configuration
- **PowerShell build automation** with validation and signing support
- **GitHub Actions CI/CD** for automated package building
- **Comprehensive exclusion patterns** for clean repository archiving
- **Production-ready packaging** validated and tested

### âœ… Windows System Operations
- **Windows Services Management**: Start, stop, restart, list services with filtering
- **Windows Event Log Tools**: Query, export, monitor, and clear event logs
- **Windows Performance Monitoring**: Real-time performance counters and system metrics
- **Windows Permissions Management**: File/directory permissions analysis and modification

### âœ… Core Operations
- **PowerShell & CMD Execution**: Reliable command execution with output capture and error handling
- **File Operations**: Create, read, write, move, copy files and directories with comprehensive error handling
- **Archive Management**: Create/extract ZIP archives with intelligent exclusion patterns
- **JSON Tools**: Parse, validate, format, and query JSON files with JSONPath support
- **Media Metadata**: Extract metadata from images, audio, and video files
- **System Information**: Comprehensive OS, hardware, and environment reporting
- **Health Monitoring**: Built-in health checks and diagnostic tools

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx windows-operations-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "windows-operations-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/windows-operations-mcp", "run", "windows-operations-mcp"]
  }
}
```
### Option 1: MCPB Package (Recommended)

1. **Download the latest release** from the [GitHub Releases](https://github.com/sandraschi/windows-operations-mcp/releases) page
2. **Drag the `.mcpb` file** to Claude Desktop for automatic installation
3. **Follow the configuration prompts** to set up your preferences
4. **Restart Claude Desktop** to complete the installation

### Option 2: For Cursor IDE

**Important:** Cursor uses system Python. Install dependencies in the Python that Cursor uses:

```powershell
# Find system Python path (check Cursor error logs if needed)
# Example: C:\Users\sandr\AppData\Local\Programs\Python\Python310\python.exe
python -m uv pip install -e .
```

See `CURSOR_SETUP.md` for detailed Cursor configuration instructions.

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx windows-operations-mcp
```

### ðŸŽ¯ Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "windows-operations-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/windows-operations-mcp", "run", "windows-operations-mcp"]
  }
}
```
## ðŸ› ï¸ Development & Building

### Prerequisites

```bash
# Install MCPB CLI (official toolchain)
npm install -g @anthropic-ai/mcpb

# Install Python dependencies (EXACT VERSIONS)
pip install "fastmcp>=3.1.1+.0,<3.0.0"
uv pip install -r requirements.txt
```

### Repository Structure

```
windows-operations-mcp/
â”œâ”€â”€ mcpb/                          # MCPB configuration and manifest
â”‚   â”œâ”€â”€ manifest.json              # AI-generated runtime configuration
â”‚   â””â”€â”€ assets/                    # Icons, screenshots
â”œâ”€â”€ src/                           # Python source code
â”‚   â””â”€â”€ windows_operations_mcp/    # Main Python package
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ mcp_server.py          # Main server entry point
â”‚       â”œâ”€â”€ ai.py                  # SOTA AI Router
â”‚       â”œâ”€â”€ web.py                 # Integrated FastAPI bridge
â”‚       â””â”€â”€ tools/                 # Tool modules
â”œâ”€â”€ web_sota/                      # SOTA Vite Dashboard (Port 10749)
â”œâ”€â”€ scripts/                       # Build and utility scripts
â”‚   â””â”€â”€ build-mcp-package.ps1     # MCPB package builder
â”œâ”€â”€ docs/                          # Documentation
â”œâ”€â”€ requirements.txt               # Python dependencies
â””â”€â”€ README.md                      # This file
```

### Building MCPB Packages

```powershell
# Show help and available options
.\scripts\build-mcp-package.ps1 -Help

# Build and sign the package (default behavior)
.\scripts\build-mcp-package.ps1

# Build without signing (for development/testing)
.\scripts\build-mcp-package.ps1 -NoSign

# Specify custom output directory
.\scripts\build-mcp-package.ps1 -OutputDir "C:\builds"
```

### Local Development Workflow

```bash
# 1. AI-generate manifest.json (place in mcpb/manifest.json)
# ENSURE: fastmcp>=3.1.1+.0 in requirements.txt
# ENSURE: cwd: "src" and PYTHONPATH: "src" in mcp_config

# 2. Validate manifest
cd mcpb
mcpb validate manifest.json

# 3. Build MCPB package
mcpb pack . ../dist/package.mcpb

# 4. Test installation
# Drag dist/*.mcpb to Claude Desktop
```

## ðŸŽ¯ Available Tools

### Windows Services Management
- `list_windows_services` - List services with filtering
- `start_windows_service` - Start Windows services
- `stop_windows_service` - Stop Windows services
- `restart_windows_service` - Restart Windows services

### Windows Event Log Tools
- `query_windows_event_log` - Query event logs with filtering
- `export_windows_event_log` - Export event logs to files
- `clear_windows_event_log` - Clear event logs with backup
- `monitor_windows_event_log` - Real-time event log monitoring

### Windows Performance Monitoring
- `get_windows_performance_counters` - Query performance counters
- `monitor_windows_performance` - Monitor performance over time
- `get_windows_system_performance` - Comprehensive system metrics

### Windows Permissions Management
- `get_file_permissions` - Analyze file/directory permissions
- `set_file_permissions` - Modify file permissions
- `analyze_directory_permissions` - Bulk permission analysis
- `fix_file_permissions` - Fix common permission issues

### Archive Management (with exclusions)
- `create_archive` - Create archives with intelligent exclusions
- `extract_archive` - Extract archives
- `list_archive` - List archive contents

### Core Operations
- `run_powershell_tool` - Execute PowerShell commands
- `run_cmd_tool` - Execute CMD commands
- `read_file` / `write_file` - File operations
- `get_system_info` / `health_check` - System monitoring
- `get_help` - Tool documentation and help

## âš™ï¸ Configuration

### User Configuration Options

When installing the MCPB package, you can configure:

- **Working Directory**: Default directory for file operations
- **Log Level**: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
- **Performance Monitoring**: Enable detailed metrics collection

### Environment Variables

The server respects these environment variables:

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `PYTHONPATH`: Python module search path
- `PYTHONUNBUFFERED`: Force unbuffered output

## ðŸ”§ Troubleshooting

### Extension Fails to Start

**Symptoms:** Extension shows as failed in Claude Desktop settings.

**Common Causes:**
1. **Python Path Issues**: Incorrect `PYTHONPATH` configuration
2. **Missing Dependencies**: Required packages not installed
3. **Permission Issues**: Insufficient permissions for operations

**Solutions:**
1. **Check Python Path**: Ensure `PYTHONPATH` includes the `src` directory
2. **Verify Dependencies**: Run `uv pip install -r requirements.txt`
3. **Check Logs**: Review `%APPDATA%\Claude\logs\mcp-server-windows-operations.log`

### Manual Configuration Workaround

If the MCPB package fails to start, add a manual entry to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "windows-operations-manual": {
    "command": "python",
      "args": ["C:/Users/{YOUR_USERNAME}/AppData/Roaming/Claude/Claude Extensions/local.mcpb.sandraschi.windows-operations-mcp/src/windows_operations_mcp/server.py"],
      "cwd": "C:/Users/{YOUR_USERNAME}/AppData/Roaming/Claude/Claude Extensions/local.mcpb.sandraschi.windows-operations-mcp/src",
    "env": {
        "PYTHONPATH": "C:/Users/{YOUR_USERNAME}/AppData/Roaming/Claude/Claude Extensions/local.mcpb.sandraschi.windows-operations-mcp/src",
      "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

## ðŸ§ª Testing

### Test Coverage

The project maintains **comprehensive test coverage** across all components:

- **Unit Tests**: 16+ test modules covering all tools and utilities
- **Integration Tests**: MCP server integration testing
- **Coverage Reports**: HTML coverage reports generated automatically
- **Test Categories**: Archive tools, file operations, JSON tools, media tools, command execution

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage report
python -m pytest --cov=src --cov-report=html --cov-report=term

# Run specific test categories
python -m pytest tests/unit/tools/ -v           # Tool tests
python -m pytest tests/unit/utils/ -v           # Utility tests
python -m pytest tests/integration/ -v          # Integration tests

# Run with verbose output
python -m pytest -vv

# Run PowerShell test script
.\tests\run_tests.ps1
```

### Manual Testing

```bash
# Test MCP server directly
cd src
python -m windows_operations_mcp

# Test specific tools
python -c "
from windows_operations_mcp.tools.windows_services import list_windows_services
result = list_windows_services()
print('Services found:', len(result.get('services', [])))
"

# Test package build
.\scripts\build-mcp-package.ps1 -NoSign
```

## ðŸ¤ Contributing

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch**: `git checkout -b feature/new-tool`
4. **Install dependencies**: `uv pip install -r requirements.txt`
5. **Run tests**: `python -m pytest`
6. **Make your changes** with proper documentation
7. **Submit a pull request**

### Adding New Tools

1. **Create tool module** in `src/windows_operations_mcp/tools/`
2. **Implement tool functions** with proper decorators and documentation
3. **Add registration function** that registers tools with FastMCP
4. **Register in main server** by importing and calling the registration function
5. **Add tests** in `tests/unit/tools/`
6. **Update documentation** in this README

### Code Standards

- **Type Hints**: Use comprehensive type annotations
- **Error Handling**: Implement proper exception handling with logging
- **Documentation**: Use self-documenting multiline decorators
- **Testing**: Maintain >90% test coverage
- **Security**: Validate inputs and handle sensitive operations safely

## ðŸ“‹ MCPB Compliance Checklist

- âœ… **MCPB Manifest**: Proper `mcpb/manifest.json` with AI generation (v0.2 format)
- âœ… **Python Path Configuration**: Correct `PYTHONPATH` and `cwd` settings
- âœ… **FastMCP 3.1.1+.3**: Latest version requirement enforced
- âœ… **Exclusion Patterns**: Intelligent artifact exclusion for archiving
- âœ… **Self-Documenting Tools**: Comprehensive parameter and return documentation
- âœ… **Error Handling**: Robust error handling with detailed diagnostics
- âœ… **Build Process**: Automated MCPB package building with PowerShell scripts
- âœ… **CI/CD Integration**: GitHub Actions for automated testing and builds
- âœ… **Test Coverage**: Comprehensive unit and integration tests
- âœ… **Documentation**: Complete guides and examples

## ðŸ“„ License

MIT License - see LICENSE file for details.

## ðŸ†˜ Support & Resources

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/sandraschi/windows-operations-mcp/issues) - Bug reports and feature requests
- **Discussions**: [GitHub Discussions](https://github.com/sandraschi/windows-operations-mcp/discussions) - Community support
- **Documentation**: Check the `docs/` directory for comprehensive guides

### Documentation
- ðŸ“– **[Documentation Index](docs/README.md)** - Complete documentation guide
- ðŸ“– **[MCPB Building Guide](docs/mcp/MCPB_BUILDING_GUIDE.md)** - Package building instructions
- ðŸ“– **[Getting Started](docs/mcp/GETTING_STARTED.md)** - Quick start guide
- ðŸ“– **[Examples](docs/mcp/EXAMPLES.md)** - Usage examples
- ðŸ“– **[Repository Status](REPOSITORY_STATUS_REPORT.md)** - Current project status

### Quick Links
- **FastMCP Documentation**: [https://github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp)
- **Model Context Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Desktop**: [https://claude.ai/desktop](https://claude.ai/desktop)

## ðŸ“Š Project Status

**Version**: 0.2.0 ðŸŽ‰ (MCPB Release)  
**Status**: âœ… Production Ready  
**Health Score**: 9.0/10  
**Last Updated**: October 8, 2025

See [REPOSITORY_STATUS_REPORT.md](REPOSITORY_STATUS_REPORT.md) for detailed status information.

---

**Built with â¤ï¸ using FastMCP 3.1.1+.3 and MCPB standards**  
*Providing reliable Windows system operations through the Model Context Protocol*

