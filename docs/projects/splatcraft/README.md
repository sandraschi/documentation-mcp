# SplatCraft

**Version**: v0.1.0 — Pure-Rust 3D Gaussian Splatting Studio & Radiance Field Pipeline.
**Repository**: [`d:\Dev\repos\splatcraft`](file:///d:/Dev/repos/splatcraft) | [GitHub: sandraschi/splatcraft](https://github.com/sandraschi/splatcraft)
**Parent Suite**: Sovereign Craft Suite / Spatial & 3D

---

## Features & Architecture

```
splatcraft-core (PLY/Splat Parser / Spherical Harmonics / Rasterizer)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
splatcraft-mcp (L1/L2)                        splatcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (wgpu / egui 0.37 Splat Viewport)
```

- **Consolidates Fleet Repos**: `splatmaker-mcp`, `blender-mcp`, `vroidstudio-mcp`.
- **Pure-Rust Radiance Fields**: Zero C++/CUDA dependencies for playback; native `wgpu` compute shaders.
- **PLY & Splat Ingestion**: Ingests, crops, optimizes, and exports compressed Gaussian splat scenes.
