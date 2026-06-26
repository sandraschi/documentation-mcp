# Blender Workflows: The Sandra Lifecycle

These multi-step workflows define how Blender integrates with the broader Sandra fleet.

## 🤖 Workflow: "From Blueprint to Unity"

This workflow describes the process of creating a new robot asset and moving it into simulation.

1.  **Chassis Generation**: Agent uses `generate_robot_mesh` in **Blender** to create the core geometry based on hardware specs.
2.  **Texture Baking**: Agent triggers **GIMP** to generate PBR maps, then applies them in Blender via `apply_shader_textures`.
3.  **Rigging Validation**: Agent runs therig validation script to ensure bone names match the **Unity3D** humanoid standard.
4.  **Export**: Agent triggers `export_fbx_rigged`.
5.  **Sim-Import**: Agent uses **Unity3D MCP** to spawn the model into a test world.

## 🖼️ Workflow: "Technical Documentary Snapshot"

Used for creating high-fidelity visual documentation for SOTA milestones.

1.  **Scene Lighting**: Agent automates lighting placement using the `manage_scene_lights` tool.
2.  **Camera Focus**: Agent aligns the active camera to the target component (e.g., the Livox LiDAR mount).
3.  **Cycles Render**: Agent executes `trigger_batch_render` at 4K resolution.
4.  **Pathing**: The final image is moved to the **mcp-central-docs** assets folder for embedding.

---
*Last updated: 2026-02-14*
