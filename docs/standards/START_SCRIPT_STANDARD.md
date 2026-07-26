# start.ps1 — Fleet Standard (SOTA 2026)

**Status:** Active
**Last updated:** 2026-07-12
**Template:** `mcp-server-template/start.ps1`

---

## Why

The `start.ps1` is the day-one touchpoint for every user, every CI run, and every probe. A broken start script means the repo looks dead. A fleet-wide audit found four distinct code qualities across 167 repos — from 15-line stubs with no port clearing to 200-line orchestration scripts with FleetStartMode.ps1 delegation.

This standard defines the minimum viable start script that every repo MUST have.

---

## Requirements

### R1: Port Zombie Kill (MANDATORY)

Before binding ANY port, the script MUST kill any existing process on that port:

```powershell
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  Killing zombie on :$Port (PID $($_.OwningProcess))" -ForegroundColor Yellow
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}
```

Without this, restarting a server after Ctrl+C gives `address already in use` because the OS hasn't released the port.

### R2: Health Poll After Backend Start (MANDATORY)

After launching the backend, poll `/api/health` for up to 60 seconds before declaring success:

```powershell
$ok = $false
for ($i = 0; $i -lt 60; $i++) {
    try {
        $r = Invoke-WebRequest -Uri $HealthEndpoint -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $ok = $true; break }
    } catch {}
    Start-Sleep 1
}
```

Without this, the frontend starts before the backend is listening, and the user sees "Connection refused" in the browser.

### R3: Browser Auto-Open (RECOMMENDED)

After both backend and frontend are ready, open the frontend URL in the default browser:

```powershell
if (-not $Headless -and -not $NoBrowser -and -not $BackendOnly) {
    Start-Sleep 3
    Start-Process "http://127.0.0.1:$FrontendPort"
}
```

The `-NoBrowser` flag allows headless/server deployments to suppress this.

### R4: Require-Command Prereq Checks (RECOMMENDED)

For naked-PC users who don't have Python/Node on PATH, auto-install via winget:

```powershell
function Require-Command {
    param([string]$Cmd, [string]$WingetId, [string]$Label)
    if (Get-Command $Cmd -ErrorAction SilentlyContinue) { return }
    Write-Host "  $Label not found - installing via winget..."
    winget install --id $WingetId --silent --accept-source-agreements --accept-package-agreements
    # Refresh PATH after install
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
}
```

### R5: Headless Mode (MANDATORY for CI)

Every start.ps1 MUST support `-Headless` for CI and fleet-probe contexts:

```powershell
param([switch]$Headless)

if ($Headless -and ($Host.UI.RawUI.WindowTitle -notmatch 'Hidden')) {
    Start-Process pwsh -ArgumentList '-NoProfile', '-File', $PSCommandPath, '-Headless' -WindowStyle Hidden
    exit
}
```

### R6: `npm install` Guard (RECOMMENDED)

Skip `npm install` when `node_modules` already exists — cuts startup time from 30s to 2s on repeat runs:

```powershell
if (-not (Test-Path (Join-Path $WebRoot "node_modules"))) {
    Push-Location $WebRoot
    npm install
    Pop-Location
}
```

---

## start.bat — Bootstrapper

Every repo MUST have a `start.bat` at the repo root that delegates to `start.ps1`:

```bat
@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1" %*
```

This is the double-click entry point for users who don't know about PowerShell.

---

## Parameter Contract

Every start.ps1 SHOULD accept these switches:

| Switch | Effect |
|--------|--------|
| `-Headless` | Hide all windows (for CI, probes) |
| `-BackendOnly` | Start backend only, no frontend |
| `-FrontendOnly` | Start frontend only, no backend |
| `-NoBrowser` | Don't open browser automatically |

---

## Fleet Audit

Run `scripts/audit-start-scripts.ps1` to check all 167 repos for compliance:

```powershell
.\scripts\audit-start-scripts.ps1            # Summary report
.\scripts\audit-start-scripts.ps1 -Detail    # Per-repo breakdown
```

The script checks for:
- Presence of both `start.ps1` and `start.bat`
- Port kill logic (`Get-NetTCPConnection` presence)
- Health poll (`Invoke-WebRequest` in a loop)
- Headless mode switch
- Browser auto-open logic

---

## Template

The canonical reference is `mcp-server-template/start.ps1`. Copy it when scaffolding a new repo, then customize the six config variables at the top:

```powershell
$RepoName = "your-mcp-name"
$BackendPort = 10700
$FrontendPort = 10701
$HealthEndpoint = "http://127.0.0.1:$BackendPort/api/health"
$BackendPackage = "your_package.server"
$WebRoot = Join-Path $PSScriptRoot "web_sota"
```

---

## Naked-PC Note

For Steve-class users (no Python, no Node, no git), the `Require-Command` function auto-installs missing tools via winget. This is the fleet's first line of naked-PC defense. See `NAKED_PC_INSTALL_STANDARD.md` for the full protocol.
