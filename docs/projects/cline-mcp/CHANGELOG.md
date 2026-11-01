# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-07

### Added
- **Webapp (Agent Console)**: fleet-standard React + Vite + Tailwind console (`web_sota/`) — Overview (KPIs + LLM provider probes), Agents (start/abort real sessions with live events), Schedules (cron CRUD), AI Chat (local LLM), Tools (live MCP tool list), System Logs, Settings, Help. Ports 11102 (FE) / 11103 (BE).
- **HTTP backend mode**: `CLINE_MCP_HTTP_PORT` starts express REST (`/api/v1/health|tools|logs|agents/sessions|schedules`), fleet CORS, in-memory log ring buffer; shares `handleTool()` with the stdio MCP server.
- **Start scripts**: `start.ps1` / `start.bat` / `fleet-start.config.ps1` (fleet engine).

### Changed
- **Bumped `@cline/sdk` 0.0.60 → 0.0.71** (Agent runtime: run/abort/subscribe/snapshot).
- `agent_team_run`: real coordinator plans subtasks → N sub-agents execute in parallel (was placeholder strings).
- `agent_schedule_*`: real `node-cron` execution + disk persistence in `CLINE_MCP_DATA_DIR` (was in-memory no-op); cron re-attached on restart.
- `agent_session_stop`: real `agent.abort()` (was status flag only); status streams live agent events.
- Fix: stdio process exits on stdin EOF (cron timers kept the event loop alive → zombie).
- README: full tools/providers/schedules/webapp documentation.

### Verified
- `agent_run` on local Ollama (`qwen3.6:latest`) → `completed` / `PONG`; schedule create/list/delete round-trip; webapp walked end-to-end in browser (zero console errors); tsc + biome + production build clean.

## [0.1.0] - 2026-07-14

### Added
- Initial MCP server wrapping the Cline SDK: `agent_run`, sessions (start/status/stop/list), schedules (create/list/delete), `agent_team_run`, `help`.
