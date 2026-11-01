# 03 - Fleet Inventory: What We Already Have (7:7 Map)

Measured 2026-10-08 from D:/Dev/repos + mcp-central-docs/projects. We do not have
an ArtCraft. We have the bricks for one. Strategy is bridge + mesh, not rewrite.

## 7:7 map

| Adobe | ArtCraft Craft | Fleet holder | Strength | Gap to close |
|---|---|---|---|---|
| Photoshop | PhotoCraft (early alpha) | gimp-mcp (18 tools, ~1000 PDB proxy, G'MIC 500+, GEGL, live bridge :10824 + headless gimp-console) | Real editing, batch, color mgmt, snapshot vision loop | PSD vector load, feather/density parity, HEIC, copy/paste polish |
| Illustrator | VectorCraft | inkscape-mcp + qcad-mcp + codecad-mcp + freecad-mcp | SVG paths, CAD exchange (dxf-svg), step import | Appearance panel parity, live glow/character panels, font-list robustness |
| Premiere | FilmCraft (no web) | davinci-resolve-mcp (9 portmanteau tools, Resolve Python API, 10842/10843) + videogen-mcp/ittybitty (topic-to-video, stock + Jellyfin/Plex + Wan LocalGen + Veo, NSIS app, 11054/11055) + obs-mcp + handbrake-mcp + demo-vid-mcp + directmedia-mcp | Edit + color + Fairlight + render + stock/shorts/chapters + stream | Unified timeline object shared across davinci + ittybitty, AEP import, motion-blur codec parity |
| Lightroom | LightCraft | immich-mcp (photo library) + comfyops library/depot | Library catalog, gallery, history | RAW develop sliders, non-destructive stack,alsolight/effects parity |
| After Effects | EffectCraft | vfx-mcp + blender-mcp VSE/compositor/geonodes + tahoma2d-mcp | Text/shape/solid layers, VSE, render, 48+ blender tools | Comp model shared with FilmCraft timeline, .ecproj stability |
| InDesign | DesignCraft | libreoffice-mcp + pdf-mcp | Text frames, threading concept, export | 3-column thread line, pull-quote wrap, Properties text-frame options |
| Acrobat | PdfCraft (early alpha) | pdf-mcp | Read/combine/split basics | Organize + secure + threaded comments + All-tools panel |

## Engine layer (our edge vs his hosted tokens)

- comfyops-mcp: local gen engine. Prompt-to-image verified (FLUX.2 klein 4B fp8, SD1.5 seed-reproducible), video/upscale/inpaint curated (Wan 2.1/2.2, Hunyuan, LTX, Mochi, ESRGAN, SUPIR). 27 workflows, VRAM guard, SQLite library, MCP sampling assist. MIT. Pair with civitai-mcp (search/download into models tree) + huggingface-mcp + invokeai-mcp.
- songgeneration-mcp + suno-mcp + audiotool-nexus-mcp + reaper-mcp + stems-mcp + mixx-dj-mcp + virtualdj-mcp: sound/music/dialogue side his 5 sound models cover thinly.
- worldlabs-mcp + splatmaker-mcp + godot-mcp + unity3d-mcp + vroidstudio-mcp + vrchat-mcp + myvrworlds: 3D/worlds/splats/avatars beyond his Marble/TripoSplat.
- blender-mcp: 48+ tools, headless --background default + live bridge addon optional, GLB/VRM/VRChat/Unity export, Rodin/Tripo/Hunyuan hooks, Tauri installer ~15 MB via just build-native. This IS our 3D stage.
- avatar-mcp + avatar-pipeline-mcp: identity/character persistence primitive his Identity Transfer needs.

## What is missing for a mini-ArtCraft loop

1. Shared scene/shot objects. Today: 4 SQLite DBs, 4 naming schemes. Need: `location.json` (room/world), `character.json` (identity + pose), `shot.json` (camera + layers), passed blender -> gimp -> videogen -> comfy.
2. Unified model router (see 02). comfyops needs catalog table + flags.
3. Uniform agent ops naming: `snapshot` (base64 PNG), `mission` (goal + retries + report), `library recent/search/record` on every media repo.
4. Desktop regression docs + free-port launcher pilot (see 02).
5. Crossconnect declarations per FLEET_CROSSCONNECT_STANDARD + CROSSCONNECT_PATTERN: check overlap first, 1-hop rule, soft degradation, no transitive chains. blender-mcp already lists qcad/freecad/resonite/speech companions correctly.

## Recommended mesh (phase 1, no new repo)

- blender-mcp (stage/pose/render) <-> gimp-mcp (2D composite/inpaint/color) <-> comfyops-mcp (gen/upscale) <-> videogen-mcp (assemble/depot/publish) with davinci-resolve-mcp as pro finish option.
- Contracts: hands-in (prompts, .blend, refs, mesh URLs, bpy scripts) / hands-out (GLB/FBX/OBJ/USD, VRM, .blend, PNG/MP4, splats) already documented in blender-mcp README. Extend same table to other three.
- Telemetry: SQLite per action (pywinauto pattern) + Prometheus/Loki where present (gimp/davinci). Query failure patterns by tool before adding features.

## Competitive note

He rewrites (Rust native). We wrap (bridge to Blender/GIMP/Resolve/Comfy). Rewrite wins independence, wrap wins tomorrow usability + MIT freedom + local GPU. Do not abandon wrap to chase rewrite. Add thin Rust only where hot, keep Python MCP as agent contract.
