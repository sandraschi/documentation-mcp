---
title: "Unsloth: Local LLM Fine-Tuning & RL"
category: integration
status: active
audience: mcp-dev
skill_candidate: true
related:
  - integrations/local-llm/README.md
  - standards/LOCAL_LLM_STANDARDS.md
  - standards/SOTA_REQUIREMENTS.md
  - integrations/unsloth/TECHNICAL.md
  - integrations/unsloth/WORKFLOWS.md
last_updated: 2026-08-05
---

# Unsloth — Local LLM Fine-Tuning & Reinforcement Learning

**Upstream:** [github.com/unslothai/unsloth](https://github.com/unslothai/unsloth) · **Docs:** [unsloth.ai/docs](https://unsloth.ai/docs) · **License:** Apache-2.0 (core) / AGPL-3.0 (Studio UI)
**Assessment date:** 2026-08-05 · **Machine verified:** Goliath (RTX 4090, 24 GB)

---

## 1. Verdict (TL;DR)

| Question | Answer |
|----------|--------|
| **Can we install it locally?** | **YES.** Native Windows support since mid-2025 — **no WSL required** for either Unsloth Studio (web UI) or Unsloth Core (Python library). Goliath's RTX 4090 / driver 620.02 / Python 3.13.5 / uv are all within official requirements. |
| **Should we?** | **YES, as a complement — not a replacement.** Unsloth gives the fleet a **local fine-tuning / RL track** (data stays on the machine) alongside the existing **cloud track** (Azure Foundry finetuning skill: SFT/DPO/RFT). It does **not** replace Ollama / local-llm-mcp for day-to-day inference. |
| **Recommended entry path** | Unsloth Studio via `irm https://unsloth.ai/install.ps1 \| iex` (~15 min), then validate with a small QLoRA run, then decide whether to wire the **MCP control endpoint** into the fleet. |

---

## 2. What Unsloth Is

A third-party open-source library + web UI that accelerates **LLM fine-tuning, RL, and inference** on consumer GPUs:

- **~2x faster training, ~70% less VRAM** vs vanilla HuggingFace TRL, **MoE up to 12x faster** (DeepSeek, GLM, Qwen, gpt-oss), **RL (GRPO) with ~80% less VRAM**
- **Own Triton/mathematical kernels** built on PyTorch + HF Transformers — this is the core differentiator; also patches upstream bugs (works directly with Llama, Qwen3, Gemma, gpt-oss, Mistral teams)
- **Dynamic quantization** (4-bit/8-bit/16-bit/FP8) — no separate bitsandbytes dependency for the common paths
- **GGUF support via llama.cpp** — run, export, and serve quantized models; dynamic GGUF quants with long-context fixes
- Two distribution tracks:
  - **Unsloth Studio (Beta)** — web UI: model search/download, data recipes (PDF/CSV/DOCX → dataset), training, RL, chat, code execution, model arena, GGUF export, OpenAI/Anthropic-compatible API, optional **MCP control endpoint**
  - **Unsloth Core** — the original Python library (`pip`/`uv`): `FastLanguageModel` + `SFTTrainer`/`GRPOTrainer` notebooks and scripts

---

## 3. Verified Machine Readiness (Goliath, 2026-08-05)

| Requirement | Official floor | Goliath | OK? |
|-------------|---------------|---------|-----|
| OS | Windows 10/11 64-bit | Windows (win32) | ✅ |
| GPU | NVIDIA RTX 30/40/50 (CUDA cap ≥ 7.0) | RTX 4090 24 GB | ✅ |
| Driver | Latest NVIDIA driver | **620.02** (CUDA 13.0 capable) | ✅ |
| Python | 3.11–3.13 | **3.13.5** (`py` launcher) | ✅ |
| uv | any recent | **0.9.4** (old; `uv self update` recommended) | ✅ |
| Git | any | `C:\Program Files\Git\cmd\git.exe` | ✅ |
| winget / nvcc | Studio installer pulls own; Core does not need | not on PATH — **not required** | ✅ |

**Notes**
- `nvcc` is **not** needed for either track — PyTorch wheels bundle the CUDA runtime. Studio's setup script installs CUDA Toolkit matched to the driver if required.
- Python is not on `PATH` (only `py`), which is fine — both install methods create their own venv via uv.

---

## 4. Install Options (Windows)

### A. Unsloth Studio — web UI (recommended to start)

```powershell
irm https://unsloth.ai/install.ps1 | iex
```

- Same command updates the install later.
- Launches with: `unsloth studio -p 8888` (default port 8888; `-H 0.0.0.0` for LAN).
- First run compiles llama.cpp binaries (5–10 min).
- Re-running the installer is idempotent and swaps the llama.cpp backend (CPU / Vulkan via `UNSLOTH_FORCE_VULKAN=1`).

### B. Unsloth Core — Python library

```powershell
uv venv unsloth_env --python 3.13
.\unsloth_env\Scripts\activate
uv pip install unsloth --torch-backend=auto
```

`--torch-backend=auto` resolves the correct torch/triton build (avoids the classic Windows triton/bitsandbytes DLL failures). Plain `pip install unsloth` on Windows works **only** if PyTorch is already installed.

### C. Docker (zero-setup alternative)

`unsloth/unsloth` image on Docker Hub — same image for Blackwell/RTX 50. Jupyter Lab on 8888.

### D. WSL2 (legacy path)

Still supported; only needed if you specifically want **vLLM** (vLLM is not available on native Windows — WSL/Linux only).

---

## 5. Feature Matrix

### Inference
| Feature | Notes |
|---------|-------|
| Model search + download | GGUF, LoRA adapters, safetensors |
| GGUF hardware controls | GPU/layer placement, MoE expert offload, multi-GPU, tensor parallelism |
| Chat | images, audio, PDFs, code, DOCX; auto parameter tuning |
| Tool calling | self-healing tool calling, web search |
| Code execution | sandbox/artifacts testing |
| API endpoints | OpenAI-compatible `/v1/chat/completions` + `/v1/responses`, Anthropic `/v1/messages` |
| Agent bridging | `unsloth start claude \| codex \| hermes \| openclaw \| opencode` (incl. `--as-subagent`) |
| MCP | chat-side MCP client support **and** an opt-in **MCP control endpoint** for AI clients |
| Model arena | side-by-side model comparison |
| Export | GGUF, 16-bit safetensors, others |

### Training / RL
| Feature | Notes |
|---------|-------|
| Methods | LoRA / QLoRA, full fine-tune, 4-bit / 8-bit / 16-bit / FP8, RL (GRPO, FP8 RL, vision RL) |
| Context | long-context packing: 3x faster, 30% less VRAM, 500K+ context on 80 GB |
| Modalities | text, **vision**, **audio/TTS (Orpheus)**, **embeddings** |
| Data recipes | auto-dataset from PDF/CSV/DOCX, visual node editor |
| Observability | live training curves, loss, GPU usage |
| Multi-GPU | supported (DDP / balanced); "major improvements coming" |

---

## 6. VRAM Budget for RTX 4090 (24 GB) — official Unsloth numbers

QLoRA = 4-bit, LoRA = 16-bit. These are **absolute minimums** (batch 1, short context).

| Model params | QLoRA (4-bit) | LoRA (16-bit) | **Fits 24 GB?** |
|--------------|---------------|---------------|-----------------|
| 3B | 3.5 GB | 8 GB | ✅ comfortable |
| 7B | 5 GB | 19 GB | ✅ |
| 8B | 6 GB | 22 GB | ✅ |
| 9B | 6.5 GB | 24 GB | ✅ (16-bit borderline) |
| 11B | 7.5 GB | 29 GB | ✅ QLoRA only |
| 14B | 8.5 GB | 33 GB | ✅ QLoRA only |
| 27B | 22 GB | 64 GB | ✅ QLoRA (tight) |
| 32B | 26 GB | 76 GB | ❌ over budget |
| 40B+ | 30+ GB | 96+ GB | ❌ |

**4090 sweet spot: QLoRA on 7B–14B dense models; up to 27B 4-bit on tight budgets. 16-bit LoRA up to ~9B. 32B+ requires a second GPU or cloud.**
OOM fix: reduce `per_device_train_batch_size` to 1–3.

---

## 7. Fleet Usage Cases

1. **Local SFT / QLoRA fine-tuning** of Gemma 4 (E2B / 12B), Qwen3/3.5 (4B), Llama 3.x (8B), gpt-oss (20B) on the 4090 — data never leaves the machine (vs cloud Foundry).
2. **Local RL (GRPO)** — e.g. DeepSeek-V4-Flash RL is a listed supported model; 80% less VRAM than vanilla RL.
3. **TTS / vision / embedding fine-tunes** — Orpheus-TTS (3B), vision models, embeddinggemma.
4. **GGUF export → Ollama / llama.cpp deployment** — train a LoRA, merge, export GGUF, serve via existing local-llm-mcp / Ollama stack.
5. **Local model serving for agents** — `unsloth start opencode/claude/codex`; OpenAI/Anthropic-compatible API usable as a provider in fleet webapps.
6. **MCP control endpoint** — an AI client can manage models, training runs, checkpoints, and exports over MCP. Candidate for a future fleet repo or an extension of local-llm-mcp.

---

## 8. Limitations (honest)

1. **vLLM not on native Windows** — WSL/Linux only. Unsloth's own kernels are fine; only the vLLM-backed fast-inference path is lost on Windows.
2. **VRAM ceiling** — see §6: 32B+ training does not fit 24 GB. 70B QLoRA marketing numbers assume bigger setups.
3. **GPU contention** — the 4090 currently serves Ollama. Training saturates the GPU for hours; pause/offload Ollama during runs or accept degraded serving.
4. **Core install on Windows requires PyTorch preinstalled** (plain `pip install unsloth`); use `--torch-backend=auto` or Studio to avoid this.
5. **License** — core Apache-2.0, **Studio UI AGPL-3.0**. Fine locally; AGPL matters only if Studio is redistributed/modified commercially.
6. **Multi-GPU training** is functional but explicitly "improvements coming" — single-GPU is the strong path (Goliath is single-GPU anyway).
7. **Disk** — torch + models + run outputs ~30–60 GB; shares the HF cache (`%USERPROFILE%\.cache\huggingface`).
8. **CPU-only mode** — chat + data recipes only, **no CPU training**.
9. **Python < 3.14** — Studio pins/creates its own 3.13 env; do not point it at fleet project venvs.

---

## 9. Documentation Structure

- [TECHNICAL.md](TECHNICAL.md) — architecture, full install reference (env vars, launch/remote options), API + MCP endpoint details, hardware matrix, licensing, Windows troubleshooting.
- [WORKFLOWS.md](WORKFLOWS.md) — SOPs: Core SFT pipeline, Studio GUI flow, GRPO/RL, GGUF export, `unsloth start` agents, MCP control endpoint, fleet integration paths, validation checklist.
- Related: [Local LLM integration](../local-llm/README.md) · [LOCAL_LLM_STANDARDS.md](../../standards/LOCAL_LLM_STANDARDS.md)

---
*Maintained by: Fleet docs (SOTA 2026) · Last updated: 2026-08-05*
