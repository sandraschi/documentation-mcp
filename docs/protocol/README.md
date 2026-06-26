# MCP Protocol Documentation

**Last Updated:** 2025-12-04

Complete guide to the Model Context Protocol (MCP) - the universal standard for AI-to-tool communication.

---

## 📚 In This Section

| Document | What You'll Learn |
|----------|------------------|
| **[OVERVIEW.md](OVERVIEW.md)** | Protocol fundamentals, key concepts, how MCP works |
| **[TRANSPORTS.md](TRANSPORTS.md)** | ⭐ Stdio, HTTP, SSE, WebSocket - complete guide |

---

## 🚀 Quick Start

New to MCP? Start here:

1. **Read** [OVERVIEW.md](OVERVIEW.md) - Understand what MCP is and why it matters
2. **Choose** [TRANSPORTS.md](TRANSPORTS.md) - Pick the right transport for your use case
3. **Build** [../getting-started/README.md](../getting-started/README.md) - Create your first server in 5 minutes
4. **Deploy** [../deployment/README.md](../deployment/README.md) - Take it to production

---

## 🎯 What is MCP?

**Model Context Protocol** is an open standard that lets AI assistants connect to external tools, data sources, and services.

Think of it as **USB for AI** - a universal connection standard.

### Three Core Primitives

1. **Tools** - Actions the AI can perform (functions)
2. **Resources** - Data the AI can read (files, APIs)
3. **Prompts** - Templates for common workflows

### Four Transport Options

1. **Stdio** - Local process communication (Claude Desktop)
2. **HTTP** - REST-style API (testing, simple deployments)
3. **SSE** - Server-Sent Events (streaming, long operations)
4. **WebSocket** - Bidirectional streaming (chat, real-time)

→ See [TRANSPORTS.md](TRANSPORTS.md) for complete comparison

---

## 📖 Protocol Fundamentals

### JSON-RPC 2.0

MCP uses JSON-RPC 2.0 for all messages:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "example_tool",
    "arguments": {"param": "value"}
  },
  "id": 1
}
```

### Message Flow

```
Client                                Server
  │                                     │
  ├──────── initialize ─────────────────►│
  │◄──────── initialize result ──────────┤
  │                                     │
  ├──────── tools/list ─────────────────►│
  │◄──────── tools (array) ─────────────┤
  │                                     │
  ├──────── tools/call ─────────────────►│
  │◄──────── result ────────────────────┤
```

### Tool Schema

```python
{
  "name": "send_email",
  "description": "Send an email to a recipient",
  "inputSchema": {
    "type": "object",
    "properties": {
      "to": {"type": "string", "description": "Recipient email"},
      "subject": {"type": "string"},
      "body": {"type": "string"}
    },
    "required": ["to", "subject", "body"]
  }
}
```

---

## 🔧 Implementation Paths

### Option 1: FastMCP (Python) - Recommended

**Easiest and most popular**

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"
```

→ Complete guide: [../fastmcp/README.md](../fastmcp/README.md)

### Option 2: MCP SDK (TypeScript)

**Official Node.js implementation**

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});
```

→ See: https://github.com/modelcontextprotocol/typescript-sdk

### Option 3: Custom Implementation

**Any language with JSON-RPC support**

Requirements:
- JSON-RPC 2.0 message handling
- Transport implementation (stdio/HTTP/SSE/WebSocket)
- Tool/resource/prompt registration
- Schema validation

→ Spec: https://spec.modelcontextprotocol.io/

---

## 🎨 Architecture Patterns

### Local Development

```
┌──────────────────────────────────┐
│      Developer Machine           │
│                                  │
│  ┌─────────┐      ┌───────────┐ │
│  │ Claude  │◄────►│ MCP Server│ │
│  │ Desktop │stdio │  (Python) │ │
│  └─────────┘      └───────────┘ │
│                        │         │
│                        ▼         │
│                   Local Files    │
└──────────────────────────────────┘
```

### Remote Deployment

```
┌──────────────┐         ┌───────────────────┐
│   Claude     │         │   Cloud Server    │
│   Desktop    │◄──SSE──►│   MCP Server      │
│   (Local)    │         │                   │
└──────────────┘         │   ┌──────────┐    │
                         │   │ Database │    │
                         │   └──────────┘    │
                         │   ┌──────────┐    │
                         │   │  APIs    │    │
                         │   └──────────┘    │
                         └───────────────────┘
```

### Microservices

```
┌──────────────┐         ┌─────────────────────┐
│   Client     │         │   Load Balancer     │
│              │◄──HTTP─►│                     │
└──────────────┘         └──────┬──────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌─────────┐ ┌─────────┐ ┌─────────┐
              │ MCP     │ │ MCP     │ │ MCP     │
              │ Server 1│ │ Server 2│ │ Server 3│
              └─────────┘ └─────────┘ └─────────┘
```

---

## 🔒 Security Considerations

### Local (Stdio)
- ✅ No network exposure
- ✅ OS-level process isolation
- ⚠️ Server runs with user permissions
- ⚠️ Be careful with sensitive operations

### Remote (HTTP/SSE/WebSocket)
- ⚠️ **Use HTTPS in production**
- ⚠️ **Add authentication (API keys, OAuth)**
- ⚠️ **Rate limiting**
- ⚠️ **Input validation**
- ⚠️ **CORS configuration**
- ⚠️ **Firewall rules**

→ Complete security guide: [../deployment/security.md](../deployment/security.md)

---

## 📊 Performance Considerations

| Transport | Latency | Throughput | Overhead |
|-----------|---------|------------|----------|
| **Stdio** | ~1-5ms | High | Minimal |
| **HTTP** | ~10-50ms | Medium | Moderate |
| **SSE** | ~10-50ms | High (streaming) | Low |
| **WebSocket** | ~5-20ms | Very High | Low |

**Recommendations:**
- **Stdio**: Best for local, low-latency operations
- **SSE**: Best for remote with streaming needs
- **WebSocket**: Best for real-time bidirectional communication
- **HTTP**: Best for simple, stateless operations

---

## 🆘 Troubleshooting

### Common Issues

**Server not appearing in Claude Desktop**
→ Check `claude_desktop_config.json` syntax  
→ Verify Python path  
→ Restart Claude Desktop  
→ Check logs: `%APPDATA%\Claude\logs\`

**Transport connection failed**
→ Verify server is running  
→ Check firewall rules  
→ Test with curl (HTTP)  
→ Enable debug logging

**Tool not working**
→ Check tool schema  
→ Verify parameter types  
→ Add logging  
→ Test in isolation

→ Complete guide: [../troubleshooting/README.md](../troubleshooting/README.md)

---

## 📚 Learning Path

### Beginner
1. Read [OVERVIEW.md](OVERVIEW.md) - Protocol basics
2. Read [TRANSPORTS.md](TRANSPORTS.md) - Choose transport
3. Try [../getting-started/README.md](../getting-started/README.md) - First server

### Intermediate
1. Study [../fastmcp/3.1-features.md](../fastmcp/3.1-features.md) - Current features
2. Learn [../patterns/README.md](../patterns/README.md) - Design patterns
3. Implement state management

### Advanced
1. Build dual-interface servers (stdio + HTTP)
2. Add monitoring [../../monitoring/README.md](../../monitoring/README.md)
3. Containerize [../docker/README.md](../docker/README.md)

### Expert
1. Implement custom transport
2. Build MCP client
3. Contribute to specification

---

## Agent2Agent (A2A) — related open standard

A2A is **not** MCP; it standardizes **agent-to-agent** discovery and tasks (often JSON-RPC over HTTP), and complements MCP. Fleet rollout order and port reminders live centrally here:

- **[A2A fleet rollout (mcp-central-docs)](../operations/A2A_FLEET_ROLLOUT.md)** — pointer + phase summary  
- **Canonical plan:** [plex-mcp `A2A_FLEET_ROLLOUT_PLAN.md`](https://github.com/sandraschi/plex-mcp/blob/main/docs/mcp-technical/A2A_FLEET_ROLLOUT_PLAN.md)

Official A2A project: https://a2a-protocol.org/ · https://github.com/a2aproject/A2A

---

## 🔗 Official Resources

- **Specification**: https://spec.modelcontextprotocol.io/
- **Website**: https://modelcontextprotocol.io/
- **GitHub**: https://github.com/modelcontextprotocol
- **FastMCP**: https://github.com/jlowin/fastmcp
- **Glama Registry**: https://glama.ai/mcp/servers

---

## 🗺️ Related Documentation

| Section | Purpose |
|---------|---------|
| [getting-started/](../getting-started/) | Quick start guide |
| [fastmcp/](../fastmcp/) | FastMCP implementation guide |
| [deployment/](../deployment/) | Production deployment |
| [docker/](../docker/) | Containerization |
| [patterns/](../patterns/) | Design patterns |
| [troubleshooting/](../troubleshooting/) | Common issues |

---

## 📝 Contributing

Found an issue? Have a suggestion?

1. Check existing documentation
2. Review [../../CONTRIBUTING.md](../../CONTRIBUTING.md)
3. Follow [../../STANDARDS.md](../../STANDARDS.md)
4. Submit improvements

---

**Ready to dive deeper?**

→ Start with [OVERVIEW.md](OVERVIEW.md) for protocol fundamentals  
→ Then [TRANSPORTS.md](TRANSPORTS.md) to choose your transport  
→ Finally [../getting-started/README.md](../getting-started/README.md) to build your first server!

