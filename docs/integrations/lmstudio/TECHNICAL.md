# LM Studio: Technical Specifications (0.4.0+, updated 2026-10-26)

## Hardware

- **GPU**: CUDA (NVIDIA) on RTX 4090. `lms runtime survey` prints GPU inventory; `lms runtime update llama.cpp` (and `mlx` on macOS) updates engines.
- **CPU offload**: Dynamic by VRAM. Keep ~2 GB headroom for KV cache + OS (Last Byte rule).
- **Model storage**: Check **My Models** tab for the active dir (fleet note: keep weights off near-full D:; prefer N:\AI drive per vLLM recipe).

## Endpoints

**Native REST v1** (`lms server start --port 1234`):

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/chat` | POST | Stateful chat. Returns `response_id` + `stats` (tokens in/out, tok/s, TTFT). Continue with `previous_response_id`. Accepts `integrations` (MCP), `context_length`. Streaming incl. model-load + prompt-processing events |
| `/api/v1/models` | GET | List |
| `/api/v1/models/load` | POST | Load (note: `model_instance_id` renamed to `instance_id` in 0.4.0) |
| `/api/v1/models/unload` | POST | Unload |
| `/api/v1/models/download` | POST | Download |
| `/api/v1/models/download/status` | GET | Download status |

**OpenAI-compat** (`baseURL http://localhost:1234/v1`): `/v1/models`, `/v1/responses` (also powers Codex), `/v1/decisions`, `/v1/chat/completions`, `/v1/embeddings`, `/v1/completions`.
**Anthropic-compat**: `/v1/messages` (Claude Code: `ANTHROPIC_BASE_URL=http://localhost:1234`, `ANTHROPIC_AUTH_TOKEN=lmstudio`).
**Jev-compat (TypeSafe AI)**: System One decisions endpoint.

Capability split: `/api/v1/chat` + `/v1/responses` support stateful chat + local/remote MCPs + load/prompt streaming events + per-request `context_length`. `/v1/chat/completions` + `/v1/messages` support custom tools + assistant-message passthrough but NOT MCP-via-API. Only `/api/v1/chat` supports per-request `context_length`.

## Auth

Permission keys (Settings > Server). Native: `Authorization: Bearer $LM_API_TOKEN`. Anthropic-compat accepts `x-api-key` or `Authorization: Bearer`.

## MCP via API (requires 0.4.0+, two server settings)

- Ephemeral per-request: `integrations: [{type: "ephemeral_mcp", server_label, server_url, allowed_tools?, headers?}]`. Requires "Allow per-request MCPs".
- Preconfigured: `integrations: ["mcp/playwright"]` from `mcp.json` (`%USERPROFILE%\.lmstudio\mcp.json` on Windows, `~/.lmstudio/mcp.json` elsewhere, Cursor-style notation). Requires "Allow calling servers from mcp.json".
- `allowed_tools` restricts tools (also trims prompt). Omit = all tools.

## Load options (0.4.0)

- **Max Concurrent Predictions**: N parallel requests via llama.cpp continuous batching (llama.cpp engine 2.0; MLX pending). Default parallel slots 4, Unified KV Cache on (no extra overhead claim). Beyond N queues.
- **Unified KV Cache**: Shared preallocation for varying request sizes (default on).
- **Idle TTL + auto-evict**: Auto-unload idle models after TTL (see Developer > core/ttl-and-auto-evict).
- **context_length**: Per-request on `/api/v1/chat` only.

## `lms` CLI (MIT, github.com/lmstudio-ai/lms)

`lms chat|get|ls|ps|load|unload|import` (models), `lms server start|stop|status`, `lms log stream`, `lms daemon up|down|status|update`, `lms link enable|disable|status`, `lms runtime`, `lms clone|push|dev|login`. `lms load --gpu=max|auto|0.0-1.0 --context-length=N [--identifier=name]`. `lms chat` has slash commands (/model, /download, /system-prompt, /help, /exit).

## SDKs

- TS: `npm install @lmstudio/sdk` (`LMStudioClient`, `client.llm.model("openai/gpt-oss-20b")`).
- Python: `pip install lmstudio` (`lms.Client()`, `client.llm.model(...)`).
- HTTP: any OpenAI/Anthropic client pointed at localhost.

---
Sources: lmstudio.ai/developers, /docs/developer, /docs/developer/rest, /docs/developer/core/mcp, /docs/cli, /blog/0.4.0. *Last updated: 2026-10-26. Prior: 2026-02-14.*
