# Changelog

## 0.1.2 (2026-08-17)

- **MiniMax H3 video (native ComfyUI >= 0.33)**: new curated workflows `minimax-h3-t2v`
  and `minimax-h3-i2v` via the core `MiniMaxH3ImageToVideo` node - omni-modal t2v/i2v
  with native stereo audio (voice, SFX, music) in a single pass, 8-step turbo LoRA path
  (ComfySwitchNode default on), 768p short edge canvas, 24fps
- **generate**: `_apply_params` now injects prompt/width/height into
  `MiniMaxH3ImageToVideo`; VRAM guard estimates 16 GB for both H3 workflows
- **models manifest**: download candidates for the official Comfy-Org/MiniMax-H3 set
  (pruned int8_convrot diffusion, nvfp4 Qwen3-VL-32B encoder, video + audio VAEs,
  turbo 8-step LoRA)

## 0.1.1 (2026-08-15)

- **comfy_models download**: HF Hub streaming download with optional sha256 verification,
  subdir allowlist, dest_name rename, Bearer auth (COMFYOPS_HF_TOKEN) for gated repos
- **config**: load repo-root .env (MODELS_DIR now resolves to D:\ComfyUI\models - the
  models page showed "no models found" because the default dir did not exist)
- **ComfyUI**: updated 0.27 -> 0.33 (git pull + torch 2.11 cu128); sidecar now runs
  with ComfyUI's own venv python and start.ps1 actually launches it
- **Gallery**: sorting (6 modes), filters (workflow/model/search/date), batch ops
  (select, export CSV/JSON, delete), crossconnects (related panel), pagination -
  new REST: GET /api/gallery, POST /api/gallery/delete, GET /api/gallery/export,
  GET /api/gallery/{id}/related
- **Acceptance verified**: FLUX.2 klein text-to-image (seed-reproducible PNG,
  official wiring: CLIPLoader qwen_3_4b type=flux2 + CLIPTextEncode, fp8 compute)
- **Manager hardening**: history-poll retry (slow ComfyUI no longer kills tools),
  free_vram() after each generation (stale VRAM guard fixed), workflow validation
  before VRAM check
- **Pruned**: 16.8GB mistral text encoder + unverified flux2-t2i (9B dev) workflow
- 27 curated workflows, 86 pytest cases

## 0.1.0 (2026-07-12)

- Initial release
- comfy_generate: image, video, upscale, inpaint, edit
- comfy_workflows: list, get, validate, register
- comfy_models: list_installed, check_vram, health
- comfy_library: recent, search, record
- comfy_agentic_assist: SEP-1577 sampling
- Prefab UI cards (show_comfyops_status_card, show_generation_card)
- Vite + React + Tailwind webapp (Dashboard, Generate, Gallery, Workflows, Models)
- 6 curated workflow JSONs
- 12 pytest cases
