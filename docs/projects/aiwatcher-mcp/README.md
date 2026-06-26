# aiwatcher-mcp

**Type:** MCP Server + Webapp  
**Status:** Active — Production-Capable  
**Version:** 0.1.0 (pyproject) / 0.2.0 (feature track)  
**Ports:** Backend **10946** / Frontend **10947**  
**Repo:** `D:\Dev\repos\aiwatcher-mcp`  
**GitHub:** https://github.com/sandraschi/aiwatcher-mcp  
**Glama:** https://glama.ai/mcp/servers?query=sandraschi  
**Last assessed:** 2026-05-01

---

## Description

Personal AI news intelligence system. Polls RSS/Atom feeds, arXiv, Gmail (Alpha Signal newsletters), and Readly magazines; scores items with Claude or local LLMs (Ollama/LM Studio); fires voice wake-ups via speechops for urgency ≥ 8.5; delivers a daily HTML digest to Sandra and Steve by email. Interest bundles allow multiple scoring personas on the same ingestion pipeline.

The fleet's situational awareness layer — compresses the firehose of AI tooling news into what actually matters for the fleet, portfolio, and daily decisions.

---

## Architecture

```
APScheduler (5 background jobs, UTC)
  ├── poll_all_feeds()    30m  — RSS/Atom/arXiv/Gmail/Readly
  ├── distill_items()      6h  — LLM scoring (relevance + urgency 0-10)
  ├── process_alerts()  04:55  — robofang + speechops TTS for urgency ≥ 8.5
  ├── generate_digest() 06:00  — HTML email → Sandra + Steve + Calibre
  └── expire_old_items() 03:00 — retention (default 90d, keep urgency ≥ 8.5)

Ingestion: feedparser (RSS/Atom) + arXiv-mcp + Gmail-mcp + readly-mcp
Distillation: Anthropic | Ollama | LM Studio (OpenAI-compat)
Storage: SQLite + FTS5 (BM25) + WAL + cross-feed dedup (difflib 0.85/48h)
Transport: FastMCP MCP + Starlette REST (dual, same process, port 10946)
```

---

## MCP Tools (20)

| Tool | Purpose |
|------|---------|
| `poll_feeds` | Manually trigger feed poll |
| `distill_pending` | Run LLM scoring on-demand |
| `check_alerts` | Fire alert pipeline on-demand |
| `generate_digest` | Preview/regenerate digest |
| `send_digest_now` | Force-send outside schedule |
| `get_top_items` | Top scored items by urgency |
| `get_feeds_list` | List feeds with health status |
| `add_feed` | Add RSS/Atom feed |
| `get_feed_health` | Degraded/disabled feed report |
| `search_items` | FTS5 full-text search |
| `get_digest_history` | List persisted digests |
| `expire_old_items` | Manual retention trigger |
| `get_bundles_list` | List scoring bundles (SQLite) |
| `list_fleet_bundles` | List bundles (MCD JSON) |
| `create_bundle_from_topic` | LLM-elicit + create bundle |
| `update_fleet_bundle` | Edit bundle config |
| `link_feed_to_bundle` | Associate feed with bundle |
| `get_bundle_health` | Per-bundle stats + top tags |
| `find_feeds_for_topic` | Discover + verify real feeds |
| `import_opml` | Bulk import from OPML XML |

Prompts: `breaking_news_brief`, `portfolio_impact_analysis`  
Resources: `aiwatcher://feeds/list`, `aiwatcher://stats`  
Prefab UI: `show_dashboard_card`

---

## Start

```powershell
.\start.bat        # or start.ps1
# Manual:
uv run -m aiwatcher_mcp.api   # backend + MCP :10946
cd webapp && npm run dev       # frontend :10947
```

---

## Configuration (`.env`)

Key settings:

| Var | Default | Notes |
|-----|---------|-------|
| `LLM_PROVIDER` | `anthropic` | `anthropic` / `ollama` / `lmstudio` |
| `DISTILLATION_MODEL` | `claude-3-5-sonnet-latest` | Any model on provider |
| `ALERT_THRESHOLD` | `8.5` | Urgency score to trigger TTS wake-up |
| `FEED_POLL_INTERVAL_MINUTES` | `30` | Feed polling cadence |
| `EMAIL_ENABLED` | `false` | Enable digest email delivery |
| `ROBOFANG_ENABLED` | `true` | Robofang Council alert integration |
| `CALIBRE_ENABLED` | `false` | Archive digests to Calibre library |

---

## Fleet Integrations

| Integration | Status | Notes |
|-------------|--------|-------|
| speechops | Active | TTS wake-ups via `/api/v1/tts`, SAPI5 fallback |
| robofang | Active | Breaking news events via `/api/v1/events` |
| email-mcp | Optional | Digest delivery; SMTP fallback |
| calibre-mcp | Optional | Archive digests as ebooks |
| arxiv-mcp | Optional | cs.AI/cs.LG/cs.RO ingestion |
| gmail-mcp | Optional | Alpha Signal newsletter parsing |
| readly-mcp | Optional | Magazine article ingestion |

---

## Known Issues (as of 2026-05-01)

See `ASSESSMENT.md` for full detail.

**P1:**
- `.env` may be git-tracked — contains secrets, must verify `git rm --cached .env`
- `GET /api/env` returns raw API keys + SMTP password in cleartext — no auth guard
- `/api/capabilities` reports 11 tools, actual count is 20

**P2:**
- No pagination on `/api/items`
- `sent_calibre` DB column is dead code
- OPML import logic duplicated between `server.py` and `api.py`
- `speechops_backend_url` default points at own port (10946) — wrong
- `validate_distillation_model()` fires live API call on every startup

---

## Stack

| Component | Version |
|-----------|---------|
| Python | ≥3.11 |
| fastmcp | ≥3.2.0 |
| starlette | ≥0.46.0 |
| apscheduler | ≥3.10.4 |
| aiosqlite | ≥0.20.0 |
| anthropic | ≥0.52.0 |
| feedparser | ≥6.0.11 |
| React | 18.x |
| Vite + Tailwind + Zustand + TanStack Query | current |

---

## Tags

`[aiwatcher-mcp, fastmcp, news-ingestion, distillation, alerting, scheduling, sqlite, active, webapp]`
