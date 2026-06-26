# Cursor Changelog Digest — June 2026

**Status:** Active  
**Updated:** 2026-06-06  
**Source:** [cursor.com/changelog](https://cursor.com/changelog)  
**Prior digest:** [CURSOR_V3_UPGRADE_APR_2026.md](../../integrations/cursor-ide/CURSOR_V3_UPGRADE_APR_2026.md)

Fleet-focused summary of releases **3.6 (May 29)** through **3.7 (Jun 5, 2026)**. What to adopt, what to watch, what to wire into **cursor-mcp** and Fritz.

---

## Timeline

| Date | Version | Headline |
|------|---------|----------|
| May 29 | 3.6 | IDE **Auto-review** run mode (Shell, MCP, Fetch) |
| Jun 3 | — | **Enterprise Organizations** — multi-team spend rollup |
| Jun 4 | 3.7 | **SDK batch** — custom tools, auto-review, JSONL stores, nested subagents |
| Jun 4 | 3.7 | **Canvases** — Design Mode, **context usage report** |
| Jun 5 | 3.7 | **Design Mode in browser** — multi-select, voice while agent runs |

---

## 1. SDK / API (Jun 4) — adopt first

### Custom tools (`local.customTools`)

Pass function definitions on `Agent.create()` or per `send()`. SDK exposes them via built-in MCP server **`custom-user-tools`**. Subagents inherit parent custom tools.

**Fleet stance:** Use for **thin glue** (one function, no server). Keep **FastMCP fleet servers** for portmanteau tools, concurrency safety, and HTTP `/mcp` for Fritz.

### Auto-review (`local.autoReview`)

Headless SDK runs can route tool calls through a classifier instead of auto-executing everything. Steer via `permissions.json`:

```json
{
  "autoRun": {
    "allow_instructions": [
      "Read-only inspections under ./dist are fine."
    ],
    "block_instructions": [
      "Always pause delete operations."
    ]
  }
}
```

**Fleet stance:** Required pattern for Fritz/CI SDK scripts touching `fileops`, `docker-mcp`, `git-github`.

### Persistence — JSONL and custom stores

- `JsonlLocalAgentStore` — append-only, diffable, VCS-friendly
- Implement `LocalAgentStore` — Postgres, in-memory CI, etc.
- Python bridge: host / JSONL / composed JSONL stores

**Fleet stance:** JSONL for local experiment logs; Postgres only if agent state must live beside app DB.

### Nested subagents

Subagents spawn subagents automatically (reviewer → test-writer → …). No feature flag.

**Fleet stance:** Prefer over hand-rolled Fritz chains for **single-repo** deep tasks; keep Fritz YAML for **cross-MCP** fleet flows.

### Reliability and ops

| Item | Fleet use |
|------|-----------|
| **`requestId` on every `send()`** | Correlate spend, logs, support — wire into cursor-mcp phase 2 |
| **Reliable `wait()` on local runs** | CI scripts can trust terminal `RunResult` |
| **Cloud streaming on HTTP/1.1** | Proxies / older CI images |
| **Lighter `@cursor/sdk` import** | Cloud-only scripts skip local stack until needed |
| **Workspace-scoped `list_runs` (Python)** | Fixes cwd mismatch in subprocess bridges |
| **Composer 2 → 2.5 auto-route** | Legacy scripts stay on cheaper model |

**Upgrade:** `npm install @cursor/sdk` · `pip install cursor-sdk` (Python 0.1.6+)

---

## 2. Design Mode and Canvases (Jun 4–5)

### Browser Design Mode (Jun 5)

- Multi-select DOM elements — agent sees code + layout relationships
- **Voice input** while agent is mid-run — queue next change without waiting

**Fleet stance:** Primary path for **wrapper webapp** UIs (plex, godot, jellyfin dashboards). Complements Playwright MCP; less prose, more point-and-fix.

### Canvas Design Mode + context report (Jun 4)

- Annotate UI inside **canvases** (same interaction model as browser)
- **Context usage report** canvas — breakdown of tokens: system prompt, tools, rules, skills
- **Debug with Agent** button — new chat to trim context bloat
- Canvas share fullscreen, embedded prompt buttons, chart styling

**Fleet stance:** Run context report **before** enabling more MCPs in a heavy session. Overlaps fleet [canvas skill](../../../integrations/huashu-design-skill.md) and Cursor native canvases — use native for token diagnostics; Huashu for hi-fi HTML prototypes.

---

## 3. IDE Auto-review (3.6, May 29)

Settings → Agents → **Run Mode → Auto-review**. Classifier for Shell, **MCP**, Fetch: allowlist → sandbox → hold for approval.

**Fleet stance:** Turn on for daily IDE work with 50+ MCP servers. Block destructive portmanteau ops in classifier instructions (mirrors SDK `permissions.json`).

---

## 4. Enterprise Organizations (Jun 3)

Org → Teams → **Groups** with separate spend limits, model access, agent permissions. Org-level usage analytics and spend rollup.

**Fleet stance:** Relevant if Sandra moves to Teams/Enterprise — **cursor-mcp** `CURSOR_ADMIN_API_KEY` could target org rollup APIs. Solo Pro: dashboard + `alert_check` only.

---

## Fleet adoption priority

| Priority | Action |
|----------|--------|
| **P0** | IDE Auto-review + context usage canvas before big agent sessions |
| **P0** | Keep `coworker_cursor_spend_watch` on 2h schedule |
| **P1** | SDK scripts: `local.autoReview` + `permissions.json` for headless runs |
| **P1** | Design Mode for webapp wrapper repos |
| **P2** | `local.customTools` for one-off glue; not a replacement for fleet MCPs |
| **P2** | JSONL store for SDK experiment logs |
| **P3** | Nested subagents inside single-repo SDK jobs |
| **P3** | Enterprise org APIs when/if on Teams plan |

---

## cursor-mcp alignment (v0.1.1+)

| Tool | Jun 2026 coverage |
|------|-------------------|
| `cursor_usage` | Spend guardrails (unchanged) |
| `cursor_cloud` | Cloud agent monitor (unchanged) |
| `cursor_docs` | Topics: `sdk-jun-2026`, `design-mode`, `auto-review`, `context-canvas` |
| `cursor_sdk` | `capabilities`, `autoreview_template`, `custom_tools_guide`, `upgrade_notes` |

Phase 2 backlog: log `requestId` from Cloud Agents API runs; gated `cloud.start` with pre-flight `alert_check`.

---

## Risks unchanged

- **Token bombs:** More subagents + Design Mode loops + MCP catalog = still monitor spend
- **Concurrency:** Parallel agents (v3) + nested subagents → FastMCP 3.2+ locking mandatory
- **Unicode emoji regression:** Still enforce NO EMOJIS IN CODE in rules

---

## References

- [Changelog](https://cursor.com/changelog)
- [TypeScript SDK](https://cursor.com/docs/sdk/typescript)
- [Python SDK](https://cursor.com/docs/sdk/python)
- [CLOUD_AGENTS.md](CLOUD_AGENTS.md)
- [cursor-mcp](../../projects/cursor-mcp/README.md)
- [Huashu Design skill](../../integrations/huashu-design-skill.md)
