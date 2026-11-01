# Postmortem: Fleet unified start migration (2026-07-27)

**Duration:** ~5 hours (evening session)  
**Scope:** ~115 manifest webapps, 129+ `starts/*.bat` launchers, central engine + per-repo configs  
**Severity:** High — widespread start failures, user blocked from normal `.bat` workflow  
**Author:** Fleet agent session (Cursor)

---

## Executive summary

We migrated the fleet from 115+ snowflake `start.ps1` scripts to a unified launcher stack (one engine, thin wrapper, per-repo `fleet-start.config.ps1`). The **architecture is sound**; the **execution was not**. A blind bulk regen of configs and several PS 5.1 / vendoring / probe gaps caused cascading failures that required hours of reactive fixes.

**Current state (end of session):**

| Area | Status |
|------|--------|
| `.bat` parse / dispatch (PS 5.1) | Fixed (em dash, UTF-8 BOM) |
| Uvicorn targets | Fixed (0 fail on audit, 15 checked) |
| `uv sync --extra dev` | Fixed (SyncExtras only when optional-deps defines `dev`) |
| Stale `node_modules` | Fixed (install on manifest change + legacy-peer-deps fallback) |
| Zombie port reclaim | Fixed (taskkill /T, no blind frontend reuse) |
| Browser open on `.bat` | Fixed (PS 5.1 single-line poll command + reuse paths) |
| `FleetStartMode.ps1` vendoring | Synced fleet-wide (~115–180 repos) |
| Automated smoke gate | Added `fleet-smoke-gate.ps1`; probe infra fixed |

---

## Timeline (approximate)

| Time | Event |
|------|--------|
| T+0 | User requests unified `start.ps1`; `-RefreshAll` / `-ConvertLegacy` on `starts/*.bat` |
| T+1 | User reports `dreame-start.bat` still broken — only 2 repos migrated to unified wrapper; rest still snowflakes |
| T+1.5 | Bulk `repair-fleet-unified-start.ps1` on 115 repos |
| T+2 | **Instacrash:** all `.bat` fail — UTF-8 em dashes in `Invoke-FleetWebappStart.ps1` break **Windows PowerShell 5.1** (what `.bat` calls via `powershell.exe`) |
| T+2.5 | Strip em dashes fleet-wide (127 `start.ps1` files); add lint + ASCII guard |
| T+3 | Dreame/readly backend fail: `SyncExtras=@('dev')` but `dev` lives in `[dependency-groups]`, not `[project.optional-dependencies]` |
| T+3.5 | Fleet-wide `-ConfigOnly` regen for SyncExtras; 115 configs rewritten |
| T+4 | git-github-mcp: `Attribute "app" not found` — blind default `{pkg}.server:app` wrong for many repos |
| T+4.5 | Uvicorn audit + improved `Get-InferredUvicornTargetFromServerPy`; 10 pre-regen failures → 0 post-regen |
| T+5 | filesystem-mcp Vite crash (stale `node_modules`, missing `@tauri-apps/api`); npm install logic fixed fleet-wide |
| T+5 | mcp-central-docs port 10794 zombie / Vite bump to 10795 — blind frontend reuse skipped zombiekill |
| T+5 | Browser no longer opens — multiline here-string in `Start-FleetBrowserWhenReady` silent fail on PS 5.1 |
| T+5 | Automated probe attempts stall / fail until probe launcher bugs fixed; `fleet-smoke-gate.ps1` added |

---

## Root causes

### 1. PS 5.1 vs PS 7 split (critical)

- **Symptom:** Instant parse error on every `.bat`; error pointed at line ~492 (`string missing terminator`).
- **Cause:** `Invoke-FleetWebappStart.ps1` written in UTF-8 **without BOM** with Unicode em dashes (`U+2014`). PS 7 parses fine; **`powershell.exe` 5.1** misreads bytes and breaks string parsing.
- **Fix:** ASCII-only user-facing strings (or UTF-8 BOM); `lint-fleet-powershell.ps1` + `.cursor/rules/powershell-51-launcher-ascii.mdc`.
- **Lesson:** All fleet launcher `.ps1` must be validated with **`powershell.exe`**, not only `pwsh`.

### 2. Blind bulk config generation (critical)

- **Symptom:** `Error loading ASGI app. Attribute "app" not found in module "git_github_mcp.server"` and similar across many repos.
- **Cause:** `repair-fleet-unified-start.ps1 -ConfigOnly` defaulted `UvicornTarget = '{module}.server:app'` without verifying the symbol exists. Many repos use `web_app`, `gateway:app`, `module-serve`, etc.
- **Fix:** `Get-InferredUvicornTargetFromServerPy`, `audit-fleet-uvicorn-targets.ps1`, fleet-wide regen. Post-audit: **15 checked, 0 fail**.
- **Lesson:** Never fleet-wide regen without **verify step** (import probe or audit script) in the same pipeline. Fail closed.

### 3. SyncExtras / uv dependency model mismatch

- **Symptom:** dreame-mcp, readly-mcp: `Extra 'dev' is not defined in optional-dependencies`.
- **Cause:** Config always emitted `SyncExtras = @('dev')`; many fleet repos define `dev` under **`[dependency-groups]`**, not `[project.optional-dependencies]`. `uv sync --extra dev` only works for the latter.
- **Fix:** `Test-PyprojectHasDevOptionalExtra`; omit SyncExtras when not applicable. ~18–20 repos corrected.
- **Lesson:** Infer from **pyproject.toml structure**, not convention.

### 4. Stale `node_modules` skip

- **Symptom:** filesystem-mcp Vite: `Failed to resolve import "@tauri-apps/api/event"`.
- **Cause:** Engine only ran `npm install` when `node_modules` **missing entirely**. Partial/stale trees skipped install.
- **Fix:** `Test-FleetFrontendInstallNeeded` (lockfile/mtime, `.bin` check); `--legacy-peer-deps` fallback; one-time `Invoke-FleetFrontendInstallSweep.ps1` (94/98 success).
- **Lesson:** Never gate install on folder existence alone.

### 5. Zombiekill / port reclaim regression

- **Symptom:** Vite: `Port 10794 is in use, trying another one...` → binds 10795 (backend port).
- **Cause:** (a) Blind “frontend already listening → reuse” without `-ReuseIfRunning`; (b) weak kill (`Stop-Process` before `taskkill /F /T`); (c) npm lacked `--strictPort`.
- **Fix:** Reclaim unless `-ReuseIfRunning` + HTTP OK; pre-bind kill; strict port args; vendored `FleetStartMode.ps1` synced fleet-wide.
- **Lesson:** **Kill first, bind second.** `--strictPort` is safety net, not primary behavior.

### 6. Browser open regression

- **Symptom:** `.bat` starts stack but no browser.
- **Cause:** (a) `Start-FleetBrowserWhenReady` used multiline here-string in `Start-Process -Command` — **silent no-op on PS 5.1**; (b) browser only invoked inside `if ($startFrontend)` — reuse/early-return paths skipped it; (c) `$skipBrowser` incorrectly included `-FrontendOnly`.
- **Fix:** Single-line `-Command`; `Invoke-FleetMaybeOpenBrowser` on reuse + fallback; legacy `$NoBrowser` gating only.
- **Lesson:** Test browser open on **default `.bat` path** with PS 5.1, not probe flags.

### 7. Vendored helper drift

- **Symptom:** Fixes to central `FleetStartMode.ps1` did not apply to repos until manual copy.
- **Cause:** Each repo loads `{repo}/scripts/FleetStartMode.ps1`, not the central file. Bulk migration updated engine + configs but not all vendored copies promptly.
- **Fix:** Explicit fleet-wide sync (115–180 repos). Repair script should always re-vendor when canonical changes.
- **Lesson:** Treat vendored files as **release artifacts** — sync is part of every engine change.

### 8. Automated check failures (probe / subagents)

- **Symptom:** User still manually paste-crash-fixing; background workers often stalled; probe did not catch issues early.
- **Cause:** Multiple probe bugs: `-Headless` skipped frontend during probe; `FLEET_PROBE_RUN` semantics wrong; `Backend.Env` null crash; log parse errors; probe ran before migration fixes landed.
- **Fix:** Probe launcher fixes; `fleet-smoke-gate.ps1` wrapping `fleet-basic-smoke-all.ps1`; 4-repo batch: 3× `stack_ok`, 1× `stack_degraded` (filesystem `/mcp/sse` 404 noise).
- **Lesson:** **Gate before merge/regen**, not after user reports. Subagents are poor substitute for a single runnable gate command in foreground.

---

## Collateral damage

| Item | Impact |
|------|--------|
| 115 `fleet-start.config.ps1` regen (multiple passes) | Overwrote manual fixes (e.g. dreame custom backend briefly reverted) |
| 127 `start.ps1` em-dash strip | Low risk (comments only) |
| mcp-central-docs `Bundles.tsx` | Merged import line (bulk-edit corruption) — fixed |
| glance-mcp / magentart-mcp | Corrupted encodings — re-wrapped from template |
| User trust / time | ~5 hours lost to reactive fixes |

---

## What worked

- **One engine + per-repo config** model — correct long-term; ports live in `fleet-start.config.ps1`, not in engine.
- **`starts/*.bat` LAUNCHDIR pattern** — 129/131 standardized; symlinks no longer cause instacrash.
- **Audit scripts** once fixed: `audit-fleet-uvicorn-targets.ps1`, `lint-fleet-powershell.ps1`.
- **`fleet-smoke-gate.ps1`** — single entry point for pre-flight checks.

---

## Action items (done vs remaining)

### Done this session

- [x] Em dash strip + PS 5.1 lint rule
- [x] SyncExtras inference fix + fleet regen
- [x] Uvicorn target audit + repair inference
- [x] npm install / legacy-peer-deps fleet fix
- [x] Zombiekill + strictPort
- [x] Browser PS 5.1 fix + reuse paths
- [x] FleetStartMode fleet-wide sync
- [x] `fleet-smoke-gate.ps1`
- [x] Probe launcher bug fixes
- [x] filesystem-mcp health/config restore

### Remaining / recommended

- [ ] Run `fleet-smoke-gate.ps1 -SyncManifest` after any future `-ConfigOnly` regen
- [ ] Wire `audit-fleet-uvicorn-targets.ps1` + `lint-fleet-powershell.ps1` into `repair-fleet-unified-start.ps1` as **hard gate** (non-zero exit blocks regen)
- [ ] Auto re-vendor `FleetStartMode.ps1` on every repair run (checksum compare)
- [ ] Exclude `/mcp/sse` 404 from dirty-log degrade or add route (filesystem-mcp cosmetic)
- [ ] Add manifest entries for glance-mcp / magentart-mcp if they need `starts/*.bat`
- [ ] Document: **always test with `powershell.exe`**, never assume `pwsh`

---

## Commands (operator reference)

```powershell
# Pre-flight single repo
Set-Location D:\Dev\repos\mcp-central-docs
.\scripts\fleet-smoke-gate.ps1 -RepoFilter dreame-mcp

# Full fleet gate
.\scripts\fleet-smoke-gate.ps1 -SyncManifest

# Uvicorn target audit
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\Dev\repos\mcp-central-docs\scripts\audit-fleet-uvicorn-targets.ps1"

# PS 5.1 launcher lint
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\Dev\repos\mcp-central-docs\scripts\lint-fleet-powershell.ps1"

# Re-vendor port helpers
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "D:\Dev\repos\mcp-central-docs\scripts\vendor-fleet-startmode.ps1"
```

---

## Follow-up: headless fork-storm + re-vendor gap (2026-08-17)

Two latent defects from the original migration surfaced and were fixed on 2026-08-17:

| Defect | Symptom | Fix |
|--------|---------|-----|
| **Stale vendored `FleetStartMode.ps1`** | All 182 vendored copies predated the headless env-guard (commit `c4ae560`); `repair-fleet-unified-start.ps1` only vendored when *missing*, so the fix never propagated | `Ensure-FleetStartModeVendored` now hash-compares against canonical and **re-vendors on drift**; synced 176 repos to canonical |
| **Headless spawn loop** | Old guard checked `RawUI.WindowTitle -match 'Hidden'` — a hidden console's title is the exe path, so `-Headless` re-spawned hidden `powershell.exe` forever (fork storm) and never booted | Env-var guard `FLEET_HEADLESS_REENTERED` in canonical `FleetStartMode.ps1`; CUA tests unaffected (`FLEET_PROBE_RUN=1` bypasses the path entirely) |
| **Next.js frontend kind missing** | Engine passed vite flags (`--port/--host/--strictPort`) which `next dev` rejects (`unknown option '--host'`) — broke calibre-mcp/plex-mcp | Added `Frontend.Kind='next'` (`-p N -H 127.0.0.1`) to both launch paths |
| **Webapp backend target drift** | calibre-mcp/plex-mcp configs pointed at the MCP daemon (`{pkg}.server:app`, health-only) instead of the webapp backend (`webapp\backend\app.main:app` — REST + `/mcp`) | Configs fixed: `WorkDir=webapp\backend`, `WebRoot=webapp\frontend`, `LoadDotEnv=$true` |
| **Legacy launcher repos** | meta_mcp/civitai-mcp/docker-mcp/mcp-federation-hub still on hand-rolled start.ps1 (windowtitle headless check, old FleetStartMode API) | Migrated all 4 to fleet wrapper + canonical FleetStartMode; federation-hub switched to `Backend.Kind='nssm'` (NSSM-managed bridge) |

**Port reallocation (same session):** leanforge-mcp moved 10855/10856 → 10867/10868 (dormant repo yielding ports); mcp-federation-hub retroactively registered at its actual running ports 10856/10857.

---

## Blameless summary

The migration tried to do too much in one unattended batch (115 configs, wrong defaults, no PS 5.1 validation, no import verification). Reactive fixes addressed each failure class, but only after user pain. The correct workflow going forward: **small pilot → smoke gate → fleet-wide**, with audit/lint as blocking steps in the repair script itself.

---

## Related docs

- `mcp-central-docs/standards/START_SCRIPT_STANDARD.md`
- `mcp-central-docs/docs/operations/FLEET_WEBAPP_PROBE.md`
- `.cursor/rules/powershell-51-launcher-ascii.mdc`
