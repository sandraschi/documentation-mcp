# Cursor IDE — MCP Client Reference

**Last Updated:** June 6, 2026
**Cursor version:** 3.0 (Pro)
**MCP config:** `C:\Users\sandr\.cursor\mcp.json`
**Global rules:** `.cursor/rules/` per-repo or Cursor Settings → Rules

---

## What Cursor Is (as MCP client)

Cursor is an AI-first code editor (VS Code fork) and one of our three primary MCP clients alongside Claude Desktop and Antigravity. Its MCP implementation is more IDE-oriented than Claude Desktop — tools are invoked by the agent during coding tasks, not conversationally.

Key differences from Claude Desktop:
- MCP tools available to the Composer/Agent panel, not the chat sidebar
- Tool calls happen inline during code generation — less visible to the user
- No red error overlay in the UI (errors appear in the agent output pane)
- Context window is shared between code context and tool results
- Multi-workspace setups require explicit shell context management (see `standards/CURSOR_RULES.md`)

---

## MCP Config File

Location: `C:\Users\sandr\.cursor\mcp.json`

Same JSON structure as Claude Desktop:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "python",
      "args": ["D:\\Dev\\repos\\my-server\\server.py"]
    }
  }
}
```

**Sync with master config:** `D:\Dev\repos\mcp-central-docs\operations\MASTER_MCP_CONFIG.json`

---

## CodeMode / tool_search in Cursor

Cursor handles CodeMode the same way Claude Desktop does — it calls `tool_search` before
using tools on a CodeMode server. The difference is how it surfaces:

- **Claude Desktop:** `tool_search` call is visible in the chat window as a tool use block
- **Cursor:** `tool_search` call appears in the Composer/Agent output, less prominent

The underlying mechanism is identical — see `fastmcp/code-mode.md` for the full explanation.
The friction reduction is the same: Cursor doesn't load 200+ tool schemas into its code
context at session start.

**Historical note:** Before CodeMode was common, large MCP servers in Cursor would cause
visible slowdowns and occasional context overflow errors during long coding sessions.
The portmanteau + CodeMode approach eliminates this.

---

## Multi-Workspace Shell Context Rule

From `standards/CURSOR_RULES.md` — mandatory for multi-repo workspaces:

> When switching to work on a different repo in a multi-workspace setup:
> 1. Start a fresh shell (don't reuse existing terminals from other repos)
> 2. Always `cd` to the target repo root as the first command
> 3. Verify `Get-Location` shows correct directory before running other commands

Add to `.cursor/rules/` or Cursor global rules settings.

---

## Cursor-Specific `.cursorrules` / Rules

Cursor supports per-repo rules in `.cursor/rules/*.mdc` files (MDC format).
These are injected into the agent context automatically when working in that repo.

Our fleet standard: each MCP server repo has a `.cursor/rules/` directory with:
- `server-standards.mdc` — FastMCP patterns, portmanteau structure, import rules
- `windows-shell.mdc` — PowerShell rules, path handling

Global user rules (applies to all repos): Cursor Settings → Rules → User Rules

---

## Global agent skills (Huashu Design)

For **design and prototype** workflows driven from plain language (HTML prototypes, Playwright smoke checks, deck/motion export patterns), the fleet documents **Huashu Design** as an optional **global** client skill—not an MCP server. Install and trust notes: [../huashu-design-skill.md](../huashu-design-skill.md).

---

## Known Cursor MCP Quirks

| Issue | Workaround |
|-------|-----------|
| Agent reuses wrong shell after workspace switch | Always open fresh terminal, `cd` explicitly |
| MCP server not picked up after config edit | Restart Cursor (no hot-reload) |
| Large tool catalogs slow agent response | Use portmanteau or CodeMode servers |
| Tool call errors not surfaced clearly | Check `.cursor/logs/` or agent output pane |
| Path confusion in multi-workspace | Full absolute paths in all MCP args |

---

## Cloud Agents

Async agents in cloud VMs (GitHub `@cursor`, Slack, Linear, API). Draw from included API pool first; always Max Mode; token-bomb risk with parallel runs and large MCP fleets.

→ Fleet decision guide: **[ecosystem/cursor/CLOUD_AGENTS.md](../../ecosystem/cursor/CLOUD_AGENTS.md)**

## Public Profiles

Shareable page at `cursor.com/@handle` (usage charts, links). Not billing or account switching.

→ **[ecosystem/cursor/PROFILES.md](../../ecosystem/cursor/PROFILES.md)**

## cursor-mcp (proposed)

Platform API MCP (cloud agents, usage) — distinct from **cursor-app-control** (IDE). Not built yet.

→ **[ecosystem/cursor/CURSOR_MCP_PROPOSAL.md](../../ecosystem/cursor/CURSOR_MCP_PROPOSAL.md)**

---

## Relevant Docs

- **[Cloud Agents (fleet guide)](../../ecosystem/cursor/CLOUD_AGENTS.md)** — When to use cloud vs local; billing; token-bomb guardrails
- **[Public Profiles](../../ecosystem/cursor/PROFILES.md)** — `cursor.com/@handle`; not multi-account billing
- **[cursor-mcp proposal](../../ecosystem/cursor/CURSOR_MCP_PROPOSAL.md)** — Planned platform API server
- **[Huashu Design (global skill)](../huashu-design-skill.md)** — Optional HTML/design agent skill (not MCP)
- **[CHANGELOG_DIGEST_JUN_2026.md](../../ecosystem/cursor/CHANGELOG_DIGEST_JUN_2026.md)** — Jun 2026 SDK, Design Mode, context canvas, auto-review
- **[CURSOR_V3_UPGRADE_APR_2026.md](CURSOR_V3_UPGRADE_APR_2026.md)** — Apr 2026 v3 release analysis
- Master MCP config: `operations/MASTER_MCP_CONFIG.json`
- Multi-workspace shell rule: `standards/CURSOR_RULES.md`
- CodeMode / tool_search: `fastmcp/code-mode.md`
- Claude Desktop comparison: `integrations/claude-desktop/README.md`
- Antigravity IDE: `integrations/antigravity-ide/README.md`
