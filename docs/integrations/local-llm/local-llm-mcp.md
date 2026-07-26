# Local LLM MCP: Optional LLM Hub

The Local LLM MCP server provides centralized MCP tools for managing LLM providers (Ollama, LM Studio, cloud). It also includes a web dashboard for provider configuration and GPU telemetry.

Most fleet MCPs call Ollama directly via `*_SAMPLING_BASE_URL` — this repo is for when you need a unified multi-provider surface.

## 🚀 Server Registration

```json
{
  "local-llm": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/local-llm-mcp", "run", "llm-mcp"],
    "env": {
      "PROVIDERS__OLLAMA_BASE_URL": "http://localhost:11434",
      "PROVIDERS__VLLM_BASE_URL": "http://localhost:8000/v1"
    }
  }
}
```

## Portmanteau Tools

The server utilizes the **SOTA Portmanteau Pattern** to consolidate individual operations into unified interfaces:

| Tool | Action | Orchestration Role |
| :--- | :--- | :--- |
| `llm_health` | Monitoring | Central telemetry and engine heartbeat for the ecosystem. |
| `llm_models` | Inventory | Consolidated registry of all available weights across vendors. |
| `llm_generation` | Inference | Industrial-grade text and chat generation API. |
| `llm_multimodal` | Vision | Unified vision analysis for all supporting local/cloud backends. |

## SOTA Dashboard

This server provides a premium **Model Orchestration Dashboard** (Vite/React) on dedicated ports:

- **Frontend**: `10832`
- **Config API**: `10833`

### Key Modules:
- **Fleet Launcher**: Cross-service navigation for the entire workstation (Blender, Robotics, etc.).
- **Live Config Engine**: Browser-based management for `.env` credentials and endpoints.
- **Resource Analytics**: Real-time GPU and VRAM telemetry.

## Interaction Principles

- **Hub Pattern**: The server provides a central control plane for multi-provider LLM ops. Most fleet MCPs bypass this hub and call Ollama directly via `*_SAMPLING_BASE_URL`.
- **Persistence Layer**: Configuration changes made via the UI are persisted directly to the backend filesystem.
- **Dashboard**: Port 10832 (Vite React) proxies to port 10833 (FastAPI REST).

---
*Last updated: 2026-04-15*
