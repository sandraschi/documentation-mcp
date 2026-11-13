# RobotCraft

**Version**: v0.1.0 — Embodied Intelligence Studio & Universal Robotics Operating Workstation.
**Repository**: [`d:\Dev\repos\robotcraft`](file:///d:/Dev/repos/robotcraft) | [GitHub: sandraschi/robotcraft](https://github.com/sandraschi/robotcraft)
**Control Port**: `14116` (`robotcraft --control 14116`)
**Parent Suite**: Sovereign Craft Suite / Craft Bundlers

---

## Architecture & Fleet Consolidation

RobotCraft is the primary robotics bundler, consolidating 9 disparate robotics servers:
- **Consolidates Fleet Repos**: `robotics-mcp`, `ros-mcp`, `gazebo-mcp`, `unitree-mcp`, `yahboom-mcp`, `limx`, `nori` (`norirobotics-mcp`: Nori A3 home robot, LeRobot recording, VR spawn), `vbot`, `rust-saschirob-mcp`.

```
robotcraft-core (Kinematics / URDF Parser / ROS2 Node Bridge)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
robotcraft-mcp (L1/L2)                       robotcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 3D Teleop & Actuator Canvas)
```

- Hardware telemetry, forward/inverse kinematics solvers, Gazebo simulation bridges, and physical actuator tele-op.
