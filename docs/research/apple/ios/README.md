# iOS and iPadOS: Mobile development (May 2026)

## Platform context

| Release | Notes |
|---------|-------|
| **iOS 26** | SDK generation for Xcode 26 |
| **iOS 26.4** (Mar 2026) | Siri + Google Gemini hybrid |
| **iOS 27** | Expected WWDC 2026 — Core AI framework |

## Agentic development (primary change)

iOS app development is **no longer Xcode-click heavy** for greenfield work:

1. **Xcode 26.3** with Claude Agent or Codex — in-IDE agentic loop  
2. **External agents** via `xcrun mcpbridge` (Cursor, Claude Code on Mac)  
3. **`AGENTS.md`** — project context both agents read  

Full guide: [development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md)

Comparable to **Cursor + MCP on Windows** for fleet Python repos.

## Fleet use case: VRM dance / MV apps

Native Swift apps (Doll Dancer class) — **not godot-mcp**:

- [VRM_DANCE_APP.md](./VRM_DANCE_APP.md)  
- [docs/avatars/MMD_EXPLAINER.md](../../docs/avatars/MMD_EXPLAINER.md)  

avatar-mcp on Windows stages VRM; Mac agent integrates into Xcode project.

## App integration APIs (shipped apps)

| API | Use |
|-----|-----|
| **App Intents** | Siri, Shortcuts, Spotlight, widgets |
| **Foundation Models** | On-device AI features inside app |
| **Apple Intelligence** | System features + developer framework |

MCP is **not** embedded in App Store apps — dev-time only via Xcode.

## Distribution quick reference

| Path | Need |
|------|------|
| **Simulator** | Free — Xcode only |
| **TestFlight / App Store** | Apple Developer Program ($99/yr) |
| **Web toy (no native)** | itch.io HTML — see [gamedev](../../docs/gamedev/README.md) |

Full matrix (IAP, commissions, TestFlight internal/external): **[DISTRIBUTION_AND_MONETIZATION.md](./DISTRIBUTION_AND_MONETIZATION.md)**

Windows cannot code-sign iOS — Mac or Mac CI required for store builds.

## iPadOS / visionOS

Same Xcode 26 agentic workflow; adjust UI for form factor / spatial layout in prompts.

---
*Last updated: 2026-05-28*
