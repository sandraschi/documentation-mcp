---
title: KVTC and KVPress integration plan (Docs MCP / Robofang)
status: planning
tags: [kvpress, kvtc, long-context, nvidia, robofang, docs-mcp, memops, planning]
source: research/KVTC_KVPRESS_INTEGRATION_PLAN.md
---

# KVTC / KVPress — MemOps note

KV cache compression (NVIDIA KVPress, Python, Apache 2.0) reduces VRAM for long-context inference by compressing the transformer’s key-value cache. It does **not** replace nemoclaw store/recall (those are semantic memory in LanceDB).

**When it helps:** Only if we add a Hugging Face–based long-context inference path (e.g. a dedicated service). Current Ollama/API chat and nemoclaw tools are unchanged.

**RTX 4090:** Not overtaxed; kvpress *reduces* peak VRAM for a given context length. Use models that already fit (8B–13B or quantized 70B); kvpress then stretches how much context fits.

**Plan:** (1) Local PoC with kvpress pipeline on 4090. (2) Standalone long-context service (HF + kvpress). (3) Optional integration in docs_mcp or council for long-doc QA / long-context think steps. vLLM and Ollama are out of scope for this integration.

**References:** [NVIDIA/kvpress](https://github.com/NVIDIA/kvpress), arXiv 2511.01815 (KVTC), arXiv 2510.00636 (Expected Attention).
