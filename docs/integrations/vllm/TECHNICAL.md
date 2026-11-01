# vLLM: Technical Specifications

Last updated: 2026-10-23. Target: single RTX 4090 24GB (Ada sm_89, Goliath) + WSL2.
Supersedes 2026-02-14 version which had no model tables.

## 1. Hardware and software baseline

- GPU: NVIDIA RTX 4090 24GB. Driver >= 550, CUDA 12.4+ runtime. AWQ Marlin kernels
  need CUDA 12.4+; older bundled CUDA silently falls back to slow paths (decode <60 tok/s).
- CPU/RAM: Ryzen 9 class + 64GB DDR4/5. Needed for KV swap, prefix-cache host spill, fast safetensors load.
- OS path A (recommended Oct 2026): WSL2 Ubuntu + pip venv (`~/vllm`, python 3.10-3.12).
  `pip install -U vllm huggingface_hub`. Wheels bundle their own CUDA runtime.
- OS path B (now viable, was unreliable pre-2026-08): Docker Desktop + WSL2 backend +
  NVIDIA Container Toolkit, official image `vllm/vllm-openai:latest` (0.10.x tested).
  Do NOT build from source on WSL2, it is very slow. Use the official image first.
- Port: 11400 for Goliath vLLM OpenAI endpoint. 8000 is FORBIDDEN per WEBAPP_PORTS.md.
- Disk: weights on `N:\AI\hf` (WSL `/mnt/n/AI/hf`). D: is near-full. ext4 `~/models`
  is faster than 9p `/mnt/n` if load >5 min.

## 2. VRAM math for 24GB

Usable under `--gpu-memory-utilization 0.90`: about 21.6GB. Rest is CUDA graphs,
NCCL, Marlin workspace (~1-2GB).

Rule of thumb: weights + (tokens * kv_bytes_per_token) + 1.5GB overhead < 21.6GB.

| Quant | Bytes/param | 8B | 22B | 27B | 30B-A3B MoE | 32B | 70B |
|-------|-------------|----|-----|-----|-------------|-----|-----|
| BF16  | 2.0 | ~16GB | ~44GB | ~54GB | ~56.9GB | ~64GB | ~140GB |
| FP8   | 1.0 | ~8GB | ~22GB | ~27GB | ~30GB | ~32GB | ~70GB |
| AWQ/GPTQ 4-bit | ~0.55 | ~4.5GB | ~12-13GB | ~15-16GB | ~17.2GB | ~18-19GB | ~36-38GB |
| GGUF Q4_K_M | ~0.58 | ~5GB | ~13-14GB | ~16GB | ~18GB | ~19GB | ~40GB |

KV cache extra (FP8 KV, 128K ctx example): Qwen3-Coder-30B-A3B (4 KV heads x 128 dim
x 48 layers) ~49KB/token, so 128K ctx ~6GB on top of ~17.2GB weights. Fits Profile A.
Dense 32B at 128K is heavier, use 64K if sharing GPU with Plex/ComfyUI.

## 3. Model fit tables - single RTX 4090 + vLLM

### 3a. Runs well (fleet picks)

| Model | Format that fits | Resident approx | Ctx practical | Notes |
|-------|------------------|-----------------|---------------|-------|
| Qwen3-8B dense | BF16 | ~16GB | 32-128K | 120-220 tok/s. Best single-user speed. `vllm serve Qwen/Qwen3-8B` |
| Qwen3-Coder-30B-A3B-Instruct | AWQ 4-bit | ~17.2GB + KV | 64-131K | Fleet coding pick. 3B active, MoE. Needs `quantization_config` in config.json. Tool parser `qwen3_coder`. |
| Qwen3.8-27B dense | Q4 / AWQ 4-bit | ~16GB | 32-131K | Apache 2.0. 61.7 SWE-bench Pro. Base for Bonsai 2. |
| Qwen3-32B / Qwen2.5-Coder-32B dense | AWQ 4-bit | ~18-19GB | 32-64K | Tight but fits. Reduce `max-model-len` to 64K if KV pressure. |
| Qwen3.6-27B dense | Q4_K_M | ~16GB | 32-64K | Same class as 3.8-27B. |
| Qwen3.6-35B-A3B MoE | AWQ 4-bit / Q4 | ~19-20GB | 32-64K | Borderline good. Profile B (`0.80`, 64K). |
| Devstral-2 22B | Q4 | ~13-14GB | 32-64K | Agentic specialist. Headroom for long ctx. |
| gpt-oss-20B | Q4 | ~12GB | 32-64K | Fits easy. |
| DeepSeek-R1-Distill-Qwen 32B | AWQ 4-bit | ~18GB | 32-64K | Reasoner. Same envelope as Qwen 32B. |
| Mistral Small 24B | Q4 | ~14GB | 32K | 24GB-class staple. |

### 3b. Borderline / conditional

| Model | Condition to fit | Verdict |
|-------|------------------|---------|
| Qwen3-Coder-Next 30B | CPU offload, ~18.3GB VRAM reported | Works, slower. Use AWQ if available. |
| Qwen3.8-Flash-Next MoE | Check HF quant size, active-small only | Likely yes if AWQ under 19GB. Verify card. |
| Bonsai 2 27B ternary 5.9GB | Ollama / llama.cpp only | NOT a vLLM path. Ternary packing needs compatible kernels. Keep in Ollama, not vLLM. |
| GLM-5.3-Flash 320B/18B-active | No single-4090 | API only. Wait for 27B distill (~16GB) for local. |

### 3c. Does NOT fit single 4090

| Model | Why | Path |
|-------|-----|------|
| Qwen3.8-Max 2.4T (~95B active) | ~1.2TB Q4 | API only, datacenter |
| GLM-5.3 743B MoE | ~400GB+ Q4 | API only |
| Mistral Large 4 Le Chonk | ~400GB+ Q4 | API only |
| Llama 3.3 70B dense BF16/FP8 | 70-140GB | 2x4090 TP Q4 (~36-40GB total) works, single does not |
| Qwen3-235B-A22B | ~130GB Q4 | 4+ GPUs or API |

Dual-4090 (48GB, tensor-parallel): 70B Q4 at ~100 tok/s, ~5-10% slower than
theoretical single-48GB. vLLM `--tensor-parallel-size 2`, Ollama layer-split also works.

## 4. Docker (Oct 2026 - now recommended as alt to venv)

```bash
docker run --gpus all --ipc=host -p 11400:8000 \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  -e HF_HOME=/root/.cache/huggingface \
  vllm/vllm-openai:latest \
  --model Qwen/Qwen3-Coder-30B-A3B-Instruct-AWQ \
  --served-model-name qwen3-coder-30b \
  --max-model-len 131072 \
  --kv-cache-dtype fp8 \
  --enable-prefix-caching \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --gpu-memory-utilization 0.90 \
  --max-num-seqs 4
```

Required: `--gpus all`, `--ipc=host` (or `--shm-size 8g`). Without it NCCL stalls.
WSL2 localhost forwarding: `[wsl2] localhostForwarding=true` in `.wslconfig`,
then `wsl --shutdown`. Verify from Windows PowerShell:
`Invoke-RestMethod http://localhost:11400/v1/models`.

Image is ~8-10GB, normal. For Plex/ComfyUI coexistence use Profile B:
`--max-model-len 65536 --gpu-memory-utilization 0.80`.

## 5. Config and API

- Protocol: OpenAI-compatible `/v1/models`, `/v1/chat/completions`, `/metrics`.
- PagedAttention: on by default. Prefix caching: `--enable-prefix-caching`
  (block-hashed 16-token blocks, LRU, <1% overhead).
- Tool calling: `--enable-auto-tool-choice --tool-call-parser <name>`.
  Smoke test must return `finish_reason: tool_calls`, not prose.
- Metrics to watch: `prefix_cache_hits/queries` (>0.5 good), decode tok/s
  (120-220 expected for 30B-A3B AWQ; <60 = Marlin fallback or contention).

Backups: *.20261023_234900.bak in this folder.
