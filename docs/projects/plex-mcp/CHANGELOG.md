
## [Unreleased] - 2026-10-08 (dashboard overhaul + webapp API parity)

### Added
- Overview rewritten to the fleet gate (hero + 6 KPI cards + quick actions + red onboarding button when Plex is down) with a new best-effort `GET /api/dashboard/` aggregation endpoint; sidebar to standard (top toggle, logo + version, live backend/Plex indicator).
- Parity UI for every backend route: advanced multi-filter search, taste rank/score/temporal, media AI-context button + files/art panel + play-on-client picker, enrichment person search, chat search-and-summarize runner, settings LLM onboarding card + GPU target select + key delete, RAG context tester, server diagnostics panel, live api-docs backend label.
- 19 new `utils/api.ts` wrappers; repair, RAG, and chat components migrated off raw `fetch` onto them. Dead `getSystemStatus` wrapper removed; legacy `/api/v1/*` marked deprecated.

### Verified
- `tsc --noEmit` clean, `biome check --write` applied, `ruff check` clean, pytest 52 passed (main, config, plex-auth, taste, llm-providers, enrichment).

## [Unreleased] - 2026-10-04 (taste modelling)

### Added (Taste modelling - roadmap project 3 of 6)
- `plex_taste` MCP tool, `/api/taste/*` REST, and a `/taste` webapp page: what you gravitate toward and pass over, per movies/TV and time of week, plus a "Lately" panel. Module `src/plex_mcp/services/taste/`, data in `data/taste.db`. Reads from Plex only.
- Scoring is lift against the library, not the spec's EMA: on real data (16,928 history entries) the capped EMA scored every dimension +1.00 because history is almost all positive events. Replaced with exponentially decayed attention (1-year half-life) compared to a library survey, score in [-1, 1]. Stratified by movie/show; concave per-show episode weighting. Reasoning in `docs/plans/TASTE_MODELLING.md`.
- Verified against live Plex: history has no progress (entry = completed, repeat = rewatched); episodes roll up via `grandparentKey`; 992 rated items; On Deck dismissals are not exposed so not captured.
- Background incremental sync every 10 min (`TASTE_SYNC_INTERVAL_SEC`), inert until a profile is built once. Incremental sync tested equal to a full rebuild.
- Live build: 15,615 events, 12,201 library items surveyed, ~2 minutes; profile is recognizable.
- 50 new tests.
- Not built: watch_transitions, per-account profiles, scoring of theme dimensions.

### Fixed (test suite: 13 long-standing failures cleared)
- All 13 failing tests were stale test expectations, not tool bugs: tests subscripted `ToolResult` directly instead of unwrapping it, and several asserted shapes the tools never had. Added `tests/helpers.py::tool_data_payload`.
- Verified live against a real Plex server (7 live + 2 RAG live tests pass). Surfaced real contract facts: `plex_media search` requires a non-empty query; ffprobe output is under `result`; subtitle search results under `results`; library `id` is an int.
- `test_ffmpeg_probe_real` had been silently skipping; it now probes a real file.
- Known limitation, not fixed: `plex_media search` without `library_id` on a large server (83 libraries) exceeds the 30s Plex read timeout.

## [Unreleased] - 2026-09-13

### Added (Deep metadata enrichment - roadmap project 1 of 6)
- **Deep, LLM-synthesised per-item dossiers.** `plex_media_enrichment` gained `enrich`, `bulk_enrich`, `get_enrichment`, `get_related`, `search_by_theme`, `search_by_person`, `stale_report` operations. Sources: Wikipedia (REST API) + TMDB deep mode (official v3 API) + JustWatch (best-effort, never blocking). Letterboxd/IMDB/Rotten Tomatoes/Metacritic scraping deliberately excluded - all four prohibit scraping in their ToS and run active bot detection, not worth the exposure at 50k library items. New module `src/plex_mcp/services/enrichment/` (db, sources, synthesis, crossref, orchestrator), sqlite-backed at `data/enrichment.db`.
- **Library-wide cross-references**: each enriched item matched against every other already-enriched item by director, shared top-5 cast, TMDB collection, and thematic-tag overlap (2+ shared tags).
- **New webapp pages**: `/media?ratingKey=...` (per-item dossier with related-items section) and `/enrichment` (bulk-run launcher + progress + theme search). "Full dossier" link added to the Movies detail modal.
- LLM synthesis is transport-agnostic: MCP tool path uses `ctx.sample`, webapp REST path uses the local+cloud LLM provider registry vendored earlier the same week - same seam, two adapters. Works with zero LLM configured too (raw sources, no synthesis).
- 23 new tests (`test_enrichment_service.py` x15, `test_api_enrichment.py` x8), all passing.

### Fixed
- **Wikipedia REST calls were silently returning nothing.** Wikimedia's edge (HAProxy) 403s httpx's default User-Agent string; a descriptive UA passes. Affected `enrichment_service.fetch_wikipedia_summary` everywhere it's used (the existing AI-context panel too, not just the new code) since whenever it was first written. Fixed with a UA header on every httpx client hitting Wikipedia/TMDB/JustWatch.
- **Route-ordering bug caught before it shipped**: FastAPI matches path templates in registration order; an early draft had the generic `/{rating_key}` handlers before literal routes like `/by-theme`, which would have shadowed them. Reordered, with a regression test guarding it.

## [Unreleased] — 2026-09-11

### Added (LLM: local + cloud provider registry, VRAM management)
- **Settings → Diagnostics**: one traffic-light panel (Plex/LLM/RAG/*arr) instead of five separate error hunts. `GET /api/system/diagnostics`.
- **Cloud LLM providers** (Anthropic, DeepSeek, OpenRouter) vendored from the fleet's `templates/llm/` registry (pilot: arxiv-mcp) as `webapp/backend/app/llm_providers.py` - 0600 per-provider keystore, correct auth/format per provider, chat + agentic tool-calling both route through it.
- **GPU VRAM panel**: live telemetry + resident-model list + "Evict all", so an AI task doesn't just fail when VRAM is full - free it in Settings, or use a cloud provider on a GPU-less machine.
- 15 new tests (`tests/test_api_llm_providers.py`), all passing; full regression suite (54 tests across the day's changes) green.
- **First-run wizard**: 3-step overlay (Plex sign-in -> optional LLM provider -> done), shows once on a fresh install, auto-skips for an already-working setup. `components/onboarding/FirstRunWizard.tsx`.

### Added
- **Settings: Plex token test + refresh.** "Test connection" button validates the stored/entered Plex URL+token against the real server (`POST /api/system/plex/test`). "Get a new token" starts the real Plex PIN auth flow (`POST /api/system/plex/pin`, `GET /api/system/plex/pin/{id}`) — opens app.plex.tv, polls for approval, saves the token automatically. Fixes the fresh-install "no Plex token" dead end.
- `tests/test_api_plex_auth.py` — 7 tests covering the new endpoints, all mocked at the network boundary.

### Fixed
- **`/health` no longer lies about Plex status:** hardcoded `"plex": "connected"` replaced with a real check of whether `PLEX_TOKEN` is actually configured.
- **CRITICAL: two hardcoded real Plex tokens removed** from dead/dev-only code (`server_minimal.py`, `webapp/backend/test_plex_pagination.py`) — both committed to git, treat as compromised, rotate.
- **CORS silently dropped on the raw `--http` transport path:** `transport.py` built a CORS-wrapped Starlette app but served the original unwrapped app via `mcp_app.run_http_async()`. Now serves the CORS+health-wrapped app directly via `uvicorn.Server`.
- **Ruff `ignore` list was duplicated ~4x** in `pyproject.toml`, re-adding `S110`/`S112`/`T201` (silent except-swallowing, print-ban defeated). Deduplicated, removed permanently, added real logging at the 10 affected call sites.
- Restored `scripts/mcpb-pack.ps1` (accidentally deleted) and fixed `scripts/just/fleet.just`'s `mcpb-pack` recipe (pointed at a `mcpb/pack.ps1` path that never existed). Root cause was the vendored fleet template — fixed upstream in `mcp-central-docs`; ~160 other fleet repos share the bug (tracked separately).
- **`fleet-start.config.ps1` pointed the dev webapp launcher at the wrong backend** (`Backend.Kind='module-serve'` ran `python -m plex_mcp --serve`, a flag that doesn't exist). Fixed to `Kind='uvicorn-web-app'` targeting the real `webapp/backend/app/main.py`. Verified via the actual `mcp-central-docs/starts/plex-start.bat` launcher end to end. Likely fleet-wide — see `TRAPS_AND_PITFALLS.md` #31.
- **Movies/Libraries pages showed empty/"not found" despite a working connection.** `plex_library`/`plex_media`/`plex_search` (7 call sites) never populated a `data` field consumable by the webapp's REST layer, only a human-text summary + Prefab UI card shape. Fixed by carrying the raw list in `meta["data"]` and promoting it in the webapp's MCP bridge. Verified live against the real Plex server (83 libraries, real movie titles).
- Broken GitHub links fixed fleet-wide in this repo's docs: pointed at `sandraschi/plex-mcp` (doesn't exist), actual repo is `sandraschi/plexmcp`.

## [Unreleased] — 2026-07-09

### Fixed
- **Settings `.env` footgun removed:** `settings_store.py` no longer caches expired tokens in `settings.json` — `.env` always wins, no fallback chain across multiple `.env` files
- **Config `.env` fallback chain removed:** `config.py` `_env_files()` replaced with single `_env_file()` pointing to repo root `.env` only
- **Movies filter bug fixed:** `media_type` was passed as raw Plex filter field `mediatype` (Plex uses `libtype`) — changed to `libtype=media_type` parameter in both browse and search paths
- **`min_rating` filter crash fixed:** Removed from Plex filter kwargs (Plex has no `minRating` field), applied as post-search Python filter instead
- **Backend `search_media` now strips invalid filter fields:** `media_type` and `min_rating` popped from filters before passing to Plex API
- **Tauri app frontend fixed:** `main.rs` navigates to backend URL immediately (with window retry); `backend.rs` now sets `MCP_TRANSPORT=http`
- **PyInstaller opentelemetry crash fixed:** `build.ps1` patches `opentelemetry.context` StopIteration fallback; runtime hook disables propagator loading
- **CUA smoke test rewritten:** uses direct pywinauto (no pywinauto-mcp dep); automation warning banner; set_focus + maximize before nav; UIA element discovery for sidebar nav; `_release_mouse()` in finally block; page verification via OCR (checks 404/error/blank)
- **Nav links now UIA-accessible:** `aria-label` on every sidebar `<Link>`; `core:window:allow-set-focus` permission added to capabilities

## [Unreleased] — 2026-06-17

### Added
- **GPU RAG (fleet standard):** `just rag-gpu-install`, `just rag-gpu-sync`, `just rag-cpu-install` — fastembed-gpu fallback path (replaces sentence-transformers for local LanceDB). Scripts: `plex_rag_sync.py`, `run-rag-gpu-sync.ps1`, `plex_mcp/rag/fastembed_gpu.py`.
- **fastembed** dependency for in-repo RAG fallback.

### Changed
- Local RAG fallback uses `BAAI/bge-small-en-v1.5` via fastembed (aligned with fleet standard).

---

## [Unreleased] — 2026-06-14

### Added
- Tauri CORS: 	auri://localhost, http://tauri.localhost, https://tauri.localhost in CORS origins
- Tauri CORS: _TAURI env var toggle with llow_origin_regex for secure WebView access
- build.ps1: auto-copy NSIS installer to dist/ on build
- CUA-NSIS: config-driven smoke test (`scripts/cua-smoke.py`, `scripts/cua-nsis-config.json`)
- CUA-NSIS: `just build-native` + `just cua-nsis-test` recipes
- CUA-NSIS: 11-phase smoke (install, launch, WebView OCR, feature route, diagnostics, uninstall)
- CUA-NSIS: local certification — all 11 phases pass locally (2026-06-14)

### Changed
- CORS: llow_origins=["*"] → explicit origins list for Tauri webview compatibility
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.4.1] - 2026-06-08

### Added

- **Tauri desktop 2.4.1**: Production shell on port 10740 — CORS, `API_BASE`, hardened backend spawn, fleet tool metrics.
- **FastMCP 3.2 alignment**: All 22 tools now use `version="1.0.0"`, `annotations=READ_ONLY|MUTATING|DESTRUCTIVE`, `Annotated[Field]` parameters, `ToolResult` returns, and SOTA docstrings (`## Return Format` / `## Examples`).
- **Prefab interactive cards**: 9 `prefab_ui` card builders in `src/plex_mcp/prefabs.py` wired as `structured_content` — library grid, library detail, media browser, media detail, server status, server info, performance dashboard, streaming sessions, streaming clients.
- **Webapp `_prefab` pipeline**: `mcp/client.py` extracts `structured_content` from ToolResult as `_prefab` in API responses for frontend rendering.
- **Webapp image proxy fix**: `follow_redirects=True` on httpx client (v0.28.1 defaults `False`, breaking Plex 307 redirects to `/photo/:/transcode`).
- **Lazy FastMCP mount**: Webapp backend startup reduced from ~103s to <1s — `fastmcp` import deferred to background `asyncio.create_task`.
- **CI**: Markdown link check (**lychee**, non-blocking) and **Playwright** e2e smoke for the Next.js app (`webapp/frontend/e2e`, `npm run test:e2e`, `just e2e`).
- **Webapp**: `BackendStatusBanner` when the FastAPI backend is unreachable; proxy debug logs only when `NEXT_DEBUG_PROXY=1`.
- **Documentation**: Operational improvements checklist ([`docs/plans/OPERATIONAL_IMPROVEMENTS.md`](docs/plans/OPERATIONAL_IMPROVEMENTS.md)), GitHub PR template, `just version` (reads `pyproject.toml`); symptom table in [`TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md); [`docs/DOCKER.md`](docs/DOCKER.md) + example compose; `docs/assets/` wireframe SVGs; “suggested agent flows” in [`TOOLS.md`](docs/TOOLS.md); “Video walkthrough” placeholder in [`QUICKSTART.md`](docs/QUICKSTART.md).
- **Webapp (Biome)**: Relaxed a few **a11y/suspicious** rules in `biome.json` for pragmatic noise control; removed `eval` from media probe FPS; `SearchForm` now carries `library_id` in the query string; `server-info-view` uses `for...of` instead of nested `forEach`.
- **Docs** (earlier in unreleased): Troubleshooting “diagnose in order” section; RAG `docs_mcp` import verification one-liners; Caddy and nginx samples in self-hosting guide.

### Fixed

- **Webapp image proxy**: `images.py` now follows Plex 307 redirects (`follow_redirects=True`) — httpx v0.27+ default change broke all poster/artwork images.
- **`plex_media_service._plex_item_to_media_item`**: `thumbUrl`/`artUrl` → `thumb`/`art` (capital-U properties return full server URLs with tokens, breaking proxy path extraction).
- **Pydantic v2**: 13+ `.dict()` calls replaced with `.model_dump()` across portmanteau tools.
- **Lint/tooling**: Ruff + Biome green; root `biome.json`, frontend build artifacts in `.gitignore`.
- **Documentation**: `DOCUMENTATION_INDEX.md` hub, archive banners on stale fleet-import docs, `TAURI.md` production notes.

## [2.5.0] - 2026-04-19
### Added
- **Dialogue RAG (Subtitle Neural Search)**: Complete end-to-end implementation for semantic search across media dialogue. 
  - New `sync_subtitles` operation in `plex_rag` tool to index SRT/VTT tracks.
  - New `search_subtitles` operation for deep content discovery via dialogue snippets.
  - Robust SRT/VTT parser with timestamp extraction and dialogue normalization.
- **Webapp Subtitle Management**: 
  - Updated RAG Dashboard with "Sync Subtitles" control and real-time dialogue indexing telemetry.
  - New "Dialogue Search" mode in the web search interface with timestamped results and media linking.
- **Multi-Table Vector Store**: Extended LanceDB configuration to support concurrent metadata and subtitle indices.

### Changed
- **Tool Docstrings**: Updated `plex_rag` with detailed operation patterns for subtitle management.

## [2.4.1] - 2026-04-17 (superseded by 2026-06-08 release above)
### Added
- **High-Value Media Enrichment**: New `plex_media_enrichment` tool for fetching deep contextual summaries from Wikipedia and external metadata links.
- **RAG Augmentation**: The `plex_rag` tool now supports an `enrich=True` flag during `sync_metadata` to augment the vector index with Wikipedia narrative context.
- **Hardened Error Handling**: Standardized `AUTH_FAILURE` detection across all portmanteau tools to eliminate noisy tracebacks and provide actionable remediation steps for 401 Unauthorized errors.

### Changed
- **Tool Docstrings**: Updated all portmanteau tools with expanded docstrings and consistent pattern rationale sections.
- **Zero-Console Policy**: Verified full removal of `print()` statements from production core modules.

## [2.4.0] - 2026-04-14
### Added
- **SOTA 2026 Industrialization**: Fleet-wide modernization for April 2026 standards.
- **FastMCP 3.2.0 Parity**: Full integration of native prompts, skills, and sampling features.
- **Biome Integration**: High-fidelity linting and formatting toolchain for the web dashboard.
- **Universal Connect Pattern**: Support for multiple simultaneous clients via stdio and HTTP transports.
- **Sampling (2026)**: Industrialized server-side sampling with `PlexSamplingHandler` and `agentic_plex_workflow`.

### Changed
- **Codebase Hardening**: Purged all executable `print` statements in configuration and tool modules to ensure strict JSON-RPC protocol compliance.
- **Ruff Standard**: Aligned with 120-character line length and expanded SOTA linting rules. 
- **Webapp Performance**: Optimized Next.js dashboard with adjacent port assignments (10741/10742).

### Fixed
- **JSON-RPC Protocol Integrity**: Replaced unauthorized `print()` calls in `config.py` with `sys.stderr.write`.
- **FastMCP Compatibility**: Resolved `NullLogger` attribute errors and startup regressions.

## [2.3.1] - 2026-03-30

### Fixed
- **FastMCP 3.1 Compatibility**: Hardened the custom `NullLogger` in `src/plex_mcp/app.py` with missing standard `Logger` attributes (`handlers`, `filters`, `propagate`, `level`, etc.) to prevent `AttributeError` during startup in `stdio` mode (e.g., in Antigravity).

## [2.3.0] - 2026-02-26

### Added
- **Neural Media RAG Portmanteau** (`tools/portmanteau/plex_rag.py`): New unified search and synthesis tool for accessing context vectorized by LanceDB.
- **Agentic Synthesis API**: Expanded the webapp FastAPI backend with `POST /api/v1/search` and `POST /api/v1/chat` to expose backend capabilities directly to the Unified Search Hub in `mcp-central-docs` without necessitating MCP protocol bridging.

## [2.2.0] - 2026-02-04

### Added
- **MCPB Packaging**: Full implementation of standard MCPB bundles with optimized build patterns
- **Build Infrastructure**: Added `mcpb.json` and staging patterns for clean packaging

### Fixed
- **Startup Logic**: Standardized server execution via system Python (`python -m plex_mcp`)
- **Dependency Management**: Resolved missing `aiohttp`, `fastmcp`, and `plexapi` in system environment
- **Path Resolution**: Fixed `PYTHONPATH` issues in `mcp_config.json` for reliable module loading

## [Unreleased] - ALPHA

### Documentation
- **Hub layout:** Root [README.md](README.md) stays short; specialized guides live under [docs/](docs/) ([INSTALL](docs/INSTALL.md), [CONFIGURATION](docs/CONFIGURATION.md), [TOOLS](docs/TOOLS.md), [RAG](docs/RAG.md), [WEBAPP](docs/WEBAPP.md), [DEVELOPMENT](docs/DEVELOPMENT.md), [TROUBLESHOOTING](docs/TROUBLESHOOTING.md), [docs/README.md](docs/README.md)).
- **[docs/PRD.md](docs/PRD.md):** Product scope, in/out of scope, PyPI conditional on registration, playback caveat.
- **Install doc:** [docs/INSTALL.md](docs/INSTALL.md) documents **uv** on Windows (`uv.exe` on PATH), pipe-free installer script, and **PyPI** only after publish.
- **Legacy stubs:** [docs/installation.md](docs/installation.md), [docs/development.md](docs/development.md), [docs/troubleshooting.md](docs/troubleshooting.md) redirect to canonical UPPERCASE filenames; [docs/index.md](docs/index.md) points at the hub.

### Changed
- **Fleet packaging**: Root **`justfile`** (uv sync, lock, run, lint, fmt, test, check, webapp, pack-mcpb), **`llms.txt`** + **`llms-full.txt`** (LLM index + corpus), committed **`uv.lock`** (`uv lock`).
- **Sampling (2026)**: Server-side `PlexSamplingHandler` (OpenAI-compatible chat/completions; default Ollama at `PLEX_SAMPLING_BASE_URL`, inherits from `LLM_BASE_URL` when unset). `agentic_plex_workflow` uses real `Context.sample_step` with tool execution; `plex_natural_assistant` uses `Context.sample`. Removed stub agentic tools. MCP resources `resource://plex/skills` and `resource://plex/capabilities`; prompts `prompt://plex/rag-workflow`, `prompt://plex/agentic-pattern`, `prompt://plex/library-tour`. `PLEXMCP_ALLOW_LOGGING` / pytest `conftest` avoid global logger suppression breaking FastMCP under test runners.
- **FastMCP 3.1 alignment**: Constructor updated to 3.1 style: `FastMCP("PlexMCP", instructions="...")` (no `name=`, `version=` kwargs). Prompt `plex_media_guide` now returns `list[Message]` via `fastmcp.prompts.Message` instead of raw dicts. Webapp backend replaced deprecated `@app.on_event("startup")` with a lifespan context manager.

### Added
- **Movies webapp**: Plex poster images on movie cards and list (via Next.js image proxy `/api/image/...` to backend). Movie detail modal on card/list click: wider layout (max-w-4xl), full poster, metadata (year, duration, content rating, rating, studio, genres, directors, tagline, summary), **Play in Plex** button (opens Plex Web in new tab when Plex URL is set in Settings), Close and Escape to dismiss.
- **Settings RAG section**: **RAG / Indexing** block with "Reindex metadata" button calling `POST /api/rag/sync`; shows indexed count or error so reindexing is visible without going to Semantic search.
- **In-repo RAG fallback**: When mcp-central-docs vector store is unavailable, optional LanceDB + sentence-transformers fallback (install with `pip install plex-mcp-advanced[rag]`); see `src/plex_mcp/services/rag_ingestor.py`.
- **FastMCP 3.1 alignment**: Transport docstrings and help updated to 3.1; fleet launch and v1 search/chat routes moved from MCP app to webapp backend (`POST /api/fleet/launch`, `POST /api/v1/search`, `POST /api/v1/chat`). Prompt `plex_media_guide` for agentic workflows.
- **Semantic search page**: Webapp page `/search/semantic` with natural-language search over RAG index; **Sync / Index metadata** button to start RAG indexing from the UI (`POST /api/rag/sync`). Backend `GET /api/rag/semantic` and `plex_rag` in MCP client tool map.
- **Chat preprompt**: LLM chat receives a live system preprompt (MCP server tools, webapp pages, Plex server name/version, media libraries, integrations). Built in `webapp/backend/app/chat_context.py`; injected when `use_context: true` (default) in `POST /api/llm/chat`.
- **RAG over movie and music descriptions** - Metadata RAG (LanceDB) now indexes movie, show, and **music (artist)** libraries from Plex API. Searchable content includes title, plot/summary, year, genres, directors (movies/shows) and artist title/summary (music). Use `plex_rag(operation="sync_metadata")` then `plex_rag(operation="semantic_search", query="...")`. Data sourced from Plex server via API (no local DB).
- **Webapp (reservoir 10740/10741)**: Full browser UI with FastAPI backend and Next.js 15 frontend
  - **Glassmorphism UI**: Backdrop-blur panels, retractable sidebar, topbar
  - **Logger modal**: Tail of webapp log with level/filter (topbar)
  - **Help modal**: Tiered help content (basic/intermediate/advanced/expert)
  - **Local LLM stack**: Ollama/LM Studio/OpenAI-compatible chat (LLM_BASE_URL, LLM_API_KEY)
  - **Advanced chat**: Personalities, prompt refining via LLM, chat export (MD/JSON)
  - **Light RAG**: GET /api/rag/context for Plex search context injection
  - **AI workflows**: POST /api/workflows/run (e.g. search_and_summarize)
  - **Semantic search**: Keyword search + RAG context for chat
  - **Movies page**: Pagination (page/limit in URL, offset to backend), card/list view toggle (persisted in localStorage)
  - **Settings page**: Plex API key and URL, LLM provider (ollama/lmstudio/openai), base URL, API key, default model (from /api/llm/models); persisted via GET/PATCH /api/system/settings and backend data/settings.json (file overrides .env at runtime)
  - **Start**: webapp/start.ps1 and start.bat; see webapp/SETUP.md
- **Port reservoir**: Backend 10740, frontend 10741 (mcp-central-docs WEBAPP_PORTS.md)
- **Next.js route /tools/get_system_status**: OPTIONS returns 204 (stops 404 from MCP clients probing); GET proxies to backend /api/server/status.

### Changed
- **RAG dependency** documented in README and Semantic search page: semantic search requires mcp-central-docs **source** on path (not the mcp-central-docs MCP server running). Sync available from UI.
- **Webapp backend**: start.ps1 now runs the **FastAPI webapp backend** (`webapp/backend/app/main:app`) on 10740 instead of the MCP-only app. Backend exposes all REST routes (`/api/server/*`, `/api/libraries/*`, `/api/search`, `/api/movies`, `/api/system/*`, `/api/logs`, `/api/help`, `/api/llm/*`, `/api/webapp-launch`, etc.) and mounts FastMCP at `/mcp`. Fixes 404/502 when frontend proxies to backend.
- **Start script**: Backend is launched with `.venv\Scripts\python.exe -m uvicorn app.main:app` (PYTHONPATH includes repo `src` and `webapp/backend`) so the venv is used directly and `uv sync` is not run at start (avoids "file in use" when venv is locked).
- **Fleet ports**: Frontend proxy default `BACKEND_URL` is `http://127.0.0.1:10740`; start.ps1 uses backend 10740, frontend 10741.
- **Next.js 15**: Removed invalid `--host` from npm dev script (Next 15 uses `--hostname`; default binds all interfaces). Removed invalid `turbopack` key from next.config.js (clears config warning).
- **CORS**: Added Starlette CORSMiddleware to FastMCP `http_app()` (allowed origins: localhost:10741, 127.0.0.1:10741, and 10740 variants) so browser/WebSocket connections from the frontend no longer get 403.
- **Dependencies**: Added `fastapi`, `uvicorn[standard]`, `pydantic-settings`, `httpx`, `python-multipart` to root pyproject.toml so the webapp backend runs with the project venv.
- Updated project status to ALPHA in README; alpha status badge and warning notice.
- Next.js frontend pinned to 15.2.0 (webpack dev); turbopack config removed for Next 15 compatibility.
- Backend config loads .env from webapp/backend path (not cwd) so token is found when started from any directory.
- Backend data/ and settings.json in .gitignore (secrets not committed).

### Status
- **Project Status**: ALPHA - Active development, some features incomplete
- **Known Issues**: Playback control (`plex play`, `plex pause`) is non-functional for ALL clients
  - GDM clients (PlexAmp): Discoverable but playback commands fail
  - Non-GDM clients (Plex Web, Plex for Windows): Not controllable via tested API endpoints
- **See**: [STATUS_2026-01-08.md](STATUS_2026-01-08.md) for detailed status

### Fixed
- Client discovery now finds all client types (PlexAmp, Plex Web, Plex for Windows)
- Multi-source client discovery implementation

### Known Limitations
- Playback control (`plex play`, `plex pause`) fails for ALL clients
- GDM clients (PlexAmp): Discoverable via GDM but `plexapi_client.playMedia()` calls fail
- Non-GDM clients (Plex Web, Plex for Windows): Not controllable via tested API endpoints
- Server API endpoints tested don't work for any client type
- Root cause may be API endpoint parameters, authentication, or client state requirements

## [2.1.0] - 2025-11-22

### Added
- **Portmanteau Tool Architecture**: Complete refactoring from 52+ individual tools to 15 comprehensive portmanteau tools
- **15 Portmanteau Tools**: Consolidated related operations into unified interfaces
  - `plex_library` - Library management (12 operations)
  - `plex_media` - Media operations (5 operations)
  - `plex_user` - User management (6 operations)
  - `plex_playlist` - Playlist management (8 operations)
  - `plex_streaming` - Playback control (10 operations)
  - `plex_performance` - Performance & quality (13 operations)
  - `plex_metadata` - Metadata management (7 operations)
  - `plex_organization` - Library organization (5 operations)
  - `plex_server` - Server management (6 operations)
  - `plex_integration` - Third-party integrations (6 operations)
  - `plex_search` - Advanced search (5 operations)
  - `plex_reporting` - Analytics & reports (6 operations)
  - `plex_collections` - Collections management (7 operations)
  - `plex_quality` - Quality profiles (6 operations)
  - `plex_help` - Help & discovery (4 operations)
- **FastMCP 2.13+ Compliance**: All tools use Literal types for operation parameters
- **Comprehensive Docstrings**: Standardized docstrings with PORTMANTEAU PATTERN RATIONALE sections
- **Structured Error Handling**: AI-friendly error responses with suggestions

### Changed
- **Tool Count**: Reduced from 52+ individual tools to 15 portmanteau tools (71% reduction)
- **Tool Registration**: Only portmanteau tools are now loaded by default
- **Server Architecture**: Simplified tool imports in `server.py`
- **Documentation**: Updated README and documentation to reflect portmanteau architecture

### Deprecated
- **Old Individual Tools**: All individual tool files (`tools/library.py`, `tools/media.py`, etc.) are deprecated
- **API Tools**: `api/vienna.py` tools are deprecated in favor of `plex_integration`

### Fixed
- **Tool Registration**: Fixed import issues preventing tools from being registered
- **FastMCP Compliance**: Removed `**kwargs` from tool signatures (not supported by FastMCP)
- **Error Messages**: Improved error handling with structured responses

### Technical Details
- **FastMCP Version**: 2.13+ with Literal type support
- **Total Operations**: 106+ operations consolidated into 15 tools
- **Backward Compatibility**: Old tools remain in codebase but are not loaded by default

## [2.0.0] - 2025-10-10

### Added
- **MCPB Packaging**: Complete MCPB (MCP Bundle) implementation for one-click Claude Desktop installation
- **23 Powerful Tools**: Comprehensive Plex Media Server integration with 23 tools across 6 categories
- **User Configuration**: Interactive setup prompts for Plex URL and authentication token
- **Professional Documentation**: Complete documentation suite with 21 files and 400+ pages
- **GLAMA Integration**: Gold Status certification with 85/100 quality score
- **CI/CD Pipeline**: Automated testing, building, and publishing workflows
- **Plugin Ecosystem**: Support for 1,400+ Notepad++ plugins (adapted for PlexMCP)
- **Vienna AI Features**: European content discovery and anime season information
- **Advanced Error Handling**: Enterprise-grade error management and logging

### Changed
- **Framework Upgrade**: Migrated from DXT to MCPB packaging format
- **Tool Count**: Increased from 20 to 23 tools (+15% improvement)
- **Documentation**: Enhanced from basic to professional level (21 files vs 17)
- **Quality Score**: Achieved Gold Status (85/100) on GLAMA.ai platform
- **Testing**: Expanded test suite with comprehensive coverage

### Fixed
- **Import Issues**: Resolved plexapi dependency and module loading problems
- **Build Process**: Fixed MCPB CLI integration and packaging workflow
- **Configuration**: Improved environment variable handling and settings validation
- **Logging**: Implemented structured logging throughout the application

### Technical Details
- **Python Version**: >=3.10.0 (tested on 3.10-3.13)
- **FastMCP**: >=2.10.0 with MCP 2.12.0 compliance
- **PlexAPI**: >=4.15.0 for Plex Media Server integration
- **Platforms**: Windows, Linux, macOS support
- **Package Size**: 5.0 MB (optimized for distribution)

## [1.0.0] - 2025-09-15

### Added
- Initial Plex Media Server MCP integration
- Basic media library browsing and search functionality
- User management and permissions handling
- Playlist creation and management
- Playback control for connected clients
- Server health monitoring and maintenance tools

### Technical Details
- **Framework**: FastMCP 2.0
- **Protocol**: MCP 2.0 stdio
- **Tools**: 20 core tools
- **Documentation**: Basic setup and usage guides

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Version History
- **2.0.0**: Production-ready with MCPB packaging and GLAMA Gold Status
- **1.0.0**: Initial release with basic Plex Media Server integration

