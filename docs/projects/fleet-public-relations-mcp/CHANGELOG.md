# Changelog

## v0.1.2 (2026-07-26)

- Tone: ban AI *authorship* self-promo (“written by AI”, “no human involved”); still name MCP/Cursor plainly
- Outbound lane: scraper-mcp readiness gate, FLEET_PROMOTION tone lint, draft engine
- Tools: `pr_readiness_check`, `pr_tone_lint`, `pr_draft`, `pr_approve_draft`, `pr_queue_fediverse`, `pr_campaign_status`
- Handoff to mastodon-mcp outbox only (no inline Mastodon API)
- Webapp: Campaigns + Drafts pages
- SQLite campaigns/drafts tables

## v0.1.1 (2026-07-25)

- assfix: Claude Code session context injection (.claude-plugin + hooks)
- assfix: Windsurf/GitHub Copilot session context rules
- assfix: Dashboard hero section with backend status + quick-start guidance
- assfix: LLM provider multi-detect (Ollama/LM Studio/vLLM) in Settings page
- assfix: `gates-green` recipe in justfile
- assfix: `_error_response()` helper with `logger.exception()` auto-logging
- assfix: `logger.exception()` in all except blocks (was `log.warning`)
- assfix: pytest coverage config (30% threshold) + `pytest-cov` dep
- assfix: Zustand store for LLM provider state (shared between Chat + Settings)
- assfix: Chat is now skill-first (fetches `GET /api/skills` on mount, uses skill content as base preprompt)
- assfix: `GET /api/skills` endpoint on backend
- assfix: Chat controls bar shows active skill name (`skill:fleet-pr-outreach`)
- assfix: Shared LLM provider probe utility (`lib/provider.ts`)
- assfix: Updated Settings to use Zustand store + shared probe utility
- assfix: StatCard data-testid forwarding
- assfix: `.gitignore` coverage for `*.bak`, `reports/`

## v0.1.0 (2026-07-14)

- Initial scaffold: FastMCP 3.4.4 server with 4 core PR outreach tools
- Starlette REST API on port 11094
- SQLite-backed thread/feedback store
- LLM competency evaluator via OpenAI-compatible endpoint
- RahRah Shield spam filter (crypto-shill blocklist)
- Admiral alert push integration
- Vite/React/Tailwind dashboard on port 11095
- Pages: Dashboard, Threads, Feedback, Settings
- Ctrl+Scroll zoom hook, backend-status health polling
- 6 passing tests, ruff + tsc clean
