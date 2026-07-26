# chatvault — chat-history preservation (fleet gap, idea stage)

**Status:** Gap identified 2026-07-20 (during Ednaficator chronik session) · not built
**Tags:** [chatvault, fleet-gap, preservation, idea, medium]

## The gap

Years of Claude / Gemini / ChatGPT / Perplexity conversations — "Gott und die Welt,
not just dev work" — live inside vendor silos with no local, durable copy. By the
50-year principle (see ednaficator PRD): these are primary-source material about
Sandra's thinking and life, arguably chronik-grade, and currently one account
suspension away from gone.

## Honest feasibility

| Source | Export path | Reality |
|---|---|---|
| Claude | account data export (Settings → export) | full JSON, manual trigger, works |
| Gemini | Google Takeout | works, bulky, manual |
| ChatGPT | Settings → export | works, emailed zip |
| Perplexity | per-thread only | weakest; partial |

No consumer bulk APIs → the durable design is a **ritual, not a daemon**: monthly
export → drop zips into `chatvault/inbox/` → normalizer script → one markdown file
per conversation (`YYYY-MM-DD-slug.md`, frontmatter: source, date, title, tags) →
git repo. Plain markdown = the ednaficator longevity rule applies verbatim.
Playwright scraping as a fallback is fragile and ToS-gray — last resort, not design.

## v0 scope (≈1 day when picked up)

1. Repo `chatvault` (private): `inbox/`, `conversations/<source>/`, normalizer for
   the three export formats (Claude JSON, Takeout, ChatGPT zip)
2. Dedup by conversation ID; re-runs idempotent
3. Embedding index (same stack as chronik) + thin `chatvault-mcp` for querying
   from Claude Desktop ("what did I think about X in 2025?")
4. Calendar reminder for the monthly export ritual — the pipeline is worthless
   without the habit

## Later / maybe

Cross-link chronik-relevant chats into schipal-chronik intake (Sandra-gated, as
always) · sentiment/topic timelines · Cursor/Windsurf/opencode local histories
(different formats, already local, lower risk)

## Non-goals

Real-time sync · scraping daemons · anything that breaks when a vendor redesigns
their frontend
