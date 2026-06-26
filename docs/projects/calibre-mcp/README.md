# calibre-mcp — Project Hub

Central index for all calibre-mcp planning and roadmap documentation.

**Repository:** `D:\Dev\repos\calibre-mcp`
**Current version:** 1.7.0 (2026-04-16)
**Status:** Active, heavy development

## What it is

FastMCP 3.2 server providing AI-assisted Calibre ebook library management.
Simultaneous stdio (Claude Desktop, Cursor) + HTTP (webapp on 10720) transport.
Includes a functional Calibre GUI plugin, a Next.js webapp frontend, LanceDB
semantic search over metadata and full-text, and deep book research
synthesising Wikipedia + SF Encyclopedia + TVTropes + Anime News Network +
Open Library + local library data via local LLM sampling.

Used by Sandra across ~13,000 books in multiple Calibre libraries.

## Where documentation lives

All design specs and roadmap documents live in the repo itself under
`docs/plans/`. This hub mirrors them for fleet-level discovery.

| Doc                                      | Purpose                               |
|------------------------------------------|---------------------------------------|
| `ROADMAP.md` (here)                      | High-level fleet view                 |
| `TODO.md` (here)                         | Implementation tracking               |
| `PLUGIN_IDEAS.md` (here)                 | Calibre plugin feature brainstorm     |
| `VIEWER_EXTENSIBILITY_ANALYSIS.md`       | Honest analysis of Calibre viewer limits |
| [PROMOTION.md](./PROMOTION.md)           | Goodreads, forums, wrappee etiquette (no AI spam) |

Per-project specs live in the repo:

| Spec                                           | Project              | Effort |
|-----------------------------------------------|----------------------|--------|
| `calibre-mcp/docs/plans/ROADMAP.md`           | Strategic overview   | —      |
| `calibre-mcp/docs/plans/READING_FLOW_INTEGRATION.md` | Reading tracking | 2–3 d  |
| `calibre-mcp/docs/plans/ANNOTATION_INTELLIGENCE.md` | Highlights import | 3–4 d  |
| `calibre-mcp/docs/plans/BOOK_OF_THE_DAY.md`   | Daily surfacer       | 1 d    |
| `calibre-mcp/docs/plans/DUPLICATE_DETECTION.md` | Dupe cleanup       | 1–2 d  |
| `calibre-mcp/docs/plans/AUDIOBOOK_GENERATOR.md` | Book → M4B         | 5–7 d  |

Agent Skills for AI-assisted implementation:

- `calibre-mcp/.cursor/skills/calibre-mcp-*/SKILL.md` (one per project
  + orchestrator)

## Linked fleet entries

- `FLEET_INDEX.md` — fleet overview, current version line
- `calibre-plugins` — sibling workspace for Phase 2 RAG-search plugin
  development (currently stubs only; features merged into main
  calibre_plugin instead)

---

*Maintained by Sandra Schipal. Architecture and roadmap by Claude Opus 4.7
(Anthropic), April 2026.*
