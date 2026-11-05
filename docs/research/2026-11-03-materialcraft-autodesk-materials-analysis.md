# Autodesk Materials & Substance Designer: The Archetype MaterialCraft Clones, and How It Fits the Craft Suite

**Status:** Research & Analysis Doc | **Date:** 2026-11-03  
**Subject:** Autodesk Materials (Revit / AutoCAD / 3ds Max physical materials) and Adobe Substance 3D Designer, the procedural material authoring archetypes cloned and unified by `storytold/materialcraft`.  
**Evidence Base:** Fresh binary inspection and live execution on Goliath (`C:\Program Files\MaterialCraft\materialcraft-cli.exe` v0.1.0 `cedabf0` installed 2026-11-02), live command registry (570 lines of commands), full node library inspection (12,000+ lines of node definitions across procedural noise, generators, blends, and color maps), sample graph cook benchmarks (98.7ms), and comparative analysis against Autodesk Material Library (`.adsklib`) and Adobe Substance Designer.  

**Related Documents:**
- `mcp-central-docs/research/2026-11-01-texturecraft-substance-painter-analysis.md` — companion 3D mesh painter doc
- `mcp-central-docs/research/2026-10-29-fusion-360-and-solidcraft-parity.md` — SolidCraft CAD analysis
- `mcp-central-docs/standards/rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md` — Craft CLI & MCP strategy
- `mcp-central-docs/patterns/CRAFT_MULTI_APP_FLOWS.md` — multi-app workflow pipelines
- `mcp-central-docs/reference/COOL_REPOS.md` — upstream repo index

---

## 1. Executive Summary: What Does MaterialCraft Clone?

**MaterialCraft clones the procedural material authoring workflows of Adobe Substance 3D Designer and the architectural PBR material systems of Autodesk (Revit, AutoCAD, 3ds Max, and Inventor).**

In modern 3D CAD and visualization workflows, materials have bifurcated into two approaches:
1. **Proprietary Architectural CAD Material Editors (Autodesk `.adsklib`):** Form-based physical properties specifying surface appearances (albedo, roughness, specular reflectance, bump/relief, tint) bundled with physical structural attributes for architectural rendering.
2. **Procedural Node-Based Material Graphs (Substance 3D Designer):** Math- and noise-driven directed acyclic graphs (DAG) that generate resolution-independent, tileable PBR texture sets from first principles without relying on static raster photos.

MaterialCraft merges these paradigms into a clean-room, pure-Rust desktop application and headless engine. It replaces subscription-locked, heavyweight authoring tools with an ultra-fast, local, deterministic procedural synthesizer.

---

## 2. Live Measurements on Goliath (2026-11-03)

Source of truth: `C:\Program Files\MaterialCraft\materialcraft-cli.exe` and `materialcraft.exe`.

- **Installed Version:** `materialcraft-cli 0.1.0 (cedabf0 2026-11-02)`
- **Binary Footprint:**
  - `materialcraft-cli.exe`: 13.9 MB (13,960,064 bytes)
  - `materialcraft.exe` (GUI): 29.2 MB (29,228,928 bytes)
- **Engine Command Surface:** 570 lines of structured commands via `materialcraft-cli commands`.
- **Node Library Surface:** 12,004 lines of node specifications (`materialcraft-cli nodes`) covering procedural noise, pattern generators, edge wear, filters, and mathematical composition.
- **Cook Performance:** A full 24-node procedural brick wall package (`sample`) cooks in **98.8 ms** total on CPU, with individual generator passes taking < 1 ms and heavy procedural noise (Clouds, Grunge) taking ~15–19 ms.

---

## 3. Feature-by-Feature Parity

| Archetype Feature (Autodesk / Substance Designer) | MaterialCraft Implementation (`storytold/materialcraft`) | Architectural Mechanism |
|---|---|---|
| **Graph Authoring** | Node-based DAG connecting procedural generators, noises, transforms, and blend filters | Multi-threaded graph evaluation engine (`cook` verb, dependency topological sort) |
| **PBR Channel Mapping** | Base Color, Roughness, Metallic, Normal (OpenGL/DirectX), Height/Displacement, Ambient Occlusion | Dedicated semantic output nodes (`def: "output"` with `usage: enum`) |
| **Procedural Primitives** | Brick generator, tile patterns, clouds, Perlin/Simplex/Worley noise, grunge maps | Native Rust generators with parameterized math (`brick_generator`, `grunge_map_1`, `clouds_2`) |
| **Non-Destructive Editing** | Instant parameter tweaking (`--set roughness=0.4 --set tint="#aa7744"`) | Parameterized exposed inputs on graphs (`inputs: {}`, dynamic re-cook) |
| **Real-Time 3D Preview** | Viewport displaying material on 3D geometry with IBL studio lighting | 3D viewport scenes: `rounded_cube`, `cube`, `sphere`, `cylinder`, `plane`, `torus`, `material_ball` |
| **Offline / Beauty Rendering** | Arnold / Iray high-quality ray tracing | Headless `--hq` beauty renderer with true height displacement, AO, and key lighting (no GPU required) |
| **Package Container** | `.sbs` / `.sbsar` (Substance) or `.adsklib` (Autodesk) | `.mcraft` (structured JSON package containing graphs, resources, and exposed properties) |
| **Export Formats** | High-bitdepth PBR map export (8, 16, 32-bit float/int) | Multi-format exporter (`export` verb: PNG, JPG, TGA, TIF, BMP, WebP, EXR, HDR) |
| **Headless / Agent API** | Python Automation API / Autodesk Dynamo scripting | **First-class MCP server** (`materialcraft-cli mcp`) and JSON-RPC daemon (`materialcraft-cli serve --port <port>`) |

---

## 4. Architectural CAD & BIM Fit: Autodesk Materials vs. MaterialCraft

### Where Autodesk Materials Dominates
In Autodesk Revit and AutoCAD, materials are not solely graphical textures. An Autodesk Material contains:
- **Identity & Graphics:** Shading color, surface patterns (cut patterns, surface hatching).
- **Physical Assets:** Thermal conductivity, specific heat, density, tensile strength, and porosity for structural and energy simulations.
- **Certified Manufacturer Catalogs:** Pre-graded libraries from paint, brick, and glazing manufacturers.

### Where MaterialCraft Excels
- **Procedural Infinitude:** Rather than tiling a low-resolution photographic swatch that visibly repeats across large building facades, MaterialCraft synthesizes seamless, mathematically non-repeating architectural finishes (concrete, masonry, metal cladding, terrazzo, timber).
- **Lightweight Distribution:** A `.mcraft` package is a few kilobytes of code and graph recipes, rather than multi-gigabyte uncompressed texture archives.
- **Zero Cloud & License Lock-in:** Standalone executable running without Autodesk Desktop Licensing Service or cloud authentication checks.

---

## 5. The Craft 3D Trilogy: SolidCraft + MaterialCraft + TextureCraft

Within the ArtCraft suite, 3D asset creation forms a modular tripartite pipeline:

```
[ SolidCraft ] ----> B-Rep Solids / Meshes (.step, .obj, .glb)
       |
       +------------> [ MaterialCraft ] ----> Procedural PBR Textures / .mcraft
                             |                 (Albedo, Normal, Roughness, Height, AO)
                             v
                     [ TextureCraft ] ------> 3D Model Painting & Mesh Baking
                             |                 (Smart edge wear, decals, weathering)
                             v
                     [ LookCraft / GameCraft / Fleet Renders ]
```

1. **SolidCraft:** Authors parametric mechanical and architectural geometry (cloning Autodesk Fusion/Inventor).
2. **MaterialCraft:** Authors procedural architectural and PBR materials from math and graph nodes (cloning Autodesk Material Editor and Substance Designer).
3. **TextureCraft:** Paints those materials directly onto the 3D meshes with UV projection, seam blending, and baked curvature masks (cloning Substance 3D Painter).

---

## 6. Headless Automation, CLI & Native MCP Server

MaterialCraft implements the standardized ArtCraft automation interface:

```bash
# Inspect graph structure, nodes, and inputs
materialcraft-cli info <package.mcraft | sample>

# Create a package from a built-in template
materialcraft-cli new <bricks|wood|stone_tiles|metal_plates|ground> building_facade.mcraft

# Cook graph with overridden parameters
materialcraft-cli cook building_facade.mcraft --set roughness=0.35 --set tint="#8b4513"

# Render beauty pass of the material on a test sphere or architectural wall
materialcraft-cli render building_facade.mcraft preview.png --scene material_ball --hq

# Export cooked PBR maps in 16-bit TIFF or EXR
materialcraft-cli export building_facade.mcraft ./textures/ --format exr --depth 16

# Run as an interactive Model Context Protocol (MCP) server for agents
materialcraft-cli mcp --read-root D:/Dev/repos/assets --write-root D:/Dev/repos/output
```

This headless automation makes MaterialCraft an ideal procedural generation sidecar for coding agents generating CAD models, architectural visualizations, and game environments.
