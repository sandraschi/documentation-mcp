# Apple app projects (fleet portfolio)

Monetizable iOS/macOS app ideas that **reuse sandraschi fleet work** — not generic App Store clones.

**Rules for this portfolio**

- Ship **working** features; no fake success paths or demo data sold as product.
- Monetization must be **StoreKit IAP/subscription** or honest paid app — document license boundaries (Hub, MMD, third-party APIs).
- Windows fleet (MCP servers) is **backend/dev**; the phone app talks to real APIs or on-device Apple frameworks.
- Revenue expectations are **modest unless noted** — these are “make a few bucks” + portfolio, not guaranteed income.

## Fleet iPad apps (separate folder)

New fleet-connected iPad specs live under **[projects/apple/](../../projects/apple/README.md)** — not in this index until shipped.

| Project | Doc | Status |
|---------|-----|--------|
| **CalFolio** (Calibre on iPad) | [CALFOLIO.md](../../projects/apple/CALFOLIO.md) · [EPUB reader](../../projects/apple/EPUB_READER.md) | Pre-scaffold — calibreops backend |

---

## How to pick a project

| If you want… | Start with |
|--------------|------------|
| **Calibre library on iPad (fleet)** | [CalFolio](../../projects/apple/CALFOLIO.md) |
| Proven consumer niche + creative fleet | [VRMDance](vrmdance.md) |
| **Raspbot / agentic robot remote** | **[Boomy Commander](boomy-commander.md)** |
| Fastest paid utility (1–2 weeks) | [Tapo Grid](tapo-grid.md) |
| Recurring sub from power users | [Fleet Pulse](fleet-pulse.md) |
| AI differentiation without cloud bills | [On-Device Study Coach](on-device-study-coach.md) |
| World Labs / 3D showcase | [Marble Pocket](marble-pocket.md) |
| Media library angle | [Shelf Remote](shelf-remote.md) |

## Portfolio index

| Project | Model | Effort | Fleet hook | Doc |
|---------|-------|--------|------------|-----|
| **VRMDance** | Free + IAP packs | High | avatar-mcp, Hub, MMD pipeline | [vrmdance.md](vrmdance.md) |
| **Boomy Commander** | Free + IAP (~$5) | Med | yahboom-mcp agent missions, swarm minuet | [boomy-commander.md](boomy-commander.md) |
| **Tapo Grid** | Paid or sub | Low–Med | Tapo RTSP, home cameras | [tapo-grid.md](tapo-grid.md) |
| **Fleet Pulse** | Sub ($2–5/mo) | Med | MCP health, Tailscale | [fleet-pulse.md](fleet-pulse.md) |
| **On-Device Study Coach** | Sub | Med | Foundation Models, JLPT angle | [on-device-study-coach.md](on-device-study-coach.md) |
| **Marble Pocket** | Free + IAP worlds | Med | worldlabs-mcp, GLB viewer | [marble-pocket.md](marble-pocket.md) |
| **Shelf Remote** | Paid / tip jar | Low | plex-mcp, jellyfin pattern | [shelf-remote.md](shelf-remote.md) |
| **Ring Glance** | Paid | Low | ring-mcp, WebRTC patterns | [ring-glance.md](ring-glance.md) |

## Active repo

| Repo | Project | Status |
|------|---------|--------|
| [apple-test](https://github.com/sandraschi/apple-test) | VRMDance | Phase 1 — Hub OAuth + stage |
| **boomy-commander** | [private repo](https://github.com/sandraschi/boomy-commander) | Boomy Commander | Phase 1 — REST client + free drive + IAP shell |

## Shared infrastructure

| Topic | Doc |
|-------|-----|
| Xcode 26 agentic workflow | [../development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md) |
| Install paths, IAP, commission | [../ios/DISTRIBUTION_AND_MONETIZATION.md](../ios/DISTRIBUTION_AND_MONETIZATION.md) |
| App Store submission | [../publishing/README.md](../publishing/README.md) |
| Factory-scale list (Vienna/robotics) | [../DARK_APP_FACTORY.md](../DARK_APP_FACTORY.md) |

## AI on iOS — what actually sells

Avoid “yet another ChatGPT wrapper” — Apple and users punish redundant cloud chat apps.

| Pattern | Works when… |
|---------|-------------|
| **On-device Foundation Models** | Task-specific: summarize *my* notes, drill flashcards, caption *my* photos — privacy as feature |
| **App Intents + Shortcuts** | Power users pay for deep automation ( Plex, Home, fleet triggers ) |
| **Cloud AI (your API key)** | Pro tier for heavy users who opt in; disclose data flow in App Privacy |
| **No AI in v1** | Camera grid, Plex remote, fleet status — ship utility first, add AI when it solves one job |

## Realistic revenue framing

| Tier | Expectation |
|------|-------------|
| **Utility ($2.99–9.99 one-time)** | Dozens–low hundreds of sales/month if ASO and niche fit |
| **Subscription ($2.99–6.99/mo)** | Needs retention loop (daily use, new content packs, cameras, study streaks) |
| **IAP content (dances, worlds, packs)** | Works for creative apps; needs catalog + updates |
| **VRMDance-class** | Top of portfolio effort; only project with direct “cottage industry” comps |

None of this replaces a salary. Goal: **first App Store payouts**, learning StoreKit + review, and apps that justify maintenance via fleet reuse.

---
*Last updated: 2026-05-28*
