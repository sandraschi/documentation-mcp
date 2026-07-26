# DeepSeek DSPark on DGX Spark — viability reassessment

**Created:** 2026-06-30  
**Context:** Community has shipped working inference recipes for DeepSeek V4 Flash with DSpark speculative decoding on 2x DGX Spark. This document assesses whether DSpark changes the "DGX Spark is a dud" verdict from `dgx-spark-lessons-vs-2026-silicon.md`.

---

## What is DSpark

DSpark is DeepSeek V4 Flash's built-in **speculative decoding head**. The model has a draft predictor that proposes ~5 tokens ahead; a modified vLLM checks them against the full model, accepting ~67% on average. The result is ~3.4 accepted draft tokens per step, roughly doubling effective throughput versus raw autoregressive decode.

DSpark is **part of the model**, not a separate framework. The community repos (below) integrate it into a vLLM fork with multi-node DGX Spark support.

### Key community repos (June 2026)

| Repo | Focus | Stars |
|------|-------|-------|
| `MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark` | 2-node NVFP4 KV recipe, Keys concurrency patch, 1M context | 54 |
| `tonyd2wild/DeepSeek-v4-Flash-DSpark-60-tok-s-900K-ctx-2x-DGX-Spark` | Single-stream deep-context benchmark reference | 19 |
| `tonyd2wild/DeepSeek-v4-Flash-DSpark-1M-NVFP4-KV-2x-DGX-Spark` | 1M NVFP4 KV variant | 48 |
| `fraserprice/dspark-vllm` | vLLM fork with DSpark for RTX Pro | 2 |
| `drowzeys/Keys-Concurrency-Patch-for-DSpark-DeepSeek-V4-Flash` | Concurrency fix for multi-session serving | 9 |

All MIT/Apache-2.0. No official DeepSeek repo ships this packaged for DGX Spark.

---

## Performance numbers (validated on 2x DGX Spark, 1 GPU/node, TP=2)

### Mode A: Single-stream deep context (tonyd2wild benchmark)

| Metric | Value |
|--------|-------|
| Token/s | **~60 tok/s** (mean 62.5 across 3 runs) |
| Acceptance rate | **~67%** |
| Accepted/draft | **3.4** tokens |
| Max context | **~900K tokens** (fp8 KV) |
| GPU KV cache | ~2M tokens (NVFP4 path) |

Benchmark settings: `code_completion`, 512 prompt tokens, 256 max tokens, temp=0, thinking=false.

### Mode B: High-concurrency (MiaAI-Lab + Keys patch)

| Metric | Value |
|--------|-------|
| Aggregate decode | **~315 tok/s** (C16 static), **~205 tok/s** (C16 staggered) |
| Max context | **200K tokens** per session |
| Concurrent sessions | **16** |
| 1M-context profile | 6 concurrent sessions, ~182 tok/s aggregate |

### Mode C: 1M deep context (MiaAI-Lab + NVFP4 KV)

| Metric | Value |
|--------|-------|
| Token/s | ~60 tok/s |
| Context window | **~1M tokens** |
| Concurrent sessions | **6** (shared KV pool, ceiling per request) |
| GPU KV cache | ~2.04M tokens |

---

## Does this change the "DGX Spark is a dud" verdict?

### The old verdict (pre-DSpark)

From `dgx-spark-lessons-vs-2026-silicon.md`:

- GB10 is **memory-bandwidth-bound** at ~273 GB/s LPDDR5X
- Stock vLLM on 2x DGX Spark with DeepSeek V4 Flash raw decode: **~19-42 tok/s**
- "128 GB unified RAM did not fix a slow GPU"
- "Decode still crawls"

### The new verdict (with DSpark)

**DSpark speculative decoding roughly doubles throughput** — from the ~20-40 tok/s raw range to **~60 tok/s** measured. This is a genuine improvement, not marketing:

| | Raw decode (old) | DSpark decode (new) |
|---|---|---|
| Throughput | ~19-42 tok/s | **~60 tok/s** |
| Context | Not reliably measured | **~900K-1M** validated |
| Concurrency | Single stream only | **Up to 16 sessions** (at 200K ctx) |

### Honest assessment

**60 tok/s at 900K context is usable.** Not fast, but usable. Reading speed is ~8-15 tok/s for a human, so 60 tok/s is ~4-7x reading speed. For agent workloads (tool calls, reasoning, code generation), this is workable.

**The bandwidth wall still exists.** DSpark doesn't fix LPDDR5X bandwidth — it's a software-level speculative decoding optimization. You're still memory-bound. The 67% acceptance rate means ~33% of draft tokens are wasted compute.

**But "usable" is a new category.** The old verdict was "crawls" / "dud." With DSpark, 2x DGX Spark moves into "functional agent server" territory for a specific model (DeepSeek V4 Flash). Whether that's worth ~$8K-10K (2x ~$4-5K units) depends on use case.

---

## Would this be useful for the fleet?

### What it enables

| Use case | Fit |
|----------|-----|
| **Local DeepSeek V4 Flash inference** | Yes — this is the only consumer-priced hardware that can fit V4 Flash |
| **Private agent serving** | Yes — no API key, no cloud dependency, no rate limits |
| **Deep-context work (100K-1M tokens)** | Yes — the large unified memory is the differentiator |
| **Replacement for DeepSeek API** | Partial — 60 tok/s is slower than API (likely 100+ tok/s) but free after hardware purchase |
| **Fleet MCP tool execution** | Yes — serves as an OpenAI-compatible endpoint at `http://127.0.0.1:8888/v1` |
| **Replacement for 4090** | No — different use case; 4090 is for 7B-70B models at high speed; DGX Spark is for 300B+ at usable speed |

### What it doesn't enable

- **Training or fine-tuning** — far too slow, not enough compute
- **Running non-DeepSeek models** — DSpark is DeepSeek V4-specific
- **Low-latency real-time** — 60 tok/s with batching means first-token latency is seconds, not milliseconds

---

## Two operational profiles

### Profile 1: Agent server (deep context, moderate concurrency)

```
MAX_MODEL_LEN=1048576    # 1M context
MAX_NUM_SEQS=6           # 6 concurrent agents
KV_CACHE_DTYPE=nvfp4_ds_mla
GPU_MEMORY_UTILIZATION=0.84
```

Best for: Long-running agent sessions, code review of entire repos, multi-file context.

### Profile 2: High-throughput serving (shorter context, high concurrency)

```
MAX_MODEL_LEN=200000     # 200K context
MAX_NUM_SEQS=16          # 16 concurrent sessions
VLLM_USE_B12X_WO_PROJECTION=1
```

Best for: Multi-user serving, batch processing, many independent short requests.

---

## Hardware requirements

| Item | Minimum | Notes |
|------|---------|-------|
| Nodes | **2x DGX Spark** | TP=2 requires 2 nodes; single node cannot serve V4 Flash |
| Memory | 128 GB/node | Unified LPDDR5X; both GPUs must see model weights |
| Networking | NVLink-C2C + RoCE between nodes | `MASTER_ADDR` on private interlink |
| Storage | ~150 GB free | Model weights + KV cache runtime |
| OS | Linux (Ubuntu 22.04+) | Docker + NVIDIA container toolkit |
| Power | 2x 100-300W | Per-node TDP under load |

**Single-node is impossible.** DeepSeek V4 Flash (300B+ params) cannot fit in a single GB10's 128 GB, even at NVFP4. The model is sharded across two nodes with TP=2.

**Estimated cost:** 2x DGX Spark at ~$4,000-4,700/unit = **~$8,000-9,400** total. As of June 2026, availability is poor (shortage + low volume). Used market may have shelf-sitters from disappointed early buyers.

---

## Comparison: DGX Spark vs Alternatives for running DeepSeek V4 Flash

| Platform | Tok/s (est.) | Context | Cost | Availability |
|----------|-------------|---------|------|-------------|
| **DeepSeek API (cloud)** | ~100+ | 1M | Pay-per-token | Always |
| **2x DGX Spark + DSpark** | ~60 | 900K-1M | ~$8-9K upfront | Poor (shortage) |
| **RTX 4090 (24 GB)** | Cannot run | N/A | $1.6K | Good |
| **RTX 5090 (32 GB)** | Cannot run | N/A | TBD | Late 2026 |
| **2x RTX PRO 6000 (96 GB)** | Unknown | Unknown | ~$20K+ | Enterprise |
| **Mac Studio M3 Ultra (192 GB)** | ~15-25 (est.) | Limited by bandwidth | ~$7K | Good |

**The value proposition for DGX Spark is narrow:** it's the cheapest hardware that can self-host DeepSeek V4 Flash at all. If you need a private, no-API-key V4 Flash endpoint with deep context, there is no alternative at this price point. But it's a slow endpoint relative to cloud, and the hardware is hard to buy.

---

## Key risks

1. **Community-only support.** DSPark on DGX Spark is maintained by community forks of vLLM, not by DeepSeek or NVIDIA. No guarantee of updates, bug fixes, or vLLM upstream merge.

2. **Single-model lock-in.** This hardware/software stack is purpose-built for DeepSeek V4 Flash. If a better open-weight model ships that doesn't use DSPark speculative heads, the 60 tok/s advantage disappears.

3. **Hardware availability.** DGX Spark was widely returned/disappointing. Units on the used market may have thermal/software issues. New units are scarce.

4. **NVFP4 software fragility.** The NVFP4 KV-cache path is experimental. Community reports of illegal instruction crashes, CUDA graph failures on ARM64. The Stage C padded-envelope path works but is described as a workaround, not a fix.

5. **DGX Station / GB300 may obsolete this.** If NVIDIA ships GB300 at a comparable price with real HBM bandwidth, 2x DGX Spark becomes obsolete overnight. The current 2026 silicon roadmap suggests this could happen within 12 months.

---

## Recommendation

**Wait.** DSPark makes DGX Spark technically viable for running V4 Flash locally, but:

- DGX Spark availability is poor
- The GB10 is a known-questionable silicon generation
- The 60 tok/s is at the bottom edge of "usable"
- GB300/DGX Station could ship within a year with far better bandwidth

If you get offered two used DGX Sparks at a steep discount (<$2K each), it becomes interesting. At MSRP, the cloud API is cheaper and faster unless you have a specific need for private, local, no-rate-limit deep-context inference.

When/if DGX Station ships with GB300 + HBM-class bandwidth, revisit immediately — that would make self-hosting V4 Flash (and successors) genuinely competitive with cloud.

---

## References

- `dgx-spark-lessons-vs-2026-silicon.md` — Why DGX Spark was a dud (pre-DSpark)
- `products/rtx-spark-platform.md` — RTX Spark superchip platform (GB10-class, fall 2026)
- `products/dgx-station-windows.md` — DGX Station with GB300 (HBM bandwidth)
- `MiaAI-Lab/DeepSeek-v4-Flash-DSpark-2x-DGX-Spark` — Primary recipe repo
- `tonyd2wild/DeepSeek-v4-Flash-DSpark-60-tok-s-900K-ctx-2x-DGX-Spark` — Benchmark reference
