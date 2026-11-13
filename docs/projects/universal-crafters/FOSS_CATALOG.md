# Universal Crafters — FOSS Catalog (self-hostable, BYOK-friendly)

**Date:** 2026-11-07 · **Rule:** every entry must be clonable + runnable without
a seat. Commercial entries appear only as the thing a FOSS entry replaces.

## A. Software cloners / oracles (the reversing half)

| Repo | License | Replaces | Run cost | Notes |
|---|---|---|---|---|
| `storytold/craft-anything` | MIT/Apache-2.0 | v0/Lovable for owned sites | Free + Claude sub | 320 tools, Study→Build→Check→Ready, Clean-room/Deep, BYOK Claude/Codex/Copilot/Grok, fal opt-in. `_upstream/craft-anything`. Alpha. |
| `morluto/rea` | MIT | IDA-lite + JS unpackers | Free + agent sub, Hopper opt. | ~350 MCP tools, evidence ledger, RL-env export. No build loop. `_upstream/rea`. 439k stars = audit surface, not hype. |
| `abi/screenshot-to-code` | Apache-2.0 (check fork) | v0 one-shots | VLM cents | Shot → Tailwind/HTML. No evidence, no check. Good first-stage for Craft Anything capture/. |
| `firecrawl/firecrawl` (+ `mendable/firecrawl`) | Apache-2.0 / AGPL halves | Manual CDP scraping | Self-host free, cloud pay | Markdown/JSON from any URL. Use as Deep-mode feeder when Clean-room screenshots aren't enough. |
| `openv0/openv0`, `v0-sdk`-likes, `same.new` (open core) | MIT variants | v0 lock-in | VLM cents | Prompt → Next.js + deploy-you-own. Pair with Craft Anything checks/ to close the loop makers leave open. |

## B. Photo → 3D (the bodies half — fal optional, local preferred)

| Repo / weight | License | fal twin | VRAM (local) | Notes |
|---|---|---|---|---|
| `microsoft/TRELLIS` (image/Text-to-3D; TRELLIS-2 paper = evolution) | MIT | `fal-ai/trellis-2` $0.25–0.35 | ~16GB+ | Best single-photo prior today. GLB out. Hallucinates backs — photograph them. |
| `Tencent/Hunyuan3D-2` (+ `Hunyuan3D-2mini`/Turbo) | MIT | `fal-ai/hunyuan-3d/*` $0.015–0.16 | 8–24GB by variant | Fast iteration; mini runs on smaller GPUs. Good for toys/knickknacks. |
| `VAST-AI-Research/TripoSG` (+ TripoSR tiny) | MIT | `tripo3d/*` $0.01/credit | 8–16GB | Cheapest loop. TripoSR single-view in seconds for fit previews. |
| `wjakob`/`instant-nsr`-family + `graphdeco-inria/gaussian-splatting` | Mixed BSD/MIT | — (view-only) | 8GB+ | Splats are PREVIEWS, not prints. Use for client approval, then mesh. Fleet `splatcraft` owns this. |
| `nerfstudio-project/nerfstudio` | Apache-2.0 | — | 12GB+ | Multi-photo (20+) altar: matrioska turntable → NeRF → mesh. Overkill for one shot, king for Meissen lace. |
| `alicevision/Meshroom` (COLMAP pipeline) | MPL-2.0 | — | CPU+CUDA opt | Photogrammetry when you HAVE angles. No hallucination: measures, doesn't dream. Pair with ruler. |
| `microsoft/MoGe` (metric geometry) | MIT | `microsoft/moge-2/3` on fal | Small | Depth/normals/point-cloud first; rescues relief detail Trellis smooths. |
| `Blender` (headless `bpy`) | GPL | — | CPU | Repair/retopo/base-flatten/split. Script it: `blender --background --python fix.py`. The unglamorous step that makes prints work. |

## C. Mesh → print (deterministic, no AI needed)

| Tool | License | Role |
|---|---|---|
| `OrcaSlicer` / `prusa3d/PrusaSlicer` / `bambulab/BambuStudio` | AGPL/GPL/Proprietary-mixed | Slice GLB/STEP→3MF/gcode. Orca = fleet default (Prusa lineage, Bambu profiles, calibration built in). |
| `Ultimaker/Cura` | LGPL-3.0 | Fallback slicer, huge profile library for exotic makerspace machines. |
| `FreeCAD` / `OpenSCAD` | LGPL/GPL | Parametric re-model of critical fits (matrioska ring, figurine base peg). SolidCraft (fleet) for Rust-native CAD when it matures. |
| `MeshLab` / `trimesh` (Python) | GPL/BSD | `trimesh` script = CI for bodies: `is_watertight`, `is_volume`, wall thickness probe. Run before every USB export. |

## D. What to install on Goliath first (order matters)

1. `craft-anything` (inspect + rebuild) + `rea` (deep inspect) side by side — different licenses, different engines, both MCP.
2. `TRELLIS` + `Hunyuan3D-2mini` local (4090 24GB holds both) — kill the $0.30/pop habit for drafts; pay fal only for finals.
3. `Blender` + `trimesh` + `OrcaSlicer` — the physical Check step Craft Anything lacks.
4. `firecrawl` self-host — Deep-mode feeder with receipts, not vibes.

Total seat cost: €0. Total marginal cost per matrioska draft: €0 + filament.
Final glamour pass: fal cents when the local mesh isn't pretty enough.
