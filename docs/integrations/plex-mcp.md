# Plex MCP Integration

## Overview

Plex MCP (plex-mcp-advanced) is a FastMCP 3.2 server for Plex Media Server. It provides stdio (Claude Desktop) and a **React webapp** (Next.js 15 + FastAPI backend) for browsing libraries, **movies with Plex posters**, semantic (RAG) search, media enrichment, and chat with local LLM.

**Repository**: [plex-mcp](https://github.com/sandraschi/plex-mcp)  
**Framework**: FastMCP 3.2  
**Webapp ports**: Backend 10740, frontend 10741 (port range 10700–10800).

## Capabilities

- **MCP tools**: Portmanteau tools for libraries, media (browse/search), playlists, streaming, server, metadata, **plex_rag** (semantic search over movie/show/music metadata), **plex_media_enrichment** (high-value Wikipedia discovery), etc.
- **Webapp**:
  - **Movies**: Plex poster images via image proxy; card/list view; **movie detail modal** on click (poster, year, duration, rating, genres, directors, tagline, summary, **Play in Plex** button when Plex URL is set).
  - **Semantic search**: RAG over Plex metadata (movie/show/music); "Sync / Index metadata" to index.
  - **Settings**: Plex token/URL, LLM config; **RAG / Indexing** section with "Reindex metadata" button.
  - Overview, Libraries, Search, Chat (local LLM with live preprompt), Server, Logger/Help modals.

## RAG / Semantic search

- **Indexing**: From webapp use "Reindex metadata" on Settings or "Sync / Index metadata" on Semantic search page (`POST /api/rag/sync`). Via MCP: `plex_rag(operation='sync_metadata')`.
- **Query**: Semantic search page or `plex_rag(operation='semantic_search', query='...')`.
- **Enrichment**: Support for `enrich=True` during sync to augment index with Wikipedia summaries. Dedicated [Media Enrichment Guide](https://github.com/sandraschi/plex-mcp/blob/main/docs/ENRICHMENT.md).
- **Dependency**: Prefers mcp-central-docs vector store on path; optional **in-repo fallback** (LanceDB + sentence-transformers) via `pip install plex-mcp-advanced[rag]` when mcp-central-docs is not available.

## References

- [Plex MCP README](https://github.com/sandraschi/plex-mcp#readme)
- [Plex MCP Webapp README](https://github.com/sandraschi/plex-mcp/blob/main/webapp/README.md)
- [MCP Central – WEBAPP_PORTS](../docs/operations/WEBAPP_PORTS.md)

---

*Last updated: 2026-04; v2.4.1, Media Enrichment, Wikipedia RAG Augmentation.*
