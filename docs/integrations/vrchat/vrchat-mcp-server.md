# VRChat MCP: The Agentic Control Layer

The VRChat MCP server manages the higher-level social state and coordinate with the **OSC MCP** for parameter modulation.

## 🚀 Server Registration

```json
{
  "vrchat": {
    "command": "python",
    "args": ["-m", "vrchat_mcp.server"],
    "cwd": "D:/Dev/repos/vrchat-mcp",
    "env": {
      "VRC_OSC_IP": "127.0.0.1",
      "VRC_OSC_PORT": "9000"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `set_social_parameter` | Expression | High-level wrapper for OSC messages (e.g., "Set Smile to 1.0"). |
| `monitor_instance` | Telemetry | Tracks current world ID and player count. |
| `broadcast_chatbox` | Communication | Sends text replies directly to the VRChat chatbox. |
| `load_avatar_config` | Orchestration | Switches between pre-defined social identities in the vault. |

## 📊 Interaction Principles

- **Latency Management**: OSC messages are buffered to prevent world-state jitter.
- **Social Awareness**: Chatbox messages are throttled to ensure peer-appropriate communication speeds.

---
*Last updated: 2026-02-14*
