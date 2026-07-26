# Agentic Macro Operations (SOTA 2026)

**Established**: 2026-07-02

Certain user utterances should expand to a defined set of operations rather than a literal single action. This prevents gaps where the agent does the bare minimum of what was said rather than what was intended.

## Repo Discovery (Read Before Any Subagent Task)

**Subagents exploring a repo MUST run `patterns/REPO_DISCOVERY_SOP.md` first** to locate the actual source root. The fleet has two layouts: `src/{package}/` (standard) and `{package}/` at root (legacy flat). A subagent checking only `src/` will falsely report flat-layout repos as "empty scaffold."

## SOP Chaining Convention

SOPs live in `mcp-central-docs/patterns/*.md`. Macros call SOPs by reference — the expanded step reads `patterns/SOP_NAME.md` during execution:

```
1. Read `patterns/DOC_SYNC_SOP.md` — full SOP
2. Execute Phase 1 (Inventory & Validate)
...
```

Conventions:
- **A macro's expanded steps may call `read patterns/{name}.md`** to load an external SOP. This avoids duplicating SOP text inside the macro definition.
- **A macro may also name a SOP inline** in its description as a reference for the agent to look up (e.g. `See patterns/DOC_SYNC_SOP.md`).
- **SOPs may reference other SOPs** by path — the agent resolves them by reading at execution time.
- **No SOP file should be inlined into a macro.** If the same SOP appears in two macros, extract it.

## Standard Macros

### `fix all`

Trigger: user provides a list of issues (from meta-mcp, code review, audit, grader) and says "fix all".

Expands to:

1. **Read every flagged issue** — understand each deficiency
2. **Fix each issue** in order of severity (HIGH → MEDIUM → LOW)
3. **Fix pre-existing gate failures found along the way** — every lint error, typecheck error, test failure, broken import, syntax error encountered in files you touch or that block verification. See CLAUDE.md §5 "Fix Gates Before You Leave Them"
4. **Verify** — run linter, typechecker, and test suite. Repeat until all pass
5. **Report** — list what was fixed, what was out of scope and why

### `update docs`

Trigger: "update docs" or "update documentation" in the context of a repo.

Expands to:

1. Read `patterns/DOC_SYNC_SOP.md` — full SOP
2. Execute all 5 phases (Inventory, MCD Page, Content Audit, FLEET_INDEX, Commit)
3. Run verification checklist at the end of the SOP

### `ship`

Trigger: "ship it" or "release" after work is complete.

Expands to:

1. Check `.nopublish` — abort if present
2. Run all gates (lint, typecheck, tests) — abort on fail
3. Run `just build-native` (if Tauri) or equivalent build
4. Verify artifact exists (NSIS exe, wheel, etc.)
5. `git add`, `git commit`, `git push`
6. Create GitHub release from tag (if version bumped)

### `nsis build`

Trigger: "nsis build <repo>" — build NSIS installer + CUA smoke test.

Expands to:

1. `cd D:\Dev\repos\{repo}`
2. Pre-flight: verify `native/`, `tauri.conf.json` targets `["nsis"]`, resources are `.env.example` not `.env`. Fix if wrong.
3. Build: `just build-native`
4. Gate: `native/target/release/bundle/nsis/*-setup.exe` >= 1 MB
5. Smoke: `just cua-nsis-test` (7 phases)
6. Report: path, size, phase results

### `certify`

Trigger: "certify" or "certify the build".

Expands to:

1. `ruff check src/`
2. `tsc --noEmit` (if webapp)
3. `uv run pytest` or `just test`
4. `just cua-nsis-test` (if native/)
5. `npx playwright test` (if webapp/e2e)
6. Report pass/fail per gate

### `assess and fix` (aliases: `assfix`)

Trigger: "assess and fix <repo>" or "assfix <repo>" — full repo audit, fix, docs sync, and MCPB build.

Expands to:

See `mcp-central-docs/patterns/repo-assess-and-fix.md` for full SOP with per-category checklists.

Full SOP with per-category checklists: `mcp-central-docs/patterns/repo-assess-and-fix.md`. READ IT BEFORE EACH ASSFIX RUN.

**Phase 1 — Assess** (read-only). Catalog every gap, emit report with SOTA score.
> **PHASE GATE**: `Test-Path reports/assess-*.md` — report must exist before fixing.
> **Pre-check**: Also verify `reports/` is in `.gitignore` (add if missing) and check `.ghaudit-timestamp` for ghaudit recency.

**Phase 2 — Fix** in severity order (CRITICAL → HIGH → MEDIUM → LOW).

**Phase 3 — Lint + typecheck**. `ruff check --fix`, `ruff format`, then tsc/biome if webapp.
> **PHASE GATE**: `ruff check src/ && ruff format src/ --check` must both pass.

**Phase 4 — Docs**. `update docs` macro.

**Phase 5 — Build**. MCPB pack (skip if `.nopublish`).

**Phase 6 — Verify & push**. Write `.assess-fix-timestamp`, commit, push (skip git if `.nopublish`).
> **TERMINAL GATE** — run after Phase 6. Any FAIL means loop back to Phase 2:
> ```powershell
> $allPassed = $true
> if (Test-Path ".assess-fix-timestamp") {
>     try { $null = Get-Content ".assess-fix-timestamp" -Raw | ConvertFrom-Json; Write-Host "  [PASS] .assess-fix-timestamp exists and valid JSON" -ForegroundColor Green }
>     catch { Write-Host "  [FAIL] .assess-fix-timestamp not valid JSON" -ForegroundColor Red; $allPassed = $false }
> } else { Write-Host "  [FAIL] .assess-fix-timestamp missing" -ForegroundColor Red; $allPassed = $false }
> # Also check ghaudit was run
> if (Test-Path ".ghaudit-timestamp") {
>     $gh = Get-Content ".ghaudit-timestamp" -Raw | ConvertFrom-Json
>     Write-Host "  [INFO] ghaudit last run: $($gh.timestamp)" -ForegroundColor Cyan
> } else {
>     Write-Host "  [INFO] ghaudit never run — run 'ghaudit <repo>' for GitHub health check" -ForegroundColor Yellow
> }
> $dirty = git diff --stat
> if ($dirty) { Write-Host "  [FAIL] uncommitted changes:`n$dirty" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] working tree clean" -ForegroundColor Green }
> uv run ruff check src/ --quiet; if ($LASTEXITCODE -ne 0) { Write-Host "  [FAIL] ruff check" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] ruff check clean" -ForegroundColor Green }
> uv run ruff format src/ --check --quiet; if ($LASTEXITCODE -ne 0) { Write-Host "  [FAIL] ruff format" -ForegroundColor Red; $allPassed = $false }
> else { Write-Host "  [PASS] ruff format clean" -ForegroundColor Green }
> if ($allPassed) { Write-Host "=== ASSFIX COMPLETE ===" -ForegroundColor Green }
> else { Write-Host "=== ASSFIX INCOMPLETE — fix [FAIL] items, re-run gate ===" -ForegroundColor Yellow }
> ```

### `polish`

Trigger: "polish" or "clean up" at the end of a feature.

Expands to:

1. Fix all lint/type warnings (not just errors)
2. Add `data-testid` attributes to new UI elements
3. Verify dark theme consistency (no light backgrounds, color-scheme: dark)
4. Check for hardcoded tool lists (must be dynamic discovery)
5. Verify Prefab card coverage for list/status/stats tools
6. Run verification gates to confirm nothing broke

### `lint green`

Trigger: "lint green" — make the linter pass across the complete repo.

Expands to:

1. `ruff check src/ --fix` — Python lint + auto-fix
2. `biome check --write` — JS/TS lint + auto-fix (if webapp present, Biome is the fleet JS/TS linter per `WEBAPP_SOTA_STANDARDS.md`)
3. Re-run both and report any remaining issues that need manual fix
4. If Biome is not available (not in repo), use `npx eslint` or the project's configured linter

### `types green`

Trigger: "types green" — TypeScript typecheck clean.

Expands to:

1. `npx tsc --noEmit` in the webapp directory
2. Iterate: read each error, fix, re-run until clean
3. Report what was fixed

### `gates green`

Trigger: "gates green" — lint + typecheck + tests all green.

Expands to:

1. Run `lint green` macro — until clean
2. Run `types green` macro — until clean
3. Run `uv run pytest` or `just test` — until all tests pass
4. Report: pass/fail per gate

### `start green`

Trigger: "start green" or "start environment" — bring the full dev stack up.

Expands to:

1. Clear port zombies: `Get-NetTCPConnection` on the repo's ports → `Stop-Process`
2. Start backend: `uv run python -m {package}.server` (or `start.ps1` equivalent)
3. Health poll: poll `/api/v1/health` up to 60s
4. Start frontend: `npm --prefix webapp run dev` (or `bun run dev`)
5. Open browser to frontend URL
6. Report: URL, backend port, status

### `sync deps`

Trigger: "sync deps" or "update dependencies".

Expands to:

1. `uv sync` — sync Python dependencies, lockfile
2. If webapp present: `bun install` or `npm install`
3. If lockfiles changed: `git add` the lockfiles
4. Report: any new/removed/changed deps

### `bump version`

Trigger: "bump version" — increment project version across all version files.

Expands to:

1. Bump version in `pyproject.toml`
2. Bump version in `tauri.conf.json` (if native/)
3. Bump version in `glama.json` (if exists)
4. Add entry to `CHANGELOG.md`
5. `git add` the affected files

### `scan fleet`

Trigger: "scan fleet" — after finding and fixing a bug in one repo, check all others.

Expands to:

1. Identify the antipattern or bug signature from the fix
2. Run `rg -l` across `D:\Dev\repos\` for the same pattern
3. List repos that match
4. For each: fix or file an issue
5. Update the relevant pitfalls doc in `mcp-central-docs` if the pattern is not documented
6. Report: repos scanned, matches found, actions taken

### `gh status`

Trigger: "gh status" — quick GitHub pulse check.

Expands to:

1. `gh auth status` — verify CLI is logged in
2. `gh api notifications --jq '.[:10] | .[] | "\(.repository.full_name) — \(.subject.title)"'` — unread notifications
3. `gh search issues --limit 5 --state=open "user:sandraschi"` — or equivalent, flag open issues across fleet
4. `github_ops(operation="pr_list", owner="sandraschi", state="open")` — check open PRs
5. Report: auth state, notification count, open PRs, any CI failures

### `zombie clean`

Trigger: "zombie clean" — clean up stale processes and lock files.

Expands to:

1. Scan common fleet ports (Get-NetTCPConnection) for processes that have been running >4h on unused ports
2. Kill zombies by PID, escalate to taskkill /F when Stop-Process fails
3. Find and remove stale `.venv\.lock` files across `D:\Dev\repos\`
4. Find and remove `__pycache__` dirs (excluding `.venv` and `node_modules`)
5. Report: what was killed, what was cleaned

### `mcp pulse`

Trigger: "mcp pulse" — check all MCP servers are alive.

Expands to:

1. Call `opencode_system(action="mcp_pulse")` on opencode-cli-mcp — probes all configured MCP servers via psutil (local) or HTTP (remote)
2. Report: green check for alive, red X for dead, yellow for skipped

This replaces the old pattern of manually reading `~/.config/opencode/opencode.json` and probing each server.

### `assfixstat`

Trigger: "assfixstat" — show which repos have been assessed/fixed and which haven't.

Expands to:

1. Scan fleet MCP repos for `.assess-fix-timestamp` (fixed) vs absent (unfixed). Filters to genuine project repos (has `pyproject.toml`, `package.json`, or `README.md` — excludes hidden/system dirs):
   ```powershell
   $reposRoot = "D:\Dev\repos"
   $all = Get-ChildItem $reposRoot -Directory | Where-Object {
       $_.Name -notmatch '^[._]' -and $_.Name -notin @('build','dist','data','logs','temp','tmp','tools','scripts','profiles',
           'external','externals','backups','analysis','junk','quarantine','security_reports','security_tools','cua-reports',
           'tests','test','native','webapp','workspaces','_archives','_exchange','_junk','_workspaces','node_modules','.venv') -and
       (Test-Path (Join-Path $_.FullName "pyproject.toml") -PathType Leaf) -or
        (Test-Path (Join-Path $_.FullName "package.json") -PathType Leaf) -or
        (Test-Path (Join-Path $_.FullName "README.md") -PathType Leaf)
   } | Sort-Object Name
   $fixed = Get-ChildItem $reposRoot -Recurse -Filter ".assess-fix-timestamp" -Depth 3 | ForEach-Object {
       $r = $_.Directory.Name
       $c = Get-Content $_.FullName -Raw
       $isJson = $false; try { $null = $c | ConvertFrom-Json; $isJson = $true } catch {}
       $ts = if ($isJson) { ($c | ConvertFrom-Json).timestamp } else { ($c -split "`n" | Select-String "2026" | ForEach-Object { $_ -replace '.*?(2026[^\s,}]+).*','$1' } | Select-Object -First 1) }
       $reportDir = Join-Path $_.Directory "reports"
       $latest = if (Test-Path $reportDir) { Get-ChildItem $reportDir -Filter "*.md" | Sort-Object Name -Descending | Select-Object -First 1 }
       $score = if ($latest) { Select-String -Path $latest.FullName -Pattern "SOTA Score:" | ForEach-Object { $_.Line -replace '.*SOTA Score:\s*','' } }
       [PSCustomObject]@{ Repo = $r; Status = "fixed"; Date = $ts; Score = $score }
   }
   $fixedNames = $fixed | ForEach-Object { $_.Repo }
   $unfixed = $all | Where-Object Name -notin $fixedNames | ForEach-Object {
       [PSCustomObject]@{ Repo = $_.Name; Status = "unfixed"; Date = $null; Score = $null }
   }
   $result = $fixed + $unfixed
   $result | Sort-Object Status, Repo | Format-Table -AutoSize Repo, Status, @{N="Date";E={$_.Date}}, Score
   Write-Host "`nSummary: $($fixed.Count) fixed, $($unfixed.Count) unfixed / $($all.Count) total" -ForegroundColor Cyan
   ```
2. Report: table with columns Repo, Status (fixed/unfixed), Date, Score, summary line.

### `ocstat`

Trigger: "ocstat" — full opencode status report.

Expands to:

1. Call `opencode_system(action="mcp_pulse")` — probe all MCP servers for liveness
2. Call `opencode_system(action="config_drift")` — check local server paths exist
3. Call `opencode_system(action="status")` — server health, session count, config summary
4. Call `opencode_system(action="project")` — active project context
5. Format a structured report:
   - opencode server: health check + version
   - Active project
   - MCP servers: alive/dead/skipped per-server breakdown
   - Config drift: stale paths that need cleanup
   - Known issues: list dead servers with recovery hints

### `list expansions`

Trigger: "list expansions" or "what expansions do you have?".

Expands to:

Print all registered macros with their trigger phrases and a one-line summary. Current set:

| Macro | Trigger | Purpose |
|-------|---------|---------|
| `assess and fix` | "assess and fix <repo>" / "assfix <repo>" | Full repo assessment (11-category, read-only → structured report), fix in severity order, lint, docs, MCPB build, verify, push |
| `fix all` | "fix all" | Fix flagged issues, fix pre-existing gate failures, verify |
| `update docs` | "update docs" | Sync README, CHANGELOG, STATUS, PRD, llms-full.txt, mcd project page |
| `ship` | "ship it" | Lint → test → build → verify → commit → push → release |
| `certify` | "certify" | Run all verification gates: ruff, tsc, pytest, cua, playwright |
| `nsis build` | "nsis build <repo>" | Pre-flight check, `just build-native`, verify .exe, `just cua-nsis-test` |
| `polish` | "polish" | Warnings, data-testid, dark theme, dynamic discovery, Prefab |
| `lint green` | "lint green" | ruff + biome to zero errors across repo |
| `types green` | "types green" | tsc --noEmit to zero errors |
| `gates green` | "gates green" | Lint + typecheck + tests all green |
| `start green` | "start green" | Kill zombies → start backend → health poll → start frontend → open |
| `sync deps` | "sync deps" | uv sync + bun install, commit lockfiles if changed |
| `bump version` | "bump version" | Bump pyproject.toml, tauri.conf.json, glama.json, CHANGELOG |
| `scan fleet` | "scan fleet" | Grep all repos for same antipattern, fix or file |
| `gh status` | "gh status" | GitHub auth, unread notifications, open PRs, CI pulse |
| `zombie clean` | "zombie clean" | Kill zombie processes on fleet ports, remove stale `.venv\.lock` files, purge `__pycache__` across repo |
| `mcp pulse` | "mcp pulse" | Check all MCP servers in opencode config are running and responding, report dead/hung ones |
| `assfixstat` | "assfixstat" | Show which repos have been assessed/fixed and which haven't |
| `ocstat` | "ocstat" | Full opencode status report — server health, active project, MCP pulse per-server breakdown, config drift |
| `ghaudit` | "ghaudit" | Fleet-wide GitHub hygiene scan: issues, PRs, CI, topics, descriptions, stale branches, bug cross-ref |
| `spec` | "spec <feature>" | Spec-First Interview: ask clarifying questions, write SPEC.md, get approval before coding |
| `pr clean` | "pr clean" / "squash" | Squash fixup commits, rebase onto base, verify diff, push |
| `qualitycheck` | "qualitycheck <repo>" | Strategic quality assessment: originality, difficulty, wrappee, competition, tool surface, webapp, fleet integration, battlegroup fit → growth gaps |
| `audit deps` | "audit deps" | Check deps for CVEs, stale versions, incompatible licenses |
| `port check` | "port check <repo>" | Verify repo ports match fleet registry, detect conflicts |
| `env sync` | "env sync" | Sync .env.example with actual env vars used in source |
| `tag` | "tag <version>" | Create annotated git tag, push, verify CI triggered |
| `drift` | "drift" | Fleet-wide gap analysis: compare all repos against SOP without fixing |
| `onboard` | "onboard <repo>" | First-time setup: install deps, start stack, open browser |
| `template sync` | "template sync" | Compare boilerplate files against reference repos, show diffs |
| `ci check` | "ci check <repo>" | List recent CI workflow runs, identify failures, report pass/fail per workflow |
| `fork trawl` | "fork trawl <repo>" | Enumerate forks, classify real work vs autoscraped, extract patterns |
| `bench` | "bench <repo>" | Run pytest benchmarks, report regression vs last run |

### `ghaudit`

Trigger: "ghaudit" — fleet-wide GitHub hygiene scan.

Full SOP: `mcp-central-docs/patterns/GHAUDIT_SOP.md`

Expands to:

1. Follow GHAUDIT_SOP — auth check, per-repo probes (issues, PRs, CI, metadata, stale branches, bug cross-ref), aggregate report
2. Report: fleet-wide table sorted by severity, summary counts
3. Do NOT fix anything — present findings for user action

### `spec`

Trigger: "spec <feature>" — Spec-First Interview for a new feature.

Full SOP: `mcp-central-docs/patterns/SPEC_INTERVIEW_SOP.md`

Expands to:

1. Follow the Spec-First Interview SOP: interview user on what/why/how/non-goals
2. Write `SPEC.md` to the repo root with: goal, requirements, non-goals, API contracts, open questions
3. Present the spec to the user for approval
4. Do NOT start coding until user explicitly approves the spec
5. Report: spec written, pending approval

### `pr clean`

Trigger: "pr clean" or "squash" — clean up a PR branch before merging.

Expands to:

1. `git log --oneline origin/main..HEAD` — count commits, check for fixup/squash messages
2. `git rebase -i origin/main` — squash fixup commits, keep meaningful commit messages
3. `git diff --stat origin/main` — verify the diff is clean and contains only intended changes
4. `git push --force-with-lease` — push cleaned branch
5. Report: how many commits squashed, diff size, pushed

### `qualitycheck`

Trigger: "qualitycheck <repo>" — strategic quality assessment beyond mechanical SOTA compliance.

Full SOP: `mcp-central-docs/patterns/QUALITY_CHECK_SOP.md`

Expands to:

1. Follow QUALITY_CHECK_SOP — score 8 strategic dimensions (originality, difficulty, wrappee importance, competitive situation, tool surface, webapp quality, fleet integration, battlegroup fit)
2. **Docs quality check**: Read `patterns/DOC_SYNC_SOP.md` and execute Phase 3 (Content Audit) at minimum. Score the docs dimension (0-10) and report gaps. See DOC_SYNC_SOP for minimum standards per file.
3. Identify 3-5 growth gaps with impact ratings
4. Write report to `reports/quality-{repo}-{date}.md` + `.qualitycheck-timestamp`
5. Report: overall score, rating (Flagship/Strong/Good/Weak/Runt), top growth opportunities

### `audit deps`

Trigger: "audit deps" — check all dependencies for security, freshness, and fleet compatibility.

Full SOP: `mcp-central-docs/patterns/DEP_AUDIT_SOP.md`

Expands to:

1. Follow DEP_AUDIT_SOP — security scan, freshness check, license audit
2. Write report to `reports/deps-{date}.md` + `.deps-timestamp` (committed)
3. Report: security issues, stale deps, license flags. Do NOT auto-upgrade — present findings for user decision.

### `port check`

Trigger: "port check <repo>" — verify a repo's ports match the fleet registry.

Expands to:

1. Read `mcp-central-docs/operations/WEBAPP_PORTS.md` for the repo's registered ports
2. Grep the repo for hardcoded port numbers: `rg -n "109[0-9]{2}|108[0-9]{2}|107[0-9]{2}" src/ webapp/ --include "*.py" --include "*.ts" --include "*.tsx" --include "*.json"`
3. Check for zombie listeners: `Get-NetTCPConnection -LocalPort <port> -ErrorAction SilentlyContinue`
4. Verify `start.ps1`, `config.py`/`settings.py`, and `vite.config.ts` all use the registered ports
5. Report: registered ports, actual ports in code, mismatches, zombie processes

### `env sync`

Trigger: "env sync" — sync `.env.example` with actual env vars used in source code.

Expands to:

1. Extract all `os.getenv("...")` / `os.environ.get("...")` calls from `src/` — collect unique env var names
2. Extract all `import.meta.env.VITE_*` / `process.env.*` references from `webapp/src/` — collect unique names
3. Read current `.env.example` — list existing entries
4. Diff: find env vars in code but missing from `.env.example` (add them), and vars in `.env.example` but not in code (flag as possibly dead)
5. Add missing variables to `.env.example` with placeholder values and a comment describing what they do
6. Report: added X, flagged Y as possibly dead, total tracked

### `tag`

Trigger: "tag <version>" — create and push a git tag for release.

Expands to:

1. Verify working tree is clean (`git diff --stat` must be empty)
2. Verify version in `pyproject.toml` matches `<version>` (or `tauri.conf.json` if native/)
3. `git tag -a v<version> -m "Release v<version>"` — create annotated tag
4. `git push origin v<version>` — push tag to trigger CI
5. Verify CI was triggered (check GitHub Actions via `gh` or browser)
6. Report: tag created, pushed, CI status

### `drift`

Trigger: "drift" — fleet-wide gap analysis: compare every repo against the SOP checklist without fixing.

Full SOP: `mcp-central-docs/patterns/DRIFT_SCAN_SOP.md`

Expands to:

1. Follow DRIFT_SCAN_SOP — enumerate repos, run lightweight probes, aggregate report
2. Write report to `reports/drift-{date}.md` + `.drift-timestamp` (committed)
3. Report: total repos scanned, pass rate, worst offenders, stale assessments

### `onboard`

Trigger: "onboard <repo>" — interactive first-time setup for a repo you haven't run before.

Full SOP: `mcp-central-docs/patterns/ONBOARD_SOP.md`

Expands to:

1. Follow ONBOARD_SOP — verify repo, install deps, check .env, start backend, health poll, start frontend, open browser
2. Report: ports, health status, dashboard URL, any missing config

### `template sync`

Trigger: "template sync" — pull latest boilerplate from reference repos into this repo.

Expands to:

1. Identify which boilerplate files exist: `start.ps1`, `FleetStartMode.ps1`, `build.ps1`, `tauri.conf.json`, `hooks.nsh`, `{repo}-backend.spec`
2. For each file that exists, compare against the reference template:
   - `start.ps1` → compare with `pywinauto-mcp/webapp/start.ps1` or `email-mcp/webapp/start.ps1`
   - `FleetStartMode.ps1` → compare with `pywinauto-mcp/scripts/FleetStartMode.ps1`
   - `tauri.conf.json` → compare with `pywinauto-mcp/web_sota/src-tauri/tauri.conf.json`
   - `{repo}-backend.spec` → compare with `pywinauto-mcp/pywinauto-mcp-backend.spec`
3. Show diffs for each file that has drifted from the reference
4. Ask user which files to update — do NOT overwrite without confirmation
5. Report: files checked, files drifted, files updated

### `ci check`

Trigger: "ci check <repo>" or "ci check <owner>/<repo>" — check CI workflow status for a repo.

Full SOP: `mcp-central-docs/patterns/CI_CHECK_SOP.md`

Expands to:

1. Follow CI_CHECK_SOP — list recent workflow runs, identify failures, extract failed step name and branch
2. For fleet repos, cross-reference: pre-existing failure or new? Infrastructure vs code failure?
3. Report: pass/fail table with workflow name, branch, status, failed step, age
4. Do NOT re-run, cancel, or open PRs to fix CI

### `fork trawl`

Trigger: "fork trawl <repo>" or "fork trawl <owner>/<repo>" — classify forks of a repo by signal.

Full SOP: `mcp-central-docs/patterns/FORK_TRAWL_SOP.md`

Expands to:

1. Follow FORK_TRAWL_SOP — enumerate forks, gather per-fork signals, classify (real work / autoscraped / derivative), extract findings from real-work forks
2. Report: table, counts, top 1-2 patterns worth investigating
3. Do NOT clone, open issues, or contact fork authors

### `bench`

Trigger: "bench <repo>" — run performance benchmarks and report regression.

Expands to:

1. Check for existing benchmark config: `pytest.ini` has `--benchmark`, or `tests/benchmarks/` exists
2. If no bench config exists, report that and stop — don't add benchmarks
3. Run `uv run pytest tests/ --benchmark-only -q` — capture results
4. Compare against previous run if `.benchmark-last.json` exists in repo root
5. Report: pass/fail, regressions, improvements, save results to `.benchmark-last.json`
6. Do NOT fail CI over performance regressions — just report them

## Adding New Macros

To add a macro, update this file and add a Domain Read List entry in
`CLAUDE.md` (global) pointing to it. Macros should be:

- **Named** with a short trigger phrase
- **Scoped** to a specific user intent
- **Listed** as concrete expanded steps (not vague)
- **Self-limiting** (stop conditions defined)

## Anti-Patterns

- **Under-expansion**: Treating "fix all" as fixing just the first issue. Expand fully.
- **Over-expansion**: Running `ship` when user only said "update docs". Start only what was said.
- **Silent expansion**: Not telling the user a macro expanded. Always report the expanded plan.
