# LiveKit MCP Integration

**Last Updated:** 2026-04-06 (v2.0.0 Teams++)
**Purpose:** SOTA MCP server patterns for LiveKit-based video conferencing and AI agent projects (FastMCP 3.2+ compliance)

---

## Overview

LiveKit projects (e.g. AG-Visio/teleconference-mcp) often combine:

- **Web app** - Next.js + LiveKit React components
- **Voice agent** - Python livekit-agents worker
- **MCP server** - Dev tooling for Claude/Cursor

The MCP server provides tools that help AI assistants understand and operate the LiveKit stack during development and debugging.

---

## Recommended Tools

### Implemented (teleconference-mcp reference)

| Tool | Description |
|------|-------------|
| `move_mouse` | Moves the system cursor (Remoting) |
| `click_mouse` | Performs a mouse click (Remoting) |
| `type_text` | Types text into active window (Remoting) |
| `generate_meeting_summary` | Generates a styled synopsis (Conferencing) |
| `extract_action_items` | Extracts TODOs from transcript (Conferencing) |

### Proposed (LiveKit-aware)

| Tool | Description |
|------|-------------|
| `livekit_room_list` | List active rooms and participant counts (via LiveKit HTTP API) |
| `livekit_agent_status` | Check if agent worker is running, last heartbeat |
| `livekit_token_generate` | Generate a test token for a room (dev only) |
| `conference_health` | Aggregate health: LiveKit server, Redis, web app, agent |

---

## LiveKit HTTP API

For room listing and management, use the LiveKit server's HTTP API (when enabled) or the official `livekit-server-sdk`:

```typescript
import { RoomServiceClient } from "livekit-server-sdk";

const roomService = new RoomServiceClient(livekitUrl, apiKey, apiSecret);
const rooms = await roomService.listRooms();
```

Requires `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`.

---

## FastMCP Python Alternative

For Python-heavy stacks, use FastMCP:

```python
from fastmcp import FastMCP
from livekit import api

mcp = FastMCP("livekit-mcp")

@mcp.tool()
async def livekit_room_list() -> dict:
    """SOTA 2026: Async room discovery (FastMCP 3.2+)."""
    room_service = api.RoomServiceClient()
    rooms = await room_service.list_rooms()
    return {
        "success": True,
        "rooms": [{"name": r.name, "num_participants": r.num_participants} for r in rooms],
    }

# Tool Discovery (FastMCP 3.2+)
# tools = await mcp.list_tools()
```

---

## Configuration

### Cursor

```json
{
  "mcpServers": {
    "ag-visio-mcp": {
      "command": "node",
      "args": ["packages/mcp-server/dist/index.js"],
      "cwd": "D:\Dev\repos\teleconference-mcp"
    }
  }
}
```

### Claude Desktop

```json
{
  "mcpServers": {
    "ag-visio-mcp": {
      "command": "node",
      "args": ["packages/mcp-server/dist/index.js"],
      "cwd": "D:\Dev\repos\teleconference-mcp"
    }
  }
}
```

---

## uv Monorepo Integration

The MCP servers live in `packages/remoting_mcp/` and `packages/conferencing_mcp/`. They are managed via `uv` and orchestrated by `just`.

```
teleconference-mcp/
├── packages/
│   ├── remoting_mcp/      # Python FastMCP (Input Injection)
│   └── conferencing_mcp/  # Python FastMCP (Meeting Intelligence)
├── apps/
│   ├── web/               # Next.js + LiveKit UI
│   └── agent/             # Python livekit-agents worker
├── pyproject.toml          # Monorepo uv config
└── justfile                # Operational Dashboard
```

---

## Related

- [LIVEKIT_INTEGRATION_GUIDE.md](LIVEKIT_INTEGRATION_GUIDE.md) - Full LiveKit integration
- [TURBOREPO_MCP_MONOREPO_PATTERN.md](../../docs/patterns/TURBOREPO_MCP_MONOREPO_PATTERN.md) - Monorepo structure



