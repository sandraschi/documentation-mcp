# repair-start-scripts.ps1
# Mass repair for fleet start.ps1 files to SOTA standards

$BaseDir = "D:\Dev\repos"
$StartScripts = Get-ChildItem -Path $BaseDir -Filter "start.ps1" -Recurse -Depth 3

foreach ($Script in $StartScripts) {
    $Content = Get-Content $Script.FullName -Raw
    
    # Only target webapp start scripts
    if ($Content -match "npm run dev" -or $Content -match "uvicorn" -or $Content -match "python -m") {
        Write-Host "Repairing $($Script.FullName)..." -ForegroundColor Cyan
        
        $ProjectRoot = Split-Path -Parent $Script.Directory.FullName
        $ProjectName = $Script.Directory.Parent.Name
        $ModuleName = $ProjectName -replace "-", "_"
        
        # Determine likely uvicorn entry point
        $EntryPoint = "${ModuleName}.server:app"
        if ($Content -match "server:mcp.app") { $EntryPoint = "${ModuleName}.server:mcp.app" }
        elseif ($Content -match "web_bridge:app") { $EntryPoint = "src.${ModuleName}.web_bridge:app" }
        
        # Determine Ports (if possible)
        $WebPort = 10700 # Default
        if ($Content -match "\$WebPort\s*=\s*(\d+)") { $WebPort = $matches[1] }
        elseif ($Content -match "--port\s+(\d+)") { $WebPort = $matches[1] }
        
        $BackendPort = [int]$WebPort + 1
        
        $SOTATemplate = @"
# Webapp Start - Standardized SOTA (Auto-Repaired)
`$WebPort = $WebPort
`$BackendPort = $BackendPort
`$ProjectRoot = Split-Path -Parent `$PSScriptRoot

# 1. Kill any process squatting on the ports
Write-Host "Checking for port squatters on `$WebPort and `$BackendPort..." -ForegroundColor Yellow
`$pids = Get-NetTCPConnection -LocalPort `$WebPort, `$BackendPort -ErrorAction SilentlyContinue | Where-Object { `$_.OwningProcess -gt 4 } | Select-Object -ExpandProperty OwningProcess -Unique
foreach (`$p in `$pids) {
    Write-Host "Found squatter (PID: `$p). Terminating..." -ForegroundColor Red
    try { Stop-Process -Id `$p -Force -ErrorAction Stop } catch { Write-Host "Warning: Could not terminate PID `$p." -ForegroundColor Gray }
}

# 2. Setup
Set-Location `$PSScriptRoot
if (-not (Test-Path "node_modules")) { npm install }

# 3. Start the Python backend (Background)
Write-Host "Starting Python backend on port `$BackendPort ..." -ForegroundColor Cyan
`$env:PYTHONPATH = "`$ProjectRoot;`$(Join-Path `$ProjectRoot 'src')"
`$backendCmd = "``$env:PYTHONPATH = '`$ProjectRoot;`$(Join-Path `$ProjectRoot 'src')'; Set-Location '`$ProjectRoot'; uv run uvicorn $EntryPoint --host 127.0.0.1 --port `$BackendPort --log-level info"
Start-Process powershell -ArgumentList "-NoExit", "-Command", `$backendCmd -WindowStyle Normal

# 4. Run server (Vite dev)
Write-Host "Starting Vite frontend on port `$WebPort ..." -ForegroundColor Green
npm run dev -- --port `$WebPort --host
"@

        $SOTATemplate | Out-File $Script.FullName -Encoding utf8
    }
}

Write-Host "Mass repair complete." -ForegroundColor Green
