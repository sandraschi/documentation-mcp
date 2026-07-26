# comfyops-mcp — Local Generative AI Engine PRD

**Status:** Draft — pre-implementation
**Source:** FLEET_GAP_ANALYSIS_2026-07.md §11

## Vision

Turn Goliath's RTX 4090 into the fleet's local generative engine. One server that wraps ComfyUI, manages model downloads, queues jobs against available VRAM, and auto-ingests results into Immich/Plex. New model families need a workflow file + checkpoint download — never a code change to the server.

## Architecture Decision

Wrap **ComfyUI** in API mode (`--listen`, `/prompt`, websocket progress). Do NOT reimplement diffusers pipelines by hand. ComfyUI is the ecosystem standard and first to support new model families.

## Core Requirements

### 1. ComfyUI Sidecar Management
- `start.ps1` launches ComfyUI with `--listen 127.0.0.1 --port <reserved>`
- Health-check `/system_stats` before accepting jobs
- Both ComfyUI port + MCP backend port + frontend port registered in WEBAPP_PORTS.md
- Serial job queue (one generation at a time on 24 GB shared with LM Studio/Ollama)
- `vram_guard` checks free VRAM before queueing; defers rather than failing

### 2. Generation (comfy_generate)
- image, video (t2v/i2v via Wan/LTX workflows), upscale, inpaint, edit
- Every call = SQLite-persisted job with websocket progress relay
- Seeds ALWAYS recorded; response includes full reproduction params
- Job queue supports status/cancel/list operations (Fleet job pattern)

### 3. Workflow Depot (comfy_workflows)
- LOAD-BEARING: agents parameterize curated graphs; they cannot author them
- v0.1 ships 8-10 curated workflow JSONs: flux-klein-t2i, qwen-t2i-text, zimage-fast, sdxl-lora-t2i, wan22-t2v, wan22-i2v, ltx-fast-t2v, esrgan-upscale, supir-restore, flux-inpaint
- Each workflow JSON has a sidecar `.md` documenting exposed parameters
- validate: workflow JSON can be submitted to ComfyUI without errors

### 4. Model Management (comfy_models)
- list_installed: scan the model directory, report what's available
- download: HuggingFace hub, hash-verified, as a background job
- vram_check: query `nvidia-smi` BEFORE queueing; refuse jobs that cannot fit with a clear message

### 5. Library & Ingest (comfy_library)
- recent + search over SQLite generation metadata (prompt, seed, model, workflow, timestamp)
- ingest_immich: push to Immich album "AI Art" via immich-mcp or direct API
- ingest_plex: videos → Plex library
- Auto-ingest on by default, per-generation opt-out

### 6. Agentic Workflow (comfy_agentic_workflow)
- SEP-1577 sampling: brief → workflow selection → generate → (optional) vision-check via local VLM → param-adjust retry (max 3)

## Model Roster

Verify current quant availability at build time.

| Model | Type | VRAM | License | Role |
|-------|------|------|---------|------|
| FLUX.2 [klein] 9B | Image | ~6 GB | Apache 2.0 | Daily driver |
| FLUX.2 [klein] 4B | Image | ~3 GB | Apache 2.0 | Fast draft |
| Qwen-Image-2.0 7B | Image | ~8 GB | Apache 2.0 | Text rendering |
| Z-Image Turbo 6B | Image | ~5 GB | Apache 2.0 | Speed |
| SDXL 1.0 | Image | ~5 GB | MIT | LoRA ecosystem |
| Wan 2.2 14B | Video | ~20 GB | Apache 2.0 | Quality |
| LTX-Video 5B | Video | ~8 GB | Apache 2.0 | Speed (~30s/clip) |
| ESRGAN | Upscale | ~1 GB | MIT | Archive restoration |
| SUPIR | Upscale/restore | ~8 GB | Apache 2.0 | Archive restoration |

FLUX.2 [dev] 32B: non-commercial license, quant-only on 24 GB (Q4 ~18 GB). Record exclusions in manifest.

Models manifest at `models_manifest.yaml` (outside repo, at `D:\models\comfyui\` or existing model dir): HF repo ids + hashes + license.

## Phase 2: LoRA Training

Wrap **ai-toolkit** (config-file driven subprocess):
- `train_lora`: dataset dir + base model + steps → .safetensors into LoRA dir
- `dataset_prep`: pull an Immich album → captioned dataset via local VLM
- `list_loras`: scan LoRA directory with metadata
- First mission: style LoRA from the 2024 SD favorites

### Phase 2b: Archive Restoration
`comfy_generate.upscale` batch mode over the 2024 SD archive: SUPIR or Real-ESRGAN → 4K → Immich album "SD 2024 Remastered" alongside originals. Deterministic, resumable (skip already-processed by hash).

## Non-Goals (v0.1)

- Audio generation (separate track on ai-producer-hub/Demucs)
- Real-time video streaming (generation is batch, not live)
- Multi-GPU distribution (single 4090 for v0.1)
- Training from scratch (LoRA fine-tuning only, Phase 2)

## Acceptance

- `comfy_generate.image` flux-klein returns real PNG, seed-reproducible
- Wan 2.2 i2v produces playable MP4, auto-ingested to Plex
- vram_check refuses job while 20 GB LLM loaded, with actionable message
- 40+ pytest cases
- Playwright smoke on webapp (Gallery, Generate, Workflows, Models, Jobs)
