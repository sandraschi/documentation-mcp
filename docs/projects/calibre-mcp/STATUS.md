# calibre-mcp — Status

**As of:** 2026-07-09
**Current version:** 1.8.6
**Status:** Full rebuild certified. CUA-NSIS 7/7 phases pass. Frontend standalone server fixed.

## 2026-07-09: Tauri rebuild + SOTA gaps closed

- **NSIS build certified**: CUA-NSIS smoke test passes 7/7 phases (install, launch health, diagnostics, uninstall)
- **Tauri build no longer breaks webapp**: `build.ps1` restores standalone `.next/` after NSIS build (was leaving `basePath:/app` in routes manifest)
- **Frontend standalone fixed**: `start.ps1` uses `node .next/standalone/server.js` with `PORT=10721`, auto-copies static files
- **Session context injection**: `.claude-plugin/`, `hooks/`, `.cursorrules`, `.windsurfrules` — agents get tool-awareness on session start
- **PyInstaller fixes**: `annotated_doc` metadata preserved, OpenTelemetry runtime hook added for `StopIteration` crash
- **`backend.rs` bugs fixed**: removed self-kill in `free_port()`, added `MCP_TRANSPORT=http` env var
- **`just cua-nsis-test`** recipe added
- **Playwright tests expanded** from 2 to 9 tests

## 2026-07-05 (evening): Agentic chat + UX polish

- **Agentic chat**: `/api/llm/agentic` with proper OpenAI-compatible tool calling (ReAct loop, 6 MCP tools, native `tool_calls` protocol)
- **Custom personality**: Editable textarea stored in localStorage
- **Logger modal**: Level filter dropdown, auto-scroll toggle, refresh, color-coded levels
- **Layout fixes**: AppLayout `h-screen` + `flex-col` on main for proper height distribution
- **Zoom keyboard shortcuts**: Ctrl+Plus/Minus/0 added
- **Sidebar**: Toggle in header bar (right edge, fleet standard)
- **Book list**: Shows first 2 lines of rendered HTML description
- **Containers dropdown**: Removed (fleet infra noise)
- **LLM timeout**: 30s → 120s, wrapped in try/except for friendly errors

## 2026-07-05: SOTA compliance sweep

- **Webapp backend merge**: Single FastAPI process serves REST API + MCP at `/mcp` + health + diagnostics on port 10720
- **Health endpoint** now returns full shape (server, version, uptime, tool_count, providers)
- **CORS**: Explicit Tauri origins (tauri://localhost, http://tauri.localhost, https://tauri.localhost)
- **NSIS**: Fleet-standard hooks (Stop-Process, UninstallPrevious, Sleep 3000, ExecWait)
- **Tauri backend**: Fleet-standard spawn (MCP_PORT/MCP_HOST, 240s kill poll, TCP health check)
- **Chat page**: Full SOTA rewrite (localStorage persistence, export/clear, provider status, example prompts, data-testids)
- **Sidebar**: Collapse toggle moved to top (fleet standard)
- **Zoom**: CSS `zoom` fallback + keyboard shortcuts + UI controls in topbar
- **Version gaslights fixed**: All version strings unified to `1.8.6`
- **API route mismatches fixed**: arXiv double-prefix, health/help/status route alignment
- **Removed**: Containers dropdown (fleet infrastructure noise)

## Tauri NSIS installer (2026-06-17)

- **PyInstaller onefile sidecar** with `noarchive=True` (fixes stdlib PYZ import bug)
- **SPAStaticFiles** subclass handles dynamic SPA routes (falls back to index.html)
- **Next.js `basePath: "/app"`** for Tauri builds — assets served under `/app/_next/`
- **CORS** includes `tauri://localhost`, `http://tauri.localhost`, `https://tauri.localhost`, `http://goliath:10721`
- **CORS regex** `r"https?://tauri\.localhost(:\d+)?"` gated on `CALIBRE_TAURI` env var
- **Frontend served by backend** at `/app/` — no separate dev server needed in production
- **Build verified**: install → launch → health 200 → `/app/` 200 → `_next` assets 200

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
