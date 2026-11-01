# OpenSERP — FOSS SERP API

**Status**: Active · **License**: MIT · **Language**: Go · **GitHub**: [karust/openserp](https://github.com/karust/openserp)
**Local port**: 7000 (outside fleet reserved range — no conflict)
**MCP server**: `npx -y @openserp/mcp` (OSS mode → `localhost:7000`; Cloud mode → `OPENSERP_API_KEY`)

## What

Self-hosted, MIT-licensed SERP (Search Engine Results Page) API. Single Go binary (~10 MB), 6 search engines, structured JSON output. Drop-in free replacement for SerpAPI ($50/mo).

## Engines

Google, Bing, Yandex, Baidu, DuckDuckGo, Ecosia — same JSON schema across all.

## Two versions: OSS vs Cloud

Same endpoints, same response schema — client code migrates in either direction, so you are never locked in. What differs is who fights the anti-bot war (see below).

| | Self-hosted OSS (this repo) | OpenSERP Cloud |
|---|---|---|
| Price | Free, MIT | Paid (see [openserp.org/cloud](https://openserp.org/cloud)) |
| Infra | You run it: Go binary, `openserp serve`, or Docker (`karust/openserp:latest`, `127.0.0.1:7000:7000`, `serve -a 0.0.0.0 -p 7000`) | Vendor runs it, you send HTTP + key |
| Auth | None. No accounts, no keys, nothing to rotate or age out | `OPENSERP_API_KEY` |
| Scraper freshness | Whatever binary/image you last pulled. Stale the moment engines move | Vendor updates centrally, you benefit immediately |
| IP reputation | Yours alone: one box, one IP, robotic patterns burn it fast | Vendor proxy pools, rotation, residential egress |
| Best for | Personal low-volume digging on localhost | Anything scheduled, fleet-scale, or "search must just work" |

## Limits and failure modes (read before trusting results)

The limits are not OpenSERP's — they are the search engines' anti-bot enforcement: rate limits, captchas, challenges, IP reputation blocks. Consequences for us:

- **Empty results are not absence.** A silent backend looks exactly like "nothing exists." The fleet rule (see `standards/SEARCH_TOOLING_POSTURE.md` rule 1): never treat empty search as absence — cross-check with `fetch` against a primary URL before calling anything rumor. (Observed 2026-09-20: a dead backend returned 0 hits for generic queries; the claims verified minutes later via direct fetch.)
- **Single-IP burn**: one box running megasearch repeatedly will hit captchas, then temp blocks, then silence. Low volume + cache on + `mode=any` keeps the profile small.
- **Staleness**: engines change markup and bot detection constantly. An 8-month-old image is fighting last year's war. See Docker hygiene below.
- **No keys to age out**: OSS mode has no credentials, so "it worked yesterday, silent today" is never a key problem. Suspect engine-side blocking or a dead local service (`:7000` empty) first.

## Docker / image hygiene

`--restart unless-stopped` restarts the *container*, not the *image*. A container happily restarts an 8-month-old binary with 8-month-old scrapers. Freshness discipline:

```powershell
docker pull karust/openserp:latest
docker images karust/openserp --format "{{.Repository}}:{{.Tag}} created {{.CreatedSince}}"
```

- Pull on a cadence (monthly is the sane floor for a solo dev; the arms race moves weekly).
- After pulling, recreate the container — the running one still uses the old layers until you do.
- If Docker Desktop itself is down (nothing on :7000, engine API 500s), no image age matters — revive the engine first, then check the container, then the image age, in that order.

## Tools (via MCP)

| Tool | Description |
|------|-------------|
| `search` | Query a specific engine |
| `mega_search` | Multi-engine deduplicated search |
| `fast_search` | Fastest available engine |
| `any_search` | First engine that responds |
| `image_search` | Image search |
| `extract` | URL content → clean markdown |
| `list_engines` | Available engines |
| `get_usage` | Cloud credit balance |

## Usage

```powershell
# Start local server
openserp serve -a 127.0.0.1 -p 7000

# Search
curl "http://127.0.0.1:7000/google/search?text=hello&limit=5"

# Via MCP (stdio)
npx -y @openserp/mcp
```

## Alternatives (when OSS SERP is the wrong pipe)

Official (ToS-clean, billed, thinner — reranked toward AI-answerable, smaller indexes, compliance filtering). Good for scheduled fleet polling; weak for frenzy discovery:

- **Tavily** (AI-native pair with Exa): search + extract, `search_depth: advanced`. Free 1k/mo at `tavily.com`. memops wiring exists, key pending (`TAVILY_API_KEY`).
- **Exa** (AI-native pair): embeddings-first neural search. Same shape as Tavily; not wired yet, follows the Tavily pattern line for line when wanted.
- **Brave** (`llm-context` grounding mode): cleanest grounding snippets.
- **Bing Search API, SerpAPI, Perplexity Sonar**: billed, official, thinner.

Primary (no SERP needed, highest signal): vendor research posts, MSRC/security bulletins, vendor engineering blogs, RSS/Atom, arXiv. Most of what the fleet cites lives here — fetch directly.

Full posture, risk ladder, and fleet rules: `standards/SEARCH_TOOLING_POSTURE.md` (auto order `openserp -> tavily -> duckduckgo -> serpapi -> bing`).

## The anti-bot arms race (and the TVTropes playbook)

Engines and guarded sites (Cloudflare et al.) A/B-test bot defenses continuously; any scraper is stale the day it ships. Two viable strategies, opposite poles:

1. **Outsource the race** (Cloud / official APIs): pay a vendor per call; they maintain scrapers, proxies, rotation. Correct for scheduled/fleet use.
2. **Be a polite guest** (personal digging): low volume, cache on, generous delays, backoff-and-retry on blocks, honest accounting of what got blocked. Correct for a human digging on localhost.

Worked example of strategy 2 in-fleet: `tvtropes-mcp` scrapes a Cloudflare-guarded site with 8–15s randomized delays between requests (`scraper_delay_min/max`), Cloudflare-block detection with 30s backoff-and-retry, per-page `blocked`/`retry_count`/`http_status` accounting in SQLite, and user-facing "blocked, backing off" messages. It survives *because* it is slow and polite — the exact posture prescribed above, and the exact opposite of what fleet-scale polling needs. Do not point megasearch-style volume at a site you also want to stay welcome on.

What does not work: high-volume scraping from one IP with no proxies, no backoff, and an old binary — then reading the empty results as truth.

## Fleet Relevance

- **Google v. SerpApi (2026-07-20)**: DMCA scraping lawsuit dismissed — public web data ruled fair game. Strengthens legal position for any scraping in fleet.
- **Use cases**: web-search tool for opencode/Claude, SEO rank tracking, LLM grounding, arxiv-mcp or browser-mcp enrichment.
- **No Docker required**: Go binary, runs as background process.

## Background

- [Google v. SerpApi — Court Grants Motion to Dismiss (SerpApi blog)](https://serpapi.com/blog/google-v-serpapi-the-court-granted-our-motion-to-dismiss/)
- [Google's lawsuit announcement](https://blog.google/technology/ai/serpapi-lawsuit/)
- [OpenSERP GitHub](https://github.com/karust/openserp)
- [OpenSERP MCP server](https://github.com/openserpapi/mcp)
