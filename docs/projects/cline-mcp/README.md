# cline-mcp

MCP server wrapping the **Cline SDK** (`@cline/sdk` 0.0.71) — run agents, manage abortable sessions, schedule cron tasks, coordinate multi-agent teams. A thin, honest bridge: everything advertised actually executes.

## Quick Start

```bash
npm install
npm run build          # required after clone — dist/ is gitignored
node dist/index.js     # stdio mode
```

`just build` / `just serve` / `just check` also work.

## Tools

| Tool | Description | Real? |
|------|-------------|-------|
| `agent_run` | One-shot agent execution (anthropic / openai / ollama / lmstudio) | ✅ executes via SDK `Agent.run()` |
| `agent_session_start` | Start persistent background session | ✅ real agent, progress events captured |
| `agent_session_status` | Live status + last agent event + output | ✅ via `agent.subscribe()` / snapshot |
| `agent_session_stop` | Abort a running session | ✅ real `agent.abort()` |
| `agent_session_list` | List sessions | ✅ |
| `agent_schedule_create` | Real cron schedule | ✅ fires real agent runs (`node-cron`), persisted to disk |
| `agent_schedule_list` | List schedules + last run/output/error | ✅ |
| `agent_schedule_delete` | Delete schedule | ✅ stops the cron job |
| `agent_team_run` | Multi-agent team: coordinator plans → N sub-agents execute in parallel | ✅ real coordinator + parallel sub-agent runs |
| `help` | Usage reference | ✅ |

## Env Vars

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | API key for Anthropic (default provider) |
| `OPENAI_API_KEY` | — | API key for OpenAI (`provider=openai`) |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Local Ollama endpoint (`provider=ollama`) |
| `OLLAMA_DEFAULT_MODEL` | `muse-glimmer` | Default model for `provider=ollama` (SFB brain tier) |
| `CLINE_MCP_DEFAULT_PROVIDER` | `ollama` | Default provider when none is passed (set to `anthropic` to restore previous behavior) |
| `CLINE_MCP_PORT` | `11096` | HTTP server port (reserved) |
| `CLINE_MCP_DATA_DIR` | `%APPDATA%\cline-mcp` (win) / `~/.config/cline-mcp` | Schedule persistence directory |

## Providers

- `anthropic` (set `CLINE_MCP_DEFAULT_PROVIDER=anthropic` to make this the default again) — `claude-sonnet-4-6`, needs `ANTHROPIC_API_KEY`
- `openai` — needs `OPENAI_API_KEY`
- `ollama` (default) — local, no key (default model `muse-glimmer`, override with `model=` or `OLLAMA_DEFAULT_MODEL`)
- `lmstudio` — local OpenAI-compatible (`http://localhost:1234`)

## Schedule persistence

Schedules survive restarts — stored as JSON in `CLINE_MCP_DATA_DIR/schedules.json`, cron jobs are re-attached on startup. Sessions are in-memory (server lifetime).

## Example

```bash
# One-shot on local Ollama
{"name":"agent_run","arguments":{"prompt":"Summarize the repo","provider":"ollama","model":"qwen3.6:latest"}}

# Recurring morning digest at 09:00 Mon-Fri
{"name":"agent_schedule_create","arguments":{"name":"morning-digest","cron":"0 9 * * 1-5","prompt":"Write the daily fleet digest","provider":"ollama"}}

# Team: coordinator plans, 3 sub-agents execute in parallel
{"name":"agent_team_run","arguments":{"goal":"Audit the webapp for dead buttons","agents":3,"provider":"ollama"}}
```

## Webapp (Agent Console)

A fleet-standard React + Vite + Tailwind console at `web_sota/` (dark theme, 8 pages).

| Port | Service |
|------|---------|
| 11102 | Webapp frontend (Vite dev) |
| 11103 | Webapp backend (Node REST + agent runtime, `CLINE_MCP_HTTP_PORT`) |
| 11096 | MCP stdio (`CLINE_MCP_PORT`, reserved) |

Start the whole stack with `start.bat` / `./start.ps1` (fleet engine, builds dist if missing) or:

```bash
# backend (HTTP mode)
$env:CLINE_MCP_HTTP_PORT = "11103"; node dist/index.js
# frontend (separate terminal)
cd web_sota && bun install && bun run dev
```

Pages: **Overview** (health KPIs, provider detection), **Agents** (start/abort real sessions, live events), **Schedules** (cron CRUD), **AI Chat** (local LLM), **Tools** (live MCP tool list), **System Logs** (ring buffer), **Settings** (LLM probes, env reference), **Help**.

REST API: `GET /api/v1/health`, `/tools`, `/logs`, `/agents/sessions` (GET/POST/DELETE), `/schedules` (GET/POST/DELETE). Fleet CORS enabled (dev origin + Tauri WebView + Tailscale/LAN).

## Stack

- **Runtime**: Node.js 22+ / TypeScript
- **SDK**: `@cline/sdk` 0.0.71 (agent runtime, abort, events)
- **Cron**: `node-cron`
- **MCP**: `@modelcontextprotocol/sdk` (stdio transport)
