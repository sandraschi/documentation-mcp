### 7. justfile MUST use `powershell.exe`, not `pwsh.exe`

`pwsh.exe` is PowerShell 7+, which is NOT installed on a naked PC.
`powershell.exe` is Windows PowerShell 5.1, which ships with every Windows 10/11.

```justfile
# CORRECT
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

# WRONG -- pwsh is not installed on naked PCs
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
```

Note: use `windows-shell` (not `shell`) so that just falls back to sh on
Linux/macOS if anyone runs these recipes cross-platform.

### 8. Never use `$ErrorActionPreference = "Stop"` globally

winget returns non-zero exit codes for conditions that are not errors — most
notably "package already installed" (exit code `-1978335189`). With `Stop` mode,
PowerShell treats this as a terminating error and crashes the window instantly
before printing anything, which looks like an instacrash with no output.

```powershell
# WRONG -- crashes on winget "already installed" exit code
$ErrorActionPreference = "Stop"

# CORRECT -- handle errors explicitly where they matter
# (leave ErrorActionPreference at default: Continue)
```

Where you need to abort on failure, check `$LASTEXITCODE` explicitly after
each critical command and call `exit 1` with a clear message:

```powershell
& $uvExe sync --project $RepoRoot
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: uv sync failed." -ForegroundColor Red
    exit 1
}
```
title: "Naked-PC Install Standard"
category: standard
status: active
audience: mcp-dev
related:
  - standards/WEBAPP_STANDARDS.md
  - operations/WEBAPP_PORTS.md
last_updated: 2026-04-24
---

# Naked-PC Install Standard

**Every MCP webapp start.ps1 MUST work on a fresh Windows machine with nothing pre-installed.**

This standard exists because non-dev users (e.g. Steve) hit blockers like
"vite not found" or "uv not recognised" when cloning a repo and double-clicking
start.bat. These are silent assumptions baked into start.ps1 that break on any
machine that isn't Sandra's Goliath.

---

## What "naked PC" means

A machine with only a stock Windows install — no Python, no Node.js, no npm,
no vite, no uv, no pip, no just, no git beyond what Windows ships with.
The only assumption is winget (available on Windows 10 1809+ and all Windows 11).

## The full dependency chain

```
winget  →  uv        →  Python 3.11+ (auto-fetched by uv)
                     →  .venv with all Python deps

winget  →  Node.js   →  npm
                     →  node_modules/.bin/vite (and all other local frontend tools)

winget  →  just      →  available as `just` in PowerShell after install
                        (justfile must declare: set shell := ["powershell.exe", ...])
```

**Four winget calls covers everything on a naked PC:**

**Python does NOT need to be installed separately.** uv has managed its own
CPython downloads since v0.2.x. When `uv sync` runs on a machine with no Python,
it reads `requires-python` from `pyproject.toml` and downloads the appropriate
CPython automatically into its own cache. This means:

- `Require-Command "uv"` covers Python implicitly
- Every repo MUST declare `requires-python = ">=3.11"` (or appropriate version) in pyproject.toml
- Never add a separate `Require-Command "python"` — it's redundant and would
  install a system Python that uv ignores anyway

**vite, ruff, tailwind, typescript** are all local devDependencies — installed
by `npm install` into `node_modules/`. They must never be required globally.

**just is installed by start.bat and IS available on all customer PCs after first run.**

`just` has a clean winget entry (`Casey.Just`, updated weekly, currently v1.49.0).
Add it to the `Require-Command` chain in every start.ps1 and it becomes available
fleet-wide with no manual action from the user.

One Windows-specific issue: `just` defaults to `sh` as its shell, which requires
Git Bash or Cygwin. Since the fleet uses PowerShell, every justfile MUST declare:

```justfile
set shell := ["powershell.exe", "-NoProfile", "-Command"]
```

Without this, recipes will fail on machines that don't have Git Bash installed.



### 1. Prereq guard via winget

Include `Require-Command` and call it for `uv`, `node`/`npm`, and `just`.
**Important:** winget lives in `%LOCALAPPDATA%\Microsoft\WindowsApps` which is
absent from child PowerShell sessions launched by `.bat` files. Always probe by
path, and always inject the path into the bat before calling PowerShell:

**In every `.bat` launcher — add this line before the powershell call:**
```bat
set "PATH=%PATH%;%LOCALAPPDATA%\Microsoft\WindowsApps"
```

**In start.ps1 — probe for winget by path, not just by name:**

```powershell
function Require-Command {
    param([string]$Cmd, [string]$WingetId, [string]$Label)
    if (Get-Command $Cmd -ErrorAction SilentlyContinue) {
        Write-Host "  [ok] $Label" -ForegroundColor DarkGreen
        return
    }
    Write-Host "  [--] $Label not found - installing via winget ..." -ForegroundColor Yellow
    # Probe for winget by full path -- WindowsApps often absent from child-session PATH
    $wingetExe = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $wingetExe) {
        $candidates = @(
            "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe",
            "$env:PROGRAMFILES\WindowsApps\Microsoft.DesktopAppInstaller_*\winget.exe"
        )
        foreach ($c in $candidates) {
            $found = Get-Item $c -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) { $wingetExe = $found.FullName; break }
        }
    } else { $wingetExe = $wingetExe.Source }
    if (-not $wingetExe) {
        Write-Host "ERROR: winget not found. Install $Label manually (id: $WingetId)" -ForegroundColor Red
        exit 1
    }
    & $wingetExe install --id $WingetId --silent --accept-source-agreements --accept-package-agreements
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
    if (-not (Get-Command $Cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Installed $Label but '$Cmd' not in PATH yet. Reopen PowerShell and retry." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "  [ok] $Label installed" -ForegroundColor Green
}

Require-Command "uv"   "Astral.uv"         "uv (Python package manager)"
Require-Command "node" "OpenJS.NodeJS.LTS"  "Node.js LTS"
Require-Command "npm"  "OpenJS.NodeJS.LTS"  "npm"
Require-Command "just" "Casey.Just"         "just (command runner)"
```

Winget is available on Windows 10 1809+ and all Windows 11. If a user somehow
lacks winget, the error message tells them the winget ID to install manually.

### 2. Resolve uv path — never call bare `uv`

```powershell
$uvExe = (Get-Command uv).Source
& $uvExe sync --project $RepoRoot
```

Bare `uv` on some machines resolves to a PATH shim that fails in non-interactive
PowerShell sessions. Using the resolved path is reliable everywhere.

### 3. npm install only if node_modules is absent

```powershell
$npmExe = (Get-Command npm).Source
if (-not (Test-Path (Join-Path $WebRoot "node_modules"))) {
    Push-Location $WebRoot
    & $npmExe install --prefer-offline 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: npm install failed." -ForegroundColor Red
        Pop-Location; exit 1
    }
    Pop-Location
}
```

`--prefer-offline` uses the npm cache on repeat installs (faster for dev).

### 4. Explicit vite guard after npm install

This is the exact bug Steve hit. vite is a devDependency — it must be local:

```powershell
# npm: node_modules/.bin/vite or vite.cmd
# Bun (Windows): node_modules/.bin/vite.exe or vite.bunx - NOT a bare "vite" file
function Test-ViteBinPresent {
    param([string]$WebRootPath)
    $bin = Join-Path $WebRootPath "node_modules\.bin"
    foreach ($name in @('vite', 'vite.cmd', 'vite.exe', 'vite.bunx')) {
        if (Test-Path -LiteralPath (Join-Path $bin $name)) { return $true }
    }
    return (Test-Path -LiteralPath (Join-Path $WebRootPath "node_modules\vite\package.json"))
}
if (-not (Test-ViteBinPresent -WebRootPath $WebRoot)) {
    Write-Host "ERROR: vite missing from node_modules after install." -ForegroundColor Red
    Write-Host "Delete '$WebRoot\node_modules' and re-run." -ForegroundColor Yellow
    exit 1
}
```

If `node_modules` exists but vite bins are missing (stale partial install), **re-run** `bun install` / `npm install` instead of skipping.

### 5. Import smoke-test before the health-wait loop

The health-wait loop will spin for 90 seconds if the backend crashes on startup.
A 2-second import check surfaces the error immediately:

```powershell
& $uvExe run --project $RepoRoot python -c "import mypackage.api; print('  [ok] Import OK')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: import check failed -- see output above." -ForegroundColor Red
    exit 1
}
```

### 6. Helpful error on health timeout

```powershell
if (-not $ready) {
    Write-Host "ERROR: backend health timed out after ${maxWait}s." -ForegroundColor Red
    Write-Host "Run this directly to see the error:" -ForegroundColor Yellow
    Write-Host "  cd $RepoRoot; $uvExe run python -m mypackage.api" -ForegroundColor Yellow
    exit 1
}
```

---

## What MUST be local (never assumed global)

| Tool | Location | How installed |
|---|---|---|
| vite | `webapp/node_modules/.bin/vite` (npm) or `vite.exe` (Bun on Windows) | `bun install` / `npm install` (devDependency) |
| tailwindcss | `webapp/node_modules/.bin/tailwindcss` | `npm install` |
| typescript / tsc | `webapp/node_modules/.bin/tsc` | `npm install` |
| ruff | `.venv/Scripts/ruff.exe` | `uv sync` (dev dep) |
| pytest | `.venv/Scripts/pytest.exe` | `uv sync` (dev dep) |

## What CAN be assumed (present on Sandra's Goliath, not on Steve's machine)

Nothing. Assume zero. winget handles it.

### 9. ASCII-only text in `start.ps1` / `start.bat` (no em dash)

**EM DASH (`—`, U+2014) is never allowed** anywhere in launcher scripts - including comments and `Write-Host` strings. UTF-8 without BOM on Windows PowerShell 5.1 corrupts these characters and breaks parsing (see [Unicode Safety](./patterns/unicode_safety.md)).

Use ASCII `-` or ` -- ` only. Enforce with:

```powershell
powershell.exe -NoProfile -File D:\Dev\repos\mcp-central-docs\scripts\check-unicode-safe.ps1 -RepoPath .
```

## INSTALL.md requirement

Full-stack repos: **`webapp/start.ps1`** + **`webapp/start.bat`** are canonical; repo-root **`start.bat`** should delegate (see [START_SCRIPT_STANDARD.md](./START_SCRIPT_STANDARD.md), [templates/start-root.bat](./templates/start-root.bat)). MCD shortcuts: [just-starts/README.md](../just-starts/README.md).

Every repo with a start.bat MUST have an `INSTALL.md` at the root with:
1. The two-command quick start (`git clone` + `start.bat`)
2. A manual step-by-step for when start.bat itself fails
3. A table of what is/isn't required globally

See `D:\Dev\repos\aiwatcher-mcp\INSTALL.md` as the reference implementation.

---

## Fleet remediation status

| Repo | Status |
|---|---|
| aiwatcher-mcp | Fixed 2026-04-24 |
| arxiv-mcp | Fixed 2026-04-24 |
| chip-design-mcp | Fixed 2026-05-31 (`start.bat` PATH + pause, `just` chain, `powershell.exe`) |
| All others | TODO — scan needed |

To find all start.ps1 files still using bare `npm install` without node check:

```powershell
Get-ChildItem D:\Dev\repos -Recurse -Filter "start.ps1" |
    Select-String "npm install" |
    Where-Object { $_.Line -notmatch "Require-Command" } |
    Select-Object -ExpandProperty Path |
    Sort-Object -Unique
```
