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

## Command Execution Substrate
Always use these absolute paths to ensure reliability:

| Tool | Absolute Path |
| :--- | :--- |
| **ripgrep (rg)** | `C:\Users\sandr\AppData\Local\Microsoft\WinGet\Links\rg.exe` |
| **just** | `C:\Users\scoop\shims\just.exe` |
| **Ruff** | `C:\Users\sandr\AppData\Local\Programs\Python\Python313\Scripts\ruff.exe` |
| **Biome** | `C:\Users\sandr\.local\bin\biome.exe` |
| **lake** | `$env:USERPROFILE\.elan\bin\lake.exe` |
| **bun** | `C:\Users\sandr\.bun\bin\bun.exe` |
| **uv** | `C:\Users\sandr\.local\bin\uv.exe` |
| **fd** | `C:\Users\sandr\.local\bin\fd.exe` |
| **PSScriptAnalyzer** | `C:\Users\sandr\OneDrive\Dokumente\PowerShell\Modules\PSScriptAnalyzer\1.25.0\PSScriptAnalyzer.psd1` |
| **markdownlint** | `C:\Users\sandr\AppData\Roaming\npm\markdownlint.cmd` |
| **yamllint** | `C:\Users\sandr\.local\bin\yamllint.exe` |
| **taplo** | `C:\Users\sandr\.cargo\bin\taplo.exe` |
| **hadolint** | `C:\Users\sandr\.local\bin\hadolint.exe` |
| **shellcheck** | `C:\Users\sandr\.local\bin\shellcheck.exe` |
| **actionlint** | `C:\Users\sandr\.local\bin\actionlint.exe` |
| **py** | `C:\Windows\py.exe` |
| **ollama** | `C:\Users\sandr\AppData\Local\Programs\Ollama\ollama.exe` |
| **winget** | `C:\Users\sandr\AppData\Local\Microsoft\WindowsApps\winget.exe` |
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
