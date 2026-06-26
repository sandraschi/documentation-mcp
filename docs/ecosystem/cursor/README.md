# Cursor IDE - MCP & Agent Integration (SOTA)

**Status:** Active  
**Updated:** 2026-06-06  
**Index:** [Jun 2026 changelog](CHANGELOG_DIGEST_JUN_2026.md) · [No local provider](NO_LOCAL_PROVIDER.md) · [Cloud Agents](CLOUD_AGENTS.md) · [Profiles](PROFILES.md) · [cursor-mcp](CURSOR_MCP_PROPOSAL.md)
**Target:** Cursor 2.x (Oct 2025+), 3.x (2026)

Cursor has evolved rapidly in late 2025 and early 2026, adding multi-agent workflows, native Skills, and deeper MCP integration. This guide covers MCP server setup, Agent modes, Skills, and SOTA patterns for MCP development.

---

## 1. Cursor 2.0+ Overview (Oct 2025)

### Multi-Agent Architecture

- **Up to 8 agents in parallel** on a single prompt
- Agents run in isolated workspaces (git worktrees or remote machines) to avoid file conflicts
- Role-based prompting: planner, implementer, tester, docs specialist
- Aggregated diff viewer to see all agent changes across multiple files

### Composer Model

- Cursor’s own agentic coding model, ~4x faster than similar models
- Most turns complete in under 30 seconds
- Codebase-wide semantic search for large codebases
- Native browser tool for testing and iterating until results are correct

### Key 2.0 Features

- **Plan Mode in background**: Create a plan with one model, build with another
- **Team Commands**: Custom commands and rules managed centrally, applied to all team members
- **Browser (GA)**: Embedded in-editor, element selection, DOM forwarding to the agent
- **Sandboxed Terminals (GA)**: macOS runs agent commands in a secure sandbox by default
- **Voice Mode**: Control Agent with speech-to-text and custom submit keywords
- **Improved Code Review**: Easier review of changes across multiple files

---

## 2. Agent Modes (2026)

| Mode | Use case | Capabilities | Tools |
|------|----------|--------------|-------|
| **Agent** | Complex features, refactoring | Autonomous exploration, multi-file edits | All tools |
| **Ask** | Learning, planning, questions | Read-only exploration | Search only |
| **Plan** | Complex features needing planning | Creates plans, clarifying questions | All tools |
| **Debug** | Tricky bugs, regressions | Hypotheses, instrumentation, runtime analysis | All tools + debug server |

- **Switching**: Mode picker dropdown or `Ctrl+.` / `Cmd+.`
- **Custom modes removed** (Cursor 2.1): Use [Custom slash commands](https://cursor.com/docs/agent/chat/commands) instead. Define workflows with `/` prefix; limit tools by including instructions in the command prompt.

---

## 3. Agent Skills (2026)

Skills are portable, version-controlled packages that extend agents with domain-specific knowledge and workflows.

### Skill Directories

| Location | Scope |
|----------|--------|
| `.cursor/skills/` | Project |
| `~/.cursor/skills/` | User (global) |
| `.claude/skills/` | Claude compatibility |
| `.codex/skills/` | Codex compatibility |

### SKILL.md Format

```yaml
---
name: my-skill
description: Short description; used by agent to decide relevance.
disable-model-invocation: false  # true = only when /skill-name invoked
---

# Instructions
Step-by-step guidance, conventions, best practices.
```

### Optional Structure

- `scripts/` – Executable code the agent can run
- `references/` – Extra docs loaded on demand
- `assets/` – Static resources (templates, images)

### Migration from Rules/Commands (Cursor 2.4)

Use `/migrate-to-skills` to convert:

- Dynamic rules ("Apply Intelligently") → standard skills
- Slash commands → skills with `disable-model-invocation: true`

---

## 4. MCP Integration

### Config Location (Windows)

- **MCP config**: `%APPDATA%\Cursor\User\globalStorage\cursor-storage\mcp_config.json`
- **Key**: `mcpServers`

### Setup

1. Cursor Settings > Features > MCP
2. "+ Add New MCP Server"
3. Set name, transport (stdio or SSE), command/URL

### Behavior

- MCP tools are available only in Agent (Composer)
- Agent selects tools when relevant
- User approval required before execution
- Not all models support all tools

---

## 5. Rules System (MDC)

- **Location**: `.cursor/rules/`
- **Format**: `[name].mdc` (Markdown + YAML frontmatter)
- **Replaces**: Single `.cursorrules` (deprecated)
- See [mcp-sota-standards.mdc](../../../.cursor/rules/mcp-sota-standards.mdc) for SOTA patterns.

---

## 6. SOTA Patterns for MCP Developers

### Mermaid Diagrams

Composer and Plan Mode support streaming Mermaid diagrams. Use for state machines, API flows, and multi-server orchestration.

### Debug Mode

- Agent generates hypotheses and adds instrumentation
- You reproduce the bug; agent collects runtime data
- Agent proposes a targeted fix and removes instrumentation
- Don’t manually remove logs during a Debug session

### Internal Tools

Cursor’s Agent uses internal tools (e.g. Grep/ripgrep, Read, Write). These are IDE tools, not MCP integrations; document them under Cursor/agent capabilities, not under MCP integrations.

---

---

## 7. Cloud Agents

Isolated cloud VMs for async, PR-shaped work. **Not the fleet default** — always Max Mode, MCP-heavy runs can token-bomb.

→ Full decision guide: **[CLOUD_AGENTS.md](CLOUD_AGENTS.md)** (pros/cons, billing, guardrails, decision flow)

---

## 8. Public Profiles

Shareable identity page at `cursor.com/@handle` — **not** billing profiles or multi-account switching.

→ **[PROFILES.md](PROFILES.md)** (what it is / isn't, privacy, separate work+personal workaround)

---

## 9. cursor-mcp

**cursor-mcp** (:11000) — Cursor *platform* APIs (usage/spend guardrails, cloud agents). Separate from **cursor-app-control** (IDE/Glass). Fritz: `coworker_cursor_spend_watch` every 2h.

→ Repo **`D:\Dev\repos\cursor-mcp`** · **[CURSOR_MCP_PROPOSAL.md](CURSOR_MCP_PROPOSAL.md)** · **[projects/cursor-mcp/README.md](../../projects/cursor-mcp/README.md)**

---

## 10. 2026 Regressions & Known Issues

### ⚠️ Unicode Emoji Pollution
A significant regression in early 2026: The Cursor LLM (all models) frequently inserts superfluous Unicode emojis into scripts and program code. 
- **Impact**: Breaks build pipelines and sensitive parsers.
- **Remedy**: Explicitly include "NO EMOJIS IN CODE" in `.cursor/rules/`.

### 🪟 Zen Mode Disconnect
While Cursor 3.0 introduced "Zen Mode," it often defaults to high-sycophancy interaction styles which conflict with Sandra's industrial-technical standard.

---

## 11. June 2026 releases (3.6–3.7)

SDK custom tools, auto-review, JSONL stores, nested subagents, Design Mode (browser + canvas), context usage canvas, IDE auto-review run mode.

→ **[CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md)** (fleet adoption priorities)

---

## 12. Version & Landscape

- **Cursor 3.7 (Jun 2026)**: Design Mode voice/multi-select; SDK batch; context canvas.
- **Cursor 3.6 (May 2026)**: IDE Auto-review for MCP/Shell/Fetch.
- **Cursor 3.x**: Agent delegation, cloud agents, Skills, canvases.
- **Unicode regression**: Still enforce NO EMOJIS IN CODE.
- **Antigravity IDE**: Parallel for browser/orchestration patterns; **not** a local-inference lane ([IDE matrix](../IDE_LOCAL_INFERENCE.md)).
- **Local inference**: Use **Zed + Ollama/LM Studio** — Cursor has [no native local provider](NO_LOCAL_PROVIDER.md).

---

## References

- [No local provider (Ollama/LM Studio)](NO_LOCAL_PROVIDER.md)
- [IDE local inference matrix](../IDE_LOCAL_INFERENCE.md)
- [Jun 2026 changelog digest](CHANGELOG_DIGEST_JUN_2026.md)
- [Cloud Agents (fleet guide)](CLOUD_AGENTS.md)
- [Public Profiles](PROFILES.md)
- [cursor-mcp](CURSOR_MCP_PROPOSAL.md)
- [Cursor 2.0 Blog](https://cursor.com/blog/2-0)
- [Cursor 2.0 Changelog](https://cursor.com/changelog/2-0)
- [Agent Modes](https://cursor.com/docs/agent/modes)
- [Agent Skills](https://cursor.com/docs/context/skills)
- [MCP in Cursor](https://cursor.com/docs/cookbook/building-mcp-server)
- [Agent Skills Standard](https://agentskills.io)
