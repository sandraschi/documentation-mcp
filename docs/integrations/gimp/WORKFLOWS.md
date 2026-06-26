# GIMP Workflows: Procedural Media

These workflows define the automated image processing pipelines in the Sandra ecosystem.

## 🎨 Workflow: "The Robot Texturing Pipeline"

Bridge between raw reference images and 3D models.

1.  **Extraction**: Agent captures a high-res photo of the physical robot chassis.
2.  **Processing**: `gimp_mcp` applies `generate_pbr_maps` to create a seamless texture set.
3.  **Optimization**: Maps are scaled to 2K (Standard) or 4K (Ultra) based on the target node.
4.  **Sync**: Files are moved to the **Blender** project folder for automated material mapping.

## 📝 Workflow: "SOTA Documentation Polish"

Used for preparing visual assets for the fleet documentation.

1.  **Capture**: Agent takes a screenshot of a new UI component.
2.  **Branding**: `gimp_mcp` applies a SOTA-compliant border and shadow.
3.  **Labeling**: `annotate_technical` adds version control markers and timestamps.
4.  **Deployment**: The finalized asset is registered in the **mcp-central-docs** frontend.

---
*Last updated: 2026-02-14*
