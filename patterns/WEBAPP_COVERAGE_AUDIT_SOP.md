# Webapp Coverage Audit - SOP

**Trigger**: `webapp coverage`, `coverage audit`, `gap fill`
**Scope**: Single repo. Map every backend capability (MCP tools, REST routes)
against what the webapp actually calls, then fill the gaps in phases.
**Pilot**: system-admin-mcp (2026-10-08) — found 5 orphaned endpoints + 9
unsurfaced tool groups; Phase 1 shipped metrics card, install flow, legacy
decisions. Nearly all fleet repos have the same shape of drift (backend grows
via MCP tools, webapp lags), so run this SOP per repo after assfix.

---

## Why this exists

assfix checks that a webapp *exists and meets the SOTA layout*. It does not
check that the webapp *covers the backend*. Backends grow operation by
operation (each new `@mcp.tool` + REST route), while pages are added rarely —
so coverage rots silently. The generic Tools page (run-any-tool-by-name) masks
it: everything is technically reachable, nothing is actually surfaced. This
SOP makes the rot visible and fills it in priority order.

**Rule**: audit is read-only. Fill in severity phases, never all at once.

---

## Phase 1 — Enumerate backend surface (read-only)

MCP tools (names only):

```powershell
Get-ChildItem <repo>/src -Recurse -Filter *.py |
  Select-String -Pattern "@mcp\.tool" -Context 0,1
```

REST routes (method + path):

```powershell
Select-String -Path <repo>/src/*/.../server.py -Pattern '@app\.(get|post|delete)\("([^"]+)"'
# plus any module that calls register_*_routes(app) — grep for it
```

Portmanteau ops (the `Literal[...]` list — each op is a capability):

```powershell
Select-String -Path <repo>/src/.../portmanteau.py -Pattern '"[a-z_]+",$'  # adapt per file
```

Output: three lists (tools, routes, ops).

## Phase 2 — Enumerate webapp usage (read-only)

Every backend URL the frontend touches, per file:

```powershell
Get-ChildItem <repo>/web_sota/src -Recurse -Include *.tsx,*.ts |
  Select-String -Pattern '/api/[a-z0-9_/{}-]+'
```

Plus: tool names passed to `/api/tools/call`, and portmanteau `operation:`
literals invoked from pages. Output: route → pages map.

## Phase 3 — Diff and classify

Build the matrix. Typical classes (system-admin-mcp findings in parens):

| Class | Meaning | Example |
|---|---|---|
| Orphaned endpoint | Route with zero callers | `GET /api/metrics`, legacy `/api/chat` |
| Unsurfaced op | Portmanteau op reachable only via generic runner | `disk_cleanup`, `set_permissions` |
| Read-only page, mutating backend | Page lists but can't act | services list without start/stop |
| Test-only endpoint | Intentionally UI-less | `/api/v1/diagnostics` (CUA smoke) |
| Dead contract | Endpoint the frontend migrated away from | decide keep-documented vs delete |

Score it like assfix: HIGH = orphaned mutation endpoints / dead contracts in
critical paths; MEDIUM = unsurfaced read ops; LOW = doc-only gaps.

## Phase 4 — Fill in phases (the fix order that worked)

1. **Visibility, zero mutations**: metrics/status cards, install/onboarding
   flows, keep-vs-delete decisions on dead contracts (with tests pinning the
   decision either way).
2. **Read-only sections**: one page section per uncovered GET group.
3. **Mutations with confirmations**: dry-run-first where the tool supports it,
   confirm dialogs, admin gates; one backend POST route per mutation
   (existing `_run_tool` pattern), then UI, then tests.
4. **New surfaces**: pages for whole subsystems (watches, agentic triggers),
   shutdown/danger-zone patterns.

Per phase: backend route → UI → pytest for route → e2e where pages change →
≤5-file commits → push. Never mix phases in one commit.

## Gotchas (paid for on the pilot)

- The pre-commit stash vs whole-tree hooks trap: stage ALL webapp fixes
  before splitting commits, or hooks scan reverted files (see assfix report
  2026-10-07 follow-up §3).
- `biome ci .` covers `e2e/` and config files, not just `src/` — a broken
  spec or CRLF config fails the hook, not the page code.
- `just --list` / `actionlint` / `tsc -b` (not just `--noEmit`) each catch
  things the others miss; run all four.
- Legacy endpoints: deleting breaks unknown external clients; keeping
  without a test rots. Pin with a contract test either way.
