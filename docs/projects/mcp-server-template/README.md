# MCP Server Generator

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.2-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>


> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**🚀 Generate FastMCP 3.1.0+ compliant servers with stdio transport in seconds**

## Features

- ✅ Simple command-line interface
- ✅ Generates fully functional MCP servers
- ✅ Uses stdio transport for MCP client compatibility
- ✅ Includes example tools (help, hello)
- ✅ Proper Python package structure
- ✅ pyproject.toml with all necessary dependencies

## Quick Start

```powershell
git clone https://github.com/sandraschi/mcp-server-template
cd mcp-server-template
just
```

This opens an interactive dashboard showing all available commands. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start.

### Manual Setup

If you don't have `just` installed:
### 1. Generate a New MCP Server
# Generate a new server
python simple_gen.py MyServer
# Navigate to the server directory
cd mcp_myserver
# Install in development mode
uv pip install -e .
# Run the server
python -m myserver.server

## Server Structure

```
mcp_myserver/
├── pyproject.toml    # Project configuration
└── src/
    └── myserver/     # Your server package
        ├── __init__.py
        └── server.py # Main server implementation
```

## Available Tools

The generated server comes with two example tools:

1. `help()` - Shows available commands
2. `hello(name)` - Example tool that greets a user

## Development

### Adding New Tools

Edit `src/your_server_name/server.py` and add new tools using the `@app.tool` decorator:

```python
@app.tool
async def your_tool(param1: str, param2: int = 42) -> dict:
    """Documentation for your tool."""
    return {"result": f"Processed {param1} with {param2}"}
```

### Testing

1. Install test dependencies:
   ```bash
   pip install pytest
   ```

2. Run tests:
   ```bash
   python -m pytest tests/
   ```


## 🛡️ Industrial Quality Stack

This project adheres to **SOTA 14.1** industrial standards for high-fidelity agentic orchestration:

- **Python (Core)**: [Ruff](https://astral.sh/ruff) for linting and formatting. Zero-tolerance for `print` statements in core handlers (`T201`).
- **Webapp (UI)**: [Biome](https://biomejs.dev/) for sub-millisecond linting. Strict `noConsoleLog` enforcement.
- **Protocol Compliance**: Hardened `stdout/stderr` isolation to ensure crash-resistant JSON-RPC communication.
- **Automation**: [Justfile](./justfile) recipes for all fleet operations (`just lint`, `just fix`, `just dev`).
- **Security**: Automated audits via `bandit` and `safety`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/yourusername/fastmcp) - The MCP server framework
Restart Claude Desktop. Done.

## Examples

- `python generate_mcp_server.py "File Manager"`
- `python generate_mcp_server.py "Database Helper"`
- `python generate_mcp_server.py "API Client"`

Each generates a working MCP server with:
- ✅ FastMCP 3.1.0+ patterns
- ✅ Built-in testing
- ✅ Claude Desktop config
- ✅ Anti-pattern protection

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### 📦 Quick Start
Run immediately via `uvx`:
```bash
uvx mcp-generate
```

### 🎯 Claude Desktop Integration
Add to your `claude_desktop_config.json`:
```json
"mcpServers": {
  "mcp-generate": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/mcp-server-template", "run", "mcp-generate"]
  }
}
```
## Basic Usage

### Starting the Server (STDIO Mode Only)

```bash
# Start the MCP server
mcp-server

# Start with debug logging
MCP_DEBUG=1 mcp-server
```

### Available Tools (Basic Set)

- `list_tools`: List all available MCP tools
- `get_tool_info`: Get detailed information about a specific tool
- `get_server_info`: Get information about the MCP server
- `get_system_info`: Get basic system information
- `health_check`: Server health status

## Current Limitations

### **MCPB Packaging - NOT READY**
- `mcpb_pack/` directory is empty
- No manifest or build scripts
- Cannot package for Claude Desktop yet

### **Testing - NOT READY** 
- `tests/` directory is empty
- No test framework or examples
- Cannot verify server functionality

### **Prompt Templates - NOT READY**
- `prompts/` directory is empty  
- No tool prompt examples
- No Claude Desktop integration guides

### **Dual Transport - PARTIAL**
- Only STDIO transport implemented
- HTTP mode mentioned in config but not working
- No development/testing HTTP server

## Development Status

### **Estimated Completion Timeline:**
- **MCPB Packaging**: 2-3 days of development needed
- **Test Infrastructure**: 2 days of development needed  
- **Prompt Templates**: 1 day of development needed
- **Dual Transport**: 1 day of development needed
- **Documentation**: 1 day to complete missing sections

**Total**: ~7-8 days of focused development to complete template

### **Current Development Time:**
- **Basic MCP Server**: ~2-3 hours (what currently works)
- **Full Template Vision**: Not possible yet due to missing components

## Adding a New Tool (Current Process)

1. Create a new Python file in `src/mcp_server_template/tools/`
2. Define your tool function with the `@mcp.tool` decorator
3. Add proper type hints and docstring
4. Register the tool in `src/mcp_server_template/tools/__init__.py`

Example:
```python
# src/mcp_server_template/tools/example.py
from fastmcp import FastMCP

def register(mcp: FastMCP) -> None:
    @mcp.tool
    async def example_tool(text: str) -> str:
        """Example tool that echoes input.
        
        Args:
            text: Text to echo back
            
        Returns:
            The input text
        """
        return f"Echo: {text}"
```

## Known Issues

1. **Configuration Complexity**: Current config is overengineered for basic functionality
2. **Empty Directories**: Several directories claim features but contain no files
3. **Documentation Mismatch**: Some docs reference non-existent features
4. **No Integration Testing**: Cannot verify Claude Desktop compatibility

## Contributing

This template needs significant work to be production-ready. Priority areas:

1. **Implement MCPB packaging** (highest priority)
2. **Create test infrastructure** 
3. **Add prompt templates**
4. **Complete dual transport**
5. **Simplify configuration**

See `docs/WINDSURF_FIXING_PLAN.md` for detailed implementation plan.

## Architecture

```text
mcp-server-template/
├── src/mcp_server_template/     # Main implementation (WORKING)
│   ├── tools/                   # Tool implementations (BASIC)
│   ├── utils/                   # Utilities (WORKING)
│   └── main.py                  # Entry point (WORKING)
├── tests/                       # Test suite (EMPTY - NEEDS WORK)
├── mcpb_pack/                    # MCPB packaging (EMPTY - NEEDS WORK)
├── prompts/                     # Prompt templates (EMPTY - NEEDS WORK)
├── docs/                        # Documentation (PARTIAL)
└── pyproject.toml              # Project config (WORKING)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/yourusername/fastmcp) - The MCP server framework
- Based on MCP protocol standards for Claude Desktop integration

---

**⚠️ Important**: This template is a work in progress. Do not use for production until missing components are implemented. See assessment documents in `docs/` for detailed status.
