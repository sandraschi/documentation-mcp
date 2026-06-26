---
project: openclaude-mcp
status: active
priority: high
tags: [openclaude, kairos, ollama, local-llm, claude-code-leak, fastmcp, mcp, sse-push, docker]
created: 2026-04-05
updated: 2026-05-02
ports: [10932, 10933]
repo: D:\Dev\repos\openclaude-mcp
---

# openclaude-mcp

MCP control plane for running OpenClaude (Claude Code harness) against local Ollama models.
Zero cloud token cost. 24/7 on RTX 4090. Full KAIROS autoDream support.
SSE push, session persistence, Docker Compose, ULTRAPLAN e2e tests, multimodal, usage analytics, KAIROS state persistence.

## Status

`active — v0.2.2: 15 tools, 81 tests, interactive examples, API reference`

| Component | Status |
|---|---|
| FastMCP 3.2 server | done — SSE + REST bridge + Prefab UI + auth middleware |
| Model router | done — Ollama health, VRAM metadata, 6 models, defaults persisted |
| Session management | done — subprocess lifecycle, NDJSON protocol, env whitelist |
| Session persistence | done — JSON store, restart-safe, stale PID cleanup |
| Usage analytics | done — per-session prompt/output/estimated token counters |
| KAIROS daemon | done — FileLock, abort-on-activity, configurable interval + budget, state persisted |
| Webapp (React) | done — SSE push, xterm.js, 9 pages, interactive examples playground |
| Multimodal input | done — send_multimodal tool, base64 images, 3 formats |
| ULTRAPLAN | done — configurable model, token tracking, 5 e2e tests |
| SSE push | done — GET /api/events, asyncio.Queue broadcast |
| Interactive examples page | done — live Run buttons, response JSON, timing, session walkthrough |
| API reference page | done — searchable, 15 tool params/returns, env vars, error codes |
| Docker Compose | done — ollama + mcp + webapp (nginx) |
| CI/CD | done — GitHub Actions (ruff + pytest) |
| Caregiver alerts | done — persistent file + webhook delivery |
| Bun install safety | done — no shell=True, httpx download + verify |

## Architecture

```
openclaude-mcp/
├── server.py                       FastMCP 3.2 — 15 tools, auth, SSE push, lifespan
├── docker-compose.yml              Full stack (ollama + mcp + webapp)
├── openclaude/
│   ├── model_router.py             Ollama health + model metadata + default persistence
│   ├── session.py                  Subprocess lifecycle + NDJSON + usage analytics + multimodal
│   ├── kairos.py                   autoDream daemon + configurable budget + state persistence
│   ├── session_persistence.py      JSON store + stale PID cleanup + KAIROS state save/load
│   └── logging_util.py             Centralized log handler
├── webapp/
│   └── src/
│       ├── api.ts                  REST client + SSE EventSource subscription
│       ├── store.ts                Zustand store — SSE-powered state updates
│       └── pages/
│           ├── Dashboard.tsx       Stats, default model, quick actions
│           ├── Sessions.tsx        Session management + prompt + xterm.js
│           ├── Models.tsx          Model cards with VRAM/speed/license
│           ├── Kairos.tsx          Per-session KAIROS toggle + log viewer
│           ├── Examples.tsx        Interactive playground with live Run buttons
│           ├── LoggerPage.tsx      Real-time unified system log stream
│           ├── HelpPage.tsx        Searchable API reference — 15 tools, params, returns, env vars, errors
│           └── SettingsPage.tsx    Backend config, Desktop snippet, legal
├── start.ps1 / start.bat           Port clearing, uv sync, health gate
├── tests/
│   ├── unit/                       41 tests (fast, no external deps)
│   ├── smoke/                      11 tests (server import + REST ping)
│   ├── integration/                18 tests (REST bridge)
│   └── e2e/                        11 tests (ULTRAPLAN + full session with respx mock)
└── .github/workflows/ci.yml        Ruff + pytest on push/PR
```

## Ports

| Service | Port | Protocol |
|---|---|---|
| MCP SSE (FastMCP 3.2) | 10932 | SSE |
| REST bridge | 10932 | HTTP JSON |
| SSE push (webapp events) | 10932 | SSE |
| React webapp (Vite / nginx) | 10933 | HTTP |
| Ollama | 11434 | HTTP |

## FastMCP 3.2 Features Used

- `lifespan` context manager — startup Ollama check, session persistence, graceful shutdown
- `mcp.http_app(path="/sse")` — ASGI mount for SSE transport
- `@mcp.tool(app=True)` — `fleet_dashboard` Prefab UI tool
- `PrefabApp` DSL — `Badge`, `Column`, `Row`, `Table`, `Text`
- `Context | None` pattern — tools work from both MCP and REST calls

## Model Recommendations (RTX 4090, 24 GB VRAM)

| Model | Tag | Active Params | VRAM @ Q4 | Speed | Context | Multimodal |
|---|---|---|---|---|---|---|
| **Gemma 4 12B** ⭐ | `gemma4:12b` | 12B dense | ~10–14 GB | Strong on 4090 | 256K | **Text + image** (encoder-free) |
| Gemma 4 26B (heavy) | `gemma4:26b` | 26B MoE | ~17 GB | 40-60 tok/s | 256K | Agentic; heavy VRAM |
| Gemma 4 E4B (edge) | `gemma4:e4b` | ~4B eff. | ~5 GB on **Pi 5 16G** | CPU/GPU | 128K+ | **Text + image + audio** |
| Gemma 4 E2B (edge light) | `gemma4:e2b` | ~2B eff. | &lt;1.5 GB on **Pi 5 16G** | CPU | 128K+ | **Multimodal**, ROS-friendly |
| Qwen2.5-Coder 32B | `qwen2.5-coder:32b-instruct-q4_K_M` | 32B | ~19 GB | 30-40 tok/s | 128K | Text only |
| DeepSeek R1 32B | `deepseek-r1:32b` | 32B | ~19 GB | 25-35 tok/s | 64K | Text only |
| Qwen3.5 35B-A3B MoE | `qwen3.5:35b-a3b` | 3B | ~8.5 GB | 112 tok/s | 128K | Text only |
| Qwen3.5 27B Dense | `qwen3.5:27b` | 27B | ~15 GB | 40 tok/s | 128K | Text only |
| Llama 3.1 8B | `llama3.1:8b` | 8B | ~5 GB | 80-100 tok/s | 128K | Text only |

Default: `gemma4:12b`. Apache-2.0, **multimodal** (images in-chat), best **shared-4090** tradeoff. On **Pi 5 16 GB** use `gemma4:e4b` or `gemma4:e2b` for multimodal edge. Use `gemma4:26b` only when the GPU is dedicated to inference.

## ULTRAPLAN

Cloud planning + local execution. Requires `ANTHROPIC_API_KEY`.

Flow:
1. Call `ultraplan(session_id, goal)` from MCP client or webapp
2. Server calls configurable Anthropic model (`OPENCLAUDE_ULTRAPLAN_MODEL`, default `claude-sonnet-4-6`) with 30-min timeout
3. Plan (up to 8192 tokens) returned with token usage tracking
4. Plan fed into local session for step-by-step execution — zero additional cloud cost
5. Error handling: timeouts, connection errors, HTTP errors all return structured responses

E2e tested with `respx`-mocked Anthropic API (no real API key needed).

## Security / Hardening

- **REST auth**: Optional token-based (`OPENCLAUDE_MCP_TOKEN`) via `AuthMiddleware`
- **Subprocess isolation**: `create_subprocess_exec` (no shell), env whitelist, separate stderr
- **Bun install**: Downloads installer script via `httpx.get()`, no `iex` pipe
- **Caregiver alerts**: Persistent log file + optional webhook for kid-safe mode
- **CI/CD**: Ruff lint + pytest on every push

## Quick Start

```powershell
# Native
.\setup.ps1
.\start.ps1
open at http://localhost:10933

# Docker
docker compose up
open at http://localhost:10933
```

## Test Suite

```powershell
uv run pytest                    # 79 tests
uv run pytest tests/unit/        # 41 fast unit tests
uv run pytest -m smoke           # 11 smoke tests
uv run pytest -m integration     # 18 integration tests
uv run pytest -m e2e             # 5 ULTRAPLAN e2e tests (mocked)
```

## Key Files

| File | Purpose |
|---|---|
| `server.py` | FastMCP entry point + REST bridge + SSE push |
| `openclaude/session.py` | Subprocess lifecycle, NDJSON protocol |
| `openclaude/kairos.py` | autoDream daemon |
| `openclaude/model_router.py` | Model registry + default persistence |
| `openclaude/session_persistence.py` | JSON session store |
| `Dockerfile` | UV-based Python container image |
| `docker-compose.yml` | Full stack orchestration |
| `.github/workflows/ci.yml` | CI/CD pipeline |

## Related Projects

- `reversing-mcp` — Ghidra AI-assisted reverse engineering (active)
- `meta-mcp` — fleet health monitoring (active)
- `mcp-federation-hub` — 80+ server orchestration (active)
