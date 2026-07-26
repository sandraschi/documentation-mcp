# LMCache Evaluation

**Date:** 2026-06-16  
**Status:** Evaluated — not applicable yet, revisit if fleet moves to vLLM/SGLang  
**Source:** https://github.com/LMCache/LMCache  
**License:** Apache 2.0  
**Related:** `research/KVTC_KVPRESS_INTEGRATION_PLAN.md`

---

## 1. What it is

LMCache is a **KV cache management layer** for self-hosted LLM inference engines. It turns KV cache from temporary GPU state into persistent, reusable storage that can be shared across requests, sessions, and engine instances. Part of the PyTorch Foundation ecosystem since Oct 2025.

Key capabilities:

- **Tiered KV cache offloading**: GPU → CPU RAM → local SSD → remote backends (Redis, Mooncake, S3, GDS, NIXL)
- **Prefix cache reuse**: Shared system prompts, RAG contexts reused across requests without recomputation
- **Non-prefix reuse (CacheBlend)**: Reuse cached KV blocks at arbitrary positions, not just prefix
- **PD disaggregation**: Prefill/decode split across workers with KV transfer over NVLink/RDMA/TCP
- **KV compression**: Pluggable SERDE interface for compression, token dropping, custom serialization
- **Observability**: Prometheus metrics for cache hit rates, lifecycle, per-user usage
- **Multi-process architecture**: Standalone daemon — no fate-sharing with inference engine crashes
- **Engine-neutral**: Works with vLLM, SGLang, NVIDIA Dynamo

## 2. Does it help the fleet? Honest assessment

**No, not today.** The fleet's LLM usage pattern doesn't match LMCache's target:

| Factor | Fleet reality | LMCache requirement |
|--------|--------------|---------------------|
| Serving engine | Ollama (local), Anthropic/Google APIs (cloud) | vLLM or SGLang |
| GPU count | 1× RTX 4090 | Multi-GPU clusters benefit most |
| Request volume | Individual MCP tool calls, low concurrency | High-throughput serving with shared prefixes |
| KV cache mgmt | Ollama handles internally; cloud APIs abstract it | Requires direct engine integration |
| Install | `pip install lmcache` + CUDA build deps (csrc/) | Heavy — C++/CUDA extensions, cmake |

**Where it would help (future triggers):**

- **Trigger 1**: Fleet migrates from Ollama to vLLM/SGLang for local serving (e.g., for better batching, longer context, or DeepSeek V3/R1 serving)
- **Trigger 2**: Fleet adds a second GPU and wants prefill/decode disaggregation
- **Trigger 3**: Multiple MCP tools concurrently hitting a local LLM with shared system prompts (RAG-heavy agentic workflows where prefix reuse would cut TTFT significantly)
- **Trigger 4**: Fleet runs a multi-node inference setup (e.g., via P2P CPU memory sharing)

## 3. Architecture notes (for future reference)

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────┐
│  vLLM / SGLang  │────▶│  LMCache Daemon  │────▶│  Storage    │
│  (inference)    │     │  (standalone)    │     │  Backend    │
│                 │◀────│                  │     │  (Redis,    │
│                 │     │  KV store/load   │     │  disk, CPU) │
└─────────────────┘     └──────────────────┘     └─────────────┘
```

- LMCache runs as a **separate process** from the inference engine
- Communicates via shared memory or TCP
- KV cache persists across engine restarts
- Config via YAML (storage backend, chunk size, eviction policy)

Supported storage backends (C++ connectors in `csrc/storage_backends/`):
- CPU RAM (default)
- Local filesystem (SSD)
- Redis / Valkey
- Mooncake (distributed KV store)
- Aerospike
- S3-compatible object storage
- NVIDIA GDS (GPU Direct Storage)
- NIXL (NVIDIA Inference eXchange Library)

## 4. Comparison with KVTC/KVPress

| | LMCache | KVPress |
|---|---------|---------|
| **Purpose** | KV cache persistence, reuse, and sharing | KV cache compression during generation |
| **Scope** | Infrastructure layer (storage, transfer, observability) | Algorithm layer (compression methods) |
| **Engine** | vLLM, SGLang, Dynamo | HuggingFace transformers |
| **Complementary?** | Yes — LMCache could use KVPress-style compression in its SERDE pipeline | Yes — compressed KV could be stored via LMCache |
| **Fleet fit** | Not yet | Not yet (same reason — Ollama abstracts KV) |

## 5. Install path (when ready)

```bash
pip install lmcache

# With vLLM integration
pip install lmcache[vllm]

# Config
cat > lmcache.yaml << EOF
storage:
  type: local_cpu    # or: local_disk, redis, mooncake
  path: /tmp/lmcache
chunk_size: 256
eviction_policy: lru
EOF

# Launch daemon
lmcache serve --config lmcache.yaml

# Launch vLLM with LMCache
vllm serve meta-llama/Llama-3-8B --enable-lmcache --lmcache-config lmcache.yaml
```

## 6. Community health

- 5,000+ GitHub stars (Aug 2025)
- PyTorch Foundation member (Oct 2025)
- NVIDIA Dynamo integration (Sep 2025)
- Active development (weekly commits on `dev` branch)
- Production users: Cohere, CoreWeave
- Partners: AMD, NVIDIA, Redis, Intel
- Regular community meetings, Slack workspace
- Well-documented: https://docs.lmcache.ai/

## 7. Decision

**Park it.** Revisit when any of the triggers in section 2 fire. The project is healthy, well-maintained, and Apache 2.0 — no risk of it disappearing. When the fleet needs production-grade local LLM serving beyond Ollama, LMCache + vLLM is the stack to evaluate first.
