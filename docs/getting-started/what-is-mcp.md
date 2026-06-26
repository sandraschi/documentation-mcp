# What is MCP?

**Last Updated:** 2025-12-04

---

## The Problem MCP Solves

AI assistants like Claude are powerful, but they're isolated. They can't:

- Access your files
- Query your databases
- Control your applications
- Remember context between sessions
- Use your internal APIs

**Enter MCP (Model Context Protocol)**: A universal standard for connecting AI to the real world.

---

## MCP in One Sentence

**MCP is a USB port for AI** - a standard protocol that lets any AI assistant connect to any data source or tool, without custom integrations for each combination.

---

## How It Works

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Claude    │ ◄─MCP─► │  MCP Server │ ◄─────► │  Your Data   │
│  (Client)   │         │             │         │  Your Tools  │
└─────────────┘         └─────────────┘         └──────────────┘
```

### Three Components

1. **Client** (Claude Desktop, custom apps)
   - Sends requests over MCP
   - Displays results to user

2. **Server** (Your Python code)
   - Exposes tools, resources, prompts
   - Handles client requests
   - Returns structured data

3. **Transport** (Stdio, HTTP, SSE, WebSocket)
   - Carries messages between client and server
   - Handles connection management

---

## Core Concepts

### Tools

**What**: Functions the AI can call

**Example**:
```python
@mcp.tool()
def get_weather(city: str) -> dict:
    """Get current weather for a city"""
    return {"city": city, "temp": 72, "condition": "sunny"}
```

**Usage**: Claude can call this tool when you ask "What's the weather in Vienna?"

### Resources

**What**: Data the AI can read

**Example**:
```python
@mcp.resource("file://config.json")
def get_config() -> str:
    """Application configuration"""
    return json.dumps({"version": "1.0.0"})
```

**Usage**: Claude can read configuration without executing code

### Prompts

**What**: Pre-defined conversation starters

**Example**:
```python
@mcp.prompt()
def code_review_template() -> str:
    """Template for code reviews"""
    return "Review this code for: security, performance, readability"
```

**Usage**: Users can quickly start common workflows

---

## Why MCP?

### Before MCP

Each AI assistant needed custom integration with each tool:

```
Claude ──► Custom Slack Integration
       ──► Custom GitHub Integration
       ──► Custom Database Integration
       ──► Custom API Integration (×1000)

GPT-4  ──► Different Slack Integration
       ──► Different GitHub Integration
       ──► ... (Rebuild everything!)
```

**Result**: Integration explosion, no portability

### With MCP

One server, any client:

```
Claude ─┐
GPT-4  ─┼──► MCP Server ──► Your Tools
Custom ─┘
```

**Result**: Build once, use everywhere

---

## Real-World Examples

### 1. Plex Media Server

```python
@mcp.tool()
def search_library(query: str) -> list:
    """Search Plex library"""
    return plex.search(query)

@mcp.tool()
def play_movie(title: str) -> str:
    """Start playing a movie"""
    return plex.play(title)
```

**Usage**: "Play The Matrix" → Claude calls `play_movie("The Matrix")`

### 2. Vienna Transit

```python
@mcp.tool()
def next_departures(station: str) -> list:
    """Get next departures from a station"""
    return wienerlinien_api.departures(station)
```

**Usage**: "When's the next U4?" → Claude checks real-time data

### 3. Reaper DAW

```python
@mcp.tool()
def start_recording() -> str:
    """Start audio recording"""
    reaper.record()
    return "Recording started"
```

**Usage**: "Start recording" → Claude controls Reaper

---

## MCP vs Alternatives

### MCP vs Custom APIs

| Aspect | Custom API | MCP |
|--------|-----------|-----|
| **Standardization** | Each API different | Universal protocol |
| **Client support** | Custom per client | Any MCP client |
| **Discoverability** | Manual docs | Self-describing |
| **Type safety** | Varies | Built-in via JSON Schema |

### MCP vs Function Calling

| Aspect | Function Calling | MCP |
|--------|-----------------|-----|
| **Scope** | Single LLM API call | Persistent connection |
| **State** | Stateless | Can maintain state |
| **Resources** | Not supported | Yes (read-only data) |
| **Transport** | HTTP only | Multiple (stdio, HTTP, SSE, WebSocket) |

---

## Architecture

### Local (Stdio)

```
┌─────────────────────────────┐
│       Your Computer         │
│                             │
│  ┌────────┐    ┌─────────┐ │
│  │ Claude │◄──►│  Server │ │
│  │Desktop │    │(Python) │ │
│  └────────┘    └─────────┘ │
│                             │
└─────────────────────────────┘
```

**Best for**: Local development, desktop tools

### Remote (HTTP/SSE)

```
┌─────────────┐         ┌─────────────────┐
│   Claude    │         │   Your Server   │
│  (Local)    │◄─HTTP──►│   (Remote)      │
└─────────────┘         └─────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  Database    │
                        │  Files       │
                        │  APIs        │
                        └──────────────┘
```

**Best for**: Production, web apps, multiple clients

---

## Key Benefits

### 1. **Composability**

Mix and match servers:

```json
{
  "mcpServers": {
    "plex": {...},
    "database": {...},
    "transit": {...}
  }
}
```

Claude can use all three simultaneously!

### 2. **Security**

Controlled access:
- Servers run with your permissions
- No cloud data sharing required
- You control what AI can access

### 3. **Simplicity**

Build a server in 10 lines:

```python
from fastmcp import FastMCP

mcp = FastMCP("Simple")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

### 4. **Extensibility**

Add features without changing clients:
- New tools? Just add a function
- New resources? Add a resource handler
- New prompts? Add a prompt template

---

## The MCP Ecosystem

### Clients

- **Claude Desktop** - Official Anthropic client
- **Custom apps** - Build your own with MCP SDK
- **Web apps** - HTTP-based clients
- **CLI tools** - Terminal-based clients

### Servers

- **Community servers** - 100+ on Glama registry
- **Your servers** - Build custom integrations
- **Official servers** - Anthropic-maintained examples

### Tools

- **FastMCP** - Python server framework (easiest!)
- **MCP TypeScript SDK** - Node.js framework
- **Inspector** - Debug MCP connections
- **Zoo Analyzer** - Analyze server quality

---

## Next Steps

Now that you understand what MCP is:

1. **Build your first server**: [README.md](README.md#quick-start-5-minutes)
2. **Learn the protocol**: [../protocol/README.md](../protocol/README.md)
3. **Choose your transport**: [choosing-transport.md](choosing-transport.md)
4. **Master FastMCP**: [../fastmcp/README.md](../fastmcp/README.md)

---

**Questions?**

- Read the [Protocol Overview](../protocol/OVERVIEW.md)
- Check [Troubleshooting](../troubleshooting/README.md)
- Review [Examples](../../templates/scripts/)

---

**The future of AI integration is here. Start building!** 🚀

