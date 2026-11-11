# RobotCraft Specification & Architecture Plan
**Embodied Intelligence Studio & Universal Robotics Operating Environment**

**Version**: 0.1.0-DRAFT  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Robotics Telemetry, Kinematics, Gazebo/Isaac Simulation, Multi-Robot Swarm Control  
**Standard Port**: 14116 (Assigned via fleet registry)  

---

## 1. Executive Summary & Fleet Consolidation

### The Fragmented State of the Fleet
The `sandraschi` workspace currently maintains exceptional, deep robotics servers, but they are completely siloed:
- `robotics-mcp`: Generic kinematics and spatial geometry.
- `ros-mcp`: ROS 1 / ROS 2 topic subscriber and action server bridge.
- `gazebo-mcp`: Gazebo physics world step control and entity spawner.
- `unitree-mcp`: Go1 / Go2 / B2 quadruped locomotion and posture telemetry.
- `yahboom-mcp` & `rust-yahboom-mcp`: ROSMASTER / Jetbot serial protocol and camera pan-tilt.
- `limx-robotics-mcp`: Bipedal humanoid / wheeled-biped balance control.
- `norirobotics-mcp`: Industrial 6-DOF arm path planning and inverse kinematics.
- `vbot-mind-mcp`: High-level behavior tree and goal planning.

### The RobotCraft Synthesis
RobotCraft consolidates all physical hardware drivers, simulators, and kinematic math into **a single unified robotics workstation and universal MCP environment**:

```
                         ┌─────────────────────────────┐
                         │       RobotCraft Studio     │
                         │    (Native wgpu 3D + egui)  │
                         └──────────────┬──────────────┘
                                        │ Universal Command Bus
         ┌──────────────────────────────┼──────────────────────────────┐
         ▼                              ▼                              ▼
  ┌─────────────┐               ┌─────────────┐                ┌─────────────┐
  │ Kinematics  │               │ Simulators  │                │   Hardware  │
  │  & Planning │               │ & Digital   │                │   Adapters  │
  │ • URDF / SDF│               │   Twins     │                │ • Unitree   │
  │ • Forward/IK│               │ • Gazebo    │                │ • Yahboom   │
  │ • Obstacles │               │ • Isaac Sim │                │ • ROS 2 DDS │
  │ • RRT* / SLAM               │ • MuJoCo    │                │ • Serial/CAN│
  └─────────────┘               └─────────────┘                └─────────────┘
```

---

## 2. Core Architecture: The 4 Operational Layers

```
Layer 4: AI & Autonomous Agents
  • Vision-Language-Action (VLA) inference bridge
  • Stigmergic multi-robot task allocation
  • Natural language mission control ("Inspect zone B for oil leaks")
──────────────────────────────────────────────────────────────────
Layer 3: Studio GUI & Visualization (wgpu + egui)
  • Real-time 3D URDF model rendering with joint angle articulation
  • LiDAR point-cloud viewer & 2D occupancy grid SLAM visualizer
  • Virtual analog sticks, faders, emergency kill-switches
──────────────────────────────────────────────────────────────────
Layer 2: Universal Kinematics & Spatial Engine (robotcraft-core)
  • Forward & Inverse Kinematics (DH parameters & Pinocchio/nalgebra)
  • Dynamic collision detection & safety fence enforcement
  • Universal trajectory interpolation (cubic splines, trapezoidal velocity)
──────────────────────────────────────────────────────────────────
Layer 1: Real-Time Hardware & Transport Abstraction (robotcraft-hal)
  • Serial / USB UART (Yahboom, Arduino, Bus Pirate)
  • Ethernet / CAN bus (Unitree Go2 High/Low-Level UDP, LimX)
  • ROS 2 DDS native client (CycloneDDS / Zenoh bridge)
```

---

## 3. Crate Architecture (ArtCraft 3-Tier Standard)

```
robotcraft/
├── Cargo.toml
├── justfile
├── AGENTS.md
├── crates/
│   ├── robotcraft-hal/        # Hardware Abstraction Layer
│   │   ├── src/
│   │   │   ├── unitree.rs     # Quadruped UDP protocol (Low/High level)
│   │   │   ├── yahboom.rs     # Jetbot & ROSMASTER serial framing
│   │   │   ├── ros2.rs        # Zenoh/DDS topic publisher & subscriber
│   │   │   └── serial_can.rs  # USB-CAN & UART transport
│   ├── robotcraft-core/       # Kinematics, URDF Parsing, Trajectory Bus
│   │   ├── src/
│   │   │   ├── lib.rs         # Command::dispatch & JSON-RPC registry
│   │   │   ├── urdf.rs        # Robot model loader & joint tree
│   │   │   ├── ik.rs          # 6-DOF & leg inverse kinematics
│   │   │   ├── trajectory.rs  # Waypoint planner with acceleration limits
│   │   │   └── slam.rs        # 2D/3D point cloud & occupancy map
│   ├── robotcraft-mcp/        # FastMCP 2024-11-05 Stdio Server & CLI
│   │   └── src/main.rs        # robotcraft-cli teleop, stream, record, sim
│   └── robotcraft-app/        # Native Studio GUI (egui + wgpu 3D viewport)
│       └── src/
│           ├── main.rs        # Smoke test & window bootstrap
│           ├── gui.rs         # HUD, joint sliders, telemetry graphs
│           └── viewport_3d.rs # wgpu 3D scene, joint mesh renderer, camera orbits
```

---

## 4. Universal Command Bus Schema

| Command Identifier | Input Payload | Output Payload | Description |
|---|---|---|---|
| `robot.connect` | `adapter: String, address: String` | `session_id, hardware_info, battery_pct` | Establishes communication with robot |
| `robot.teleop` | `linear_x, linear_y, angular_z` | `current_velocity, status` | Real-time velocity/twist command |
| `robot.pose.set` | `joint_angles: Vec<f32>` | `actual_angles, ik_error` | Set arm or leg joint positions |
| `robot.urdf.load` | `urdf_xml: String` | `joint_names, link_tree, dof` | Loads and parses robot model |
| `robot.sim.step` | `dt: f32` | `world_state, contact_forces` | Advances physics simulation step |
| `robot.emergency_stop` | `reason: String` | `motors_disabled: bool` | Hardware-enforced kill switch |

---

## 5. Integration with the Fleet

- **DatabaseCraft Synergy**: All mission waypoints, LiDAR map snapshots, telemetry logs, and maintenance logs store directly in DatabaseCraft's `field_service` or custom robotics tables (`mission_telemetry.dbcraft`).
- **LookCraft & ArtCraft Synergy**: Mission operational reports compile into `WordCraft` and `PdfCraft`. Visual camera feeds export to `FilmCraft`.
