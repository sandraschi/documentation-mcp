# Universal Crafters — Buildings and Machines (second bodies category)

**Date:** 2026-11-07 · **Companion to:** `PHYSICAL_LOOP.md` (small bodies:
matrioska, figurines, Meissen). This note covers the two bigger body classes
that also have NO integrated cloner yet: **buildings** (house + rooms +
floorplans → AutoCAD → BIM/Revit) and **machines** (visible gears, 16th-century
automata dolls).

Rule up front, same as porcelain: clone what you own or are allowed to measure.
Your house yes. A listed monument's interior for resale no. A museum automaton's
photos for study yes, its saleable replica only with permission.

## 1. Buildings: house → AutoCAD → BIM/Revit

### What you start with (and why it is enough)

- Many photos of house + every room (overlap 60-80%, doorways included).
- Whatever floorplans exist (scan, PDF, photo of paper — scale note wins).
- 5 tape/laser measures: one long wall per floor, one door width (standard
  800/900mm as check), one ceiling height per floor. Ruler-in-frame, but at
  building scale.

Photos alone give shape without scale. Floorplans alone give scale without the
as-built truth (walls moved in 1974, nobody redrew). Together they pin each other.

### Pipeline that works by hand today

```
1. CAPTURE   phone walk: exterior ring + room-by-room loops, slow pans for
             NeRF/splat; stills for photogrammetry. Floorplan scans beside.
2. SPARSE    COLMAP / Meshroom / OpenMVS → camera poses + sparse points.
             Output is truth-about-cameras, not yet a house.
3. DENSE     choice by goal:
             - pretty walkthrough → Gaussian splat / NeRF (nerfstudio) → viewer
             - measurable shell → dense MVS mesh (Meshroom/COLMAP+OpenMVS)
4. RECTIFY   floorplan → vector: wall centerlines in LibreCAD/QCAD/FreeCAD
             Draft, scaled to your laser measures (NOT to the scan's guess).
5. 2D CAD    export DXF/DWG (LibreDWG, ODA File Converter, BricsCAD compat):
             plans, sections, elevations. This IS the deliverable most
             makerspaces/carpenters accept. Stop here if that was the job.
6. BIM       BlenderBIM/Bonsai + IfcOpenShell: walls become IfcWall, doors/
             windows become IfcDoor/IfcWindow with types, rooms IfcSpace,
             storeys IfcBuildingStorey. Classify, don't just draw.
7. REVIT     import IFC/DWG into Revit (or ArchiCAD) for the office that
             demands `.rvt`. Round-trip is lossy — keep IFC as source of
             truth, Revit as export. Once fleet craft apps for BIM/Revit
             exist (cadcraft lineage), they target step 6 natively and
             step 7 via IFC, never via `.rvt` binary.
```

### Why no cloner does this

| Blocker | Detail |
|---|---|
| Scale ambiguity | Single-photo Trellis-style lifts hallucinate backs; houses need meters, not vibes. Only multi-view + tape closes scale. |
| Occlusion | Furniture hides walls, rooms hide structure. Software cloners assume the DOM is complete; houses never are. |
| Tolerance regime | Matrioska wants 0.25mm. Houses want 10-50mm + a wall-type table. Different Check step entirely. |
| Closed toolchain | AutoCAD DWG + Revit RVT are proprietary binaries. FOSS writes DXF/IFC reliably, reads DWG/RVT approximately. Any "up to Revit" promise must say: IFC in, RVT via Autodesk import. |
| Legal weight | A bad website clone is a bug. A bad load-bearing wall move is a collapse + monument-protection fine. Verifier must be stricter than for toys. |

### FOSS that covers each step (no seats)

- Poses/sparse: `colmap/colmap`, `alicevision/Meshroom`, `cvg/openMVS`.
- Pretty: `nerfstudio-project/nerfstudio`, `graphdeco-inria/gaussian-splatting`.
- 2D CAD: `LibreCAD/LibreCAD`, `FreeCAD/FreeCAD` Draft, `OpenSCAD` for parts.
- BIM: `IfcOpenShell/IfcOpenShell` + `Bonsai` (ex-BlenderBIM) — IFC4 authoring that Revit actually imports.
- Convert: ODA File Converter (freeware, not FOSS — quarantined to one export box), `LibreDWG` for DXF plumbing.
- Fleet hooks: `cadcraft` (CAD verbs), `qgiscraft` (geo/parcel context), `modcraft` (geometry), `makercraft` (print/mill outputs).

### Check step for houses (steal this when the craft apps land)

- [ ] Laser-vs-model on 3 control dims (≤1% or re-scale, never fudge)
- [ ] Every room closed polygon, named IfcSpace, area vs floorplan ≤2%
- [ ] Doors/windows scheduled (count + swing + width), not just holes
- [ ] Wall types listed (thickness + material), not single-line guesses
- [ ] IFC validates (`IfcOpenShell` validator, zero errors) before any Revit import
- [ ] Photos of as-built deviations kept in `checks/` beside the model

## 2. Machines: gears you can see → parts you can cut

Scope: **simple mechanical machines whose gears are visible** — hand crank,
clock, music box, automata doll linkage. If you cannot see it move, you cannot
clone it honestly. Closed gearbox + no drawings = measure-by-disassembly or stop.

### Pipeline

```
1. WATCH    video the mechanism through its full cycle (slow crank welcome),
            then stills of every gear face-on + edge-on, teeth counted twice.
2. COUNT    teeth Z, outer diameter D → module m = D/(Z+2) (spur gears);
            note pressure angle 20deg default, center distances, backlash feel.
3. SKETCH   FreeCAD Gear workbench / OpenSCAD involute gear / SolidCraft
            parametric gear: Z + m are PARAMETERS, everything follows.
4. ASSEMBLE shafts, cams, levers, barrel pins as separate bodies with joints;
            animate one revolution by hand before any print/mill.
5. OUTPUT   STL/3MF for prints, STEP/DXF for laser/mill, PDF drawing for the
            makerspace binder. First run in PLA/brass-look, then final stock.
```

### 16th-century automata dolls (the crown case)

- They ARE clonable in this regime: cam stacks, levers, bellows, pinned
  barrels are all visible once the back plate is off (with the owner's —
  or museum's — permission), slow, and made of re-makable brass/wood.
- Clone as TWO projects, never one blob: **movement** (mechanism, parametric,
  must run) + **doll** (shell/costume, Trellis-style lift like a matrioska).
  Shell people and movement people are different crafts; keep `app/movement/`
  and `app/shell/` apart.
- Ethics: many automata are unique cultural property. Study freely, publish
  mechanism notes, sell replicas only with rights. Same clean-room rule as
  code and porcelain.

## 3. What the fleet builds next (no new craft)

- `cadcraft`: `plan_vectorize` (floorplan scan → DXF centerlines + scale),
  `ifc_classify` (mesh/plan → IFC walls/doors/spaces via IfcOpenShell).
- `modcraft`/`makercraft`: `gear_measure` (Z + D → m + parametric gear),
  `assembly_check` (one-revolution sim + backlash report).
- Shared `checks/body.md` extended: mm table for toys, m table for houses,
  teeth table for gears — one ledger, three rulers.
- Revit stance: IFC-first, RVT-via-import, documented lossy. Never promise
  native `.rvt` writes from FOSS. The "up to Revit" in the request means
  exactly this until a licensed craft app exists.
