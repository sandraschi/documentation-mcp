# Ollama: Technical Specifications

This document outlines the hardware optimization and internal logic of the Ollama stack on the Sandra workstation.

## 💻 Hardware Optimization

- **GPU**: **NVIDIA RTX 4090 (24GB GDDR6X)**. Models are offloaded to VRAM for maximum tokens-per-second.
- **CPU**: Ryzen 9 5900X serves as the fallback for ultra-large models that exceed VRAM.
- **Memory**: 64GB DDR4. Allows for concurrent running of multiple 7B/13B models.

## ⚙️ Configuration & API

- **Protocol**: HTTP/REST on Port `11434`.
- **Environment Variables**:
  - `OLLAMA_HOST`: `0.0.0.0` (Enables access from fleet robots over Tailscale).
  - `OLLAMA_ORIGINS`: `*` (Configured for local dev safety).
  - `OLLAMA_KEEP_ALIVE`: `1h` (Maintains models in VRAM for rapid agent response).

## 🏗️ Modelfile Standards
Every model deployed to the fleet must follow the **Sandra Modelfile** template:
- **System Prompt**: Materialist/Reductionist identity enforcement.
- **Temperature**: `0.1` (For technical precision) or `0.7` (For creative brainstorming).
- **Parameters**: `num_ctx: 32768` for large technical documents.

---
*Last updated: 2026-02-14*
