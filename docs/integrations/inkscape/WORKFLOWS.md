# Inkscape Workflows: Automated Graphics

These workflows define the automated vector processing patterns in the Sandra ecosystem.

## 📐 Workflow: "The Fleet Topology Generator"

Used for creating an up-to-date visual map of the 58-service fleet.

1.  **Data Ingestion**: Agent reads the current `apps_catalog.py` to get the list of active services.
2.  **Node Generation**: `inkscape_mcp` uses `generate_topology_node` to spawn symbols for each service.
3.  **Connection Mapping**: Agent calculates lines and arrows based on service dependencies.
4.  **Polish**: `edit_svg_element` adds title text and version markers.
5.  **Export**: `export_to_bitmap` creates a 4K PNG for the **mcp-central-docs** landing page.

## 🤖 Workflow: "2D Blueprint for Fabrication"

Preparing precision diagrams for 3D printing or CNC.

1.  **Source**: Export a 2D cross-section from **Blender**.
2.  **Refinement**: Inkscape standardizes the path strokes and scales to exact millimeters.
3.  **Export**: The finalized PDF/DXF is moved to the **Robotics Project** folder.

---
*Last updated: 2026-02-14*
