# Install

```powershell
uv sync
```

## Quick Start

```powershell
# Full stack (backend + frontend dashboard)
.\start.bat

# Stdio only (Claude Desktop / opencode)
uv run python -m fleet_public_relations_mcp.server

# HTTP mode (REST API + MCP)
uv run uvicorn fleet_public_relations_mcp.api:app --port 11094

# Frontend dev (requires npm install in webapp/)
cd webapp && npm install && npm run dev
```

## Requirements

- Python 3.11+
- uv (https://docs.astral.sh/uv/)
- Node.js + npm (for webapp dashboard)
- Ollama or OpenAI-compatible endpoint for LLM evaluator
