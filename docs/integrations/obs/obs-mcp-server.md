# OBS MCP Server: The Agentic Control Layer

The OBS MCP server enables the Antigravity agent to control the OBS engine via the WebSocket 5.0 protocol.

Target: OBS Studio v33.0.0. Safe Mode does NOT start WebSocket Server in 33.0+ - expect connection-refused in Safe Mode.

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
- **Safe-Mode guard (33.0+)**: If WebSocket connect fails, check `obs_frontend_is_safe_mode` / tell user to restart OBS normally. Do not retry-loop in Safe Mode.
- **Audio monitoring (33.0+)**: `monitoring_type` is deprecated, use `monitoring_enabled` boolean.
- **Replay buffer**: Use new saved-event/output signal to confirm `save_replay_buffer` file path instead of guessing `REPLAY_BUFFER_PATH`.

---
*Last updated: 2026-10-24 - OBS 33.0.0*
