# macOS: Desktop development (October 2026)

## Context

- **macOS Golden Gate 27.2** (Oct 2026) — **current, Apple-silicon-only**; last version with full Rosetta 2 (Tahoe 26 was the last Intel release)
- **Xcode 27.2** agentic IDE — primary development surface for Apple targets
- **Apple Intelligence / Foundation Models + Core AI** available for Mac apps  

## Agentic Xcode on Mac

Same workflow as iOS — see [development/AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md).

Mac is the **required machine class** for:

- iOS / iPadOS / visionOS code signing  
- TestFlight archives  
- Xcode Previews + Simulator at full fidelity  

## Fleet split: Mac + Windows

| Workload | Typical host |
|----------|--------------|
| Xcode / Swift / App Store | Mac |
| avatar-mcp, blender-mcp, godot-mcp, RTX inference | Windows (4090) |
| Cross-machine | Tailscale; shared staging paths or git |

Run fleet MCP servers on Mac too if desired (`uv run` works) — not required.

## Metal and local ML

- **MPS / MLX / Core ML** — unchanged; use for app runtime ML  
- **Ollama / llama.cpp** — local LLMs for non-Xcode tooling  
- **MCP fleet servers** — Python FastMCP on macOS identical to Windows  

## Shell tooling

- **Homebrew** — `ollama`, dev dependencies  
- **Zsh** — default shell  

## References

- [AGENTIC_XCODE_26.md](../development/AGENTIC_XCODE_26.md)  
- [MCP_AND_APPLE.md](../MCP_AND_APPLE.md)  

---
*Last updated: 2026-10-28 (27.2 generation)*
