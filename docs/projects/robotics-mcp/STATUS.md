# Robotics MCP - Project Status

**Last Updated:** 2026-03-03
**Status:** Federated Robotics Fleet Hub
**Version:** 0.3.0
**Source Repo:** `D:\Dev\repos\robotics-mcp` (Fleet Hub)

**ADN Status Note:** Advanced Memory `adn_content` - `adn-notes/robotics-mcp-adn-status-2026-02-08` (Mounted server fixes + IntegrationStatusBanner)

---

## Overview

**Unified robotics coordination via Federated MCP** - The `robotics-mcp` project has evolved into a central hub for coordinating specialized robot servers. The robot-specific logic (sensors, low-level control) has been migrated to dedicated MCPs for better scalability and modularity.

**Fleet Hub Stats**: ~1,500+ lines Orchestration logic, ~5,000+ lines Fleet Dashboard.

**Core Fleet Members**:
- **Yahboom ROSMASTER**: [yahboom-mcp](file:///d:/Dev/repos/yahboom-mcp) - ROS 2 manipulation and navigation.
- **Dreame D20 Pro**: [dreame-mcp](file:///d:/Dev/repos/dreame-mcp) (Planned Extract) - LIDAR mapping and vacuuming.
- **Virtual Robotics**: [virtual-robotics-mcp] - Unity/VRChat simulation.

---

## Current Status (2026-02-08)

### What Works (Real, Not Mock)

| Feature | Status | Details |
|---|---|---|
| FastMCP 3.1.1++ compliance | DONE | All tools have `ctx: Context`, server lifespan enabled |
| Dreame D20 Pro control | DONE | python-miio: start/stop/pause/dock/zone cleaning |
| Dreame LIDAR map retrieval | DONE | Raw MiIO siid=23/piid=1 + vacuum-map-parser-dreame |
| Dreame map 3D export | DONE | OBJ mesh, PLY point cloud, Unity NavMesh JSON, Blender script |
| Gazebo Fuel model browser | DONE | Search, download, local management via fuel.gazebosim.org API |
| Gazebo model spawn | DONE | ROS service calls (Classic + Gz Sim) |
| Yahboom roslibpy client | DONE | Real rosbridge WebSocket integration (connect, move, arm, gripper) |
| Elegoo serial protocol | DONE | Actual serial communication, sensor parsing |
| MCP stdio + HTTP transport | DONE | Binary mode, DevNullStdout, FastAPI router |
| MCP server composition | DONE | Mount external MCP servers with graceful fallback |
| Webapp live data | DONE | useRobots hook, direct MCP client, dark mode fix |
| Webapp full sidebar nav | DONE | Zero invisible pages - all routes discoverable |
| Webapp Gazebo model browser | DONE | Search, thumbnails, download, spawn controls |
| Webapp Dreame 3D export | DONE | UI for exporting maps to OBJ/PLY/Unity/Blender |
| Workflow storage (SQLite) | DONE | CRUD for workflow definitions |

### Mock/Stub (Labeled Honestly)

| Feature | Status | Notes |
|---|---|---|
| Unitree Go2/G1 control | STUB | Returns `not_implemented` - no SDK integrated |
| Drone flight control | MOCK | Tool exists, handler returns `simulated: True` |
| LLM provider connection | MOCK | sleep(1.0) + "connected" |
| Webapp physics sim | MOCK | Fake IMU/odometry, labeled as demo |
| Physical-virtual sync | STUB | Returns `simulated: True` |

### Known Limitations

- Yahboom not tested on real hardware yet (needs Raspberry Pi + rosbridge)
- Dreame requires cloud token extraction (scripts provided)
- Gazebo model spawn needs active rosbridge connection
- No authentication on HTTP API
- `robot_control.py` is a 1374-line god-object (refactor planned)

---

## 13 Portmanteau Tools

1. **robotics_system** - System management (help, status, list_robots)
2. **robot_control** - Unified physical/virtual robot control (Dreame, Yahboom, Elegoo, Hue, virtual)
3. **robot_behavior** - Animation, camera, navigation, manipulation
4. **robot_manufacturing** - 3D printing, CNC, laser cutting
5. **robot_virtual** - Virtual robot CRUD + platform operations
6. **robot_model_tools** - 3D model creation, import, export, conversion
7. **vbot_crud** - Virtual robot lifecycle management
8. **drone_control** - Core drone flight operations
9. **dreame_control** - Dreame D20 Pro: vacuum ops + LIDAR map export
10. **gazebo_models** - Gazebo Fuel: search, download, spawn, local management
11. **workflow_management** - Robotics workflow orchestration
12. **virtual_robotics** - Legacy virtual robotics operations
13. **robot_navigation** - Path planning and obstacle avoidance

---

## MCP Server Composition

Integrates 6 external MCP servers with graceful fallback. All tool calls to mounted servers use `call_mounted_server_tool()` from `utils/mcp_client_helper.py` (BUG-OSC-001 and BUG-UNITY-001 fixed 2026-02-08):

- **osc-mcp** - OSC communication (prefix: `osc`) - ENABLED, calls via `call_mounted_server_tool()`
- **unity3d-mcp** - Unity3D integration (prefix: `unity`) - ENABLED with safety (30s timeout, 3 retries), calls via `call_mounted_server_tool()`
- **vrchat-mcp** - VRChat integration (prefix: `vrchat`) - DISABLED (protocol conflicts)
- **avatar-mcp** - Avatar/VRM control (prefix: `avatar`) - DISABLED (timeseries conflicts)
- **blender-mcp** - 3D model creation (prefix: `blender`) - DISABLED (protocol hangs)
- **gimp-mcp** - Texture editing (prefix: `gimp`) - DISABLED (protocol hangs)

---

## HTTP API

### Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/health` | GET | Health check |
| `/api/v1/robots` | GET | List all robots |
| `/api/v1/robots/{id}` | GET | Get robot info |
| `/api/v1/robots` | POST | Register robot |
| `/api/v1/robots/{id}/control` | POST | Control robot |
| `/api/v1/robots/{id}` | DELETE | Unregister robot |
| `/api/v1/tools` | GET | List all MCP tools |
| `/api/v1/tools/{name}` | POST | Call MCP tool |
| `/api/v1/status` | GET | Server status |

---

## Webapp Pages (Full Sidebar Coverage)

| Section | Pages |
|---|---|
| Dashboard | Home (`/dashboard`), Live Status (`/status`) |
| Robot Control | Control Sandbox (`/control`), Dreame D20 Pro (`/dreame`), Yahboom ROS2 Car (`/yahboom`) |
| Telemetry | Map / LiDAR (`/map`), ROS 2 Ecosystem (`/ros2`) |
| Sensors | Sensor Dashboard (`/sensors`) |
| Environments | Environments / WorldLabs Marble (`/environments`) |
| Virtual Platforms | VBot Chain (`/vbot-ecosystem`), Unity3D (`/unity3d`), VRChat (`/vrchat`), Resonite (`/resonite`) |
| Avatars & VRM | VRM Avatars (`/vrm-avatars`), VRoid Studio (`/vroid`) |
| Niantic Splats | Gaussian Splat manager (`/niantic-splats`) |
| Ecosystem | Apps Hub (`/apps`), Tools Explorer (`/tools`) |
| AI & LLM | LLM Management (`/llm-management`) |
| Workflows | All Workflows (`/workflows`), Create New (`/workflows/new`) |
| Monitoring | System Monitoring (`/monitoring`) |
| Settings | Settings (`/settings`) |
| Onboarding | Getting Started (`/onboarding`) |
| Documentation | Doc Browser (`/documentation`), Robot Fleet, Dreame D20 Pro, Architecture, WorldLabs Marble, Niantic Splats, VR Platforms, VRM Avatars, ROS Fundamentals, ROS Integration, MCP Server, Setup Prerequisites, Software Installation, Hardware Requirements, Development Workflow, Watchfiles |

### IntegrationStatusBanner (2026-02-08)

New Tailwind/shadcn component added to 8 heavy integration pages. Shows per-service connection status with Start button and Setup Guide link:

| Page | Required Services |
|---|---|
| Unity3D | Unity3D, Blender |
| VRChat | VRChat, OSC Bridge |
| Resonite | Resonite, OSC Bridge |
| Gazebo | Gazebo Sim, ROS 2 Bridge |
| Niantic Splats | Unity3D, Blender |
| Environments/WorldLabs | Unity3D, Blender |
| VRM Avatars | Blender, Avatar MCP |
| VRoid | Blender, Avatar MCP |
| VBot Control | Unity3D, VRChat, Resonite (compact) |

---

## Key Features (2026-02-08)

### Why Dreame D20 Pro as Starter Robot

Most robotics projects start with expensive, fragile hardware that gathers dust. The Dreame D20 Pro is a real household appliance that doubles as a sophisticated robotics platform:

- **Cheap**: ~$200-300 on Amazon (vs $300-600 for Yahboom, $1,600+ for Unitree Go2)
- **Available**: Ships from Amazon in 1-2 days, no niche suppliers
- **Actually useful**: Vacuums and mops daily. Your partner will not complain about "that robot thing"
- **Advanced LIDAR**: Full room-mapping LDS laser scanner with exportable floor plans
- **Open software stack**: `python-miio` + raw MiIO protocol + `vacuum-map-parser-dreame`. No vendor lock-in
- **Autonomous**: Auto-charges, auto-empties, runs on schedule for weeks unattended
- **Cute**: Watching it navigate chair legs is endearing. Make it do a little dance (rapid zone changes) and it gets cuter still
- **One gap**: No camera. Supplement with a Tapo C200 (~$25) for visual coverage

### Dreame D20 Pro LIDAR to 3D Pipeline

1. Retrieve raw LIDAR map via MiIO protocol (siid 23, piid 1)
2. Parse with `vacuum-map-parser-dreame` - walls, rooms, obstacles, robot position
3. Export to: **OBJ** (3D mesh), **PLY** (point cloud), **Unity NavMesh JSON**, **Blender Python script**
4. Import into Blender via `blender-mcp` or Unity via drag-and-drop

### Gazebo Fuel Model Browser

1. Search models from `fuel.gazebosim.org` by keyword/category
2. Download models to local `~/.gz/fuel/` directory
3. Spawn models in running Gazebo simulation via ROS services
4. Manage local model cache

### Yahboom roslibpy Integration

Real `roslibpy.Ros` WebSocket client replacing 100% mock code:
- Connect/disconnect to rosbridge
- Subscribe to `/odom`, `/scan`, `/battery`
- Publish to `/cmd_vel`
- Arm control and gripper operations
- All simulated responses explicitly labeled `simulated: True`

---

## Technology Stack

- **FastMCP 3.1.1++** - MCP server framework with `ctx: Context` compliance
- **FastAPI** - HTTP endpoints (port 12230)
- **React 19 + Vite 7** - Webapp frontend
- **Tailwind 4 + shadcn/ui** - Webapp styling
- **roslibpy** - ROS bridge WebSocket client
- **python-miio** - Dreame vacuum control
- **vacuum-map-parser-dreame** - LIDAR map parsing
- **aiohttp** - Async HTTP for Gazebo Fuel API
- **structlog** - JSON structured logging (stderr only)

---

## Roadmap

### Completed (Phase 1+2)
- ✅ Virtual robot spawning in Unity
- ✅ World Labs Marble/Chisel environment loading
- ✅ FastMCP 3.1.1++ compliance (all tools)
- ✅ Dreame D20 Pro full integration + LIDAR 3D export
- ✅ Yahboom roslibpy real implementation
- ✅ Gazebo Fuel model browser + spawner
- ✅ Webapp live data + complete sidebar navigation

### Phase 3: Production Hardening (Next)
- Connect Yahboom to real Raspberry Pi hardware
- Mount ros-mcp-server as composed server
- Add WebSocket push for real-time robot state
- Add authentication to HTTP API
- Refactor robot_control.py god-object

### Phase 4: Differentiation
- Multi-robot coordination (unique differentiator)
- Physical-virtual sync (Dreame position to Unity twin)
- Safety layer (velocity clamping, emergency stop)
- ROS2 auto-discovery

---

## Bugs Fixed (2026-02-08)

| ID | Severity | Description |
|---|---|---|
| BUG-001 | CRITICAL | `WorkflowExecuteRequest.debug_mode` AttributeError |
| BUG-002 | CRITICAL | startup/shutdown events scoped inside route handler |
| BUG-003 | MEDIUM | Duplicate Hue docstring line |
| BUG-004 | HIGH | `ai_query` missing from action Literal type |
| BUG-005 | HIGH | Private `_tools` dict access |
| BUG-006 | HIGH | Deprecated `asyncio.get_event_loop()` |
| BUG-008 | MEDIUM | Linux-default serial port on Windows |
| BUG-009 | MEDIUM | Webapp connecting to wrong MCP port |
| MOCK-* | HIGH | All gaslighting mocks replaced with honest `simulated: True` |
| BUG-OSC-001 | HIGH | All osc-mcp calls used `Client(self.mcp).call_tool()` targeting main server instead of mounted OSC server. Fixed to `call_mounted_server_tool()` in virtual_robotics.py, vbot_crud.py, robot_animation.py |
| BUG-UNITY-001 | HIGH | Same pattern for all unity3d-mcp calls in virtual_robotics.py (4 blocks) and robot_animation.py (6 actions). Fixed to `call_mounted_server_tool()` |

---

## License

MIT License

