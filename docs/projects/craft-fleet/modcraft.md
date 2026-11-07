# ModCraft — Assessment

**Repo:** `D:\Dev\repos\modcraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first parametric 3D solid modeling, CSG, and automated BOM synthesis —
native on Goliath, zero cloud. Port `14120`. Consolidates `freecad-mcp`,
`qcad-mcp`, `kicad-mcp`, `codecad-mcp`, `chip-design-mcp`.

## Model / verbs

- **Model:** solid/parametric part + assembly + BOM line (component inventory link).
- **Crates:** `modcraft-geometry`, `modcraft-core`, `modcraft-mcp`, `modcraft-app`.
- Geometry/core split is the strongest crate seam in the new generation.

## Architecture

Rust ArtCraft 3-tier, MIT/Apache. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-04 (fleet i18n).

## Strengths

- Biggest consolidation win available: 5 CAD MCPs into one studio.
- Geometry crate isolates the kernel math from plumbing — correct layering.
- BOM-to-inventory link (job_parts) is the cross-craft multiplier done right.

## Gaps / risks

- CAD kernels are decade-scale work; CSG-from-scratch vs wrapping a kernel
  (OpenCASCADE via bindings, or headless FreeCAD) is THE decision — unmade at triage.
- Overlap with SolidCraft (already parametric, already shipped) and the rebuild
  PLAN's `meshcraft` pick-one-host advice (FreeCAD vs Blender timebox). Modcraft
  must state its relation to SolidCraft in writing or it duplicates it.
- QCAD (2D drafting) + KiCad (PCB) + solid modeling in one repo is three products;
  sequence them (solids → BOM first, PCB later).
- No `docs/`, no geometry tests (cube union → expected volume is the hello-world proof).

## Next 3 steps

1. Kernel decision doc: build vs wrap, with SolidCraft relationship paragraph.
2. CSG hello-world tests (primitive volumes, boolean union on fixtures).
3. `docs/PRD.md` + one democraft recipe: `mod/primitive-bom` (part → BOM artifact).

## Verdict

Best crate seam, hardest build-vs-wrap decision in the fleet. C+ until the kernel
decision is written and primitive-volume tests go green.
