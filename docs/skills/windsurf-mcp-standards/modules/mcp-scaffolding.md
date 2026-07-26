# MCP Server Scaffolding Standards

## Overview
Standards for creating new MCP servers from scratch, including project structure, initial setup, and foundational patterns.

## Project Structure Requirements

### Required Files
```
mcp-server-name/
├── src/mcp_server_name/
│   ├── __init__.py
│   ├── server.py          # Main FastMCP server
│   └── tools/            # Tool implementations
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── docs/
│   ├── README.md
│   └── integration-guide.md
├── pyproject.toml
├── .cursorrules
├── .cursorignore
└── README.md
```

### Naming Conventions
- **Package**: `snake_case` (e.g., `blender_mcp`)
- **Tools**: `snake_case` with domain prefix (e.g., `blender_create_mesh`)
- **Classes**: `PascalCase` (e.g., `BlenderToolManager`)

## FastMCP Server Template

### Basic Server Structure
```python
from fastmcp import FastMCP

# Initialize server
app = FastMCP(
    name="server-name",
    instructions="Server purpose and capabilities",
    version="1.0.0"
)

# Tool implementations
@app.tool()
async def example_tool(param: str) -> dict:
    """Tool description with Args and Returns sections."""
    return {"result": f"processed {param}"}

# Resource implementations
@app.resource("resource://{type}/{id}")
async def get_resource(type: str, id: str) -> str:
    """Resource description."""
    return f"Resource content for {type}/{id}"

if __name__ == "__main__":
    import mcp.server.stdio
    mcp.server.stdio.run_server(app.to_server())
```

## Initial Setup Checklist

### 1. Package Configuration
- [ ] `pyproject.toml` with FastMCP 3.2+ dependency
- [ ] Proper package metadata and keywords
- [ ] Development dependencies (pytest, ruff, mypy)

### 2. Code Quality Setup
- [ ] Type hints throughout codebase
- [ ] Ruff configuration for formatting/linting
- [ ] MyPy configuration for type checking
- [ ] Pre-commit hooks for quality gates

### 3. Testing Infrastructure
- [ ] Basic server startup test
- [ ] Tool functionality tests
- [ ] Error handling tests
- [ ] Async operation tests

### 4. Documentation
- [ ] Complete README with installation/usage
- [ ] Tool documentation with examples
- [ ] Integration guide for different IDEs
- [ ] API reference documentation

## Domain-Specific Scaffolding

### Creative Tools (Blender, GIMP, Inkscape)
```python
# Sampling-enabled server structure
from fastmcp import FastMCP
from typing import Dict, Any

app = FastMCP(
    name="creative-mcp",
    instructions="Creative tool integration with AI sampling workflows"
)

@app.tool()
async def sample_workflow(iterations: int = 5) -> Dict[str, Any]:
    """Implement sampling pattern for creative AI workflows."""
    # Implementation following sampling standards
    pass
```

### Infrastructure Tools
```python
# Infrastructure server with monitoring
app = FastMCP(
    name="infra-mcp",
    instructions="Infrastructure monitoring and management"
)

@app.tool()
async def get_system_status() -> Dict[str, Any]:
    """System health and metrics."""
    # Implementation with proper error handling
    pass
```

## Testing Templates

### Server Startup Test
```python
import pytest
from mcp_server_name.server import app

def test_server_initialization():
    """Test that server initializes without errors."""
    assert app.name == "server-name"
    assert len(app.list_tools()) >= 0
```

### Tool Integration Test
```python
@pytest.mark.asyncio
async def test_tool_execution():
    """Test tool executes successfully."""
    result = await app.call_tool("example_tool", {"param": "test"})
    assert "result" in result
```

## Common Pitfalls to Avoid

### ❌ Don't Do This
- Hardcoded paths or URLs
- Synchronous operations in async functions
- Missing error handling
- Inadequate logging
- No input validation

### ✅ Do This Instead
- Use pathlib for cross-platform paths
- Proper async/await patterns
- Structured error responses
- Comprehensive logging
- Pydantic models for validation

## Next Steps
After scaffolding, proceed to:
1. [Tool Implementation Standards](./tool-implementation.md)
2. [Testing Standards](./testing.md)
3. [Documentation Standards](./documentation.md)
4. [Packaging Standards](./packaging.md)