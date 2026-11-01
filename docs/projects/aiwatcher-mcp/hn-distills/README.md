# HN Distills Archive (aiwatcher-mcp)

Running archive of on-demand HN thread distills (`hn_distill_thread`).
Session-log files rotate after 30 days - this directory keeps the distills
that are worth finding again: security disclosures, model drops, tool
verdicts, ideas for the fleet.

## SOP - adding a distill

1. One file per distill: `YYYY-MM-DD-hn-<hn_id>-<slug>.md`
2. Frontmatter block at top: hn_id, title, points/comments at scan time,
   distilled_comments, hn_url, date distilled.
3. Body: thread_summary, positions, disagreement, tools_mentioned, try_this
   (straight from the distill JSON), plus a `Fleet action` line when Sandra
   or Steve should do something (rotate keys, try a tool, watch a repo).
4. Add a row to the index below, newest first.
5. Point at it from the day's session-log entry (pointer, not a copy).
6. Keep it ASCII: hyphens only, no em dashes, no smart quotes.

Distill cost note: one LLM distill per task max (~30-90s on local Ollama).
Since 2026-10-18 the tool fails fast with `{busy:true}` / `{timeout:true}`
instead of hanging past the MCP client timeout - on either, retry with
`max_comments=8`.

## Index (newest first)

| Date | HN id | Title | Signal |
|------|-------|-------|--------|
| 2026-10-18 | 50138531 | DeepSeek search and fetch, $0.75/1000 req | RAG search provider candidate - trial on small budget |
| 2026-10-18 | 50129045 | DeepSeek-v4.1-Flash-1017 | Open model drop - eval candidate, watch token burn |
| 2026-10-18 | 50133401 | OpenCode Hacked: User credentials leaked | Security - rotate OpenCode provider keys now |
