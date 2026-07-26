---
title: "Fleet RAG Standard (2026)"
category: standard
status: active
audience: mcp-dev
skill_candidate: false
related:
  - src/docs_mcp/ARCHITECTURE.md
  - standards/FRONTMATTER_STANDARD.md
  - standards/LOCAL_LLM_STANDARDS.md
  - standards/LLM_AND_INSTALL_TIERS.md
  - standards/WEBAPP_SOTA_STANDARDS.md
last_updated: 2026-06-01
---

# Fleet RAG Standard (2026)

**Status:** Active fleet pattern  
**Canonical implementation:** `mcp-central-docs` → `src/docs_mcp/backend/rag_core.py`  
**Architecture detail:** [docs_mcp ARCHITECTURE](../src/docs_mcp/ARCHITECTURE.md)

---

## 1. Purpose

Define the **default Retrieval-Augmented Generation (RAG) stack** for fleet MCP servers and webapps. Goals:

- **Embedded first** — no separate vector DB service to install or babysit
- **Local embeddings** — no paid embedding API for baseline search
- **Shared wrapper** — one `BaseVectorStore` pattern across repos
- **Agent-friendly metadata** — YAML frontmatter filters in LanceDB

This doc is the **policy**. Implementation lives in `rag_core.py`, `ingestor.py`, and per-repo copies.

---

## 2. Canonical stack (mandatory default)

| Layer | Fleet choice | Notes |
|-------|--------------|-------|
| **Vector store** | [LanceDB](https://lancedb.com/) | Disk-backed, embedded, serverless |
| **Embeddings** | `BAAI/bge-small-en-v1.5` via [FastEmbed](https://github.com/qdrant/fastembed) | 384-dim, MIT, good speed/quality tradeoff |
| **Chunking** | 1000 chars, 200 overlap | Markdown-aware breaks (`ingestor.py`) |
| **Default top-k** | 5 | Tune per tool; cap agent payloads |
| **Synthesis** | Calling LLM (client or `ctx.sample()`) | RAG returns **chunks**, not final answers |

```python
from docs_mcp.backend.rag_core import BaseVectorStore

store = BaseVectorStore(
    db_path="/path/to/lancedb",
    table_name="documents",
    embedding_model_name="BAAI/bge-small-en-v1.5",
)

store.add_documents([
    {
        "id": "standards/agent-protocols#chunk-0",
        "content": "...",
        "metadata": {"category": "standard", "status": "active", "source": "standards/AGENT_PROTOCOLS.md"},
    }
])

hits = store.search("FastMCP startup probes", limit=5)
hits = store.search("active standards only", limit=10, where="metadata.status = 'active'")
```

**Why LanceDB + bge-small (not Chroma/Qdrant/Pinecone by default):**

- Zero background process — fits naked-PC and Tauri bundle constraints
- Same pattern in `docs_mcp`, optional RAG in `plex-mcp`, `calibre-mcp`, `myconf`, `tvtropes-mcp`, `obsidian-mcp`
- Sub-50 ms retrieval at fleet doc scale on local NVMe
- FastEmbed cache under repo `data/cache/fastembed` (see `config.CACHE_PATH`)

---

## 3. Document contract

Every indexed item MUST include:

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `id` | string | yes | Stable chunk id (`{path}#chunk-{n}`) |
| `content` | string | yes | Searchable text |
| `metadata` | dict | yes | Filters + provenance |
| `source` | string | recommended | Human-readable path or URI |

**Metadata from frontmatter:** Markdown ingest parses YAML per [FRONTMATTER_STANDARD.md](./FRONTMATTER_STANDARD.md). Store `category`, `status`, `audience`, `skill_candidate`, `last_updated` as filterable LanceDB columns.

**Exclude dirs during crawl:** `node_modules`, `.git`, `.venv`, `junk`, `backup`, `dist`, `__pycache__` (see `ingestor.EXCLUDE_DIRS`).

---

## 4. Pipeline

```
Ingest                    Index                     Retrieve                 Synthesize
──────                    ─────                     ────────                 ──────────
glob .md / folder    →    FastEmbed embed      →    query embed         →    LLM reads chunks
parse frontmatter         LanceDB table             cosine search            cites sources
chunk 1000/200 overlap    metadata columns          optional where=          (client-side)
```

### 4.1 Ingestion

- **MCD hub:** `ContentIngestor` in `ingestor.py`; UI folder ingest → `/api/v1/ingest_folder`
- **CLI:** `just search`, `just semantic`, `just report` (see [scripts/README.md](../scripts/README.md))
- **Reindex recipe:** per-repo `just reindex` where applicable (e.g. `obsidian-mcp`)

### 4.2 Retrieval

- Return **raw chunks + scores/distances** to the agent; do not silently substitute a canned answer
- Apply `where` pre-filters when the tool scope is narrow (e.g. `category = 'standard'`)
- Keep `limit` modest (5–20) to protect context window

### 4.3 Synthesis

- **Tier A (local):** Ollama / LM Studio — see [LOCAL_LLM_STANDARDS.md](./LOCAL_LLM_STANDARDS.md)
- **Tier B (cloud):** optional; never required for search-only tools
- **Install tiers:** never bundle models in MCPB/Tauri — [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md)

---

## 5. When to deviate

Use a **managed** vector DB only when embedded LanceDB is insufficient:

| Scenario | Consider |
|----------|----------|
| Multi-tenant SaaS, billions of vectors | Qdrant Cloud, Pinecone, Milvus cluster |
| Strict hybrid BM25 + vector at scale | Weaviate, Elasticsearch + dense vectors |
| Prototype only, throwaway | Chroma in-memory |

Document the deviation in the repo README and `glama.json` notes. Do **not** introduce a second default stack fleet-wide without updating this standard.

---

## 6. Webapp integration

Repos with a SOTA webapp SHOULD expose:

| Surface | Minimum |
|---------|---------|
| **Search page** | Query box + ranked chunks + source links |
| **Folder ingest** | Pick local path → index into LanceDB (MCD pattern) |
| **Reindex control** | Operator trigger after doc changes |

See [WEBAPP_SOTA_STANDARDS.md](./WEBAPP_SOTA_STANDARDS.md) § Embedded RAG.

**MCD reference ports:** frontend **10794**, backend **10795** — [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md).

---

## 7. Security

- Treat ingested text as **untrusted** at synthesis boundary — [PROMPT_INJECTION_HARDENING.md](./PROMPT_INJECTION_HARDENING.md)
- Do not index secrets (`.env`, tokens, private keys); extend `EXCLUDE_DIRS` for repo-specific sensitive paths
- Optional: metadata encryption for LanceDB at rest (MCD changelog — transparent metadata encryption)

---

## 8. Performance targets (fleet)

| Metric | Target |
|--------|--------|
| Query latency (p95, local index) | < 100 ms |
| Cold embed (first query after boot) | < 2 s |
| Ingest | Batch embed; log progress every N docs |

GPU (RTX 4090): accelerates FastEmbed during bulk ingest; query embed is CPU-fast enough at bge-small scale.

---

## 9. Roadmap (explicit non-goals today)

Not required for fleet compliance until promoted here:

- [ ] Cross-encoder re-ranking layer
- [ ] Hybrid BM25 + dense (LanceDB hybrid when stable for our scale)
- [ ] Multimodal blob indexing (images/video segments)
- [ ] Federated / multi-party RAG

Track experiments in repo-local `docs/` or `STATUS.md`; do not expand this standard with aspirational prose.

---

## 10. Reference repos

| Repo | RAG usage |
|------|-----------|
| **mcp-central-docs** | Canonical `BaseVectorStore`, docs MCP tools, web dashboard |
| **plex-mcp** | Optional LanceDB media metadata |
| **calibre-mcp** | Library semantic search |
| **myconf** | Meeting transcripts + insights tables |
| **tvtropes-mcp** | Trope/work semantic search |
| **obsidian-mcp** | Vault reindex |
| **jellyfin-mcp** | `RAGService` for media context |

---

## 11. Checklist (new RAG feature)

- [ ] Uses `BaseVectorStore` or documents why not
- [ ] Embedding model defaults to `BAAI/bge-small-en-v1.5`
- [ ] Chunks have stable `id` + `source` + filterable `metadata`
- [ ] Ingest excludes noise dirs
- [ ] Search tool returns chunks, not hallucinated summaries
- [ ] LLM synthesis is optional and tier-aware
- [ ] Ports registered in `WEBAPP_PORTS.md` if web-facing

---

**Owner:** Sandra Schi  
**Review:** Quarterly or when embedding model / LanceDB major version changes
