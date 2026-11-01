---
title: "SOTA Windows/PowerShell Guardrails (2026)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# SOTA Windows/PowerShell Guardrails (2026)

## Unicode (never em dash)

- **EM DASH (`—`) is never allowed** in `.ps1`, `.bat`, or `justfile` (any line, including comments).
- Use ASCII `-` or ` -- ` only. Checker: `mcp-central-docs/scripts/check-unicode-safe.ps1` ([Unicode Safety](../patterns/unicode_safety.md)).

## Native PowerShell Syntax Mandatory
- **No `&&`**: PowerShell 7+ has `&&`/`||` but older docs warned against it. Use `;` or `if ($?) { ... }` for PS5.1 compat.
- **No `tail`**: Use `Get-Content <path> -Tail <n>`.
- **No `grep`**: Use `Select-String -Pattern "<regex>"`.
- **No `cat`**: Use `Get-Content`.
- **No `ls` / `ll`**: Use `Get-ChildItem` (gci).
- **No `rm -rf`**: Use `Remove-Item -Recurse -Force`.
- **No recursive scans of repo root**: Never `Get-ChildItem -Recurse` on a repo root — you'll hit `.venv/`, `node_modules/`, `build/`. Always target `src/` specifically, or use `fd` to filter by extension + exclude patterns (`fd -e py -H --exclude .venv --exclude node_modules`).
  - **Known false positive**: `git rm` is NOT `rm -rf` — it modifies the git index only, never touches files on disk. The linter flags it anyway (better safe than sorry). Use `git reset --soft` as a workaround, or pipe individual files: `git ls-files path | ForEach-Object { git rm --cached $_ }`.

## Join-Path: two positional args MAX (PS 5.1 compat) — HARD RULE, recurred ~20x

**`Join-Path` takes exactly two positional path arguments on Windows PowerShell 5.1** (`powershell.exe`, the OS-default interpreter on every naked PC and most CI runners). `-AdditionalChildPath` (which allows 3+ segments) is **PowerShell 6+ (`pwsh`) only**. Code authored/tested under `pwsh` 7 passes silently and then crashes the moment it runs under bare `powershell.exe`:

```
Join-Path : A positional parameter cannot be found that accepts argument '..'.
```

```powershell
# WRONG — 3 positional args, crashes on PS 5.1
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." "..")).Path

# CORRECT — combine extra segments into one relative-path string
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

# ALSO CORRECT — nest calls
$repoRoot = (Resolve-Path (Join-Path (Join-Path $PSScriptRoot "..") "..")).Path
```

This exact bug shipped in the fleet-canonical CUA test script template and was inherited byte-identical by ~195 repos (391 file occurrences, see [TRAPS_AND_PITFALLS.md #35](../TRAPS_AND_PITFALLS.md)) before being caught. It has now recurred independently roughly 20 times across unrelated sessions — **before writing any multi-segment `Join-Path` call, use the two-args-max form above by default.** Don't reach for `-AdditionalChildPath` on a script that might ever run under 5.1 (which is effectively all of them, since `powershell.exe` is what's on PATH by default).

## Never pair a mutating action with a fixed sleep as the only verification — HARD RULE

**"Kill it, sleep N seconds, assume it's dead" / "Start it, sleep N seconds, assume it's up" is not a safety measure — it's a guess about machine speed that day, dressed up as one.** A 2026-09-17 fleet grep found this shape in 29+ scripts outside the two NSIS-build-specific instances that motivated this rule (see [TRAPS_AND_PITFALLS.md #36](../TRAPS_AND_PITFALLS.md)).

```powershell
# WRONG — kill, sleep, assume dead
Stop-Process -Name foo -Force
Start-Sleep -Seconds 2
# ... proceeds as if foo is definitely gone

# WRONG — start, sleep, assume up
Start-Process $exe
Start-Sleep -Seconds 5
# ... proceeds as if $exe is definitely ready

# CORRECT — poll the actual condition, with a real timeout, and fail loudly if it never holds
$waitSec = 15
$elapsed = 0
while ($elapsed -lt $waitSec -and (Get-Process -Name foo -ErrorAction SilentlyContinue)) {
    Start-Sleep -Milliseconds 500
    $elapsed += 0.5
}
if (Get-Process -Name foo -ErrorAction SilentlyContinue) {
    Write-Host "WARNING: foo still alive after ${waitSec}s" -ForegroundColor Yellow
}
```

A single fixed sleep is a race condition wearing a seatbelt costume: on a fast machine with a warm disk cache it happens to pass, and on a loaded machine, a cold PyInstaller onefile extraction, or one where Windows Defender is scanning the freshly-written files, it silently doesn't — and the script has no way to tell the difference because it never checked. This bit hardest in NSIS build gates: a fixed-sleep-then-single-`HasExited`-check smoke test let a broken PyInstaller backend (missing `PIL._imaging`) ship into a signed installer as "PASSED", because `Kill()` fired before the process had gotten far enough into extraction to reach the line that would have crashed it (full incident: [TRAPS_AND_PITFALLS.md #36a](../TRAPS_AND_PITFALLS.md)).

**Rule:** whenever you kill a process, start a process, or free a port, verify the actual condition (process gone / port closed / port open / health check responds / log line seen) in a poll loop with a real timeout — never a bare `Start-Sleep` followed by code that assumes success. If the condition never holds within the timeout, fail loudly (`throw`, non-zero exit, or at minimum a visible warning) rather than silently continuing as if it had.

**Detection (re-run to check current fleet exposure):**
```powershell
rg -U -P 'Stop-Process[^\n]*\n(\s*\}[^\n]*\n)?\s*Start-Sleep -Seconds \d' D:\Dev\repos --type ps1 -l
rg -U -P 'Start-Process[^\n]*\n(\s*\}[^\n]*\n)?\s*Start-Sleep -Seconds \d' D:\Dev\repos --type ps1 -l
```

## Command Execution Substrate
Always use these absolute paths to ensure reliability:

| Tool | Absolute Path |
| :--- | :--- |
| **ripgrep (rg)** | `C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\rg.exe` |
| **just** | `C:\Users\<user>\scoop\shims\just.exe` |
| **Ruff** | `C:\Users\<user>\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe` |
| **Biome** | `C:\Users\<user>\.local\bin\biome.exe` |
| **lake** | `$env:USERPROFILE\.elan\bin\lake.exe` |
| **bun** | `C:\Users\<user>\.bun\bin\bun.exe` |
| **uv** | `C:\Users\<user>\.local\bin\uv.exe` |
| **fd** | `C:\Users\<user>\.local\bin\fd.exe` |
| **PSScriptAnalyzer** | `C:\Users\<user>\OneDrive\Dokumente\PowerShell\Modules\PSScriptAnalyzer\1.25.0\PSScriptAnalyzer.psd1` |
| **markdownlint** | `C:\Users\<user>\AppData\Roaming\npm\markdownlint.cmd` |
| **yamllint** | `C:\Users\<user>\.local\bin\yamllint.exe` |
| **taplo** | `C:\Users\<user>\.cargo\bin\taplo.exe` |
| **hadolint** | `C:\Users\<user>\.local\bin\hadolint.exe` |
| **shellcheck** | `C:\Users\<user>\.local\bin\shellcheck.exe` |
| **actionlint** | `C:\Users\<user>\.local\bin\actionlint.exe` |
| **py** | `C:\Windows\py.exe` |
| **ollama** | `C:\Users\<user>\AppData\Local\Programs\Ollama\ollama.exe` |
| **winget** | `C:\Users\<user>\AppData\Local\Microsoft\WindowsApps\winget.exe` |
| **pywinauto** | `pip install pywinauto` (dep of CUA smoke test) |
| **Pillow** | `pip install Pillow` (dep of CUA smoke test, screenshot capture) |
| **pytesseract** | `pip install pytesseract` (dep of CUA smoke test, OCR verification) |
| **Tesseract-OCR** | `C:\Program Files\Tesseract-OCR\tesseract.exe` (install via `winget install Tesseract-OCR`) |

## PowerShell Linting (PSScriptAnalyzer)

Every fleet `.ps1` script should pass `Invoke-ScriptAnalyzer` with zero Errors (Warnings are advisory).

- **Install** (one-time, user scope):
  ```powershell
  Install-Module -Name PSScriptAnalyzer -Force -SkipPublisherCheck -Scope CurrentUser
  ```
- **Run** on the current repo:
  ```powershell
  Invoke-ScriptAnalyzer -Path . -Recurse -Severity Error, Warning | Format-Table -AutoSize ScriptName, Line, RuleName, Severity, Message
  ```
- **Fleet just recipe**: `just ps-lint` (current dir) or `just ps-lint-repo repo-name`

At minimum, every `build.ps1`, `start.ps1`, and `deploy.ps1` in the fleet SHOULD be
linted before merge. The ~800 `Write-Host` warnings across fleet are acceptable for
console script output — use judgment on severity level.

- **NEVER use `$pid` as a variable name**: `$pid` is PowerShell's automatic variable for the current process ID. Assigning to `$pid` (`$pid = ...`) overwrites it, corrupting subsequent calls. Use `$targetPid` or `$owningPid` instead.
- **Script Line Endings**: Git hooks (`.git/hooks/*`) must use **LF** line endings. CRLF will break bash execution in Windows.
- **Quote Paths**: Wrap file paths in double quotes if they contain spaces.
- **NEVER use `Start-Process -Title`**: The `-Title` parameter was added in PowerShell 7 (Core). Windows PowerShell 5.1 has no such parameter and will crash with `A parameter cannot be found that matches parameter name 'Title'`. Use `Start-Process -FilePath $exe -ArgumentList $args -NoNewWindow:$false` without `-Title`, or use `Start-Process` in PS7-only scripts guarded by `$PSVersionTable.PSEdition`.

## Dry-Run First Pattern

Every destructive/modifying script SHOULD implement a `-DryRun` or `-WhatIf` switch:

```powershell
param([switch]$DryRun, [switch]$Force)
$ErrorActionPreference = "Stop"

foreach ($item in $items) {
    if ($DryRun) {
        Write-Host "[DRY-RUN] Would modify $item" -ForegroundColor Yellow
        continue
    }
    # actual modification
}
```

This applies to: batch renames, recursive find-replace, file moves, registry edits, git mass operations. Never run blind.

## Scope & Variable Gotchas (HIGH LEVERAGE)

PowerShell's **dynamic scope** causes subtle bugs when variables are modified inside loops or functions. The parent scope is NOT modified unless explicitly targeted.

### $script: prefix on function array writes

When a function appends to an array variable, it creates a **local copy** unless `$script:` is used:

```powershell
# WRONG — creates local $results, parent is empty
function Add-Item($v) { $results += $v }
$results = @(); Add-Item "x"; $results.Count  # → 0

# CORRECT — modifies script-level variable
function Add-Item($v) { $script:results += $v }
$results = @(); Add-Item "x"; $results.Count  # → 1
```

### foreach loop scope isolation

`foreach` and `ForEach-Object` create child scopes. Variables modified inside do NOT propagate to the parent unless using `$script:`:

```powershell
# WRONG — $found stays $false outside the loop
$found = $false
foreach ($item in $items) { if ($item -match "x") { $found = $true } }
# $found is STILL $false — the foreach scope created a local copy

# CORRECT — use $script: prefix inside the loop
$found = $false
foreach ($item in $items) { if ($item -match "x") { $script:found = $true } }
```

### [regex]::Matches() enumeration

`[regex]::Matches()` returns a `System.Text.RegularExpressions.MatchCollection`. When iterated inside a `foreach` loop that also modifies a parent-scope variable, the match enumeration may silently **yield zero results** even though `Count` is positive:

```powershell
# WRONG — may silently fail inside script scopes
foreach ($m in [regex]::Matches($text, 'pattern')) {
    $script:results += $m.Value  # foreach may see zero matches
}

# CORRECT — force evaluation before iteration
$matches = [regex]::Matches($text, 'pattern')
$count = $matches.Count  # force evaluation
foreach ($m in $matches) { ... }

# ALSO CORRECT — pipe to ForEach-Object (different scope behavior)
[regex]::Matches($text, 'pattern') | ForEach-Object { ... }

# BEST for reliable file scanning — Select-String is PowerShell-native
Select-String -Path $file -Pattern 'pattern' | ForEach-Object { ... }
```

### Rule of thumb

If a `foreach` loop or function modifies a **collection variable** (`$list += ...`), `[regex]::Matches()` result, or **boolean flag** (`$found = $true`), always use `$script:` prefix. Test in isolation before relying on the result outside the loop.

## Subprocess Spawning & Working Directory Pitfalls (CRITICAL)

### Pitfall 1: Double-Nesting Relative Working Directories
When launching a process via `Start-Process` or building an inline shell command (`powershell.exe -Command ...` or `cmd.exe /k ...`), **never** pass an unresolved relative directory both as `-WorkingDirectory` and inside `Set-Location`:
```powershell
# WRONG: if WorkDir is 'webapp\backend' and Cwd is already set to 'webapp\backend',
# Set-Location tries to resolve relative to Cwd, producing:
# 'D:\...\webapp\backend\webapp\backend' -> PathNotFound error!
$cmd = "Set-Location '$workDir'; uv run uvicorn ..."
Start-Process powershell.exe -WorkingDirectory $workDir -ArgumentList @('-Command', $cmd)

# CORRECT: Always anchor and resolve to an absolute path first
$resolvedWorkDir = if ([System.IO.Path]::IsPathRooted($workDir)) {
    $workDir
} else {
    Join-Path $RepoRoot $workDir
}
$resolvedWorkDir = (Resolve-Path -LiteralPath $resolvedWorkDir).Path
$cmd = "Set-Location '$resolvedWorkDir'; uv run uvicorn ..."
Start-Process powershell.exe -WorkingDirectory $resolvedWorkDir -ArgumentList @('-Command', $cmd)
```

### Pitfall 2: ConPTY Pipe Teardown Error `0x800700e8` (`ERROR_NO_DATA`)
On Windows 11 with Windows Terminal (`wt.exe` / OpenConsole), launching detached child consoles using `cmd.exe /c` or `powershell.exe` without `-NoExit` will cause Windows Terminal to display:
`[error 2147942632 (0x800700e8) when launching ...]`
if the child command encounters an immediate parse/runtime failure or exits too quickly. The instantaneous exit tears down the pseudoconsole pipe (`ConPTY`) before Windows Terminal attaches stdout/stderr.
- For interactive dev sessions: ALWAYS use `cmd.exe /k` (or `powershell.exe -NoExit`) so the window stays alive, preserving error output and preventing ConPTY pipe crashes.
- For automated probe / headless runs: conditionally switch to `/c` only when `$env:FLEET_PROBE_RUN -eq '1'` or `-Headless`.

### Pitfall 3: Private Monorepo Dependency Trap (CRITICAL ARCHITECTURAL PITFALL)
Repositories destined for public release or standalone use **MUST NEVER** require private infrastructure (e.g. `mcp-central-docs` or hardcoded `D:\Dev\repos` paths) to install, build, test, or launch.
- **WRONG**: A `start.ps1` that checks `Test-Path $EnginePath` and crashes if `mcp-central-docs` is missing. Public clones on external machines will fail immediately.
- **CORRECT (Bi-Modal Fallback)**:
  1. Check if the central fleet engine exists (`mcp-central-docs\scripts\Invoke-FleetWebappStart.ps1`).
  2. If present: delegate to the fleet engine for multi-repo orchestration and telemetry.
  3. If missing: gracefully drop into an autonomous standalone launcher that starts backend and frontend locally using the repo's own `fleet-start.config.ps1`.
- All paths in `fleet-start.config.ps1` must be **relative** (`webapp\backend`, `webapp\frontend`, `src`), never hardcoded to developer workstations (`D:\Dev\repos\...`).
