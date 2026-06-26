# Blender MCP: The Agentic Control Layer

The Blender MCP server provides the automation bridge between the Antigravity agent and the Blender engine. It enables programmatic geometry creation, rigging, and rendering without manual GUI interaction.

## 🚀 Server Registration

The server must be registered in the agent's MCP configuration (`mcp_config.json`):

```json
{
  "blender": {
    "command": "python",
    "args": ["-m", "blender_mcp.server"],
    "cwd": "D:/Dev/repos/blender-mcp",
    "env": {
      "BLENDER_EXECUTABLE": "C:/Program Files/Blender Foundation/Blender 4.0/blender.exe"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `generate_robot_mesh` | Mesh Creation | Spawns a parameterized chassis for new robot prototypes. |
| `apply_shader_textures` | PBR Mapping | Connects GIMP-generated textures to the Principled BSDF node. |
| `trigger_batch_render` | Rendering | Executes a headless Cycles render of the current scene. |
| `export_fbx_rigged` | Interop | Exports the model with a verified rig for Unity ingestion. |

## 📊 Interaction Principles

- **Headless First**: Agents should prioritize `--background` operations to minimize resource overhead.
- **Atomic Operations**: Each tool call should correspond to a single, verifiable change in the `.blend` data structure.

---
*Last updated: 2026-02-14*
