# Davinci Resolve MCP: The Agentic Control Layer

The Davinci Resolve MCP server provides an automation gateway to the Resolve Python API, enabling programmatic timeline assembly and rendering.

## 🚀 Server Registration

```json
{
  "davinci_resolve": {
    "command": "python",
    "args": ["-m", "davinci_mcp.server"],
    "cwd": "D:/Dev/repos/davinci-mcp",
    "env": {
      "RESOLVE_SCRIPT_API": "python3",
      "RESOLVE_DATABASE": "SandraMain"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `append_to_timeline` | Assembly | Links a new media clip into the active editing timeline. |
| `apply_color_grade` | Post-Processing | Imports a pre-defined LUT or node-tree to the clip. |
| `trigger_render_job` | Export | Starts a background render job on the Deliver page. |
| `get_project_status` | Telemetry | Monitors render progress and database health. |

## 📊 Interaction Principles

- **Scripting Security**: The server requires Davinci Resolve to be **open** for the API to be reachable.
- **Reference Logic**: All clips should be moved to the local `MediaPool` before being added to a timeline.

---
*Last updated: 2026-02-14*
