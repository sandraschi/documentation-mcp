# Agentic Coding Comparison: Claude Code, Antigravity, Cursor & OpenCode

**Date:** 2026-11-15  
**Scope:** Late-2026 state of the four primary agentic coding platforms in daily rotation — three megacorp/VC-backed platforms pushing their own models (**Claude Code**, **Antigravity**, **Cursor**) vs. the scrappy MIT-licensed FOSS contender (**OpenCode**).

---

## 1. At-a-Glance Matrix

| Dimension | **Claude Code** (Anthropic) | **Antigravity (`agy`)** (Google) | **Cursor** (Anysphere) | **OpenCode** (FOSS / MIT) |
|---|---|---|---|---|
| **Backing & License** | Anthropic (proprietary) | Google (proprietary IDE/CLI; Apache 2.0 SDK wrapping closed Go `localharness`) | Anysphere / VC-backed (proprietary VS Code fork + CLI) | Community / MIT open-source |
| **Surfaces** | Terminal CLI, IDE extensions, Claude Desktop | Standalone IDE (VS Code fork), `agy` TUI CLI, Python SDK, Sidecars | Standalone IDE (VS Code fork), Cursor CLI (`agent` / `cursor-agent`) | TUI, standalone desktop app, VS Code extension, mobile companion |
| **Model Strategy** | **Claude-only** (pushes Anthropic frontier models) | **Gemini-only** (pushes Gemini 4 Carbon / Argon / Hydrogen) | **First-party Grok (4.5–4.7) + Composer (2.5)** (xAI/SpaceX tie-in) + multi-model routing | **Model-agnostic** (75+ providers via Models.dev, Ollama, OpenCode Zen $0) |
| **Account / Billing** | Claude Pro / Max / API | Google AI Pro / Ultra / Gemini API (free tier gutted Jun 2026) | Cursor Pro / Ultra / Business (one sub per account) | **No account required** (bring your own API key, local Ollama, or free Zen) |
| **Context Window** | Anthropic model limits; subagents isolate context | **1M unified** (input + thinking + output) on Gemini 4 | Model-dependent; codebase semantic indexing | Model-dependent; **LSP + progressive skill loading** |
| **Multi-Agent** | Isolated **Subagents** (`.claude/agents/`, summary return) | **Orchestrator** (Argon/Carbon + Hydrogen), `/swarm`, `/teamwork`, subagents | Up to **8 parallel agents** in git worktrees / remote Cloud Agents | Multi-session & parallel subagents (mix cheap + frontier models) |
| **Extensibility** | **Hooks** (deterministic lifecycle), Skills (`SKILL.md`), Plugins, MCP | Skills, Rules, Hooks, Plugins, Sidecars, MCP (~50-tool budget) | Skills (`/migrate-to-skills`), MDC rules, Slash commands, MCP | Open **Agent Skills** (`SKILL.md`), `opencode.json`, `AGENTS.md`, MCP |
| **Local / Offline ($0)** | No (Anthropic API/sub only) | No (no first-class Ollama/LM Studio) | Poor (no first-class local provider) | **First-class** (Ollama, LM Studio, any OpenAI-compat endpoint) |

---

## 2. Platform Deep Dives

### A. Claude Code (Anthropic)

**Positioning:** Programmable, terminal-first agentic engineering platform with the most mature deterministic lifecycle controls.

- **Strengths:**
  - **Deterministic Hooks:** Event-driven lifecycle scripts (`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`) that run shell commands, HTTP calls, MCP tools, or single-turn checks. Unlike `CLAUDE.md` instructions (which a model can misread), a hook returning exit code `2` hard-blocks dangerous actions or auto-runs formatters deterministically.
  - **Context Hygiene via Subagents + Lazy Skills:** Custom subagents (`.claude/agents/`) run in isolated context windows and return only clean summaries. Unified `SKILL.md` skills keep zero instructions in context until invoked (with `disable-model-invocation: true` for sensitive workflows).
  - **Plugin Packaging:** Clean `.claude-plugin/plugin.json` bundling for sharing hooks, skills, subagents, and MCP servers.
  - **Lazy MCP Tool Discovery:** Loads lightweight tool names at startup and resolves full schemas on demand.
- **Quirks:**
  - `CLAUDE.md` is loaded in full every session—bloating it (>200 lines) degrades attention and burns context.
  - Anthropic cracked down on third-party tools piggybacking on Claude Pro/Max OAuth subscriptions, pushing multi-provider users toward OpenCode or raw API keys.
- **Gaps:**
  - **100% Anthropic model lock-in** (no Gemini, GPT, or local Ollama).
  - **No native GUI IDE** of its own (relies on terminal TUI + editor extensions / Claude Desktop).

---

### B. Antigravity (`agy` — Google)

**Positioning:** Google's agentic IDE + lightweight `agy` CLI + Python SDK, tightly tuned around Gemini 4's 1M context and multi-model orchestration.

- **Strengths:**
  - **1M Unified Context + Long Decode:** Gemini 4 (Carbon, Argon, Hydrogen) shares a 1,048,576-token window across input, thinking, and output, with long-decode support up to 1M tokens.
  - **Orchestrator (Model Hot-Swapping):** Automatically pairs a frontier planner (**Argon** on Pro/Ultra, **Carbon** on Ultra) with **Hydrogen** for fast code edits and test loops—cutting quota burn (~24%) and wall-clock time (~19%) vs. running a single heavy model end-to-end.
  - **Rich Native Primitives:** Built-in `/swarm`, `/teamwork`, `run_workflow`, browser subagent, and interactive **Sidecars** (e.g., 3D viewers, live UI panels) that go beyond plain terminal text.
  - **Tunable Thinking Levels:** `low`, `medium`, `high` across Gemini 4, plus `xhigh` on Hydrogen (which often punches near Argon on execution tasks).
- **Quirks:**
  - **Pro vs. Ultra Gatekeeping:** `Carbon` and `Orchestrator (Carbon)` are Ultra/Enterprise-only; Pro accounts get `Orchestrator (Argon)`, `Argon`, and `Hydrogen` under a rolling **5-hour + weekly** compute quota.
  - **Closed Critical Path in Open-Source Wrapper:** The Python SDK (`google-antigravity`) is Apache 2.0, but the actual agent loop, thinking, and compaction live inside a compiled, closed-source Go binary (`localharness`).
  - **~50-Tool MCP Budget:** Requires active MCP tool curation (e.g., via `agy-fleet-mcp`) when connecting large server fleets.
  - **No Multi-Account Switcher:** Stores auth in `~/.gemini`; requires Linux `unshare`/`bwrap` or Windows `USERPROFILE` wrappers for parallel accounts.
- **Gaps:**
  - **100% Google/Gemini lock-in** (no Ollama, DeepSeek, or Anthropic).
  - **Free tier gutted** (Jun 2026); requires paid Pro/Ultra or API billing.
  - **Historical data-safety caution** on recursive workspace deletions during heavy orchestration (keep cold backups / git hygiene).

---

### C. Cursor (Anysphere)

**Positioning:** The polished IDE leader for visual task delegation, parallel git-worktree agents, and multi-model routing—now backed by a SpaceX/xAI partnership pushing **Grok (4.5–4.7)** as its flagship frontier tier alongside **Composer (2.5)** for fast coding.

- **Strengths:**
  - **Best-in-Class IDE UX:** Up to **8 parallel agents** isolated in git worktrees, an aggregated multi-file diff viewer, embedded **Browser** with DOM element forwarding, and distinct **Agent / Ask / Plan / Debug** modes.
  - **First-Party Grok + Composer Split:** **Grok (4.5–4.7)** brings up to 500k context, adjustable effort (`low`/`medium`/`high`/`xhigh`), and strong long-horizon reasoning/self-verification, while **Composer (2.5)** handles fast, low-cost (200k context) everyday agentic edits—both drawing from Cursor's shared first-party usage pools.
  - **Native Multi-Profile on Desktop:** `--user-data-dir` works cleanly out of the box on Windows 11, macOS, and Linux for running separate work/personal logins simultaneously.
  - **MCP UX & Guardrails:** Auto-review pipeline (allowlist → sandbox → classifier → approval prompt) plus timed auto-approve (~60s) in Cursor 3.13+.
- **Quirks:**
  - **CLI Is Secondary:** While Cursor CLI (`agent` / `cursor-agent`) exists, its core identity is the GUI IDE; running two CLI accounts still hits the `~/.cursor` single-dir quirk (`unshare` / `USERPROFILE` wrapper).
  - **Unicode Emoji Regression:** Known fleet quirk where Cursor outputs superfluous emojis in code/scripts unless constrained by rules.
  - **Public Profiles Confusion:** `cursor.com/@handle` profiles are social/activity pages, *not* billing or account-switching profiles.
- **Gaps:**
  - **No First-Class Local Inference:** Weak/broken story for Ollama and LM Studio compared to Zed or OpenCode.
  - **No In-App Account Switcher:** Requires `--user-data-dir` workarounds.
  - **Subscription & Credit Opacity:** Tightening usage pools and opaque model-routing economics as Cursor steers users toward its first-party **Grok** / **Composer** usage pools over third-party models.

---

### D. OpenCode (FOSS / MIT)

**Positioning:** The scrappy, MIT-licensed open-source contender—built for total model freedom, zero account lock-in, and full ownership of the agent loop.

- **Strengths:**
  - **Zero Account / Zero Lock-In:** Works with **75+ providers** (Models.dev), raw API keys (Anthropic, Google, OpenAI, DeepSeek, xAI), local **Ollama / LM Studio** ($0), or **OpenCode Zen** free routing.
  - **Self-Owned Critical Path:** 100% auditable MIT codebase—no closed-source Go harness or opaque telemetry black box.
  - **Smart Context Architecture:** Native **LSP** integration + progressive `SKILL.md` loading (only skill names/descriptions at startup; full instructions loaded on match) + Plan vs. Build mode separation + parallel subagents that can mix cheap/local workers with frontier debuggers.
  - **Vibrant FOSS Skill Ecosystem:** Community packs like **Obra Superpowers** (TDD + systematic debugging), **Caveman** (anti-slop token compression), and **Grill Me** (pre-code edge-case interviews).
- **Quirks:**
  - **Config Path Divergence:** Uses `.opencode/skills/` and `opencode.json` (plus `AGENTS.md`), which can trip up scripts written for `.claude/` or `.cursor/`.
  - **Community Plugin Telemetry & Bloat:** Some third-party skill/plugin packs (e.g., Superpowers) enable telemetry by default (`SUPERPOWERS_DISABLE_TELEMETRY=1`) or ship unmaintained scripts that need pruning.
  - **Weaker-Model Discipline:** Because it lets you plug in cheap or local models, weak models can suffer from "hallucinated confidence" unless paired with strict `AGENTS.md` rules and TDD/verification skills.
- **Gaps:**
  - **Less Turnkey Polish:** No megacorp-hosted 1M-context proprietary orchestrator or polished VS Code fork diff/browser UX out of the box (though TUI, desktop app, VS Code ext, and mobile companion exist).
  - **No Bundled Compute Quota:** If you aren't using free Zen or local Ollama, you pay per-token API rates directly.

---

## 3. The Arms Race: Key Patterns in Late 2026

1. **Vertical Integration vs. Open Routing:**  
   Anthropic (Claude Code), Google (Antigravity), and Cursor (first-party **Grok 4.5–4.7** + **Composer 2.5**) are all vertically integrating—bundling subscriptions, hiding raw token math behind rolling 5-hour/weekly compute windows or shared first-party pools, and steering traffic to their own/partner models. **OpenCode** is the pressure-release valve: open harness, bring-your-own-key/local model.
2. **`SKILL.md` + `AGENTS.md` Convergence:**  
   All four have converged on progressive `SKILL.md` bundles and repo-level markdown rules (`AGENTS.md` / `CLAUDE.md` / `.mdc`), making agent workflows increasingly portable across tools.
3. **Planner + Executor Split Is the New Default:**  
   Running a flagship reasoning model on every file edit is too slow and burns quota. Antigravity formalizes this as **Orchestrator** (Argon/Carbon + Hydrogen); Claude Code does it via **Explore/Plan + Subagents**; OpenCode does it via **Plan/Build + mixed-model subagents**; Cursor does it via **Plan mode + Grok (4.6/4.7) / Composer (2.5) / parallel worktrees**.

---

## 4. Practical Rotation Strategy (Pro Accounts + OpenCode)

If you alternate across **Antigravity Pro**, **Claude Pro**, **Cursor Pro**, and **accountless OpenCode**:

| Situation | Best Tool | Why |
|---|---|---|
| **Large codebase / multi-file refactor** | **Antigravity (`Orchestrator (Argon)`)** | 1M unified context + Argon planning / Hydrogen execution saves Pro quota. |
| **Hard, safety-critical CLI/repo automation** | **Claude Code** | Deterministic `PreToolUse`/`PostToolUse` hooks + isolated subagents + strong instruction following. |
| **Visual multi-file diffs, UI/browser work, parallel worktrees** | **Cursor IDE** | Best GUI diffing, embedded browser DOM forwarding, **Grok (4.6/4.7)** + **Composer (2.5)** in first-party pools. |
| **Quota exhausted / local Ollama / $0 / non-bundled models (DeepSeek, GPT, etc.)** | **OpenCode** | No account needed, 75+ providers, full MIT transparency, strong LSP + skills. |

---

## Related Docs

- [Antigravity Ecosystem](antigravity/README.md) · [Gemini 4 & Orchestrator](antigravity/GEMINI_4_MODELS_AND_ORCHESTRATOR.md) · [Antigravity Multi-Account](antigravity/MULTI_ACCOUNT_SWITCHING.md)
- [Cursor Ecosystem](cursor/README.md) · [Grok vs Composer](cursor/GROK_VS_COMPOSER.md) · [Cursor Multi-Account](cursor/MULTI_ACCOUNT_SWITCHING.md)
- [OpenCode Ecosystem](opencode/README.md)
- [Cross-IDE Local Inference Matrix](IDE_LOCAL_INFERENCE.md)
