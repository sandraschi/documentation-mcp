# Intelligence Stack — Cross-Project TODO & Assessment
<!-- Cursor: read this at the start of any session touching aiwatcher-mcp, arxiv-mcp, or readly-mcp -->

**Last updated:** 2026-06-05 (second pass)
**Scope:** aiwatcher-mcp · arxiv-mcp · readly-mcp
**Purpose:** Single source of truth for the tri-server intelligence pipeline.

---

## Architecture

```
readly-mcp (:10863) ──────────────────────────────────────────────┐
  Playwright browser, Readly.com login                            │
  list_articles / extract_article_text / list_library             │  full article text
  /api/content/match (arXiv cross-reference)                      │
  MISSING: /api/magazines/latest  ← BLOCKER                       │
  MISSING: /api/articles/read-all ← BLOCKER                       │
                                                                  ▼
arxiv-mcp (:10770) ──────── papers ──────────────────► aiwatcher-mcp (:10946)
  LanceDB hybrid RAG (BAAI/bge-small-en-v1.5)          APScheduler (7 jobs incl. readly)
  Deep epistemic profiling (claim-level)                Tiered flash/pro distillation
  Lab blog fetcher (4 sources)                          Relevance + Urgency 0–10
  DOI resolution + Calibre bridge                       Per-persona scoring (Sandra)
  ArXiv HTTP retry/backoff (http_policy.py)             Cloud allow-matrix
  10 MCP prompts                                        Daily HTML digest
                                                                  │
          robofang (:10871) ◄───── urgency ≥ 8.5 ────────────────┤
          speechops (:10895) ◄──── TTS wake-up ──────────────────┤
          email-mcp (:10812) ◄──── daily digest ─────────────────┤
          calibre-mcp (:10720) ◄── archival ─────────────────────┤
          fleet-agent-mcp / Fritz ◄─ day_prep briefing ──────────┤
          vla-mcp (:11024) ◄────── VLA bridge (config present) ───┘
```

---

## Current status (2026-06-05 second pass)

| Repo | Version | State |
|------|---------|-------|
| aiwatcher-mcp | 0.1.6 (needs 0.1.7 bump) | Code ahead of CHANGELOG. Readly pipeline implemented, awaiting readly-mcp endpoints. Tiered distillation shipped. |
| arxiv-mcp | 0.7.0 (unlogged additions) | http_policy.py + store_paper_to_calibre shipped but not in CHANGELOG. RAG reindex still required. |
| readly-mcp | 0.2.0 | Content tools shipped. **BLOCKER: watchlist endpoints not yet implemented.** |

---

## BLOCKER — readly-mcp endpoints (implement next)

aiwatcher's `poll_readly_articles()` is fully written and calls two endpoints that don't exist yet:

### `GET /api/magazines/latest?name=X`
**File:** `D:\Dev\repos\readly-mcp\src\readly_mcp\server.py` + `core\browser.py`

```python
# browser.py — add method:
async def open_latest_issue(self, magazine_name: str) -> dict:
    search = await self.search_magazines(magazine_name)
    results = search.get("results") or []
    if not results:
        return {"success": False, "error": f"Magazine not found: {magazine_name}"}
    return await self.open_url(results[0]["url"])

# server.py — add endpoint:
@app.get("/api/magazines/latest")
async def api_open_latest(name: str = ""):
    if not name:
        raise HTTPException(status_code=400, detail="name parameter required")
    try:
        await browser_manager.start_browser(headless=False)
    except Exception:
        pass
    return await browser_manager.open_latest_issue(name)
```

### `GET /api/articles/read-all?max=10`
**File:** `D:\Dev\repos\readly-mcp\src\readly_mcp\server.py` + `core\browser.py`

Batch-extracts all articles from current issue. Must navigate back to issue URL between
each article extract (since `extract_article_text` navigates away to the article page).

```python
# browser.py — add method:
async def read_all_articles(self, max_articles: int = 10) -> dict:
    issue_url = self.page.url
    listing = await self.list_articles()
    articles_meta = listing.get("articles", [])[:max_articles]
    results = []
    for article in articles_meta:
        if self.page.url != issue_url:
            await self.page.goto(issue_url)
            await self.page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(1.5)
        extracted = await self.extract_article_text(article["index"])
        if "error" not in extracted and extracted.get("word_count", 0) >= 50:
            results.append(extracted)
    return {
        "issue_title": listing.get("issue_title"),
        "issue_url": issue_url,
        "articles": results,
        "count": len(results),
        # extraction_failed / reason for aiwatcher health check:
        "extraction_failed": len(results) == 0,
        "reason": "no_articles_extracted" if len(results) == 0 else None,
    }

# server.py — add endpoint:
@app.get("/api/articles/read-all")
async def api_read_all_articles(max: int = 10):
    try:
        await browser_manager.start_browser(headless=False)
    except Exception:
        pass
    return await browser_manager.read_all_articles(max_articles=min(max, 20))
```

### Scroll+wait in `list_articles` (also needed for read-all to work properly)
**File:** `D:\Dev\repos\readly-mcp\src\readly_mcp\core\browser.py`

Add before the `page.evaluate()` in `list_articles()`:
```python
# Scroll to trigger lazy-loaded article list
for _ in range(3):
    await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await asyncio.sleep(1.0)
await self.page.evaluate("window.scrollTo(0, 0)")
await asyncio.sleep(0.5)
```

---

## aiwatcher-mcp — remaining items for 0.1.7

### `readly_watchlist` MCP tool (missing from server.py)
`set_runtime_readly_watchlist()` in `readly_ingestion.py` exists but no MCP tool calls it.

**File:** `D:\Dev\repos\aiwatcher-mcp\src\aiwatcher_mcp\server.py`

```python
from aiwatcher_mcp.readly_ingestion import (
    get_effective_readly_watchlist,
    set_runtime_readly_watchlist,
)

@mcp.tool()
async def readly_watchlist(action: str = "get", magazines: str = "") -> dict:
    """Get or mutate the Readly magazine watchlist at runtime.
    action: get | set | add | remove
    magazines: comma-separated names (required for set/add/remove)
    """
    current = get_effective_readly_watchlist()
    act = action.lower().strip()
    if act == "get":
        cfg = get_settings()
        return {
            "watchlist": current,
            "count": len(current),
            "readly_enabled": cfg.readly_enabled,
            "readly_mcp_url": cfg.readly_mcp_url,
            "poll_interval_hours": cfg.readly_poll_interval_hours,
        }
    parts = [p.strip() for p in magazines.split(",") if p.strip()]
    if act == "set":
        if not parts:
            return {"error": "magazines required for set"}
        set_runtime_readly_watchlist(parts)
    elif act == "add":
        if not parts:
            return {"error": "magazines required for add"}
        merged = list(current)
        for p in parts:
            if p not in merged:
                merged.append(p)
        set_runtime_readly_watchlist(merged)
    elif act == "remove":
        if not parts:
            return {"error": "magazines required for remove"}
        remove_set = {p.lower() for p in parts}
        set_runtime_readly_watchlist([m for m in current if m.lower() not in remove_set])
    else:
        return {"error": f"unknown action: {action}"}
    return {"action": act, "watchlist": get_effective_readly_watchlist()}
```

### Tests (add to complete 0.1.7)
- `tests/test_readly_ingestion.py` — mock httpx, watchlist loop, legacy fallback
- `tests/test_scheduler.py` — readly job registered when enabled + watchlist set
- `tests/test_config.py` — `parsed_readly_watchlist()` comma parsing, empty string
- `tests/test_server.py` — `readly_watchlist` get/set/add/remove

### CHANGELOG + version bump
- Bump `server_version` in `config.py` to `0.1.7`
- Bump `pyproject.toml`
- Write CHANGELOG entry covering: readly watchlist pipeline, tiered flash/pro distillation,
  cloud allow-matrix, VLA bridge config, scheduler retention job

---

## arxiv-mcp — remaining items

### CHANGELOG entries for unlogged shipped features
- `http_policy.py` — `ArxivApiFailure`, `arxiv_retry()`, structured backoff with `Retry-After` support
- `store_paper_to_calibre` — full `calibredb` pipeline with abstract→comments and optional Markdown TXT format
- `extensions` hook in `server.py` — `register_extension_tools` (no content yet, hook ready)

### P0: RAG reindex
**Still required** if not already done manually since 0.7.0 switched to FastEmbed BAAI/bge-small-en-v1.5.
```python
reindex_depot_vectors()
# or: POST http://localhost:10770/api/depot/reindex
```

### P2: Lab blog coverage gaps
- Mistral AI blog (`mistral.ai/news`) — most relevant European lab
- Meta AI blog (`ai.meta.com/blog`) — Llama releases
Add as new source keys in `lab_blog.py` with Jina fallback for JS-rendered pages.

### `extensions` module
`register_extension_tools` is hooked but the module doesn't exist yet. Either create
`src/arxiv_mcp/tools/extensions.py` with a no-op register, or remove the try/except
import until there's something to put in it. Current state: silently passes on ImportError,
which is fine but leaves a confusing breadcrumb.

---

## Cross-cutting

### CROSS-3: arxiv ↔ readly cross-reference [P3]
readly-mcp has `POST /api/content/match` accepting a query + magazine list, returning
articles whose titles overlap the query. When arxiv-mcp ingests a paper, it could optionally
call this to find magazine coverage of the same topic.

Config: `ARXIV_READLY_URL` (default empty = disabled), `ARXIV_READLY_MAGAZINES`.
Add as optional step in `ingest_and_analyze_paper`, storing `readly_coverage` in depot record.

### CROSS-4: Fritz longform urgency tuning [P2]
Fritz creates pulse tasks for urgency ≥ 8.0. Readly longform articles typically score
6-7 urgency even when highly relevant (they're not breaking news). Consider:
- Separate threshold: `FRITZ_READLY_URGENCY_THRESHOLD=6.5`
- Or: `relevance ≥ 7.5 AND tags contains readly` as an additional Fritz task trigger

### CROSS-5: VLA bridge in aiwatcher [P2]
`config.py` now has `VLA_MCP_URL=:11024` and `VLA_MCP_ENABLED=true`. No integration code
yet — the config field is a placeholder. When vla-mcp is stable, aiwatcher could ingest
VLA mission events as fleet journal items via `ingest_fleet_event`.

---

## Suggested watchlist

```
READLY_WATCHLIST=New Scientist,MIT Technology Review,c't,Wired,Die Presse,NZZ,IEEE Spectrum,Scientific American,Nature,New Statesman
```

---

## Fragility notes

- **Readly DOM selectors are the weakest link.** Readly React app updates break selectors
  silently. The `extraction_failed` / `word_count` guards in aiwatcher's `_ingest_article()`
  (wc < 50 threshold) are the only defence.
- **Browser state is global.** `browser_manager` is a module-level singleton in readly-mcp.
  Don't run `smart_scrape` concurrently with the aiwatcher scheduler polling.
- **READLY_AUTH_TOKEN is session-only.** Re-set via `POST /api/auth/token` after restart.
- **ArXiv retry backoff.** `http_policy.py` adds systematic retry but arXiv's rate limits
  are aggressive (~3s between API calls). `ARXIV_MCP_CLIENT_DELAY_SECONDS` default is 3.0.
