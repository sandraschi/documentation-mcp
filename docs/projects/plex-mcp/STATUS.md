# plex-mcp — Status

**As of:** 2026-10-08
**Current version:** 2.4.1
**Status:** Active, stable. Settings has a real Plex token facility, a Diagnostics panel, and a local+cloud LLM provider registry with VRAM management; a first-run wizard covers Plex+LLM setup on a fresh install; deep per-item enrichment (Wikipedia+TMDB+JustWatch, LLM-synthesised dossiers, library cross-references) and taste modelling (profile learned from watch history, scored against the library) shipped as roadmap projects 1 and 3; Movies/Libraries data-bridge bug, the NSIS build pipeline, and a broken dev-webapp launcher config all fixed; two leaked tokens removed from source.

## 2026-10-08: Dashboard overhaul + webapp API-parity audit (in progress)

- **Overview rewritten to the fleet gate**: hero (brand + headline + Browse/Search/Chat CTAs,
  `dashboard-hero-cta`) + 6 KPI cards (libraries, server, enriched, semantic index, taste,
  LLM) + quick actions + library preview + `onboarding-cue` red button when Plex is down.
  New `GET /api/dashboard/` aggregation endpoint (best-effort per section, never 500).
- **Sidebar brought to standard**: collapse toggle moved to the top header (was bottom),
  logo + version in header, live connection indicator (backend/Plex probe every 15s).
- **Full backend-vs-webapp gap audit** (every `@router` route vs every `api.ts` export +
  caller): unsurfaced = `POST /api/search/advanced`, taste `score/` + `rank` + `temporal/`,
  media `ai-context` (wrapper exists, no caller) + `stream-url`/`file`/`art`,
  `playback/play` + `/clients`, `workflows/run`, `llm/onboarding`, `DELETE llm/keys`,
  `rag/context`, `system/diagnostics` (wrapper exists, no caller), single-library
  `GET /{id}` + `/{id}/items` (no wrapper), `fleet/launch` vs `webapp-launch` duplicate.
  Orphaned wrappers: `getLlmGpus`/`getLlmLoaded`/`unloadLlm`, `searchByPerson`.
  Tech debt: repair, rag/stats, chat agentic/refine/models use raw `fetch` instead of
  `api.ts`. Dead: `getSystemStatus` (no backend route), legacy `/api/v1/*`.
- **Parity build tracked as TODO project 7** (phases 0–4): contracts → search/taste/
  diagnostics → media actions → LLM/VRAM + RAG → dead-code cleanup. See TODO.md.

## 2026-10-04: Taste modelling (roadmap project 3 of 6)

- **`plex_taste` tool + `/taste` page + `/api/taste/*`**: a taste profile learned from Plex watch history (what you gravitate toward / pass over), per movies vs TV and per time of week, plus recent shifts and `score_item`/`score_library` ranking. Reads from Plex only; data in `data/taste.db`.
- **Deliberately not the spec's EMA**: on real data (16,928 history entries) it scored every dimension +1.00. Now lift against the library (decayed attention vs a library survey), stratified by kind. See `plex-mcp/docs/plans/TASTE_MODELLING.md`.
- Live build here: 15,615 events, 12,201 library items, ~2 min; the result is recognizable.
- Test suite repaired the same day (13 long-standing failures were stale test expectations); an unscoped `plex_media search` timing out on large servers was found and handed off separately.

## 2026-09-13: Deep metadata enrichment (roadmap project 1 of 6)

- **`plex_media_enrichment` gained a full deep-enrichment surface**: `enrich`, `bulk_enrich`, `get_enrichment`, `get_related`, `search_by_theme`, `search_by_person`, `stale_report` alongside the existing title-only quick lookups. Sources: Wikipedia (REST API) + TMDB deep mode (official v3 API: full cast/crew/keywords/collection) + JustWatch (best-effort availability, never blocking). Letterboxd/IMDB/Rotten Tomatoes/Metacritic scraping was deliberately scoped out — all four prohibit scraping in their ToS and run active bot detection; not worth the exposure at 50k library items (a call Sandra made explicitly before implementation).
- **Library-wide cross-references**: each enriched item is matched against every other already-enriched item by director, shared top-5 cast, TMDB collection, and thematic-tag overlap (2+ shared tags) — grows denser as more of the library gets enriched.
- **New webapp pages**: `/media?ratingKey=...` (per-item dossier: synopsis, critical overview, "why this matters," content warnings, thematic tags, related items) and `/enrichment` (bulk-run launcher with live progress, stale count, theme search). "Full dossier" link added to the Movies detail modal.
- LLM synthesis is transport-agnostic: MCP tool path uses `ctx.sample`, webapp REST path uses the local+cloud LLM provider registry vendored earlier this week — same seam, two adapters. Works with zero LLM configured too (returns raw sources, no synthesised dossier).
- **Found and fixed a real pre-existing bug**: Wikimedia's edge 403s httpx's default User-Agent string outright, so `enrichment_service.fetch_wikipedia_summary` silently returned `None` on every call, everywhere it was used (not just the new code) — since whenever it was first written. Fixed with a descriptive UA on every httpx client hitting Wikipedia/TMDB/JustWatch.
- 23 new tests (`test_enrichment_service.py` x15, `test_api_enrichment.py` x8, including a regression test for a route-ordering bug caught before it shipped — FastAPI's `/{rating_key}` catch-all would have shadowed `/by-theme` etc. if registered first).
- Full detail: `plex-mcp/docs/plans/DEEP_METADATA_ENRICHMENT.md` and `CHANGELOG.md`.

## 2026-09-11 (later): Diagnostics panel + local/cloud LLM provider registry + VRAM management

- **Settings → Diagnostics**: one traffic-light panel (Plex/LLM/RAG/*arr) checked at once instead of hunting through separate pages. `GET /api/system/diagnostics`.
- **Cloud LLM providers vendored from the fleet template** (`templates/llm/`, pilot arxiv-mcp): Anthropic, DeepSeek, OpenRouter join Ollama/LM Studio/vLLM/OpenAI. New module `webapp/backend/app/llm_providers.py` — 0600 per-provider keystore (never in `settings.json`, never echoed back), correct auth/message-format per provider (Anthropic differs from OpenAI-style), chat and agentic tool-calling both provider-aware (Anthropic gracefully degrades to plain chat for tool-calling rather than sending it a format it can't parse).
- **GPU VRAM panel** in Settings: live NVIDIA telemetry, resident Ollama models, "Evict all" — so an AI task doesn't just fail when VRAM is full; free it, or fall back to a cloud provider on a GPU-less machine.
- Also fixed while building the NSIS installer: `just build-native` was silently building an unrelated Zed IDE extension (root `Cargo.toml`/`build.ps1` collision, now moved to `zed-extension/` with its own bug fixed too), a false-failure in `native/build.ps1`'s post-build step, a `Join-Path` syntax bug in the vendored `cua-nsis-test.ps1` (PS7-only form invoked via PS5.1 fleet-wide — ~195 other repos share it, tracked separately), and the CUA smoke test's own summary printing "ALL PHASES PASSED" while a phase had failed.
- Deleted confirmed-dead code (root `plex/` package, `server_minimal.py`, `server_fixed_head.py`, stray `.bak` files); README Stack section and Help page brought up to date.
- 22 new tests added today (`test_api_plex_auth.py` x7, `test_api_llm_providers.py` x15); full regression suite green.
- Full detail: `plex-mcp/docs/plans/GAP_ANALYSIS_AND_IMPROVEMENTS.md` and `OPERATIONAL_IMPROVEMENTS.md` Phase 4.

## 2026-09-11: Settings Plex auth facility + Movies data-bridge fix + launcher config fix

- **Settings → Plex now has "Test connection" and "Get a new token"** (real Plex PIN sign-in flow via app.plex.tv). Previously there was no way to validate or refresh a token from the UI at all — fresh installs hit a dead end on "no Plex token".
- **Movies/Libraries pages were silently broken** even with a valid token: `plex_library`/`plex_media`/`plex_search` never carried a `data` field the webapp's REST layer could read (only human-text summaries + Prefab UI card JSON). Fixed and verified live against the real Plex server.
- **`fleet-start.config.ps1` had the webapp launcher pointed at the wrong backend** (`module-serve` → `python -m plex_mcp --serve`, a flag that doesn't exist) — `just serve`/`start.ps1` never actually started the real FastAPI backend. Fixed to `uvicorn-web-app`, verified via the actual `mcp-central-docs/starts/plex-start.bat` launcher. This pattern (`Backend.Kind='module-serve'` with no matching `--serve` flag) is suspected fleet-wide across ~33+ other repos — see `TRAPS_AND_PITFALLS.md` #31 and `mcp-central-docs` task `task_0e2422c4`.
- **Two hardcoded real-looking Plex tokens removed from git-tracked source** (`server_minimal.py`, dead code; `webapp/backend/test_plex_pagination.py`, a dev script) — both should be treated as compromised.
- **`scripts/mcpb-pack.ps1` restored** after an accidental deletion, and the vendored `fleet.just`'s `mcpb-pack` recipe fixed (pointed at a path — `mcpb/pack.ps1` — that has never existed; root cause was the canonical template, fixed upstream, ~160 other repos affected, tracked separately).
- **GitHub repo slug bug found and fixed in docs**: README/docs linked to `sandraschi/plex-mcp` (doesn't exist) instead of the real `sandraschi/plexmcp`. Local folder is named `plex-mcp` by fleet convention; upstream repo is still named `plexmcp` — consider renaming the GitHub repo to match (not yet done, needs Sandra's call).
- Ruff `ignore` list de-duplicated in `pyproject.toml`; `S110`/`S112`/`T201` permanently removed (were silently masking real issues); added a real endpoint test suite (`tests/test_api_plex_auth.py`, 7 tests).

## 2026-07-09: Settings footgun removed + filter bugs fixed

- **`.env` fallback chain removed**: `settings_store.py` and `config.py` now read from repo root `.env` only — no more stale tokens from cached `settings.json` or sibling `.env` files winning by accident
- **Movies filter bug fixed**: `media_type` was passed as raw Plex filter `mediatype` — changed to `libtype=media_type` in both browse and search; `min_rating` stripped from Plex filter kwargs (Plex has no `minRating` filter)
- **`search_media` sanitised**: `media_type` and `min_rating` popped from `**filters` before reaching Plex API

## Current state

FastMCP 3.2 server + FastAPI backend + Next.js frontend. Used
nightly by Sandra against a library of ~50,000+ video items
(movies, TV, documentaries, misc).

### Infrastructure

- **Backend FastAPI:** `http://localhost:10741/api/*`
- **FastMCP HTTP:** `http://localhost:10741/mcp` (same process)
- **Frontend Next.js:** `http://localhost:10742`
- **Plex Media Server:** `http://localhost:32400`
- **Ollama:** `http://localhost:11434` (default model `gemma3:12b`)
- **Webapp state DB:** SQLite within plex-mcp workspace

### Stdio transport

Launches as stdio MCP from Claude Desktop:
`uv run plex-mcp-advanced` from `D:/Dev/repos/plex-mcp`.

## Tool surface

19 portmanteau tools covering the full Plex operational surface:

- **Library** — `plex_library` (sections, metadata refresh, library lifecycle)
- **Media** — `plex_media` (browse, search, metadata), `plex_metadata`
- **Playback** — `plex_streaming` (session control, volume), `plex_performance`
- **Playlists & users** — `plex_playlist`, `plex_user`
- **Search** — `plex_search` (keyword), `plex_rag` (LanceDB semantic)
- **Enrichment** — `plex_media_enrichment` (currently Wikipedia only;
  project 1 expands to 8+ sources)
- **Organization** — `plex_organization`, `plex_collections`
- **Quality** — `plex_quality` (quality profiles)
- **Server** — `plex_server` (server info, identity)
- **Reporting** — `plex_reporting` (usage, analytics)
- **Integration** — `plex_integration` (Tautulli, *arr read-only status)
- **Natural** — `plex_natural_assistant` (sampling-based)
- **Agentic** — `agentic_plex_workflow` (multi-step, SEP-1577)
- **FFmpeg** — `plex_ffmpeg_mgr`, `plex_audio_mgr`
- **Help** — `plex_help`

## Webapp frontend

Next.js, Tailwind, glassmorphism theme. Pages:
- `/` — dashboard
- `/libraries` — section browser
- `/movies`, `/shows`, `/music` — per-library pages
- `/search` — keyword + semantic
- `/chat` — local LLM assistant
- `/settings` — Plex, LLM, *arr configuration

## Roadmap

Six projects specced, none yet implemented. See `TODO.md` for
tracking and `README.md` for orientation. Full specs in
`D:\Dev\repos\plex-mcp\docs\plans\`.

Ordered by priority:
1. Deep metadata enrichment (3–4 days)
2. Subtitle RAG (4–5 days)
3. Taste modelling (2–3 days)
4. Mood picker (1–2 days)
5. Episode intelligence (3–4 days)
6. Cross-library linking (2 days)

**Recommended order:** 1 → 3 → 4 → 2 → 5 → 6. Enrichment and
taste modelling produce data that makes everything else smarter;
mood picker is the daily-use payoff; subtitle RAG is the most
ambitious and slots in after the foundations.

## Known issues

- **Playback control unreliable** for non-GDM clients (Plex Web,
  Windows App). GDM discovery works for PlexAmp with latency.
  Not planned for near-term fix — Plex's client protocol is
  brittle and the effort isn't justified for the edge case.
- **RAG coverage thin** at project start (metadata only). The
  roadmap will change this considerably (subtitle RAG + deep
  enrichment expand coverage substantially).

## Repositories

- Main: `D:\Dev\repos\plex-mcp`
- Fleet docs mirror: `D:\Dev\repos\mcp-central-docs\projects\plex-mcp\`
- GitHub: `https://github.com/sandraschi/plexmcp` (local folder name `plex-mcp` differs from the upstream repo name — long-standing drift, not yet reconciled)

## Recent releases

- **v2.4.1 (April 2026)** — SOTA 14.1 compliance, webapp
  modernization, justfile recipes
- **v2.4.0** — FastMCP 3.2 upgrade, industrialized stack
- **v2.3.x** — `plex_rag` LanceDB integration, sampling support
- **v2.2.x** — `plex_media_enrichment` (Wikipedia)
- **v2.1.x** — Universal Connect (simultaneous stdio + HTTP)

---

*Status maintained by Sandra S.. Entry authored by Claude Opus 4.7,
April 2026.*
