# Robotics Fleet — Architecture & Tool Reference

**Last Updated**: 2026-06-11  
**Status**: Active  

## Fleet Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                     robotics-mcp (coordinator + marketplace)                      │
│        sim_fleet_status · sim_fleet_route · sim_fleet_backends                   │
│        sim_marketplace_search · sim_marketplace_info                             │
└───┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬────────────┘
    │          │          │          │          │          │          │
    │       physics    physics+  hardware   spatial     social   real-time
    │          │       render     │          │           │           │
 ┌──▼──┐   ┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌───▼───┐  ┌───▼───┐  ┌───▼───┐
 │MuJoCo│   │Isaac│  │Gazebo│  │ LimX │  │Resonite│  │VRChat │  │Unity3D│
 │:11046│   │:11049│  │:10991│  │:11044│  │:10979 │  │:10712 │  │:10831 │
 └──────┘   └──────┘  └──────┘  └──┬───┘  └───────┘  └───────┘  └───────┘
                                    │
                              ┌─────▼─────┐
                              │  unitree  │
                              │  :11052   │
                              └───────────┘
                                    │
                              ┌─────▼─────┐
                              │  ros-mcp  │
                              │  :11050   │
                              └───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              ┌─────▼────┐   ┌──────▼──────┐  ┌────▼────┐
              │World Labs│   │   Blender   │  │  ROS 2  │
              │ :10865   │   │   :10849    │  │ network │
              │ 3D worlds│   │ furniture/  │  │ (real   │
              │ terrain  │   │   assets    │  │ robot)  │
              └──────────┘   └─────────────┘  └─────────┘
                         ▲                    ▲
                         │ Environment        │ Real hardware
                         │ generators         │ bridge
```

## Backend Registry

| ID | Name | Backend | Frontend | Role |
|----|------|---------|----------|------|
| `mujoco` | MuJoCo (DeepMind) | :11046 | :11047 | Fast physics, differentiable, GPU parallel, contact-rich |
| `isaac` | Isaac Sim (NVIDIA) | :11049 | :11048 | Photorealistic, GPU physics, synthetic data, RTX |
| `gazebo` | Gazebo (OSRF) | :10991 | :10990 | Sensor simulation, ROS native, terrains, outdoor |
| `limx` | LimX Robotics | :11044 | :11045 | TRON 1, Oli, VLA policies, RL deployment |
| `unitree` | Unitree Robotics | :11052 | :11053 | Go2, H1, H1-2, G1, B2, MuJoCo + ROS 2 |
| `resonite` | Resonite (XR) | :10979 | :10978 | XR worlds, spatial audio, avatars, multi-user |
| `vrchat` | VRChat | :10712 | :10712 | Social VR, user-generated worlds, avatars |
| `unity3d` | Unity 3D | :10831 | :10830 | Real-time 3D, physics engine, asset pipeline |
| `worldlabs` | World Labs (Marble) | :10865 | :10864 | 3D world generation, image/text-to-world, splats |
| `blender` | Blender | :10849 | :10848 | 3D modelling, furniture, assets, sculpting, animation |

## Middleware

| ID | Name | Port | Role |
|----|------|------|------|
| `ros` | ros-mcp | :11050 | ROS 2 bridge — topics, services, params, bags, launch |

## Decision Tree

```
"What do you want to do?"
│
├─ Physics simulation ──────────────────┬─ Fast, differentiable → MuJoCo
│                                       ├─ Sensors, ROS, outdoor → Gazebo
│                                       ├─ Photorealistic, GPU → Isaac Sim
│                                       └─ Hardware-specific (LimX) → limx-robotics-mcp
│
├─ Spatial / XR ────────────────────────┬─ XR worlds, avatars → Resonite
│                                       ├─ Social VR, VRChat → VRChat
│                                       └─ Real-time 3D scenes → Unity3D
│
├─ Robot control ───────────────────────┬─ ROS 2 topic/service → ros-mcp
│                                       ├─ Coordinated multi-sim → robotics-mcp
│                                       └─ Hardware-specific (LimX, yahboom) → platform MCP
│
└─ "I don't know" ─────────────────────→ sim_fleet_route probes all, picks best
```

## Tool Pattern (All Sim MCPs)

Every simulation MCP follows the same 14-tool pattern:

### Core Sim Tools (9)
1. `sim_status` / `ros_status` — health check
2. `load_model` / `load_world` / `load_scene` — depot ingestion
3. `start_sim` — launch background process
4. `stop_sim` — terminate
5. `get_state` — read simulation state
6. `apply_control` — send commands
7. `list_models` / `list_worlds` / `list_scenes` — depot browser
8. `list_jobs` — active and completed jobs
9. `export_frame` — render output (where applicable)

### AI Tools (5)
10. `agentic_sim_workflow` — multi-step LLM planning
11. `natural_language_control` — NL → actuator commands
12. `analyze_sim_state` — LLM describes robot behavior
13. `analyze_sim_logs` — LLM diagnoses issues
14. `discover_model` — LLM finds and loads models

## State Machine Standard

All sim MCPs use the same state machine pattern (`state_machine.py`, 0 external deps):

```
IDLE → MODEL_LOADED → STARTING → RUNNING → STOPPING → STOPPED
                           ↘ CRASHED ↗
```

Reference implementation in `mujoco-mcp/src/mujoco_mcp/state_machine.py`:
- `SimState` enum (8 states)
- `SimJob` dataclass (process, timestamps, error info)
- `transition_*` helpers with guard assertions
- `_on_enter_state` lifecycle hooks

## AI Workflow Standard

All AI tools support dual execution:
1. **MCP sampling** (`ctx.sample()`) — uses host LLM (Claude Desktop, Cursor)
2. **Ollama fallback** — `http://localhost:11434/api/generate` when sampling unavailable

The pattern is:
```python
try:
    result = await ctx.sample(prompt)
    # use sampling result
except Exception:
    import httpx
    resp = httpx.post("http://127.0.0.1:11434/api/generate", ...)
    # use Ollama result
```

## Orchestrator Tools (robotics-mcp)

| Tool | Description |
|------|-------------|
| `sim_fleet_status` | Probe all backends, report availability |
| `sim_fleet_route` | Pick best backend for a task by keyword matching |
| `sim_fleet_backends` | List all registered backends statically |
| `sim_marketplace_search` | Search curated robot model catalog with LLM fallback |
| `sim_marketplace_info` | Get full metadata for a specific model |

## Port Summary

| Range | Assignment |
|-------|-----------|
| 10700–10899 | Hardware-specific MCPs |
| 10900–10999 | Fleet services |
| 11044–11045 | limx-robotics-mcp |
| 11046–11047 | mujoco-mcp |
| 11048–11049 | isaac-mcp |
| 11050–11051 | ros-mcp |
| 11052–11053 | unitree-mcp |
