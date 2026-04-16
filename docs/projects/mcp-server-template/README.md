# MCP Server Generator

**ðŸš€ Generate FastMCP 3.1.1++ compliant servers with stdio transport in seconds**

## Features

- âœ… Simple command-line interface
- âœ… Generates fully functional MCP servers
- âœ… Uses stdio transport for MCP client compatibility
- âœ… Includes example tools (help, hello)
- âœ… Proper Python package structure
- âœ… pyproject.toml with all necessary dependencies

## Quick Start

### 1. Generate a New MCP Server

```bash
# Generate a new server
python simple_gen.py MyServer

# Navigate to the server directory
cd mcp_myserver

# Install in development mode
uv pip install -e .

# Run the server
python -m myserver.server
```

## Server Structure

```
mcp_myserver/
â”œâ”€â”€ pyproject.toml    # Project configuration
â””â”€â”€ src/
    â””â”€â”€ myserver/     # Your server package
        â”œâ”€â”€ __init__.py
        â””â”€â”€ server.py # Main server implementation
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
- âœ… FastMCP 3.1.1++ patterns
- âœ… Built-in testing
- âœ… Claude Desktop config
- âœ… Anti-pattern protection

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

## ðŸš€ Installation

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (RECOMMENDED)
- Python 3.12+

### ðŸ“¦ Quick Start
Run immediately via `uvx`:
```bash
uvx mcp-generate
```

### ðŸŽ¯ Claude Desktop Integration
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
â”œâ”€â”€ src/mcp_server_template/     # Main implementation (WORKING)
â”‚   â”œâ”€â”€ tools/                   # Tool implementations (BASIC)
â”‚   â”œâ”€â”€ utils/                   # Utilities (WORKING)
â”‚   â””â”€â”€ main.py                  # Entry point (WORKING)
â”œâ”€â”€ tests/                       # Test suite (EMPTY - NEEDS WORK)
â”œâ”€â”€ mcpb_pack/                    # MCPB packaging (EMPTY - NEEDS WORK)
â”œâ”€â”€ prompts/                     # Prompt templates (EMPTY - NEEDS WORK)
â”œâ”€â”€ docs/                        # Documentation (PARTIAL)
â””â”€â”€ pyproject.toml              # Project config (WORKING)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastMCP](https://github.com/yourusername/fastmcp) - The MCP server framework
- Based on MCP protocol standards for Claude Desktop integration

---

**âš ï¸ Important**: This template is a work in progress. Do not use for production until missing components are implemented. See assessment documents in `docs/` for detailed status.

