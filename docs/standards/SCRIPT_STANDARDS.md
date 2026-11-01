---
title: "Fleet Script Standards (SOTA 2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-09
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Fleet Script Standards (SOTA 2026)

> Every `.ps1`/`.py` that touches ≥3 repos or ≥3 files in one repo MUST follow this.

See also: `POWERSHELL_STANDARDS.md`, `TAURI_PRODUCTION_PITFALLS.md` §Batch Size Limit (10 files/commit), `GIT_REPOSITORY_SAFETY.md`.

---

## 1. Header (MANDATORY)

Every script MUST start with:

```powershell
<#
.SYNOPSIS
  One-line what it does.

.DESCRIPTION
  Why it exists, what fleet standard it enforces, and the 10-file batch limit.

.PARAMETER DryRun
  Default true. No writes, only git diff --stat + log.

.PARAMETER Execute
  Switch to actually write files (requires -Confirm).

.EXAMPLE
  .\fleet-sweep-tauri-sota.ps1 -DryRun
  .\fleet-sweep-tauri-sota.ps1 -Execute -Repo qcad-mcp

.NOTES
  Fleet: mcp-central-docs/standards/SCRIPT_STANDARDS.md
  Idempotency: re-running must produce 0 diff if already fixed.
#>
[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]
param(
  [switch]$DryRun = $true,
  [switch]$Execute,
  [string[]]$Repo,
  [string]$ReposDir = "D:\Dev\repos"
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
```

* `SupportsShouldProcess` gives `-WhatIf`/`-Confirm` for free.
* `DryRun` is the safe default. `Execute` without `DryRun` must error: `if ($Execute -and -not $PSCmdlet.ShouldProcess(...)) { throw }`.

## 2. Backup (MANDATORY for ≥3 files)

Before any write, timestamped `.bak` per file:

```powershell
Copy-Item $f "$f.$(Get-Date -Format 'yyyyMMdd_HHmmss').bak" -Force
```

* Pattern is in `.gitignore` (`*.bak`, `*.bak.*`) - zero commit risk.
* Cleanup is explicit: `Get-ChildItem -Recurse -Filter "*.bak*" | Remove-Item` only when user says `cleanup`.

## 3. Idempotency Guards

Every patch must be a no-op if already fixed:

```powershell
$c = Get-Content $p -Raw
if ($c -match "manualChunks") { Write-Verbose "SKIP $p already code-split"; continue }
```

* For `vite.config.ts`: only patch if `manualChunks` absent.
* For `backend.rs`: only if `for i in 0..240` present.
* For `spec`: only if `_keep_dist` contains hyphen-only `opentelemetry-`.

Re-running the sweep must yield `git diff --quiet` (0 diff).

## 4. Per-Repo Gates (MANDATORY)

After patching a repo's files, run gates **before** `git add`:

```powershell
$ok = $true
$ok = $ok -and (Invoke-WithRetry { & "$env:USERPROFILE\.cargo\bin\cargo.exe" check --manifest-path "$repo/native/Cargo.toml" } -OperationName "cargo check $repo")
$ok = $ok -and (Push-Location "$repo/webapp/frontend"; npx tsc --noEmit; $LASTEXITCODE -eq 0)
$ok = $ok -and (& "C:\Users\<user>\.local\bin\uv.exe" run ruff check "$repo/src" --quiet; $LASTEXITCODE -eq 0)
if (-not $ok) {
  Write-ErrorLog "Gate failed for $repo - rolling back" "Error" $_
  foreach ($f in $patched) { Copy-Item "$f.*.bak" $f -Force } # rollback
  continue
}
```

* `Invoke-WithRetry` from `POWERSHELL_STANDARDS.md` §1.2 (3×, exponential backoff) for transient `cargo`/`npm` locks.
* On gate fail, **rollback** that repo from `.bak` and log `FAIL` - don't commit, don't abort fleet.

## 5. Logging + Audit Trail (MANDATORY)

* Structured log: `reports/sweep-YYYY-MM-DD.md` (gitignored) with per-repo `PASS/FAIL/SKIP`, `files patched`, `commit sha`, `gate output`.
* Also `Write-Verbose`/`Write-ErrorLog` to console with `Host` = `Goliath` and `timestamp` ISO8601.
* Never use `2>nul` - use `2>$null` (see `POWERSHELL_STANDARDS.md` §6).

## 6. Git Batch Limit (HARD RULE)

* **One repo = one commit, max 10 files/commit.** If a repo needs 13 files, do `10 + 3` commits.
* `git add -- $files` (not `git add -A` - that grabs `build/`, `cua-reports/`, `*.bak`).
* `git status --porcelain` review before commit - never blind-commit unrelated `M`.
* Commit message: `sweep: {repo} {what} (fleet {standard} §X)` with `Co-Authored-By`.

## 7. Error Handling (MANDATORY)

* `try/catch` per file, `catch { Write-ErrorLog "Failed $f" "Error" $_; continue }` - don't abort fleet on one bad `pyproject.toml`.
* `trap` at top level to log fatal and `exit 1` only on fleet-wide failure (e.g., `ReposDir` missing).
* `exit 0` on partial success (some repos PASS, some FAIL) - CI treats `0` as "sweep completed, see report".

## 8. Exit Codes

* `0` - sweep completed (even if some repos FAIL, report has details).
* `1` - fatal (ReposDir missing, not a git repo, no write permission).

## 9. Example Fleet Sweep Template

See `scripts/fleet-sweep-tauri-sota.ps1` - the hardened implementation of the `qcad`→`blender` code-split + backend spawn fix (port off Docker, `\\?\` strip, `opentelemetry_api` keep).

---

**Checklist before letting a sweep touch the next 50 repos:** DryRun → 5-file idempotent → per-repo gates → rollback on fail → structured log → `git diff` review.
