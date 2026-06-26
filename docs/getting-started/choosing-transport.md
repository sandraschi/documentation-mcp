# Choosing Your MCP Transport

**Last Updated:** 2025-12-04

---

## Overview

MCP supports **four transports** for client-server communication:

1. **Stdio** - Standard input/output (pipes)
2. **HTTP** - REST-style HTTP requests
3. **SSE** - Server-Sent Events (HTTP streaming)
4. **WebSocket** - Full-duplex WebSocket connection

**Which should you use?** It depends on your use case!

---

## Quick Decision Matrix

| Use Case | Transport | Why |
|----------|-----------|-----|
| **Claude Desktop (local)** | Stdio | Built-in, zero config |
| **Claude Desktop (remote)** | SSE | Best streaming support |
| **Web app** | SSE or WebSocket | Real-time updates |
| **Simple API** | HTTP | REST-like, familiar |
| **Mobile app** | HTTP or WebSocket | Network-friendly |
| **Real-time collaboration** | WebSocket | Low latency, bidirectional |

---

## Stdio Transport

### What It Is

Process communication via standard input/output streams.

```
┌─────────┐ stdin  ┌─────────┐
│ Claude  │───────►│ Server  │
│ Desktop │ stdout │ Process │
│         │◄───────│         │
└─────────┘        └─────────┘
```

### When to Use

✅ **Local Claude Desktop**  
✅ **Development and testing**  
✅ **Single-user tools**  
✅ **Simple desktop integrations**

❌ Remote servers  
❌ Web applications  
❌ Multiple concurrent clients

### Setup

**Claude Desktop config** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "fastmcp", "run", "D:/path/to/server.py"]
    }
  }
}
```

**Server code**:

```python
from fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def my_tool() -> str:
    return "Hello from stdio!"

# Stdio is the default - just run it
# fastmcp dev server.py
```

### Pros & Cons

**Pros:**
- ✅ Zero network configuration
- ✅ Fast (no network overhead)
- ✅ Secure (local only)
- ✅ Simple setup

**Cons:**
- ❌ Local only
- ❌ One client at a time
- ❌ No remote access
- ❌ Process lifecycle tied to client

---

## HTTP Transport

### What It Is

Traditional REST-style HTTP requests and responses.

```
┌─────────┐  HTTP  ┌─────────┐
│ Client  │───────►│ Server  │
│         │  GET   │  :8000  │
│         │◄───────│         │
└─────────┘  JSON  └─────────┘
```

### When to Use

✅ **Simple APIs**  
✅ **Load-balanced deployments**  
✅ **Stateless operations**  
✅ **Familiar REST patterns**

❌ Streaming/real-time  
❌ Long-running operations  
❌ Bidirectional communication

### Setup

**Server code**:

```python
from fastmcp import FastMCP

mcp = FastMCP("HTTP Server")

@mcp.tool()
def my_tool() -> str:
    return "Hello from HTTP!"

# Run with HTTP transport
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

**Start server**:

```powershell
python server.py
```

**Claude Desktop config**:

```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://localhost:8000"
    }
  }
}
```

### Pros & Cons

**Pros:**
- ✅ Remote access
- ✅ Multiple clients
- ✅ Familiar HTTP/REST
- ✅ Easy to debug (curl, Postman)
- ✅ Standard load balancing

**Cons:**
- ❌ No streaming
- ❌ Request/response only
- ❌ Higher latency for many requests
- ❌ Stateless (unless you add persistence)

---

## SSE Transport (Server-Sent Events)

### What It Is

HTTP-based streaming with server-to-client events.

```
┌─────────┐  HTTP  ┌─────────┐
│ Client  │───────►│ Server  │
│         │◄═══════│  :8000  │  (streaming)
└─────────┘  SSE   └─────────┘
```

### When to Use

✅ **Remote Claude Desktop** (RECOMMENDED)  
✅ **Real-time updates**  
✅ **Progress notifications**  
✅ **Long-running operations**  
✅ **Server-to-client streaming**

❌ Client-to-server streaming  
❌ Full bidirectional communication

### Setup

**Server code**:

```python
from fastmcp import FastMCP

mcp = FastMCP("SSE Server")

@mcp.tool()
def long_operation() -> str:
    """Long-running operation with progress"""
    # FastMCP handles SSE automatically
    return "Operation complete!"

# Run with SSE transport
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

**Start server**:

```powershell
python server.py
```

**Claude Desktop config**:

```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### Pros & Cons

**Pros:**
- ✅ Real-time streaming
- ✅ Progress updates
- ✅ Remote access
- ✅ Multiple clients
- ✅ HTTP-compatible (firewalls, proxies)
- ✅ Automatic reconnection

**Cons:**
- ❌ One-way streaming (server → client)
- ❌ More complex than HTTP
- ❌ Browser limitations (EventSource)

---

## WebSocket Transport

### What It Is

Full-duplex communication over a single connection.

```
┌─────────┐   WS   ┌─────────┐
│ Client  │◄══════►│ Server  │  (bidirectional)
└─────────┘        └─────────┘
```

### When to Use

✅ **Real-time collaboration**  
✅ **Bidirectional streaming**  
✅ **Low latency required**  
✅ **Chat applications**  
✅ **Gaming/interactive tools**

❌ Simple request/response  
❌ Stateless operations

### Setup

**Server code**:

```python
from fastmcp import FastMCP

mcp = FastMCP("WebSocket Server")

@mcp.tool()
def chat(message: str) -> str:
    """Chat tool with low latency"""
    return f"Echo: {message}"

# Run with WebSocket transport
if __name__ == "__main__":
    mcp.run(transport="websocket", host="0.0.0.0", port=8000)
```

**Start server**:

```powershell
python server.py
```

**Client code** (custom client):

```python
import websockets
import json

async def connect():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            "method": "tools/call",
            "params": {"name": "chat", "arguments": {"message": "Hello"}}
        }))
        
        # Receive response
        response = await websocket.recv()
        print(response)
```

### Pros & Cons

**Pros:**
- ✅ Full bidirectional streaming
- ✅ Low latency
- ✅ Single persistent connection
- ✅ Efficient for frequent messages
- ✅ Real-time updates both ways

**Cons:**
- ❌ More complex setup
- ❌ Stateful connections
- ❌ Load balancing challenges
- ❌ Not all clients support WebSocket

---

## Comparison Table

| Feature | Stdio | HTTP | SSE | WebSocket |
|---------|-------|------|-----|-----------|
| **Remote access** | ❌ | ✅ | ✅ | ✅ |
| **Multiple clients** | ❌ | ✅ | ✅ | ✅ |
| **Streaming** | ✅ | ❌ | ✅ (one-way) | ✅ (bidirectional) |
| **Latency** | Low | Medium | Low-Medium | Low |
| **Setup complexity** | Simple | Simple | Medium | Complex |
| **Claude Desktop** | ✅ Built-in | ✅ Supported | ✅ Recommended | ⚠️ Custom |
| **Firewall-friendly** | N/A | ✅ | ✅ | ⚠️ |
| **Load balancing** | N/A | ✅ Easy | ⚠️ Medium | ❌ Hard |

---

## Recommended Patterns

### Development Workflow

1. **Start with Stdio**
   - Fast iteration
   - Zero network config
   - Test in Claude Desktop locally

2. **Switch to SSE**
   - Deploy to remote server
   - Keep Claude Desktop support
   - Add real-time features

3. **Add WebSocket** (if needed)
   - For real-time collaboration
   - For bidirectional streaming
   - For custom clients

### Production Deployment

**Single server:**
```
Stdio (Claude Desktop) ─┐
                        ├─► MCP Server
SSE (Web clients) ──────┘
```

**Load balanced:**
```
                  ┌─► Server 1
HTTP/SSE ─► LB ───┼─► Server 2
                  └─► Server 3
```

---

## Port Configuration

### Stdio
- No network port required
- Process communication only

### HTTP/SSE/WebSocket
- **Development**: `localhost:8000`
- **Production**: Standard ports (80/443 with HTTPS)
- **Custom**: Any available port

**Example Docker port mapping**:

```yaml
ports:
  - "8000:8000"  # HTTP/SSE/WebSocket
```

---

## Security Considerations

### Stdio
- ✅ Local only - inherently secure
- ✅ No network exposure
- ⚠️ Process permissions matter

### HTTP/SSE/WebSocket
- ⚠️ **Use HTTPS in production**
- ⚠️ **Add authentication**
- ⚠️ **Validate all inputs**
- ⚠️ **Rate limiting**
- ⚠️ **CORS configuration**

**Production example**:

```python
# Add authentication
from fastmcp import FastMCP
from fastapi import Header, HTTPException

mcp = FastMCP("Secure Server")

async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    # Verify token...

# Run with HTTPS
mcp.run(
    transport="sse",
    host="0.0.0.0",
    port=443,
    ssl_certfile="/path/to/cert.pem",
    ssl_keyfile="/path/to/key.pem"
)
```

---

## Migration Path

### From Stdio to SSE

**Before** (stdio):
```json
{
  "command": "python",
  "args": ["-m", "fastmcp", "run", "server.py"]
}
```

**After** (SSE):
```python
# Add to server.py:
if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

```json
{
  "url": "http://your-server.com:8000/sse"
}
```

**No code changes required!** FastMCP handles transport transparently.

---

## Next Steps

1. **Test locally**: Start with Stdio ([README.md](README.md))
2. **Learn protocol**: Read [../protocol/TRANSPORTS.md](../protocol/TRANSPORTS.md)
3. **Deploy remotely**: Follow [../deployment/README.md](../deployment/README.md)
4. **Add Docker**: See [../docker/README.md](../docker/README.md)

---

**Need help deciding?**

- **Local development** → **Stdio**
- **Remote server** → **SSE**
- **Simple API** → **HTTP**
- **Real-time collaboration** → **WebSocket**

**Still unsure?** Start with **Stdio** for development, switch to **SSE** for production!

