# RustDesk MCP — Product Requirements Document

## 1. Overview

**Project Name**: RustDesk MCP Server  
**Version**: 0.1.0  
**Last Updated**: 2026-07-07  
**Repository**: [github.com/sandraschi/rustdesk-mcp](https://github.com/sandraschi/rustdesk-mcp)  
**Ports**: 10804 (frontend), 10805 (backend)  
**Status**: Pre-release — feature-complete, prod-hardening phase

### 1.1 Product Vision

RustDesk MCP is a **bridge between AI agents and remote desktop infrastructure**. It wraps RustDesk — the open-source remote desktop tool — into a 16-tool FastMCP surface so that LLMs and AI agents can autonomously manage remote machines: check device status, establish remote sessions, transfer files, wake sleeping hardware, and monitor resources — all through natural language.

The server has zero dependency on Docker or external management servers. It communicates directly with RustDesk's own TCP protocol (hbbs/hbbr) and CLI, with optional REST API fallback for enterprise deployments.

### 1.2 Problem Statement

RustDesk ships as a GUI-only client with basic CLI tools (`--get-id`, `--connect`, `--server`) and no REST API. There is no programmatic interface for AI agents to:

- Check whether RustDesk is installed and running
- Look up the local device ID
- Connect to a peer or disconnect a session
- Browse the address book
- Transfer files to/from a remote machine
- Wake a sleeping machine on the LAN
- Monitor CPU/memory/disk/network during a remote session

This server solves all of the above through a standard MCP tool surface.

### 1.3 Why not lejianwen/rustdesk-api?

The original design depended on the community `lejianwen/rustdesk-api` (a Docker-based management server). That approach was abandoned because:

- Docker dependency is unacceptable for non-dev users ("Steve class")
- The API server requires a full database + auth infrastructure
- The socket-based approach works with any running RustDesk hbbs/hbbr, no extra services

The REST API fallback still exists for users who do run the pro API server.

## 2. Target Audience

| Audience | Use Case | Value |
|----------|----------|-------|
| **AI Power Users** | Remote desktop via chat | Ask an LLM to connect, check status, transfer files |
| **System Administrators** | Fleet management | Automate session monitoring, address book queries, WOL |
| **IT Support Engineers** | Remote assistance | Scripted connect/disconnect for help desk workflows |
| **Home Lab Operators** | Infrastructure automation | Wake sleeping machines, check health, automated tasks |
| **DevOps** | CI/CD remote access | Programmatic remote access for deployment pipelines |

## 3. Features

### 3.1 MCP Tool Surface (16 tools)

#### Status & Discovery (READ_ONLY)

| Tool | Description |
|------|-------------|
| `get_rustdesk_status` | Service health, connection count, mock mode detection |
| `get_detailed_rustdesk_status` | Local ID, active sessions, address book, network config, performance |
| `check_rustdesk_installation` | Installation check, service state, executable path, config dir |
| `get_rustdesk_id` | Local device ID (9-10 digit numeric) for incoming connections |

#### Connection Management (READ_ONLY: list/read, MUTATING: connect/disconnect)

| Tool | Description |
|------|-------------|
| `list_active_sessions` | Active sessions via TCP socket + API + log parsing + session manager |
| `get_address_book` | Saved peers from addrbook.toml config file |
| `connect_to_peer` | Connect to remote machine by ID + password, optional session_id tracking |
| `disconnect_peer` | Disconnect specific session or all sessions |

#### File Transfer (MUTATING)

| Tool | Description |
|------|-------------|
| `transfer_file` | Upload/download files. Tries CLI `--file-transfer`, then REST API, returns `not_implemented` with SCP/SFTP suggestions if neither works |
| `list_remote_files` | List remote directory files (pro API server required) |

#### Screen Capture (MUTATING)

| Tool | Description |
|------|-------------|
| `take_screenshot` | Capture remote desktop (CLI v1.2.0+ or API server) |
| `start_recording` | Start recording (GUI-only — CLI does not expose recording) |
| `stop_recording` | Stop current recording |

#### Monitoring (READ_ONLY)

| Tool | Description |
|------|-------------|
| `monitor_resources` | CPU/memory/disk/network sampling over time (psutil) |
| `get_connection_quality` | System-level network I/O counters (psutil — not per-connection quality) |

#### Network (MUTATING)

| Tool | Description |
|------|-------------|
| `wake_on_lan` | Send magic packet to wake sleeping machine on LAN |

### 3.2 Dual Transport

| Mode | Usage | For |
|------|-------|-----|
| **stdio** | `python -m rustdesk_mcp` (default) | Claude Desktop, opencode, Cursor stdio |
| **HTTP streamable** | `MCP_PORT=10805 python -m rustdesk_mcp --http` | Tauri WebView, webapp, Cursor HTTP |

### 3.3 Backend Service Architecture

The `RustDeskService` uses a hybrid fallback chain for every operation:

```
CLI subprocess (rustdesk.exe --command)
  -> TCP Socket Client (hbbs:21116 / hbbr:21117)
    -> REST API (JWT auth, pro server at RUSTDESK_API_URL)
      -> SessionManager (in-memory fallback)
        -> Mock mode (if nothing is configured)
```

This means the server works in every deployment scenario — from a bare Windows machine with just RustDesk installed, up to a full enterprise API server.

### 3.4 Webapp (port 10804)

React 19 + Vite 7 + Tailwind 3 + TypeScript 5.9 + zustand + framer-motion + lucide-react.

| Page | Route | Features |
|------|-------|----------|
| **Dashboard** | `/` | Health KPIs, exponential backoff retry, data-testid, version/uptime |
| **Chat** | `/chat` | 4 personalities + Custom, skill-based preprompt (`/api/skills`), streaming, TTS SpeakButton, STT MicButton, Zustand store, localStorage persistence, export .txt |
| **Tools** | `/tools` | Dynamic discovery from `/api/tools`, annotation badges (READ/RW), expandable drill-down |
| **Skills** | `/skills` | Live skill browser, fetches markdown from backend |
| **API Docs** | `/api-docs` | Swagger/ReDoc toggle, quick-ref endpoint strip, iframe embed, "Open in browser" fallback |
| **Apps** | `/apps` | Fleet discovery — live port scan across 25+ known fleet ports |
| **Control** | `/control` | Remote click/type wired to `POST /api/control/`, security guard toggle |
| **Status** | `/status` | Connection telemetry |
| **Logging** | `/logs` | Ring-buffer log viewer, filter/search/pagination, JSON/CSV export, live tail |
| **Settings** | `/settings` | LLM provider/model configuration |
| **Help** | `/help` | Quick start, security, MCP parameters |
| **About** | `/about` | Server info |

#### Chat Speech Features

- **TTS**: SpeakButton on each assistant message reads via `window.speechSynthesis`
- **STT**: MicButton on input captures via Web Speech API, appends to input
- **Repo-aware voice**: Skill preprompt prepended to transcribed text
- **Markdown stripping**: `stripMarkdown()` before speech to avoid raw `**bold**` sounding bad

### 3.5 Desktop App (Tauri 2.0 NSIS)

Single-file NSIS installer containing:
- Rust operator shell (WebView2 + backend lifecycle)
- React `web_sota/dist` (embedded in operator)
- Python backend (PyInstaller onefile, embedded in `bundle.resources`)
- `.env.example` (NOT real `.env` — fleet security standard)

Build: `just build-native` (frontend -> tsc gate -> PyInstaller with size gate -> Tauri -> NSIS)

### 3.6 Session Context Injection

| Channel | Content |
|---------|---------|
| **.cursorrules** | RustDesk tool-awareness prompt: recall action (`get_rustdesk_status`, `get_address_book`, `list_active_sessions`), concrete tool calls, save action (`disconnect_peer`) |
| **.windsurfrules** | Copy of .cursorrules |
| **.claude-plugin/** | Claude Code SessionStart text injection via hooks.json |
| **.github/copilot-instructions.md** | GitHub Copilot injection |
| **llms.txt / llms-full.txt** | Tool registry + full documentation for LLM consumption |

### 3.7 LLM Provider Discovery

On webapp mount, probes:
- Ollama at `:11434` (`GET /api/tags`, 2s timeout)
- LM Studio at `:1234` (`GET /v1/models`, 2s timeout)

Provider status shown as green/red dot in chat header. Configured via `AI_PROVIDER`, `AI_ENDPOINT`, `AI_MODEL` env vars.

### 3.8 Build Artifacts

| Track | Command | Output |
|-------|---------|--------|
| Native | `just build-native` | `native/target/release/bundle/nsis/RustDesk MCP_0.1.0_x64-setup.exe` |
| MCPB | `mcpb pack . dist/rustdesk-mcp.mcpb` | `dist/rustdesk-mcp.mcpb` |
| Dev stack | `start.ps1` | Full backend + frontend, opens browser |
| CUA-NSIS smoke | `just cua-nsis-test` | 7-phase test: kill -> install -> launch -> health -> screenshot -> diagnostics -> uninstall |

## 4. Technical Specifications

### 4.1 Stack

| Layer | Technology |
|-------|-----------|
| **MCP Framework** | FastMCP >=3.4.2 |
| **REST Framework** | FastAPI >=0.95.0 |
| **Python** | >=3.12 |
| **Package Manager** | uv (lockfile: uv.lock) |
| **JS Package Manager** | bun (in web_sota/) |
| **Frontend** | React 19, Vite 7, TypeScript 5.9, Tailwind 3 |
| **State** | zustand, localStorage |
| **Desktop** | Tauri 2.0, Rust, NSIS installer |
| **Linting** | ruff (Python), biome (JS/TS) |
| **CI** | GitHub Actions (Windows) |
| **Testing** | pytest, Playwright (E2E), pywinauto (CUA-NSIS smoke) |

### 4.2 Dependencies

**Python (deployed):** fastmcp, fastapi, pydantic, psutil, aiohttp, httpx, structlog, pywinauto, pywinctl, wakeonlan, prefab-ui

**Python (dev):** pytest, pytest-asyncio, pyinstaller

**JS (deployed):** react, react-dom, react-router-dom, zustand, framer-motion, lucide-react, @radix-ui/\*, @tanstack/react-query, @tauri-apps/api

**JS (dev):** typescript, vite, tailwindcss, biome, postcss, autoprefixer

### 4.3 Port Allocation

| Port | Service |
|------|---------|
| 10804 | Frontend (Vite dev server) |
| 10805 | Backend (FastAPI + FastMCP HTTP) |
| 21116 | RustDesk hbbs (ID server, socket) |
| 21117 | RustDesk hbbr (relay server, socket) |

## 5. Known Limitations

| Limitation | Details | Mitigation |
|-----------|---------|------------|
| File transfer | Requires RustDesk CLI v1.2.0+ `--file-transfer` or pro API server | Returns `not_implemented` with SCP/SFTP suggestions and `error_type` field |
| Screen recording | RustDesk CLI does not expose recording controls | Return `not_implemented` with "use RustDesk GUI" suggestion |
| Connection quality | Uses system-level psutil metrics, not RustDesk per-connection quality | System counters are real but not per-session |
| Remote file listing | Requires pro API server | Returns `not_implemented` with API configuration suggestion |
| Screenshots | Requires CLI v1.2.0+ or API server | Returns `not_implemented` with upgrade suggestions |
| No per-session quality stats | Cannot get latency/bandwidth per RustDesk session | General network counters available |

## 6. Non-Goals

- **Not a RustDesk GUI replacement**: This server provides programmatic access, not a visual remote desktop client
- **Not a file sync tool**: File transfer is one-shot upload/download, not rsync/Syncthing
- **Not an enterprise MDM**: No device enrollment, GPO, or MDM-style management
- **Not a VPN**: Uses RustDesk's P2P relay, not a VPN tunnel
- **Not Docker-dependent**: Zero Docker requirement; the socket client talks directly to RustDesk servers
- **Not cloud-hosted**: Designed for local execution on the user's machine

## 7. Roadmap

### v0.1.0 (current)
- 16 MCP tools with SOTA docstrings and annotations
- Dual transport (stdio + HTTP)
- File transfer with CLI + API fallback
- Session tracking via socket + API + log parsing
- Wake-on-LAN
- React SOTA webapp (11 pages, chat, streaming, TTS/STT, fleet discovery)
- Tauri 2.0 NSIS installer with embedded backend
- Session context injection (all 5 channels)

### v0.2.0 (planned)
- **Real file transfer implementation** via direct RustDesk relay protocol reverse-engineering
- **Per-connection quality metrics** from the RustDesk protocol
- **Real remote screenshot** via native RustDesk protocol
- **Tray icon** for background operation (Tauri tray plugin)
- **Auto-update** via Tauri updater
- **Multiple concurrent remote sessions** in chat
- **Prefab UI cards** for status, sessions, address book

### v0.3.0 (stretch)
- **Remote file sync** — bidirectional sync over RustDesk relay
- **Clipboard bridge** — copy/paste between local and remote
- **Multi-hop connections** — connect through a jump host
- **Session recording playback** in webapp
- **SSH tunnel fallback** when RustDesk relay unreachable
- **Mac/Linux support** for non-Windows hosts running RustDesk

## 8. Quality Gates

Every release must pass:

1. `just lint` — ruff check + biome check (zero errors)
2. `uv run pytest tests/` — all unit tests pass
3. `tsc --noEmit` (web_sota/) — zero TypeScript errors
4. `just cua-nsis-test` — 7-phase CUA-NSIS smoke test passes
5. `npx playwright test` — Playwright E2E tests pass
6. `just build-native` — full build pipeline completes with valid NSIS output
7. Security audit — no `.env` in bundled resources (only `.env.example`)
8. Size gate — backend exe >= 5 MB, NSIS exe >= 1 MB
