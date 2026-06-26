# Gazebo Workflows: Virtual Prototyping

These workflows define the automated robotics simulation patterns in the Sandra ecosystem.

## 🤖 Workflow: "The Obstacle Avoidance Audit"

Testing a new navigation algorithm in a randomized environment.

1.  **Generation**: Agent spawns a "Stroheckgasse Apartment" world.
2.  **Randomization**: `gazebo_mcp` command triggers `spawn_entity` for 5 randomized obstacles from **Gazebo Fuel**.
3.  **Deployment**: Agent spawns a **Unitree Go2** at the origin.
4.  **Execution**: The navigation script begins. Agent monitors telemetry and records any collisions.
5.  **Iteration**: Simulation is reset, obstacles are moved, and the test repeats.

## 🛰️ Workflow: "LiDAR Perception Mapping"

Validating the **Livox Mid-360** visual range.

1.  **Assembly**: Agent builds a complex industrial scene using assets from the **MARBLE-Project**.
2.  **Actuation**: Agent commands the robot to rotate 360 degrees.
3.  **Metrology**: Agent collects the synthetic point cloud data via the ROS 2 bridge.
4.  **Analysis**: Agent compares the synthetic map against the theoretical "Ground Truth" floor plan.

---
*Last updated: 2026-02-14*
