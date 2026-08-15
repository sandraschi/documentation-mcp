# User Interest Catalog (aiwatcher + arxiv-mcp)

**Established**: 2026-08-15
**Reference impls**: `aiwatcher-mcp` (feeds/bundles/EMAIL_RECIPIENTS), `arxiv-mcp` (watch authors/categories/codehunt)
**Cross-refs**: `patterns/AIWATCHER_IDE_HOST_SIGNAL.md`, `projects/sandrafleetbot/README.md`

## Purpose

Per-user interest catalogs decide **who gets what** in the fleet's digest/alert
pipeline. One person per catalog, one place per person, so opt-in/opt-out and
content selection are reviewable and don't require touching pipeline code.

**Context (2026-08-15):** Steve was removed from `EMAIL_RECIPIENTS` because the
digest was spammy for him. He opts back in once a catalog exists that matches
his interests. Do NOT add a recipient back to a global list without a catalog
entry for them.

## Catalog structure

Every user has one section. Required: interests (keywords), feeds/bundles,
arxiv watchlist, digest tone, alert level.

```yaml
sandra:
  interests: [fleet, mcp, llm, robotics, vla, music, tech-media]
  aiwatcher:
    bundles: [V4-Flash-Local, China-Open-Weights, Fleet]   # bundle ids/names
    email_recipient: true                                    # in EMAIL_RECIPIENTS
    digest_tone: terse                                       # terse | full | none
  arxiv:
    watch_authors: [research-team-x]                         # arxiv_mcp watch authors
    categories: [cs.AI, cs.LG, cs.RO]
    codehunt: true                                           # open-weight repo drops
steve:
  interests: [crypto, finance, ai-tools]                     # example — to be filled
  aiwatcher:
    bundles: []
    email_recipient: false                                   # opts back in per catalog
    digest_tone: none
  arxiv:
    watch_authors: []
    categories: []
    codehunt: false
```

## Where things live

| Concern | Location |
|---|---|
| Digest recipients | `aiwatcher-mcp/.env` → `EMAIL_RECIPIENTS` (comma list) + `config.py` default |
| Bundles (interests) | aiwatcher `bundles` table + `data/aiwatcher.sqlite3`; UI: `get_bundles_list`, `update_fleet_bundle`, `create_bundle_from_topic` |
| Feeds per bundle | `link_feed_to_bundle`, `find_feeds_for_topic` (probes URLs before adding) |
| Per-recipient tone | aiwatcher `DIGEST_TONE_*` env knobs (terse/full) |
| arXiv watch authors | `arxiv-mcp` watch-list (env/config + `arxiv_help(topic='watch_authors')`) |
| arXiv categories | `ARXIV_MCP_CODEHUNT_CATEGORIES` (default cs.AI, cs.RO, cs.SD) |
| Codehunt tracking | `arxiv-mcp` `data/arxiv_mcp/codehunt/tracking.sqlite3` |

## Rules

1. **One source of truth**: the catalog doc is the human-readable spec; the
   env/config values are the machine truth. Keep them in sync — any change
   updates both in one commit.
2. **Opt-in, not opt-out**: nobody is on a recipient list by default except
   the operator (Sandra). Adding a recipient requires a catalog entry first.
3. **Content matches interests**: a bundle added to a catalog must have at
   least one linked feed that was probe-validated (`find_feeds_for_topic`).
4. **No third-party infra for raw data**: digests/alerts sent outside the
   tailnet carry sanitized summaries only (see P2 posting policy in
   `projects/sandrafleetbot/README.md`).

## Adding a user

1. Add their section to this catalog with placeholder interests.
2. Interview them (or use `create_bundle_from_topic`) to build 1-2 bundles
   with probe-validated feeds.
3. Set arxiv watch authors/categories if relevant.
4. Add their address to `EMAIL_RECIPIENTS` (aiwatcher `.env` + `config.py`
   default) and restart the service: `nssm restart aiwatcher-mcp`.
5. Verify with `get_bundle_health` + a `generate_digest` preview before the
   first real delivery.

## Verification

- `nssm status aiwatcher-mcp` = SERVICE_RUNNING, `GET :10946/health` = 200
- Recipient list matches the catalog's `email_recipient: true` entries
- Every catalog bundle has ≥ 1 linked, probe-validated feed
- arxiv codehunt scan produces hits only for cataloged categories
