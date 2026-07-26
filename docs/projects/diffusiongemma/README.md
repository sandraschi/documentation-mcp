# DiffusionGemma — Fleet Research Project

**Status:** Active assessment (June 2026)  
**Hardware target:** Goliath (RTX 4090, 24 GB VRAM, 64 GB RAM)  
**License:** Apache 2.0 (model weights)  
**Tags:** `#diffusiongemma` `#dllm` `#local-llm` `#goliath` `#inference` `#research`

---

## Acronym du jour: **dLLM**

The hype-cycle ticker moves on. Fleet nomenclature watch:

| Era (approx.) | Acronym | Expansion | What it meant |
|---------------|---------|-----------|---------------|
| 2024–2025 | **LWM** | Large World Model | World models, video/physics prediction, "understand environments" |
| 2025–2026 | **VLA** | Vision-Language-Action | Robotics brain — see, talk, act (π0, OpenVLA, Gemini Robotics) |
| 2026 → | **dLLM** | Diffusion Large Language Model | Text gen via discrete diffusion, not autoregression |

**dLLM** is the acronym du jour — DiffusionGemma made it stick in production tooling (vLLM, HuggingFace, llama.cpp PR). Same pattern as LWM and VLA before it: a real architectural shift gets a three-letter badge, conference talks multiply, LinkedIn posts achieve singularity density, and six months later everyone argues about the definition.

Fleet usage: **dLLM** for the paradigm, **DiffusionGemma** for Google's specific model, **AR LM** for the autoregressive incumbent. Do not confuse dLLM with DLM (diffusion language model — same thing, less trendy capitalization) or MDLM (masked diffusion LM — a sub-family).

Prior acronyms not dead — VLA still owns robotics-mcp integration discourse; LWM still shows up in worldlabs/video-gen contexts. dLLM just has the microphone right now.

**Fleet doctrine:** [catch them all](./FLEET_USAGE.md#fleet-doctrine-catch-them-all) — every paradigm gets an MCP slot, not just the du jour.

---

## What This Project Covers

Assessment archive for [DiffusionGemma](https://deepmind.google/models/gemma/diffusiongemma/) in **mcp-central-docs**.

**Fleet integration owner:** [`diffusion-llm-mcp`](https://github.com/sandraschi/diffusion-llm-mcp) — ports 10834/10835, doc-heavy repo, catch-them-all dLLM slot.

Not a production deployment yet; structured evaluation of whether and where dLLM fits on Goliath alongside AR models.

## Document Index

| Doc | Purpose |
|-----|---------|
| [**HLE_AND_CAIS.md**](./HLE_AND_CAIS.md) | Humanity's Last Exam — essentialism, goalpost moving, Scotsman, Butlerian stick (canonical) |
| [ASSESSMENT.md](./ASSESSMENT.md) | Model assessment, benchmarks honesty, analogy to early image diffusion (SD 1.x artifact era) |
| [RESEARCH.md](./RESEARCH.md) | Field timeline, arXiv / DeepMind papers, predecessor models (MDLM, LLaDA, Dream, MMaDA) |
| [FLEET_USAGE.md](./FLEET_USAGE.md) | Goliath fit, catch-them-all doctrine, `local-llm-mcp` routing, Ednaficator / batch MCP |
| [WINDOWS_SCAFFOLD.md](./WINDOWS_SCAFFOLD.md) | Windows build and run guide (llama.cpp diffusion branch, GGUF, Transformers fallback) |
| [PROGNOSIS.md](./PROGNOSIS.md) | Agent opinions, PRC/FOSS competitive dynamics, 12–18 month outlook |

## TL;DR

| Question | Answer |
|----------|--------|
| Runs on Goliath? | **Yes** — Q4_K_M GGUF, ~16–18 GB VRAM |
| Ready for Ollama/LM Studio? | **No** — needs llama.cpp PR branch or Transformers |
| Replace main chat model? | **Not yet** — quality gap on most benchmarks + no streaming |
| HLE (Humanity's Last Exam)? | **~12%, beats Gemma 4 AR no-tools** — anti-saturation frontier eval; slightly Yudkowsky-shaped surprise (see ASSESSMENT) |
| Good for batch/synthetic workloads? | **Yes** — 200–400 tok/s vs ~40–60 for 32B AR |
| Revolutionary? | **Architecturally significant, practically niche** — see PROGNOSIS |

## Key Links

- [DeepMind product page](https://deepmind.google/models/gemma/diffusiongemma/)
- [Google AI — Diffusion explained](https://ai.google.dev/gemma/docs/diffusiongemma/explained)
- [Model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)
- [HuggingFace weights](https://huggingface.co/google/diffusiongemma-26B-A4B-it)
- [Unsloth GGUF](https://huggingface.co/unsloth/diffusiongemma-26B-A4B-it-GGUF)
- [llama.cpp diffusion PR](https://github.com/ggml-org/llama.cpp/pull/24423) (use `llama-diffusion-cli`)

## Hardware Snapshot (Goliath, verified 2026-06-17)

| Spec | Value |
|------|-------|
| GPU | NVIDIA GeForce RTX 4090 |
| VRAM | 24,564 MiB |
| System RAM | ~64 GB |
| CUDA (driver) | 13.1 |
| Compute capability | 8.9 (Ada — use GGUF Q4, not NVFP4) |

---

*Last updated: 2026-06-17 · HLE_AND_CAIS.md added*
