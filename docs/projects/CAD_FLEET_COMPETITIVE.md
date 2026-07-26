# CAD Fleet Competitive Analysis

Last updated: 2026-05-28

Compares **qcad-mcp** (2D DXF) vs **freecad-mcp** (3D BIM/FEM/CFD) in the sandraschi MCP fleet.

## Executive summary

| | **qcad-mcp** | **freecad-mcp** |
|---|-------------|-----------------|
| **Domain** | 2D drafting, floor plans, DXF depot | 3D CAD, BIM, FEM, CFD, 3D print |
| **Engine** | ezdxf (+ optional QCAD Pro) | FreeCAD 1.1.1+ |
| **MCP tools** | 7 (plan_*) | 46+ |
| **CFD** | No | OpenFOAM + FluidX3D (GPU) |
| **Tauri** | Done | Done |
| **Ports** | 10966 / 10967 | 10944 / 10945 |
| **Uniqueness** | Lightweight 2D→3D extrusion for fleet | **Only fleet repo with full CFD + ML export pipeline** |

**Next repo for deep investment:** **freecad-mcp** if the goal is differentiated physics/CFD; **qcad-mcp** if the goal is fast 2D→Resonite/Unity floor-plan handoffs with minimal deps.

## qcad-mcp — strengths

- **Low friction**: pure Python + ezdxf; no heavy CAD install required for core tools.
- **Persistent CAD depot** with REST CRUD — agents and humans share the same file store.
- **Room analysis**: doors, windows, areas from DXF — strong for architecture agents.
- **Fleet bridge**: `plan_extrude` → STL for resonite-mcp / unity3d-mcp / blender-mcp.
- **Tauri native** already shipping pattern (10966/10967).

## qcad-mcp — gaps

- No physics simulation (by design).
- No IFC/BIM semantics (2D only).
- QCAD Pro optional path not required but limits DXF→PDF fidelity without it.

## freecad-mcp — strengths

- **CFD stack**: OpenFOAM (Docker) + **FluidX3D** (OpenCL GPU) — rare in open-source agent tooling.
- **Natural-language CFD**: LLM generates OpenFOAM case dictionaries from plain English.
- **FEM**: CalculiX structural analysis (stress, strain, safety factor).
- **BIM / Arch**: walls, slabs, IFC import/export — complements qcad 2D plans.
- **ML pipeline**: parametric sweeps → point clouds → surrogate models (replace slow sims).
- **Marketplace**: Printables / Thingiverse / GrabCAD import.
- **46 MCP tools** vs 7 for qcad — broader agent surface.

## freecad-mcp — gaps

- Heavy prerequisites (FreeCAD, Docker for OpenFOAM, optional FluidX3D build).
- PyInstaller/Tauri sidecar is large and slow to build.
- FluidX3D integration still evolving vs mature OpenFOAM path.

## CFD as fleet moat

```text
qcad-mcp (2D DXF floor plan)
    → freecad-mcp (3D domain + OpenFOAM case)
        → FluidX3D (GPU LBM on RTX 4090)
            → CSV / VTK velocity fields
                → godot-mcp / resonite-mcp (visualization)
                    → robotics-mcp (digital twin)
```

No commercial MCP competitor offers this **2D plan → 3D CFD → social VR / robotics** chain in one fleet.

## Competitive landscape (external)

| Product | CAD | Agent/MCP | CFD | Notes |
|---------|-----|-----------|-----|-------|
| Onshape API | Cloud CAD | REST only | No | SaaS, no local fleet |
| Fusion 360 API | Desktop CAD | Scripts | Basic sim | Closed ecosystem |
| FreeCAD + macros | Open | Manual | CfdOF addon | No MCP agent layer |
| **freecad-mcp** | Open | **FastMCP 3.2** | **OpenFOAM + FluidX3D** | Fleet-integrated |
| **qcad-mcp** | 2D open | **FastMCP 3.2** | No | DXF specialist |

## Recommendation

1. **Ship resonite-mcp Tauri** — operator UX for Agent Lab (done in-repo).
2. **Next deep repo: freecad-mcp** — double down on FluidX3D + fleet E2E (qcad DXF → freecad domain → sim → resonite marble world).
3. **Keep qcad-mcp** as the thin 2D front-end; avoid duplicating CFD there.
4. **Competitive analysis publish** — freecad CFD + agent NL config is the headline differentiator for GitHub/README.

## References

- [freecad-mcp README](file:///D:/Dev/repos/freecad-mcp/README.md)
- [qcad-mcp README](file:///D:/Dev/repos/qcad-mcp/README.md)
- [Digital twin pipeline](file:///D:/Dev/repos/mcp-central-docs/docs/robotics/DIGITAL_TWIN_PIPELINE.md)
- [tauri_nsis_building.md](file:///D:/Dev/repos/mcp-central-docs/standards/rules/tauri_nsis_building.md)
