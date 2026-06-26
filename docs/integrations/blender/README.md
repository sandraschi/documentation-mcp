# Blender: The 3D Geometry Core

Blender is the primary 3D engine in the **Sandra** ecosystem. While the fleet uses **Unity3D** for real-time simulation, Blender serves as the master authority for geometry creation, high-fidelity rendering, and robot rigging.

## 🏛️ Role in the Sandra Ecosystem

- **Master Asset Generator**: Every 3D model in the fleet (Unitree Go2, R1, Scout) is authored or refined in Blender before deployment.
- **Reference Visualization**: High-fidelity Cycles renders provide ground-truth visual data for the agentic vision systems.
- **Rigging Authority**: The bone structures used in the social VR platforms (**VRChat**, **Resonite**) are standardized using Blender's rigging toolset.

## 📂 Documentation Structure

- [Technical Specifications](TECHNICAL.md): Hardware requirements, install paths, and engine logic.
- [Agentic Control Layer](MCP_INTERFACE.md): The Blender MCP server interface and tools.
- [Sandra Workflows](WORKFLOWS.md): Multi-step patterns for model generation and export.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
