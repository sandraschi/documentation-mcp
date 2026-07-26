# Session Context Injection (SOTA 2026)

**Established**: 2026-07-02
**Reference impl**: `advanced-memory-mcp` — `.claude-plugin/`, `hooks/hooks.json`, `skills/advanced-memory/agentic-zettelkasten/SKILL.md`
**Inspiration**: `iamtouchskyer/memex` — Claude Code plugin + SessionStart hooks pattern

## Problem

AI coding agents forget what MCP tools are available between sessions. A user
connects `arxiv-mcp`, `email-mcp`, `plex-mcp`, and `advanced-memory-mcp` to
Claude Desktop — but on the next session, the agent doesn't know they exist
unless prompted. The user has to manually remind the agent: "you can search my
email" or "check my notes from last session."

This is the **session amnesia problem**: MCP tool registration persists across
sessions, but tool *awareness* does not. The agent won't use tools it doesn't
remember are available.

## Solution

Inject a short **tool-awareness prompt** at session start through each IDE's
native injection channel. The content is identical across IDEs — a 10-15 line
summary of what the server does and the 1-2 most important discovery calls.
Only the delivery mechanism differs.

## Channel Matrix

| IDE | Injection channel | File | Format | Auto-loaded? |
|-----|------------------|------|--------|-------------|
| **Claude Code** | Plugin hooks | `.claude-plugin/plugin.json` + `hooks/hooks.json` | JSON `SessionStart` hook with `type: "text"` | Yes — every session |
| **Cursor** | Cursor rules | `.cursorrules` | Markdown appended as system prompt | Yes — every session |
| **Windsurf** | Windsurf rules | `.windsurfrules` | Same as `.cursorrules` | Yes — every session |
| **Antigravity** | Agent skills | `.agents/skills/<name>/SKILL.md` | Skill loaded on demand via `config.json` | Optional (user toggles) |
| **GitHub Copilot** | Custom instructions | `.github/copilot-instructions.md` | Markdown | Yes — every session |
| **OpenCode** | Agent skills | `.opencode/skills/<name>/SKILL.md` | Markdown skill loaded on-demand via `skill()` tool | No — listed in `<available_skills>`, agent calls `skill({name: "..."})` when needed |
| **OpenCode** (alt) | Config references | `opencode.jsonc` `references` section | JSON array with description + autocomplete | Yes — every session |

## The Prompt Template

Every server's injection prompt follows this structure:

```
## <Server Display Name>

<1-sentence elevator pitch — what the server DOES>

**Before starting work, <domain-specific recall action>:**
1. <primary discovery call with tool name and args>
2. <secondary check or status call>

**At end of work, <domain-specific save action>:**
- <how to persist insights, close loops, or clean up>
```

### Principles

1. **Keep it under 15 lines.** The agent's context is finite. Don't recite the full tool list.
2. **Give concrete tool calls, not abstract advice.** `adn_nav(operation="recent", timeframe="7d")` not "check what you worked on recently."
3. **Domain-tailor the recall action.** A research server recalls papers, a media server searches the library, a memory server checks recent notes.
4. **Include the save action.** The close-of-work pattern is just as important as the open.

### Examples

**Memory server** (`advanced-memory-mcp`):
```
## Session Context (Advanced Memory)

You have access to a persistent knowledge graph with 79 tools.
Your memory persists across sessions.

**Before starting work:**
1. Check recent activity: adn_nav(operation="recent", timeframe="7d")
2. Semantic search for task context: adn_search(operation="rag", prompt="<describe task>")

**At end of work, save insights:**
- Use the agentic-zettelkasten skill for structured capture
- Always embed [[wikilinks]] in sentences explaining the relationship
```

**Research server** (`arxiv-mcp`):
```
## Session Context (arXiv Research)

You have access to arXiv paper search, full-text extraction, and Semantic Scholar
citation graphs. 20+ tools for academic research.

**Before starting work:**
1. Search for relevant papers: search_papers(query="<topic>", limit=10)
2. Check category recents: getRecent(category="cs.AI", count=10)

**At end of work, save findings:**
- Ingest key papers to corpus: ingest_paper_to_corpus(paper_id="...")
- Store to Calibre for offline reading: store_paper_to_calibre(paper_id="...")
```

**Email server** (`email-mcp`):
```
## Session Context (Email MCP)

You can read, search, send, and manage email across IMAP accounts.

**Before starting work:**
1. Check recent inbox: list_emails(folder="INBOX", limit=10, sort="date_desc")
2. Search for task-relevant threads: search_emails(query="<project name>")

**At end of work:**
- Draft and send any emails the user asked for
- Mark relevant messages as read/starred
```

## Reference Implementation

See `advanced-memory-mcp` for the complete multi-channel setup:

```
advanced-memory-mcp/
├── .claude-plugin/
│   └── plugin.json              # Claude Code extension manifest
├── hooks/
│   └── hooks.json               # SessionStart text injection
├── .cursorrules                 # Cursor rules (includes tool-awareness)
├── .windsurfrules               # Windsurf rules (symlink or copy of .cursorrules)
└── skills/advanced-memory/
    └── agentic-zettelkasten/
        └── SKILL.md             # Structured Zettelkasten protocol
```

The `skills/` directory is optional but RECOMMENDED for servers with complex
workflows that benefit from step-by-step guidance (Zettelkasten create-vs-update
decisions, paper ingestion pipelines, multi-step email workflows).

## Per-IDE Implementation Notes

### Claude Code

Claude Code reads `.claude-plugin/plugin.json` from the workspace root.
The `hooks` field points to `hooks/hooks.json`, which defines a `SessionStart`
hook with `type: "text"` containing the injection prompt.

```json
// .claude-plugin/plugin.json
{
  "name": "repo-name",
  "version": "0.1.0",
  "description": "...",
  "hooks": "../hooks/hooks.json"
}

// hooks/hooks.json
{
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "text",
        "text": "## Session Context\n\n..."
      }]
    }]
  }
}
```

### Cursor

Cursor reads `.cursorrules` from the workspace root and appends it as a system
instruction on every session. Append the tool-awareness prompt at the bottom
of the existing `.cursorrules` (don't replace existing rules).

### Windsurf

Windsurf reads `.windsurfrules`. The format is identical to `.cursorrules`.
If the repo already has `.cursorrules`, `.windsurfrules` can be a copy.

### Antigravity

Antigravity uses `.agents/skills/` with `config.json` for auto-loading.
Create a `session-start/SKILL.md` skill and add it to `config.json`'s
auto-load list.

```json
// .agents/skills/config.json
{
  "auto_load": ["session-start"],
  "skills": { ... }
}
```

### GitHub Copilot

Create `.github/copilot-instructions.md` with the prompt text. Copilot reads
this file from the repo root or from the GitHub organization settings.

### OpenCode

OpenCode reads skills from `.opencode/skills/<name>/SKILL.md`. The agent sees available skills in `<available_skills>` and loads one via `skill({name: "..."})` when the task matches. **Skills are NOT auto-injected** — the agent must decide to load them.

Required YAML frontmatter in `SKILL.md`:
```yaml
---
name: session-context       # must match directory name, lowercase with hyphens
description: "..."          # shown to agent in available_skills list
---
```

Example:
```markdown
---
name: session-context
description: Lightweight arXiv session start prompt
---

## Session Context (arXiv Research)
...
```

**Important:** OpenCode's `opencode.json` `instructions` field takes an **array of file paths** (not inline text). Do NOT use it for inline session injection — use `.opencode/skills/` instead.

## Fleet Rollout Strategy

| Phase | Scope | Repos |
|-------|-------|-------|
| **Phase 1 — Canary** | `advanced-memory-mcp` | Prove the pattern with all 3 text-injection channels |
| **Phase 2 — Research & dev** | `arxiv-mcp`, `git-github-mcp`, `email-mcp` | Highest session-start value |
| **Phase 3 — Media** | `plex-mcp`, `calibre-mcp`, `bookmarks-mcp` | Media library awareness |
| **Phase 4 — All user-facing MCP** | Every repo with MCP tools | Mechanical rollout |

**Skip**: infrastructure repos (`depot-mcp`, `fleet-agent-mcp`, `monitoring-mcp`),
host-app wrappers where the host must be open (`blender-mcp`, `gimp-mcp`),
and repos with no Claude/Cursor integration path.

## Anti-Patterns

- **Over-injection**: Listing all 79 tools in the prompt. Keep it to the 1-2 most
  useful discovery calls. The agent discovers other tools organically.
- **Stale prompts**: The injection text hardcodes tool names. If tools are renamed,
  the injection text goes stale. Audit after any tool rename.
- **Duplicate channels**: Don't inject the same content through both `.cursorrules`
  AND `.claude-plugin` if the IDE itself uses both. Claude Code uses only
  `.claude-plugin`. Cursor uses `.cursorrules`.
- **No close-of-work hook**: The session-start injection is only half the value.
  The skill/workflow for saving insights is the other half. Always include both.
