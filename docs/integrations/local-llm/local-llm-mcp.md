# Local LLM MCP: Fleet Orchestration Hub

The Local LLM MCP server serves as the **industrial-grade orchestration hub** for managing and querying inference engines across the local ecosystem. It acts as both a JSON-RPC gateway and a premium visual dashboard for fleet-wide monitoring.

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

## 🛠️ Portmanteau Edge Tools

The server utilizes the **SOTA Portmanteau Pattern** to consolidate individual operations into unified interfaces:

| Tool | Action | Orchestration Role |
| :--- | :--- | :--- |
| `llm_health` | Monitoring | Central telemetry and engine heartbeat for the ecosystem. |
| `llm_models` | Inventory | Consolidated registry of all available weights across vendors. |
| `llm_generation` | Inference | Industrial-grade text and chat generation API. |
| `llm_multimodal` | Vision | Unified vision analysis for all supporting local/cloud backends. |

## 🖥️ SOTA Orchestration Dashboard

This server provides a premium **Model Orchestration Dashboard** (Vite/React) on dedicated ports:

- **Frontend**: `10832`
- **Config API**: `10833`

### Key Modules:
- **Fleet Launcher**: Cross-service navigation for the entire workstation (Blender, Robotics, etc.).
- **Live Config Engine**: Browser-based management for `.env` credentials and endpoints.
- **Resource Analytics**: Real-time GPU and VRAM telemetry.

## 📊 Interaction Principles

- **Hub Pattern**: The server acts as a central control plane. Other MCP services (e.g., Robotics, Plex) frequently use this hub as their primary inference backend.
- **Persistence Layer**: Configuration changes made via the UI are persisted directly to the backend filesystem.
- **Failover Logic**: Automatic routing to secondary engines (Ollama/LM Studio) if primary high-performance vLLM instances are busy.

---
*Last updated: 2026-04-15*
