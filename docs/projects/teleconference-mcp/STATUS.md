# Teleconference MCP — Status Report

**Last Updated:** 2026-07-13
**Status:** Active Development (SOTA 2026)
**Version:** 0.1.0
**Source Repo:** `D:\Dev\repos\teleconference-mcp`

---

## Overview

Self-hosted video conferencing platform with AI voice agent ("Visio"), built on LiveKit and Turborepo. Targets development teams requiring on-premises, privacy-respecting conferencing with intelligent voice assistance, remote desktop, and RAG memory.

---

## Health Summary

| Component | Status | Port | Notes |
|-----------|--------|------|-------|
| Web Dashboard | Healthy | 10886 | Next.js 16, TailwindCSS 4 |
| Conferencing MCP | Healthy | 10720 | FastMCP 3.2, 25 tools split into 5 modules (diagnostics/signaling/intelligence/conferences/rooms) |
| Remoting MCP | Healthy | 10725 | FastMCP 3.2, 8 tools with Context injection, screen capture + input injection |
| AI Agent | Conditional | 10887 | Requires Ollama + gemma2 |
| LiveKit Server | Healthy | 15580 | Docker, WebRTC SFU |
| Redis | Healthy | 16379 | Docker, state bus + pub/sub |

---

## Implemented Features

### Web Application (10886)
- Multi-room conferencing with grid/focus layout + screen share auto-focus
- Screen sharing via `getDisplayMedia` → LiveKit `publishTrack`
- Background blur via `@livekit/track-processors` `BackgroundBlur`
- Meeting recording via LiveKit Egress API (`/api/egress`)
- Meeting Intelligence Panel — AI summaries/action items with LanceDB persistence
- Real-time transcription (3 data sources: native, data channel, metadata)
- Chat panel via LiveKit `useChat`
- Device test page (`/test`) with live preview + audio levels
- Scheduling UI (`/meetings`) — create, list, upcoming/past, copy invite link
- Settings: devices, theme (dark/light/system), telemetry, Ollama model mgmt
- Health dashboard (`/health`) — LiveKit reachability, room list, auto-refresh
- Help modal (`?`), log viewer (filter, download, clear, auto-scroll)
- Pre-join device validation, reconnection banner, room URL discovery
- Sidebar nav (Dashboard, Meetings, Health, Settings)
- Mobile responsive (sidebar hidden, panels stack on < 1024px)

### AI Agent (Visio)
- Voice pipeline: Silero VAD → Whisper STT → Ollama LLM → Piper TTS
- Custom `SOTAOllamaLLM` adapter for livekit-agents 1.x
- Dynamic MCP tool discovery (scans 10700–10800 SSE endpoints)
- Dynamic tool delegation via `CombinedMCPFunctionContext`
- LanceDB RAG (transcripts, codebase, mission_logs, meeting_insights tables)
- Contact manager: Windows COM (Outlook) + local system users
- Screen reading via UIAutomation COM
- Reductionist logic / jargon LDDO detection
- State bus via Redis pub/sub (`ag_visio_fleet_state`)

### Conferencing MCP (10720)
- `generate_meeting_summary / extract_action_items` — LLM sampling + LanceDB
- `conference_schedule/list/get/update/cancel` — SQLite full CRUD
- `conference_upcoming` — next N days filter
- `room_create/list/delete/update_metadata` — LiveKit API
- `participant_invite/list/remove` — calendar participant management
- `room_participant_list/kick/mute/send_data` — real-time control
- `get_dev_stats` — git branch/status/log + disk volumes via PowerShell
- `query_system_logs / sample_log_analysis` — Windows Event Log + iterative sampling
- `get_substrate_heartbeat / orchestrate_industrial_diagnostics` — LiveKit/Ollama/system health
- `orchestrate_remote_support` — RustDesk registry probe and launch
- `list_active_conferences` — LiveKit rooms + scheduled conferences
- `sample_system_forensics` — ctx.sample() anomaly analysis
- `inter_agent_ping / notify_conference_active` — inter-agent signaling
- `set_translation_language` — live translation target

### Remoting MCP (10725)
- `move_mouse / click_mouse / type_text / press_key` — pynput input injection
- `join_meeting` — mss screen capture → BGRA→I420 → LiveKit VideoTrack at 15 FPS
- `leave_meeting / get_status / screen_resolution`

### Infrastructure
- Docker Compose with persisted volumes (`livekit_data`, `redis_data`, `lancedb_data`)
- Env var pattern `${VARIABLE:-default}` replacing hardcoded secrets
- `livekit.yaml` — port 15580, RTC 50000–60000

---

## Roadmap

### Completed (v2.3.0)
- Test infrastructure overhaul: 7 new parametrized test files (51 tests), 68 total Python tests
- Tool-level test coverage: diagnostics, conferencing CRUD, room mgmt, intelligence, signaling, remoting, participants
- Shared fixtures: mock_ctx (Context + sample), mock_livekit_api, mock_subprocess, temp_conference_db
- Playwright E2E: port fixed 15500→10886, new dashboard.spec.ts (12 tests), 22 total E2E specs
- LiveKit 2026 upgrades: UserTurnLimitOptions (60s cap), AutoRestartPolicy, OTel tracing config, TURN hardening
- `[tool.coverage]` config added; test count 44→68 (+55%)
- Duplicate fixture dedup, stale pytest.ini removed

### Completed (v2.2.0)
- Monolith refactored: 855-line mcp_server.py split into 5 tool modules (diagnostics/signaling/intelligence/conferences/rooms)
- FastMCP 3.2 docstring SOTA: 38 tools with Annotated/Field, ## Return Format, ## Examples
- Context injection added to all 8 remoting_mcp tools
- Shared `cid(ctx)` correlation_id helper eliminates 19x boilerplate
- Version constraint fix: pyproject.toml fastmcp>=3.1.0,<4
- `_now_iso()` promoted to public API; `conf.datetime/conf.timezone` → direct imports
- health_server.py bug fixes (_start_time race, off-by-one counter)
- justfile: test, typecheck, install recipes added; lint scope widened
- 36 lint errors resolved, 35 files clean

### Completed (v2.1.0)
- Screen sharing from browser dashboard
- Scheduling UI with create/list/copy-link
- Meeting recording via LiveKit Egress
- Background blur via track-processors
- Chat panel tab activated
- E2E Playwright tests (13 specs)
- Mobile responsive layout
- Full stubs replacement (contacts, vision, remote support)
- Screen capture wiring in remoting-mcp
- Dynamic MCP tool registration in agent
- Health monitoring and ThemeProvider
- Entrypoint fix and dep cleanup

### Phase 2.5 (Partially Complete)
- ✅ Scheduling UI (create meeting, room link)
- ✅ MCP tools for calendar CRUD (via conferencing-mcp)
- ⬜ Email invitations via SMTP / Email MCP
- ⬜ CalDAV sync

### Phase 3 (Wishlist)
- Breakout rooms, whiteboard, file sharing, E2E encryption
- `useRpc` hook (Components v2.9.21) — declarative agent calls from webapp
- Model swaps via `update_options` (Agents v1.5.10) — runtime LLM model changes
- Answering Machine Detection (Agents v1.5.9) — telephony bridge
- Perplexity / Mistral LLM connectors (Agents v1.5.7-1.5.12)

---

## Technology Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 16, React 19, TypeScript strict, TailwindCSS 4, @livekit/components-react 2.9 |
| Agent | Python 3.12, livekit-agents 1.5, Ollama, Whisper, Piper, Silero |
| Backend | FastMCP 3.2, LanceDB 0.30, FastEmbed, SQLite |
| Remoting | mss 10, pynput 1.8, pywin32 311 |
| Infra | Docker Compose, LiveKit 1.x, Redis 7 |
| Monorepo | Turborepo, npm workspaces, uv |
| Quality | Ruff, Pytest (68 parametrized tests), Vitest (27), Playwright (22 E2E), Coverage, Bandit, Safety |

---

## Claude Desktop Integration

```json
"mcpServers": {
  "teleconference-mcp": {
    "command": "uv",
    "args": ["--directory", "D:\Dev\repos\teleconference-mcp", "run", "teleconference-mcp"]
  }
}
```

---

## Integration Points

- **MCP Central Docs**: `integrations/livekit/` (integration guide, MCP patterns)
- **Fleet registry**: `operations/fleet-registry.json` (id: teleconference-mcp, port: 10886)
- **Web app registry**: `operations/webapp-registry.json` (port 10886)
- **Patterns**: `patterns/README.md` (Turborepo MCP Monorepo Pattern reference)

