# Shelf Remote

**Model:** One-time $2.99–4.99 (or “buy me a coffee” IAP)  
**Comps:** Official Plex/Jellyfin apps (heavy); you want **minimal remote**

## Product

Connect to **one** Plex or Jellyfin server (URL + token). Browse libraries, play on server (cast to existing Plex client), or direct stream on phone. Poster grid, search, now-playing transport. Nothing else.

## Fleet reuse

| Piece | Source |
|-------|--------|
| API knowledge | [plex-mcp](../../integrations/plex-mcp.md), jellyfin-mcp project docs |
| Dark App Factory #06 | Plex Zero-Remote concept |

## Monetization

| Approach | Notes |
|----------|-------|
| **Paid upfront** | Honest for utilities — “Plex remote without bloat” |
| **Tip IAP** | Free core + optional support purchase |

Hard to win on features vs official apps; win on **speed and minimal UI** for your own server, then list for others.

## AI angle

- None in v1
- v2: Foundation Models “what should I watch?” from **local** library metadata only

## Effort / revenue

- **Effort:** Low–medium (REST client, AVPlayer)
- **Upside:** Small but global niche (self-hosters); good first StoreKit exercise

## Legal

- Not affiliated with Plex/Jellyfin — use trademarks correctly in listing
