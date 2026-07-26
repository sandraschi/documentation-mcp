# OpenCode — FOSS AI Coding Agent

**Status:** Active use (July 2026 — updated from Apr 2026 baseline)
**Category:** AI coding agent / Cursor alternative
**License:** MIT
**Homepage:** https://opencode.ai
**GitHub:** https://github.com/anomalyco/opencode
**Stars:** ~160K (July 2026 — up from 149K in April)

---

## Who Built It

OpenCode is built and maintained by **Anomaly** (`anomalyco` on GitHub), a small team of terminal enthusiasts. The four known co-founders:

- **Paul Copplestone** — co-founder of Supabase; left to join Anomaly for this project
- **Jay V** — team lead; Neovim power-user; known for aggressive release cadence (~3.2 releases/day sustained over months)
- **Brendon** — core contributor; handles much of the Tauri desktop app work
- **Adam Elmore** — AWS Hero, indie hacker, hosts AWS FM podcast; joined as a friend at launch

The team previously built **terminal.shop** — a fully functional coffee subscription store operable entirely from the command line, which made over $100K in its first year. That background is directly relevant: when they built OpenCode, they weren't learning how to do terminal UIs. They had already shipped polished TUI product to paying customers.

OpenCode launched **June 19, 2025**, as an MIT-licensed, Claude Code-compatible alternative. Within five months it had 650K monthly active users. By March 2026 it hit #1 on Hacker News with 1,099 points and 546 comments. By April 2026: ~149K GitHub stars, 864+ contributors, 11,630+ commits.

Parallel project: **models.dev** — an open-source database of AI models, also by Anomaly.

---

## What It Is

OpenCode is a **provider-agnostic AI coding agent** available as:

- A terminal TUI (primary interface, built with their own `opentui` library, successor to Bubble Tea)
- A desktop GUI app (Tauri-based, currently in beta)
- IDE extensions (Zed supported; VS Code/others via LSP)

It operates as an **agentic loop** — not just a chat interface. The agent can read files, write/edit files, run shell commands, grep, glob, navigate LSP symbols, and call external MCP tools. It is architected as a **client/server system**: the `opencode` CLI runs a local HTTP server, and any client (TUI, desktop app, potentially a mobile app) connects to it. This means you can run the agent on a remote machine and drive it from another device.

Two built-in agent modes, switchable with Tab:

- **Build** — full file modification access; the default work mode
- **Plan** — read-only; for analysis and exploration without touching anything

---

## Provider Support

Supports 75+ providers via a unified abstraction layer (Vercel AI SDK under the hood):

- **Anthropic** (Claude Sonnet, Opus, Haiku — any model via API key)
- **OpenAI / Azure OpenAI**
- **Google Gemini / Vertex AI**
- **Amazon Bedrock**
- **OpenRouter** (aggregates hundreds of models including DeepSeek V4)
- **Groq, Together AI, Cerebras, Mistral, Perplexity, xAI**
- **Ollama** (local; any model that fits in your VRAM)
- **LM Studio, llama.cpp**
- **OpenCode Zen** — their own curated pay-as-you-go tier; good default for new users
- **OpenCode Go** — alternative managed tier
- **LLM Gateway, Cloudflare AI Gateway**
- **GitHub Copilot** (with caveats — see drama below)

You can switch models mid-session. Model references follow the format `<providerId>/<modelId>`.

---

## Key Features

**MCP Integration** — Supports both stdio and SSE MCP servers, configured in `opencode.jsonc`. MCP tools become available to the agent automatically alongside built-in tools, following the same permission model. This is the hook for Sandra's fleet.

**LSP Integration** — Automatically manages Language Server Protocol servers for 20+ languages. The agent can access diagnostics, type information, references, and symbols — giving it the same codebase intelligence as your IDE. Currently only diagnostics are exposed to the AI; completions/hover/definitions are parsed but not yet surfaced to the agent.

**Multi-session** — Multiple parallel agent sessions on the same project simultaneously. This is unique among CLI tools. You can run a Plan agent and a Build agent in parallel.

**Custom commands** — Reusable prompts stored as Markdown files (`~/.config/opencode/commands/` or per-project). Support named argument placeholders (`$ISSUE_NUMBER`, `$AUTHOR_NAME`, etc.). A `user:prime-context` command that runs `git ls-files` + reads README is a common pattern.

**Undo/Redo** — `/undo` and `/redo` revert or reapply AI edits without touching Git. Important safety net for agentic workflows.

**Session sharing** — `/share` generates a link to a specific conversation. Private by default, opt-in sharing.

**AGENTS.md generation** — `/init` analyzes your project and generates a codebase conventions file. Helps the agent understand your project structure from the start.

**Plugin system** — Extensible plugin architecture; plugins can return metadata in execute results (as of v1.4.8).

**ACP (Agent Client Protocol)** — Internal protocol that all clients use to talk to the backend server. Enables the client/server split.

---

## Windows Desktop App (Beta) — Current Status (April 2026)

The desktop app is built with **Tauri** (Rust backend, web frontend). It ships as a separate binary from the CLI/TUI. The desktop app runs a local `opencode-cli` sidecar process in the background; most issues trace back to that sidecar failing to spawn or health-check correctly.

**Installation (Windows):**
```
scoop bucket add extras
scoop install extras/opencode-desktop
```
Or download directly from https://opencode.ai/download (look for the Windows `.exe` installer).

**Config location on Windows:**
```
%USERPROFILE%\.config\opencode\opencode.jsonc
```

**Known Windows-specific issues (active as of April 2026):**

- *Sidecar spawn failure* — "Error: Failed to spawn OpenCode Server" on first launch; usually caused by a port conflict or missing CLI installation. Fix: ensure the CLI (`opencode`) is also installed and on PATH. If `OPENCODE_PORT` is set in your environment, unset it or pick a free port.
- *Health check timeout* — Sidecar starts but desktop app can't reach it within the timeout window. Common after updates; fix by fully quitting, deleting `opencode.settings.dat` / `opencode.global.dat` / `opencode.workspace.*.dat` from the app data directory, and relaunching.
- *Input not accepting text* — Reported on Windows 11 as of v1.14.20 (issue #23875, April 22 2026); the command input box sometimes refuses keyboard input. Workaround: click elsewhere in the window first, or restart the app.
- *Pane resize glitch* — Panes get attached to the mouse pointer during resize (same issue, Windows 11).
- *File tree disappearing* — Fixed in v1.4.9 (April 17 2026). Update if you're on an older build.
- *`ctrl+z` behavior* — Fixed in a recent release; terminal suspend and input undo now work correctly on Windows.
- *WSL path confusion* — If you have WSL installed, the app can conflate Windows and WSL paths. Stick to native Windows paths in config.

**Recommendation for Sandra's setup:** The CLI/TUI is more reliable on Windows right now. Use the desktop app as a secondary interface; file an issue if you hit new breakage since the team responds fast.

---

## Community Echo

The Hacker News thread (March 20, 2026, #1 post) surfaced three dominant themes:

1. **Relief at genuine lock-in escape.** The most upvoted sentiment was "finally a real open-source alternative." Developers are uncomfortable with tools whose entire workflow depends on one provider's pricing decisions.

2. **Performance debate.** Claude Code reportedly uses multiple GB RAM and high CPU; OpenCode TUI uses 1GB+ (notable for a TUI, and a legitimate complaint). The team has an open Memory Megathread (issue #20695) tracking this.

3. **Privacy incident (now resolved).** In v1.2.20, a developer ran the tool through mitmproxy and discovered it was silently sending prompts to Grok's free tier for session title generation — even when the user had configured only local models. Grok's free tier trains on submitted data. This was fixed after community outcry. **Check your version; anything post-v1.2.20 has the fix.** The incident damaged trust briefly but the team responded quickly.

**Drama: the Anthropic ToS clash (January 2026).** Some users discovered they could use Claude Pro/Max subscription credentials through OpenCode instead of Claude Code, effectively getting OpenCode's flexibility at Anthropic's subscription price. Anthropic tightened enforcement on January 9, 2026 — the error message is now "This credential is only authorized for use with Claude Code and can't be used for other API requests." Standard API keys still work fine; this only affected subscription credential abuse.

**Release velocity** is both a strength and a weakness. ~3.2 releases per day, every day, for months. Problems get fixed fast; new problems get introduced fast. Always check the changelog before updating if you're mid-project.

---

## Comparison to Cursor / Claude Code

| Dimension | OpenCode | Cursor | Claude Code |
|---|---|---|---|
| License | MIT / FOSS | Proprietary | Proprietary |
| Cost | API costs only | $20/month Pro | Usage-based (Anthropic API) |
| Provider lock-in | None (75+ providers) | Partial (multiple but Cursor-managed) | Anthropic only |
| Primary interface | Terminal TUI + desktop beta | Full IDE (VS Code fork) | Terminal |
| IDE autocomplete | No (agent-level only) | Yes (inline) | No |
| Multiagent | No (single session; parallel sessions possible but not coordinated) | No | No |
| LSP integration | Yes (diagnostics exposed to AI) | Yes (native IDE) | Limited |
| MCP support | Yes (stdio + SSE) | Yes | Yes |
| Local model support | Yes (Ollama, LM Studio, llama.cpp) | Limited | No |
| Windows support | Beta (rough edges) | Stable | Stable |
| RAM usage | ~1GB+ (TUI); more (desktop) | High | Moderate |

---

## Gaps and Limitations (April 2026)

**Not multiagent.** OpenCode runs one agent per session. You can open multiple sessions and run them in parallel (manually), but there is no orchestration layer, no agent-to-agent communication, no supervisor/worker hierarchy. For fleet-scale automation across 135 repos, you would need to script this externally. This is a significant gap vs. what robofang or a proper multiagent framework would give you.

**No inline autocomplete.** OpenCode operates at the task level, not the keystroke level. It does not replace Copilot-style inline suggestions in your editor. Many users run OpenCode alongside a Copilot subscription for autocomplete. For Sandra's workflow (Cursor/Windsurf already provide autocomplete), this is not a gap.

**Context window management is opaque.** On large codebases, the agent hits context limits without clearly communicating what it can and cannot "see." There's no explicit context visualizer or warning system equivalent to Cursor's token counter.

**Error recovery is clunky.** When the agent makes a mistake mid-task, clean rollback depends on `/undo` or good git hygiene. Always work on a clean git branch. The undo system is per-session; it does not persist across restarts.

**Documentation lags the feature set.** As of April 2026, docs are still catching up. You will sometimes need to read GitHub issues or the source to understand current behavior.

**Windows is second-class.** Linux and macOS are clearly first-class. Windows works, but you hit more rough edges, especially in the desktop beta. The TUI is more reliable than the desktop app on Windows currently.

**RAM usage.** ~1GB for a TUI is high. The team is aware (Memory Megathread). Not a problem on Goliath (64GB) but worth monitoring.

**FastMCP 3.2 pattern accuracy varies by model.** OpenCode itself is model-agnostic, so code quality depends entirely on what you route through it. DeepSeek V4 and local models may hallucinate older FastMCP API shapes. Test before trusting on fleet work.

---

## Cost Model for Sandra's Stack

| Provider | Model | Est. cost | Use case |
|---|---|---|---|
| Local (Ollama) | Qwen3.5 27B | Free | Routine fleet work, offline |
| Local (Ollama) | Qwen3.5 35B-A3B MoE | Free | Faster (~112 tok/s), 3B active params |
| OpenRouter | DeepSeek V4 | ~$0.10-0.30/M tokens | Cheap cloud, bulk tasks |
| Anthropic API | Claude Sonnet 4.6 | Standard API rates | High-accuracy work, FastMCP 3.2 tasks |
| Anthropic API | Claude Opus 4.6 | Standard API rates | Complex architecture sessions |

Running OpenCode with Ollama on the 4090 is effectively free at the point of use. DeepSeek V4 via OpenRouter is the cheapest cloud option for tasks where local quality isn't enough.

---

## Installation (Windows — Goliath)

**CLI (recommended, most stable):**
```powershell
# Via Scoop (recommended)
scoop install opencode

# Via npm
npm i -g opencode-ai@latest

# Via Chocolatey
choco install opencode
```

**Desktop app (beta):**
```powershell
scoop bucket add extras
scoop install extras/opencode-desktop
```

**Config file:** `%USERPROFILE%\.config\opencode\opencode.jsonc`

**MCP server config example:**
```jsonc
{
  "mcpServers": {
    "my-mcp-server": {
      "type": "stdio",
      "command": "path\\to\\mcp-server.exe",
      "env": [],
      "args": []
    },
    "remote-sse": {
      "type": "sse",
      "url": "http://localhost:10800/sse"
    }
  }
}
```

**Troubleshooting desktop app startup failures:**
1. Quit the app fully
2. Delete: `%APPDATA%\opencode\opencode.settings.dat`, `opencode.global.dat`, `opencode.workspace.*.dat`
3. Relaunch
4. If still failing: check that `opencode` CLI is installed and on PATH (the desktop app spawns it as a sidecar)

---

## Verdict for Sandra's Workflow

OpenCode is a legitimate Cursor partial-replacement, not a toy. The FOSS + provider-agnostic architecture is the right long-term bet — no vendor can hold you hostage via pricing. The ability to route to local Qwen3.5 on the 4090 or DeepSeek V4 via OpenRouter makes it essentially free to run for routine work.

The gaps that matter for this fleet:

- Not multiagent — won't replace robofang or orchestration scripts for fleet-scale tasks
- Windows desktop beta still rough — use CLI/TUI for serious work
- FastMCP 3.2 accuracy depends on which model you use; test before trusting cheap models on fleet repos

Best fit right now: **terminal TUI + Ollama for local work, OpenRouter/DeepSeek for cloud bursts, Anthropic API for high-stakes sessions.** Run alongside Cursor/Windsurf rather than fully replacing them until the desktop app matures.

---

## Links

- Homepage: https://opencode.ai
- GitHub: https://github.com/anomalyco/opencode
- Changelog: https://opencode.ai/changelog
- Docs: https://opencode.ai/docs
- Troubleshooting: https://opencode.ai/docs/troubleshooting/
- models.dev (Anomaly's model database): https://models.dev
- Anomaly GitHub org: https://github.com/anomalyco

---

---
## What Changed Since April 2026 (v1.14 → v1.17.19)

OpenCode's release cadence is ~1-3 per day. The April-to-July gap is massive.

### New Features Relevant to the Fleet

| Feature | Version | What it does | Fleet relevance |
|---------|---------|--------------|-----------------|
| **Agent Skills** | v1.16+ | OpenCode has a skill system similar to Claude's. Skills are loaded into agent context at session start. | We could inject tool-awareness skills into opencode via `.opencode/skills/` for every repo |
| **Custom Tools** | v1.14+ | `.opencode/tools/` directory — `.ts` files become tools the agent can call | Already used by opencode-cli-mcp. Our MCPB install tool fits here |
| **References** | v1.17.0+ | Structured config system for project references with descriptions, autocomplete, and agent context injection | Could replace some `.cursorrules` / `CLAUDE.md` patterns |
| **Code Mode MCP Adapter** | v1.17.14 | Native code mode for running confined scripts against MCP tools. Hides `execute` tool unless enabled. | Aligns with FastMCP's `CodeMode` — same concept, different impl |
| **MCP Resources** | v1.17.10 | Can read MCP resources and resource templates via tools | Our `@mcp.resource()` endpoints are now consumable from opencode |
| **Yolo Mode** | v1.17.12 | Auto-approves all permissions (no approval prompts) | Useful for CI/automation — but dangerous for prod |
| **Go Mode** | v1.15+ | Second agent mode alongside Plan/Build. CLI-focused. | Not directly relevant |
| **Mini Mode** | v1.17.10 | `--mini` CLI flag for lightweight sessions | Useful for quick tasks |
| **Plugin API** | v1.17.10+ | Namespaced plugin hooks, V2 plugin API for Effect/Promise | If we build plugins, we hook into opencode directly |
| **ACP (Agent Client Protocol)** | v1.16+ | OpenCode can run as an ACP agent for other editors | OpenCode as a provider for Zed/JetBrains |

### MCP Improvements (High Signal)

- v1.17.14: **Code mode MCP adapter** — opencode can now script MCP tools in a confined sandbox
- v1.17.12: **Yolo mode** — auto-approve permissions (use with caution)
- v1.17.10: **MCP resource tools** — can list and read MCP resources
- v1.17.10: **MCP server instructions injected into session context**
- v1.17.7: **MCP servers receive workspace as client root**
- v1.17.4: **MCP servers support `cwd`** — start from workspace-relative directory
- v1.17.4: **Structured MCP tool output** — readable form instead of raw JSON
- v1.17.0: **MCP catalogs paginate correctly** — no more truncated tool lists
- v1.17.0: **MCP servers respect advertised capabilities**
- v1.16.x: **Multiple MCP servers** can be configured in `opencode.jsonc`
- v1.16.x: **OAuth for MCP servers** — browser-based auth flow

### Gaps Still Present

Windows desktop app is still in beta but improving (WSL support added in v1.17.0, better server management). CLI/TUI remains the primary reliable interface. The doc site is now much better than April — `docs/` covers tools, rules, agents, models, themes, keybinds, commands, permissions, policies, LSP, MCP servers, ACP, skills, references, and custom tools.

### What This Means for the Fleet

1. **We should ship `.opencode/skills/`** alongside `.cursorrules` — opencode now has a skill system
2. **`opencode.jsonc` references** may replace some `CLAUDE.md` content — opencode reads both
3. **MCP resource tools** mean our `@mcp.resource()` endpoints are directly consumable in opencode
4. **Code mode** alignment with FastMCP's CodeMode is worth investigating
5. **Yolo mode** is useful for CI but dangerous — document as a known risk

---

*Last updated: 2026-07-13 by Claude*
