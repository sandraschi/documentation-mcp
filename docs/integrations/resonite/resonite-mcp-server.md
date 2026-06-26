# Resonite MCP: The Agentic Control Layer

The Resonite MCP server enables the Antigravity agent to interact with Resonite instances and world data structures.

## 🚀 Server Registration

```json
{
  "resonite": {
    "command": "python",
    "args": ["-m", "resonite_mcp.server"],
    "cwd": "D:/Dev/repos/resonite-mcp",
    "env": {
      "RESONITE_WS_URL": "ws://localhost:10782"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `spawn_object_vrm` | Construction | Direct injection of **Avatar MCP** models into the active session. |
| `update_logix_node` | Logic | Programmatically modifies a parameter in a world-logic graph. |
| `get_world_telemetry` | Discovery | Scans the instance for active users and their positions. |
| `snapshot_world` | Backup | Triggers a save of the current world state to the fleet vault. |

## 📊 Interaction Principles

- **Object Authority**: Agents should respect world ownership flags before attempting to move GameObjects.
- **Concurrency**: Resonite is highly multithreaded; tool calls should be atomic to avoid race conditions.

---
*Last updated: 2026-02-14*
