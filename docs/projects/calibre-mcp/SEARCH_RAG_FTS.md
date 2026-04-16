# CalibreMCP — search, RAG, and phrase jump

**Companion to** [README.md](./README.md). Technical mirror; **canonical** detail lives in the [upstream repo](https://github.com/sandraschi/calibre-mcp) (`docs/AGENTIC_AND_RAG.md`).

**Related:** [CALIBRE_DEBUG_EXPORT_AND_RAG_PLAN.md](./CALIBRE_DEBUG_EXPORT_AND_RAG_PLAN.md) — `calibre-debug` JSON export for external RAG pipelines, comment truncation vs LanceDB metadata index, phased implementation checklist.

---

## Three lanes (use the right one)

| Lane | Best for | Mechanism |
|------|-----------|-----------|
| **Calibre FTS** | Exact words, rare phrases, “that line from Hamlet” | `full-text-search.db`, `search_fulltext` |
| **Metadata RAG** | “Japanese locked-room thrillers”, vibe / tags / comments | LanceDB `lancedb_metadata/` |
| **Chunk RAG** | Scenes, tropes, paraphrase over book *body* text | FTS text → embeddings in `{library}/lancedb` (`books_rag`), or portmanteau paths under `lancedb_calibre/` |

**Practical rule:** phrase / quote → FTS first; fuzzy intent → metadata or chunk RAG; combine when the user mixes both.

---

## On-disk layout (under the library folder)

| Path / table | Role |
|--------------|------|
| `lancedb_metadata/` | Metadata-only semantic index. |
| `lancedb/` + `books_rag` | Chunks from Calibre’s indexed `searchable_text` → `rag_retrieve`. |
| `lancedb_calibre/` | `calibre_media`, `calibre_fulltext` (portmanteau `calibre_rag`, DeepIngestor). |

Vector code is **bundled in calibre-mcp** (`rag/lancedb_vector_store.py`) — no runtime import from other documentation repos.

---

## Jump to a quote

`search_fulltext(..., resolve_locations=True)` adds:

- Character offsets in Calibre’s `searchable_text` when the query matches literally.
- **PDF:** page + hit rect (PyMuPDF).
- **EPUB:** spine item href / order (ebooklib).
- **Calibre viewer:** `ebook-viewer --open-at search:…` — opens the book and runs Find (see [Calibre ebook-viewer manual](https://manual.calibre-ebook.com/generated/en/ebook-viewer.html)).

---

## HTTP transport

With **`--http`**, the MCP server can expose helpers such as **`/api/v1/chat`**, proxying to a local Ollama or OpenAI-compatible API via **`LLM_PROVIDER`**, **`LLM_BASE_URL`**, **`LLM_API_KEY`** — aligned with the webapp backend LLM routes.

---

[← Back to project README](./README.md)
