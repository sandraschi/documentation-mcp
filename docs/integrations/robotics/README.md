# Robotics MCP: Unified Physical & Virtual Orchestration

The Robotics MCP is the central nervous system for the fleet's robotic assets. It provides a unified abstraction layer for controlling physical hardware (**Unitree Go2/R1**, **Moorebot Scout**) and virtual agents (**Unity3D**, **VRChat**) through a standardized command-and-control interface.

## ðŸš€ Deployment & Multi-Platform Strategy

### Core Architecture
- **Framework**: FastMCP 3.1.1+.4+ (SOTA).
- **Physical Integration**: ROS 1.4 Bridge, Unitree SDK.
- **Virtual Integration**: OSC (Port `9000`), Unity Event System.
- **Strategy**: Dual-mode execution allowing identical logic to run on physical hardware and virtual twins.

### MCP Registration
```json
{
  "robotics": {
    "command": "python",
    "args": ["-m", "robotics_mcp.server"],
    "cwd": "D:/Dev/repos/robotics-mcp",
    "env": {
      "ROBOT_MODE": "hybrid",
      "UNITY_WS_URL": "ws://localhost:10780/robotics",
      "PHYSICAL_BRIDGE_IP": "192.168.12.1"
    }
  }
}
```

## ðŸ¤– Robot Control & Perception

### Unified Actuation Tools
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `execute_motion` | Execution | Standardized movement commands (linear/angular) translated to ROS or Unity. |
| `get_robot_status` | Telemetry | Unified state view (Battery, Joint Angles, LiDAR health). |
| `deploy_robot` | Orchestration | Power-on sequence and sensor initialization for a specific robot ID. |

### Perception & Vision
- **`process_lidar_stream`**: Real-time analysis of the **Livox Mid-360** or virtual LiDAR data for obstacle avoidance.
- **`object_recognition`**: Leveraging the **RTX 4090** to categorize objects in the robot's binocular view.

## ðŸ› ï¸ Advanced SOTA Workflows

### The "Twin-Sync" Pattern
Agents use the Robotics MCP to validate behaviors in simulation before physical deployment:
1. **Simulation**: Agent deploys the **Scout** in **Unity3D** to test a navigation script.
2. **Analysis**: Agent monitors collisions and CPU load in the virtual environment.
3. **Deployment**: Upon virtual success, the agent triggers `deploy_robot` on the physical Scout.

### VRChat Social Robotics
Integration with **vrchat-mcp** allows robots to act as social avatars, bridging physical Vienna with the virtual VRChat events:
- **Operation**: Agent maps Unitree Go2 joint data to an OSC-compatible avatar in VRChat.

## ðŸ“Š Performance & Integrity
- **Real-time Loop**: Actuator loop maintained at 50Hz for smooth motion.
- **Safety Protocol**: Mandatory "E-Stop" command availability in all robot-control tools.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*

