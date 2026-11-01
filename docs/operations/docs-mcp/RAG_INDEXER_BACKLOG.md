# RAG indexer hygiene

**Priority:** P2  
**Repo:** mcp-central-docs (`docs_mcp` ingest)

---

- Exclude binary/large files at ingest (images, PDFs over threshold, archives in-tree).
- De-duplicate near-identical chunks (cosine similarity > 0.98 across paths).
- Ingest report → `operations/RAG_INDEX_REPORT_<date>.md`: chunks per folder, skipped files, staleness distribution.
