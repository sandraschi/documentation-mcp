# cursor-mcp

**Type:** MCP Server  
**Status:** Active — v0.1.1  
**Ports:** HTTP **11000** (`/mcp`) · stdio for Cursor IDE  
**Repo:** `D:\Dev\repos\cursor-mcp`  
**Last updated:** 2026-06-06

---

## Description

FastMCP server for Cursor **platform APIs**: usage/spend guardrails (`cursor_usage alert_check`), cloud agent monitoring, fleet doc snippets. Replaces manual dashboard anxiety checks.

Complements **cursor-app-control** (IDE/Glass). See [CURSOR_MCP_PROPOSAL.md](../../ecosystem/cursor/CURSOR_MCP_PROPOSAL.md).

---

## Fritz integration

| Flow | Recurrence | Tool |
|------|------------|------|
| Cursor Spend Watch | `2h` | `coworker_cursor_spend_watch` |

Emails on **warn** / **critical** only. [FRITZ_INTEGRATION.md](https://github.com/sandraschi/cursor-mcp/blob/main/docs/FRITZ_INTEGRATION.md) in repo.

---

## Auth

| Env | Purpose |
|-----|---------|
| `CURSOR_API_KEY` | `/v1/me`, `/v1/agents` |
| `CURSOR_ADMIN_API_KEY` | `/teams/spend`, usage events (Teams admin key) |

---

## Tools (v0.1.1)

| Tool | Role |
|------|------|
| `cursor_usage` | Spend guardrails (`alert_check`) |
| `cursor_cloud` | Cloud agent monitor |
| `cursor_docs` | Fleet snippets incl. Jun 2026 topics |
| `cursor_sdk` | SDK guidance — customTools, autoReview, stores |

## Related

- [CHANGELOG_DIGEST_JUN_2026.md](../../ecosystem/cursor/CHANGELOG_DIGEST_JUN_2026.md)
- [CLOUD_AGENTS.md](../../ecosystem/cursor/CLOUD_AGENTS.md)
- [PROFILES.md](../../ecosystem/cursor/PROFILES.md)
- [fritz-coworker](../fritz-coworker/README.md)
