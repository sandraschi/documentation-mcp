# 2026-10-18 - hn-50138531 - DeepSeek search and fetch, $0.75 per 1000 requests

- hn_id: 50138531
- title: DeepSeek search and fetch - $0.75 per 1000 successful requests
- points/comments at scan: 132 pts / 56 comments
- distilled_comments: 8 of 89 thread nodes
- hn_url: https://news.ycombinator.com/item?id=50138531
- source link: https://api-docs.deepseek.com/guides/search/
- date distilled: 2026-10-18 (morning session, opencode human-driven)

## How it surfaced

Top-20 HN scan (24h window). Companion to the v4.1-Flash-1017 model drop
(50129045): DeepSeek's own hosted search + fetch, exposed as MCP tools,
priced per successful request. Directly relevant to aiwatcher RAG search
provider choice (vs Tavily / Brave / Exa / self-hosted SearXNG).

## Distill result

thread_summary: The thread discusses DeepSeek's new search and fetch MCP
tools, which charge $0.75 per 1000 successful requests. Users compare this
pricing to alternatives like SearXNG and Kagi, noting DeepSeek's competitive
rate. Concerns are raised about anti-bot protections, rate limits, and the
lack of a free tier for testing.

positions:
- cost_efficiency (most): Pricing is competitive compared to other providers.
- technical_concerns (some): Anti-bot handling and rate limits questioned.
- alternatives (few): Some prefer free or self-hosted solutions like SearXNG.

disagreement: Practicality of paid-per-success pricing vs free alternatives,
plus technical limits (anti-bot, rate limits).

tools_mentioned: DeepSeek Search and Fetch MCP, SearXNG AI Kit, Kagi API,
Ollama Cloud.

try_this: Test DeepSeek's API with a small budget to evaluate performance
and cost before committing to larger-scale usage.

## Fleet action

- aiwatcher search provider eval: DeepSeek search/fetch MCP vs current
  Tavily/Brave/Exa mix. Cheap enough to trial on a small budget. Watch:
  anti-bot gaps, rate limits, no free tier. Open, low urgency.
