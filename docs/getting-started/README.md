# Getting Started with MCP

**Last Updated:** 2025-12-04

Welcome! This guide will get you building MCP servers in **5 minutes**.

---

## 🚀 What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how applications provide context to LLMs. Think of it as a **USB port for AI** - a universal way to connect AI assistants to data and tools.

### Why MCP?

- **Universal**: Works with Claude Desktop, custom apps, any LLM client
- **Secure**: Controlled access to resources
- **Composable**: Mix and match servers
- **Simple**: Build powerful tools in minutes

---

## 🎯 Quick Start (5 Minutes)

### Prerequisites

```powershell
# Python 3.11+
python --version

# Pip
pip --version
```

### Step 1: Install FastMCP

```powershell
pip install "fastmcp>=3.4.4"
```

### Step 2: Create Your First Server

Create `my_server.py`:

```python
from fastmcp import FastMCP

# Initialize server
mcp = FastMCP("My First Server")

# Add a simple tool
@mcp.tool()
def greet(name: str) -> str:
    """Greet someone by name"""
    return f"Hello, {name}!"

# Add a resource
@mcp.resource("greeting://welcome")
def welcome_message() -> str:
    """Welcome message resource"""
    return "Welcome to MCP!"
```

### Step 3: Test It

```powershell
# Run in development mode
fastmcp dev my_server.py
```

You should see:
```
✓ Server started successfully
✓ Tools: 1 (greet)
✓ Resources: 1 (greeting://welcome)
```

### Step 4: Connect to Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-first-server": {
      "command": "python",
      "args": ["-m", "fastmcp", "run", "D:/path/to/my_server.py"]
    }
  }
}
```

Restart Claude Desktop. You're done! 🎉

---

## 📖 Next Steps

### Learn the Protocol
→ [../protocol/README.md](../protocol/README.md) - Understand MCP fundamentals  
→ [../protocol/TRANSPORTS.md](../protocol/TRANSPORTS.md) - Stdio vs HTTP vs SSE vs WebSocket

### Master FastMCP
→ [../fastmcp/README.md](../fastmcp/README.md) - Complete FastMCP guide  
→ [../fastmcp/3.1-features.md](../fastmcp/3.1-features.md) - Current features (Prompts, Skills, CodeMode)

### Deploy to Production
→ [../deployment/README.md](../deployment/README.md) - Production deployment  
→ [../docker/README.md](../docker/README.md) - Docker containerization

### Learn Patterns
→ [../patterns/README.md](../patterns/README.md) - Design patterns  
→ [../patterns/MCP_ORPHAN_GUARD_PATTERN.md](../patterns/MCP_ORPHAN_GUARD_PATTERN.md) - Prevent zombie processes

---

## 🔧 Common Tasks

### Add a Tool with Parameters

```python
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform basic math operations
    
    Args:
        operation: One of: add, subtract, multiply, divide
        a: First number
        b: Second number
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else 0.0
```

### Add a Resource

```python
@mcp.resource("config://settings")
def get_config() -> dict:
    """Application configuration"""
    return {
        "version": "1.0.0",
        "debug": True
    }
```

### Add State (Persistent Storage)

```python
from fastmcp import Context

@mcp.tool()
def remember(ctx: Context, key: str, value: str) -> str:
    """Remember a value"""
    ctx.state[key] = value
    return f"Remembered {key} = {value}"

@mcp.tool()
def recall(ctx: Context, key: str) -> str:
    """Recall a remembered value"""
    return ctx.state.get(key, "Not found")
```

### Error Handling

```python
from fastmcp import FastMCP
from typing import Optional

@mcp.tool()
def divide_safe(a: float, b: float) -> Optional[float]:
    """Divide two numbers safely
    
    Returns None if division by zero
    """
    if b == 0:
        return None
    return a / b
```

---

## 🎨 Choose Your Transport

### Stdio (Local Development)
**Best for:** Local Claude Desktop, testing, simple tools

```json
{
  "command": "python",
  "args": ["-m", "fastmcp", "run", "server.py"]
}
```

### HTTP (Remote/Production)
**Best for:** Remote servers, web apps, multiple clients

```python
# Start HTTP server
mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

→ See [../protocol/TRANSPORTS.md](../protocol/TRANSPORTS.md) for complete guide

---

## 📚 Templates

### Use the Generator Script

```powershell
cd D:\Dev\repos\mcp-central-docs\templates\scripts
.\new-mcp-server.ps1 -ProjectName "my-awesome-server"
```

This creates a complete server with:
- FastMCP 3.1+ setup
- Docker configuration
- CI/CD workflows
- Documentation templates
- Testing structure

---

## 🆘 Troubleshooting

### Server Not Appearing in Claude Desktop

1. Check `%APPDATA%\Claude\claude_desktop_config.json` syntax
2. Check Python path: `where python`
3. Restart Claude Desktop completely
4. Check Claude logs: `%APPDATA%\Claude\logs\`

### Import Errors

```powershell
# Upgrade FastMCP
pip install --upgrade "fastmcp>=3.4.4"

# Check installation
python -c "import fastmcp; print(fastmcp.__version__)"
```

### Tool Not Working

```python
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)

@mcp.tool()
def my_tool(arg: str) -> str:
    logging.debug(f"Tool called with: {arg}")
    return f"Result: {arg}"
```

→ More troubleshooting: [../troubleshooting/README.md](../troubleshooting/README.md)

---

## 🎓 Learning Path

### Beginner (Day 1)
1. ✅ Quick Start (above)
2. Read [what-is-mcp.md](what-is-mcp.md)
3. Build 2-3 simple tools
4. Test in Claude Desktop

### Intermediate (Week 1)
1. Read [../protocol/README.md](../protocol/README.md)
2. Learn [../fastmcp/3.1-features.md](../fastmcp/3.1-features.md)
3. Add resources and prompts
4. Implement state management

### Advanced (Month 1)
1. Study [../patterns/](../patterns/)
2. Add HTTP transport
3. Containerize with [../docker/](../docker/)
4. Set up monitoring [../../monitoring/](../../monitoring/)

### Expert (Month 3+)
1. Implement portmanteau pattern
2. Add orphan guard protection
3. MCPB packaging
4. Publish to Glama registry

---

## 🔗 Essential Links

| Resource | Purpose |
|----------|---------|
| [FastMCP Docs](../fastmcp/README.md) | Complete FastMCP guide |
| [Protocol](../protocol/README.md) | MCP protocol basics |
| [Patterns](../patterns/README.md) | Design patterns |
| [Deployment](../deployment/README.md) | Production deployment |
| [Docker](../docker/README.md) | Containerization |
| [Troubleshooting](../troubleshooting/README.md) | Common issues |

---

## 🤝 Community

- **Official MCP**: https://modelcontextprotocol.io
- **FastMCP**: https://github.com/jlowin/fastmcp
- **Glama Registry**: https://glama.ai/mcp/servers

---

**Ready to build something awesome?** 🚀

Start with the [Quick Start](#-quick-start-5-minutes) above, then explore [../protocol/README.md](../protocol/README.md) to understand how MCP works!

