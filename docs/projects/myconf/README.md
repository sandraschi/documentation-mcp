# myconf (AG-Visio / Teams++)

**Professional video conferencing platform** with AI voice agent integration, built on Turborepo and LiveKit. Features real-time transcription, multi-room support, screen sharing, meeting recording, background blur, and comprehensive device testing.

**Version**: 2.3.0 | **Status**: Active Development | **Ports**: Web 10886, Conferencing MCP 10720, Remoting MCP 10725, Agent 10887

---

## Stability & SOTA Alignment

Adheres to strict **SOTA (State-Of-The-Art) standards**:
- **Ruff linting** with 120-char line limit, zero errors across 42 files
- **68 Python tests** (pytest, parametrized) + **27 frontend unit tests** (vitest) + **22 E2E specs** (Playwright)
- **Bandit** security scanning + **Safety** dependency auditing
- **Pre-commit hooks** for ruff, mypy, trailing-whitespace, yaml/json validation
- **CI pipeline**: parallel Node 20 + Python 3.12 jobs with Codecov

---

## Architecture

```
Browser (port 10886)
  │ WebSocket
  ▼
LiveKit SFU (port 15580) ─── Redis (port 16379)
  │ WebRTC           │ Data Channel
  ▼                   ▼
Visio AI Agent (port 10887)
  │ SSE discovery (10700-10800)
  ▼
conferencing-mcp (10720)   remoting-mcp (10725)
  SQLite + LanceDB           mss + pynput
```

---

## Features

### Web Application (port 10886)
- Multi-room conferencing with grid/focus layout
- Screen sharing via `getDisplayMedia` + LiveKit track publishing
- Background blur via `@livekit/track-processors`
- Meeting recording via LiveKit Egress API
- Meeting intelligence panel (AI summaries + action items)
- Real-time transcription with speaker identification
- Chat panel via LiveKit `useChat`
- Device test page (`/test`) with camera/mic/speaker validation
- Scheduling UI (`/meetings`) — create, list, copy invite link
- Settings: devices, theme (dark/light/system), telemetry, Ollama model management
- Health dashboard (`/health`) with LiveKit and discovery status
- Help modal (`?`), log viewer (filter, download, clear)
- Pre-join device validation, reconnection banner, room discovery
- Mobile responsive layout (sidebar hidden, panels stack on < 1024px)

### AI Agent (Visio)
- Voice pipeline: Silero VAD → Whisper STT → Ollama LLM → Piper TTS
- Dynamic MCP tool discovery (scans 10700–10800)
- LanceDB RAG memory (transcripts, codebase, mission logs)
- Contact manager (Windows COM + local users)
- Screen reading via UIAutomation OCR
- Jargon detection / LDDO analysis
- Automatic room joining, context-aware responses

### MCP Servers

**conferencing-mcp** (port 10720, FastMCP 3.2):
- `generate_meeting_summary` / `extract_action_items` — LLM sampling + LanceDB persist
- `conference_schedule/list/get/update/cancel` — SQLite calendaring
- `room_create/list/delete/update_metadata` — LiveKit room CRUD
- `participant_invite/list/remove` — participant management
- `room_participant_list/kick/mute` — real-time participant control
- `room_send_data` — data channel broadcast
- `get_dev_stats` — git + disk status
- `get_substrate_heartbeat` — LiveKit + Ollama health probe
- `orchestrate_remote_support` — RustDesk detection and launch
- `list_active_conferences` — LiveKit rooms + scheduled conferences

**remoting-mcp** (port 10725, FastMCP 3.2):
- `move_mouse / click_mouse / type_text / press_key` — input injection
- `join_meeting / leave_meeting` — screen publishing to LiveKit
- `get_status / screen_resolution` — state queries

### Infrastructure
- Docker Compose: LiveKit (15580–15582), Redis (16379), Web (15500), Agent
- Ollama runs outside Docker on host PC
- Docker volumes for persistent data: `livekit_data`, `redis_data`, `lancedb_data`

---

## Quick Start

```powershell
git clone https://github.com/sandraschi/myconf.git
cd myconf
uv sync
npm install
docker compose up -d livekit redis
.\start.ps1 all
```

### Individual Services

```powershell
uv run -m myconf conferencing   # MCP server (port 10720)
uv run -m myconf remoting       # Remoting MCP (port 10725)
uv run -m myconf agent          # AI agent (port 10887)
uv run -m myconf web            # Dashboard (port 10886)
```

---

## Documentation

| Guide | Location |
|-------|----------|
| Installation | `docs/INSTALL.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| LiveKit Reference | `docs/LIVEKIT.md` |
| Features | `docs/FEATURES.md` |
| Usage | `docs/USAGE.md` |
| Technical Reference | `TECHNICAL.md` |
| Changelog | `CHANGELOG.md` |
| PRD | `PRD.md` |

---

## Testing

```powershell
# Python (44 tests)
uv run pytest tests/ apps/agent/tests/ -v

# Web unit (27 tests)
cd apps/web && npx vitest run

# Web E2E (13 specs, requires dev server)
cd apps/web && npx playwright test
```

---

## Claude Desktop Integration

```json
"mcpServers": {
  "myconf": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/myconf", "run", "myconf"]
  }
}
```

---

## License

MIT
