# Gazebo: Multi-Robot Simulation & Physics

Gazebo is the primary physics-based simulation engine in the **Sandra** ecosystem, used to validate robotics algorithms, test sensory perception, and train neural controllers in a safe virtual environment before physical deployment.

## 🏛️ Role in the Sandra Ecosystem

- **Physics Validation**: Simulating gravity, friction, and collision dynamics for **Unitree** and **Scout** robots.
- **Sensor Emulation**: Providing high-fidelity data for LiDAR, cameras, and IMU sensors in a synthetic environment.
- **Fleet Training**: Orchestrating multi-robot scenarios to test cooperative behavior and urban navigation.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): Physics engines (ODE, DART), SDF standards, and ROS 2 bridging.
- [Gazebo MCP Server](gazebo-mcp-server.md): THE agentic control layer for spawning entities and world management.
- [Free Marketplaces](MARKETPLACES.md): **CRITICAL** guide to free model resources (Fuel, models, and community assets).
- [Sandra Workflows](WORKFLOWS.md): Automated simulation testing and virtual environment generation.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
