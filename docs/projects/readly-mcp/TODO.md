# readly-mcp — TODO
<!-- Cross-project context: D:\Dev\repos\mcp-central-docs\operations\INTEL_STACK_TODO.md -->
<!-- Downstream consumer: aiwatcher-mcp `readly_ingestion.py` + APScheduler `readly_poll` -->

**Last updated:** 2026-06-03  
**Repo:** `D:\Dev\repos\readly-mcp`  
**Version:** 0.2.0 → target **0.2.1** (watchlist pipeline)  
**Port:** :10863

## Status

**Shipped (v0.2):** `list_articles`, `extract_article_text`, `search_magazines`, `list_library`,
`GET /api/magazines/open`, `POST /api/content/match`, `GET /api/pipeline/liveness`. REST bridge live.
aiwatcher `readly_ingestion.py` calls `/api/articles/list` + `/api/articles/extract` today — single-page only.

**Blocks:** `INTEL_STACK_TODO.md` **CROSS-1** until P1 below ships.

---

## P1 — Watchlist pipeline (required)

### 1. `open_latest_issue()` — `src/readly_mcp/core/browser.py`

Combine `search_magazines` + `open_url` into one scheduler-friendly call. aiwatcher must open a
named magazine without two round-trips.

```python
# browser.py — add after open_url()

async def open_latest_issue(self, magazine_name: str) -> dict:
    """
    Search Readly for magazine_name, open the first catalogue result.
    Returns issue-level page when Readly redirects to current issue.
    """
    if not self.page:
        raise RuntimeError("Browser not started")

    name = (magazine_name or "").strip()
    if not name:
        return {"success": False, "error": "magazine_name required"}

    search = await self.search_magazines(name)
    results = search.get("results") or []
    if not results:
        return {
            "success": False,
            "error": f"Magazine not found: {name}",
            "query": name,
            "results_count": 0,
        }

    # Prefer catalogue/issue URLs over bare magazine landing pages
    pick = results[0]
    for candidate in results[:5]:
        url = candidate.get("url") or ""
        if "/read/" in url or "/issue/" in url or "catalogue" in url:
            pick = candidate
            break

    opened = await self.open_url(pick.get("url") or "")
    if not opened.get("success"):
        return opened

    return {
        "success": True,
        "magazine_name": name,
        "magazine_title": pick.get("title"),
        "url": opened.get("url"),
        "title": opened.get("title"),
        "issue_title": opened.get("title"),
    }
```

**REST:** `GET /api/magazines/latest?name=New+Scientist`  
**MCP tool:** `open_latest_issue(magazine_name: str)`  
**File:** `src/readly_mcp/server.py` — mirror `api_open_magazine` browser-start pattern:

```python
@app.get("/api/magazines/latest")
async def api_open_latest(name: str = ""):
    if not name.strip():
        raise HTTPException(status_code=400, detail="name parameter required")
    try:
        await browser_manager.start_browser(headless=False)
    except Exception as exc:
        logger.debug("Browser already running: %s", exc)
    return await browser_manager.open_latest_issue(name)
```

**Acceptance:** `GET /api/magazines/latest?name=New Scientist` returns `success: true` and
`page.url` contains readly domain; subsequent `list_articles` returns ≥1 article.

---

### 2. `read_all_articles()` — batch extractor with navigate-back

**Problem:** `extract_article_text(index)` navigates away from the issue index. After one extraction
the browser sits on an article URL; a second `list_articles()` sees article chrome, not the issue TOC.

**Solution:** Pin `issue_url` at batch start; re-`goto` issue between extractions; re-resolve index
from fresh listing each iteration (indices shift after navigation).

```python
# browser.py

async def read_all_articles(self, max_articles: int = 10) -> dict:
    """
    List articles on current issue page, extract full text for each.
    Navigates back to issue_url between extractions.
    """
    if not self.page:
        raise RuntimeError("Browser not started")

    issue_url = self.page.url
    listing = await self.list_articles()
    if listing.get("extraction_failed"):
        return {
            "success": False,
            "issue_url": issue_url,
            "error": listing.get("reason", "list_articles failed"),
            "articles": [],
            "count": 0,
        }

    articles_meta = (listing.get("articles") or [])[: max(1, max_articles)]
    results: list[dict] = []
    skipped: list[dict] = []

    for i, meta in enumerate(articles_meta):
        if self.page.url != issue_url:
            await self.page.goto(issue_url)
            await self.page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(1.5)
            # Re-list so index matches current DOM order
            listing = await self.list_articles()
            articles_meta = listing.get("articles") or []
            if i >= len(articles_meta):
                break
            meta = articles_meta[i]

        extracted = await self.extract_article_text(int(meta.get("index", i)))
        if extracted.get("error"):
            skipped.append({"index": meta.get("index"), "title": meta.get("title"), "error": extracted["error"]})
            continue
        if extracted.get("word_count", 0) < 50:
            skipped.append({"index": meta.get("index"), "title": meta.get("title"), "error": "low_word_count"})
            continue
        results.append(extracted)

    avg_wc = (
        sum(a.get("word_count", 0) for a in results) / len(results) if results else 0
    )
    _record_poll_stats(
        magazines_attempted=1,
        articles_extracted=len(results),
        avg_word_count=int(avg_wc),
        magazine=listing.get("issue_title"),
    )

    return {
        "success": len(results) > 0,
        "issue_title": listing.get("issue_title"),
        "issue_url": issue_url,
        "articles": results,
        "count": len(results),
        "skipped": skipped,
        "avg_word_count": int(avg_wc),
    }
```

**REST:** `GET /api/articles/read-all?max=10`  
**MCP tool:** `read_all_articles(max_articles: int = 10)`  
**Timeout:** REST handler should use 120s+ client timeout (10 articles × ~10s each).

**Acceptance:** After `magazines/latest`, `read-all` returns ≥3 articles with `word_count > 50`
for a subscribed magazine (e.g. New Scientist).

---

### 3. Scroll+wait loop in `list_articles()` — lazy DOM

Readly issue indexes lazy-load article cards. Current code breaks early at `results.length >= 3`
inside `page.evaluate`, so only ~3 articles appear.

**Change `list_articles()` in `browser.py`:**

```python
async def list_articles(self) -> dict:
    if not self.page:
        raise RuntimeError("Browser not started")

    await self.page.wait_for_load_state("domcontentloaded")
    await asyncio.sleep(1.5)

    # Trigger lazy-loaded article cards
    prev_count = 0
    for _ in range(5):
        await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1.0)
        count = await self.page.evaluate("""() => {
            return document.querySelectorAll('a[href*="/read/"]').length;
        }""")
        if count == prev_count:
            break
        prev_count = count
    await self.page.evaluate("window.scrollTo(0, 0)")
    await asyncio.sleep(0.5)

    page_title = await self.page.title()
    articles = await self.page.evaluate("""() => {
        // ... existing selector cascade ...
        // REMOVE early break: if (results.length >= 3) break;
        // Collect ALL matches per selector pass, dedupe by href
    }""")

    normalized = _quality_check_articles(articles)
    if normalized.get("extraction_failed"):
        return {
            "issue_title": page_title,
            "page_url": self.page.url,
            "articles": [],
            "count": 0,
            "extraction_failed": True,
            "reason": normalized["reason"],
        }

    return {
        "issue_title": page_title,
        "page_url": self.page.url,
        "articles": [
            {"title": a["title"], "url": a["url"], "index": i}
            for i, a in enumerate(normalized["articles"])
        ],
        "count": len(normalized["articles"]),
    }
```

---

### 4. Selector quality guard — nav elements vs articles

When primary selectors fail, the h1/h2/h3/h4 fallback returns **navigation chrome**
(Home, My Library, Search, Discover) instead of article titles. Downstream distillation then
scores nav labels as “articles”.

```python
# browser.py — module constants
_NAV_TITLE_BLOCKLIST = frozenset({
    "home", "my library", "search", "discover", "categories", "newsstand",
    "settings", "account", "sign in", "log in", "readly", "back", "menu",
    "magazines", "newspapers", "podcasts",
})

def _quality_check_articles(raw: list[dict]) -> dict:
    """Reject listings that look like nav/header scrape, not issue TOC."""
    cleaned = []
    for row in raw:
        title = (row.get("title") or "").strip()
        href = (row.get("url") or "").strip()
        if len(title) < 12:
            continue
        if title.lower() in _NAV_TITLE_BLOCKLIST:
            continue
        if not href and len(title) < 20:
            continue
        cleaned.append({"title": title[:200], "url": href})

    if not cleaned:
        return {"articles": [], "extraction_failed": True, "reason": "no_articles_after_filter"}

    # Nav leak detector: majority of titles are blocklisted short strings
    nav_hits = sum(1 for a in raw if (a.get("title") or "").strip().lower() in _NAV_TITLE_BLOCKLIST)
    if nav_hits >= 2 and nav_hits >= len(raw) // 2:
        return {"articles": [], "extraction_failed": True, "reason": "nav_elements_detected"}

    if cleaned and cleaned[0]["title"].lower() in _NAV_TITLE_BLOCKLIST:
        return {"articles": [], "extraction_failed": True, "reason": "nav_elements_detected"}

    return {"articles": cleaned, "extraction_failed": False}
```

Log at **WARNING** when `nav_elements_detected` — include `page_url` for debugging.

---

### 5. `list_library` issue URL verification

`list_library` may return magazine-level URLs instead of current-issue URLs.

**Action:** Manual test with subscribed account; document in `README.md`:

| URL pattern | Usable for watchlist? |
|-------------|----------------------|
| contains `/read/` or `/issue/` | ✅ open directly |
| `/magazine/` or `/catalogue/` only | ⚠️ needs `open_latest_issue` search path |

Watchlist pipeline should **not** depend on `list_library` until verified; use `magazines/latest` only.

---

## P2 — Resilience and health

### 6. Extend `/api/pipeline/liveness` with poll stats

**File:** `src/readly_mcp/server.py`

Add module-level `_last_poll_stats: dict` updated by `read_all_articles()` via `_record_poll_stats()`.

```python
_last_poll_stats: dict = {
    "magazines_attempted": 0,
    "articles_extracted": 0,
    "avg_word_count": 0,
    "low_yield_magazines": [],
    "last_run_at": None,
}

def _record_poll_stats(**kwargs) -> None:
    global _last_poll_stats
    from datetime import UTC, datetime
    _last_poll_stats.update(kwargs)
    _last_poll_stats["last_run_at"] = datetime.now(UTC).isoformat()
    if kwargs.get("articles_extracted", 0) < 2:
        mag = kwargs.get("magazine")
        if mag:
            lows = list(_last_poll_stats.get("low_yield_magazines") or [])
            if mag not in lows:
                lows.append(mag)
            _last_poll_stats["low_yield_magazines"] = lows[-10:]
```

Extend `api_pipeline_liveness` response:

```json
{
  "success": true,
  "healthy": true,
  "last_poll": {
    "magazines_attempted": 3,
    "articles_extracted": 12,
    "avg_word_count": 847,
    "low_yield_magazines": ["New Scientist"],
    "last_run_at": "2026-06-03T18:00:00+00:00"
  }
}
```

aiwatcher scheduler can log a warning when `articles_extracted == 0` after a poll batch.

---

### 7. Playwright selector fallback strategy (ongoing)

- Keep selector cascade documented in `browser.py` header comment.
- When Readly ships DOM changes, add new selectors **above** fallbacks, never rely on heading scrape alone.
- Consider screenshot-on-failure to `data/debug/` when `extraction_failed` (P3).

---

## P3 — Future

| Item | Notes |
|------|-------|
| Issue date SQLite cache | Skip re-scrape of same issue per magazine |
| `READLY_HEADLESS=true` | Test bot detection before enabling |
| arxiv depot crossref | `/api/content/match` exists; wire from arxiv `ingest_and_analyze_paper` (see arxiv-mcp TODO) |
| Visual verification | Playwright screenshot diff when `nav_elements_detected` |

---

## Implementation checklist

- [ ] `browser.open_latest_issue()`
- [ ] `browser.read_all_articles()` + `_record_poll_stats()`
- [ ] `browser.list_articles()` scroll loop + remove `>= 3` early break
- [ ] `_quality_check_articles()` + `_NAV_TITLE_BLOCKLIST`
- [ ] REST: `GET /api/magazines/latest`, `GET /api/articles/read-all`
- [ ] MCP tools: `open_latest_issue`, `read_all_articles`
- [ ] Liveness `last_poll` block
- [ ] Manual test script: latest → read-all for 2 magazines
- [ ] Bump version **0.2.1**, CHANGELOG, `llms.txt` tool list

---

## Test plan (manual)

```powershell
# readly-mcp running with READLY_AUTH_TOKEN set
Invoke-RestMethod "http://127.0.0.1:10863/api/magazines/latest?name=New Scientist"
Invoke-RestMethod "http://127.0.0.1:10863/api/articles/read-all?max=5"
Invoke-RestMethod "http://127.0.0.1:10863/api/pipeline/liveness"
```

Expect: `read-all.count >= 1`, each article `word_count > 50`, liveness shows `last_poll`.
