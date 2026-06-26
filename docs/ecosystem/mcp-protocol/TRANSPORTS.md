# MCP Transport Methods

**Last Updated:** 2025-12-03  
**Status:** Active  
**Official Spec:** https://spec.modelcontextprotocol.io/specification/basic/transports/

---

## Overview

The Model Context Protocol (MCP) supports **multiple transport methods** for client-server communication. All are part of the official Anthropic standard.

```
┌─────────────────────────────────────────────────────────┐
│               MCP Protocol Layer                        │
│       (Tools, Resources, Prompts - JSON-RPC)           │
└─────────────────┬───────────────────────────────────────┘
                  │
        ┌─────────┼─────────┬─────────────┐
        │         │         │             │
   ┌────▼───┐ ┌──▼───┐ ┌───▼────┐  ┌────▼─────┐
   │ Stdio  │ │ HTTP │ │  SSE   │  │WebSocket │
   │        │ │HTTPS │ │        │  │          │
   └────────┘ └──────┘ └────────┘  └──────────┘
```

All transports use **JSON-RPC 2.0** for message formatting.

---

## 1. Stdio Transport

**Status:** ✅ Primary method, most common  
**Use Case:** Local process spawning

### How It Works

The MCP client spawns the server process and communicates via **standard input/output** (stdin/stdout).

```
┌──────────────────────────────────────────┐
│          MCP Client                      │
│   (Claude Desktop, Cursor, etc.)         │
│                                          │
│  1. Spawns: python server.py             │
│  2. Connects to process stdin/stdout     │
│  3. Sends JSON-RPC via stdin  ────────►  │
│  4. Receives JSON-RPC via stdout ◄────── │
└──────────────────────────────────────────┘
                  │
                  │ Process stdio
                  │
┌──────────────────────────────────────────┐
│          MCP Server Process              │
│                                          │
│  - Reads JSON-RPC from stdin             │
│  - Executes tools                        │
│  - Writes JSON-RPC to stdout             │
└──────────────────────────────────────────┘
```

### Implementation (FastMCP)

**Server Side:**
```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def example_tool(param: str) -> dict:
    """Example tool"""
    return {"result": param}

if __name__ == "__main__":
    # Run in stdio mode (default)
    mcp.run(transport="stdio")
```

**Client Side:**
```python
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

# Spawn server process and connect via stdio
transport = StdioTransport(
    command="python",
    args=["server.py"],
    env=os.environ.copy()
)

client = Client(transport)

async with client:
    await client.initialize()
    result = await client.call_tool("example_tool", param="test")
```

### Configuration (Claude Desktop)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["path/to/server.py"],
      "env": {
        "API_KEY": "secret"
      }
    }
  }
}
```

### Pros & Cons

**Pros:**
- ✅ Simple - no network configuration needed
- ✅ Secure - process-level isolation
- ✅ Fast - no network overhead
- ✅ Standard - supported by all MCP clients

**Cons:**
- ❌ Local only - can't access remote servers
- ❌ Platform-specific - harder to containerize
- ❌ No load balancing or scaling

---

## 2. HTTP/HTTPS Transport

**Status:** ✅ Fully supported by Anthropic standard  
**Use Case:** Remote servers, testing, non-MCP clients

### How It Works

The MCP server runs as an **HTTP service**. Clients make HTTP requests to call tools.

```
┌──────────────────────────────────────────┐
│          MCP Client                      │
│   (Any HTTP client)                      │
│                                          │
│  POST /mcp/v1/tools/call ────────────►   │
│  {                                       │
│    "tool": "example_tool",               │
│    "params": {"param": "test"}           │
│  }                                       │
│                                          │
│  ◄──────── Response                     │
└──────────────────────────────────────────┘
                  │
                  │ HTTP/HTTPS
                  │
┌──────────────────────────────────────────┐
│          MCP Server (HTTP)               │
│   Running on host:port                   │
│                                          │
│  - Receives HTTP POST requests           │
│  - Executes tools                        │
│  - Returns HTTP JSON responses           │
└──────────────────────────────────────────┘
```

### Implementation (FastMCP + FastAPI)

**Server Side:**
```python
from fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn

mcp = FastMCP("my-server")

@mcp.tool()
def example_tool(param: str) -> dict:
    """Example tool"""
    return {"result": param}

# Create HTTP interface
app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp/v1/tools/list")
async def list_tools():
    tools = [{"name": name, "description": func.__doc__} 
             for name, func in mcp._tools.items()]
    return {"tools": tools}

@app.post("/mcp/v1/tools/call")
async def call_tool(request: dict):
    tool_name = request["tool"]
    params = request.get("params", {})
    result = await mcp._tools[tool_name](**params)
    return {"success": True, "result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
```

**Client Side:**
```python
import httpx

async def call_mcp_tool(url: str, tool_name: str, params: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{url}/mcp/v1/tools/call",
            json={"tool": tool_name, "params": params}
        )
        return response.json()

# Usage
result = await call_mcp_tool(
    "https://server.example.com:3000",
    "example_tool",
    {"param": "test"}
)
```

### Testing with curl

```bash
# Start HTTP server
python server.py --http 3000

# Health check
curl http://localhost:3000/health

# List tools
curl -X POST http://localhost:3000/mcp/v1/tools/list

# Call tool
curl -X POST http://localhost:3000/mcp/v1/tools/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "example_tool", "params": {"param": "test"}}'
```

### Pros & Cons

**Pros:**
- ✅ Remote access - can be on different machines
- ✅ Language agnostic - any HTTP client works
- ✅ Testable - use curl/Postman
- ✅ Scalable - load balancers, multiple instances
- ✅ Cloud-friendly - works in Kubernetes, Docker

**Cons:**
- ❌ Network overhead - slower than stdio
- ❌ Security - need HTTPS, auth, rate limiting
- ❌ Complexity - must manage server lifecycle

---

## 3. SSE Transport (Server-Sent Events)

**Status:** ✅ Supported for streaming  
**Use Case:** Long-running operations, progress updates

### How It Works

Uses **HTTP with SSE** for server-to-client streaming.

```
┌──────────────────────────────────────────┐
│          MCP Client                      │
│                                          │
│  Connects to SSE endpoint                │
│  ◄───── Stream of events                │
│  {                                       │
│    "event": "progress",                  │
│    "data": {"percent": 50}               │
│  }                                       │
└──────────────────────────────────────────┘
                  │
                  │ SSE Stream
                  │
┌──────────────────────────────────────────┐
│          MCP Server (SSE)                │
│                                          │
│  - Maintains open connection             │
│  - Streams events as they occur          │
│  - Client receives in real-time          │
└──────────────────────────────────────────┘
```

**Best for:**
- Progress updates during long operations
- Real-time notifications
- Streaming large responses

---

## 4. WebSocket Transport

**Status:** ✅ Supported for bidirectional streaming  
**Use Case:** Interactive sessions, chat-like interfaces

Similar to SSE but **bidirectional** - both client and server can send messages at any time.

---

## Dual Interface Servers

**Best practice:** Support BOTH stdio AND HTTP in the same server.

### Implementation Pattern

```python
from fastmcp import FastMCP
from fastapi import FastAPI
import uvicorn
import sys

mcp = FastMCP("dual-interface-server")

@mcp.tool()
def example_tool(param: str) -> dict:
    """Works in both modes"""
    return {"result": param}

# HTTP interface
app = FastAPI()

@app.post("/mcp/v1/tools/call")
async def call_tool(request: dict):
    tool_name = request["tool"]
    params = request.get("params", {})
    result = await mcp._tools[tool_name](**params)
    return {"success": True, "result": result}

if __name__ == "__main__":
    if "--http" in sys.argv:
        # HTTP mode
        port = int(sys.argv[sys.argv.index("--http") + 1] 
                   if len(sys.argv) > sys.argv.index("--http") + 1 
                   else 3000)
        print(f"Starting HTTP mode on port {port}...")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # Stdio mode (default)
        print("Starting stdio mode...")
        mcp.run(transport="stdio")
```

**Usage:**
```bash
# Stdio mode (for Claude Desktop)
python server.py

# HTTP mode (for remote access)
python server.py --http 3000
```

### Benefits

- **Local clients** (Claude Desktop) use stdio
- **Remote clients** use HTTP
- **Testing** with curl/Postman
- **Flexibility** to choose transport

---

## Choosing the Right Transport

| Scenario | Recommended Transport |
|----------|----------------------|
| Claude Desktop integration | **Stdio** |
| MCP Studio | **Stdio** |
| Remote server access | **HTTP/HTTPS** |
| Kubernetes/Docker | **HTTP/HTTPS** |
| Testing with curl | **HTTP** |
| Cross-machine | **HTTP/HTTPS** |
| Simple local use | **Stdio** |
| Long operations | **SSE** or **WebSocket** |
| Chat interface | **WebSocket** |

---

## Transport Comparison

| Feature | Stdio | HTTP/HTTPS | SSE | WebSocket |
|---------|-------|------------|-----|-----------|
| **Complexity** | Low | Medium | Medium | High |
| **Network** | No | Yes | Yes | Yes |
| **Remote** | ❌ | ✅ | ✅ | ✅ |
| **Testable** | Hard | Easy | Medium | Medium |
| **Streaming** | ❌ | ❌ | ✅ | ✅ |
| **Bidirectional** | ✅ | ❌ | ❌ | ✅ |
| **Claude Desktop** | ✅ | ✅ | ✅ | ✅ |
| **Language Agnostic** | ❌ | ✅ | ✅ | ✅ |

---

## Official Resources

- **MCP Specification:** https://spec.modelcontextprotocol.io/
- **Transport Spec:** https://spec.modelcontextprotocol.io/specification/basic/transports/
- **FastMCP Docs:** https://github.com/jlowin/fastmcp
- **Claude Desktop Config:** `../claude-desktop/`

---

## Related Documentation

- `OVERVIEW.md` - MCP protocol basics
- `../fastmcp/` - FastMCP implementation guide
- `../claude-desktop/` - Claude Desktop configuration

---

**All transport methods are valid per Anthropic standards. Choose based on your use case!**

