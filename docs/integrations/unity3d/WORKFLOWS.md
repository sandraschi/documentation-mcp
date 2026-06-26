# Unity3D Workflows: Virtual Deployment

These workflows define the life-cycle of virtual simulation and XR authoring in Unity.

## 🦾 Workflow: "Rigid Physics Validation"

Used to test a robot's mechanical design before physical fabrication.

1.  **Import**: Agent triggers `spawn_robot_prefab` to load the **Blender** export.
2.  **Environment Setup**: Agent spawns the "Stroheckgasse Apartment" environment using **Marble** assets.
3.  **Sensor Initialization**: Agent verifies that the virtual **Livox LiDAR** is correctly outputting ray-casts.
4.  **Test Run**: Agent executes a navigation script and monitors for collisions via `inspect_hierarchy`.

## 🎭 Workflow: "Social VR Avatar Export"

The bridge between Unity simulation and social presence.

1.  **Scene Cleaning**: Agent disables all simulation-specific scripts.
2.  **VRChat SDK Check**: Agent runs the SDK validation tool via `unity3d_mcp`.
3.  **OSC Mapping**: Agent maps social parameters (e.g., eye tracking) using the **OSC MCP**.
4.  **Build & Upload**: Agent triggers the VRChat build script to deploy the avatar.

---
*Last updated: 2026-02-14*
