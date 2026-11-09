# Adobe Substance 3D Painter: The Archetype TextureCraft Clones, and How It Fits the Craft Suite

**Status:** Research & Analysis Doc | **Date:** 2026-11-01  
**Subject:** Adobe Substance 3D Painter (formerly Allegorithmic Substance Painter), the industry-standard PBR texture painting package cloned and adapted by `storytold/texturecraft`.  
**Evidence Base:** Source tree at `_upstream/texturecraft` (ArtCraft suite), live command and crate registry (11 crates, egui + wgpu architecture), documentation, and comparative teardowns against Adobe Substance 3D Painter 10.x / Substance Designer / ArmorPaint.  

**Related Documents:**
- `mcp-central-docs/patterns/CRAFT_MULTI_APP_FLOWS.md` — multi-app Craft workflows
- `mcp-central-docs/research/2026-10-29-fusion-360-and-solidcraft-parity.md` — SolidCraft CAD analysis
- `mcp-central-docs/reference/COOL_REPOS.md` — upstream repo index
- `_upstream/texturecraft/README.md` — upstream specification

---

## 1. Executive Summary: What Does TextureCraft Clone?

**TextureCraft clones Adobe Substance 3D Painter** (originally developed by Allegorithmic, acquired by Adobe in 2019).

Substance 3D Painter is the undisputed industry standard for texturing 3D assets across AAA game development, visual effects, animation, and industrial design. Prior to Substance Painter's rise in 2014–2016, texturing required flattening 3D models into 2D UV texture layouts and hand-painting color, bump, and specular maps in 2D software like Photoshop. Substance Painter revolutionized the industry by introducing:
1. **Direct 3D PBR Painting:** Brushing textures directly onto the 3D polygonal surface across complex UV seams.
2. **Layered Material Channel Blending:** A unified layer stack driving multiple PBR channels simultaneously (Base Color, Roughness, Metallic, Normal, Height, Ambient Occlusion, Opacity).
3. **Baked Mesh Map Generators:** Baking surface geometry (curvature, ambient occlusion, world normals, thickness, position) to drive procedural "Smart Materials" and "Smart Masks" (e.g. edge-wear on exposed convex edges, dirt and grime accumulation in concave crevices).

TextureCraft is an open-source, pure-Rust, zero-telemetry, zero-subscription reimplementation of this exact paradigm.

---

## 2. Feature-by-Feature Parity: Substance 3D Painter vs. TextureCraft

| Substance 3D Painter Standard | TextureCraft Implementation (`_upstream/texturecraft`) | Architectural Mechanism |
|---|---|---|
| **Workspace Layout** | Asset shelf (left), 3D/2D synchronized viewport (center), Texture Sets, Layer Stack, and Properties (right) | Single-workspace egui docking layout (`crates/ui-egui`) |
| **PBR Multi-Channel Engine** | Channels: Base Color, Roughness, Metallic, Normal, Height, AO, Emissive, Opacity | Multi-channel texel composition engine (`crates/compose`, `crates/texel`) |
| **Mesh Map Baking** | Ray-traced baking: AO, Curvature, World Normal, Position, Thickness, ID Map | GPU ray-traced mesh map baking via wgpu compute shaders (`crates/bake`, ~12× faster than CPU) |
| **Smart Materials & Masks** | Procedural generators driven by mesh maps (edge-wear, rust, cavities) | Mask generators & material graph shaders (`crates/engine/src/materials.rs`) |
| **3D Seamless Painting** | 3D surface projection across UV seams with surface normal falloff | Surface stamp raycasting & seam stitching (`crates/paint/src/brush.rs`) |
| **Rendering Preview** | **F10** key switches to Iray GPU path tracing with denoising | **F10** Rendering Mode path traces on GPU at 256+ samples with denoiser (`crates/render`) |
| **Project File Format** | `.spp` (proprietary Substance Painter project container) | `.tcraft` (lossless, copy-on-write snapshot container) |
| **Export Presets** | Channel packing presets for Unreal Engine 5, Unity URP/HDRP, glTF, USD, Blender | Configurable export templates with arbitrary channel packing and bit depths (`crates/formats`) |
| **Agent Automation** | Python / QML scripting API (cumbersome, often requires GUI attach) | **First-class MCP server** (`texturecraft-cli -- mcp`) + JSON control channel on port 7878 |

---

## 3. The SolidCraft + TextureCraft Synergy in the Fleet

In the ArtCraft ecosystem, applications form specialized creative chains:
- **SolidCraft** (`_upstream/solidcraft`): Parametric CAD solid modeling (cloning Autodesk Fusion). Emits precise B-Rep solids and triangulated meshes (`.glb`, `.obj`, `.step`).
- **TextureCraft** (`_upstream/texturecraft`): Ingests the 3D meshes produced by SolidCraft or external DCCs, bakes curvature and occlusion maps, applies PBR wear, weathering, coatings, and paint, and exports textured GLB or engine-ready PBR maps.
- **LookCraft / GameCraft / FilmCraft**: Consumes the textured PBR assets for scene assembly, real-time gaming, and cinematic rendering.

This creates a complete end-to-end open-source 3D content creation pipeline without Autodesk, Adobe, or cloud lock-in.

---

## 4. Technical Analysis of TextureCraft's Architecture

TextureCraft is split into 11 specialized Rust crates under `crates/`:

```
crates/
  core        L0  Domain entities, color models, PBR channel definitions
  geom        L0  Mesh representations, UV unwrap parsing, primitive meshes
  formats     L0  Mesh and image format I/O (glTF, FBX, OBJ, USD, EXR, HDR, PNG)
  texel       L1  Tiled, copy-on-write texel buffer engine with CPU multithreading
  paint       L1  Brush stroke dynamics, alpha stamps, symmetry, projection
  bake        L2  GPU ray-traced mesh bakers (AO, curvature, thickness, normals)
  compose     L2  Layer stack compositing, blend modes, procedural pattern generators
  render      L3  Interactive GPU path-tracer (wgpu) with real-time denoiser
  engine      L4  Session state, project management, command history, undo snapshots
  automation  L5  JSON control socket, CLI command runner, stdio MCP server
  ui-egui     L6  Desktop interface with split 3D/2D viewports and docking panels
```

### Strengths & Notable Highlights
- **Pure-Rust & Memory Safe:** No panics in production crates (`#![deny(clippy::unwrap_used)]`).
- **Zero Asset Piracy:** All bundled materials, environments (IBL), brush alphas, and procedural primitives are procedurally synthesized in code (documented in `ATTRIBUTION.md`).
- **Headless & Agent-Native:** Full headless rendering and export via `texturecraft-cli render` and `texturecraft-cli export`, making it directly automatable by coding agents via MCP.
