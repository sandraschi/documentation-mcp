# Gazebo MCP Server: The Agentic Control Layer

The Gazebo MCP server enables the Antigravity agent to programmatically control the simulation world and its entities.

## 🚀 Server Registration

```json
{
  "gazebo": {
    "command": "python",
    "args": ["-m", "gazebo_mcp.server"],
    "cwd": "D:/Dev/repos/gazebo-mcp",
    "env": {
      "GZ_RELAY_PORT": "11345",
      "GAZEBO_MODEL_PATH": "D:/Dev/repos/gazebo-models"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `spawn_entity` | Actuation | Injects a robot or object (from Fuel or local disk) into the world. |
| `get_simulation_status` | Monitoring | Retrieves simulation time, RTF (Real Time Factor), and physics load. |
| `control_sim_state` | Lifecycle | Pauses, unpauses, or resets the simulation for test iterations. |
| `apply_external_force` | Testing | Injects disturbance forces into a robot joint to test controller stability. |

## 📊 Interaction Principles

- **RTF Awareness**: Agents must monitor the Real Time Factor. If RTF < 1.0, the workstation is overloaded, and simulation results may be unreliable.
- **Entity Identification**: Always use the `entity_name` to target specific robots in a multi-bot environment.

---
*Last updated: 2026-02-14*
