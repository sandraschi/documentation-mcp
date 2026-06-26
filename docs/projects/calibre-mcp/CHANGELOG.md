# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This mirror is kept loosely in sync with `D:\Dev\repos\calibre-mcp\CHANGELOG.md`.

## [Unreleased]
### Added
- **Roadmap documentation** for next-phase projects: reading-flow integration,
  annotation intelligence, book-of-the-day, duplicate detection, audiobook
  generator. Full specs in `docs/plans/` in the main repo, agent skills in
  `.cursor/skills/`, fleet-level README/TODO/STATUS mirrored here.
- **`PLUGIN_IDEAS.md`** — brainstorm of future Calibre plugin features
  grouped by theme (reading-time features, library management, discovery,
  writing capture, multimedia, meta-tools).
- **`VIEWER_EXTENSIBILITY_ANALYSIS.md`** — honest analysis of what the
  Calibre viewer plugin API (`ViewerPlugin` class) actually allows,
  correcting an earlier incorrect claim that it was fully sealed.

## [1.7.0] - 2026-04-16
### Added
- **`media_research_book`** — deep book research with concurrent source
  fetching across Wikipedia, SF Encyclopedia, TVTropes, Anime News Network,
  Open Library, plus local library data, synthesised via LLM sampling.
  REST endpoint `POST /api/rag/research/{book_id}`.
- **Plugin v1 shipped** — working Calibre GUI plugin at ~38KB. Tabbed
  metadata editor, semantic search dialog, streaming research dialog with
  offline Ollama support.
- Webapp `/rag` page gains 4th tab "Research" with streaming progress +
  source attribution + local data badges.

## [1.6.0] - 2026-04-14
### Added
- **RAG endpoints** beyond metadata search: `/api/rag/retrieve` (passage
  retrieval), `/api/rag/synopsis` (LLM-generated synopsis from passages),
  `/api/rag/research` (orchestrated deep research).
- **Series analysis** tool — gap detection, reading order suggestions.
  UI page at `/series/analysis`.
- **Extended metadata v2** — read_status, date_read, mood, culprit,
  locked_room_type, original_language, translator, edition_notes.
  Stored in `calibre_mcp_data.db` (not Calibre's metadata.db).
- **Calibre plugin** (first working release) — talks to webapp via httpx
  and to local state DB directly.

## [1.5.0] - 2026-03-31
### Added
- Import Hub Stabilization: hardening of automated book ingestion sources
- Anna's Archive UX Optimization: CAPTCHA/timer detection, mirror management
- arXiv reliability: exponential backoff, custom User-Agent
- Global Import Settings: persistent UI settings for target library and
  automated tag injection

## [1.4.0] - 2026-03-27
### Added
- MCPB packaging alignment (v0.2 manifest)
- docs/PROMPTS.md and docs/COOKBOOK.md
- skill://calibre-expert bundled expert skill
- Self-contained LanceDB vector store
- Background metadata RAG index build with progress polling

### Changed
- Unified CI workflow with PyPI publishing
- Webapp startup SOTA (port reservoir 10720/10721)

### Fixed
- Book isbn/lccn AttributeError (ORM mapping)
- Webapp layout standardization

## [1.3.0] - 2026-02-26
### Added
- Neural Media RAG portmanteau (LanceDB-backed)
- DeepIngestor for full-text parsing and semantic chunking
- Agentic Synthesis API for central-docs integration

## [1.2.0] - 2026-02-04
### Added
- MCPB packaging support

### Fixed
- Startup reliability (standardized Python, dependency resolution)

## [1.1.0] - 2026-01-22
### Added
- Natural language search via FastMCP sampling
- Auto-open books when search results are unique
- Title-specific search bypassing FTS

## [1.0.0] - 2025-10-21
### Added
- Initial release with core library management tools
