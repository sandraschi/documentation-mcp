# Awesome DeepSeek Agent — Fleet Overview

**Source:** [github.com/deepseek-ai/awesome-deepseek-agent](https://github.com/deepseek-ai/awesome-deepseek-agent)
**Last Updated:** 2026-05-24
**Stars:** 2.1k | **Forks:** 230

Curated by DeepSeek's own org — a reference list of guides for integrating DeepSeek models
(DeepSeek-V4-Pro and DeepSeek-V4-Flash) into popular AI agent and coding-assistant tools.
Each guide covers installation, configuration, and first run via `api.deepseek.com`.

---

## Tool Index (18 entries)

### 1. Cherry Studio
- **Type:** Cross-platform desktop AI client
- **Repo:** [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio)
- **Website:** [cherry-ai.com](https://cherry-ai.com)
- **Platforms:** Windows, macOS, Linux
- **Key features:** 300+ pre-configured assistants, multi-model chat, AI translation, knowledge bases (RAG over PDF/Markdown/Office), MCP server support, bundled OpenClaw for IM bots (Feishu, WeChat)
- **Fleet relevance:** High. Desktop client that unifies LLM access including DeepSeek V4. Has MCP support built in. Bundles OpenClaw — our fleet already has OpenClaw integrated. This is a potential fleet desktop companion app.
- **Install:** Download installer from releases page. Configure DeepSeek provider via Settings GUI, fetch model list, add `deepseek-v4-pro` / `deepseek-v4-flash`.
- **DeepSeek integration:** Built-in DeepSeek provider. 1M context window out of the box. Reasoning effort selector (high → max) mapped to API values.

### 2. Claude Code
- **Type:** AI coding assistant (terminal)
- **Maker:** Anthropic
- **Fleet status:** Already heavily used in the fleet. Guide covers DeepSeek compatibility setup.
- **Key points:** Can use DeepSeek as alternative backend via OpenAI-compatible proxy configuration.

### 3. GitHub Copilot
- **Type:** AI peer programmer (VS Code extension)
- **Maker:** GitHub/Microsoft
- **Fleet status:** Well known.
- **Key points:** Guide covers using DeepSeek V4 models as Copilot backend via custom model configuration.

### 4. GitHub Copilot CLI
- **Type:** Terminal-native coding assistant with agentic capabilities
- **Maker:** GitHub/Microsoft
- **Fleet status:** Potentially useful for fleet terminal workflows.
- **Key points:** Agentic CLI tool that can use DeepSeek as backend.

### 5. Codex
- **Type:** OpenAI's coding agent
- **Maker:** OpenAI
- **Fleet status:** Reference tool. Guide covers DeepSeek integration.
- **Key points:** OpenAI's answer to Claude Code. DeepSeek compatibility via proxy.

### 6. Kilo Code
- **Type:** AI coding assistant (CLI + editor extension)
- **Repo:** [@kilocode/cli](https://www.npmjs.com/package/@kilocode/cli) (npm)
- **Key features:** CLI-first with editor extension mode. `/connect` for provider setup, `/models` for model switching. Built-in DeepSeek provider with V4 Flash/Pro models.
- **Fleet relevance:** Medium. Another CLI coding assistant option. Clean onboarding with `/connect` → search "deepseek" → paste API key flow.
- **Install:** `npm install -g @kilocode/cli`
- **DeepSeek integration:** Built-in provider. Supported models: DeepSeek Chat, DeepSeek Reasoner, V4 Flash, V4 Pro.

### 7. WorkBuddy / CodeBuddy
- **Type:** AI agent and coding assistant (desktop app)
- **Key features:** Custom model support via local `models.json`. OpenAI-compatible endpoint config. Project-level and user-level config files.
- **Fleet relevance:** Medium. Desktop app with local config — easy to set up.
- **DeepSeek integration:** Via `~/.codebuddy/models.json` with `api.deepseek.com/v1/chat/completions`. Environment variable `DEEPSEEK_API_KEY`. UTF-8 without BOM required for config file.
- **Gotchas:** Must fully quit and restart for model changes. Environment variable expansion may fail in some desktop versions.

### 8. OpenCode
- **Type:** Open-source AI coding assistant (terminal, web)
- **Fleet status:** THIS IS OUR CURRENT TOOL. We run OpenCode.
- **Key points:** Native DeepSeek V4 support. Guide covers configuring DeepSeek as the backend model.

### 9. Oh My Pi
- **Type:** Terminal AI coding agent (forked from Pi)
- **Repo:** [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)
- **Version:** v14.5+
- **Key features:** OMP-specific tools, model roles, MCP, plugins, agent workflows. Fork of Pi with enhanced capabilities. Ships built-in DeepSeek V4 entries, but custom `models.yml` needed for reliable use.
- **Fleet relevance:** Medium-High. Feature-rich terminal agent with MCP support. Could complement OpenCode.
- **DeepSeek compatibility details (important gotchas):**
  - `supportsToolChoice: false` — DeepSeek V4 thinking mode rejects `tool_choice` parameter
  - `requiresReasoningContentForToolCalls: true` — must preserve `reasoning_content` across tool-call turns
  - `requiresAssistantContentForToolCalls: true` — tool-call messages need non-null `content`
  - `supportsDeveloperRole: false` — system prompt goes as `system` role, not `developer`
  - `maxTokensField: max_tokens` — not OpenAI's `max_completion_tokens`
  - `extraBody.thinking.type: enabled` — explicitly enables V4 thinking mode
  - Reasoning effort map: OMP `xhigh` → DeepSeek `max`
  - No OAuth `/login` — API key via env var required
- **Install:** Per repo instructions. Configure via `~/.omp/agent/models.yml`.

### 10. OpenClaw
- **Type:** Open-source personal AI assistant (chat tools + terminal)
- **Repo:** [openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Min version:** >= v2026.4.24 (for proper DeepSeek V4 thinking support)
- **Fleet status:** ALREADY IN FLEET. We run openclaw-molt-mcp.
- **Key features:** Connects to Feishu, WeChat, and other chat platforms. Extensible via Skills. Web UI, TUI, and terminal modes. QuickSetup onboarding.
- **Install:** `curl -fsSL https://openclaw.ai/install.sh | bash` (Linux/Mac) or `iwr -useb https://openclaw.ai/install.ps1 | iex` (Windows).
- **DeepSeek integration:** `openclaw onboard --install-daemon` → QuickStart → DeepSeek provider → API key → model name. Built-in provider with V4 thinking mode support.

### 11. AstrBot
- **Type:** Open-source agent assistant for chat platforms
- **Key features:** Feishu, Telegram support. Extensible with skills, plugins, MCP servers.
- **Fleet relevance:** Medium. Similar territory to OpenClaw but different ecosystem.
- **DeepSeek integration:** OpenAI-compatible endpoint configuration.

### 12. Deep Code
- **Type:** Open-source terminal AI coding assistant
- **Repo:** [lessweb/deepcode-cli](https://github.com/lessweb/deepcode-cli)
- **Key features:** Built specifically for DeepSeek-V4. Deep thinking mode, reasoning effort control, Agent Skills (SKILL.md discovery), web search capability. VSCode extension companion available. Image paste from clipboard (`Ctrl+V`).
- **Fleet relevance:** High. Purpose-built for DeepSeek V4 — this is the deepest DeepSeek-native coding tool. Agent Skills format matches our fleet convention (`~/.agents/skills/<name>/SKILL.md`).
- **Install:** `npm install -g @vegamo/deepcode-cli`
- **Config:** `~/.deepcode/settings.json` — simple JSON with `MODEL`, `BASE_URL`, `API_KEY`, `thinkingEnabled`, `reasoningEffort`.
- **Key shortcuts:** `Enter` send, `Shift+Enter` newline, `Esc` interrupt, `/` skills menu, `/new` fresh conversation, `/resume` continue previous.

### 13. Hermes
- **Type:** Self-improving AI agent
- **Maker:** Nous Research
- **Website:** [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com)
- **Key features:** Built-in learning loop — creates skills from experience, improves them over time, persists knowledge, builds evolving preference model across sessions. One-line installer.
- **Fleet relevance:** Medium-High. Nous Research is a leading open-weight model research lab. Self-improving agent architecture is novel. Learning loop concept could inform fleet agent design.
- **Install:** `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash` (requires only Git).
- **DeepSeek integration:** `hermes setup` → Quick Setup → DeepSeek provider → API key → Base URL `https://api.deepseek.com` → `deepseek-v4-pro`.

### 14. nanobot
- **Type:** Lightweight AI agent
- **Repo:** [nanobot-ai](https://github.com/nanobot-ai/nanobot) (installed via `uv tool install nanobot-ai`)
- **Key features:** Chat platform integration, memory, MCP support. Python-based, installed via `uv` (Astral's tool). Lightweight footprint.
- **Fleet relevance:** Medium. Python-native, lightweight, MCP-capable. Good fit for fleet's Python-heavy ecosystem.
- **Install:** `uv tool install nanobot-ai`
- **Config:** `~/.nanobot/config.json` — providers, agents, defaults. Point at `api.deepseek.com/v1`.

### 15. Crush
- **Type:** Glamorous open-source terminal AI coding agent
- **Maker:** Charm (charmbracelet)
- **Repo:** [@charmland/crush](https://www.npmjs.com/package/@charmland/crush) (npm)
- **Key features:** Multi-model switching, LSP integration (language server protocol for IDE-level code intelligence), MCP servers, agentic coding workflows. Charm-quality TUI aesthetics (same team behind Bubble Tea, Glow, etc.).
- **Fleet relevance:** High. LSP integration is a killer feature — provides real IDE-level code understanding (go-to-definition, diagnostics, refactoring) inside a terminal agent. No other tool in this list has LSP built in.
- **Install:** `npm install -g @charmland/crush` or `brew install charmbracelet/tap/crush` (macOS).
- **Config:** `~/.config/crush/crush.json` — providers block with `openai-compat` type, DeepSeek models with 1M context window.
- **DeepSeek integration:** `crush` → `Ctrl+L` (model switcher) → DeepSeek → V4-Pro or V4-Flash.

### 16. Pi (pi-mono)
- **Type:** Minimal extensible terminal coding harness
- **Repo:** [badlogic/pi-mono](https://github.com/badlogic/pi-mono)
- **Key features:** TypeScript extensions, skills, prompt templates, themes. Tree-structured sessions. 15+ built-in providers. Aggressively extensible design — minimal core, everything is an extension.
- **Fleet relevance:** Medium. Extensible architecture is interesting from a design perspective. Tree-structured sessions are a unique approach to conversation management.
- **Install:** `npm install -g @earendil-works/pi-coding-agent` or `curl -fsSL https://pi.dev/install.sh | sh`
- **Config:** `~/.pi/agent/models.json` — providers with `compat` block including `requiresReasoningContentOnAssistantMessages`, `thinkingFormat: "deepseek"`, `reasoningEffortMap`.
- **DeepSeek integration:** Pricing-aware config with cost per token. `/model` command to switch.

### 17. Reasonix
- **Type:** DeepSeek-native coding agent (terminal)
- **Repo:** [esengine/reasonix](https://github.com/esengine/reasonix)
- **Key features:** Designed entirely around DeepSeek's API — no translation shim. Cache-first loop for cost efficiency. Flash-first by default, `/pro` to arm V4-Pro for next turn, `/preset max` for full Pro session. Automatic tool-call repair. Talks directly to `api.deepseek.com`.
- **Fleet relevance:** High. DeepSeek-native — no OpenAI-compat layer. Cache-first architecture reduces API costs. The `/pro` and `/preset` pattern is smart: use Flash for iteration, Pro for critical reasoning.
- **Install:** No global install — `npx reasonix code` in project directory. API key stored to `~/.reasonix/config.json` via built-in wizard.
- **DeepSeek integration:** Deepest possible — native API consumer. No environment variable needed.

### 18. Langcli
- **Type:** AI coding assistant (CLI + Zed ACP Agent)
- **Website:** [langcli.com](https://langcli.com)
- **Key features:** 100% Claude Code compatible. Supports mainstream LLM models. CLI and Zed ACP Agent modes. Uses LangRouter for API key management (free trial available).
- **Fleet relevance:** Medium. Claude Code compatibility means drop-in replacement potential. Zed integration is unique.
- **Install:** `bash -c "$(curl -fsSL https://assets.langcli.com/installation/install-langcli.sh)"` or `npm i -g langcli-com`.

### 19. DeepSeek-TUI (Bonus — most technically impressive)
- **Type:** Open-source Rust terminal coding assistant
- **Repo:** [Hmbown/DeepSeek-TUI](https://github.com/Hmbown/DeepSeek-TUI)
- **Key features:** Codex-style 13-crate Rust workspace. Direct DeepSeek API consumer (no proxy). 1M token context window. Sandboxed tool execution — macOS (Seatbelt), Linux (Landlock), Windows. MCP client AND server. Sub-agents via `agent_spawn`. Built-in RLM (recursive-LM) for oversized input processing in sandboxed Python REPL. HTTP runtime API (`deepseek serve --http`) for IDE embedding.
- **Fleet relevance:** VERY HIGH. This is the most architecturally sophisticated tool on the list. Rust + sandboxed execution + MCP server + sub-agent spawning + HTTP runtime API. Could serve as a reference architecture for fleet native app development.
- **Install:** `npm install -g deepseek-tui` (cross-platform prebuilt) or `cargo install deepseek-tui-cli` (Rust 1.85+).
- **Config:** `~/.deepseek/config.toml` (main config). `~/.deepseek/mcp.json` (MCP servers). Skills at `~/.deepseek/skills/<name>/` or `./.deepseek/skills/<name>/`. Hooks (pre/post lifecycle) in config.
- **Modes:** `Tab` cycles Plan (read-only) / Agent (approval required) / YOLO (auto-approve all).
- **Reasoning:** `Shift+Tab` cycles effort: off → high → max.
- **This mirrors OpenCode's Plan/Agent/YOLO mode system closely.**

---

## Fleet Quick-Assessment Matrix

| Tool | Type | DeepSeek Native | MCP | Skills | Fleet Interest |
|------|------|:---:|:---:|:---:|:---:|
| **DeepSeek-TUI** | Rust terminal agent | Yes | Client+Server | SKILL.md | VERY HIGH |
| **Reasonix** | Terminal agent | Yes (best) | — | — | HIGH |
| **Deep Code** | Terminal agent | Yes | — | SKILL.md | HIGH |
| **Crush** | Terminal agent | Compat | Yes | — | HIGH (LSP!) |
| **Cherry Studio** | Desktop client | Built-in | Built-in | — | HIGH |
| **OpenClaw** | Personal assistant | Built-in | Yes | Skills | ALREADY IN FLEET |
| **OpenCode** | Terminal agent | Yes | Yes | SKILL.md | CURRENT TOOL |
| **Oh My Pi** | Terminal agent | Compat | Yes | — | MEDIUM-HIGH |
| **Hermes** | Self-improving agent | Built-in | — | Auto-creates | MEDIUM-HIGH |
| **Pi** | Terminal harness | Compat | — | Extensions | MEDIUM |
| **Kilo Code** | CLI + editor ext | Built-in | — | — | MEDIUM |
| **nanobot** | Lightweight agent | Compat | Yes | — | MEDIUM |
| **Langcli** | Claude Code clone | Compat | — | — | MEDIUM |
| **AstrBot** | Chat platform agent | Compat | Yes | Skills | MEDIUM |
| **WorkBuddy** | Desktop agent | Compat | — | — | LOW-MEDIUM |
| **Claude Code** | Terminal agent | Compat | Yes | — | ALREADY KNOWN |
| **GitHub Copilot** | IDE extension | Compat | — | — | ALREADY KNOWN |
| **Copilot CLI** | Terminal agent | Compat | — | — | KNOWN |
| **Codex** | Terminal agent | Compat | — | — | REFERENCE |

---

## Key Architectural Patterns Worth Noting

### 1. Plan → Agent → YOLO Mode Cycling (DeepSeek-TUI, OpenCode)
Both DeepSeek-TUI and our OpenCode use a three-mode system. DeepSeek-TUI maps it to `Tab` key cycling. This pattern is becoming the de facto standard for agentic coding assistants.

### 2. LSP Integration (Crush)
Crush is the only tool integrating Language Server Protocol. This gives it real IDE-level code understanding without being an IDE extension. A potential fleet differentiator if we adopt this approach.

### 3. Cache-First Loop (Reasonix)
Reasonix's cache-first architecture reduces API costs by reusing cached responses. Combined with Flash-first iteration + on-demand Pro mode, this is the most cost-conscious design.

### 4. Sandboxed Tool Execution (DeepSeek-TUI)
DeepSeek-TUI uses OS-level sandboxing: macOS Seatbelt, Linux Landlock, Windows sandbox. This is proper security engineering — not regex-based tool filtering.

### 5. Recursive-LM (DeepSeek-TUI)
Built-in RLM processes oversized inputs in a sandboxed Python REPL without polluting parent context. Solves the context window overflow problem for 1M-token documents.

### 6. Sub-Agent Spawning (DeepSeek-TUI)
`agent_spawn` with full lifecycle family (`agent_wait`, `agent_result`, `agent_cancel`). This is the agent spawning pattern also emerging in our fleet (OpenClaw sessions, Goose sessions).

### 7. Self-Improving Loop (Hermes)
Hermes creates skills from experience, improves them during use, and persists knowledge across sessions. This is the "agent that writes its own tools" pattern.

### 8. Skill Discovery Convention (Deep Code, DeepSeek-TUI, OpenCode)
All three use `~/.agents/skills/<name>/SKILL.md` and `./.deepcode/skills/<name>/SKILL.md` (project-level). This convention is converging across tools — our fleet already follows it.

---

## DeepSeek V4 API Compatibility — Common Gotchas

From the Oh My Pi and Pi guides, these are the key DeepSeek V4 thinking-mode quirks:

1. **`tool_choice` rejected in thinking mode** — must set `supportsToolChoice: false`
2. **`reasoning_content` must be preserved** across tool-call turns in conversation history
3. **Tool-call messages need non-null `content`** — `requiresAssistantContentForToolCalls: true`
4. **`developer` role unsupported** — system prompts must use `system` role
5. **`max_tokens` not `max_completion_tokens`** — DeepSeek uses OpenAI's old field name
6. **Reasoning effort is two-level** — `high` (default) and `max`. Not `low`/`medium`/`xhigh`.
7. **Must send `extraBody.thinking.type: enabled`** on some clients for V4 thinking mode
8. **1M context window** but many clients cap at 128K input — configurable in `models.json`/`models.yml`

---

## Resources

- **DeepSeek Platform:** [platform.deepseek.com](https://platform.deepseek.com/) — get API keys
- **DeepSeek API Docs:** [api-docs.deepseek.com](https://api-docs.deepseek.com/)
- **Source repo:** [github.com/deepseek-ai/awesome-deepseek-agent](https://github.com/deepseek-ai/awesome-deepseek-agent)
- **DeepSeek V4 models:** `deepseek-v4-pro` (reasoning, $1.74/$3.48 per M tokens) and `deepseek-v4-flash` (fast, $0.14/$0.28 per M tokens)
- **China endpoint:** `https://api.deepseeki.com` (alternative to `api.deepseek.com`)
