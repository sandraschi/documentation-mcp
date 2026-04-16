# kyutai-mcp 🎤

[![FastMCP](https://img.shields.io/badge/FastMCP-3.1+-blue)](https://github.com/jlowin/fastmcp)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](#)

> **Voice Pipeline MCP Server** — Real-time speech orchestration with Kyutai Moshi, persona-aware proxy, and agentic briefings.

**Repo**: [D:/Dev/repos/kyutai-mcp](file:///D:/Dev/repos/kyutai-mcp)
**Version**: 0.2.0
**Framework**: FastMCP 3.1+
**Changelog**: [CHANGELOG.md](file:///D:/Dev/repos/kyutai-mcp/CHANGELOG.md)

---

## Overview

kyutai-mcp wraps [Kyutai Moshi](https://github.com/kyutai-labs/moshi) — a real-time, full-duplex speech foundation model — into a fleet-standard MCP server with a staged voice pipeline, persona-aware WebSocket proxy, and premium SOTA webapp.

### Architecture

```
MCP Client / Agent
    │
    ├─► voice_pipeline (10 operations)
    │   ├─ turn / speak_boilerplate          ← staged LLM pipeline
    │   ├─ service_status/start/stop         ← Moshi process supervisor
    │   ├─ session_history                   ← turn replay
    │   └─ proxy_status/start/stop/transcript ← persona proxy control
    │
    ├─► moshi_ops (4 operations)
    │   ├─ status / local_viability
    │   └─ references / recommend_runtime
    │
    └─► Persona Proxy (port 8999)
        Client ──WS──► Proxy ──WS──► Moshi (8998)
                         │
                         ├─ relay audio (transparent)
                         ├─ tap 0x02 text tokens → transcript
                         └─ persona callback → local LLM → inject
```

---

## Ports

| Service | Port | Type |
|---------|------|------|
| Backend (FastAPI) | **10924** | REST API |
| Frontend (Vite) | **10925** | Webapp |
| MCP (HTTP) | **10926** | MCP transport |
| Moshi (upstream) | **8998** | WebSocket |
| Persona Proxy | **8999** | WebSocket |

---

## MCP Tools

### `voice_pipeline` — Voice orchestration portmanteau

| Operation | Description |
|-----------|-------------|
| `turn` | Staged voice turn: quick-ack → intent → research → deep synthesis |
| `speak_boilerplate` | Agentic briefing: weather, world_news, ai_news, stock_market |
| `service_status` | Check Moshi process + HTTP health probe |
| `service_start` | Start supervised Moshi process |
| `service_stop` | Stop Moshi process |
| `session_history` | List sessions or replay turns |
| `proxy_status` | Check persona proxy health |
| `proxy_start` | Launch proxy on port 8999 |
| `proxy_stop` | Stop persona proxy |
| `proxy_transcript` | Fetch captured transcript from proxy session |

### `moshi_ops` — Hardware & runtime advisory

| Operation | Description |
|-----------|-------------|
| `status` | Server and Moshi-oriented status |
| `local_viability` | Environment hints for local runs |
| `references` | Pointers to upstream docs/repos |
| `recommend_runtime` | Runtime guidance (GPU, VRAM, drivers) |

---

## Persona Proxy

The WebSocket proxy sits transparently between clients and Moshi:

1. **Audio pass-through** — All `0x01` audio frames relay unmodified (zero latency impact).
2. **Text token tapping** — Moshi's inner monologue `0x02` tokens are captured into per-session transcripts.
3. **Persona injection** — When `?persona=<system_prompt>` query param is set, each sentence boundary triggers a local LLM call (Glom-On: Ollama/LM Studio). The augmented response is injected back as a `0x02` text annotation.
4. **Rate limiting** — Persona callbacks are throttled to 1 per 5 seconds to prevent flooding.

---

## Voice Pipeline Stages

```
User utterance
    │
    ├─ 1. Quick Ack (fast local model, <200ms)
    │
    ├─ 2. Intent Resolution
    │      weather │ world_news │ ai_news │ stock_market │ general
    │
    ├─ 3. Agentic Research (for data-heavy intents)
    │      Open-Meteo │ BBC RSS │ AI News RSS │ Yahoo Finance
    │
    ├─ 4. Deep Reasoner Synthesis (spoken final answer)
    │
    └─ 5. TTS-ready output
```

---

## Glom-On (Local LLM)

Auto-discovers local providers:

| Provider | Probe URL | Condition |
|----------|-----------|-----------|
| Ollama | `http://127.0.0.1:11434/api/tags` | HTTP 200, non-empty `models` |
| LM Studio | `http://127.0.0.1:1234/v1/models` | HTTP 200, `data` array |

Routing: `provider=auto` picks Ollama if healthy, else LM Studio.

---

## Robofang Integration

kyutai-mcp is registered as the **Kyutai Voice Hand** in the Robofang fleet:

- **Fleet manifest**: potassium score 9.5
- **Bridge**: `robofang_voice` MCP tool → REST relay to `http://127.0.0.1:10924`
- **Operations**: speak, status, start_service, stop_service

---

## Quick Start

```powershell
# Clone and install
cd D:\Dev\repos\kyutai-mcp
uv sync

# Start webapp (backend + frontend)
cd webapp
powershell -ExecutionPolicy Bypass -File .\start.ps1

# MCP stdio transport
uv run python -m kyutai_mcp
```

### Client wiring

**Stdio:**
```json
{
  "mcpServers": {
    "kyutai-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/kyutai-mcp", "run", "python", "-m", "kyutai_mcp"]
    }
  }
}
```

**HTTP:** `http://127.0.0.1:10926/mcp`

---

## Discovery

- **Catalog**: `GET /api/mcp/catalog`
- **Glama**: `glama.json` at repo root; `GET /api/discovery/glama`
- **Well-known**: `GET /.well-known/mcp/manifest.json`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KYUTAI_BACKEND_URL` | `http://127.0.0.1:10924` | Backend REST API |
| `MOSHI_WS_URL` | `ws://127.0.0.1:8998/api/chat` | Upstream Moshi WebSocket |
| `MOSHI_PROXY_HOST` | `127.0.0.1` | Proxy bind host |
| `MOSHI_PROXY_PORT` | `8999` | Proxy bind port |

---

## Known Limitations

- **GPU scheduling**: Moshi and Ollama compete for VRAM on single-GPU systems. Future: resource scheduler.
- **Windows support**: Upstream Moshi lacks official Windows support (requires working `nvcc`/Rust).
- **In-memory state**: Sessions and transcripts are in-memory; restart clears history.

---

## Documentation

| Document | Description |
|----------|-------------|
| [MCP.md](file:///D:/Dev/repos/kyutai-mcp/docs/MCP.md) | FastMCP server, tools, discovery |
| [VOICE_WORKFLOWS.md](file:///D:/Dev/repos/kyutai-mcp/docs/VOICE_WORKFLOWS.md) | Staged voice pipeline, persona proxy |
| [MOSHI_SERVICE.md](file:///D:/Dev/repos/kyutai-mcp/docs/MOSHI_SERVICE.md) | Upstream Moshi configuration |
| [GLOM.md](file:///D:/Dev/repos/kyutai-mcp/docs/GLOM.md) | Local LLM integration |
| [WEBAPP.md](file:///D:/Dev/repos/kyutai-mcp/docs/WEBAPP.md) | Frontend/backend layout |
| [CHANGELOG.md](file:///D:/Dev/repos/kyutai-mcp/CHANGELOG.md) | Version history |
