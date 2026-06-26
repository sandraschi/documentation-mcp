# FreeCAD — Open-Source Parametric 3D CAD Modeller

**Version in fleet**: 1.1.1 (2026-04-14, portable)  
**Kernel**: OpenCASCADE Technology (OCCT) 7.9  
**License**: LGPL-2.0+  
**Repo**: [github.com/FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD)  
**Website**: [freecad.org](https://www.freecad.org)  

---

## What It Is

FreeCAD is a free, open-source parametric 3D CAD modeller for mechanical engineering and product design. It is **not** a mesh modeller (like Blender) — it creates solid models with a parametric feature tree that can be edited non-destructively. STEP files export to STL for 3D printing, web visualization, or further processing.

The fleet uses FreeCAD as the CAD backend for `freecad-mcp` (STEP → STL conversion, geometry creation, model metadata extraction).

---

## History

| Year | Milestone |
|------|-----------|
| 2001 | Project started by **Jürgen Riegel** (formerly involved with QCAD/CAM) |
| 2003 | First public release with basic geometry operations |
| 2011 | Move to Git/GitHub, community begins growing |
| 2014 | **OCCT 6.8** integration, Part Design workbench matures |
| 2019 | **FreeCAD 0.18** — stable LTS release, FEM workbench production-ready |
| 2021 | **FreeCAD 0.19** — massive community release with Assembly3 workbench |
| 2022 | **FreeCAD 0.20** — toponaming mitigation, Link improvements |
| 2024 | **FreeCAD 1.0** — first major version jump, integrated Assembly workbench, toponaming fix |
| 2026 | **FreeCAD 1.1.1** — current fleet version, ongoing improvements |

The project started as a single-developer effort and has grown to ~300+ contributors per release, backed by donations, bounties, and corporate sponsors (including NVIDIA, Microsoft, and Google through their respective open-source programmes).

---

## CAD Kernel: OpenCASCADE Technology (OCCT)

FreeCAD is built on **OCCT** (OpenCASCADE Technology), a professional-grade CAD kernel used by many commercial applications (including CATIA's geometric modeler in earlier versions). OCCT provides:

- **B-rep (Boundary Representation)** solid modelling — the industry standard for precise mechanical CAD
- **STEP/IGES import/export** — full AP203, AP214, AP242 support
- **Boolean operations** (fuse, cut, intersect)
- **Tessellation** — converts precise B-rep surfaces to triangle meshes (STL, OBJ)
- **Parametric curves and surfaces** — NURBS, Bezier, splines
- **Datum geometry** — planes, axes, coordinate systems

OCCT is LGPL-licensed, maintained by a community of contributors, and used by FreeCAD, Salome, and various commercial products.

---

## Key Workbenches

| Workbench | Purpose |
|-----------|---------|
| **Part** | Primitive geometry (box, cylinder, sphere, cone, torus), boolean operations |
| **Part Design** | Parametric feature tree: pads, pockets, revolutions, fillets, chamfers |
| **Sketcher** | 2D constraint-based sketching — the foundation for Part Design features |
| **Assembly** | Constrain parts together (bolts, mates, alignments) — new in 1.0 |
| **Draft** | 2D drafting and annotation, DXF import/export |
| **TechDraw** | Engineering drawings from 3D models (views, dimensions, annotations) |
| **Mesh** | STL/OBJ mesh import, repair, export |
| **FEM** | Finite Element Method analysis (structural, thermal, fluid) |
| **CAM/Path** | CNC toolpath generation (milling, drilling) |
| **Spreadsheet** | Parameter-driven dimensions from spreadsheet cells |
| **Fluent** | Python scripting console and macro recording |

---

## Fleet Integration

FreeCAD is used in these fleet repos:

| Repo | Purpose |
|------|---------|
| **freecad-mcp** | FastMCP 3.2 server — STEP→STL, model info, geometry creation |
| **yahboom-mcp** | STEP file conversion for Raspbot v2 3D visualisation (Viz.tsx) |

The `freecad-mcp` server runs FreeCAD's GUI in headless/bridge mode on a TCP socket, sending JSON commands to import, analyse, and export CAD files. This avoids the ~2 GB FreeCAD footprint in the server process and allows full AP214 assembly support.

---

## Community

- **Forum**: [forum.freecad.org](https://forum.freecad.org/) — primary support channel, very active
- **GitHub**: [github.com/FreeCAD/FreeCAD](https://github.com/FreeCAD/FreeCAD) — ~30k stars, ~300 contributors
- **Discord**: [discord.gg/kZaq3Vd5Mr](https://discord.gg/kZaq3Vd5Mr) — real-time help
- **YouTube**: [youtube.com/@FreeCADChannel](https://youtube.com/@FreeCADChannel) — official tutorials
- **Reddit**: [r/FreeCAD](https://reddit.com/r/FreeCAD) — 250k+ members
- **Open Collective**: [opencollective.com/freecad](https://opencollective.com/freecad) — donation-based funding
- **Bounties**: [funded.dev/freecad](https://funded.dev/freecad) — community bounties for features

Notable corporate contributors and users: NVIDIA (GPU acceleration), Google (Google Summer of Code), Microsoft (GitHub sponsor), Boeing, Airbus, and numerous hardware startups.

---

## Limitations vs Commercial CAD

| Aspect | FreeCAD | SolidWorks / Fusion 360 |
|--------|---------|------------------------|
| **Assembly performance** | Adequate for <500 parts | Smooth for 10,000+ parts |
| **Large assembly STEP import** | Works but slower | Optimised |
| **FEA integration** | Built-in (CalculiX) | Built-in (SimScale/Ansys) |
| **Surface modelling** | Limited surfacing workbench | Full NURBS surfacing |
| **UI polish** | Functional, less polished | Production-grade UX |
| **File format support** | STEP, IGES, OBJ, DXF, STL, FCStd | Full native + all exchange formats |
| **Price** | Free (LGPL) | €1,500-5,000/year |

For the fleet's use case — converting mechanical STEP assemblies to web-viewable STL — FreeCAD is the optimal choice. The AP214 assembly import under the GUI (which the bridge provides) handles even complex robot CAD files.

---

## Building from Source

FreeCAD can be built from source using CMake. Dependencies: OCCT >= 7.9, Python >= 3.10, Qt >= 5.15, PySide6, Shiboken6. Windows builds use the `conda` cross-platform recipe maintained by the FreeCAD build team. The portable distribution used by the fleet is built from the official conda forge recipe.
