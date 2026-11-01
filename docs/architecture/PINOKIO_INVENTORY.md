# Pinokio Fleet Integration — Detailed Analysis

**Date:** 2026-07-14
**Status:** analysis + inventory, most recommendations not yet acted on
**Origin:** discovered mid-session while setting up comfyops-mcp's ComfyUI/model backend. Sandra pointed at Pinokio as a possible reuse source for Wan weights; the actual find turned out much larger than that one lookup, and warranted a proper writeup rather than a passing note.

---

## 0. What Pinokio actually is, for context

Pinokio (pinokio.co) is a one-click installer/launcher for AI apps - each "app" is a self-contained folder with its own Python environment, install/start scripts (`install.js`, `start.js`), and often its own downloaded model weights. It's been used on Goliath over roughly the past year to install 20 different generative-AI apps under `D:\pinokio\api\<name>.git\`, accumulating **~550GB** of environments and model weights, most of it sitting completely unused by the fleet until this session.

This matters architecturally for one reason: **every Pinokio app is already a working, demand-only, locally-installed AI backend** - which is exactly the shape of thing the fleet's own architecture has separately been trying to build piece by piece (comfyops-mcp for image/video, songgeneration-mcp's missing local backend, ittybitty's stubbed CogVideoX). A meaningful fraction of that already exists, dormant, in Pinokio.

---

## 1. `pinokio-mcp` — architecture and verified status

### 1.1 How it works

Two-layer design, both real:

- **HTTP client** (`client.py`) talks to `pinokiod`, the Express server the Pinokio Electron app is a thin shell around. Port auto-discovery scans 42000-42059 (Pinokio no longer shows its port in the title bar in recent versions), probing `/check` with a short timeout on each candidate. Home directory resolution checks (1) `PINOKIO_HOME` env var, (2) `%APPDATA%\Pinokio\config.json`'s `home` key on Windows, (3) falls back to `~/pinokio`.
- **Filesystem fallback** (`_list_apps_filesystem`): when the daemon isn't reachable, reads `<home>/api/*/pinokio.js` directly and regex-extracts `title`/`description` fields. This is the same thing I did manually before finding pinokio-mcp already existed - the tool already had this capability built in.

### 1.2 Verified working, 2026-07-14

The README's top badges claimed "PRODUCTION READY... confirmed working endpoints." Its own Contributing section (fixed by a concurrent edit mid-session, so no longer visible in the current README) claimed "this is a scaffold waiting for API discovery" - directly contradictory, and the kind of doc-vs-reality gap this whole session has been about catching rather than trusting labels. Resolved by checking the actual code and running it:

- `client.py` is a complete, real implementation - not a stub. Real retry logic with exponential backoff, real input validation, real filesystem fallback.
- Live test: `list_apps()` against the actual running daemon on Goliath returned all 20 real installed apps via the genuine API path (`source: "api"`, not `"filesystem"`) - confirmed pinokiod was reachable even though an earlier manual port/process scan in this same session had missed it (worth noting as a minor unresolved discrepancy - the manual `Get-NetTCPConnection`/`Get-CimInstance` checks found nothing running, yet the client's own probe succeeded; not chased down further, but the client's result is the one to trust since it's a direct functional test, not an indirect process enumeration).

### 1.3 What's NOT verified / real gaps

- **Stop-app reliability is explicitly best-effort**, per the code's own comment: `stop_app()` sends an HTTP `?stop=true` signal, but the docstring notes "Pinokio UI uses WebSocket rpc after page load" for full termination - meaning a script-driven stop might not fully kill a running app's process tree, mirroring exactly the kind of process-cleanup gotcha filed earlier this session (`TRAPS_AND_PITFALLS.md` #8, `taskkill /T /F`). Not tested end-to-end in this session.
- **LAN Wide Web (cross-device app orchestration) is lightly tested** per the README, not exercised in this session at all.
- **No model-level introspection.** `pinokio-mcp` operates at the *app* level (list/start/stop/delete/status) - it has no concept of "what model weights does this app actually have downloaded." The entire model-weight inventory in §2 below was done by hand, via direct filesystem size/extension scans, not through any pinokio-mcp tool. This is a real, concrete gap: a `pinokio_models` (or similar) tool op that walks each app's likely weight-storage locations and reports real file sizes/formats would have made this whole analysis a single tool call instead of ad hoc PowerShell. Flagged as a genuine feature gap, not a criticism of what exists - `pinokio-mcp` does what its name says (app management), model inventory is a different, uncovered surface.
- **`delete_app` was read in the code but never tested this session** - deliberately, since it's destructive and untested-destructive-tools don't get exercised casually.

### 1.4 Where it sits in the fleet's orchestration hierarchy

Per `ORCHESTRATION_HIERARCHY.md`'s three-layer model (hub / Fritz-as-client / domain nodes), `pinokio-mcp` is a Layer 3 domain node like any other - it should register with `mcp-federation-hub` as one node, not attempt to become a second orchestration layer. Its actual leverage isn't as a standalone tool though - it's as **the demand-only backend lifecycle primitive for every Pinokio-hosted app**, which connects directly to the deep-analysis doc's §3 chain-reliability contract (health-check / start / ready-probe / verify / idle-shutdown for demand-only backends). Concretely: if comfyops-mcp, songgeneration-mcp, or any future fleet server ever wants to delegate "wake up Hunyuan3D" or "start SongGeneration-Studio" to something, `pinokio-mcp`'s `app_management(action="start", ...)` is already the right primitive - no consuming server needs to reimplement Pinokio's own launch mechanics. This wasn't designed as a mediating layer originally, but it's structurally already positioned as one for anything running under Pinokio specifically.

---

## 2. The 20 apps, organized by fleet domain (not just size)

### 2.1 Directly relevant to today's open threads

| App | Size | What it is | Connects to |
|---|---|---|---|
| `ml-sharp-pinokio.git` | 7.7GB | One-click single-image-to-3D-Gaussian-splat | **splatmaker-mcp** - a fundamentally different approach from the decided Nerfstudio/Splatfacto engine (which needs multi-view video/images for photogrammetry). Could let `from_prompt` skip stages 5-6 (video generation + photogrammetry) entirely for single-hero-image cases. Not evaluated yet, cross-referenced into `docs/FROM_PROMPT_DESIGN.md`. |
| `lingbot-world-pinokio.git` | 183.4GB | Purpose-built world model, image-to-video, 4-bit quant, ~20GB VRAM | **splatmaker-mcp `from_prompt` stage 5.** "World model" training targets spatial/physical consistency explicitly - exactly the unverified property every other stage-5 candidate (Wan 2.7, Veo 3, comfyops's Wan 2.2) has been flagged as uncertain on. Untested, but the single most promising unexamined candidate given the actual problem being solved. |
| `wan.git` | 30.2GB | Wan 2.1, video generation | **Already reused** - copied into comfyops-mcp's ComfyUI install this session, confirmed real (GPU-detected, native ComfyUI Wan nodes present, file sizes match exactly post-copy). This is the one item in this table that's moved from "found" to "actually integrated." |
| `Hunyuan3D-2-lowvram.git` | 75.0GB | Image-to-3D-mesh | Possibly the same "Hunyuan" already referenced as a blender-mcp AI-mesh-generation backend option in the settee-chain worked example (`FLEET_DEEP_ANALYSIS_2026-07-13.md` §2.2.1). **Not confirmed** whether blender-mcp actually routes to this Pinokio install or a separate resource - worth checking blender-mcp's actual config rather than assuming either way. |

### 2.2 Audio / music generation - a real cluster nobody's connected

| App | Size | What it is |
|---|---|---|
| `SongGeneration-Studio.git` | 40.1GB | Full song generation - lyrics, vocals, instrumental, style control |
| `yue.git` | 22.8GB | YuE, open full-song generation foundation model |
| `diffrhythm.git` | 18.4GB | Song generation up to 4m45s, lyrics or instrumental |

Three separate, real, substantial local song-generation backends (~81GB combined) sitting completely unused. The deep-analysis doc already flagged `songgeneration-mcp` as existing but "isn't in FLEET_INDEX's visible chain language anywhere" - this is very likely why: the actual local backend it should be routing generation through has never been identified or wired. Worth a real evaluation pass (which of the three is best, or whether songgeneration-mcp should support all three as pluggable backends) rather than three isolated Pinokio apps with zero fleet connection.

### 2.3 TTS - a real alternative to a known stub

| App | Size | What it is |
|---|---|---|
| `zonos.git` | 5.9GB | Zonos-v0.1, open-weight TTS, 200k+ hours multilingual training data |
| `Orpheus-TTS-FastAPI.git` | 0GB | Orpheus TTS on Llama-3B - **registered but never actually downloaded**, completely empty |

Zonos is real, substantial, and directly addresses ittybitty's already-documented gap: its `VIDEOGEN_TTS_PROVIDER` config lists `edge-tts`/`cosyvoice`, and CosyVoice is flagged in ittybitty's own Known Gaps table as "HTTP stubs, no fleet proof against live servers." Same "proven local weights beat unproven stub" logic already applied to the Wan-vs-CogVideoX proposal for ittybitty's video path applies here for its audio path. Orpheus is worth noting specifically as a *negative* finding - an app that got registered with Pinokio but where the actual download step was apparently never completed, useful as a reminder that "app is listed" doesn't mean "app has weights," same lesson as `flux-2-klein-pinokio.git` below.

### 2.4 Image generation / editing - comfyops-mcp adjacent

| App | Size | What it is |
|---|---|---|
| `MagicQuill.git` | 18.7GB | Interactive image editing - erase/add objects via a friendly UI |
| `StyleAligned.pinokio.git` | 12.0GB | Style-aligned image generation via shared attention |
| `clarity-refiners-ui.git` | 8.2GB | Image upscaling/enhancement (finegrain-image-enhancer port) |
| `flux-2-klein-pinokio.git` | 6.1GB | FLUX.2 klein - **environment only, checked directly, zero model weights** (every file over 100MB is a torch/CUDA library, nothing resembling a checkpoint) |
| `facefusion-pinokio.git` | 6.8GB | Face manipulation platform |

comfyops-mcp's roster already lists FLUX.2 klein as its "daily driver" and ESRGAN/SUPIR for upscaling - worth comparing clarity-refiners against the SUPIR plan rather than assuming SUPIR is automatically better. MagicQuill and StyleAligned are candidate ComfyUI-adjacent workflows/inspirations, not directly pluggable (they're standalone Gradio apps, not ComfyUI custom nodes) but worth knowing about. FaceFusion has no current fleet mapping - flagged for awareness, no obvious integration point today.

### 2.5 Miscellaneous / not yet mapped to a fleet need

| App | Size | What it is |
|---|---|---|
| `Frame-Pack.git` | 45.2GB | Progressive next-frame-section video generation |
| `cube.git` | 14.6GB | Roblox's 3D foundation model |
| `MMAudio.git` | 10.3GB | Synchronized audio generation from video/text input |
| `comfy.git` | 5.5GB | Pinokio's own ComfyUI wrapper - superseded by the direct `D:\ComfyUI` install done this session for comfyops-mcp, not currently in use |
| `deeperhermes.git` | 0.04GB | LLM variant - essentially unused/failed install |

MMAudio is worth a second look later - synchronized audio-from-video is directly relevant to anything in the artistic/video chain that produces silent clips and wants a soundtrack (ittybitty, comfyops-mcp video outputs). Frame-Pack and Cube are novel capabilities without an obvious current fleet slot - noted for awareness rather than action.

---

## 3. This is a case study in the fleet's own "recombinant capability" pattern

Worth naming explicitly: this whole discovery is an instance of the pattern already documented in `mcd projects/POL_AND_RECOMBINANT_CAPABILITIES.md` - a novel capability emerging from re-reading infrastructure that already exists (a year of Pinokio installs made for unrelated, one-off reasons) through a new lens (the fleet's current needs), rather than building anything new. The PoL doc's own §0 ingredient list maps cleanly:

- **Existing sensors/signals** → a year of Pinokio app installs, made incrementally, never inventoried
- **A small interpretive layer** → the size/extension scan + cross-referencing against known fleet gaps, not a new ML model
- **An agent with standing access** → this session, prompted by Sandra remembering Pinokio existed
- **A delivery channel that already exists** → `pinokio-mcp`, already built, just unverified until today

Worth adding as a new entry in that doc's §2 ("other things already in flight that fit the pattern") rather than treating it as a one-off.

---

## 3.5 Impact ranking, all 19 non-Wan apps (2026-07-14)

Weighing: real weights present, how clearly it fills an already-identified fleet gap, effort to wire in, and whether it's genuinely unique vs. redundant with something else on this list or already planned.

**High impact:**
1. `ml-sharp-pinokio.git` (7.7GB) - best impact-per-GB here. Tiny, directly relevant to splatmaker-mcp, could skip the whole video-gen-then-photogrammetry chain for single-image cases.
2. `lingbot-world-pinokio.git` (183GB) - highest ceiling, directly targets `from_prompt`'s core unsolved multi-view-consistency problem. Also highest risk: huge footprint, ~20GB VRAM, zero evaluation done.
3. `SongGeneration-Studio.git` (40GB) - fills a real, already-identified gap (songgeneration-mcp exists with nothing behind it).
4. `zonos.git` (5.9GB) - tiny, fills ittybitty's stubbed CosyVoice gap directly, 200k+ hours training data.

**Medium impact:**
5. `Hunyuan3D-2-lowvram.git` (75GB) - potentially already blender-mcp's "Hunyuan" backend (unconfirmed - check before assuming either way, five-minute task).
6. `hunyuanvideo.git` (41GB) - real alternative, same territory as Wan/lingbot-world, value not yet established vs. either.
7. `MMAudio.git` (10GB) - fills a distinct gap nothing else here covers: soundtrack generation for silent AI video output.
8. `cube.git` (14.6GB) - novel, no established consumer, plausibly relevant to the VR/3D-asset chain (robofang, worldlabs-mcp) but unconfirmed.

**Low impact / redundant with something already covered:**
9. `yue.git` / `diffrhythm.git` (23GB / 18GB) - same gap as SongGeneration-Studio, comparison options only.
10. `clarity-refiners-ui.git` (8GB) - comfyops-mcp roster already plans ESRGAN/SUPIR for this.
11. `MagicQuill.git` (18.7GB) - no clear fleet-server consumer identified.
12. `StyleAligned.pinokio.git` (12GB) - niche technique, no fleet consumer.
13. `Frame-Pack.git` (45GB) - same territory as Wan/lingbot-world/hunyuanvideo, no unique angle found.
14. `facefusion-pinokio.git` (6.8GB) - no identified fleet use case, awareness only.

**Not usable as-is:**
15. `comfy.git` - superseded, real ComfyUI already installed directly this session.
16. `flux-2-klein-pinokio.git` - environment only, zero model weights despite the name.
17. `deeperhermes.git` - essentially empty (0.04GB).
18. `Orpheus-TTS-FastAPI.git` - completely empty, never actually downloaded.

## 4. Recommendations, ranked

1. **Evaluate `ml-sharp` for splatmaker-mcp's `from_prompt`** - single-image-to-splat, potentially skips the whole video-gen-then-photogrammetry chain for some cases. Cross-referenced into `docs/FROM_PROMPT_DESIGN.md`.
2. **Evaluate `lingbot-world` for `from_prompt` stage 5** - purpose-built world model, may solve the multi-view-consistency problem better than general video diffusion. Test before finalizing the Wan-2.7-vs-Veo-3 comparison.
3. **Confirm whether `Hunyuan3D-2-lowvram` is blender-mcp's actual "Hunyuan" backend** or a second untapped resource - check blender-mcp's config/source directly.
4. **Wire `SongGeneration-Studio`/`YuE`/`DiffRhythm` into songgeneration-mcp** - real local backends exist for a server that's currently disconnected from any actual generation capability.
5. **Wire `Zonos` as an alternative to ittybitty's stubbed CosyVoice** - same reasoning already applied to Wan-for-CogVideoX.
6. **File a `pinokio_models` tool-op gap** against pinokio-mcp itself - app-level management exists and works, model-level introspection doesn't, and this analysis had to be done by hand because of it.
7. **Add this discovery as a case study to `POL_AND_RECOMBINANT_CAPABILITIES.md`** - it's a clean instance of the fleet's own named pattern.
