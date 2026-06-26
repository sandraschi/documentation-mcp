# jellyfin-mcp — Product Requirements Document

**Status:** Pre-Implementation | **Version:** 0.1.0-draft | **Date:** 2026-05-21

---

## 1. Executive Summary

jellyfin-mcp is a FastMCP 3.2+ server and React webapp wrapping the Jellyfin Media Server API. It fills the #1 priority gap identified in the fleet's `WRAPPEE_CANDIDATES_ANALYSIS.md` — a full-featured, open-source media server MCP that outperforms Plex in every dimension that matters for power users: plugins, hardware transcoding (free), WebSocket real-time events, and no licensing tier wall.

### Why Now

| Factor | Signal |
|--------|--------|
| **Jellyfin growth** | 51.8k GitHub stars, 4.8k forks, active plugin ecosystem |
| **Plex lock-in decay** | Plex deprecated plugins, paywalls DVR/transcoding, added ad-supported content |
| **MCP gap** | Zero FastMCP-based jellyfin-mcp servers exist on GitHub (10 attempts, all wrong language or abandoned) |
| **Fleet readiness** | Plex-mcp proven as reference architecture; scaffolding templates verified |
| **Legal clarity** | SCOTUS Cox ruling (Sony Music v. Cox, 2025) reinforces Betamax doctrine — media servers with substantial non-infringing use are protected |

---

## 2. Jellyfin vs Plex: Strategic Analysis

### 2.1 Technical Comparison

| Feature | Plex | Jellyfin | Winner |
|---------|------|----------|--------|
| **License** | Proprietary (freemium) | GPL-2.0 | **Jellyfin** |
| **Plugins** | Deprecated (2024) | First-class, 100+ plugins | **Jellyfin** |
| **Hardware transcoding** | Plex Pass required ($120/lifetime) | Free | **Jellyfin** |
| **DVR / Live TV** | Plex Pass required | Free | **Jellyfin** |
| **Intro skip / credit detection** | Plex Pass required | Free (plugin) | **Jellyfin** |
| **Offline sync** | Plex Pass required | Free | **Jellyfin** |
| **Real-time WebSocket API** | No (poll-only) | Yes | **Jellyfin** |
| **Multi-user** | Plex Home (complex) | Native, simple | **Jellyfin** |
| **Server language** | C++ (closed) / Python API | C# (.NET) core, REST API | Draw |
| **Client apps** | Excellent, polished | Good, open-source | Plex |
| **Metadata providers** | First-party (closed) | Plugin-based, configurable | **Jellyfin** |
| **Ad-supported content** | Yes (Plex Movies & TV) | No | **Jellyfin** |
| **Telemetry** | Mandatory, cannot fully disable | None | **Jellyfin** |
| **API docs** | Partial, semi-documented | Full OpenAPI/Swagger (auto-generated) | **Jellyfin** |

### 2.2 The Plex "Weird Hybrid" Problem

Plex occupies an ambiguous position in the media landscape:

- **De facto use case:** 90%+ of Plex servers host personal media collections (ripped DVDs, Blu-rays, downloads). This is the "private movie depot" pattern.
- **Legal figleaf:** Plex operates Plex Movies & TV (ad-supported streaming), Plex Arcade, and TIDAL integration — commercial content that provides a veneer of legitimacy.
- **The contradiction:** Plex sells itself as a legitimate media platform while knowing its user base overwhelmingly uses it as a personal piracy management system.

This ambiguity creates real problems for an MCP integration:
- Plex's API is designed for their commercial ecosystem, not for power-user media management
- Auth is tied to plex.tv cloud accounts (cannot run fully air-gapped)
- Feature gating behind Plex Pass means your tools stop working when a subscription lapses

### 2.3 The SCOTUS Cox Ruling & Legal Landscape

**Sony Music Entertainment v. Cox Communications (2025)** — The Supreme Court ruled that ISPs can be held liable for contributory copyright infringement when they knowingly profit from subscriber piracy and fail to terminate repeat infringers. This is significant for the media server ecosystem because:

1. **The Betamax Doctrine holds:** The Court explicitly reaffirmed *Sony Corp. v. Universal City Studios* (1984) — a technology with "substantial non-infringing uses" is not infringing per se. Both Plex and Jellyfin clearly qualify (legitimate DVD/Blu-ray collections, home videos, CC-licensed content).

2. **The ruling targets *conduct*, not *tools*:** Cox was liable because they *ignored infringement notices* to keep collecting subscription fees from pirate users. A media server that doesn't monetize infringement is a fundamentally different category.

3. **Plex's legal advantage evaporates:** Plex historically positioned its commercial streaming content as a legal shield against the "piracy tool" accusation. The Cox ruling makes clear this is unnecessary — the tool itself is protected regardless of whether it also has commercial content.

4. **Jellyfin is legally cleaner:** Jellyfin has zero commercial content, zero telemetry, zero profit motive. It is the purest expression of the Betamax doctrine: a tool that enables completely lawful uses (streaming your own DVDs to your own devices). There is no "figleaf" to defend because there is no gray area.

**Bottom line:** The legal environment for a Jellyfin MCP is clearer than for Plex. No cloud dependency, no commercial entanglement, no telemetry data that could be subpoenaed. Pure self-hosted media management.

---

## 3. Tool Surface Design

### 3.1 Portmanteau Architecture (22 tools, ~120 operations)

Following the plex-mcp portmanteau pattern, tools are organized by domain with an `operation` parameter using `Literal[...]` types. Each tool combines related operations to minimize tool count while maximizing capability.

#### Core Tools

| # | Tool | Operations | Category | Safety |
|---|------|------------|----------|--------|
| 1 | `jellyfin_library` | 15 | Library CRUD, scan, refresh, optimize, stats | MUTATING |
| 2 | `jellyfin_media` | 10 | Browse, search, detail, update, delete, stream info | READ_ONLY |
| 3 | `jellyfin_search` | 6 | Text search, advanced filter, people, studios, suggestions, saved | READ_ONLY |
| 4 | `jellyfin_playback` | 12 | Sessions, play, pause, stop, seek, skip, volume, subtitle, audio track, quality, transcode, report | MUTATING |
| 5 | `jellyfin_user` | 10 | List, create, update, delete, permissions, password, policy, sessions, activity, devices | MUTATING |

#### Advanced Tools

| # | Tool | Operations | Category | Safety |
|---|------|------------|----------|--------|
| 6 | `jellyfin_playlist` | 9 | List, create, update, delete, add_items, remove_items, reorder, share, export | MUTATING |
| 7 | `jellyfin_collections` | 7 | List, create, update, delete, add_items, remove_items, auto-tag | MUTATING |
| 8 | `jellyfin_metadata` | 10 | Get, update, refresh, identify, images, backdrops, providers, lock, unlock, fetch_external | MUTATING |
| 9 | `jellyfin_server` | 10 | Status, info, health, logs, restart, shutdown, updates, plugins, tasks, transcode_queue | MUTATING |
| 10 | `jellyfin_streaming` | 8 | Sessions, clients, transcode, bandwidth, direct_play, remote, LAN, kill_session | READ_ONLY |

#### Plugin & Integration Tools

| # | Tool | Operations | Category | Safety |
|---|------|------------|----------|--------|
| 11 | `jellyfin_plugin` | 8 | List, install, uninstall, enable, disable, configure, update, catalog | MUTATING |
| 12 | `jellyfin_arr_stack` | 6 | Radarr status, Sonarr status, Lidarr status, queue, history, sync | READ_ONLY |
| 13 | `jellyfin_subtitle` | 7 | Search, download, upload, delete, sync, offset, provider_config | MUTATING |
| 14 | `jellyfin_livetv` | 8 | Channels, guide, recordings, schedule, tuners, EPG, refresh, manage | READ_ONLY |
| 15 | `jellyfin_ffmpeg` | 6 | Transcode_profiles, performance, hardware_detect, path, test, benchmarks | DESTRUCTIVE |

#### AI / RAG / Enrichment Tools

| # | Tool | Operations | Category | Safety |
|---|------|------------|----------|--------|
| 16 | `jellyfin_enrichment` | 6 | TMDB, Wikipedia, MusicBrainz, OMDb, TVDB, batch_enrich | READ_ONLY |
| 17 | `jellyfin_rag` | 5 | Sync, search, status, reindex, purge | READ_ONLY |
| 18 | `jellyfin_reporting` | 8 | Library_stats, user_activity, popular, recent, genres, resolution, codec, export | READ_ONLY |
| 19 | `jellyfin_recommend` | 5 | Similar, genre_based, director, actor, watch_history | READ_ONLY |

#### Agentic & Help

| # | Tool | Operations | Category | Safety |
|---|------|------------|----------|--------|
| 20 | `jellyfin_agentic` | 3 | Workflow, natural_query, batch_operation | MUTATING |
| 21 | `jellyfin_help` | 6 | Discover, tool_help, status, tips, quickstart, faq | READ_ONLY |
| 22 | `jellyfin_integration` | 5 | Export_plex, import_plex, sync_watchstate, backup, restore | DESTRUCTIVE |

### 3.2 Jellyfin++ Features (Plugin-Enhanced)

What makes this "Jellyfin++" — capabilities unique to Jellyfin's open plugin architecture:

| Feature | Implementation | Plex Equivalent |
|---------|---------------|-----------------|
| **Intro Skip** | Configuration as MCP tool, per-library control | Plex Pass only |
| **Custom metadata providers** | Plugin install/configure via MCP | Not possible (Plex closed) |
| **Webhook automation** | MCP configures webhook plugins for arr-stack sync | Partial, brittle |
| **Themes/skins** | MCP manages theme plugins | Not possible |
| **Custom auth** | LDAP/JWT plugin management via MCP | Plex Home locked |
| **Transcode profiles** | Per-user/per-device via MCP, no paywall | Plex Pass only |
| **Library segments** | Dynamic smart collections based on MCP queries | Manual only |

---

## 4. Webapp Design

### 4.1 Pages

| Page | Route | Description | Plex-mcp Analog |
|------|-------|-------------|-----------------|
| Overview | `/` | Server health, recent activity, arr-stack status, plugin health | `/overview` |
| Library Browser | `/libraries` | Library list with type badges, item counts, scan status | `/libraries` |
| Media Grid | `/media/{type}` | Poster grid for movies/shows/music, filter bar, pagination | `/movies` |
| Media Detail | `/media/{type}/{id}` | Full metadata, artwork, cast, similar, streaming info, Play button | MovieMetadataModal |
| Search | `/search` | Text + advanced filters + semantic (RAG) tab | `/search` |
| Playback Dashboard | `/playback` | Active sessions, transcode queue, bandwidth monitor | — (plex-mcp missing) |
| Plugins | `/plugins` | Plugin catalog, installed list, configure per-plugin | — (unique to Jellyfin) |
| Live TV | `/livetv` | EPG grid, recordings, tuner status | — (unique to Jellyfin) |
| Users | `/users` | User list, permissions, sessions, watch history | — |
| Settings | `/settings` | Jellyfin URL/token, LLM config, RAG indexing, backup | `/settings` |
| RAG | `/rag` | Semantic search, indexing progress, reindex controls | `/rag` |
| Chat | `/chat` | LLM-powered natural language media queries | `/chat` |
| Help | `/help` | Tool reference, quickstart, FAQ | `/help` |

### 4.2 Key UX Differentiators vs Plex-mcp

1. **Plugin management UI** — no Plex equivalent exists
2. **Live transcode monitor** — real-time via WebSocket, no polling
3. **EPG grid** — Live TV guide, unique to Jellyfin
4. **Hardware transcode status** — GPU utilization, free for all users
5. **Plugin health dashboard** — status, version, compatibility per plugin

---

## 5. Architecture Parallels with plex-mcp

| Component | plex-mcp | jellyfin-mcp |
|-----------|----------|--------------|
| **Language** | Python 3.12+ | Python 3.12+ |
| **MCP Framework** | FastMCP 3.2+ | FastMCP 3.2+ |
| **Build system** | uv + hatchling | uv + hatchling |
| **Media SDK** | `plexapi` (4.15+) | `jellyfin-apiclient-python` (official) |
| **Backend framework** | FastAPI + uvicorn | FastAPI + uvicorn |
| **Frontend** | Next.js 15.2, React 18, Tailwind 3 | Next.js 15.2, React 18, Tailwind 3 |
| **Vector DB (RAG)** | LanceDB + sentence-transformers | LanceDB + sentence-transformers |
| **Lint/Format** | Ruff (Python), Biome (JS/TS) | Ruff (Python), Biome (JS/TS) |
| **E2E testing** | Playwright | Playwright |
| **Tool pattern** | Portmanteau (operation: Literal[...]) | Portmanteau (operation: Literal[...]) |
| **Ports** | Backend 10740, Frontend 10741 | Backend 10934, Frontend 10935 |
| **Transport** | STDIO + HTTP + SSE | STDIO + HTTP + SSE + WebSocket |
| **Native wrapper** | Tauri 2.0 (planned) | Tauri 2.0 (planned) |

### Key Architecture Divergences

1. **WebSocket layer** — Jellyfin has a native WebSocket API for real-time session/playback/transcode events. This enables a live dashboard that Plex can't match without polling.

2. **Plugin SDK** — Jellyfin plugins expose their own API endpoints. The MCP server can introspect and wrap plugin APIs dynamically.

3. **No cloud auth** — Jellyfin auth is local (user/pass or API key). No dependency on an external auth provider. This simplifies the MCP server and makes it fully air-gappable.

4. **OpenAPI auto-discovery** — Jellyfin exposes a complete Swagger spec. Tools can be partially generated from the spec rather than manually maintained.

---

## 6. Implementation Plan

### Phase 1: Core MCP Server (Week 1)
- JellyfinService class wrapping `jellyfin-apiclient-python`
- FastMCP instance with lifespan
- 5 core portmanteau tools (library, media, search, playback, user)
- STDIO transport for Claude Desktop
- Configuration via env vars (`JELLYFIN_URL`, `JELLYFIN_API_KEY`)

### Phase 2: Advanced MCP Tools (Week 2)
- Remaining 12 portmanteau tools
- WebSocket event bridge for real-time notifications
- Plugin introspection and management
- Agentic tools with FastMCP sampling

### Phase 3: Webapp (Week 3)
- FastAPI backend with REST API
- Next.js frontend with all 13 pages
- WebSocket proxy for live playback dashboard
- RAG semantic search with LanceDB

### Phase 4: Polish & Native (Week 4)
- E2E Playwright tests
- Tauri 2.0 native wrapper
- Plugin catalog integration
- Plex import/export tooling

---

## 7. Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| `jellyfin-apiclient-python` missing endpoints | Medium | Fallback to raw HTTP via httpx; contribute upstream |
| Jellyfin API version churn | Low | OpenAPI spec is stable; pin target versions |
| WebSocket complexity | Medium | Use aiohttp for WS; separate event bridge service |
| Plugin API fragmentation | Medium | Start with top-10 plugins; generic passthrough for rest |
| No Plex-level client ecosystem | Low | Jellyfin has clients for all major platforms; web player is excellent |

---

## 8. Success Metrics

- All 22 portmanteau tools operational via Claude Desktop
- WebSocket live playback dashboard real-time (<1s latency)
- Plugin management (install/configure/uninstall) works for top-10 plugins
- Semantic search indexes 10k+ items under 30 seconds
- E2E tests pass on clean checkout
- Native Tauri installer <15 MB

---

## Appendix A: Jellyfin API Key Acquisition

Unlike Plex (which requires extracting a token from browser devtools), Jellyfin provides API keys directly:

```
Dashboard → Users → (user) → API Keys → Create Key
```

Or via curl:
```bash
curl -X POST "http://jellyfin:8096/Users/AuthenticateByName" \
  -H "Content-Type: application/json" \
  -H "X-Emby-Authorization: MediaBrowser Client=\"jellyfin-mcp\", Device=\"server\", DeviceId=\"mcp-001\", Version=\"1.0\"" \
  -d '{"Username": "youruser", "Pw": ""}'
```

---

## Appendix B: Fleet Port Registration

| Port | Service | Transport |
|------|---------|-----------|
| **10934** | jellyfin-mcp Backend | FastAPI + FastMCP HTTP `/mcp` + WebSocket `/ws` |
| **10935** | jellyfin-mcp Frontend | Vite/Next.js dev (proxies `/api` → 10934) |

---

*Last updated: 2026-05-21 — Pre-implementation phase*
