# Webapp Start - Standardized SOTA (Auto-Repaired V2.5)
# Usage: .\start.ps1              interactive (backend in new window, frontend in foreground)
#        .\start.ps1 -Automated   headless: start backend, wait, start frontend, wait, open browser, exit
param([switch]$Automated)

$WebPort = 11032
$BackendPort = 11033
$ProjectRoot = Split-Path -Parent $PSScriptRoot

$FleetStartPath = Join-Path $ProjectRoot "scripts\FleetStartMode.ps1"
if (-not (Test-Path -LiteralPath $FleetStartPath)) {
    Write-Host "ERROR: Missing vendored launcher helper: $FleetStartPath" -ForegroundColor Red
    exit 1
}
. $FleetStartPath
Stop-FleetPortSquatters -Ports @($WebPort, $BackendPort) -Label "documentation-mcp"

# 2. Setup
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) { npm install }

# Backend (docs_mcp) lives in repo root src/docs_mcp; run from repo root so paths resolve
$backendCmd = "`$env:PYTHONPATH = '$ProjectRoot;$ProjectRoot\src'; Set-Location '$ProjectRoot'; uv run --project '$ProjectRoot' uvicorn docs_mcp.server:app --host 127.0.0.1 --port $BackendPort --log-level info"

if ($Automated) {
    # 3a. Start backend in background (hidden)
    Write-Host "Starting Python backend on port $BackendPort ..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Hidden
    $backendUrl = "http://127.0.0.1:$BackendPort/api/settings"
    $waited = 0
    $maxWait = 60
    while ($waited -lt $maxWait) {
        try {
            $null = Invoke-WebRequest -Uri $backendUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
            break
        } catch {
            Start-Sleep -Seconds 1
            $waited++
        }
    }
    if ($waited -ge $maxWait) {
        Write-Host "Backend did not become ready in ${maxWait}s." -ForegroundColor Red
        exit 1
    }
    Write-Host "Backend ready." -ForegroundColor Green

    # 4a. Start frontend in background (hidden)
    Write-Host "Starting Vite frontend on port $WebPort ..." -ForegroundColor Cyan
    Start-Process -FilePath "npm" -ArgumentList "run", "dev", "--", "--port", $WebPort, "--host" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden
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

    # 5. Open browser and exit
    Start-Process $frontendUrl
    Write-Host "Browser opened at $frontendUrl" -ForegroundColor Green
    exit 0
}

# 3b. Interactive: Start backend in new visible window
Write-Host "Starting Python backend on port $BackendPort ..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Normal

# Wait for backend to be ready so proxy /api/* does not get ECONNREFUSED
$backendUrl = "http://127.0.0.1:$BackendPort/api/settings"
$waited = 0
$maxWait = 45
while ($waited -lt $maxWait) {
    try {
        $null = Invoke-WebRequest -Uri $backendUrl -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        Write-Host "Backend ready." -ForegroundColor Green
        break
    } catch {
        Start-Sleep -Seconds 1
        $waited++
    }
}
if ($waited -ge $maxWait) {
    Write-Host "Backend did not respond in ${maxWait}s. Starting frontend anyway; retry /api requests after backend is up." -ForegroundColor Yellow
}

# 4b. Launch background task to open browser once frontend is ready (Auto-opened by Antigravity)
$frontendUrl = "http://127.0.0.1:$WebPort/"
$pollAndOpen = "for (`$i = 0; `$i -lt 60; `$i++) { try { `$null = Invoke-WebRequest -Uri '$frontendUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; Start-Process '$frontendUrl'; exit } catch { Start-Sleep -Seconds 1 } }"
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $pollAndOpen

# 5b. Run frontend in foreground
Write-Host "Starting Vite frontend on port $WebPort ..." -ForegroundColor Green
Write-Host "Browser will open automatically when Vite is ready." -ForegroundColor Gray

# 4b. Launch background task to open browser once frontend is ready (Auto-opened by Antigravity)
$frontendUrl = "http://127.0.0.1:$WebPort/"
$pollAndOpen = "for (`$i = 0; `$i -lt 60; `$i++) { try { `$null = Invoke-WebRequest -Uri '$frontendUrl' -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop; Start-Process '$frontendUrl'; exit } catch { Start-Sleep -Seconds 1 } }"
Start-Process powershell -ArgumentList "-NoProfile", "-WindowStyle", "Hidden", "-Command", $pollAndOpen

Write-Host "Browser will open automatically when Vite is ready." -ForegroundColor Gray
npm run dev -- --port $WebPort --host




