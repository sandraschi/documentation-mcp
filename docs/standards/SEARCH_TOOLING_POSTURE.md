# Search Tooling Posture (2026-09-20)

**Status:** active. Applies to all fleet agents and scheduled polling (aiwatcher et al).
**Rule:** discovery quality must not depend on a single dead backend. Verification beats retrieval.

## What happened

2026-09-20: memops `web_search` (DuckDuckGo backend) returned 0 results for all
queries including generics, stamped Dec 2025, news off. Same claims verified
minutes later via `fetch_fetch` against primary URLs (THN, Snyk, Rapid7) and via
local OpenSERP (`karust/openserp`, Docker, `127.0.0.1:7000`). Lesson recorded:
a silent search backend looks exactly like absence. It is not.

## The pipes

- **Official (ToS-clean, billed, thinner):** Bing Search API, Brave (+ `llm-context`
  grounding mode), Tavily (`tavily_search` + `tavily_extract`), Exa (neural,
  embeddings-first), Perplexity Sonar. Reranked toward AI-answerable, smaller
  indexes, compliance filtering. Good enough for scheduled fleet polling. Weak
  for frenzy discovery. Tavily and Exa are the AI-native pair; Brave
  `llm-context` is the cleanest grounding-snippet pipe.
- **OSS SERP (grey, self-hosted, fuller):** OpenSERP MIT, six engines, one JSON
  schema, megasearch with dedupe. No keys, no billing. Engines' ToS forbid
  automated querying; anti-bot (rate limits, challenges, IP reputation) is the
  enforcement. Upstream ships resilient mode, cache, and proxy support for
  exactly this reason.
- **Primary (cleanest, highest signal for books):** vendor research posts,
  MSRC/security bulletins, vendor engineering blogs, RSS/Atom, arXiv.
  Fetchable directly, Tier 1, no SERP needed. Most of what the books cite
  lives here.

## Provider docs

### Tavily (wired 2026-09-20, key pending)

AI search built for agents. Separate search + extract calls, clean JSON,
`search_depth: advanced` for research queries, `include_domains` maps to
`sources_filter`. Free tier 1,000/mo at `tavily.com`.

- memops `adn_web_search` provider `"tavily"`: POST `https://api.tavily.com/search`
  with `{api_key, query, search_depth: advanced, max_results}`, maps
  `results[].title/url/content/published_date`. No key means auto skips it.
- Auto order: `openserp -> tavily -> duckduckgo -> serpapi -> bing`.
- OSS-vs-Cloud comparison, limits/failure modes, image hygiene, alternatives
  table, and the anti-bot arms race (TVTropes playbook):
  `integrations/openserp/README.md`.
- Env: `TAVILY_API_KEY`. Daemon runs as LocalSystem under NSSM
  (`advanced-memory-mcp-daemon`), so user env does not reach it. Elevated:
  `nssm set advanced-memory-mcp-daemon AppEnvironmentExtra TAVILY_API_KEY=<key>`,
  then `Restart-Service advanced-memory-mcp-daemon -Force`, confirm
  `http://127.0.0.1:10732/health` shows the new `git_sha`.
- Convention: key also saved to `~/.secrets/tavily` for parity.

### Exa (next, not wired)

Neural search (`exa.ai`), embeddings-first, research-style queries. Same shape
as Tavily: one key (`EXA_API_KEY`), search + contents calls, free tier.
Wire identically to Tavily in `adn_web_search.py` when wanted: provider entry,
POST branch, availability check on env, auto order after tavily. No code yet -
say the word and it follows the Tavily pattern line for line.

## Risk ladder

1. Personal low-volume on localhost (one human digging): lowest profile.
   Megasearch `mode=any`, cache on, a few queries a day. Realistic worst case
   is captchas and temp blocks.
2. Fleet scheduled polling through OSS SERP: higher profile, faster burn,
   proxy territory. Prefer official pipes here.
3. Commercial resale of scraped results: exposed. Get a contract.

## Fleet rules

1. Never treat empty search as absence. Cross-check with fetch against a
   primary URL before calling anything rumor.
2. Discovery may use OSS SERP on localhost. Fleet polling defaults to official
   pipes. Commercial use requires a contract.
3. AIWatcher `OPENSERP_URL=http://127.0.0.1:7000` / `BACKEND=oss` is personal
   digging only. If polling volume rises, move it to official keys.
4. Cloud OpenSERP later if wanted: same schema, vendor absorbs scraping risk
   for a fee. One `OPENSERP_API_KEY`, no local container.

## Current wiring (Goliath, 2026-09-20)

- Docker `openserp`: `karust/openserp:latest`, `--restart unless-stopped`,
  `127.0.0.1:7000:7000`, `serve -a 0.0.0.0 -p 7000`.
- opencode MCP `openserp`: enabled, `OPENSERP_BASE_URL=http://127.0.0.1:7000`.
  Takes effect on session restart. `agents/local.md` keeps `openserp_*: deny`
  to hold the local 27B tool surface at ~50.
- memops `web_search`: patched 2026-09-20 (openserp first, tavily second, live
  timestamp). Pending elevated daemon restart + `TAVILY_API_KEY`. Until a generic
  query returns non-zero, do not cite its silence.
