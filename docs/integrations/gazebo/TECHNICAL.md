# Gazebo: Technical Specifications

This document outlines the simulation environment configuration on the Sandra workstation.

## 💻 Simulation Engine

- **Application**: **Gazebo Sim** (The modern rewrite, formerly Ignition).
- **Physics**: **DART** (Dynamic Animation and Robotics Toolkit) is the default for high-precision joint simulation.
- **Rendering**: **Ogre 2** for high-fidelity visual simulation, utilizing the **RTX 4090**.

## ⚙️ Configuration & Standards

- **SDF (Simulation Description Format)**: Version 1.9+ is the fleet standard.
- **ROS 2 Bridge**: Mandatory `ros_gz_bridge` integration for the **Humble/Iron** distributions.
- **Protocols**: Transport library uses Protobuf for high-speed inter-process communication.

## 🛡️ Sensor Standards
- **LiDAR**: Livox Mid-360 emulation via the `livox_laser_simulation` plugin.
- **Depth Cameras**: Realsense D435i emulation with accurate noise models.

---
*Last updated: 2026-02-14*
