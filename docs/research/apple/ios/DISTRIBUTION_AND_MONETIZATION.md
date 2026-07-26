# iOS distribution and monetization (May 2026)

Fleet reference for **how apps get onto iPhones** and **how they make money**. Separate from dev setup ([development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md)) and VRM app architecture ([VRM_DANCE_APP.md](./VRM_DANCE_APP.md)).

---

## Install paths (how software reaches an iPhone)

| Path | Cost | Audience | Signing | Notes |
|------|------|----------|---------|-------|
| **App Store** | $99/yr Developer Program | Public | Apple distribution cert | Review 24–48h typical; updates same pipeline |
| **TestFlight internal** | $99/yr | Up to 100 team members | Same | No Beta App Review for internal testers |
| **TestFlight external** | $99/yr | Up to 10,000 testers | Same | Requires **Beta App Review** first build |
| **Developer install (Xcode)** | Free Apple ID or $99/yr | Self | 7-day (free) or 1-yr (paid team) | Simulator needs no cert; device needs trust |
| **Web (itch.io HTML)** | Free | Anyone with link | None | Safari; Add to Home Screen — **not** App Store |
| **Godot iOS export → App Store** | Mac + $99/yr | Public | Same as native | Possible for **games**; poor fit for Hub/VRM dance UX |
| **EU alternative marketplaces** | Varies (DMA) | EU users only | Notarized + marketplace rules | Optional; extra compliance — fleet default is still App Store |

**Windows cannot produce signed iOS IPAs.** Mac (or Mac CI: Xcode Cloud, GitHub Actions macOS runner) required for store builds.

### Recommended progression (fleet)

```text
Simulator (Xcode) → TestFlight internal → TestFlight external → App Store
```

Mac setup: `D:/Dev/repos/apple-test/docs/SETUP_MAC.md`

---

## Marketplaces — which store for what

| Marketplace | Best for | iOS native? | Fleet doc |
|-------------|----------|-------------|-----------|
| **Apple App Store** | VRM dance apps, utilities, games | Yes | This doc + [publishing/README.md](../publishing/README.md) |
| **TestFlight** | Beta before IAP tuning | Yes | Phase 7 in SETUP_MAC |
| **itch.io (web export)** | Godot toys, jam games | Browser only | [docs/gamedev/ITCH_IO_GUIDE.md](../../docs/gamedev/ITCH_IO_GUIDE.md) |
| **Steam** | PC games | **No iPhone** | [STEAM_PUBLISHING.md](../../docs/gamedev/STEAM_PUBLISHING.md) |
| **VRoid Hub** | **Avatar content**, not app distribution | N/A (OAuth in your app) | [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md) |
| **Booth / Gumroad** | Paid VRM models, dances (files) | N/A | Import via avatar-mcp `hub_stage_file` |

Do not confuse **content marketplaces** (Hub, Booth) with **app marketplaces** (App Store).

---

## Monetization models (May 2026)

### App Store — Apple mechanisms

| Model | Apple API | Typical use | Apple cut |
|-------|-----------|-------------|-----------|
| **Free** | — | Hub-connected dance app with IAP upsell | — |
| **Paid app** | App Store price tier | Rare for dance/MV niche | 15% or 30% |
| **Consumable IAP** | StoreKit 2 | Extra dance packs, one-time character unlocks | 15% or 30% |
| **Non-consumable IAP** | StoreKit 2 | Permanent character/skin unlock | 15% or 30% |
| **Auto-renewable subscription** | StoreKit 2 | Monthly “dance club”, cloud storage | 15% or 30% |
| **Ads (AdMob etc.)** | Third-party SDK | Usually **not** used in Doll Dancer class | N/A to Apple |

**Commission:** **30%** default; **15%** if enrolled in [Small Business Program](https://developer.apple.com/app-store/small-business-program/) (≤ $1M prior-year proceeds). Subscriptions: 15% after year 1 for eligible developers.

Configure products in **App Store Connect → Your App → In-App Purchases** before coding StoreKit.

### VRM / dance app reference (Doll Dancer class)

Observed industry pattern (not legal advice):

| Layer | Monetization |
|-------|----------------|
| App download | Free |
| Extra dances / characters | **Consumable or non-consumable IAP** |
| VRoid Hub avatars | Free or creator-gated per Hub license — **not** a Hub-wide subscription |
| User-created exports (MP4) | Often free (marketing loop) |

**License separation:** IAP sells **your** bundled content. Hub models carry **per-creator** VRM license flags (`commercialUssageName`, etc.). Do not sell redistribution of Hub models without creator terms.

See [MMD_EXPLAINER.md](../../docs/avatars/MMD_EXPLAINER.md) for MMD/VMD licensing caution.

### itch.io / web (iPhone)

| Model | How |
|-------|-----|
| Free | Default for HTML5 Godot export |
| Pay what you want | itch.io project pricing — user pays on web, plays in Safari |
| No native IAP | itch is not App Store — no StoreKit |

---

## App Store submission checklist (monetization-aware)

- [ ] Apple Developer Program active ($99/yr)
- [ ] App Store Connect app record + bundle ID
- [ ] **Privacy manifest** (`PrivacyInfo.xcprivacy`) if required APIs used
- [ ] **App Privacy** questionnaire (data linked to user, Hub OAuth tokens, analytics)
- [ ] **IAP products** created in Connect **before** StoreKit code ships
- [ ] **Review notes** explaining VRoid Hub login (reviewer test account if needed)
- [ ] Export compliance / encryption (HTTPS-only often qualifies for exemption)
- [ ] AI disclosure if app calls non-Apple cloud LLMs ([publishing/README.md](../publishing/README.md))
- [ ] Screenshots + age rating (dance apps often 4+ or 9+ depending on content)

---

## What is intentionally out of scope

- Full **Fastlane** / **Xcode Cloud** recipes (see DARK_APP_FACTORY for factory vision)
- **Google Play** (Android) — separate track
- Tax / VAT / entity setup — consult accountant
- Legal review of third-party avatar licenses

---

## Related docs

| Doc | Topic |
|-----|-------|
| [publishing/README.md](../publishing/README.md) | Privacy, AI disclosure, review guidelines |
| [VRM_DANCE_APP.md](./VRM_DANCE_APP.md) | Product architecture |
| [development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md) | Xcode 26.3 + MCP |
| [docs/gamedev/README.md](../../docs/gamedev/README.md) | itch.io + Steam (games, not Hub apps) |
| [apple-test/docs/SETUP_MAC.md](file:///D:/Dev/repos/apple-test/docs/SETUP_MAC.md) | Mac onboarding |

---
*Last updated: 2026-05-28*
