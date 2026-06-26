# calibre-mcp — Status

**As of:** 2026-04-19
**Current version:** 1.7.0 (released 2026-04-16)
**Status:** Active development. Stable.

## Current state

FastMCP 3.2 server + FastAPI backend + Next.js 15 frontend + Calibre
GUI plugin. Used daily by Sandra against ~13,000 books.

### Infrastructure

- **Backend FastAPI:** `http://localhost:10720/api/*`
- **FastMCP HTTP:** `http://localhost:10720/mcp` (same process)
- **Frontend Next.js:** `http://localhost:10721`
- **Ollama:** `http://localhost:11434` (default model `gemma3:12b`)
- **State DB:** `%APPDATA%\calibre-mcp\calibre_mcp_data.db`
- **Calibre GUI plugin:** `calibre_plugin/` (installable via
  `calibre-customize -b`)

### Stdio transport

Also launches as stdio MCP server from Claude Desktop via:
`uv run python -m calibre_mcp.__main__` from `D:/Dev/repos/calibre-mcp`.

## Tool surface

FastMCP 3.2 tools, organised as portmanteau operations. Major
categories:

- **Library management** — `manage_libraries`, `query_books`,
  `manage_books`, `manage_metadata`
- **Viewer orchestration** — `manage_viewer` (opens books in system
  viewer or Calibre viewer)
- **Extended metadata** — v1.7 introduced read_status, mood,
  locked_room_type, culprit-annotated, original_language,
  translator, edition_notes, date_read
- **Search** — full-text via Calibre FTS, semantic via LanceDB
- **RAG** — metadata index + passage retrieval + synopsis generation
- **Research** — `media_research_book` (Wikipedia + SFE + TVTropes +
  Anime News Network + Open Library + local data, synthesised via
  LLM sampling)
- **Series analysis** — gap detection, reading order suggestions
- **Import** — bulk import from Anna's Archive / Z-Library metadata

Prefab UI cards for book details and library overview.

## Calibre GUI plugin (v1.7)

Working, installed. Features:
- Tabbed extended-metadata editor
- Semantic search dialog (LanceDB-backed)
- Streaming research dialog (Ollama, works offline without webapp)
- Virtual Library creation from search results
- Toolbar button with dropdown menu + context-menu entries
- Config dialog for MCP endpoint + Ollama URL/model selection

Currently an `InterfaceAction` plugin. A `ViewerPlugin` variant is
planned but not yet built — see `PLUGIN_IDEAS.md` and
`VIEWER_EXTENSIBILITY_ANALYSIS.md`.

## Webapp frontend

Next.js 15 App Router, Tailwind, dark slate with amber accents.
Pages:
- `/` — dashboard
- `/library` — main book list
- `/book/[id]` — book detail modal
- `/rag` — 4-tab RAG interface (metadata/passages/synopsis/research)
- `/series/analysis` — series gap detection
- `/settings` — config
- `/help` — contextual help (auto-generated from server capabilities)

## Roadmap

Five projects specced, none yet implemented. See `TODO.md` for
tracking and `README.md` for orientation. Full specs in
`D:\Dev\repos\calibre-mcp\docs\plans\`.

Ordered by priority:
1. Reading-flow integration (2–3 days)
2. Annotation intelligence (3–4 days)
3. Book of the day (1 day)
4. Duplicate detection (1–2 days)
5. Audiobook generator (5–7 days)

## Known issues

- **prefab_ui venv sync.** `prefab-ui` is a core dependency but has
  occasionally needed manual `uv sync` after lock file changes.
  Source code now fails with actionable error rather than silently
  dropping Prefab cards.
- **calibre_plugin/ directory not yet committed to git.** Should be
  addressed before next release.
- **Git operations from winops MCP subprocess are unreliable.**
  Console output capture fails for consoleless Windows processes —
  workaround is to run `git` commands manually from a terminal.

## Repositories

- Main: `D:\Dev\repos\calibre-mcp`
- Fleet docs mirror: `D:\Dev\repos\mcp-central-docs\projects\calibre-mcp\`
- Public: `https://github.com/sandraschi/calibremcp` (when pushed)

## Recent releases

- **v1.7.0 (2026-04-16):** `media_research_book` tool with concurrent
  multi-source fetching
- **v1.6.0 (2026-04-14):** RAG endpoints (retrieve/synopsis/research),
  series analysis, Calibre GUI plugin v1 shipped
- **v1.5.x (2026-04-earlier):** LanceDB metadata RAG, extended
  metadata schema v2 (locked-room/culprit/mood/read-status fields)
- **v1.4.x:** FastMCP 3.1 → 3.2 upgrade, Prefab UI cards

---

*Status maintained by Sandra Schipal. Entry authored by Claude Opus 4.7,
April 2026.*
