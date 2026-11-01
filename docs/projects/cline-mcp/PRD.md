# cline-mcp — Product Requirements

## Purpose

Bridge the **Cline SDK** (`@cline/sdk`) into the fleet: expose Cline's agent runtime as MCP
tools (one-shot runs, persistent sessions, cron schedules, multi-agent teams) so any MCP
client — opencode, Claude Desktop, Cursor — can drive Cline agents. A webapp console
provides monitoring and management for the HTTP backend mode.

## Why Cline?

Cline is one of the largest autonomous coding-agent projects (65k+ stars, daily releases
across extension/CLI/SDK/Desktop). Its SDK gives a stable, browser-safe agent runtime with
run/abort/events — a real integration surface. The fleet already operates opencode as its
primary agent; cline-mcp is the *integration bridge* for cases where Cline-specific
capabilities add value (cron-scheduled agents, persistent background sessions, team runs).

## Architecture

- **Single Node process, two modes**: stdio (MCP clients) or HTTP (`CLINE_MCP_HTTP_PORT`).
  Both share `handleTool()` — one implementation, two surfaces.
- **Agent runtime**: `@cline/agents` `Agent` (run, abort, subscribe, snapshot).
- **Sessions**: in-memory map; real abort via `agent.abort()`; live events via `subscribe()`.
- **Schedules**: `node-cron` jobs; definitions persisted to `CLINE_MCP_DATA_DIR/schedules.json`,
  re-attached on restart.
- **Teams**: coordinator agent plans subtasks → N sub-agents execute in parallel → aggregated.
- **Webapp**: React + Vite + Tailwind (bun), dark fleet theme, AppLayout with 8 pages,
  REST proxy to the HTTP backend.

## Shipped Features (v0.2.0)

- 10 MCP tools, all real (no stubs) — verified live against local Ollama.
- HTTP REST backend (`/api/v1/*`): health, tools, logs, sessions, schedules; fleet CORS.
- Webapp console: Overview, Agents, Schedules, AI Chat, Tools, Logs, Settings, Help.
- Start scripts (fleet engine), port registry (11102/11103/11096), README/llms docs.

## Non-Goals

- Not a Cline Desktop-for-Windows rebuild (macOS-only upstream app; Windows surfaces are
  the CLI + extension + this wrapper).
- No full `AgentTeamsRuntime` host integration (SDK team machinery is host-bound); the
  wrapper uses runtime-level coordinator + parallel sub-agents.
- No session persistence across restarts (in-memory by design; schedules persist).

## Future Candidates

- Session persistence to disk (JSON/SQLite) mirroring schedules.
- `cline` CLI (`--zen` hub / ACP) integration as an alternative backend.
- Tauri wrapper for the webapp (fleet NSIS pattern) when a desktop surface is wanted.
