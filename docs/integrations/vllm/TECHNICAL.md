# vLLM: Technical Specifications

This document outlines the high-performance architecture of the vLLM engine.

## 💻 Hardware Requirements

- **Primary GPU**: **NVIDIA RTX 4090 (24GB)**. Key for running PagedAttention with large block sizes.
- **CPU**: Substantial multi-core performance (Ryzen 9) required to feed the GPU and manage the request queue.
- **Memory**: 64GB DDR4. Essential for the KV Cache storage.

## ⚙️ Configuration & API

- **Protocol**: OpenAI-compatible REST API.
- **Serving Port**: `8000`.
- **PagedAttention**: Enabled by default to eliminate KV cache fragmentation.
- **GPU Memory Utilization**: Typically set to `0.9` for the workstation to ensure stability.

## 🏗️ Internal Logic
vLLM utilizes **Continuous Batching**, allowing new requests to be added to the batch as soon as current requests finish the prefill stage, significantly reducing time-to-first-token in a multi-user/multi-agent environment.

---
*Last updated: 2026-02-14*
