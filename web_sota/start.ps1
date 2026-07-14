# Webapp Start - Standardized SOTA (Auto-Repaired V2.5)
# Usage: .\start.ps1              interactive (backend in new window, frontend in foreground)
#        .\start.ps1 -Automated   headless: start backend, wait, start frontend, wait, open browser, exit
param([switch]$Automated,
    [switch]$ReuseIfRunning)

$WebPort = 11032
$BackendPort = 11033

$portResolve = @{
    Ports      = @($WebPort, $BackendPort)
    Label      = "documentation-mcp"
    AllowReuse = $ReuseIfRunning
}
if ($ReuseIfRunning) {
    $portResolve.HealthChecks = @{
        $WebPort = "http://127.0.0.1:$WebPort/"
        $BackendPort = "http://127.0.0.1:$BackendPort/health"
    }
}
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Source fleet helpers BEFORE using them
$FleetStartPath = Join-Path $ProjectRoot "scripts\FleetStartMode.ps1"
if (-not (Test-Path -LiteralPath $FleetStartPath)) {
    Write-Host "ERROR: Missing vendored launcher helper: $FleetStartPath" -ForegroundColor Red
    exit 1
}
. $FleetStartPath

$portState = Resolve-FleetPortConflict @portResolve
if ($portState.Action -eq 'Blocked') { exit 1 }
if ($portState.Reuse) { return }

# 2. Setup
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) { npm install }

# Log directory for backend crashes
$logDir = Join-Path $ProjectRoot "logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$backendLog = Join-Path $logDir "backend-startup.log"

# Backend (docs_mcp) lives in repo root src/docs_mcp; run from repo root so paths resolve
# Backend stderr is captured to a log file so crash details can be surfaced.
# NOTE: $ErrorActionPreference = 'Stop' is NOT set — it would turn native
# stderr (uv/uvicorn errors) into a terminating error that bypasses 2>>
# redirection, making crashes invisible.
$backendCmd = "`$env:PYTHONPATH = '$ProjectRoot;$ProjectRoot\src'; "`
    + "Set-Location '$ProjectRoot'; "`
    + "uv run --project '$ProjectRoot' uvicorn docs_mcp.server:app --host 127.0.0.1 --port $BackendPort --log-level info "`
    + "2>> '$backendLog'"

$backendUrl = "http://127.0.0.1:$BackendPort/api/settings"

# Drain TIME_WAIT on target ports so uvicorn can bind without --reuse-port
function Clear-FleetTimeWait {
    param([int[]]$Ports, [int]$MaxWaitSec = 60)
    for ($i = 0; $i -lt $MaxWaitSec; $i++) {
        $tw = @()
        foreach ($port in $Ports) {
            $raw = cmd /c "netstat -ano -p TCP 2>nul | findstr TIME_WAIT" 2>$null
            foreach ($line in ($raw -split "`r?`n")) {
                if ($line -match ":${port}\s") { $tw += $port; break }
            }
        }
        if ($tw.Count -eq 0) { return $true }
        Start-Sleep -Seconds 1
    }
    Write-Host "WARNING: TIME_WAIT not cleared on ports $($tw -join ', ') after ${MaxWaitSec}s" -ForegroundColor Yellow
    return $false
}

function Start-BackendAndPoll {
    param([switch]$Hidden)
    $ws = if ($Hidden) { "Hidden" } else { "Normal" }
    # Wait for TIME_WAIT to clear before launching
    Clear-FleetTimeWait -Ports @($BackendPort) -MaxWaitSec 60 | Out-Null
    $proc = Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle $ws -PassThru
    Write-Host "Backend PID: $($proc.Id)" -ForegroundColor DarkGray

    $waited = 0
    $maxWait = 60
    while ($waited -lt $maxWait) {
        try {
            $null = Invoke-WebRequest -Uri $backendUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            Write-Host "Backend ready." -ForegroundColor Green
            return $proc
        } catch {
            $proc.Refresh()
            if ($proc.HasExited) {
                break
            }
            Start-Sleep -Seconds 1
            $waited++
        }
    }

    # Backend failed to become ready
    $proc.Refresh()
    Write-Host "" -ForegroundColor Red
    Write-Host "=== Backend startup FAILED ===" -ForegroundColor Red
    if ($proc.HasExited) {
        Write-Host "Process exited with code $($proc.ExitCode)" -ForegroundColor Red
    } else {
        Write-Host "Process still alive after ${maxWait}s -- may be stuck or slow" -ForegroundColor Yellow
    }
    if (Test-Path $backendLog) {
        $crashLog = Get-Content $backendLog -Raw
        if ($crashLog.Trim()) {
            Write-Host "--- Backend stderr ---" -ForegroundColor Red
            Write-Host $crashLog
            Write-Host "--- end ---" -ForegroundColor Red
        }
    }
    Write-Host "Full log: $backendLog" -ForegroundColor DarkGray
    return $null
}

if ($Automated) {
    $proc = Start-BackendAndPoll -Hidden
    if (-not $proc) { exit 1 }

    # 4a. Start frontend in background (hidden)
    # NOTE: npm is npm.ps1 (not an exe), so Start-Process needs powershell.exe as the file path
    Write-Host "Starting Vite frontend on port $WebPort ..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoProfile", "-Command", "npm run dev -- --port $WebPort --host" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
    $frontendUrl = "http://127.0.0.1:$WebPort/"
    $waited = 0
    $maxWait = 30
    while ($waited -lt $maxWait) {
        try {
            $null = Invoke-WebRequest -Uri $frontendUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            break
        } catch {
            Start-Sleep -Seconds 1
            $waited++
        }
    }
    if ($waited -ge $maxWait) {
        Write-Host "Frontend did not become ready in ${maxWait}s." -ForegroundColor Red
        exit 1
    }
    Write-Host "Frontend ready." -ForegroundColor Green

    Start-Process $frontendUrl
    Write-Host "Browser opened at $frontendUrl" -ForegroundColor Green
    exit 0
}

# Interactive mode
$proc = Start-BackendAndPoll
if (-not $proc) {
    Write-Host "Backend failed to start. Frontend would have no API to connect to." -ForegroundColor Red
    Write-Host "Fix the error above, then re-run start.bat." -ForegroundColor Yellow
    exit 1
}

# 4b. Launch background task to open browser once frontend is ready
$frontendUrl = "http://127.0.0.1:$WebPort/"
$pollAndOpen = "for (`$i = 0; `$i -lt 60; `$i++) { try { `$null = Invoke-WebRequest -Uri '$frontendUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; Start-Process '$frontendUrl'; exit } catch { Start-Sleep -Seconds 1 } }"
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $pollAndOpen

# 5b. Run frontend in foreground
Write-Host "Starting Vite frontend on port $WebPort ..." -ForegroundColor Green
Write-Host "Browser will open automatically when Vite is ready." -ForegroundColor Gray

npm run dev -- --port $WebPort --host





