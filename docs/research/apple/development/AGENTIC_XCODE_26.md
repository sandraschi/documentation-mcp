# Agentic Xcode 26+ (May 2026)

Apple platform development is now **agent-first**, comparable to Cursor on Windows for fleet workflows.

## May 2026 situation

| Release | What changed |
|---------|----------------|
| **Xcode 26** (WWDC 2025) | Built-in coding assistant (ChatGPT, Anthropic, local models); playground macro; project-wide context |
| **Xcode 26.3** (Feb 2026 GA) | **Agentic coding**: Claude Agent + Codex in-IDE; multi-step build/test/fix loops; **Xcode as MCP server** |
| **iOS 26 / macOS 26** | Platform SDKs aligned with Xcode 26 generation |
| **iOS 26.4** (Mar 2026) | Siri + Google Gemini hybrid rollout |

**Bottom line:** You describe intent; agents navigate the project, search Apple docs, edit Swift, run builds, capture Previews, and iterate — same mental model as Cursor + MCP on Windows.

## Xcode MCP server (official)

Xcode exposes tools via **Model Context Protocol**. External agents (Cursor, Claude Code, Codex CLI) connect to the **open Xcode project**.

### Enable

1. Open project in **Xcode 26.3+**
2. **Xcode → Settings → Intelligence**
3. Turn on **Allow external agents to use Xcode tools** (under Model Context Protocol)

### Connect from terminal

```bash
# Claude Code
claude mcp add --transport stdio xcode -- xcrun mcpbridge

# OpenAI Codex
codex mcp add xcode -- xcrun mcpbridge
```

Verify: `claude mcp list` or `codex mcp list`

**Requirement:** Project must be **open in Xcode** while the external agent runs.

### What agents can do via Xcode tools

- Explore file tree and project settings
- Search **Apple Developer Documentation** (current APIs)
- Edit Swift / SwiftUI sources
- Build and run tests
- Capture **Xcode Previews** for visual verification
- Fix compile errors in a loop

Official doc: [Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode)

Apple Newsroom: [Xcode 26.3 unlocks agentic coding](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/)

Video: [Meet agentic coding in Xcode](https://developer.apple.com/videos/play/tech-talks/111428/)

## In-IDE agents (no external client)

Xcode 26.3 also bundles one-click **Claude Agent** and **Codex** downloads inside Intelligence settings — same agentic loop without leaving Xcode.

## Fleet workflow: Windows + Mac

| Task | Where |
|------|-------|
| MCP fleet servers (avatar-mcp, blender-mcp, godot-mcp) | Windows RTX box (primary) |
| iOS / macOS app target | Mac with Xcode 26.3 |
| Cross-IDE agent | Cursor on Windows **or** Claude Code with `xcrun mcpbridge` on Mac |
| VRM pipeline staging | avatar-mcp `:10793` — agent pulls staged VRM paths into Xcode project |

Typical loop for a **Doll Dancer–style iOS app**:

1. avatar-mcp `hub_download` → staged VRM on disk  
2. Mac: open Xcode project; agent adds VRM loader (Swift + GLTF/VRM library)  
3. Agent implements VMD player or baked clip playback  
4. Agent runs on Simulator + Preview until dance loop works  
5. TestFlight via App Store Connect  

No manual storyboard wiring for boilerplate — agent handles file adds, SPM packages, and build settings.

## Swift stack for VRM dance apps (not godot-mcp)

Native iOS apps in this category use:

| Layer | Typical choice |
|-------|----------------|
| VRM load/render | [three-vrm](https://github.com/pixiv/three-vrm) port, SceneKit, or Metal + glTF parser |
| Hub OAuth | VRoid Hub API (same as avatar-mcp `hub_client.py` flow, Swift port) |
| VMD motion | Custom retarget or bake from Blender; PMX/VMD parsers exist in Swift/C++ ports |
| UI | SwiftUI |
| Export | AVFoundation video composition |

**godot-mcp is for Godot games**, not App Store VRM MV editors. See [docs/avatars/GODOT_VRM_MMD_DECISION.md](../../docs/avatars/GODOT_VRM_MMD_DECISION.md).

## Minimal new-project checklist (agent-driven)

- [ ] Apple Developer Program ($99/yr) for TestFlight / App Store  
- [ ] Xcode 26.3+, iOS 26 SDK  
- [ ] Intelligence settings: pick Claude or Codex agent  
- [ ] `AGENTS.md` in repo root (Xcode + Cursor read this)  
- [ ] Privacy manifest if using Hub OAuth or analytics  
- [ ] VRoid Hub OAuth app (redirect URI for iOS custom scheme or universal link)

## AGENTS.md snippet (iOS VRM app)

```markdown
# iOS VRM Dance App

- Xcode 26.3+, Swift 6, SwiftUI, iOS 26 deployment target
- Load VRM from VRoid Hub OAuth; cache under Application Support
- Motion: VMD retarget to humanoid skeleton OR baked .usdz clips from blender-mcp
- Reference fleet docs: mcp-central-docs/docs/avatars/
- Staging VRM path (dev): ~/.avatarmcp/pipeline/staging/
```

## What is still not trivial

- App Store review + privacy disclosures for Hub/third-party AI  
- VMD retarget quality (bone naming mismatches)  
- Performance on older iPhones (draw calls, spring bones)  
- **Windows-only** machine cannot code-sign iOS builds — still need a Mac (or Mac cloud) for signing  

Agentic IDE removes **typing boilerplate**, not Apple’s signing/hardware requirements.

## References

- [Setting up coding intelligence in Xcode](https://developer.apple.com/documentation/xcode/setting-up-coding-intelligence)
- [Writing code with intelligence in Xcode](https://developer.apple.com/documentation/xcode/writing-code-with-intelligence-in-xcode)
- [Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/)
- Fleet: [ios/VRM_DANCE_APP.md](../ios/VRM_DANCE_APP.md)

---
*Last updated: 2026-05-28*
