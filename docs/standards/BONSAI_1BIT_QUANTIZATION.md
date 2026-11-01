# 1-bit LLMs: History, Mechanism, and Fleet Impact

**Status:** Active research note, feeds [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) §6
**Date:** 2026-09-23 · Owner: Sandra S.

---

## TL;DR

1-bit (really 1.58-bit / ternary) quantization is not a rounding trick applied
after the fact — it's a training-time constraint that turns out to work far
better than anyone expected in 2023. The practical payoff for a fleet running
local LLMs on a single consumer GPU: a 27B model that used to need ~18 GB of
VRAM and cold-loaded in 20+ seconds now needs ~4.4 GB and loads in ~4 seconds,
while keeping ~98% of the original model's benchmark score. Measured on this
machine (RTX 4090), not quoted from a vendor deck: **112.3 tok/s vs 67.8
tok/s** (~1.7x) steady-state generation, **3.9s vs 23.4s** (~6x) cold load,
comparing `MobiusDevelopment/Bonsai-27B-Q1_0-gguf` against the standard-quant
`qwen3.8:27b` it's distilled from, same prompt, same machine, same Ollama.

That 1.7x is real but deliberately not the ~9x figure Microsoft's own BitNet
benchmarks show — and the reason why is the most important technical nuance
in this whole note (see §4).

---

## 1. History: this started at Microsoft Research, not PrismML

| Date | Event |
|---|---|
| 2023-10-17 | [**BitNet: Scaling 1-bit Transformers for Large Language Models**](https://arxiv.org/abs/2310.11453) — Microsoft Research. Introduces `BitLinear`, a drop-in replacement for `nn.Linear` that constrains weights to {-1, +1} *during training*, not after. First proof that a transformer can be trained natively at ~1 bit/weight without the usual catastrophic quality collapse of post-training quantization (PTQ). |
| 2024-02-27 | [**The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits**](https://arxiv.org/abs/2402.17764) — Microsoft Research. The BitNet b1.58 paper. Relaxes the weight alphabet from binary {-1,+1} to **ternary {-1, 0, +1}** — log2(3) ≈ 1.58 bits/weight, hence "b1.58". The zero state matters: it lets the model *sparsify* (skip a weight entirely) rather than being forced to pick a sign for every connection, which is why ternary closes the quality gap with FP16 far more than pure binary ever could. This is the paper the "1.58-bit" name in every subsequent model traces back to. |
| 2024 | [**bitnet.cpp**](https://github.com/microsoft/BitNet) — Microsoft's official inference framework, purpose-built ternary GEMM kernels for CPU (ARM + x86) and GPU. This is the part that matters for *speed*, not just size — see §4. |
| 2025-04 | **BitNet b1.58 2B4T** — first open-weight, native 1-bit model at real scale (2B params, 4T training tokens) from Microsoft. Matches FP16 models of the same size on standard benchmarks. Proved the recipe scales past toy sizes. |
| 2026-03 | **Bonsai 8B** ([PrismML](https://prismml.com/news/bonsai-8b)) — first commercially-viable 1-bit LLM from a non-Microsoft lab. 8.2B params in 1.15 GB, ~14x smaller than a 16-bit model of the same size, 8x faster / 4-5x less energy on edge hardware. Scores 70.5 average vs Llama's 67.1 — *beats* the full-precision comparison model it's roughly sized against. |
| 2026-09-18 | **Bonsai 2 27B** ([SiliconANGLE](https://siliconangle.com/2026/09/18/prismml-launches-bonsai-2-27b-a-high-intelligence-ai-model-so-small-it-fits-on-consumer-hardware/), [TechCrunch](https://techcrunch.com/2026/09/17/prismml-hopes-its-tiny-llm-could-change-how-we-all-use-ai/)) — the model this fleet is now running. Compresses Qwen3.8 27B (~56 GB at native 16-bit) down to ~5.9 GB, retaining ~98.2% of aggregate benchmark score. |

**The throughline:** BitNet proved *native* 1-bit training works. PrismML's
contribution isn't a new theoretical result — it's a practical recipe
(see §2) for getting 1-bit-quality models *derived from* an existing strong
teacher (Qwen3.8) instead of needing a fresh multi-trillion-token pretraining
run for every size/quality tier you want. That's what makes it commercially
viable to ship a whole family of sizes (8B, 27B, and presumably more to
come) quickly.

---

## 2. Why this isn't just "more aggressive quantization"

The critical distinction, easy to miss: **standard quantization (Q4_K_M,
Q8_0, GPTQ, AWQ, etc.) is post-training** — you train a model at full
precision, then round the weights down afterward. Push that below ~4 bits
and quality falls off a cliff, because the model's weights were never
optimized to survive that rounding.

BitNet's insight, which Bonsai inherits: **constrain the weight alphabet
*during* training (or distillation), not after.** From the actual technical
writeups on Bonsai 2 ([dev.to walkthrough](https://dev.to/fernandonog/how-prism-ml-squeezed-a-27b-model-into-39-gb-411l), [PrismML docs](https://docs.prismml.com/get-started/introduction)):

- Weights are ternary {-1, 0, +1} (or binary {-1, +1} for some variants) —
  **the alphabet the student is trained to reach**, not a rounding of
  something already trained at FP16.
- Each *group* of weights keeps one FP16 scaling factor, so the model isn't
  literally 1 bit end-to-end — it's ~1.125 bits/weight once you amortize the
  per-group scale, matching the numbers vendors quote.
- The distillation recipe (PrismML calls it "DSpark") uses the full Qwen3.8
  27B as teacher, with a diffusion-flavored block-denoising objective and
  survival-probability-weighted distillation — the point of all that
  machinery is getting a ternary-constrained student to actually match a
  16-bit teacher's behavior, not just its weight statistics.
- The compression covers **everything** — embeddings, attention, MLPs, and
  the LM head — not just a subset of layers.

This is why Bonsai 2 27B keeps ~98% of Qwen3.8 27B's score instead of falling
off the PTQ cliff a naive 1-bit round of the same model would hit.

---

## 3. Why 1-bit models are *faster*, not just smaller — the memory wall

Single-request, autoregressive text generation (the actual usage pattern for
every fleet tool calling a local LLM — one request at a time, not a batched
serving farm) is **memory-bandwidth-bound, not compute-bound**. The GPU's
tensor cores are almost always waiting on weights to arrive from VRAM, not
the other way around:

```
tok/s ≈ memory_bandwidth ÷ active_bytes_per_token
```

Cut the bytes per weight and you don't just save VRAM capacity — you
directly raise the achievable tokens/sec, because the same bandwidth now
moves proportionally more "model" per second. This is the whole reason a
1-bit model isn't just "the same model, cheaper" — it's mechanically faster
at the one thing that matters for interactive/agentic local use.

Published BitNet-native numbers (architecture with purpose-built ternary
kernels, [bitnet.cpp](https://arxiv.org/pdf/2502.11880)):

- BitNet b1.58 70B: **2977 tok/s** vs LLaMA 70B's 333 tok/s on the same
  class of hardware — **~9x**.
- ARM CPU speedups of 1.37x-5.07x, x86 CPU 2.37x-6.17x, with 55-82% less
  energy per token.

---

## 4. Why our own measured number is ~1.7x, not ~9x — read this before quoting either

Those bitnet.cpp figures are for models running on **Microsoft's own
purpose-built ternary GEMM kernels**, which never materialize the weights
back to FP16/INT8 — the matmul itself operates directly on packed ternary
values.

`MobiusDevelopment/Bonsai-27B-Q1_0-gguf` is a **community GGUF port running
through Ollama's llama.cpp backend**, not bitnet.cpp. Earlier research for
this same rollout found: *"Ollama's GGUF parser has compatibility issues
with certain tensor types in Bonsai 2's quantizations, so `ollama create`
fails on both packings, and the official library has no Bonsai 2 entry to
pull instead"* — which is exactly why we're on a community upload rather
than an official one. It's a reasonable inference (not independently
confirmed by reading llama.cpp's kernel source) that this GGUF path
dequantizes toward a higher-precision compute format rather than using a
true packed-ternary matmul kernel, which would explain why the *load*
speedup (VRAM/disk bytes moved, ~6x measured) is much larger than the
*generation* speedup (compute path, ~1.7x measured) — the load-time win is
architecture-independent (fewer bytes on disk/in VRAM either way), while the
generation-time win depends on whether the compute kernel is actually
ternary-native.

**Practical takeaway:** the ~1.7x / ~6x numbers measured on this fleet's
actual RTX 4090, via Ollama, are the honest baseline to plan around for any
repo using the Ollama-served community GGUF. If a future repo runs
bitnet.cpp directly (not through Ollama), the BitNet-native ~9x figures
become the more relevant reference — but that's a different runtime, not
addressed by this rollout.

---

## 5. Hardware impact: what this actually changes for the fleet

| | Full-precision/Q4 27B (e.g. `qwen3.8:27b`) | Bonsai 2 27B (1-bit) |
|---|---|---|
| Package size | ~18 GB (Q4_K_M) / 56 GB (native FP16) | **~4.4 GB** (3.8 GB core + 629 MB vision) |
| Cold load (measured, this machine) | 23.4s | **3.9s** |
| Generation (measured, this machine) | 67.8 tok/s | **112.3 tok/s** |
| Benchmark retention vs teacher | — (is the teacher) | **~98.2%** |
| Fits alongside other GPU load on a 24 GB 4090 | Tight — one repo's own rejected-config comment measured `muse-glimmer` (18 GB) + a second model at 7.1 GB = 25 GB, over budget, causing VRAM swap and single-digit tok/s | Comfortable — leaves ~20 GB headroom for LM Studio, the IDE's own GPU use, or a second model concurrently |
| Realistic on a **16 GB** card (a cheaper dev-server GPU tier, not just the 4090) | Marginal-to-no — an 18 GB model doesn't fit at all; even Q4_K_M variants of 27B-class models eat most of 16 GB alone | **Yes, comfortably** — 4.4 GB leaves ~11 GB for context, KV cache, and anything else sharing the card |

The second-to-last row is the actual production incident that started this
whole investigation: `muse-glimmer`-family models were sized for a dedicated
24 GB card with nothing else running, and on this fleet's actual shared
4090 they were spilling past budget — the exact "GPU Optimization: The Last
Byte Rule" failure mode already documented in `LOCAL_LLM_STANDARDS.md` §🚨.

The last row is the more consequential one going forward: this class of
model makes a **cheaper 16 GB card** (RTX 4060 Ti 16GB, RTX 5060 Ti 16GB, or
similar — meaningfully less expensive than a 4090) a realistic dev-server
tier for 27B-class local inference, where it simply wasn't before. That's
a real capability shift for anyone provisioning fleet infrastructure that
doesn't already own a 4090-class card.

---

## 6. Fleet rollout status (2026-09-23)

Replaced `muse-glimmer` (all variants: base, `-65k`, `-131k`, `-kquant`) with
`MobiusDevelopment/Bonsai-27B-Q1_0-gguf` as the heavy/agentic-reasoning
default in:

- **aiwatcher-mcp** — live NSSM service, restarted and verified via logs
  (validated in <1s post-restart vs. muse-glimmer's ~14s cold-start with a
  transient "unreachable" warning)
- **arxiv-mcp** — live NSSM service, restarted (config verified; this repo
  calls its sampling model lazily, no forced end-to-end functional test)
- **fleet-agent-mcp** — live NSSM service, restarted (config verified;
  delegates through cline-mcp's REST bridge rather than calling Ollama
  directly)
- **local-llm-mcp** — the fleet's own central "unified AI gateway" /
  LM Link hub; not currently running as a service on this machine, config +
  `.env.example` fixed so new installs stop inheriting the old default
- **codecad-mcp**, **mathops-mcp** — config-only, not currently running

Checked and correctly left alone (real config already avoided
`muse-glimmer`, or the reference was in a comment, not active):
`dark-app-factory` (already on `mistral-small:24b`, with a comment
explicitly documenting *why* `muse-glimmer` was rejected — "18+7.1=25GB
swaps"), `comfyops-mcp` (already on a 9B distill).

**Practical guidance for the reasoning model itself:** Bonsai is a
reasoning-tuned model — pass `"think": false` on Ollama's native
`/api/generate` or `/api/chat` for a clean answer without a
`<think>...</think>` preamble. Measured: ~11s and a full chain-of-thought
block when `think` is omitted/true; a bare, correct answer in ~400ms when
`think:false` is set explicitly.

---

## 7. Open questions / not yet verified

- **No isolated per-process VRAM measurement.** `nvidia-smi`'s per-process
  memory column is permission-restricted in this shell (`[Insufficient
  Permissions]` for most PIDs) — the ~4.4 GB figure is the published GGUF
  package size, not a directly-measured live VRAM delta on this machine. If
  you need an exact number, run `nvidia-smi` elevated.
- **Whether Ollama's llama.cpp backend uses a true packed-ternary kernel or
  dequantizes to a higher precision for compute** is inferred from the
  load-vs-generation speedup gap (§4), not confirmed by reading source.
  Worth a follow-up if the generation-speed gap turns out to matter for a
  latency-sensitive repo.
- **Bonsai 8B** (the smaller sibling, ~1.15 GB) hasn't been evaluated for
  the fleet's "fast/routing" tier yet — `pdurugyan/qwen3.5-9b-deepseek-v4-flash`
  is still in use there and wasn't part of this rollout.

## Related

- [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md) §6 — the short version,
  model-selection-table entry
- [GPU Optimization: The Last Byte Rule](./LOCAL_LLM_STANDARDS.md#-gpu-optimization-the-last-byte-rule) —
  the VRAM-squatting failure mode `muse-glimmer` was hitting
