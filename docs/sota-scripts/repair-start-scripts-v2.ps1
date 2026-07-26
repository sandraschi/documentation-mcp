# repair-start-scripts-v2.ps1
# Mass repair for fleet start.ps1 files using webapp-registry.json for ports

$BaseDir = "D:\Dev\repos"
$RegistryPath = "D:\Dev\repos\mcp-central-docs\operations\webapp-registry.json"
$Registry = Get-Content $RegistryPath | ConvertFrom-Json

$StartScripts = Get-ChildItem -Path $BaseDir -Filter "start.ps1" -Recurse -Depth 3

foreach ($Script in $StartScripts) {
    if ($Script.FullName -match "node_modules") { continue }
    
    $Content = Get-Content $Script.FullName -Raw
    
    # Only target webapp start scripts
    if ($Content -match "npm run dev" -or $Content -match "uvicorn" -or $Content -match "python -m") {
        
        $ProjectRoot = Split-Path -Parent $Script.Directory.FullName
        $ProjectName = $Script.Directory.Parent.Name
        $ModuleName = $ProjectName -replace "-", "_"
        
        Write-Host "Processing $($ProjectName) ($($Script.FullName))..." -ForegroundColor Cyan
        
        # 1. Look up ports in registry
        $MatchedApps = $Registry.webapps | Where-Object { $_.id -eq $ProjectName -or $_.id -match "^$($ProjectName)-" -or $_.repo_path -match "/$($ProjectName)$" }
        
        $WebPort = 10700 # Default fallback
        $BackendPort = 10701
        
        $FrontendApp = $MatchedApps | Where-Object { $_.tags -contains "frontend" -or $_.id -match "frontend" } | Select-Object -First 1
        $BackendApp = $MatchedApps | Where-Object { $_.tags -contains "backend" -or $_.id -match "backend" } | Select-Object -First 1
        
        if ($FrontendApp) {
            $WebPort = $FrontendApp.port
            Write-Host "  Found Frontend Port: $WebPort" -ForegroundColor DarkGreen
        }
        elseif ($MatchedApps.Count -eq 1) {
            $WebPort = $MatchedApps[0].port
            Write-Host "  Found Single Port: $WebPort" -ForegroundColor DarkGreen
        }
        
        if ($BackendApp) {
            $BackendPort = $BackendApp.port
            Write-Host "  Found Backend Port: $BackendPort" -ForegroundColor DarkGray
        }
        else {
            $BackendPort = [int]$WebPort + 1
            Write-Host "  Guessed Backend Port: $BackendPort" -ForegroundColor DarkGray
        }

        # 2. Determine likely uvicorn entry point
        $EntryPoint = "${ModuleName}.server:app"
        if ($Content -match "server:mcp.app") { $EntryPoint = "${ModuleName}.server:mcp.app" }
        elseif ($Content -match "web_bridge:app") { $EntryPoint = "src.${ModuleName}.web_bridge:app" }
        elseif ($Content -match "webapp.backend.main:app") { $EntryPoint = "webapp.backend.main:app" }
        
        $SOTATemplate = @"
# Webapp Start - Standardized SOTA (Auto-Repaired V2)
`$WebPort = $WebPort
`$BackendPort = $BackendPort
`$ProjectRoot = Split-Path -Parent `$PSScriptRoot

# 1. Kill any process squatting on the ports
Write-Host "Checking for port squatters on `$WebPort and `$BackendPort..." -ForegroundColor Yellow
`$pids = Get-NetTCPConnection -LocalPort `$WebPort, `$BackendPort -ErrorAction SilentlyContinue | Where-Object { `$_.OwningProcess -gt 4 } | Select-Object -ExpandProperty OwningProcess -Unique
foreach (`$p in `$pids) {
    Write-Host "Found squatter (PID: `$p). Terminating...\" -ForegroundColor Red
    try { Stop-Process -Id `$p -Force -ErrorAction Stop } catch { Write-Host \"Warning: Could not terminate PID `$p.\" -ForegroundColor Gray }
}

# 2. Setup
Set-Location `$PSScriptRoot
if (-not (Test-Path \"node_modules\")) { npm install }

# 3. Start the Python backend (Background)
Write-Host \"Starting Python backend on port `$BackendPort ...\" -ForegroundColor Cyan
`$env:PYTHONPATH = \"`$ProjectRoot;`$(Join-Path `$ProjectRoot \'src\')\"
`$backendCmd = \"``$env:PYTHONPATH = \'`$ProjectRoot;`$(Join-Path `$ProjectRoot \'src\')\'; Set-Location \'`$ProjectRoot\'; uv run uvicorn $EntryPoint --host 127.0.0.1 --port `$BackendPort --log-level info\"
Start-Process powershell -ArgumentList \"-NoExit\", \"-Command\", `$backendCmd -WindowStyle Normal

# 4. Run server (Vite dev)
Write-Host \"Starting Vite frontend on port `$WebPort ...\" -ForegroundColor Green
npm run dev -- --port `$WebPort --host
"@

        $SOTATemplate | Out-File $Script.FullName -Encoding utf8
    }
}

Write-Host "Mass repair V2 complete." -ForegroundColor Green
