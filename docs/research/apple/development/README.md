# Apple development: Xcode 26+, Swift, and AI frameworks

## May 2026 context

**Xcode 26.3 is an agentic IDE** — not a future concept. Development workflow matches Cursor on Windows: describe intent, agent edits/builds/tests.

| Component | Status |
|-----------|--------|
| **Xcode 26.3** | GA — Claude Agent, Codex, MCP server for external agents |
| **Xcode 26** | Coding assistant, LLM providers, playground macro |
| **Swift 6** | Current language; strict concurrency default |
| **Foundation Models** | On-device Apple Intelligence from Swift |
| **Core ML** | Current inference framework |
| **Core AI** | WWDC 2026 (June) — iOS 27+ generative AI successor |

**Primary doc:** [AGENTIC_XCODE_26.md](./AGENTIC_XCODE_26.md)

## Quick start (agentic)

1. Install **Xcode 26.3+** from Mac App Store  
2. **Xcode → Settings → Intelligence** — enable Claude Agent or Codex  
3. Optional: `claude mcp add --transport stdio xcode -- xcrun mcpbridge` for external client  
4. Add **`AGENTS.md`** to repo root with platform targets and architecture notes  
5. Open project in Xcode; prompt agent  

## Swift

- **Swift 6** — actors, Sendable, strict concurrency  
- **SwiftUI** — default for new iOS/macOS UI  
- **Swift Package Manager** — VRM/glTF libraries as SPM deps (agent-addable)

## AI/ML frameworks

| Framework | Role |
|-----------|------|
| **Foundation Models** | On-device LLM in **your app** (not the IDE agent) |
| **Core ML** | Deploy converted models |
| **Core AI** | Planned WWDC 2026 |
| **Create ML** | Train on Mac |
| **Vision / NL / Speech** | System perception |
| **MLX** | Research / Python ML on Apple Silicon |

## Xcode Intelligence vs Foundation Models

| | Xcode Intelligence | Foundation Models |
|---|-------------------|-------------------|
| **Runs in** | IDE (dev time) | Shipped app (runtime) |
| **Use** | Write/fix Swift, build, test | User-facing AI features in app |
| **Agent** | Claude, Codex, ChatGPT | Apple on-device model |

## Build and test

- **XCTest / XCUITest** — agent can run and fix failing tests  
- **Xcode Previews** — agent captures for SwiftUI iteration  
- **TestFlight** — archive via agent-guided workflow + App Store Connect  

## Fleet + Apple projects

For VRM/dance iOS apps, read:

- [ios/VRM_DANCE_APP.md](../ios/VRM_DANCE_APP.md)  
- [docs/avatars/FLEET_VRM_PIPELINE.md](../../docs/avatars/FLEET_VRM_PIPELINE.md)  

For Godot games (not VRM App Store apps):

- [docs/avatars/GODOT_VRM_MMD_DECISION.md](../../docs/avatars/GODOT_VRM_MMD_DECISION.md)  

## References

- [AGENTIC_XCODE_26.md](./AGENTIC_XCODE_26.md)  
- [Apple Machine Learning & AI](https://developer.apple.com/machine-learning/)  
- [Setting up coding intelligence](https://developer.apple.com/documentation/xcode/setting-up-coding-intelligence)  

---
*Last updated: 2026-05-28*
