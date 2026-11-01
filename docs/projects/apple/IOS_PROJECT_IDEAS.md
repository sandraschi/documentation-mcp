# iOS Project Ideas -- Fleet-Connected iPad Apps

**Private -- Sandra S. + collaborators only. Not for public distribution.**

**Status**: IDEATION
**Date**: 2026-05-29 (reaffirmed 2026-10-28)
**Context**: Fleet of 233 `*-mcp` servers on Ryzen 9 5900X (12C/24T) / RTX 4090 24GB / 64GB.
iPad apps connect via Tailscale + FastAPI HTTP bridges already exposed by every fleet MCP.

**Active build:** **[CalFolio](./CALFOLIO.md)** (was "Calibre Companion" below) -- first Apple dev on Mac.  
**Hub:** [README.md](./README.md) | **Reader:** [EPUB_READER.md](./EPUB_READER.md) | **Publish:** [IOS_PUBLISHING.md](./IOS_PUBLISHING.md)

### Roadmap tags

| Tag | Meaning |
|-----|---------|
| **`ship`** | Standalone App Store app -- worth a repo and maintenance |
| **`ship-active`** | Shipping now (CalFolio) |
| **`merge-calfolio`** | Feature inside CalFolio, not a separate app |
| **`merge-fleet-health`** | Feature inside Fleet Health (#2 app), not separate |
| **`later`** | Possible second/third app after CalFolio + Fleet Health prove the pattern |
| **`showcase-only`** | Demo, video, or personal use -- no product commitment |
| **`skip`** | Do not build; crowded, tiny TAM, or duplicate |

---

## Connectivity Pattern

Every fleet MCP exposes a FastAPI REST bridge alongside its stdio MCP transport:

```
iPad app  --Tailscale-->  fleet server  --HTTP-->  MCP FastAPI bridge  -->  MCP tool
```

- **Tailscale** (free tier): zero port exposure, works on iOS, feels local
- **No new infra needed**: bridges are already running on fleet ports (10700-15000 reservoir)
- **Auth**: Tailscale node auth + optional API key header per server

---

## Top 3 -- Build These First

### 1. CalFolio (Calibre Companion) * PRIORITY ONE -- PRE-SCAFFOLD (backend done, app not started)

**Tag:** `ship-active` -- **highest promise** in this list (backend done, real user pain, fleet moat).

**Doc**: [CALFOLIO.md](./CALFOLIO.md) | **EPUB**: [EPUB_READER.md](./EPUB_READER.md)  
**Fleet**: calibreops (ports **10720/10721** per `operations/WEBAPP_PORTS.md` -- re-check in calibre-mcp before hard-coding)
**Gap**: Calibre's mobile story is genuinely terrible. Large existing user base actively complaining.  
**What it does**: Beautiful iPad browser for your Calibre library -- browse by series/author/tag,
download EPUB for offline, sync reading progress, RAG ("what next?"), phase 2 Plex/Jellyfin links,
fleet TTS/translate for ad-hoc audiobooks.  
**Reader**: v1 hand-off (Open in Books/KyBook); alpha+ in-app via [Readium Swift Toolkit](https://github.com/readium/swift-toolkit) -- not FolioReaderKit.  
**Monetize**: One-time purchase $4.99  
**Notes**: calibreops backend is feature-complete; CalFolio is a frontend + iPad UX problem.

### 2. arXiv Reader with AI Annotations

**Tag:** `merge-calfolio` (ingest + summary + save to library) -- standalone `ship` only if PDF+Pencil becomes the whole product.

**Fleet**: arxiv-mcp, calibreops  
**Gap**: Researchers use iPad heavily; existing arXiv apps are all mediocre.  
**What it does**: Browse/search arXiv, AI summaries, Apple Pencil annotations, save to
Calibre library, link related papers via Semantic Scholar lineage.  
**Monetize**: Freemium -- 5 papers offline free, unlimited paid $2.99/mo or $14.99 one-time  

### 3. Fleet Health Dashboard

**Tag:** `ship` -- best **#2 app** after CalFolio; merge with [Fleet Pulse](../../research/apple/projects/fleet-pulse.md) concept when scoping.

**Fleet**: glance-mcp, fileops (monitor tools), plexops, gitops  
**Gap**: iPad sysadmin panel for homelabbers -- MCP server status, Docker containers,
resource usage, logs, Plex activity. Dogfoodable from day one on own fleet.  
**Monetize**: One-time $4.99  
**Audience**: Homelabber/self-hoster community -- vocal, loyal, spread by word of mouth

---

## All 20 Ideas

### Strong Market / Fleet-Native

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `ship-active` | 1 | **CalFolio** | calibreops | $4.99 one-time | **Active** -- [CALFOLIO.md](./CALFOLIO.md); supersedes #4 |
| `merge-calfolio` | 2 | **arXiv Reader + AI** | arxiv-mcp, calibreops | -- | Paper -> Calibre -> read in CalFolio; don't rebuild PDF reader first |
| `ship` | 3 | **Fleet Health Dashboard** | glance-mcp, fileops, plexops | $4.99 one-time | Homelab audience; dogfood daily |
| `merge-calfolio` | 4 | ~~Smart E-Reader~~ | calibreops | -- | [EPUB_READER.md](./EPUB_READER.md) |
| `later` | 5 | **Plex/Jellyfin Unified Remote** | plexops, jellyfin-mcp, arr-mcp | $3.99 one-time | CalFolio phase 2 covers book<->media; full remote = separate bet |

### Interesting / Some Market

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 6 | **OCR Scanner -> Calibre** | ocr-mcp, calibreops | -- | "Add by scan" on book detail |
| `showcase-only` | 7 | **Voice Blender Remote** | blender-mcp, speechops | -- | Great demo, weak paid product |
| `skip` | 8 | **Personal AI with Memory** | advanced-memory-mcp | -- | Crowded; support burden |
| `skip` | 9 | **GitHub PR Dashboard** | git-github-mcp | -- | GitHub Mobile + Working Copy; narrow fleet hook |
| `showcase-only` | 10 | **Music Generation Sketchpad** | magentart-mcp, audiotool-nexus | -- | Press / portfolio |

### Fleet Showcase / Passion Projects

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 11 | **AI Research Notebook** | arxiv-mcp, calibreops | -- | Duplicate of #2 + CalFolio; one notebook later if ever |
| `merge-calfolio` | 12 | **Podcast / Audio Summariser** | speechops | -- | Optional "summarise" action; not an app |
| `showcase-only` | 13 | **Worldlabs Spatial Viewer** | worldlabs-mcp | -- | 3D hedge; heavy, tiny TAM |
| `showcase-only` | 14 | **Image Generation Client** | HF mcp (RTX 4090) | -- | Personal fleet remote; App Store users lack your GPU |
| `skip` | 15 | **Inkscape Remote Tablet** | inkscape-mcp | -- | Latency + pen mapping + niche |

### Honest Long Shots

| Tag | # | App | Fleet MCPs | Monetize | Notes |
|-----|---|-----|-----------|---------|-------|
| `merge-calfolio` | 16 | **Reading Stats Tracker** | calibreops | -- | Stats tab in CalFolio |
| `skip` | 17 | **Local LLM Chat Client** | (Ollama on fleet) | -- | Saturated |
| `merge-fleet-health` | 18 | **DaVinci Render Monitor** | resolveops | -- | Optional card in Fleet Health; not standalone |
| `merge-fleet-health` | 19 | **Homelab Event Feed** | aiwatcher-mcp, plexops | -- | Timeline tab in Fleet Health |
| `later` | 20 | **Vienna Transit + Events** | publictransport-mcp, vienna-live-mcp | -- | Personal/public only if you want to maintain OGD; [publictransport-mcp](../publictransport-mcp/) exists |

---

## Non-Obnoxious Monetisation Principles

- **One-time purchase** preferred for utility apps -- no dark patterns, no nag screens
- **Freemium** only with a hard, honest limit -- not artificially crippled
- **No ads** -- ever
- **Subscriptions** only where ongoing server costs justify it (AI inference credits)
- **Tip jar / "buy me a coffee"** in-app as optional for free showcase apps
- **Open core**: app free, fleet server config open-source -- monetise the polished client

---

## Tech Stack Notes

- **SwiftUI** -- iPad-optimised layouts (sidebar + detail, column navigation)
- **URLSession / async-await** -- fleet REST calls over Tailscale
- **SwiftData** -- local cache for offline metadata and reading `Locator` (CalFolio)
- **Readium Swift Toolkit** (SPM) -- in-app EPUB; see [EPUB_READER.md](./EPUB_READER.md)
- **Apple Pencil** -- Readium Decoration API (CalFolio); full annotation layer for arXiv reader
- **StoreKit 2** -- in-app purchase / one-time unlock
- **Tailscale** -- system VPN on iPad for v1; embedded SDK optional later

Generic Apple workflow (Xcode agentic, App Store): [`research/apple/README.md`](../../research/apple/README.md).

---

## Recommended build order

| Order | What | Tag |
|-------|------|-----|
| 1 | **CalFolio** | `ship-active` |
| 2 | **Fleet Health** (+ #19 timeline, optional #18 resolve card) | `ship` + `merge-fleet-health` |
| 3 | CalFolio phase 2 (Plex/Jellyfin, arXiv ingest, OCR, stats) | `merge-calfolio` |
| -- | Everything else | `showcase-only` / `skip` / `later` unless dogfood demands it |

---

## Next Steps (CalFolio)

1. Mac: scaffold repo per [IOS_PUBLISHING.md](./IOS_PUBLISHING.md); `AGENTS.md` / `CLAUDE.md`
2. PoC: calibreops REST -> SwiftUI book grid over Tailscale (phase 1 in [CALFOLIO.md](./CALFOLIO.md))
3. Reader: download EPUB + hand-off; parallel -- build Readium **TestApp** on Mac ([EPUB_READER.md](./EPUB_READER.md))
4. Endpoint checklist: table in [CALFOLIO.md section Fleet Integration](./CALFOLIO.md#fleet-integration-points)
5. App Store: naming (no "Calibre" in consumer title); competitor scan before Connect setup

---

## Related

- [README.md](./README.md) -- `projects/apple/` hub
- [CALFOLIO.md](./CALFOLIO.md) -- product spec
- [EPUB_READER.md](./EPUB_READER.md) -- reader strategy
- [IOS_PUBLISHING.md](./IOS_PUBLISHING.md) -- Xcode / TestFlight
- [calibre-mcp](../calibre-mcp/) -- backend project docs
- [research/apple/projects/README.md](../../research/apple/projects/README.md) -- portfolio (VRMDance, Boomy, ...)

---
*Last updated: 2026-10-28 (ASCII cleanup, ports 10720/10721, honest pre-scaffold status, fixed research/apple links). Ideas list from 2026-05-29.*
