# Apple and the Model Context Protocol (MCP)

## Summary (May 2026)

**Apple now ships MCP for Xcode.** Xcode 26.3+ exposes an MCP server so external agents (Cursor, Claude Code, Codex CLI) can build, test, and edit the open project. Fleet FastMCP servers (avatar-mcp, blender-mcp, godot-mcp, …) remain separate and typically run on Windows.

**Apple’s app-integration surface** for end-user apps is still **App Intents, Shortcuts, Siri, and Foundation Models** — not MCP inside App Store apps.

## Xcode MCP (official, Feb 2026)

| Item | Detail |
|------|--------|
| **Shipped in** | Xcode 26.3 |
| **Enable** | Xcode → Settings → Intelligence → **Allow external agents to use Xcode tools** |
| **Bridge command** | `xcrun mcpbridge` |
| **Claude Code** | `claude mcp add --transport stdio xcode -- xcrun mcpbridge` |
| **Codex** | `codex mcp add xcode -- xcrun mcpbridge` |
| **Requires** | Project open in Xcode while agent runs |

Capabilities: file tree, Apple doc search, Swift edits, build/test, Preview capture.

Doc: [Giving external agents access to Xcode](https://developer.apple.com/documentation/xcode/giving-external-agents-access-to-xcode)

Fleet guide: [development/AGENTIC_XCODE_26.md](development/AGENTIC_XCODE_26.md)

## MCP in the wider ecosystem

- **Open standard**: JSON-RPC, Streamable HTTP; Agentic AI Foundation governance
- **Fleet servers**: sandraschi FastMCP repos on fixed ports (see `operations/fleet-registry.json`)
- **Not merged**: Xcode MCP does not call avatar-mcp automatically — you configure both in the agent client

## Apple’s app-facing “context” APIs

| Mechanism | Role |
|-----------|------|
| **App Intents** | Siri, Shortcuts, Spotlight, widgets, Action button |
| **Foundation Models** | On-device LLM from Swift in your app |
| **Shortcuts** | User automation calling App Intents |
| **Siri + Gemini** | System assistant (iOS 26.4+) |

## Using MCP on Apple hardware

### macOS (development machine)

| Layer | Setup |
|-------|--------|
| **Xcode agentic** | Xcode 26.3 Intelligence + optional `mcpbridge` for Cursor/Claude Code |
| **Fleet MCP** | Run Python FastMCP servers locally or reach Windows box via Tailscale |
| **Local LLM** | Ollama, llama.cpp, MLX |

### iOS / iPadOS (runtime)

- **No MCP in production apps** — use Swift APIs
- **Dev**: Simulator + agentic Xcode; staged assets from avatar-mcp over network share or git LFS

## Combined workflow example

```text
Windows (RTX 4090)                    Mac (Xcode 26.3)
────────────────────                  ──────────────────
avatar-mcp hub_download               Xcode open: VRM Dance App.xcodeproj
blender-mcp bake VMD → glTF    ──►    Cursor/Claude + mcpbridge
godot-mcp (game track only)           Agent adds Swift VRM loader + TestFlight archive
```

## When to use which

| Goal | Use |
|------|-----|
| Build iOS/macOS app with AI assistant | **Xcode 26.3 agentic** + `mcpbridge` |
| Stage VRM / Hub OAuth / fleet pipeline | **avatar-mcp** (Windows or Mac if running Python) |
| Godot game character | **blender-mcp → godot-mcp GLB** — not Xcode MCP |
| Doll Dancer–style App Store app | **Swift native** — see [ios/VRM_DANCE_APP.md](ios/VRM_DANCE_APP.md) |
| Siri / Shortcuts in shipped app | **App Intents** |

## Historical note

Prior MCD versions (through March 2026) stated Apple did not ship MCP. **Xcode 26.3 superseded that** for the IDE toolchain only.

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Xcode updates (Feb 2026 agentic)](https://developer.apple.com/documentation/Updates/Xcode)
- Apple: [App Intents](https://developer.apple.com/documentation/AppIntents), [Apple Intelligence](https://developers.apple.com/apple-intelligence)

---
*Last updated: 2026-05-28*
