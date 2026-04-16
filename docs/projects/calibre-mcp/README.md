# CalibreMCP — your library, an AI that actually reads the stacks

**Central index** for fleet discovery. **Source of truth:** [sandraschi/calibre-mcp](https://github.com/sandraschi/calibre-mcp) · **Local clone:** `D:\Dev\repos\calibre-mcp`

---

## Why it exists

Thousands of EPUBs and PDFs should not mean a thousand forgotten folders. **CalibreMCP** plugs your Calibre library into the agent era: ask in plain language, search by *meaning* as well as title, jump to a line you half-remember, and let tools chain—libraries, books, viewer, export—without babysitting every click.

It is built for people who treat a digital library as a **working collection**, not a dump.

---

## What you get (at a glance)

- **FastMCP 3.1+** — portmanteau tools, sampling, skills, prompts; agentic workflows for multi-step library tasks.
- **Semantic metadata search** — LanceDB over titles, authors, tags, comments, series (`calibre_metadata_search`).
- **Full-text that respects Calibre** — uses Calibre’s own FTS index where it matters; optional **phrase locations** (PDF page, EPUB chapter, Calibre viewer “search after open”).
- **Webapp** — dark UI, semantic search page, chat (Ollama / LM Studio / OpenAI-compatible), logs, stabilized Import Hub.
- **Smart Import Hub (v1.5.0)** — One-click ingestion from **arXiv**, **Project Gutenberg**, and **Anna's Archive**; includes mirror-aware landing-page detection (CAPTCHA/timers) and manual browser fallback.
- **MCP Apps (Prefab)** — optional **`show_book_prefab_card`** (after **`query_books`** / `book_id`) and **`show_libraries_prefab_card`** (“Our Calibre” — all libraries + stats; `uv sync --extra apps`). Central fleet doc: [mcp-apps-prefab-ui.md](../../fastmcp/mcp-apps-prefab-ui.md).
- **Local-first** — direct `metadata.db` + files on disk; RAG indexes live next to your library. No cross-repo vector-store dependency at runtime.

---

## Read next (detail docs in this folder)

| Doc | What’s inside |
|-----|----------------|
| [SEARCH_RAG_FTS.md](./SEARCH_RAG_FTS.md) | FTS vs semantic RAG, on-disk `lancedb_*` layout, `search_fulltext(resolve_locations)`, HTTP chat. |
| [CALIBRE_DEBUG_EXPORT_AND_RAG_PLAN.md](./CALIBRE_DEBUG_EXPORT_AND_RAG_PLAN.md) | `calibre-debug` metadata JSON export, curated comments as RAG signal, LanceDB alignment, implementation phases (upstream script in `calibre-mcp/scripts/`). |
| [CONTENT_SERVER.md](./CONTENT_SERVER.md) | Calibre Content server + **calibredb** remote URLs vs direct `metadata.db` — when remote is enough, when it is not. |

**Upstream (full manual):** [README](https://github.com/sandraschi/calibre-mcp/blob/main/README.md) · [Agentic & RAG](https://github.com/sandraschi/calibre-mcp/blob/main/docs/AGENTIC_AND_RAG.md) · [CHANGELOG](https://github.com/sandraschi/calibre-mcp/blob/main/CHANGELOG.md) · [PRD](https://github.com/sandraschi/calibre-mcp/blob/main/docs/PRD.md)

---

## Fleet

| | |
|--|--|
| **Webapp ports** | **10720** (backend) · **10721** (frontend) — [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |
| **Start** | `calibre-mcp\webapp\start.ps1` (from upstream clone) |
| **Index** | [projects/README.md](../README.md) · [FLEET_INDEX.md](../FLEET_INDEX.md) |

---

*Tags: #calibre-mcp #calibre #ebooks #mcp #rag #fleet*
