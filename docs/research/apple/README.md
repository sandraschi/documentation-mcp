# Apple Ecosystem Documentation

## October 2026 situation (current: iOS/iPadOS 27.2, macOS Golden Gate 27.2, Xcode 27.2)

| Area | Status |
|------|--------|
| **iOS / iPadOS 27.2** (26 Oct 2026) | Current stable. More Siri AI languages, Messages/Podcasts changes, Apple Music refresh, Apple Pencil support on iPhone Duo |
| **macOS Golden Gate 27.2** | Current stable. **Apple-silicon-only** (Tahoe 26 was the last Intel release); **last version with full Rosetta 2** |
| **Xcode 27.2** | Bundled 27.2 SDKs. **Agentic IDE standing alongside Cursor / Claude Code** in 2026 tool comparisons -- in-IDE agents + `xcrun mcpbridge` MCP server for external agents |
| **Xcode 26.3** (Feb 2026) | Where agentic coding landed (Claude Agent + Codex in-IDE, MCP server) -- superseded by 27.x, mechanism unchanged |
| **Apple Intelligence** | **Foundation Models framework** -- on-device LLM, tool calling, streaming (iOS, iPadOS, macOS, visionOS). **Core AI** framework shipped with the 27 generation for new gen-AI workloads |
| **Siri** | Apple Intelligence-powered (Siri AI), expanded language coverage in 27.2; Gemini-hybrid era over |

**Dev is agent-first on Mac** -- Xcode 27 reviews as a peer of Cursor + MCP, not a laggard. See [development/AGENTIC_XCODE_26.md](development/AGENTIC_XCODE_26.md).

### Developer-facing AI/ML (October 2026)

- **Foundation Models framework** - Swift API to on-device Apple Intelligence LLM
- **Core AI** - Shipped with the 27 generation; use for new gen-AI workloads (supersedes Core ML there)
- **Core ML, Create ML, Vision, NL, Speech, MLX** - Unchanged roles for classic ML
- **Xcode Intelligence** - In-editor and external agentic coding (see below)

### Limiting Apple Intelligence per app / feature

iOS 27 has **no single global kill-switch** (deeply integrated), but Apple documents layered opt-out -- relevant for fleet iPad apps (CalFolio) and any device where AI must stay off:

- **Master toggle:** Settings > Apple Intelligence & Siri -> Apple Intelligence **off** (iPhone, iPad, Mac)
- **Per feature:** Siri AI, summarization, and similar features toggle individually (same screen)
- **Per app surface:** individual apps expose their own AI switches, e.g. Settings > Apps > Phone -> Suggestions in Voicemail **off**
- **Enforced restriction:** Screen Time > Content & Privacy Restrictions can **block** Siri / Apple Intelligence features (device-level, incl. parental/MDM control)

Official: [restrict on iPhone](https://support.apple.com/guide/iphone/turn-restrict-access-apple-intelligence-iph3fed3f2c3/ios) | [restrict on Mac](https://support.apple.com/guide/mac-help/turn-restrict-access-apple-intelligence-mchlb2e44f94/mac).

---

## Overview

Apple platform guide for the sandraschi fleet: hardware, iOS/macOS targets, agentic Xcode workflows, and how they connect to fleet MCP servers on Windows.

## Apple and MCP (updated October 2026)

**Apple ships MCP for Xcode** -- Xcode 26.3+ (current 27.2) exposes tools to external agents via `xcrun mcpbridge`. This is **complementary** to fleet FastMCP servers (avatar-mcp, blender-mcp, etc.), not a replacement.

| MCP surface | Role |
|-------------|------|
| **Xcode MCP** (`mcpbridge`) | Build/test/edit Swift, Apple doc search, Previews |
| **Fleet MCP** (Windows) | VRM pipeline, Blender, Godot, VRChat, etc. |

See [MCP_AND_APPLE.md](MCP_AND_APPLE.md).

## Path to mastery

- **[Fleet iPad apps (CalFolio)](../../projects/apple/README.md)** - Calibre companion + `projects/apple/` specs (**active pre-scaffold**)
- **[Apple app projects](projects/README.md)** - Monetizable portfolio (VRMDance, **Boomy Commander**, Tapo Grid, ...)
- **[Private iOS repos](development/PRIVATE_IOS_REPOS.md)** - **apple-test** + **boomy-commander** (private GitHub)
- **[Agentic Xcode 26-27](development/AGENTIC_XCODE_26.md)** - **Start here** for the Xcode 27 workflow
- **[iOS VRM dance app](ios/VRM_DANCE_APP.md)** - Doll Dancer-class native app (Swift, not godot-mcp)
- **[Hardware](hardware/README.md)** - Apple Silicon, agentic workload sizing
- **[iOS](ios/README.md)** - Mobile OS, App Intents, Foundation Models
- **[macOS](macos/README.md)** - Desktop, Metal/MPS, local LLMs
- **[Development](development/README.md)** - Swift, Xcode, frameworks index
- **[Publishing](publishing/README.md)** - App Store, TestFlight, privacy, StoreKit IAP
- **[iOS distribution & monetization](ios/DISTRIBUTION_AND_MONETIZATION.md)** - Install paths, marketplaces, IAP vs Hub vs itch
- **[Dark App Factory](DARK_APP_FACTORY.md)** - AI-only multi-app strategy
- **[MCP and Apple](MCP_AND_APPLE.md)** - Xcode MCP + fleet MCP together

## Fleet cross-links

| Topic | Doc |
|-------|-----|
| VRM / Hub / MMD | [docs/avatars/](../../docs/avatars/README.md) |
| godot-mcp vs VRM | [docs/avatars/GODOT_VRM_MMD_DECISION.md](../../docs/avatars/GODOT_VRM_MMD_DECISION.md) |
| Godot games on itch | [docs/gamedev/](../../docs/gamedev/README.md) |
| Robotics / Raspbot | [docs/robotics/yahboom/](../../docs/robotics/yahboom/README.md) |
| apple-test repo | [projects/FLEET_INDEX.md](../../projects/FLEET_INDEX.md) |

## References

- [Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode)
- [Xcode 26.3 agentic coding (Newsroom)](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)
- [Meet agentic coding in Xcode (Video)](https://developer.apple.com/videos/play/tech-talks/111428/)
- [Foundation Models (WWDC25)](https://developer.apple.com/videos/play/wwdc2025/286/)
- [What's new in Xcode 26 (WWDC25)](https://developer.apple.com/videos/play/wwdc2025/247/)
- [Reversing an iPhone app (Oct 2026 field guide)](../2026-10-28-ios-reverse-engineering.md) -- decrypted IPA routes, proxy-first cloning, screenshots + scripted taps without jailbreak

---
*Last updated: 2026-10-28 (27.2 generation; May 2026 snapshot superseded)*
