# cursor-mcp — Fleet Proposal

**Status:** Active — v0.1.1 (`D:\Dev\repos\cursor-mcp`)  
**Updated:** 2026-06-06  
**Changelog digest:** [CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md)
**Motivation:** Cursor platform surface (agents, usage, cloud, SDK) is growing; MCD cursor docs are expanding; fleet already has **cursor-app-control** for IDE chrome only.

---

## Problem

Today Cursor knowledge and automation are split:

| Surface | Where it lives today |
|---------|---------------------|
| IDE workspace control | **cursor-app-control** MCP (move agent, open resource, automations UI) |
| Cursor docs | `mcp-central-docs/ecosystem/cursor/` |
| Cloud Agents / SDK | Cursor REST API, `@cursor/sdk`, dashboard |
| MCP config | `~/.cursor/mcp.json`, `MASTER_MCP_CONFIG.json` |
| Rules / skills | Per-repo + global, no fleet query API |

Agents in Claude Desktop or other clients cannot ask "what is my Cursor usage?", "start a cloud agent on repo X", or "list my cloud agent runs" without ad-hoc scripts.

---

## Proposal: `cursor-mcp`

FastMCP server wrapping **Cursor platform APIs** (not the IDE UI). Thin portmanteau over official endpoints where they exist; read-only first.

### Phase 1 — Read-only (safe) — shipped v0.1.x

| Tool group | Examples |
|------------|----------|
| **Account / usage** | `cursor_usage`: summary, spend, events, alert_check, limits |
| **Cloud agents** | `cursor_cloud`: list, status, runs, cancel |
| **Docs cache** | `cursor_docs`: cloud-agents, profiles, sdk-jun-2026, design-mode, auto-review, context-canvas |
| **SDK guidance** | `cursor_sdk`: capabilities, autoreview_template, custom_tools_guide (Jun 2026) |
| **Fritz** | `coworker_cursor_spend_watch` every 2h |

### Phase 2 — Write (gated)

| Tool group | Examples |
|------------|----------|
| **Cloud agents** | Start agent with bounded prompt + model + pre-flight `alert_check` |
| **Run correlation** | Log Cloud Agents API `requestId` alongside spend snapshots |
| **Profile** | Read public profile metadata (not claim handle — human-only) |
| **Config assist** | Diff local `mcp.json` vs `MASTER_MCP_CONFIG.json` (no auto-write) |

### Explicit non-goals

- Replace **cursor-app-control** (IDE focus, Glass, workspace moves)
- Replace **meta-mcp** (fleet server lifecycle)
- Auto-edit user rules or billing without confirmation
- Bypass spend limits or on-demand billing gates

---

## Overlap with cursor-app-control

```
┌─────────────────────┐     ┌─────────────────────┐
│  cursor-app-control │     │     cursor-mcp      │
│  (IDE / Glass)      │     │  (platform API)     │
├─────────────────────┤     ├─────────────────────┤
│ move_agent_to_root  │     │ cloud_agent_list    │
│ open_resource       │     │ cloud_agent_start   │
│ open_automation     │     │ usage_get           │
│ rename_chat         │     │ agent_run_status    │
│ create_project      │     │ docs_cursor_topic   │
└─────────────────────┘     └─────────────────────┘
         │                            │
         └──────── Cursor product ────┘
```

Keep both: different trust boundaries and callers.

---

## Auth

- User API key from [cursor.com/dashboard/integrations](https://cursor.com/dashboard/integrations)
- Env: `CURSOR_API_KEY` (same as SDK)
- Never commit keys; document in `projects/cursor-mcp/` only

---

## When to build

| Signal | Action |
|--------|--------|
| Manual cloud agent + usage checks ≥ 3×/week | Scaffold repo from `mcp-server-template` |
| SDK automation in CI already | Extract shared client into `cursor-mcp` |
| Docs-only needs | Stay in `ecosystem/cursor/` (current) |

---

## Repo stub

Fleet project page (planned): [projects/cursor-mcp/README.md](../../projects/cursor-mcp/README.md)

---

## References

- [CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md)
- [Cursor changelog](https://cursor.com/changelog)
- [Cursor SDK](https://cursor.com/docs/sdk/typescript)
- [Cloud Agents API](https://cursor.com/docs/cloud-agent/api/endpoints)
- [CLOUD_AGENTS.md](CLOUD_AGENTS.md)
- [PROFILES.md](PROFILES.md)
