# Fleet Drift Scan — SOP

**Trigger**: `drift`
**Reference macro**: `agentic_macros.md` → `drift`
**Scope**: Read-only fleet-wide gap analysis. Compare every repo against the current SOP checklist without fixing anything.

---

## Why drift

assfix fixes one repo at a time. drift tells you **which** repos need fixing and **how badly**. It's the fleet-wide triage tool — run it before planning an assfix campaign to prioritise the worst offenders.

**Rule**: Never fix anything during a drift scan. If you find a gap, note it. Do not touch files.

---

## Phase 1 — Enumerate repos

Scan `D:\Dev\repos\` for genuine project repos:

```powershell
Get-ChildItem D:\Dev\repos -Directory | Where-Object {
    $_.Name -notmatch '^[._]' -and
    (Test-Path (Join-Path $_.FullName "pyproject.toml") -PathType Leaf)
} | Sort-Object Name
```

Skip hidden dirs, build dirs, temp dirs, and `mcp-central-docs` itself (it's the hub, not a server). Output: list of repo names. If >50 repos, sample every 3rd for a quick scan (flag as "sampled" in report).

---

## Phase 2 — Per-repo probes

For each repo, run these lightweight probes. **Do not run `ruff`, `pytest`, or any command that modifies files or takes >10s.**

| Probe | What to check | How | Severity if missing |
|-------|--------------|-----|--------------------|
| **assfix timestamp** | `.assess-fix-timestamp` exists? How old? | `Get-Content .assess-fix-timestamp | ConvertFrom-Json` | HIGH if >30 days or missing |
| **Required files** | `justfile`, `llms.txt`, `llms-full.txt`, `glama.json`, `start.ps1` | `Test-Path` each | MEDIUM per missing |
| **Port registration** | Repo has an entry in `WEBAPP_PORTS.md`? | `rg "{repo-name}" mcp-central-docs/operations/WEBAPP_PORTS.md` | HIGH if missing |
| **CLAUDE.md** | Exists? Non-empty? | `Test-Path CLAUDE.md` | MEDIUM if missing |
| **.gitignore** | Has `.venv/`, `node_modules/`, `__pycache__/`? | `rg ".venv" .gitignore` | LOW per missing pattern |
| **Cursor rules** | `.cursorrules` exists? Has Session Context section? | `rg "## Session Context" .cursorrules` | MEDIUM if missing |
| **Claude plugin** | `.claude-plugin/plugin.json` + `hooks/hooks.json` exist? | `Test-Path .claude-plugin/plugin.json` | MEDIUM if missing |
| **Webapp** | `webapp/` or `web_sota/` exists? | `Test-Path webapp/package.json` | INFO |
| **Tauri** | `native/` exists? | `Test-Path native/Cargo.toml` | INFO |
| **Docker** | `docker-compose.yml` exists? | `Test-Path docker-compose.yml` | INFO |

---

## Phase 3 — Aggregate

Build a report table:

```
| Repo | Assessed | Files | Port | CLAUDE | Gitign | Cursor | Plugin | Webapp | Tauri | Docker | Score |
|------|----------|-------|------|--------|--------|--------|--------|--------|-------|--------|-------|
| arxiv-mcp | 2026-07-18 | 5/5 | ok | ok | ok | ok | ok | yes | no | no | 92 |
| calibre-mcp | none | 3/5 | ok | ok | ok | missing | missing | yes | no | no | 65 |
| ...

Summary: X repos scanned, Y pass (>=80), Z need work (60-79), W runt (<60).
```

---

## Phase 4 — Persist report

Write the aggregate report to `reports/drift-{YYYY-MM-DD}.md` (in the mcp-central-docs repo, since drift is fleet-wide):

```powershell
$reportDir = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$reportPath = Join-Path $reportDir "drift-$(Get-Date -Format 'yyyy-MM-dd').md"
Set-Content -Path $reportPath -Value $reportTable
```

Also write `.drift-timestamp` at mcp-central-docs root (committed) with a summary:

```powershell
@{ timestamp = (Get-Date -Format "o"); repos_scanned = $total; pass_rate = $passRate; scored_repos = $scoredCount } | ConvertTo-Json | Set-Content ".drift-timestamp"
```

The `reports/` directory MUST be in `.gitignore`. Check before writing.

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Fixing during scan** | You lose the ability to measure improvement — before and after are the same |
| **Deep probes** | Running `ruff`, `pytest`, or `tsc` on 50 repos takes hours. Keep it to file existence checks |
| **Incomplete sampling** | If you sample, say so. An unsampled report that skipped half the fleet is misleading |
| **No timestamp** | Without the scan date, you can't tell if the data is fresh or from last month |
