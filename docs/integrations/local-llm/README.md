# Local LLM: Unified Inference Environment

This documentation covers the consolidated local-first neural ecosystem of the Sandra workstation, centered around the **Local LLM MCP Orchestration Hub**.

## 🏛️ Ecosystem Overview

The fleet utilizes a tiered inference strategy managed by a central **Model Orchestration Dashboard**:
- **Ollama**: Lightweight management and high-precision technical inference.
- **LM Studio**: Visual playground and model discovery hub.
- **vLLM**: Performance-critical distributed serving (RTX 4090 Optimized).

## 📂 Multi-File Documentation

- [Local LLM MCP Server (HUB)](local-llm-mcp.md): The industrial-grade agentic control layer and visual orchestration dashboard (`:10832`).
- **Individual Application Specs**:
  - [Ollama Integration](../ollama/README.md)
  - [LM Studio Integration](../lmstudio/README.md)
  - [vLLM Integration](../vllm/README.md)

---
*Maintained by: Antigravity AI (SOTA v14.1 Compliance)*
*Last updated: 2026-04-15*
