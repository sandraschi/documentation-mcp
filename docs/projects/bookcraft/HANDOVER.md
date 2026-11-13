# BookCraft — Handover Document

**Last Updated**: 2026-11-10
**Current State**: v0.1.0 Active Development
**Primary Artifact**: [sandraschi/bookcraft](https://github.com/sandraschi/bookcraft)

---

## 1. What Was Done
- Direct binary parsing of Calibre `metadata.db` SQLite schema.
- High-level MCP tools: `calibre_metadata_search`, `manage_books`, `rag_retrieve`.
- Built CLI verbs for book search, inspection, and format conversion.

---

## 2. Immediate Next Steps
1. Wire into the `MediaCraft` bundler along with `plex-mcp` and `immich-mcp`.
2. Integrate full-text vector RAG embeddings via `databasecraft-store`.
