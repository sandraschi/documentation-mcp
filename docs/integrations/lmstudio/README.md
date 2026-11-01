# LM Studio: Visual Model Discovery, Local Serving & Headless Daemon

LM Studio is the fleet's GUI + headless platform for discovering, downloading, and serving GGUF models on **Goliath** (RTX 4090 24 GB). As of **0.4.0 (2026-01-28)** it is no longer GUI-only: `llmster` is the same core as a standalone daemon for servers, cloud boxes, and CI.

## Role in the fleet (updated 2026-10-26)

- **Model discovery**: Browse Hub for latest experimental weights, one-click download.
- **Visual testing**: Real-time param tweaking (temperature, top-p, load options) with chat feedback, Split View, Developer Mode, in-app docs.
- **Headless serving**: `llmster` daemon (`lms daemon up`, `lms server start`) — no GUI dependency. Install: `curl -fsSL https://lmstudio.ai/install.sh | bash` (Mac/Linux) / `irm https://lmstudio.ai/install.ps1 | iex` (Windows).
- **Compat hub**: Native REST v1 (`/api/v1/*`) + OpenAI-compat (`/v1/chat/completions`, `/v1/responses`, `/v1/embeddings`) + Anthropic-compat (`/v1/messages`) + Jev-compat. Drop-in `baseURL` swap for Ollama paths.
- **MCP client + MCP via API**: `~/.lmstudio/mcp.json` for interactive chat; `/api/v1/chat` and `/v1/responses` accept `integrations` (ephemeral `ephemeral_mcp` per-request or preconfigured `mcp/<id>`) with `allowed_tools` + custom `headers`.

## Docs in this folder

- [TECHNICAL.md](TECHNICAL.md): Endpoints, auth, streaming events, parallel requests, TTL, `lms` CLI.
- [WORKFLOWS.md](WORKFLOWS.md): Daemon deploy, stateful chat, per-request MCP, server automation.
- Fleet doctrine: `standards/LOCAL_LLM_STANDARDS.md` (engine comparison), `standards/LOCAL_LLM_FIRST_DOCTRINE.md` (lineup), `standards/TOOLING_COST_MODEL.md` (tooling ladder).

## Key constraint (unchanged)

Single-writer VRAM on the shared 4090. Do NOT co-run a resident LM Studio model with Ollama/vLLM/ComfyUI — one will OOM or spill to DDR5. Probe (`lms ps` / `GET /api/ps` on Ollama side), evict before switching. See `standards/LOCAL_LLM_STANDARDS.md` eviction protocol.

---
*Last updated: 2026-10-26 (0.4.0: llmster, parallel requests, /api/v1/chat stateful + MCP, OpenAI/Anthropic compat). Prior: 2026-02-14.*
