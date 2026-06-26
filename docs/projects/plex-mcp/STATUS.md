# plex-mcp — Status

**As of:** 2026-04-19
**Current version:** 2.4.1 (released early April 2026)
**Status:** Active development, stable for daily use.

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
- GitHub: `https://github.com/sandraschi/plex-mcp`

## Recent releases

- **v2.4.1 (April 2026)** — SOTA 14.1 compliance, webapp
  modernization, justfile recipes
- **v2.4.0** — FastMCP 3.2 upgrade, industrialized stack
- **v2.3.x** — `plex_rag` LanceDB integration, sampling support
- **v2.2.x** — `plex_media_enrichment` (Wikipedia)
- **v2.1.x** — Universal Connect (simultaneous stdio + HTTP)

---

*Status maintained by Sandra Schipal. Entry authored by Claude Opus 4.7,
April 2026.*
