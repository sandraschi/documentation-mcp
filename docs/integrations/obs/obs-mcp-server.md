# OBS MCP Server: The Agentic Control Layer

The OBS MCP server enables the Antigravity agent to control the OBS engine via the WebSocket 5.0 protocol.

## 🚀 Server Registration

```json
{
  "obs": {
    "command": "python",
    "args": ["-m", "obs_mcp.server"],
    "cwd": "D:/Dev/repos/obs-mcp",
    "env": {
      "OBS_WS_HOST": "localhost",
      "OBS_WS_PORT": "4455",
      "OBS_WS_PASSWORD": "${ENV:OBS_PASSWORD}"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `switch_scene` | Orchestration | Switches the active visual layout (e.g., from "Desktop" to "Robot Cam"). |
| `start_stop_recording` | Production | Manages the file capture lifecycle for project documentation. |
| `adjust_audio_source` | Mixing | Mutes or modifies volume for specific fleet audio channels. |
| `toggle_virtual_cam` | Routing | Activates the virtual camera for injection into Resonite or Zoom. |

## 📊 Interaction Principles

- **Confirmation Loop**: Agents MUST verify the `is_recording` status after sending a start command.
- **Scene Verification**: Before switching, the agent should list available scenes to prevent errors.

---
*Last updated: 2026-02-14*
