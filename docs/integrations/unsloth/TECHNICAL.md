---
title: "Unsloth Technical Reference"
category: integration
status: active
audience: mcp-dev
skill_candidate: false
related:
  - integrations/unsloth/README.md
  - integrations/unsloth/WORKFLOWS.md
last_updated: 2026-08-05
---

# Unsloth — Technical Reference

Technical companion to [README.md](README.md). Covers architecture, install internals, launch/remote options, API surfaces, hardware matrix, licensing, and Windows troubleshooting. All facts verified against upstream docs (2026-08-05).

---

## 1. Architecture

```
Unsloth Studio (web UI, AGPL-3.0)
  ├── llama.cpp backend (GGUF inference, CPU/Vulkan/CUDA; compiled at first run)
  ├── PyTorch + Triton kernels (training/RL on CUDA)
  ├── HF Transformers + TRL (model/trainer plumbing, patched by Unsloth Zoo)
  └── FastAPI-style server: chat, training, recipes, export, API endpoints
```

Key components:

| Component | Role |
|-----------|------|
| **Unsloth Zoo** | Patching layer applied at import — replaces slow HF kernels with custom Triton kernels (attention, MLP, RoPE, cross-entropy) |
| **Dynamic quantization** | 4-bit/8-bit with on-the-fly dequantization in custom kernels; no separate bitsandbytes needed on the common paths |
| **Padding-free packing** | Long-context training: 3x faster, 30% less VRAM, 500K+ context on 80 GB |
| **GRPO/RL support** | ~80% less VRAM vs vanilla; FP8 RL and vision RL on consumer GPUs |
| **llama.cpp integration** | Dynamic GGUF quants, long-context fixes, MoE expert offload, tensor parallelism |

---

## 2. Unsloth Studio — Install Reference (Windows)

### 2.1 Install / update

```powershell
irm https://unsloth.ai/install.ps1 | iex      # install; same command updates
```

Installer behavior:
- Creates its own Python 3.11–3.13 venv via **uv** (does not touch fleet project venvs).
- Installs/compiles a llama.cpp binary bundle (first run 5–10 min).
- Installs CUDA toolkit matched to the detected driver (per requirements page).
- Re-running the installer replaces the previously selected llama.cpp backend when it differs.

### 2.2 Installer env vars

| Env var | Effect |
|---------|--------|
| `UNSLOTH_NO_TORCH=1` | GGUF-only mode (skip PyTorch) — inference without training |
| `UNSLOTH_SKIP_AUTOSTART=1` | Skip the post-install "start now" prompt (automated installs) |
| `UNSLOTH_PYTHON='3.12'` | Pin Python version |
| `UNSLOTH_STUDIO_HOME='C:\path'` | Isolated install (own venv, auth, studio.db, llama.cpp build) — must be passed at launch too |
| `UNSLOTH_FORCE_VULKAN=1` | Use Vulkan llama.cpp backend instead of CPU (GPU driver must provide Vulkan runtime; no separate SDK) |
| `UNSLOTH_NPM_REGISTRY=...` | Corporate npm mirror for the frontend build (developer install only) |

### 2.3 Launch options

```powershell
unsloth studio -p 8888                     # local only (127.0.0.1) — default, safe
unsloth studio -H 0.0.0.0 -p 8888          # bind LAN (raw port; firewall-dependent)
unsloth studio --secure -p 8888            # Cloudflare HTTPS tunnel; localhost-only + public https://*.trycloudflare.com URL; fails closed
unsloth studio -H 0.0.0.0 --cloudflare     # LAN bind + public tunnel URL
UNSLOTH_CPU_THREADS=8 unsloth studio -p 8888   # cap native CPU thread pools on high-core hosts
```

Security notes:
- **Server-side tools (web search, Python/terminal code execution) are ON by default and run as the logged-in user.** Anyone reaching the server with the API key can execute code on the machine. Keep the key private; use `--disable-tools` when exposing Unsloth.
- First public exposure (`--secure` / `--cloudflare`) with the auto-generated admin password triggers a password prompt (masked); headless setups use `UNSLOTH_STUDIO_PASSWORD=...` env var or `--password -` (stdin). Without a terminal it warns and shuts down after `UNSLOTH_STUDIO_BOOTSTRAP_TIMEOUT` (default 1 h) unless the password is changed in the UI.
- Prefer `--secure` over `-H 0.0.0.0` for anything beyond the local LAN.

### 2.4 Uninstall

```powershell
irm https://raw.githubusercontent.com/unslothai/unsloth/main/scripts/uninstall.ps1 | iex
```

Stops servers, removes install dir, launcher data, Start Menu entry, `HKCU\Software\Unsloth` key, and user PATH entries. Model cache (`%USERPROFILE%\.cache\huggingface\hub`) is **not** touched.

---

## 3. Unsloth Core — Install Reference

```powershell
winget install -e --id Python.Python.3.13   # if no Python
winget install --id=astral-sh.uv -e          # if no uv
uv venv unsloth_env --python 3.13
.\unsloth_env\Scripts\activate
uv pip install unsloth --torch-backend=auto
```

- `--torch-backend=auto` selects the correct torch/triton/CUDA build — the recommended Windows path.
- Plain `pip install unsloth` on Windows works **only** if PyTorch is already installed (e.g. torch 2.10+cu130 from `https://download.pytorch.org/whl/cu130`).
- Version floor: CUDA capability ≥ 7.0 (V100/T4/RTX 20/30/40/50, A100/H100/L40...). GTX 1070/1080 work but are slow.
- `pip install unsloth` auto-resolves compatible torch/transformers/xformers/triton versions.

---

## 4. API & Integration Surfaces

### 4.1 OpenAI / Anthropic-compatible endpoints

Studio serves local models through:
- `/v1/chat/completions` (OpenAI)
- `/v1/responses` (OpenAI Responses)
- `/v1/messages` (Anthropic Messages)

Any OpenAI-compatible client (fleet webapps, agents, LangChain-style tooling) can point at the Studio base URL.

### 4.2 `unsloth start` agent bridging

| Agent | Command |
|-------|---------|
| Claude Code | `unsloth start claude` |
| OpenAI Codex | `unsloth start codex` |
| Hermes Agent | `unsloth start hermes` |
| OpenClaw | `unsloth start openclaw` |
| **OpenCode** | `unsloth start opencode` |
| Subagent mode | `unsloth start claude --as-subagent --model unsloth/model-GGUF:quant` |

Claude Code / Codex / OpenCode keep their current model and use the local Unsloth model as a subagent.

### 4.3 MCP control endpoint (opt-in)

Unsloth exposes an **MCP control endpoint** (PR #7191) letting compatible AI clients manage:
- model loading / unload
- training runs (start, monitor, stop)
- data recipes
- checkpoints
- exports (GGUF)

This is the primary hook for fleet integration — see [WORKFLOWS.md](WORKFLOWS.md) §7.

### 4.4 Chat-side MCP client

Studio chat can load MCP servers (filesystem sandbox, custom servers) so local models can use MCP tools in conversation — relevant when evaluating local models against the fleet's own MCP surface.

---

## 5. Hardware & Performance Matrix

### Training support

| Vendor | Windows native | Notes |
|--------|---------------|-------|
| NVIDIA RTX 30/40/50 | ✅ | Primary path (Goliath: 4090) |
| AMD (RX 6000–9000) | ✅ | Native ROCm on Windows; also WSL/Linux |
| Intel | ✅ (guide) | Arc GPUs via specific guide |
| Mac (MLX) | n/a (macOS) | Training + MLX + GGUF all supported on macOS |
| CPU | ❌ training | Chat + data recipes only |
| Vulkan | inference only | GGUF inference on compatible GPUs incl. Intel |

### VRAM minimums (official, batch 1 short-context)

| Params | QLoRA 4-bit | LoRA 16-bit | 4090 verdict |
|--------|------------|-------------|--------------|
| 3B | 3.5 GB | 8 GB | ✅ |
| 7B | 5 GB | 19 GB | ✅ |
| 8B | 6 GB | 22 GB | ✅ |
| 9B | 6.5 GB | 24 GB | ✅ (16-bit borderline) |
| 14B | 8.5 GB | 33 GB | ✅ QLoRA |
| 27B | 22 GB | 64 GB | ✅ QLoRA tight |
| 32B | 26 GB | 76 GB | ❌ |
| 70B | 41 GB | 164 GB | ❌ |

OOM: lower `per_device_train_batch_size` to 1–3. Numbers vary by model; treat as floors.

---

## 6. Licensing

| Component | License |
|-----------|---------|
| Unsloth core package | **Apache-2.0** |
| Unsloth Studio UI | **AGPL-3.0** |
| Upstream deps | PyTorch (BSD), HF Transformers/TRL (Apache-2.0), llama.cpp (MIT) |

AGPL-3.0 only matters if Studio is redistributed or modified and offered as a network service. Local personal/fleet use is unaffected.

---

## 7. Windows Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `ImportError: DLL load failed` on 4-bit load | Historic bitsandbytes Windows issue; use `--torch-backend=auto` or Studio (dynamic quantization paths avoid bitsandbytes) |
| `pip install unsloth` fails / wrong torch | Plain pip on Windows needs PyTorch preinstalled — install torch first, or use the uv `--torch-backend=auto` line |
| Triton load failure | Torch/triton version mismatch; force-reinstall matching pair (`uv pip install unsloth --torch-backend=auto` handles it) |
| vLLM `fast_inference` fails | vLLM is not supported natively on Windows — use WSL/Linux or Unsloth's own kernels |
| Training OOM | Reduce batch size (1–3); use QLoRA instead of LoRA; shorten `max_seq_length` |
| Slow first launch | llama.cpp compile (5–10 min) is one-time |
| Studio won't expose publicly | See §2.3 — `--secure` fails closed if the Cloudflare tunnel cannot start |
| CUDA version mismatch | Driver 620.02 = CUDA 13.0; use cu130 PyTorch wheels (matches `--torch-backend=auto`) |

---

## 8. Version & Model Notes

- Python floor: **3.11–3.13** (3.14 NOT supported yet — do not point Studio at 3.14).
- Supported model families (2026-08 snapshot): Gemma 4 (text/image/audio, QAT+MTP+GGUF+MLX), Qwen3/3.5/3.6, Llama 3.x/4, gpt-oss (20B/24B), DeepSeek-V4-Flash, GLM-5.2 (744B via dynamic GGUF), Ministral 3, Kimi K2.7, MiniMax M3, DiffusionGemma, Orpheus-TTS, embeddinggemma. Full catalog: unsloth.ai/docs/get-started/unsloth-model-catalog.
- Model cache: `%USERPROFILE%\.cache\huggingface\hub` (shared with existing fleet HF usage; delete via Studio bin icon or manually).

---
*Last updated: 2026-08-05*
