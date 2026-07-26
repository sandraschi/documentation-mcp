# V-Bot Mind — Autonomous Virtual Robot Brain

**V-Bot Mind MCP** is the fleet's autonomous virtual robot brain runtime. It sits between
game engines (Godot, Unity3D, Resonite) and LLM inference, providing:

- **Perception ingestion**: Feed what the V-Bot sees/hears
- **LLM-driven reasoning**: Autonomous decision-making via Ollama/LM Studio
- **Episodic memory**: Persistent recall of past interactions
- **Personality engine**: Configurable traits, goals, backstory
- **Motor output**: Structured action commands back to the engine
- **Multi-bot registry**: Manage dozens of V-Bots with individual identities

## Quick Start

```bash
uv sync
start.ps1   # launches backend (11078) + frontend dashboard (11079)
```

## MCP Client Config

```json
{
  "mcpServers": {
    "vbot-mind": {
      "command": "uv",
      "args": ["run", "python", "-m", "vbot_mind.mcp.server", "--http", "--port", "11078"],
      "env": {
        "VBOT_MIND_LLM_BASE_URL": "http://127.0.0.1:11434/v1",
        "VBOT_MIND_LLM_MODEL": "qwen2.5:7b"
      }
    }
  }
}
```

## Core Tools

| Tool | Purpose |
|------|---------|
| `vbot_mind` | Full V-Bot lifecycle: create, perceive, think, act, remember, chat, configure, delete |
| `vbot_agentic_workflow` | Multi-step autonomous goal pursuit with sampling |

## Architecture

```
Game Engine (Godot/Unity3D/Resonite)
    │
    │ perception (what the bot sees)
    ▼
V-Bot Mind MCP  ──►  LLM (Ollama / LM Studio)
    │                    │
    │ motor commands     │ reasoning
    ▼                    │
Game Engine  ◄───────────┘
```

## Fleet Integration

- Feeds from `godot-mcp`, `unity3d-mcp`, `resonite-mcp` for world state
- Uses `local-llm-mcp` for inference provider discovery
- Integrates with `advanced-memory-mcp` for long-term knowledge (Phase 2)
- Consumed by `teleoperator-mcp` for VR interaction with V-Bots
