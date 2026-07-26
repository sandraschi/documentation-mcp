# codecad-mcp — Parametric CAD Product Requirements

**Status:** Draft — pre-implementation
**Source:** FLEET_GAP_ANALYSIS_2026-07.md §4

## Vision

Turn the fleet's Python-native toolchain into a mechanical design engine. An LLM describes a part in natural language, `codecad-mcp` writes build123d code, executes it in a sandbox, and exports STEP files ready for manufacturing — no CAD GUI at any point in the pipeline.

## Target Users

1. **LLM agents (primary)** — generate, edit, and validate mechanical parts via MCP tools
2. **Hardware engineers** — use the dashboard to browse the part depot and export for fabrication
3. **kicad-mcp + blender-mcp** — cross-server handoff: enclosure → board outline → 3D visualization
4. **Future FEM/CFD servers** — geometry source for simulation

## Core Requirements

### 1. Part CRUD (cad_part)
- Create from Python source string using build123d
- Execute in isolated subprocess (jailed workdir, allowlist, timeout)
- Store BREP + source in depot (SQLite metadata, files on disk)
- Edit via new source → version chain; validate watertight + volume > 0
- Delete by part id

### 2. Export (cad_export)
- STEP — the primary manufacturing export, OCCT-native
- STL — with configurable linear/angular deflection
- 3MF — additive manufacturing with units/colors
- DXF — 2D profiles for kicad-mcp board outlines
- GLTF — 3D scene for blender-mcp / godot-mcp visualization
- Technical drawing — SVG orthographic projections (front/top/right + iso); dimensions optional, mark PARTIAL if >0.5d effort

### 3. Rendering (cad_render)
- Offscreen preview via OCP (preferred) or trimesh scene fallback
- Multi-angle render matching blender-mcp's contract for vision-refine loop transfer

### 4. Library (cad_library)
- `primitives_help` — curated build123d cheatsheet as markdown resource. LOAD-BEARING: LLMs write bad build123d without it
- `standard_parts` — parametric generators: hex bolt/nut (ISO 4017/4032), washers, bearings (608/6xx), T-slot profiles. 8-10 generators v0.1

### 5. Agentic Workflow (cad_agentic_workflow)
- Sampling loop: description → generate source → `cad_part.create` → validate → on failure, feed compiler/geometry error back → retry (max 3)

## Execution Safety (NON-NEGOTIABLE)

`cad_part.create` executes arbitrary Python:
- Dedicated subprocess with `-I` isolated mode
- No network access
- 60s hard timeout
- Workdir jailed to `parts/` depot
- Import allowlist: `build123d`, `math`, `numpy`
- v0.1 subprocess isolation sufficient; deepfang sandbox noted as hardening roadmap

## Non-Goals (v0.1)

- FEM/CFD mesh generation (needs a consumer server first)
- Multi-part assemblies (build123d does not have a mature assembly model)
- STEP import → parametric reconstruction (import is static, not editable)
- Dimension annotation on technical drawings (if >0.5d effort, file NotImplementedError)

## Acceptance Criteria

- Round-trip test: parametric bracket with 4 counterbored holes → validate watertight → export STEP → re-import → volume matches within 0.1%
- Agentic test: "40mm cube, 5mm filleted edges, 20mm through-hole" → valid part in ≤3 iterations
- 30+ pytest cases
- Playwright smoke test on webapp
- docs/BUILD123D_PATTERNS.md (LLM cheatsheet, written first)
