# LM Studio: Technical Specifications

This document outlines the performance settings and internal logic of the LM Studio environment.

## 💻 Hardware Requirements

- **GPU Acceleration**: Enabled via **CUDA (NVIDIA)** for the **RTX 4090**.
- **CPU Offloading**: Managed dynamically based on VRAM availability.
- **Model Storage**: All `.gguf` files must be stored in the central `D:\Models\LM_Studio` directory for fleet indexing.

## ⚙️ Configuration & API

- **Server Identity**: OpenAI-compatible.
- **Endpoint**: `http://localhost:1234/v1`.
- **Context Length**: Set to `32k` by default for complex architecture analysis.
- **GPU Layers**: Maximum layers should be offloaded to the GPU to hit >50 t/s.

## 🏗️ Model Selection Logic
- Priority is given to **K-Quants** (e.g., Q6_K, Q8_0) to maintain high precision for technical materialist reasoning.
- Experimental models are quarantined in the `Beta` folder until validated by an agentic audit.

---
*Last updated: 2026-02-14*
