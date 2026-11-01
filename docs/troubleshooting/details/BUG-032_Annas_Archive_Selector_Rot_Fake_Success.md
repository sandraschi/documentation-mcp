# BUG-032: rtorrent-mcp's Anna's Archive search returns fabricated "success" on scraper miss

**Discovered:** 2026-09-08 (rtorrent-mcp, checking book availability for two AI-safety titles)
**Severity:** P2 (no crash, no data loss — but the tool actively misreports state as a valid empty/negative result)
**Component:** `src/rtorrent_mcp/services/annas_archive_search.py` (`_search_annas_on`), exposed via `GET /api/search/annas` on the local FastMCP backend (port 10910)
**Status:** Open — documented, not yet fixed

## Symptom

`GET /api/search/annas?query=Bostrom+Superintelligence&content_type=books`
against the already-running local backend returned:

```json
{"success":true,"query":"Bostrom Superintelligence","count":1,"results":[
  {"title":"No records foundTry broadening the search, changing language or
    file type filters, or browsing a different category.","author":"",
    "detail_url":"https://annas-archive.is/search?q=Bostrom+Superintelligence",
    "size":"Unknown","format":"Unknown","content_type":"books",
    "note":"Visit detail_url for full torrent info (can be 100TB+!)"}
]}
```

`success: true`, `count: 1` — this reads as a valid single hit to any caller
(human or agent) that doesn't inspect the `title` field closely. It is not a
hit. It's Anna's Archive's own empty-state copy, scraped as if it were a
result row.

Same query run against `annas-archive.is` directly (same User-Agent, no
cookie) returned a genuine `HTTP 200`, page title
`Search results for "Bostrom Superintelligence" | Anna's Archive`, zero
Cloudflare/challenge markers, and candidate `class="bg-white...` result
containers present in the markup — i.e. the site is up, not bot-blocking,
and appears to have real results to show. The scraper's selector chain in
`_search_annas_on` (`div.bg-white.rounded-lg` → `div.search-result` → ...
→ fallback `a[href*="/md5/"]`) does not match the site's current DOM
structure closely enough to extract them, and whatever downstream path
produces the final result list falls back to packaging the page's own
"No records found..." empty-state text as a fake result entry instead of
returning an honest `results: []` with a flag that extraction failed.

## Why this matters more than a normal empty result

This is the same failure class already tracked twice in this depot
(BUG-021, BUG-024): **a silent fallback masks the real state.** A caller
asking "is this book on Anna's Archive" gets back `success: true, count: 1`
and a plausible-looking (if malformed) result object. Nothing signals that
the scraper broke rather than the search coming up empty. An agent
downstream would report "not found" with false confidence.

## Root cause (probable)

Anna's Archive's frontend markup has drifted from what the selector chain
was written against. The code already anticipates this class of failure
("Anna's Archive has a very idiosyncratic UI... structure may vary") with a
multi-selector fallback chain, but has no terminal "all selectors and all
fallbacks missed" branch that returns an honest failure state — it appears
to fall through to treating the page's empty-state text as scrapable
content.

## Suggested fix

1. Add a terminal check: if `result_containers` is empty AND the fallback
   link selectors are empty, return `(results=[], error="no results
   extracted — selectors may be stale")` rather than any placeholder result
   row.
2. Re-derive the current selector set against a live fetch of
   `annas-archive.is/search?q=...` (structure confirmed reachable and
   real as of 2026-09-08) rather than guessing further selectors blind.
3. Consider a smoke test that asserts a known-available title (e.g. a
   public-domain classic) returns `count > 0` with real titles, to catch
   this class of drift automatically instead of via manual investigation.

## Log Snippet

```
$ curl -s "http://127.0.0.1:10910/api/search/annas?query=Bostrom+Superintelligence&content_type=books&max_results=5"
{"success":true,"query":"Bostrom Superintelligence","count":1,"results":[{"title":"No records found...
```

```
$ curl -si "https://annas-archive.is/search?q=Bostrom+Superintelligence"
HTTP/1.1 200 OK
<title>Search results for "Bostrom Superintelligence" | Anna's Archive</title>
(0 cloudflare/challenge/captcha markers; 5 candidate "bg-white" class matches)
```
