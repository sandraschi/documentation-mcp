# Local LLM MCP Server

**Optional fleet LLM control plane** — portmanteau MCP tools for local (Ollama, LM Studio) and cloud providers, plus web dashboard at 10832/10833.

## Role

This is NOT the default fleet inference path. Most fleet MCPs set `*_SAMPLING_BASE_URL=http://127.0.0.1:11434/v1` and call Ollama directly. This repo provides a centralized surface when you need multi-provider management.

## Status (2026-06)

| Component | State |
|-----------|-------|
| Server boot + tool registration | Working; failed modules skip gracefully |
| Ollama / LM Studio / cloud APIs | Usable with configured URLs/keys |
| Dashboard | Working — provider status, GPU telemetry, .env editing |
| VLLMv1Provider | Fixed (abstract methods) |
| Tauri NSIS | Scaffold exists at native/ |

## Ports

- Frontend: 10832
- API: 10833

## Tools

Portmanteau pattern: `llm_health`, `llm_models`, `llm_generation`, `llm_multimodal`, `llm_finetuning`, plus provider-specific (`llm_ollama`, `llm_lmstudio`, `llm_vllm`).

## Related

- [Project page](../../local-llm-mcp/README.md)
- [Fleet port registry](../../../operations/WEBAPP_PORTS.md)