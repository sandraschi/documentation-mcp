# Apple Ecosystem Documentation

## May 2026 situation

| Area | Status |
|------|--------|
| **Xcode 26.3** | **Agentic IDE** — Claude Agent + Codex in-IDE; build/test/fix loops; **Xcode ships an MCP server** (`xcrun mcpbridge`) for Cursor, Claude Code, Codex CLI |
| **Xcode 26** (2025) | Coding assistant, playground macro, multi-provider LLM (ChatGPT, Anthropic, local) |
| **Apple Intelligence** | **Foundation Models framework** — on-device LLM, tool calling, streaming (iOS, iPadOS, macOS, visionOS) |
| **Core ML → Core AI** | **Core AI** at **WWDC 2026** (June), targeting **iOS 27**+ ; generative AI / LLM focus |
| **Siri** | **Google Gemini** hybrid (iOS 26.4+, March 2026) — on-device simple tasks, cloud for complex |
| **iOS / macOS 26** | Current SDK generation paired with Xcode 26 |

**Dev is now agent-first on Mac** — comparable to Cursor + MCP on Windows. See [development/AGENTIC_XCODE_26.md](development/AGENTIC_XCODE_26.md).

### Developer-facing AI/ML (May 2026)

- **Foundation Models framework** – Swift API to on-device Apple Intelligence LLM
- **Xcode Intelligence** – In-editor and external agentic coding
- **Core ML** – Current on-device inference; **Core AI** supersedes for new gen-AI workloads at WWDC 2026
- **Create ML, Vision, NL, Speech, MLX** – Unchanged roles

---

## Overview

Apple platform guide for the sandraschi fleet: hardware, iOS/macOS targets, agentic Xcode workflows, and how they connect to fleet MCP servers on Windows.

## Apple and MCP (updated May 2026)

**Apple now ships MCP for Xcode** — Xcode 26.3+ exposes tools to external agents via `xcrun mcpbridge`. This is **complementary** to fleet FastMCP servers (avatar-mcp, blender-mcp, etc.), not a replacement.

| MCP surface | Role |
|-------------|------|
| **Xcode MCP** (`mcpbridge`) | Build/test/edit Swift, Apple doc search, Previews |
| **Fleet MCP** (Windows) | VRM pipeline, Blender, Godot, VRChat, etc. |

See [MCP_AND_APPLE.md](MCP_AND_APPLE.md).

## Path to mastery

- **[Fleet iPad apps (CalFolio)](../projects/apple/README.md)** – Calibre companion + `projects/apple/` specs (**active pre-scaffold**)
- **[Apple app projects](projects/README.md)** – Monetizable portfolio (VRMDance, **Boomy Commander**, Tapo Grid, …)
- **[Private iOS repos](development/PRIVATE_IOS_REPOS.md)** – **apple-test** + **boomy-commander** (private GitHub)
- **[Agentic Xcode 26+](development/AGENTIC_XCODE_26.md)** – **Start here** for May 2026 dev workflow
- **[iOS VRM dance app](ios/VRM_DANCE_APP.md)** – Doll Dancer–class native app (Swift, not godot-mcp)
- **[Hardware](hardware/README.md)** – Apple Silicon, agentic workload sizing
- **[iOS](ios/README.md)** – Mobile OS, App Intents, Foundation Models
- **[macOS](macos/README.md)** – Desktop, Metal/MPS, local LLMs
- **[Development](development/README.md)** – Swift, Xcode, frameworks index
- **[Publishing](publishing/README.md)** – App Store, TestFlight, privacy, StoreKit IAP
- **[iOS distribution & monetization](ios/DISTRIBUTION_AND_MONETIZATION.md)** – Install paths, marketplaces, IAP vs Hub vs itch
- **[Dark App Factory](DARK_APP_FACTORY.md)** – AI-only multi-app strategy
- **[MCP and Apple](MCP_AND_APPLE.md)** – Xcode MCP + fleet MCP together

## Fleet cross-links

| Topic | Doc |
|-------|-----|
| VRM / Hub / MMD | [docs/avatars/](../docs/avatars/README.md) |
| godot-mcp vs VRM | [docs/avatars/GODOT_VRM_MMD_DECISION.md](../docs/avatars/GODOT_VRM_MMD_DECISION.md) |
| Godot games on itch | [docs/gamedev/](../docs/gamedev/README.md) |
| Robotics / Raspbot | [docs/robotics/yahboom/](../docs/robotics/yahboom/README.md) |
| apple-test repo | [projects/FLEET_INDEX.md](../projects/FLEET_INDEX.md) |

## References (May 2026)

- [Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode)
- [Xcode 26.3 agentic coding (Newsroom)](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)
- [Meet agentic coding in Xcode (Video)](https://developer.apple.com/videos/play/tech-talks/111428/)
- [Foundation Models (WWDC25)](https://developer.apple.com/videos/play/wwdc2025/286/)
- [What's new in Xcode 26 (WWDC25)](https://developer.apple.com/videos/play/wwdc2025/247/)

---
*Last updated: 2026-05-28*
