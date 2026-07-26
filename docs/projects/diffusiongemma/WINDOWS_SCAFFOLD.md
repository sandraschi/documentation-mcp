# Windows Scaffold — DiffusionGemma on Goliath

Step-by-step guide for building and running DiffusionGemma on the Goliath workstation (Windows 11, RTX 4090).

**Prerequisites verified on Goliath (2026-06-17):**

| Requirement | Status |
|-------------|--------|
| RTX 4090 24 GB | ✅ |
| 64 GB RAM | ✅ |
| NVIDIA driver 591.86 / CUDA 13.1 | ✅ |
| Python 3.13 (`py` launcher) | ✅ |
| Git | Required — verify with `git --version` |
| CMake ≥ 3.18 | Required for llama.cpp build |
| Visual Studio Build Tools (C++) | Required for llama.cpp CUDA build |
| CUDA Toolkit (nvcc) | Required — separate from driver CUDA |

---

## Path A: llama.cpp + GGUF (Recommended)

This is the supported consumer-GPU path. Uses Unsloth-quantized GGUF weights and the diffusion-specific CLI.

### 1. Install build dependencies

```powershell
# Verify tools
git --version
cmake --version
nvcc --version
```

If `nvcc` is missing, install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) matching driver compatibility (12.x or 13.x).

Visual Studio 2022 Build Tools with "Desktop development with C++" workload is required.

### 2. Clone llama.cpp diffusion branch

```powershell
Set-Location C:\Users\sandr\dev
git clone https://github.com/ggml-org/llama.cpp.git llama.cpp-diffusion
Set-Location llama.cpp-diffusion
git fetch origin pull/24423/head:diffusion-support
git checkout diffusion-support
```

> PR number may be #24423 or #24427 depending on merge state — check [llama.cpp PRs](https://github.com/ggml-org/llama.cpp/pulls?q=diffusion) before building.

### 3. Build with CUDA

```powershell
cmake -B build -DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j
```

Binaries land in `build\bin\Release\` (or `build\bin\` depending on generator).

Verify:

```powershell
.\build\bin\Release\llama-diffusion-cli.exe --version
```

> **Do not use `llama-cli` or `llama-server`** — they cannot run diffusion models.

### 4. Download GGUF weights

```powershell
New-Item -ItemType Directory -Path C:\Users\sandr\dev\models\diffusiongemma -Force
Set-Location C:\Users\sandr\dev\models\diffusiongemma

# Requires huggingface-cli (pip install huggingface_hub)
py -m pip install huggingface_hub
py -m huggingface_hub.cli download unsloth/diffusiongemma-26B-A4B-it-GGUF diffusiongemma-26B-A4B-it-Q4_K_M.gguf --local-dir .
```

### 5. Run interactive chat

```powershell
Set-Location C:\Users\sandr\dev\llama.cpp-diffusion

.\build\bin\Release\llama-diffusion-cli.exe `
  -m C:\Users\sandr\dev\models\diffusiongemma\diffusiongemma-26B-A4B-it-Q4_K_M.gguf `
  -ngl 99 `
  -cnv `
  -n 512
```

### 6. Visual denoising (optional)

Watch the canvas denoise in real time — useful for understanding block diffusion:

```powershell
.\build\bin\Release\llama-diffusion-cli.exe `
  -m C:\Users\sandr\dev\models\diffusiongemma\diffusiongemma-26B-A4B-it-Q4_K_M.gguf `
  -ngl 99 `
  -cnv `
  --diffusion-visual
```

---

## Path B: HuggingFace Transformers (Fallback)

Heavier setup; useful for fine-tuning experiments via Unsloth. Not recommended as the daily inference path on Goliath.

```powershell
py -m pip install torch transformers accelerate
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "google/diffusiongemma-26B-A4B-it"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype="auto",
)
```

> `trust_remote_code=True` is mandatory — diffusion attention modules are not in standard Transformers.

VRAM at FP16 will not fit on 24 GB. Use 4-bit quantization (bitsandbytes) or stick with GGUF Path A.

---

## Path C: Unsloth Studio (GUI)

[Unsloth Studio](https://unsloth.ai/) v0.1.463-beta+ supports DiffusionGemma with claimed 1.8× inference speedup and fine-tuning. Useful for:

- Quick smoke test without building llama.cpp
- Fleet-domain fine-tune experiments
- GGUF export

---

## Directory Layout (Proposed)

```
C:\Users\sandr\dev\
├── llama.cpp-diffusion\          # PR branch build
│   └── build\bin\Release\
│       └── llama-diffusion-cli.exe
├── models\diffusiongemma\
│   └── diffusiongemma-26B-A4B-it-Q4_K_M.gguf
└── repos\mcp-central-docs\
    └── projects\diffusiongemma\   # This documentation
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Unsupported model architecture` | On llama.cpp main branch | Checkout `diffusion-support` branch |
| CUDA OOM | Desktop apps + model | Close LM Studio loaded models; use Q4_K_M not Q5/Q8 |
| Segfault on `--version` | CUDA toolkit / driver mismatch | Run `nvcc --version`; rebuild with matching CUDAToolkit_ROOT |
| `trust_remote_code` error | Transformers path | Add `trust_remote_code=True` |
| No streaming output | By design | Blocks of 256 tokens — not a bug |
| Ollama `pull` fails | No diffusion support in Ollama yet | Use Path A |

---

## Smoke Test Checklist

- [ ] `llama-diffusion-cli --version` exits 0
- [ ] Model loads without OOM (watch `nvidia-smi` during load)
- [ ] Single prompt returns coherent text block
- [ ] `--diffusion-visual` shows denoising steps
- [ ] Throughput spot-check: note tokens and wall time for 512-token generation
- [ ] Compare same prompt on Qwen 32B AR in LM Studio for quality/speed baseline

---

## What Does NOT Work on Windows Today

| Tool | Status |
|------|--------|
| `llama-cli` / `llama-server` | Cannot generate from diffusion models |
| Ollama | No diffusion model support |
| LM Studio | Awaiting upstream merge |
| NVFP4 on RTX 4090 | Blackwell-only format — use Q4_K_M |
| vLLM on Windows | vLLM is Linux-first; not a Goliath path |

---

*Return to [README.md](./README.md) for project overview.*
