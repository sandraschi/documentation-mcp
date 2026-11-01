# LiveKit MCP Integration

**Last Updated:** 2026-09-06 (server v1.13.6, agents v1.8.0)
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

### Implemented (teleconference-mcp reference, Sep 2026)

| Tool | Description |
|------|-------------|
| `move_mouse` / `click_mouse` / `type_text` | System control (Remoting) |
| `generate_meeting_summary` / `extract_action_items` | Synopsis + TODOs (Conferencing) |
| `conference_schedule` / `conference_list` / `conference_get` / `conference_update` / `conference_cancel` / `conference_upcoming` | SQLite-backed scheduling (Conferencing) |
| `participant_invite` / `participant_list_invited` / `participant_remove_invited` | Invitations (Conferencing) |
| `conference_health` | Aggregate health: LiveKit TCP 15580, Ollama, system metrics |
| Web `POST /api/token` (with `roomCreate:true`) | JWT issuance + room auto-create (server v1.12+) |
| Web `POST /api/egress/start` + `/stop`, `GET ?type=recordings` | Real Egress v2 via `EgressClient` (server v1.13.2+) |

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



