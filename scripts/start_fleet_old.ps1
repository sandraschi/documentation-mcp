# Fleet Dashboard Start Script - Clears port and runs discovery server
$WebPort = 10794
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 1. Clear port from zombies/squatters
try {
    Write-Host "[SOTA] Clearing port $WebPort..." -ForegroundColor Cyan
    npx --yes kill-port $WebPort 2>$null
}
catch {
    Write-Warning "Could not run kill-port. Attempting fallback..."
    Get-NetTCPConnection -LocalPort $WebPort -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# 2. Run discovery and serve
Write-Host "[SOTA] Launching Fleet Discovery Dashboard..." -ForegroundColor Green
Set-Location $ScriptDir
python fleet_discovery.py
