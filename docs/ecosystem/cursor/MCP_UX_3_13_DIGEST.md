# Cursor MCP UX — 3.13 fleet digest (Jul 2026)

**Status:** Active (observed + partially documented)  
**Updated:** 2026-07-27  
**Observed on:** Cursor **3.13.21** (Windows)  
**Official changelog lag:** [cursor.com/changelog](https://cursor.com/changelog) last major post **2026-07-22** (Cursor Router); same-week MCP UI/approval tweaks often ship **before** release notes.

Fleet one-pager so we stop hunting Cursor’s site every patch. Not normative for MCP server code — only **host IDE behavior** that affects memops, winops, and overnight agent runs.

---

## Why this doc exists

Cursor ships small UX fixes (MCP settings, approval timeouts) on a faster cadence than public changelog posts. For a fleet with **50+ MCP servers** and multi-IDE memops, “what changed in the host?” matters as much as server semver.

**Fleet stance:** Treat **docs + this digest + installed version** as the source of truth until Cursor publishes matching release notes.

---

## Where MCP lives now (3.9+)

| Surface | Path / action |
|---------|----------------|
| **Primary UI** | Sidebar **Customize** → **MCPs** (replaces older “Settings → Features → MCP” mental model) |
| **Legacy settings** | **Cursor Settings → Tools & Integrations → MCP** (label varies by version; same underlying config) |
| **Global config** | `%USERPROFILE%\.cursor\mcp.json` |
| **Project config** | `<repo>\.cursor\mcp.json` (merged; project wins on key collision) |
| **Command palette** | “Open MCP Settings” / view MCP logs |
| **Logs** | Output panel (`Ctrl+Shift+U`) → **MCP Logs** |

**3.13 observed UX:** Click a server in the MCP list → **compact popup/detail panel** (status, tools, auth, refresh) instead of navigating a full settings sub-page. Cleaner for toggling one server without losing context.

---

## Tool approval (agent runs)

Three layers stack — do not confuse them:

| Layer | What it gates | Fleet note |
|-------|----------------|------------|
| **Run mode** | Shell, **MCP**, Fetch during agent turns | **Settings → Agents → Approvals & Execution** — default **Auto-review** since 3.6 |
| **Auto-review classifier** | Non-allowlisted / non-sandboxed calls | Steer via `~/.cursor/permissions.json` and project `.cursor/permissions.json` |
| **Per-call approval UI** | Explicit Allow / Deny on a pending tool | **3.13:** timed wait via `awaitToolCall` + **`blockUntilMs`** — if you do not respond, call **auto-approves after ~60s** (observed; prevents AFK dead runs) |

**Docs:** [Run modes](https://cursor.com/docs/agent/security/run-modes) · [MCP tool approval](https://cursor.com/docs/mcp#tool-approval) · [permissions.json](https://cursor.com/docs/reference/permissions)

**Not the same as memops `ADVANCED_MEMORY_READONLY`:** that is **single-writer DB discipline** across IDEs. See [MCP_CLIENT_CONFIG_SNIPPETS.md — memops multi-IDE](../../patterns/MCP_CLIENT_CONFIG_SNIPPETS.md#memops-multi-ide-http-daemon--stdio-proxy).

---

## Documented changelog timeline (MCP-relevant)

| Date | Version | Headline | Link |
|------|---------|----------|------|
| 2026-07-22 | — | Cursor Router (Auto cost/balance/intelligence) | [changelog](https://cursor.com/changelog) |
| 2026-07-10 | 3.11 | Side chats, agent transcript search, repo pickers | [changelog](https://cursor.com/changelog) |
| 2026-06-30 | 3.10 | Team MCPs in team marketplaces | [team-marketplace-updates](https://cursor.com/changelog/team-marketplace-updates) |
| 2026-06-22 | 3.9 | **Customize** page — plugins, skills, MCPs unified | [customize](https://cursor.com/changelog/customize) |
| 2026-05-29 | 3.6 | **Auto-review** default for Shell/MCP/Fetch | [run-modes](https://cursor.com/docs/agent/security/run-modes) |
| 2026-03-03 | 2.6 | MCP Apps; “more reliable MCP setup”; fixed stuck MCP dialogs | [2-6](https://cursor.com/changelog/2-6) |

**Gap (2026-07-27):** MCP server **click-popup** UI and **~60s approval timeout** — **observed in 3.13.21**, **not** yet on public changelog at time of writing. Update this section when Cursor posts release notes.

**Automated watch:** aiwatcher-mcp bundle **IDE Host Signal** — [AIWATCHER_IDE_HOST_SIGNAL.md](../../patterns/AIWATCHER_IDE_HOST_SIGNAL.md) (Reddit/HN/forum RSS, `changelog-gap` tagging).

Prior fleet digest: [CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md).

---

## Fleet checklist after a Cursor update

1. **Help → About** — note version (e.g. `3.13.21`).
2. **Customize → MCPs** — spot-check memops, winops, fileops: green status, popup shows expected env.
3. **Output → MCP Logs** — one failed server is enough to explain “agent stopped calling tools.”
4. **Memops:** if config changed on disk, **toggle server off/on** or restart Cursor — stale stdio env is common (`READONLY` vs writer). See [BUG_REPORT_NSSM_SPLIT_BRAIN.md](../../../advanced-memory-mcp/docs/troubleshooting/BUG_REPORT_NSSM_SPLIT_BRAIN.md).
5. **Overnight runs:** confirm **Approvals & Execution** mode; know that **silent 60s auto-approve** may run MCP you would have blocked if awake.
6. **Sync fleet memops:** `mcp-central-docs/scripts/Sync-FleetMemopsClient.ps1 -PrimaryClient cursor`

---

## How to discover features when changelog lags

| Source | Use for |
|--------|---------|
| [cursor.com/changelog](https://cursor.com/changelog) | Named releases, enterprise features |
| [cursor.com/llms.txt](https://cursor.com/llms.txt) | Full docs sitemap |
| [cursor.com/docs/mcp](https://cursor.com/docs/mcp) | Config, OAuth, enterprise MCP policy |
| Installed `product.json` → `version` | Ground truth vs web |
| This digest | Fleet-observed host behavior between posts |

---

## Risks (unchanged)

- **Auto-approve after timeout** ≠ security review — high-risk tools (shell, winops) still deserve periodic allowlist / `block_instructions` in `permissions.json`.
- **Changelog lag** → agents and humans assume “no notes = no change” — wrong for MCP UX patches.
- **50+ MCP catalog** + Auto-review + nested subagents → monitor spend; use context canvas / trim enabled servers per task.

---

## References

- [ecosystem/cursor/README.md](README.md)
- [MCP_CLIENT_CONFIG_SNIPPETS.md](../../patterns/MCP_CLIENT_CONFIG_SNIPPETS.md)
- [CHANGELOG_DIGEST_JUN_2026.md](CHANGELOG_DIGEST_JUN_2026.md)
- [cursor.com/help/customization/mcp](https://cursor.com/help/customization/mcp)
