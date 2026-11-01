# AIWatcher — IDE Host Signal bundle

**Status:** Active  
**Updated:** 2026-07-27  
**Owner:** aiwatcher-mcp (`IDE Host Signal` bundle preset)  
**Related:** [MCP_UX_3_13_DIGEST.md](../ecosystem/cursor/MCP_UX_3_13_DIGEST.md)

Community buzz (Reddit, HN, Cursor forum) often ships **days before** [cursor.com/changelog](https://cursor.com/changelog). This bundle scores host-IDE and MCP-integration changes for the fleet.

---

## What it watches

| Source | Signal |
|--------|--------|
| r/cursor, r/CursorAI | UX regressions, MCP auth, approval timeouts |
| HN (cursor MCP/IDE, Zed, Windsurf) | Early adopter reports |
| forum.cursor.com/latest.rss | Official-ish community posts |
| Google News (cursor IDE MCP changelog) | Press + changelog keywords |
| Zed / opencode GitHub releases | Peer IDE releases |

Preset lives in `aiwatcher-mcp/src/aiwatcher_mcp/bundle_presets.py`. Applied on every `init_db()` via `ensure_fleet_bundle_presets()`.

---

## Daily / weekly agent loop

**After Cursor update or when MCP UX feels different:**

```text
1. poll_feeds
2. distill_pending
3. get_top_items (filter mentally: IDE Host Signal bundle / tags host-ux, changelog-gap)
4. check_alerts
```

**Weekly digest maintenance (5 min):**

1. `get_bundle_health` for **IDE Host Signal** — disabled feeds → fix URL or remove.
2. Any item with **urgency ≥ 8** and tag `changelog-gap` not in [MCP_UX_3_13_DIGEST.md](../ecosystem/cursor/MCP_UX_3_13_DIGEST.md) → add an **Observed** bullet with date + source link.
3. Optional: `inbox_add` or memops `adn_notes` for confirmed breaking changes.

**Token frugality:** do not re-distill old threads; rely on scheduled `distill_pending` (default every 6h). Manual `poll_feeds` only when hunting a specific rumor.

---

## Portfolio watch boost

Default `PORTFOLIO_WATCH_TERMS` (in `.env` / config) includes:

`cursor`, `windsurf`, `zed`, `auto-review`, `mcp approval`, `memops`, `changelog`

Items matching terms get `portfolio-watch` tag + urgency boost — surfaces in main digest even before bundle-specific review.

---

## Discord (optional phase 2)

For channels you already monitor (Cursor Discord `#announcements`, etc.):

- **discord-mcp** `get_messages` on a schedule
- Summarize → **aiwatcher** `inbox_add` (do not duplicate full RSS pipeline)
- Respect Discord 429 limits — 2–4h poll interval max

---

## Verify bundle exists

MCP tools:

```text
get_bundles_list
get_bundle_health(bundle_id=<IDE Host Signal id>)
list_fleet_bundles   # reads mcp-central-docs/operations/bundles.json
```

Webapp: **Bundles** page → **IDE Host Signal** → linked feeds green.

Restart aiwatcher backend once after deploy so `init_db` runs preset migration.

---

## References

- [operations/bundles.json](../operations/bundles.json) — fleet catalog entry `ide-host-signal`
- [aiwatcher-mcp/docs/IDE_HOST_SIGNAL_BUNDLE.md](../../aiwatcher-mcp/docs/IDE_HOST_SIGNAL_BUNDLE.md) — repo-local mirror
