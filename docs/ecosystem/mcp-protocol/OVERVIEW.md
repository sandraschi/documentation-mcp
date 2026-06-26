# MCP Protocol Overview

**Last Updated:** 2025-11-25  
**Status:** Active  
**Official Docs:** https://modelcontextprotocol.io/

---

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that enables AI assistants (like Claude) to connect to external tools, data sources, and services.

Think of it as a **universal plugin system** for AI.

---

## Key Concepts

### MCP Server
A program that exposes **tools**, **resources**, and **prompts** to an AI client.

```
┌─────────────────────┐
│     MCP Server      │
├─────────────────────┤
│ • Tools (actions)   │
│ • Resources (data)  │
│ • Prompts (templates)│
└─────────────────────┘
```

### MCP Client
An AI application that connects to MCP servers (e.g., Claude Desktop, Cursor).

### Transport
How client and server communicate:
- **stdio** - Standard input/output (most common for local)
- **HTTP/HTTPS** - REST API (for remote servers, testing)
- **SSE** - Server-sent events (for streaming)
- **WebSocket** - Bidirectional streaming

**See [TRANSPORTS.md](TRANSPORTS.md) for detailed comparison and implementation guides.**

---

## The Three Primitives

### 1. Tools
**Actions** the AI can perform.

```python
@mcp.tool()
async def send_email(to: str, subject: str, body: str) -> str:
    '''Send an email to the specified recipient.'''
    # Implementation
    return "Email sent"
```

### 2. Resources
**Data** the AI can read.

```python
@mcp.resource("config://settings")
async def get_settings() -> str:
    '''Return current configuration.'''
    return json.dumps(settings)
```

### 3. Prompts
**Templates** for common interactions.

```python
@mcp.prompt()
async def code_review() -> str:
    '''Prompt for reviewing code quality.'''
    return "Review this code for bugs, style, and performance..."
```

---

## How It Works

```
User: "Send an email to bob@example.com"
         │
         ▼
┌─────────────────────────────────────────┐
│            Claude Desktop               │
│  1. Understands user intent             │
│  2. Finds matching tool (send_email)    │
│  3. Calls MCP server via stdio          │
└─────────────────┬───────────────────────┘
                  │ JSON-RPC
                  ▼
┌─────────────────────────────────────────┐
│            MCP Server                   │
│  4. Receives tool call                  │
│  5. Executes send_email()               │
│  6. Returns result                      │
└─────────────────┬───────────────────────┘
                  │
                  ▼
User: "Email sent successfully!"
```

---

## Why MCP?

| Before MCP | With MCP |
|------------|----------|
| Each AI app builds custom integrations | Universal protocol for all |
| Fragmented ecosystem | Standardized approach |
| Tools locked to specific AI | Tools work across AI apps |
| Complex API wrappers | Simple tool definitions |

---

## Getting Started

### Building a Server
Use **FastMCP** (Python) - see `../fastmcp/`

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def hello(name: str) -> str:
    '''Say hello to someone.'''
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

### Configuring Claude Desktop
Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"]
    }
  }
}
```

---

## Resources

- **Official Spec:** https://modelcontextprotocol.io/
- **Transport Methods:** [TRANSPORTS.md](TRANSPORTS.md) - Stdio, HTTP, SSE, WebSocket
- **FastMCP Guide:** `../fastmcp/`
- **Server Registry:** `../glama/`
- **Packaging:** `../mcpb/`

