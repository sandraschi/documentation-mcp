# codecad-mcp — Parametric CAD via build123d

**Status:** Build brief ready — repo NOT yet created
**Priority:** P2 (parallel with comfyops-mcp)

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\codecad-mcp` (not yet scaffolded) |
| **Brief source** | `architecture/FLEET_GAP_ANALYSIS_2026-07.md` §4 |
| **Stack** | build123d (+ OCP/OCCT ~250 MB), trimesh |
| **Depends on** | mathops-mcp (soft — for dimension checking in `cad_agentic_workflow`) |
| **Consumed by** | kicad-mcp (board outline via DXF), blender-mcp (visualization via GLTF), future FEM/CFD |

## What is Code-CAD?

Parametric 3D modeling done by writing Python code via the `build123d` library (the modern successor to CadQuery). Parts are Python source — an LLM can generate, edit, diff, and version-control mechanical parts the same way it does software. No GUI, no mouse clicks, no brittle GUI automation.

## Tools (5 portmanteau)

| Tool | Ops | Notes |
|------|-----|-------|
| `cad_part` | create, edit, validate, list, get_source, delete | Python source → restricted subprocess exec → BREP |
| `cad_export` | step, stl, 3mf, dxf, gltf, technical_drawing | STEP is the primary reason this server exists |
| `cad_render` | preview_png, multi_angle | Offscreen OCP or trimesh fallback |
| `cad_library` | primitives_help, standard_parts | Load-bearing cheatsheet + parametric bolt/washer/bearing generators |
| `cad_agentic_workflow` | description → generate → validate → retry (max 3) | Highest-value single tool |

## Execution Safety

`cad_part.create` runs in a **dedicated subprocess** (not in-process eval), no network, jailed workdir, import allowlist (`build123d`, `math`, `numpy`), 60s timeout. Deepfang hardening noted as roadmap.

## Acceptance

- Round-trip: parametric bracket with 4 counterbored holes → STEP → re-import → volume within 0.1%
- Agentic: "40mm cube, 5mm filleted edges, 20mm through-hole" → valid part in ≤3 iterations
- docs/BUILD123D_PATTERNS.md as the LLM cheatsheet
