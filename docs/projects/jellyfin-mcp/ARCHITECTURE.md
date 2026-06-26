# Architecture — jellyfin-mcp

**For:** Developers, Contributors  
**Purpose:** System design and technical architecture  
**Last Updated:** 2026-05-21  
**Status:** Pre-Implementation

---

## Overview

jellyfin-mcp is a FastMCP 3.2+ server providing AI agent access to Jellyfin Media Server, paired with a React webapp dashboard. It wraps Jellyfin's REST API (full OpenAPI/Swagger spec) and WebSocket events, following the proven portmanteau tool pattern established by plex-mcp.

### Key Goals

- Expose complete Jellyfin API surface through ~22 portmanteau MCP tools
- Provide real-time playback/transcode dashboard via WebSocket bridge
- Enable plugin management (install, configure, uninstall) via MCP
- Deliver a React webapp matching plex-mcp quality with Jellyfin-specific features (plugins, LiveTV, transcode monitor)
- Support fully air-gapped operation (no cloud dependency)

### Design Principles

- **Portmanteau first** — One tool per domain, `operation` parameter for dispatch; never 1:1 tool-to-endpoint mapping
- **Async executor pattern** — Blocking SDK calls run in thread pool executor, never block the async loop
- **WebSocket event bridge** — Real-time events forwarded to the webapp via a lightweight internal relay
- **Self-hosted parity** — Feature set equals or exceeds plex-mcp; plugin architecture is an advantage, not a workaround

---

## System Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│   Claude Desktop     │     │   Web Browser        │
│   (MCP Client)       │     │   (React Dashboard)  │
└──────────┬──────────┘     └──────────┬──────────┘
           │ MCP Protocol               │ HTTP / WS
           │ (STDIO / HTTP)             │
┌──────────▼─────────────────────────▼──────────────┐
│              jellyfin-mcp Server                   │
│                                                    │
│  ┌──────────────────────────────────────────────┐ │
│  │  Transport Layer (transport.py)               │ │
│  │  STDIO | HTTP | SSE | WebSocket               │ │
│  └───────────────────┬──────────────────────────┘ │
│                      │                             │
│  ┌───────────────────▼──────────────────────────┐ │
│  │  FastMCP 3.2+ Core (app.py)                  │ │
│  │  - Lifespan (connect/disconnect Jellyfin)    │ │
│  │  - Sampling handler (LLM integration)        │ │
│  │  - Resource registration                     │ │
│  │  - Prompt templates                          │ │
│  └───────────────────┬──────────────────────────┘ │
│                      │                             │
│  ┌───────────────────▼──────────────────────────┐ │
│  │  Tool Layer (tools/portmanteau/)             │ │
│  │  - 22 portmanteau tools (120+ operations)    │ │
│  │  - Pydantic v2 input models                  │ │
│  │  - @mcp.tool() decorator registration        │ │
│  └───────────────────┬──────────────────────────┘ │
│                      │                             │
│  ┌───────────────────▼──────────────────────────┐ │
│  │  Service Layer (services/)                   │ │
│  │  - JellyfinService (REST API wrapper)        │ │
│  │  - WebSocketService (real-time events)       │ │
│  │  - PluginService (plugin lifecycle)          │ │
│  │  - EnrichmentService (TMDB, MusicBrainz)     │ │
│  │  - RAGService (LanceDB vector store)         │ │
│  │  - ArrStackService (Radarr/Sonarr/Lidarr)    │ │
│  └───────────────────┬──────────────────────────┘ │
│                      │                             │
└──────────────────────┼─────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │              │              │
┌────────▼────────┐ ┌──▼──────┐ ┌─────▼──────────┐
│ Jellyfin Server  │ │ TMDB    │ │ MusicBrainz    │
│ (REST + WS)      │ │ (REST)  │ │ (REST)         │
│ port 8096        │ │         │ │                │
└──────────────────┘ └─────────┘ └────────────────┘
```

---

## Components

### 1. MCP Server Core

**Location:** `src/jellyfin_mcp/app.py`

**Purpose:** Shared FastMCP instance with lifespan, sampling, resources, and prompts.

**Lifespan flow:**
```
startup → JellyfinService.connect() → WebSocketService.start()
         → ArrStackService.health_check() → PluginService.cache_manifest()
shutdown → WebSocketService.stop() → JellyfinService.disconnect()
```

**Dependencies:**
- FastMCP >= 3.2.0
- jellyfin-apiclient-python >= 1.10.0
- aiohttp >= 3.9.0 (WebSocket)

### 2. Transport Layer

**Location:** `src/jellyfin_mcp/transport.py`

**Purpose:** Unified multi-transport entry point. Supports:

| Mode | Flag | Use Case |
|------|------|----------|
| STDIO | `--stdio` | Claude Desktop direct |
| HTTP | `--http --port 10934` | MCP Inspector, remote agents |
| SSE | `--sse --port 10934` | Browser-based clients |
| WebSocket | `--ws --port 10934` | Webapp live dashboard |

**Environment:**
- `JELLYFIN_MCP_TRANSPORT` — Default transport mode
- `JELLYFIN_MCP_PORT` — HTTP/SSE/WS port (default: 10934)
- `JELLYFIN_MCP_HOST` — Bind address (default: 127.0.0.1)

### 3. Tool Layer

**Location:** `src/jellyfin_mcp/tools/portmanteau/`

**Organization:**
```
tools/
├── __init__.py              # Re-exports all portmanteau tools
├── agentic.py               # jellyfin_agentic (workflow, natural_query)
├── library.py               # jellyfin_library (15 ops)
├── media.py                 # jellyfin_media (10 ops)
├── search.py                # jellyfin_search (6 ops)
├── playback.py              # jellyfin_playback (12 ops)
├── user.py                  # jellyfin_user (10 ops)
├── playlist.py              # jellyfin_playlist (9 ops)
├── collections.py           # jellyfin_collections (7 ops)
├── metadata.py              # jellyfin_metadata (10 ops)
├── server.py                # jellyfin_server (10 ops)
├── streaming.py             # jellyfin_streaming (8 ops)
├── plugin.py                # jellyfin_plugin (8 ops) ← UNIQUE to Jellyfin
├── arr_stack.py             # jellyfin_arr_stack (6 ops)
├── subtitle.py              # jellyfin_subtitle (7 ops)
├── livetv.py                # jellyfin_livetv (8 ops) ← UNIQUE to Jellyfin
├── ffmpeg.py                # jellyfin_ffmpeg (6 ops)
├── enrichment.py            # jellyfin_enrichment (6 ops)
├── rag.py                   # jellyfin_rag (5 ops)
├── reporting.py             # jellyfin_reporting (8 ops)
├── recommend.py             # jellyfin_recommend (5 ops)
├── help.py                  # jellyfin_help (6 ops)
└── integration.py           # jellyfin_integration (5 ops)
```

**Registration:** Tools register via `@mcp.tool()` decorators at import time. The `__init__.py` chain imports all 22 modules during server boot.

**Pattern:**
```python
@mcp.tool(annotations=MUTATING)
async def jellyfin_library(
    operation: Annotated[LibraryOperation, Field(description="Library operation to execute.")],
    library_id: Annotated[str | None, Field(description="Target library ID.")] = None,
    params: Annotated[dict | None, Field(description="Operation-specific parameters.")] = None,
) -> dict:
    """Manage Jellyfin media libraries.

    ## Return Format
    {"success": bool, "message": str, "data": dict | list}
    """
```

### 4. Service Layer

**Location:** `src/jellyfin_mcp/services/`

| Service | File | Purpose |
|---------|------|---------|
| `JellyfinService` | `jellyfin_service.py` | Core REST API wrapper, auto-discovery, auth refresh |
| `WebSocketService` | `websocket_service.py` | Real-time event subscription, internal event bus |
| `PluginService` | `plugin_service.py` | Plugin catalog, install/uninstall/configure lifecycle |
| `EnrichmentService` | `enrichment_service.py` | TMDB, MusicBrainz, OMDb metadata augmentation |
| `RAGService` | `rag_service.py` | LanceDB vector indexing, semantic search |
| `ArrStackService` | `arr_stack_service.py` | Radarr/Sonarr/Lidarr status and queue |
| `BaseService` | `base.py` | Shared config, executor, error handling |

**Executor pattern:**
```python
class JellyfinService(BaseService):
    def __init__(self, config: JellyfinConfig):
        self.config = config
        self._client = None

    async def connect(self):
        self._client = await self._run_in_executor(
            lambda: JellyfinClient(
                server_url=config.url,
                api_key=config.api_key,
            )
        )
        self._client.authenticate()

    async def get_libraries(self) -> list[Library]:
        return await self._run_in_executor(
            lambda: self._client.library.get_media_folders()
        )
```

### 5. WebSocket Event Bridge

**Location:** `src/jellyfin_mcp/services/websocket_service.py`

Jellyfin exposes a WebSocket API at `ws://jellyfin:8096/websocket` with events for:
- `PlaybackStart` / `PlaybackStop` / `PlaybackProgress`
- `SessionStarted` / `SessionEnded`
- `LibraryChanged` (new content, metadata refresh)
- `TranscodeProgress`
- `UserDataChanged` (watch status)

The WebSocketService:
1. Connects to Jellyfin WebSocket on server start
2. Subscribes to all event types
3. Publishes events to an internal asyncio event bus
4. Webapp connects via a proxy WebSocket on port 10934 `/ws`
5. Event bus replays latest state on webapp connect

### 6. Configuration

**Location:** `src/jellyfin_mcp/config.py`

```python
class JellyfinConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="JELLYFIN_")

    url: str = "http://localhost:8096"
    api_key: str | None = None
    username: str | None = None       # Fallback auth
    password: str | None = None       # Fallback auth
    timeout: int = 30
    max_retries: int = 3
    ws_enabled: bool = True
    plugin_auto_update: bool = False
    sampling_base_url: str = "http://127.0.0.1:11434/v1"
    sampling_model: str = "llama3.2"
```

### 7. Error Handling

```
JellyfinError
├── AuthenticationError     (wrong API key, expired token)
├── ConnectionError         (server unreachable)
├── NotFoundError           (item/user/library not found)
├── ValidationError         (invalid parameters)
├── TranscodeError          (codec unsupported, GPU unavailable)
├── PluginError             (install fail, incompatible version)
└── WebSocketError          (connection lost, reconnection failed)
```

---

## Data Flow

### MCP Tool Request Flow
```
1. Claude Desktop → MCP Protocol Request
2. transport.py → Route to FastMCP
3. FastMCP → Match @mcp.tool() by name
4. Tool → Pydantic v2 validate input
5. Tool → Service.get_instance() → JellyfinService
6. JellyfinService → _run_in_executor() → jellyfin-apiclient-python
7. jellyfin-apiclient-python → HTTP → Jellyfin Server REST API
8. Response → Service.format_response() → dict
9. Tool → return {"success": True, "data": ...}
10. FastMCP → MCP Protocol Response → Claude Desktop
```

### WebSocket Real-Time Flow
```
1. WebSocketService → connect to ws://jellyfin:8096/websocket
2. Jellyfin Server → push event ("PlaybackStart")
3. WebSocketService → parse event → publish to internal bus
4. Webapp → ws://localhost:10934/ws → subscribe to bus
5. Event bus → forward event to webapp
6. React component → update playback dashboard in real-time
```

### Plugin Install Flow
```
1. User → jellyfin_plugin(operation="install", plugin_id="intro-skip")
2. PluginService → fetch plugin manifest from Jellyfin catalog
3. PluginService → download .dll / .zip to Jellyfin plugin dir
4. PluginService → jellyfin_server(operation="restart")
5. On next connect → PluginService → verify plugin loaded
```

---

## Webapp Architecture

### Backend (FastAPI)

**Location:** `webapp/backend/app/`

**Port:** 10934 (shared with MCP HTTP)

**Routes:**

| Prefix | Module | Purpose |
|--------|--------|---------|
| `/api/libraries` | `libraries.py` | Library list, detail, stats |
| `/api/media` | `media.py` | Browse, search, detail, stream info |
| `/api/playback` | `playback.py` | Sessions, control, transcode queue |
| `/api/plugins` | `plugins.py` | Plugin catalog, installed list, manage |
| `/api/users` | `users.py` | User CRUD, permissions, policies |
| `/api/livetv` | `livetv.py` | EPG, recordings, tuners |
| `/api/server` | `server.py` | Status, health, logs, tasks |
| `/api/search` | `search.py` | Text + advanced + semantic |
| `/api/images` | `images.py` | Artwork proxy (Jellyfin → browser) |
| `/api/rag` | `rag.py` | Semantic search, sync, reindex |
| `/api/enrichment` | `enrichment.py` | External metadata (TMDB, etc.) |
| `/api/llm` | `llm.py` | Chat, model listing |
| `/api/arr` | `arr_stack.py` | Radarr/Sonarr/Lidarr status |
| `/api/settings` | `settings.py` | Server config, env vars |
| `/api/help` | `help.py` | Tool reference, FAQ |
| `/mcp` | `mcp_mount.py` | FastMCP HTTP mount (lazy, ~90s) |
| `/ws` | `ws.py` | WebSocket proxy → WebSocketService bus |
| `/health` | `health.py` | Readiness probe |

### Frontend (Next.js 15.2)

**Location:** `webapp/frontend/`

**Port:** 10935

**Dependencies:**
- `next: 15.2.0`, `react: ^18.2.0`
- `tailwindcss: ^3.4.0`, `lucide-react`, `clsx`, `tailwind-merge`
- `recharts` (transcode charts), `react-hook-form` (settings)
- Dev: `playwright`, `@biomejs/biome`, `typescript: ^5.3.0`

---

## Security Architecture

### Authentication
- **API Key auth** (primary): `X-Emby-Token` header on all Jellyfin API calls
- **Username/Password** (fallback): for initial token acquisition, never stored
- **API key stored** via env var `JELLYFIN_API_KEY` or `.env` file (gitignored)

### Authorization
- Jellyfin's native user permission system is used without modification
- MCP tools respect the permissions of the authenticated Jellyfin user
- No MCP-level privilege escalation

### Network Security
- Default bind: `127.0.0.1` only
- No external exposure unless explicitly configured
- WebSocket event bridge filters sensitive events (passwords, tokens)
- No telemetry, no cloud calls, no external auth dependency

---

## Monitoring & Observability

### Logging
- Structured logging via `structlog`
- Operation, duration, success/failure per tool call
- WebSocket connection state transitions logged

### Health Checks
- `GET /health` — 200 if Jellyfin reachable
- `GET /health/ready` — 200 if all services initialized
- `GET /health/live` — 200 if process alive

### Metrics
- Tool call count, duration (per operation)
- WebSocket event throughput
- Jellyfin server response time
- Plugin catalog staleness

---

## Extension Points

1. **New portmanteau tool** — Add file to `tools/portmanteau/`, import in `__init__.py`
2. **New enrichment source** — Add class to `enrichment_service.py`, implement `fetch()` + `normalize()`
3. **New WebSocket event handler** — Register callback in `WebSocketService._dispatch()`
4. **Plugin bridge** — Jellyfin plugins can expose custom APIs; PluginService can introspect and proxy them
5. **Tauri native** — Follow `tauri_godot_sota.md` template for native desktop wrapper

---

## Dependency Graph

```
jellyfin-mcp
├── fastmcp (>=3.2.0)
│   └── pydantic (>=2.0.0)
├── jellyfin-apiclient-python (>=1.10.0)
│   └── requests, websocket-client
├── aiohttp (>=3.9.0)  ← WebSocket bridge
├── fastapi (>=0.104.0)
├── uvicorn[standard] (>=0.24.0)
├── httpx (>=0.25.0)  ← image proxy, enrichment API
├── lancedb (>=0.4.0)  ← RAG vector store
├── sentence-transformers (>=2.2.0)  ← embeddings
├── prefab-ui (>=0.18.0)  ← card UI components
├── rich (>=13.0.0)  ← CLI formatting
└── python-dotenv (>=1.0.0)
```

---

## Testing Architecture

| Layer | Tool | Scope |
|-------|------|-------|
| Unit | pytest | Service methods, tool dispatch, config parsing |
| Integration | pytest-vcr | Recorded Jellyfin API responses |
| E2E | Playwright | Webapp page navigation, search, playback dashboard |
| Load | locust | Concurrent tool calls, WebSocket event flood |

---

## Appendix: Port Assignment

| Port | Service | Protocol |
|------|---------|----------|
| **10934** | jellyfin-mcp Backend | HTTP (FastAPI + MCP + WebSocket) |
| **10935** | jellyfin-mcp Frontend | HTTP (Vite/Next.js dev + HMR) |
| 8096 | Jellyfin Server (external) | HTTP + WebSocket |

---

## Appendix: Comparison with plex-mcp Architecture

| Aspect | plex-mcp | jellyfin-mcp |
|--------|----------|--------------|
| MCP framework | FastMCP 3.2+ | FastMCP 3.2+ |
| Media SDK | plexapi (third-party) | jellyfin-apiclient-python (official) |
| Transport | STDIO, HTTP, SSE | STDIO, HTTP, SSE, **WebSocket** |
| Tool count | 20 portmanteau | 22 portmanteau |
| Real-time events | None (polling) | **WebSocket event bus** |
| Plugin management | N/A (Plex deprecated) | **First-class plugin tools + UI** |
| Live TV | N/A | **EPG grid + DVR management** |
| Auth | Cloud token (plex.tv) | **Local API key (air-gappable)** |
| Sampling handler | Ollama OpenAI-compatible | Same (shared pattern) |
| RAG | LanceDB | LanceDB |
| Prefab cards | 9 cards | 11 cards (+ plugin, transcode) |
| Webapp pages | 13 | 13 (different composition) |

---

*Last updated: 2026-05-21 — Pre-implementation phase*
