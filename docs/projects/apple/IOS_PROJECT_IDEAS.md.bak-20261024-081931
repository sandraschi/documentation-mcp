# iOS Project Ideas ÔÇö Fleet-Connected iPad Apps

**Status**: IDEATION  
**Date**: 2026-05-29  
**Context**: Fleet of ~105 MCP servers on a 24-core AMD / RTX 4090 / 64GB server.
iPad apps connect via Tailscale + FastAPI HTTP bridges already exposed by every fleet MCP.

**Active build:** **[CalFolio](./CALFOLIO.md)** (was ÔÇ£Calibre CompanionÔÇØ below) ÔÇö first Apple dev on Mac.  
**Hub:** [README.md](./README.md) ┬À **Reader:** [EPUB_READER.md](./EPUB_READER.md) ┬À **Publish:** [IOS_PUBLISHING.md](./IOS_PUBLISHING.md)

### Roadmap tags

| Tag | Meaning |
|-----|---------|
| **`ship`** | Standalone App Store app ÔÇö worth a repo and maintenance |
| **`ship-active`** | Shipping now (CalFolio) |
| **`merge-calfolio`** | Feature inside CalFolio, not a separate app |
| **`merge-fleet-health`** | Feature inside Fleet Health (#2 app), not separate |
| **`later`** | Possible second/third app after CalFolio + Fleet Health prove the pattern |
| **`showcase-only`** | Demo, video, or personal use ÔÇö no product commitment |
| **`skip`** | Do not build; crowded, tiny TAM, or duplicate |

---

## Connectivity Pattern

Every fleet MCP exposes a FastAPI REST bridge alongside its stdio MCP transport:

```
iPad app  ÔöÇÔöÇTailscaleÔöÇÔöÇÔû║  fleet server  ÔöÇÔöÇHTTPÔöÇÔöÇÔû║  MCP FastAPI bridge  ÔöÇÔöÇÔû║  MCP tool
```

- **Tailscale** (free tier): zero port exposure, works on iOS, feels local
- **No new infra needed**: bridges are already running on fleet ports (10700ÔÇô11000)
- **Auth**: Tailscale node auth + optional API key header per server

---

## Top 3 ÔÇö Build These First

### 1. CalFolio (Calibre Companion) Ô¡É PRIORITY ONE ÔÇö IN PROGRESS

**Tag:** `ship-active` ÔÇö **highest promise** in this list (backend done, real user pain, fleet moat).

**Doc**: [CALFOLIO.md](./CALFOLIO.md) ┬À **EPUB**: [EPUB_READER.md](./EPUB_READER.md)  
**Fleet**: calibreops (port **10750** ÔÇö confirm in calibre-mcp before hard-coding)  
**Gap**: Calibre's mobile story is genuinely terrible. Large existing user base actively complaining.  
**What it does**: Beautiful iPad browser for your Calibre library ÔÇö browse by series/author/tag,
download EPUB for offline, sync reading progress, RAG ("what next?"), phase 2 Plex/Jellyfin links,
fleet TTS/translate for ad-hoc audiobooks.  
**Reader**: v1 hand-off (Open in Books/KyBook); alpha+ in-app via [Readium Swift Toolkit](https://github.com/readium/swift-toolkit) ÔÇö not FolioReaderKit.  
**Monetize**: One-time purchase $4.99  
**Notes**: calibreops backend is feature-complete; CalFolio is a frontend + iPad UX problem.

### 2. arXiv Reader with AI Annotations

**Tag:** `merge-calfolio` (ingest + summary + save to library) ÔÇö standalone `ship` only if PDF+Pencil becomes the whole product.

**Fleet**: arxiv-mcp, calibreops  
**Gap**: Researchers use iPad heavily; existing arXiv apps are all mediocre.  
**What it does**: Browse/search arXiv, AI summaries, Apple Pencil annotations, save to
Calibre library, link related papers via Semantic Scholar lineage.  
**Monetize**: Freemium ÔÇö 5 papers offline free, unlimited paid $2.99/mo or $14.99 one-time  

### 3. Fleet Health Dashboard

**Tag:** `ship` ÔÇö best **#2 app** after CalFolio; merge with legacy [Fleet Pulse](../../apple/projects/fleet-pulse.md) concept when scoping.

**Fleet**: glance-mcp, fileops (monitor tools), plexops, gitops  
**Gap**: iPad sysadmin panel for homelabbers ÔÇö MCP server status, Docker containers,
resource usage, logs, Plex activity. Dogfoodable from day one on own fleet.  
**Monetize**: One-time $4.99  
**Audience**: Homelabber/self-hoster community ÔÇö vocal, loyal, spread by word of mouth

---

## All 20 Ideas

### Strong Market / Fleet-Native

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `ship-active` | 1 | **CalFolio** | calibreops | $4.99 one-time | **Active** ÔÇö [CALFOLIO.md](./CALFOLIO.md); supersedes #4 |
| `merge-calfolio` | 2 | **arXiv Reader + AI** | arxiv-mcp, calibreops | ÔÇö | Paper ÔåÆ Calibre ÔåÆ read in CalFolio; donÔÇÖt rebuild PDF reader first |
| `ship` | 3 | **Fleet Health Dashboard** | glance-mcp, fileops, plexops | $4.99 one-time | Homelab audience; dogfood daily |
| `merge-calfolio` | 4 | ~~Smart E-Reader~~ | calibreops | ÔÇö | [EPUB_READER.md](./EPUB_READER.md) |
| `later` | 5 | **Plex/Jellyfin Unified Remote** | plexops, jellyfin-mcp, arr-mcp | $3.99 one-time | CalFolio phase 2 covers bookÔåömedia; full remote = separate bet |

### Interesting / Some Market

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 6 | **OCR Scanner ÔåÆ Calibre** | ocr-mcp, calibreops | ÔÇö | ÔÇ£Add by scanÔÇØ on book detail |
| `showcase-only` | 7 | **Voice Blender Remote** | blender-mcp, speechops | ÔÇö | Great demo, weak paid product |
| `skip` | 8 | **Personal AI with Memory** | advanced-memory-mcp | ÔÇö | Crowded; support burden |
| `skip` | 9 | **GitHub PR Dashboard** | git-github-mcp | ÔÇö | GitHub Mobile + Working Copy; narrow fleet hook |
| `showcase-only` | 10 | **Music Generation Sketchpad** | magentart-mcp, audiotool-nexus | ÔÇö | Press / portfolio |

### Fleet Showcase / Passion Projects

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 11 | **AI Research Notebook** | arxiv-mcp, calibreops | ÔÇö | Duplicate of #2 + CalFolio; one notebook later if ever |
| `merge-calfolio` | 12 | **Podcast / Audio Summariser** | speechops | ÔÇö | Optional ÔÇ£summariseÔÇØ action; not an app |
| `showcase-only` | 13 | **Worldlabs Spatial Viewer** | worldlabs-mcp | ÔÇö | 3D hedge; heavy, tiny TAM |
| `showcase-only` | 14 | **Image Generation Client** | HF mcp (RTX 4090) | ÔÇö | Personal fleet remote; App Store users lack your GPU |
| `skip` | 15 | **Inkscape Remote Tablet** | inkscape-mcp | ÔÇö | Latency + pen mapping + niche |

### Honest Long Shots

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 16 | **Reading Stats Tracker** | calibreops | ÔÇö | Stats tab in CalFolio |
| `skip` | 17 | **Local LLM Chat Client** | (Ollama on fleet) | ÔÇö | Saturated |
| `merge-fleet-health` | 18 | **DaVinci Render Monitor** | resolveops | ÔÇö | Optional card in Fleet Health; not standalone |
| `merge-fleet-health` | 19 | **Homelab Event Feed** | aiwatcher-mcp, plexops | ÔÇö | Timeline tab in Fleet Health |
| `later` | 20 | **Vienna Transit + Events** | mywienerlinien, vienna-live-mcp | ÔÇö | Personal/public only if you want to maintain OGD; [mywienerlinien](../mywienerlinien/) exists |

---

## Non-Obnoxious Monetisation Principles

- **One-time purchase** preferred for utility apps ÔÇö no dark patterns, no nag screens
- **Freemium** only with a hard, honest limit ÔÇö not artificially crippled
- **No ads** ÔÇö ever
- **Subscriptions** only where ongoing server costs justify it (AI inference credits)
- **Tip jar / "buy me a coffee"** in-app as optional for free showcase apps
- **Open core**: app free, fleet server config open-source ÔÇö monetise the polished client

---

## Tech Stack Notes

- **SwiftUI** ÔÇö iPad-optimised layouts (sidebar + detail, column navigation)
- **URLSession / async-await** ÔÇö fleet REST calls over Tailscale
- **SwiftData** ÔÇö local cache for offline metadata and reading `Locator` (CalFolio)
- **Readium Swift Toolkit** (SPM) ÔÇö in-app EPUB; see [EPUB_READER.md](./EPUB_READER.md)
- **Apple Pencil** ÔÇö Readium Decoration API (CalFolio); full annotation layer for arXiv reader
- **StoreKit 2** ÔÇö in-app purchase / one-time unlock
- **Tailscale** ÔÇö system VPN on iPad for v1; embedded SDK optional later

Generic Apple workflow (Xcode agentic, App Store): [`../../apple/README.md`](../../apple/README.md).

---

## Recommended build order

| Order | What | Tag |
|-------|------|-----|
| 1 | **CalFolio** | `ship-active` |
| 2 | **Fleet Health** (+ #19 timeline, optional #18 resolve card) | `ship` + `merge-fleet-health` |
| 3 | CalFolio phase 2 (Plex/Jellyfin, arXiv ingest, OCR, stats) | `merge-calfolio` |
| ÔÇö | Everything else | `showcase-only` / `skip` / `later` unless dogfood demands it |

---

## Next Steps (CalFolio)

1. Mac: scaffold repo per [IOS_PUBLISHING.md](./IOS_PUBLISHING.md); `AGENTS.md` / `CLAUDE.md`
2. PoC: calibreops REST ÔåÆ SwiftUI book grid over Tailscale (phase 1 in [CALFOLIO.md](./CALFOLIO.md))
3. Reader: download EPUB + hand-off; parallel ÔÇö build Readium **TestApp** on Mac ([EPUB_READER.md](./EPUB_READER.md))
4. Endpoint checklist: table in [CALFOLIO.md ┬º Fleet Integration](./CALFOLIO.md#fleet-integration-points)
5. App Store: naming (no ÔÇ£CalibreÔÇØ in consumer title); competitor scan before Connect setup

---

## Related

- [README.md](./README.md) ÔÇö `projects/apple/` hub
- [CALFOLIO.md](./CALFOLIO.md) ÔÇö product spec
- [EPUB_READER.md](./EPUB_READER.md) ÔÇö reader strategy
- [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) ÔÇö Xcode / TestFlight
- [calibre-mcp](../calibre-mcp/) ÔÇö backend project docs
- [apple/projects/README.md](../../apple/projects/README.md) ÔÇö legacy portfolio (VRMDance, Boomy, ÔÇª)

---
*Last updated: 2026-05-29*
