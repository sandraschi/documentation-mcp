# arxiv-mcp

**Ports**: 10770 (backend), 10771 (frontend)
**Stack**: FastMCP 3.2, FastAPI, Starlette, Vite/React, SQLite FTS5, pypdf

## Tools

- `search_papers` — arXiv API keyword search with category filters
- `get_paper_details` — Single paper metadata by arXiv ID
- `fetch_full_text` — arXiv experimental HTML → Markdown
- `search` / `searchAdvanced` — arxiv.org HTML scraping (unified `searchtype` param)
- `getPaper` / `getContent` / `getRecent` — HTML abs page, Jina Reader, category recents
- `find_connected_papers` — Semantic Scholar citation graph
- `list_category_latest` — Rolling window of new papers
- `ingest_paper_to_corpus` — Persist to local FTS depot
- `compare_papers_convergence` — Bundle abstracts for cross-paper synthesis
- `resolve_doi` — DOI → metadata + OA status (Unpaywall + Crossref)
- `fetch_doi_content` — DOI → PDF download → text extraction (pypdf)
- Blog tools — `fetch_lab_post`, `list_lab_posts` (Anthropic, Google Research, DeepMind, Google AI)
- Prefab UI — `show_paper_card`

## Prompts

10 prompts for research workflows: deep-read, survey (consciousness, AI consciousness, neurophilosophy), convergence analysis, firefront scan, corpus build, replication audit, citation map.

## Web Dashboard

React SPA on 10771 with: keyword search, category browsing, single paper lookup, depot management, FTS search, favorites, Calibre integration, lab blog browser, sweep templates.

## Key Files

| File | Purpose |
|------|---------|
| `src/arxiv_mcp/server.py` | MCP tool registrations |
| `src/arxiv_mcp/app.py` | FastAPI REST + MCP HTTP mount |
| `src/arxiv_mcp/services/papers.py` | arXiv API + Semantic Scholar |
| `src/arxiv_mcp/arxiv_html.py` | arxiv.org HTML scraping |
| `src/arxiv_mcp/sanitize.py` | Prompt injection safety wrapping |
| `src/arxiv_mcp/doi_resolver.py` | DOI → OA PDF via Unpaywall + Crossref |
| `src/arxiv_mcp/html_extract.py` | arXiv experimental HTML → Markdown |

## Security

- All external text (titles, abstracts, full text, blog content) wrapped with adversarial safety boundary before returning to LLM
- Zero-width Unicode character stripping on all ingested text
- Spam pattern detection not applicable (academic source)
