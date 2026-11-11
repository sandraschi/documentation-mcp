# Universal Crafters — The Physical Loop (bodies, not just bytes)

**Date:** 2026-11-07 · **Claim:** no software cloner integrates physical
dingusses yet. Verified: Craft Anything docs explicitly exclude hardware
(no JTAG/SWD/UART/SPI, no Saleae, no PCB/Gerber, no silicon); REA covers
firmware *images* and logic *recordings* but not bodies; fal.ai renders GLB
but never slices or prints.

## 1. The matrioska workflow that works TODAY (by hand)

Sandra's case: a photo of a matrioska doll → new-and-improved doll on a
makerspace printer, file carried on a micro-USB stick. Same path covers anime
figurines, toy robots, living-room knickknacks, a Meissen figurine (scan your
own shelf, not the museum's — clean-room rule applies to porcelain too).

```
1. PHOTO    phone photo(s), ideally 4-8 angles, matte light, ruler in frame
            (single front photo works, back is hallucinated — say so)
2. LIFT     Trellis-2 image-to-3D on fal.ai ($0.25 512p / $0.30 1024p /
            $0.35 1536p → GLB) or local TRELLIS / Hunyuan3D-2 / TripoSG
            output: GLB mesh + texture (NOT yet printable, NOT yet parametric)
3. SPLAT?   Gaussian splat (.ply / .splat) is for LOOKING (viewer, AR),
            not for PRINTING. Keep splats for preview (splatcraft), do NOT
            feed them to the slicer. Print needs a watertight mesh.
4. FIX      Blender / Meshmixer / SolidCraft: make manifold, close holes,
            thicken walls to >=0.8mm, flatten base, split matrioska halves
            with tolerance ring (0.2-0.3mm clearance), add drain hole
5. CAD      Optional but recommended for "improved": import GLB → SolidCraft /
            FreeCAD / CADCraft, re-sketch critical rings/faces so dimensions
            are parameters, not triangles. Triangles print; parameters improve.
6. SLICE    OrcaSlicer / Bambu Studio / PrusaSlicer → .3MF/.gcode,
            0.2mm layer, PLA, 15% gyroid, brim for small feet
7. SNEAKERNET  micro-USB stick → makerspace printer (their PC, your file)
            first print = fit check in cheap PLA, then final
```

End-to-end hand cost: ~$0.30 fal + ~1h cleanup + ~€2 filament. Heavy AI lives
in step 2 only; steps 4–6 are deterministic tools the cloners should call but
don't yet.

## 2. Why the cloners don't do bodies

| Blocker | Detail |
|---|---|
| No camera-to-mesh tool | Craft Anything studies *screens* (CDP, screenshots, DOM) and *binaries*, never turntables. REA studies *code*, never calipers. |
| Mesh != CAD | Trellis/Meshy/Tripo output triangle soup. Printers want manifolds; improvers want sketches/extrudes. No bridge tool in either repo. |
| Slicer gap | No `slice`, `repair`, `orient`, `support` verbs in any of the 320 + 350 tools. Fleet `makercraft` (C+) and `splatcraft` (B-) own adjacent verbs but aren't wired to a cloner. |
| Safety/liability | A bad website clone is a bug. A bad print is a blob, a burnt nozzle, or (Meissen thin walls) shards. Vendors avoid the queue at the makerspace. |
| Metrology missing | No scale, no tolerance, no fit-check in the Check step. Website checks compare pixels; body checks need calipers + test fits. |

## 3. Model notes (grounded)

- **Trellis-2 on fal (`fal-ai/trellis-2`):** native 3D generative, image→GLB,
  priced by resolution above. Playground returns
  `{"model_glb": {"url": "...glb"}}`. Good single-photo prior, weak on backs,
  hands, text. Use 1024p for figurines; 512p suffices for matrioska blobs.
- **Meshy T2/T2.5 on fal:** Smart Topology, triangle-only, natively separated
  parts, 4k–30k tris. BETTER for prints than Trellis when you want parts
  (arms, heads) pre-separated. Optional PBR + rigging.
- **Tripo (tripo3d/p1, v2.5, H3.1) on fal:** $0.01/credit — cheapest per-try,
  good for iteration before a final Trellis pass.
- **Hunyuan3D v2/v3, Trellis base:** self-hostable weights. Fleet RTX 4090
  (24GB, Goliath) runs them locally — zero per-asset cost after setup.
  Quality trails fal-hosted post-trains slightly; fine for toys.
- **MoGe-2/3 on fal (`microsoft/moge-2/3`):** monocular geometry → depth/normals
  → textured GLB/PLY point cloud. Use when Trellis over-smooths (Meissen lace,
  knickknack relief) — depth-first, then mesh.
- **FOSS local:** `microsoft/TRELLIS` (correct repo — NOT TRELLIS-2),
  `Tencent/Hunyuan3D-2`, `VAST-AI-Research/TripoSG`, `nerfstudio-project/nerfstudio`,
  `graphdeco-inria/gaussian-splatting` + `wjakob/mitsuba`-style repair,
  `alicevision/Meshroom` (COLMAP pipeline when you have 30+ photos),
  `Blender` (repair + base flattening, scriptable headless).

## 4. What "improved" means for a print (checklist the Check step should steal)

- [ ] Watertight (no naked edges), normals outward
- [ ] Base flat within 0.1mm, brim/raft decided
- [ ] Walls >=0.8mm (0.4 nozzle × 2), Meissen fingers thickened or cut
- [ ] Matrioska split: inner/outer clearance 0.25mm, vent hole >=3mm
- [ ] Overhangs >45° supported or redesigned
- [ ] Scale held: ruler photo → real mm (write it in `craft.json`)
- [ ] Test print in draft PLA before final PETG/ASA
- [ ] Photo of print vs render kept in `checks/` (close the loop)

## 5. Responsible-use note (porcelain-grade)

Scan what you own or are allowed to copy. A Meissen figurine on your shelf is
yours to scan; the museum's behind glass is not yours to sell. Same rule as
software clean-room: layout/style/behaviour yes, protected marks/textures no.
Makerspaces ask — keep the ownership note with the USB stick.
