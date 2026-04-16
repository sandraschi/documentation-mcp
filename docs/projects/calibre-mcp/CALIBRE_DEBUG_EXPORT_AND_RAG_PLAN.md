# Calibre-debug metadata export and RAG alignment

**Canonical upstream:** `calibre-mcp` repository — `docs/CALIBRE_DEBUG_EXPORT_AND_RAG_PLAN.md`.

**Status:** Implemented upstream — script, env-driven comment cap (default **20 KiB** per book comment in embedding text, max **16 MiB**), HTML stripping, MCP tool **`calibre_metadata_export_json`**, unit tests.

---

## LanceDB lanes

| Lane | Location | Tools |
|------|----------|--------|
| **Metadata RAG** | `lancedb_metadata/` | `calibre_metadata_index_build`, `calibre_metadata_search` |
| **Export JSON** | n/a (file output) | **`calibre_metadata_export_json`**, or `scripts/export_metadata_for_rag.py` + `calibre-debug -e` |

**Env:** `CALIBRE_METADATA_COMMENT_MAX_CHARS`, `CALIBRE_METADATA_STRIP_HTML` — see upstream **`rag/text_utils.py`**.

After bulk comment edits, run **`calibre_metadata_index_build`** to refresh LanceDB.

---

## Fleet links

- [SEARCH_RAG_FTS.md](./SEARCH_RAG_FTS.md)  
- [README.md](./README.md)
