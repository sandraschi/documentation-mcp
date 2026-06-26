# Reaper MCP Server: The Agentic Control Layer

The Reaper MCP server provides an automation gateway to the ReaScript API, enabling programmatic project assembly, track management, and rendering.

## 🚀 Server Registration

```json
{
  "reaper": {
    "command": "python",
    "args": ["-m", "reaper_mcp.server"],
    "cwd": "D:/Dev/repos/reaper-mcp",
    "env": {
      "REAPER_PATH": "C:/Program Files/REAPER (x64)/reaper.exe"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `add_media_to_track` | Assembly | Spawns a new file into a specific track in the active project. |
| `set_track_fx_param` | Processing | Modifies an EQ or Compressor setting via agentic logic. |
| `trigger_render` | Export | Renders the project region to a specified audit file. |
| `sync_timeline_to_obs` | Interop | Coordinates Reaper playback position with **OBS** recording. |

## 📊 Interaction Principles

- **ReaScript Execution**: The server pushes Python scripts directly to Reaper's main thread.
- **Atomic Operations**: Avoid large script blocks; use tools to build the project incrementally.

---
*Last updated: 2026-02-14*
