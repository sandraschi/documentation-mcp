# Robotics Webapp Project Status

**Last Updated:** 2026-02-08
**Status:** Alpha - Live MCP Data Integration
**Repository:** `D:\Dev\repos\robotics-mcp\web\`

---

## Overview

Full-stack web application providing unified control interface for physical, virtual, and simulated robots. Integrated within the `robotics-mcp` repository as the `web/` directory. Connects to the MCP server on port 12230 for live robot data.

---

## Architecture

### Technology Stack

- **Frontend:** React 19 + TypeScript + Vite 7
- **Backend:** FastAPI (Python) on port 8354
- **Real-time:** WebSocket for telemetry updates
- **Styling:** Tailwind 4 + shadcn/ui components
- **Icons:** Lucide React
- **Routing:** React Router with lazy-loaded pages

### Key Components

- **MCP Client Proxy** - Backend proxy for MCP server communication (port 12230)
- **MCP Direct Client** - Frontend direct connection to MCP server (bypasses backend)
- **useRobots Hook** - React hook for live robot data and MCP server status
- **Gazebo Fuel Service** - Backend proxy for fuel.gazebosim.org REST API
- **LLM Service Layer** - AI/LLM integration
- **App Launcher Service** - Multi-desktop/multi-monitor application launching
- **WebSocket Server** - Real-time telemetry streaming

---

## Features

### Implemented (2026-02-08)

- **Dashboard with Live Data** - Real MCP server status, physical/virtual robot counts, connected robots
- **Dreame D20 Pro Controls** - Start/stop/pause/dock + LIDAR map 3D export (OBJ, PLY, Unity, Blender)
- **Gazebo Model Browser** - Search, download, spawn models from Gazebo Fuel
- **Robot Control Dashboard** - Control physical and virtual robots
- **Unity3D Page** - Launch controls, MCP connection status, desktop/monitor selection
- **VRChat Page** - Launch controls with MCP integration
- **Resonite Page** - Launch controls with MCP integration
- **Niantic Splats Page** - Gaussian splat library, capture guide, processing
- **Environments/WorldLabs Page** - World Labs Marble integration, world management
- **VRM Avatars Page** - Avatar library, upload, templates, settings
- **VRoid Page** - VRoid Studio character creator integration
- **VBot Control Page** - Real-time virtual robot control with WebSocket, WASD keyboard control
- **AI/LLM Management** - Model management, chatbot interface, personality system
- **Environment Launcher** - Launch Unity3D, Resonite, VRChat, VRoid Studio
- **Sensor Dashboard** - Real-time sensor data visualization
- **Workflow Manager** - Create, edit, execute workflows with debug mode
- **Map Visualization** - LIDAR maps and robot positions
- **Monitoring** - System performance and health
- **Settings Page** - Comprehensive configuration interface
- **MCP Server Health Monitoring** - Real-time online/offline indicators in topbar
- **IntegrationStatusBanner** - Tailwind/shadcn banner on 8 pages showing connection status for required services (Unity, Blender, VRChat, Resonite, Gazebo, OSC, Avatar MCP). Polls every 10s, one-click Start button, Setup Guide links. Compact mode for VBot Control
- **Full Sidebar Navigation** - Zero invisible pages, all routes discoverable
- **Dark Mode** - Proper theme variable support via Tailwind

### Planned

- WebSocket push for real-time robot state
- Streaming LLM responses
- Authentication
- Multi-modal support (images, audio)

---

## MCP Server Integration

### Integrated Servers

| Server | Port | Status | Purpose |
|--------|------|--------|---------|
| robotics-mcp | 12230 | Active | Core robot control (corrected from 8888) |
| local-llm-mcp | 8007 | Active | AI/LLM management |
| unity3d-mcp | 8001 | Active | Unity3D simulation |
| vrchat-mcp | 8002 | Active | Social VR |
| avatar-mcp | 8003 | Active | Avatar management |
| osc-mcp | 8004 | Active | OSC communication |
| resonite-mcp | 8006 | Active | Resonite metaverse |
| vroidstudio-mcp | 8005 | Active | Character creation |

### Integration Patterns

- **Direct Integration** - Backend directly calls MCP tools (robotics-mcp)
- **Frontend Direct** - `mcpDirect` client hits MCP server at 12230 from browser
- **Environment Integration** - Launch and control external applications
- **Gazebo Fuel Proxy** - Backend proxies fuel.gazebosim.org API calls

---

## Complete Page Map

### Dashboard
| Route | Description |
|---|---|
| `/` | Home with live MCP status, robot counts |

### Robot Control
| Route | Description |
|---|---|
| `/robot-control` | Physical robot list and control panel |
| `/robot-control/dreame` | Dreame D20 Pro vacuum + map 3D export |
| `/robot-control/gazebo` | Gazebo sim: Model Library + Robot Control + Setup |

### Map & Sensors
| Route | Description |
|---|---|
| `/map` | LIDAR map visualization and robot positions |
| `/sensors` | Real-time sensor data visualization |

### Environments
| Route | Description |
|---|---|
| `/environments` | WorldLabs Marble worlds, physics, lighting |

### Virtual Platforms
| Route | Description |
|---|---|
| `/unity3d` | Unity3D launch, connection status, desktop/monitor |
| `/vrchat` | VRChat launch controls |
| `/resonite` | Resonite launch controls |
| `/vbot-control` | VBot real-time control panel (WebSocket, WASD) |

### Avatars & VRM
| Route | Description |
|---|---|
| `/vrm-avatars` | VRM avatar library, upload, templates |
| `/vroid` | VRoid Studio character creator |

### Niantic Splats
| Route | Description |
|---|---|
| `/niantic-splats` | Gaussian splat library, capture guide, processing |

### AI & LLM
| Route | Description |
|---|---|
| `/llm-management` | Model management, chatbot, providers |

### Workflows
| Route | Description |
|---|---|
| `/workflows` | All workflows with search/filter/execute |
| `/workflows/new` | Create new workflow |
| `/workflows/execute` | Execute workflow |
| `/workflows/edit` | Edit workflow |

### Monitoring & Settings
| Route | Description |
|---|---|
| `/monitoring` | System performance and health |
| `/settings` | LLM config, MCP server management |
| `/onboarding` | Getting started guide |

### Documentation (20+ pages)
| Route | Description |
|---|---|
| `/documentation` | Documentation browser |
| `/docs/robots` | Robot fleet overview |
| `/docs/robots/dreame-d20-pro` | Dreame D20 Pro guide |
| `/docs/robots/yahboom-rosmaster` | Yahboom ROSMASTER guide |
| `/docs/robots/tdrone-mini` | Tdrone Mini guide |
| `/docs/robots/pilot-labs-scout` | Pilot Labs Scout |
| `/docs/robots/scenne-humanoid` | Scenne Humanoid |
| `/docs/robots/unitree-go2` | Unitree Go2 |
| `/docs/robots/unitree-humanoids` | Unitree Humanoids |
| `/docs/architecture` | Architecture overview |
| `/docs/world-labs` | WorldLabs Marble docs |
| `/docs/niantic-splats` | Niantic Gaussian Splats docs |
| `/docs/vr-platforms` | VR platforms integration |
| `/docs/vrm-avatars` | VRM avatar docs |
| `/docs/setup-prerequisites` | Setup guide |
| `/docs/software-installation` | Software install |
| `/docs/hardware` | Hardware guide |
| `/docs/hardware-requirements` | Hardware requirements |
| `/docs/mcp-server` | MCP server docs |
| `/docs/ros-fundamentals` | ROS basics |
| `/docs/ros-integration` | ROS integration |
| `/docs/llm-integration` | LLM integration |
| `/docs/planning-strategy` | Planning and strategy |
| `/docs/development` | Development workflow |
| `/docs/development/watchfiles` | Crash protection |
| `/docs/turbopack` | Turbopack docs |
| `/docs/vbot-scout` | VBot Scout Mini |

---

## Configuration

### Backend Environment Variables

```env
# MCP Server URL (corrected)
ROBOTICS_MCP_URL=http://localhost:12230

# Application Paths
UNITY_EDITOR_PATH=C:\Program Files\Unity\Hub\Editor\...
RESONITE_PATH=C:\Program Files\Resonite\Resonite.exe
VRCHAT_PATH=C:\Program Files (x86)\Steam\steamapps\common\VRChat\VRChat.exe
VROIDSTUDIO_PATH=C:\Program Files\VRoidStudio\VRoidStudio.exe
```

### Frontend Configuration

```env
VITE_API_URL=http://localhost:8354
```

---

## Quick Start

```powershell
cd D:\Dev\repos\robotics-mcp

# Backend
cd web\backend
pip install -r requirements.txt
python main.py

# Frontend (separate terminal)
cd web
npm install
npm run dev
```

Access at `http://localhost:4444`

---

## Data Flow

```
Browser → Frontend (React, port 4444)
  ├─ mcpDirect → MCP Server (port 12230) [direct, for status/health]
  └─ fetch → Backend API (port 8354)
       ├─ → MCP Server (port 12230) [proxied tool calls]
       ├─ → Gazebo Fuel API (fuel.gazebosim.org) [model search/download]
       └─ → WebSocket → Browser [real-time telemetry]
```

---

## Bugs Fixed (2026-02-08)

| Bug | Description |
|---|---|
| Wrong MCP port | Backend was connecting to 8888 instead of 12230 |
| startup/shutdown events | Were scoped inside route handler, never registered |
| WorkflowExecuteRequest | Missing `debug_mode` field caused AttributeError |
| Unity page crashes | Missing state variables and imports |
| VRChat page crashes | Missing useEffect, mcpService imports |
| Resonite relative imports | Fixed to @/ aliases |
| Dark mode text | Replaced hardcoded gray with theme variables |
| Invisible pages | 7+ documentation pages, Workflows, VRoid had no sidebar entries |
| BUG-OSC-001 | Backend: osc-mcp calls used `Client(self.mcp)` instead of `call_mounted_server_tool()` |
| BUG-UNITY-001 | Backend: unity3d-mcp calls used `Client(self.mcp)` instead of `call_mounted_server_tool()` |

## New Components (2026-02-08)

| Component | Location | Description |
|---|---|---|
| `IntegrationStatusBanner` | `components/IntegrationStatusBanner.tsx` | Tailwind/shadcn banner for connection status of heavy integrations. Added to 8 pages. Polls mcpService + appLauncherService every 10s |

---

## Related Projects

- **[robotics-mcp STATUS](../robotics-mcp/STATUS.md)** - Core MCP server
- **[Robotics Ecosystem](../../robotics/ROBOTICS_ECOSYSTEM.md)** - Ecosystem overview

---

**Last Updated:** 2026-02-08 (IntegrationStatusBanner, mounted server fixes, full page map)
