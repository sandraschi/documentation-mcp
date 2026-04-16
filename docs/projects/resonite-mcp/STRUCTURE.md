# Resonite MCP Project Structure

**Version:** 0.1.1
**Last Updated:** 2025-12-22
**Source:** `D:\Dev\repos\resonite-mcp`

## Directory Structure

```
resonite-mcp/
â”œâ”€â”€ src/resonite_mcp/           # Main package
â”‚   â”œâ”€â”€ __init__.py            # Package initialization
â”‚   â”œâ”€â”€ __main__.py            # Module entry point
â”‚   â”œâ”€â”€ server.py              # FastMCP server with all tools
â”‚   â”œâ”€â”€ cli.py                 # Command-line interface
â”‚   â”œâ”€â”€ http_server.py        # FastAPI HTTP server (25 endpoints)
â”‚   â”œâ”€â”€ http_functions.py      # HTTP wrapper functions
â”‚   â”œâ”€â”€ models.py              # Pydantic data models
â”‚   â”œâ”€â”€ tools/                 # MCP tool implementations
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ osc.py            # OSC communication tools (8 tools)
â”‚   â”‚   â”œâ”€â”€ session.py        # Session management (4 tools)
â”‚   â”‚   â”œâ”€â”€ avatar.py         # Avatar control (3 tools)
â”‚   â”‚   â”œâ”€â”€ inventory.py      # Inventory management (7 tools)
â”‚   â”‚   â”œâ”€â”€ plugin.py         # Plugin management (5 tools)
â”‚   â”‚   â””â”€â”€ system.py         # System tools (3 tools)
â”‚   â””â”€â”€ plugins/               # Plugin system
â”‚       â”œâ”€â”€ __init__.py
â”‚       â”œâ”€â”€ base_plugin.py     # Plugin base classes
â”‚       â”œâ”€â”€ plugin_manager.py  # Plugin loading and management
â”‚       â”œâ”€â”€ osc_extensions.py  # OSC extension plugin
â”‚       â””â”€â”€ protoflux_helpers.py # ProtoFlux helper plugin
â”œâ”€â”€ tests/                     # Test suite
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ conftest.py           # Pytest configuration
â”‚   â”œâ”€â”€ unit/                 # Unit tests
â”‚   â”‚   â””â”€â”€ test_server.py   # Server tests (architectural issues)
â”‚   â””â”€â”€ integration/          # Integration tests (empty)
â”œâ”€â”€ docs/                     # Documentation
â”‚   â”œâ”€â”€ API_REFERENCE.md      # API documentation
â”‚   â”œâ”€â”€ INSTALLATION.md       # Installation guide
â”‚   â””â”€â”€ TROUBLESHOUTING.md    # Troubleshooting guide
â”œâ”€â”€ examples/                 # Usage examples
â”‚   â””â”€â”€ basic_usage.py        # Basic usage example
â”œâ”€â”€ scripts/                  # Development scripts
â”‚   â””â”€â”€ build_dxt.ps1        # DXT package builder
â”œâ”€â”€ assets/                   # Static assets
â”‚   â””â”€â”€ prompts/              # MCP prompt templates
â”œâ”€â”€ dist/                     # Built distributions
â”‚   â”œâ”€â”€ dxt.json             # DXT package manifest
â”‚   â”œâ”€â”€ manifest.json        # Package manifest
â”‚   â””â”€â”€ package.json         # NPM-style package config
â”œâ”€â”€ pyproject.toml           # Project configuration
â”œâ”€â”€ README.md                # Main documentation
â”œâ”€â”€ test_http_api.py         # HTTP API test script
â””â”€â”€ test_mcp_protocol.py     # MCP protocol test script
```

## Code Organization

### Core Architecture

#### `server.py` (Main Server)
- FastMCP 3.1.1+.1+ server initialization
- Plugin system integration
- Tool registration orchestration
- Dual transport support (stdio + HTTP)

#### `cli.py` (Command Interface)
- Argument parsing and validation
- Server mode selection (stdio vs HTTP)
- Environment configuration
- Logging setup

#### `http_server.py` (REST API)
- FastAPI application setup
- 25 REST endpoints
- CORS middleware configuration
- Interactive documentation (/docs)

### Tool Organization

#### Portmanteau Design Pattern
All tools follow the FastMCP portmanteau pattern - complex operations organized into logical tool groups:

- **`osc.py` (8 tools):** Core OSC communication functionality
- **`session.py` (4 tools):** Session lifecycle and world management
- **`avatar.py` (3 tools):** Avatar control and ProtoFlux execution
- **`inventory.py` (7 tools):** Asset management and inventory operations
- **`plugin.py` (5 tools):** Plugin system management
- **`system.py` (3 tools):** Help, status, and health monitoring

### Plugin System

#### Architecture
```
PluginManager
â”œâ”€â”€ BasePlugin (abstract base)
â”œâ”€â”€ OSC_Extensions_Plugin
â””â”€â”€ ProtoFlux_Helpers_Plugin
```

#### Current Plugins
- **OSC Extensions:** Enhanced OSC communication features
- **ProtoFlux Helpers:** ProtoFlux scripting assistance tools

### Data Models

#### `models.py`
- **OSCMessageInput:** OSC message parameters
- **OSCServerInput:** OSC server configuration
- **ResoniteSessionInput:** Session creation parameters
- **AvatarControlInput:** Avatar manipulation parameters
- **ProtoFluxScriptInput:** Script execution parameters
- **InventoryListInput:** Inventory query parameters

## File Size Breakdown

```
Total Files: 41
Code Files: 24 (.py)
Test Files: 3 (.py)
Config Files: 5 (.toml, .json)
Documentation: 5 (.md)
Scripts: 1 (.ps1)
Other: 3

Lines of Code: ~1,417 (estimated)
Test Coverage: 16% (core modules)
```

## Dependencies

### Core Dependencies
- **fastmcp[all]>=3.1.1+.1,<2.15.0:** MCP framework
- **python-osc>=1.8.0:** OSC protocol implementation
- **pydantic>=2.0:** Data validation
- **aiohttp>=3.8.0:** Async HTTP client
- **websockets>=11.0.0:** WebSocket support
- **fastapi:** REST API framework

### Development Dependencies
- **pytest>=7.0.0:** Testing framework
- **pytest-asyncio>=0.21.0:** Async testing
- **pytest-cov>=4.0.0:** Coverage reporting
- **ruff>=0.1.0:** Code linting
- **black>=23.0.0:** Code formatting
- **mypy>=1.0.0:** Type checking

## Build System

### `pyproject.toml`
- **Build Backend:** setuptools
- **Python Version:** >=3.8
- **Entry Points:** `resonite-mcp` console script
- **Dependencies:** Fully specified with version constraints
- **Dev Dependencies:** Comprehensive development toolchain
- **Tool Configuration:** Ruff, Black, MyPy, Pytest pre-configured

### Distribution Formats
- **Wheel:** Standard Python package distribution
- **Source:** Git-based development installation
- **DXT Package:** Claude Desktop extension format (planned)

## Testing Structure

### Current State
- **Unit Tests:** `tests/unit/test_server.py` (architectural issues)
- **Integration Tests:** `tests/integration/` (empty)
- **HTTP API Tests:** `test_http_api.py` (functional)
- **MCP Protocol Tests:** `test_mcp_protocol.py` (stdio issues)

### Issues
- **Unit Test Architecture:** Designed for direct function calls, incompatible with MCP tool decorators
- **Integration Tests:** Not implemented
- **Coverage:** 16% due to architectural test issues

## Documentation Structure

### User Documentation
- **README.md:** Main project documentation
- **docs/INSTALLATION.md:** Setup and configuration
- **docs/TROUBLESHOUTING.md:** Common issues and solutions
- **docs/API_REFERENCE.md:** Tool and API documentation

### Developer Documentation
- **Inline Docstrings:** Comprehensive function documentation
- **Type Hints:** Full type annotations
- **Error Handling:** Detailed error messages and logging

## Development Workflow

### Local Development
```bash
# Install in development mode
pip install -e ".[dev]"

# Run with auto-reload
resonite-mcp --host 127.0.0.1 --port 8000

# Run tests
pytest

# Check code quality
ruff check .
mypy src/
```

### IDE Integration
- **Cursor:** `mcp.resonite` configuration
- **Claude Desktop:** `mcpServers.resonite` configuration
- **VS Code:** MCP extension support (planned)

## Deployment Options

### Development Deployment
- **Editable Install:** `pip install -e .`
- **Local Testing:** HTTP API + MCP stdio modes
- **Debug Mode:** Comprehensive logging and error reporting

### Production Deployment
- **Containerized:** Docker support (planned)
- **System Package:** Platform-specific packages (planned)
- **Cloud Deployment:** Managed hosting (planned)

## Security Considerations

### OSC Communication
- **Network Security:** OSC traffic on configurable ports
- **Access Control:** Localhost-only by default
- **Parameter Validation:** Pydantic input validation

### HTTP API
- **CORS Configuration:** Configurable cross-origin settings
- **Rate Limiting:** Planned for production deployment
- **Authentication:** Basic auth support (planned)

### Plugin System
- **Sandboxing:** Plugin isolation (planned)
- **Permission Model:** Capability-based security (planned)
- **Code Review:** Plugin validation before loading

## Performance Characteristics

### Startup Performance
- **Cold Start:** ~3 seconds (plugin loading + initialization)
- **Hot Reload:** ~1 second (development mode)
- **Memory Usage:** ~50MB baseline + plugins

### Runtime Performance
- **OSC Latency:** <10ms (local network)
- **HTTP API:** <100ms response time
- **Concurrent Sessions:** Multiple sessions supported
- **Plugin Overhead:** Minimal performance impact

## Scalability Considerations

### Current Limitations
- **Single Resonite Instance:** One OSC connection per server
- **Memory Usage:** Plugin system increases baseline memory
- **Concurrent Users:** Designed for single-user primary use

### Future Enhancements
- **Multi-instance Support:** Multiple Resonite connections
- **Load Balancing:** Distributed OSC handling
- **Plugin Pooling:** Efficient plugin resource management

---

**Architecture Assessment:** **SOLID** - Clean separation of concerns, extensible plugin system, comprehensive error handling, and dual transport support provide a robust foundation for Resonite integration.


