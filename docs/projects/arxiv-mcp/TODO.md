# arxiv-mcp — TODO
<!-- Cross-project context: D:\Dev\repos\mcp-central-docs\operations\INTEL_STACK_TODO.md -->

**Last updated:** 2026-06-03  
**Repo:** `D:\Dev\repos\arxiv-mcp`  
**Version:** 0.7.0  
**Ports:** backend :10770, frontend :10771

---

## ⚠️ P0 — REINDEX REQUIRED (do this first)

> **If you upgraded to 0.7 and have NOT reindexed, `search_depot_corpus` is returning wrong results.**
> The SQLite FTS depot is fine; only the LanceDB **vector index** is stale.

0.7 switched embeddings to **FastEmbed + `BAAI/bge-small-en-v1.5`**. Any index built with the
previous embedder produces garbage semantic search until rebuilt.

**Run once (pick one):**

```python
# MCP tool (Claude Desktop / Cursor with arxiv-mcp connected):
reindex_depot_vectors()
```

```powershell
# REST:
Invoke-RestMethod -Uri "http://127.0.0.1:10770/api/depot/reindex" -Method Post
```

- Non-destructive — FTS depot untouched, vectors rebuilt only
- Duration: few minutes depending on corpus size
- **No code changes required** — operational step only

---

## Status

Solid production state: LanceDB hybrid RAG, deep epistemic profiling, Prefab cards, runtime
introspection, Playwright e2e, readly **media traction** cross-connect (code-hunt path).

**Recently shipped (2026-06-05):** readly media traction, publication subscriber auth, bot-block
opt-in, Tech RSS + New Scientist feed, code-hunt affiliations. See `CHANGELOG.md`.

---

## P2 — Lab blog coverage gaps

**File:** `src/arxiv_mcp/lab_blog.py` — extend `SOURCES` registry (same pattern as Anthropic,
Google Research, DeepMind, Google AI Blog).

| Source key | Label | List URL | Notes |
|------------|-------|----------|-------|
| `mistral` | Mistral AI | `https://mistral.ai/news` | European lab; GDPR-relevant |
| `meta-ai` | Meta AI | `https://ai.meta.com/blog/` | Llama, open research |
| `huawei-noah` | Huawei Noah's Ark Lab | TBD — find stable blog index | Chinese frontier context |

**Per-source work:**

1. Add `SOURCES["mistral"]` with `sections`, `post_base`, `js_heavy` flag
2. Implement `list_posts` HTML scrape or RSS if available
3. Implement `fetch_post` content extractor; **Jina fallback** for JS-heavy pages
   (`ARXIV_MCP_JINA_READER_BASE_URL`, same as DeepMind)
4. Register in `tools_manifest.py` descriptions (no new tool names — `fetch_lab_post` / `list_lab_posts` are generic)
5. Add smoke test or manual checklist entry in `docs/MCP_SERVER.md`

**OpenAI Research:** Already covered by aiwatcher RSS feeds. Optional `openai-research` key here
only if epistemic profiling on cited papers is wanted (lower priority than Mistral/Meta).

---

## P3 — Readly cross-reference on depot ingest (CROSS-3)

**Status:** Media traction path ✅ (`probe_media_traction` → readly `POST /api/content/match`).  
**Open:** Store `readly_coverage` on **depot paper records** during `ingest_and_analyze_paper`.

### Goal

When a paper is ingested to the depot, optionally query readly-mcp for magazine articles covering
the same topic. Persist hits on the paper row for Prefab card + webapp paper detail.

### Config (`config.py` / `.env.example`)

```env
ARXIV_MCP_READLY_ENABLED=1
ARXIV_MCP_READLY_MCP_URL=http://localhost:10863
ARXIV_MCP_READLY_VALID_TILL=2026-12-31

# New for depot ingest (optional — empty = skip)
ARXIV_MCP_READLY_INGEST_MAGAZINES=New Scientist,Nature,Scientific American,Wired
ARXIV_MCP_READLY_INGEST_ON_DEPOT=1
```

Reuse `config/readly_watch_magazines.json` as default magazine list when env empty.

### Implementation sketch

**File:** `src/arxiv_mcp/depot_service.py` — end of `ingest_and_analyze_paper()` after successful ingest:

```python
async def _attach_readly_coverage(paper: dict) -> list[dict]:
    from arxiv_mcp.readly_client import readly_enabled, readly_base_url, load_readly_watch_magazines

    settings = load_settings()
    if not readly_enabled(settings) or not settings.readly_ingest_on_depot:
        return []

    title = paper.get("title") or ""
    magazines = settings.readly_ingest_magazines or load_readly_watch_magazines(settings)
    base = readly_base_url(settings)
    if not base or not title:
        return []

    async with httpx.AsyncClient(timeout=90) as client:
        resp = await client.post(
            f"{base}/api/content/match",
            json={"query": title, "magazines": magazines, "max_per_magazine": 2},
        )
    if resp.status_code != 200:
        return []
    hits = resp.json().get("hits") or resp.json().get("matches") or []
    return [
        {
            "magazine": h.get("magazine"),
            "title": h.get("title"),
            "url": h.get("url"),
            "match_score": h.get("match_score"),
            "source": "readly_mcp",
        }
        for h in hits[:10]
    ]
```

**Persist:** Add `readly_coverage JSON` column to depot SQLite (migration) or store in existing
`metadata_json` blob on paper record.

**Surface:**

- MCP `ingest_and_analyze_paper` return payload: `readly_coverage: [...]`
- Prefab paper card: optional “Magazine coverage” section
- Webapp paper detail (`GET /api/depot/paper/{id}`): include field
- `GET /api/settings/readly`: note `ingest_on_depot` flag

**Do not block ingest** on readly timeout — log warning, return `readly_coverage: []`.

Docs: extend `docs/READLY_INTEGRATION.md` with “Depot ingest” section.

---

## P3 — Backlog

| Item | Notes |
|------|-------|
| Calibre RAG cross-link | `store_paper_to_calibre` exists; `calibre_rag` semantic search not wired |
| Sampling cost guard | `ARXIV_MAX_SAMPLING_TOKENS` for `arxiv_agentic_assist` |
| arXiv → aiwatcher digest bridge | High-relevance `list_category_latest` → `ingest_fleet_event` on aiwatcher |
| Playwright: depot reindex UI smoke | Optional e2e after reindex button in webapp |

---

## Summary

| Priority | Action |
|----------|--------|
| **P0** | Reindex LanceDB vectors (operational, do now) |
| **P2** | Add Mistral, Meta AI, Huawei Noah to `lab_blog.py` |
| **P3** | `readly_coverage` on depot ingest |
| **P3** | Calibre RAG, sampling guard, aiwatcher fleet bridge |
