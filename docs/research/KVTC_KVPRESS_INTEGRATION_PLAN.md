# KVTC / KVPress Integration: Long Note and Plan

**Date:** 2026-03-18  
**Status:** Planning / exploratory  
**Context:** NemoClaw-style memory is implemented (store/recall/compaction); KV cache compression is not. This note covers whether and how to add it, RTX 4090 impact, and a detailed plan. Includes a MemOps-style summary at the end.

---

## 1. What we’re talking about

- **KV cache:** During autoregressive generation, the model keeps key/value vectors for every previous token so it doesn’t recompute them. For long contexts this cache grows linearly and dominates VRAM.
- **KVTC (KV Cache Transform Coding):** NVIDIA’s pipeline (PCA-style decorrelation + adaptive quantization + entropy coding) that compresses that cache by up to ~20× with small quality loss. Paper: arXiv 2511.01815.
- **KVPress:** NVIDIA’s open-source Python library (GitHub [NVIDIA/kvpress](https://github.com/NVIDIA/kvpress), `pip install kvpress`, Apache 2.0) that implements multiple KV cache compression methods and plugs into Hugging Face `transformers` via a custom pipeline. It does not literally brand “KVTC” in the README but is the same family (training-free compression of the KV cache). Supports many “presses” (e.g. ExpectedAttentionPress, KnormPress, SnapKVPress, StreamingLLMPress, DecodingPress for during-generation compression).

---

## 2. Does it help us? Honest assessment

**Where it helps:**

- **Long-context chat / RAG over huge docs:** If we ever run in-process inference (e.g. HF `transformers`) for “answer from this 100k-token doc,” the KV cache is the bottleneck. Compressing it lets us fit longer context in the same VRAM or the same context in less VRAM.
- **Council / agentic loops:** Robofang’s council does many perceive→think→act cycles. If any of that uses long conversation or long retrieved context in one forward pass, KV compression extends how much we can hold in context without going to a smaller model or heavier quantization.
- **Future-proofing:** Once we have a transformers-based long-context path, having kvpress in the stack is one dependency and a few flags; we don’t have to redesign later.

**Where it doesn’t move the needle (today):**

- **Current docs_mcp chat:** We use Ollama / LM Studio / OpenAI via `llm_client`. We don’t run HF inference in-process. So today there is no KV cache we control; adding kvpress doesn’t change current chat behavior.
- **Nemoclaw store/recall:** Those are semantic memory (LanceDB + embeddings). They don’t use the transformer’s KV cache. So KVTC/kvpress and “nemoclaw memory” solve different problems (inference-time cache vs. persistent semantic memory).

**Verdict:** It helps **if** we introduce a first-class “long-context inference” path using Hugging Face (e.g. a dedicated endpoint or agent that runs `transformers` + kvpress). It does **not** help until we have that path. So the benefit is conditional on an architectural decision: do we want such a path (e.g. for long-doc QA, council, or research)? If yes, implementing it with kvpress from the start is rational. If we stay “Ollama/API only” forever, kvpress stays unused.

---

## 3. Would it overtax the RTX 4090?

**Short answer: No. It should *reduce* peak VRAM use, not increase it.**

- The 4090 has 24 GB VRAM. The limiting factor for long context is the **size of the KV cache**, not the model weights alone (e.g. 70B in fp16 is already ~140 GB for weights; we’d run quantized. For 8B/13B, weights fit; the cache is what grows with context).
- KVPress compresses the cache **during** the same inference run. So for a given context length we use *less* VRAM (smaller cache). The compression step (scoring, pruning, optional quantization) is relatively cheap (CPU/small GPU). We are not running a second model.
- So: **kvpress is a way to fit longer context or the same context with lower peak VRAM.** It does not add a second 24 GB workload. For a 4090, the constraint remains “what model size and quant we run”; kvpress just lets that same setup handle longer sequences. We should still pick model size and quant to fit 24 GB; kvpress then stretches how much context we can attach.

**Caveat:** If we naively load a 70B fp16 model and then apply kvpress, we’re still out of memory (weights dominate). So “doesn’t overtax” assumes we keep our current discipline: models that already fit (e.g. 8B–13B, or 70B heavily quantized). Within that, kvpress is a net win for long context.

---

## 4. Detailed implementation plan

### 4.1 Prerequisites and dependencies

- **Python:** 3.10+ (we’re already there).
- **New dependency:** `kvpress` (and its deps: `torch`, `transformers` at versions kvpress expects). Optional: `flash-attn`, `eval` extras for speed and benchmarking.
- **Inference stack:** Hugging Face `transformers` + PyTorch. No vLLM/llama.cpp in the kvpress path; those would need their own integration if we ever want KV compression there.
- **Where it runs:** Either in the same process as docs_mcp (heavy: we’d load a model at startup or on first use) or in a **separate long-context service** (recommended) that we call from docs_mcp/robofang. Separate service keeps docs_mcp lightweight and avoids competing with Ollama for the 4090.

### 4.2 Phase 1: Prove it locally (no integration)

- Create a small script or notebook (e.g. under `research/` or `scripts/`):
  - `pip install kvpress` (+ torch, transformers).
  - Load a small model (e.g. Llama 3.1-8B or Qwen3-8B) with `device_map="auto"`.
  - Run the `kv-press-text-generation` pipeline with a long context and a press (e.g. `ExpectedAttentionPress(compression_ratio=0.5)` or `KnormPress`).
  - Measure: max VRAM (nvidia-smi), time to first token, and a simple quality check (e.g. one RAG-style question).
- **Exit criterion:** We can run 32k–128k tokens (or whatever our target is) with compression on the 4090 without OOM, and output is acceptable.

### 4.3 Phase 2: Long-context service (recommended)

- **Component:** Standalone Python service (FastAPI or Starlette) that:
  - Loads one HF model + one default press at startup (or on first request).
  - Exposes e.g. `POST /generate` or `POST /long-context-answer` with `context`, `question`, optional `compression_ratio` / `press`.
  - Uses kvpress pipeline under the hood; returns generated answer (and optionally metrics).
- **Deployment:** Run on the same machine as the 4090; either same process as Ollama or a separate process. If Ollama and this service share the GPU, we need a policy (e.g. “long-context service only when not doing council runs,” or use CUDA_VISIBLE_DEVICES to dedicate GPU to one at a time).
- **Config:** Port (e.g. in our 107xx range), model id, default press, max context length. Document in WEBAPP_PORTS and ops docs.

### 4.4 Phase 3: Integration with docs_mcp / robofang

- **Option A (docs_mcp):** Add a “long-context” chat or “answer from long doc” path that:
  - Takes a long document (or doc IDs) + question.
  - Calls the long-context service (or in-process HF+kvpress if we chose that) instead of Ollama/OpenAI.
  - Returns the answer. No change to existing Ollama/LM Studio/OpenAI chat unless we explicitly route certain requests to this path.
- **Option B (robofang/council):** Same idea: one “think with long context” tool or step that calls the long-context service. Council continues to use Ollama for normal turns; long-context tool is opt-in for specific tasks.
- **Observability:** Log model, press, context length, and VRAM (if available) so we can tune and avoid regressions.

### 4.5 Phase 4 (optional): Decoding compression and tuning

- KVPress supports **DecodingPress** (compress during generation) and **PrefillDecodingPress** (prefill + decoding). For very long generations we could enable decoding compression so the cache doesn’t grow unbounded.
- Tune **compression_ratio** and **press** choice (ExpectedAttention vs Knorm vs SnapKV, etc.) on our target tasks (e.g. RULER, or our own long-doc QA set) and document recommended defaults per use case.

### 4.6 What we deliberately don’t do (for now)

- **vLLM / llama.cpp:** KVPress is transformers-only. Integrating KV compression into vLLM or llama.cpp would require their codebases to support it (or a fork). Out of scope for this plan.
- **Ollama:** Ollama has its own inference stack; we don’t inject kvpress into it. Long-context would be a separate path.

---

## 5. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| 4090 shared with Ollama; OOM when both run | Run long-context service only when not running heavy council workloads; or dedicate GPU to one consumer at a time. |
| Model load time / cold start | Lazy load on first request, or keep service warm; document “first request may be slow.” |
| Quality drop from aggressive compression | Phase 1 benchmarks; choose conservative compression_ratio by default; expose ratio in config. |
| Dependency bloat (torch, transformers, kvpress) | Isolate in a dedicated venv or container for the long-context service so docs_mcp stays lean. |

---

## 6. Summary table

| Question | Answer |
|----------|--------|
| Do we implement it? | Only if we add a long-context inference path (HF + kvpress). Not required for current Ollama/API chat or nemoclaw store/recall. |
| Does it help? | Yes, for long-context chat, long-doc QA, and future council long-context steps. No, for “current docs_mcp as-is.” |
| Overtax 4090? | No. It reduces KV cache size; use models that already fit (8B–13B or quantized 70B), then kvpress stretches context. |
| Source to lift? | Yes: [NVIDIA/kvpress](https://github.com/NVIDIA/kvpress) (Python, Apache 2.0). |
| Recommended approach? | Phase 1 proof-of-concept → Phase 2 standalone long-context service → Phase 3 wire into docs_mcp or council as an optional path. |

---

## 7. MemOps note (copy to ADN / knowledge graph)

**Title:** KVTC and KVPress integration plan (Docs MCP / Robofang)

**Summary:** KV cache compression (NVIDIA KVPress, Python, Apache 2.0) can reduce VRAM for long-context inference by compressing the transformer’s key-value cache. It does not replace nemoclaw store/recall (those are semantic memory). It helps only if we add a Hugging Face–based long-context inference path (e.g. a dedicated service). RTX 4090 is not overtaxed; kvpress reduces peak VRAM for a given context length. Plan: (1) local PoC with kvpress pipeline on 4090, (2) standalone long-context service, (3) optional integration in docs_mcp or council for long-doc QA / long-context think steps. vLLM and Ollama are out of scope for this integration. Reference: `research/KVTC_KVPRESS_INTEGRATION_PLAN.md`, NVIDIA/kvpress, arXiv 2511.01815 (KVTC), arXiv 2510.00636 (Expected Attention).

**Tags:** #kvpress #kvtc #long-context #nvidia #robofang #docs-mcp #memops #planning
