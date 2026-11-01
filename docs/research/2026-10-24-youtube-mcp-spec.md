# youtube-mcp spec (pilot: Matthew Berman / Forward Future)

**Date:** 2026-10-24 (Europe/Vienna)
**Status:** SPEC - no code yet. Pilot first via RSS, build only if pilot sticks.
**Ask:** auto-follow a few fave YouTubers (Berman first). Compact text + links in, distilled digest out - same shape as AlphaSignal email flow.

## 1. Why not just keep email?

Forward Future email already lands in `AI` folder and works. Native YT wins when:
- email is late / truncated / safelink-wrapped (AlphaSignal links all route via `app.alphasignal.ai/c` tracker)
- you want transcripts (search "what did Berman say about DeepInfer?" beats rewatching 40 min)
- you want per-video scoring in AIWatcher bundles, not one daily blob

If none of those matter after 2 weeks, don't build.

## 2. v0 pilot (no new repo, this week)

- Add to `rss-mcp` or AIWatcher feeds, one feed per channel:
  `https://www.youtube.com/feeds/videos.xml?channel_id=<id>`
- Resolve handle -> channel_id once (yt-dlp / view-source / YouTube Data API). Berman pilot:
  - Forward Future (Matthew Berman) - resolve channel_id, add feed, poll 6h
  - +2 faves TBD (Sandra to name)
- Test: do you click native YT items more than the email digest? If yes -> v1.

## 3. v1 youtube-mcp (only if v0 sticks)

Portmanteau, same fleet patterns as email-mcp / readly-mcp:

```
channels_add(url_or_handle) / channels_list / channels_remove
videos_recent(channel_id?, days=3, limit=20)   # RSS first, Data API optional
video_detail(video_id)                          # title, published, duration, chapters
transcript_get(video_id, lang="en")             # youtube-transcript-api / yt-dlp captions
watchlist_poll(hours=6)                         # new videos since last poll
digest(channel_id?, days=3, push_aiwatcher?)    # transcript -> sampling summary -> markdown + aiwatcher inbox_add
```

Sources in order:
1. RSS (no key, titles/links/dates - covers 80%)
2. Captions (no key, `youtube-transcript-api` or `yt-dlp --write-auto-subs --skip-download`)
3. YouTube Data API v3 (optional, needs key, for search / stats / chapters). Keep behind flag.

Distillation mirrors email flow proven 2026-10-24:
fetch -> strip HTML -> compact text + links (<=6000 chars) -> `aiwatcher inbox_add(tags=youtube, urgency_hint)` -> `distill_pending` -> bundle `Sandra's AI Research` + morning digest.

## 4. Matthew Berman pilot definition of done

- [ ] channel_id resolved, RSS feed live in watcher
- [ ] 3-day crawl shows last ~3 Berman videos with durations
- [ ] 1 video transcript fetched, <6000 chars, readable in-page
- [ ] 1 distilled digest pushed to AIWatcher, appears in `search_items(query=Berman)`
- [ ] Sandra reads native digest 2 weeks instead of email - verdict build/kill

## 5. Fleet fit / triage

- Overlap check: `rss-mcp` (generic RSS), `substack-mcp` (newsletter shape), `readly-mcp` (magazine poll), `aiwatcher-mcp` (scoring/digest). youtube-mcp adds: channel resolution + captions + watchlist polling. No duplication if scoped to that.
- New Repo Gate: clean REST/RSS + no host-owned process -> Bucket A/B -> **Pure-Rust ArtCraft** if we build for real, not Python FastMCP. v0 pilot avoids the question entirely.
- Ports: claim from WEBAPP_PORTS only at v1 build time. Webapp catch-them-all applies (Dashboard/Inbox/Tools/Chat/Settings/Help/Logs + Channels/Videos/Digest pages).
- Costs: RSS + captions free. Data API quota free tier covers a few channels; only pay if searching at scale.
- Risks: caption IP blocks on datacenter IPs (use residential poll, cache aggressively), Shorts noise (filter <2min unless tagged), duplicate email+YT items (dedupe by title similarity in digest step).

## 6. Effort

- v0 pilot: 30 min (3 RSS feeds + 6h poll).
- v1 MVP: backend 6 tools + 1 webapp page + digest push, ~2 evenings. Same shape as mailing-lists page just shipped in email-mcp (`/mailing-lists`: presets + crawl + distill in-page + push AIWatcher).
- Kill rule: if pilot CTR < email CTR after 2 weeks, archive spec, no repo.

Related: `research/2026-10-24-gpu-marketplace-shadeform-vastai-host-economics.md`, email-mcp `docs/MAILING_LISTS.md`, AIWatcher bundle 1.
