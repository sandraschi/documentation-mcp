# myconf (AG-Visio) — Directory Structure

**Last Updated:** 2026-05-22
**Source Repo:** `D:\Dev\repos\myconf`
**Version:** 2.2.0

---

## Top-Level Layout

```
myconf/
├── myconf/                         # Python package (entry point)
│   ├── __init__.py                  # Package marker
│   ├── __main__.py                  # uv run -m myconf [conferencing|remoting|agent|web|all]
│   └── health.py                    # Shared health check utilities (LiveKit, Ollama, TCP)
├── apps/
│   ├── agent/                       # Visio AI voice agent (Python)
│   │   ├── agent.py                 # LiveKit VoicePipelineAgent with MCP discovery
│   │   ├── logic.py                 # Reductionist logic / jargon analysis
│   │   ├── memory_substrate.py      # LanceDB RAG engine (4 tables)
│   │   ├── contacts_substrate.py    # Multi-provider contact manager (Windows COM + local)
│   │   ├── vision_analyze.py        # OCR / screen perception via UIAutomation
│   │   ├── transcription_substrate.py # Multi-participant transcription handler
│   │   ├── state_bus.py             # Redis inter-agent coordination
│   │   └── tests/                   # pytest: agent, contacts, session, memory
│   ├── web/                         # Next.js 16 dashboard (port 10886)
│   │   ├── app/                     # App Router pages (/, /join/[room], /meetings, /settings, /recordings, /test)
│   │   ├── components/              # React components (AppShell, Sidebar, Topbar, MeetingIntelligencePanel, etc.)
│   │   ├── lib/                     # Settings, telemetry, discovery, prejoin, toast
│   │   ├── __tests__/               # Vitest unit tests (27 specs)
│   │   └── e2e/                     # Playwright E2E tests (13 specs)
│   └── docs/                        # Next.js documentation site (port 3001)
├── packages/
│   ├── conferencing_mcp/            # MCP server (port 10720, FastMCP 3.2)
│   │   ├── __init__.py              # Package marker
│   │   ├── mcp_server.py            # Thin orchestrator: FastMCP bootstrap + tool imports
│   │   ├── tools/                   # Tool modules (import-time @mcp.tool() registration)
│   │   │   ├── __init__.py          # Portmanteau: from . import conferences, diagnostics, ...
│   │   │   ├── diagnostics.py       # get_dev_stats, query_system_logs, sample_log_analysis,
│   │   │   │                         #   get_substrate_heartbeat, orchestrate_industrial_diagnostics,
│   │   │   │                         #   orchestrate_remote_support, sample_system_forensics
│   │   │   ├── signaling.py         # list_active_conferences, notify_conference_active, inter_agent_ping
│   │   │   ├── intelligence.py      # generate_meeting_summary, extract_action_items, set_translation_language
│   │   │   ├── conferences.py       # conference_schedule/get/list/update/cancel/upcoming,
│   │   │   │                         #   participant_invite/list_invited/remove_invited
│   │   │   └── rooms.py             # room_create/list/delete/update_metadata,
│   │   │                             #   room_participant_list/kick/mute, room_send_data
│   │   ├── conference.py            # SQLite CRUD + LiveKit API async helpers (data layer)
│   │   └── health_server.py         # HTTP health + Prometheus metrics endpoint (port 10721)
│   ├── remoting_mcp/                # MCP server (port 10725, FastMCP 3.2)
│   │   └── mcp_server.py            # Screen capture (mss) + input injection (pynput) + LiveKit publishing
│   ├── ui/                          # Shared React components (@repo/ui)
│   ├── eslint-config/               # Shared ESLint config (@repo/eslint-config)
│   └── typescript-config/           # Shared tsconfig (@repo/typescript-config)
├── tests/                           # Monorepo-wide Python tests (conftest, test_stack, test_remoting_logic)
├── docs/                            # Project documentation
│   ├── ARCHITECTURE.md              # Full architecture doc (Docker stack, service map, MCP discovery, data flow)
│   ├── FEATURES.md                  # Complete feature list
│   ├── USAGE.md                     # Usage guide
│   ├── INSTALL.md                   # Installation instructions
│   └── LIVEKIT.md                   # LiveKit configuration reference
├── docker-compose.yaml              # Full stack: livekit + redis + web + agent
├── livekit.yaml                     # LiveKit server config (ports, keys, logging, TURN)
├── justfile                         # Command runner: remoting, conferencing, agent, web, lint, fix, test, typecheck, install
├── start.ps1 / start.bat            # One-command startup
├── setup.ps1                        # One-time setup (Python venv, npm install, directories)
├── turbo.json                       # Turborepo task graph
├── package.json                     # Root workspaces (apps/*, packages/*)
├── pyproject.toml                   # Python config: fastmcp>=3.1.0,<4, Ruff, MyPy, Pytest
├── PRD.md                           # Product requirements document (422 lines)
├── CHANGELOG.md                     # Version history (v0.1.0 through v2.2.0)
├── TECHNICAL.md                     # Protocol internals and implementation details
└── README.md                        # Project overview and quick start
```

---

## apps/agent

Python LiveKit voice agent ("Visio"). Voice pipeline: Silero VAD → Whisper STT → Ollama LLM → Piper TTS.

Key files:
- **agent.py** ([430 lines]): Worker entrypoint; loads VAD, STT, TTS, custom SOTAOllamaLLM; `CombinedMCPFunctionContext` for dynamic MCP tool delegation; `user_speech_committed` hook for triggering.
- **logic.py**: Pure logic; `ReductionistLogic.reductionist_prompt`, `jargon_weights`, `analyze_saliency(text)`.
- **memory_substrate.py**: LanceDB RAG with `TextEmbedding` for vector search across transcripts and meeting insights.
- **contacts_substrate.py**: Multi-provider contact discovery (Windows COM Address Book + local system users).
- **vision_analyze.py**: OCR screen reading via Windows UIAutomation COM; saliency detection.
- **state_bus.py**: Redis pub/sub for cross-agent coordination (`ag_visio_fleet_state` channel).

---

## apps/web

Next.js 16 (App Router), React 19, TypeScript, TailwindCSS 4.

Key routes:
- **/** — Dashboard: join form, LiveKitRoom with VideoConference, AgentStatus, ReconnectionBanner
- **/join/[room]** — Guest join page: one-click from shared link, no dashboard needed
- **/meetings** — Scheduling UI: create form, upcoming/past list, copy invite link
- **/settings** — LiveKit URL, default room, devices, theme (dark/light/system), telemetry, Ollama model mgmt
- **/recordings** — Recording viewer: list view with room name, date, Play button
- **/test** — Device test: camera preview, device dropdowns, audio meter
- **/health** — LiveKit and discovery service status, active rooms

Key components:
- **AppShell.tsx** — Layout shell with sidebar, topbar, theme toggle
- **Sidebar.tsx** — Nav: Dashboard, Meetings, Health, Settings, Test
- **MeetingIntelligencePanel.tsx** — AI summaries + action items (LanceDB)
- **ScreenShareControl.tsx** — Screen sharing via `getDisplayMedia` + LiveKit `publishTrack`
- **BackgroundBlurToggle.tsx** — Camera background blur via `@livekit/track-processors`
- **RecordingButton.tsx** — Meeting recording via LiveKit Egress API
- **RemoteAssistanceOverlay.tsx** — Remote desktop via RustDesk
- **ChatPanel.tsx** — LiveKit `useChat`
- **ErrorBoundary.tsx** / **ReconnectionBanner.tsx** — Resilience
- **HelpModal.tsx** / **ShareRoomModal.tsx** / **LogViewer.tsx**

---

## packages/conferencing_mcp

FastMCP 3.2 MCP server with 25 tools across 5 modules.

### Tool Inventory

| Module | Tools | Description |
|--------|-------|-------------|
| **diagnostics.py** | `get_dev_stats`, `query_system_logs`, `sample_log_analysis`, `get_substrate_heartbeat`, `orchestrate_industrial_diagnostics`, `orchestrate_remote_support`, `sample_system_forensics` | System diagnostics, Windows Event Log, LiveKit/Ollama heartbeat, RustDesk launch, LLM forensics |
| **signaling.py** | `list_active_conferences`, `notify_conference_active`, `inter_agent_ping` | Conference grid listing, inter-agent signaling |
| **intelligence.py** | `generate_meeting_summary`, `extract_action_items`, `set_translation_language` | LLM sampling via `ctx.sample()`, LanceDB persistence, live translation |
| **conferences.py** | `conference_schedule`, `conference_get`, `conference_list`, `conference_update`, `conference_cancel`, `conference_upcoming`, `participant_invite`, `participant_list_invited`, `participant_remove_invited` | SQLite calendar CRUD, participant management |
| **rooms.py** | `room_create`, `room_list`, `room_delete`, `room_update_metadata`, `room_participant_list`, `room_participant_kick`, `room_participant_mute`, `room_send_data` | LiveKit API room + participant operations |

All tools use FastMCP 3.2 SOTA: `Annotated[T, Field(description="...")]` parameters, `## Return Format`, `## Examples`, shared `cid(ctx)` correlation_id helper.

### Data Layer
- **conference.py** ([462 lines]): SQLite (`conference.db`) for conference CRUD + participant tracking. LiveKit API async helpers for room/participant operations. Shared `now_iso()` timestamp utility.
- **health_server.py**: HTTP `/health` (JSON) + `/metrics` (Prometheus) endpoints on port 10721. Class-level `_start_time`/`_request_count`.

---

## packages/remoting_mcp

FastMCP 3.2 MCP server with 8 tools. All tools accept `ctx: Context` with correlation_id logging.

| Tool | Description |
|------|-------------|
| `move_mouse(x, y)` | Move system cursor to absolute coordinates |
| `click_mouse(button)` | Mouse click (left/right/middle) |
| `type_text(text)` | Type string into active window |
| `press_key(key_name)` | Press a specific key |
| `screen_resolution()` | Return primary monitor resolution |
| `join_meeting(url, token)` | Join LiveKit room, start screen publishing at 15 FPS (mss → BGRA→I420 → VideoTrack) |
| `leave_meeting()` | Leave room, stop screen capture loop |
| `get_status()` | Return connected/publishing/room_name/correlation_id |

---

## Infrastructure

| File | Purpose |
|------|---------|
| `docker-compose.yaml` | livekit (15580-15582), redis (16379), optional web + agent services |
| `livekit.yaml` | port 15580, RTC range 50000-60000, env var keys, STUN/TURN config |
| `justfile` | Recipes: remoting, conferencing, agent, web, build-web, lint, fix, test, typecheck, install, check-sec, audit-deps, clean, setup |
| `.pre-commit-config.yaml` | Ruff, trailing-whitespace, check-yaml, check-json |

---

## Port Scheme

| Port | Service |
|------|---------|
| 10886 | Web dashboard (Next.js) |
| 10887 | AI Agent SSE endpoint |
| 10720 | Conferencing MCP server |
| 10721 | Conferencing health/metrics HTTP |
| 10725 | Remoting MCP server |
| 15580 | LiveKit HTTP/WebSocket |
| 15581 | LiveKit WebRTC |
| 15582 | LiveKit TURN (UDP) |
| 16379 | Redis |
| 11434 | Ollama API |

---

## Config & Quality

| File | Purpose |
|------|---------|
| `pyproject.toml` | Python: fastmcp>=3.1.0,<4, Python 3.12 target, Ruff (line-length 120), MyPy, Pytest |
| `turbo.json` | Turborepo: build, lint, test, dev, type-check, check-sec, audit-deps |
| `apps/web/.env.local` | `NEXT_PUBLIC_LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` |
| `apps/agent/.env` | `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` (optional) |
