# repair-start-scripts-v2-5.ps1
# DEPRECATED — this script minified/overwrote fleet start.ps1 and caused instacrash.
# Use scripts/repair-fleet-start-unminify.ps1 and scripts/repair-starts-launchers.ps1 instead.
Write-Host "ERROR: repair-start-scripts-v2-5.ps1 is DEPRECATED and must not be run." -ForegroundColor Red
Write-Host "Use: .\scripts\repair-fleet-start-unminify.ps1" -ForegroundColor Yellow
exit 1

# Mass repair for fleet start.ps1 files using webapp-registry.json for ports
# V2.5: Robust project detection and NO HALLUCINATION policy (registry required)

$BaseDir = "D:\Dev\repos"
$RegistryPath = "D:\Dev\repos\mcp-central-docs\operations\webapp-registry.json"
$Registry = Get-Content $RegistryPath | ConvertFrom-Json
$WebApps = $Registry.webapps

$StartScripts = Get-ChildItem -Path $BaseDir -Filter "start.ps1" -Recurse -Depth 3

foreach ($Script in $StartScripts) {
    if ($Script.FullName -match "node_modules") { continue }
    
    $Content = Get-Content $Script.FullName -Raw
    
    # Only target webapp start scripts
    if ($Content -match "npm run dev" -or $Content -match "uvicorn" -or $Content -match "python -m" -or $Content -match "Auto-Repaired") {
        
        # Robust Project Name Detection (Relative from BaseDir)
        $RelPath = $Script.FullName.Replace($BaseDir + "\", "")
        $ProjectName = $RelPath.Split("\")[0]
        $ProjectRoot = Join-Path $BaseDir $ProjectName
        
        Write-Host "Processing $($ProjectName) ($($Script.FullName))..." -ForegroundColor Cyan
        
        # Registry Lookup (Case-Insensitive)
        $MatchedApps = $WebApps | Where-Object { 
            $_.id -ieq $ProjectName -or 
            $_.id -match "^$($ProjectName)-" -or 
            $_.repo_path -replace "/", "\" -match "\\$($ProjectName)$" 
        }

        if (-not $MatchedApps) {
            Write-Warning "  SKIPPING: No registry entry found for '$ProjectName'. No hallucination allowed."
            continue
        }

        $WebPort = $null
        $BackendPort = $null
        
        $FrontendApp = $MatchedApps | Where-Object { $_.tags -contains "frontend" -or $_.id -imatch "frontend" } | Select-Object -First 1
        $BackendApp = $MatchedApps | Where-Object { $_.tags -contains "backend" -or $_.id -imatch "backend" } | Select-Object -First 1
        
        if ($FrontendApp) {
            $WebPort = $FrontendApp.port
            Write-Host "  Found Frontend Port: $WebPort" -ForegroundColor DarkGreen
        }
        elseif ($MatchedApps.Count -eq 1) {
            $WebPort = $MatchedApps[0].port
            Write-Host "  Found Port: $WebPort" -ForegroundColor DarkGreen
        }
        else {
            # Multiple matches but no clear frontend, pick first's port
            $WebPort = $MatchedApps[0].port
            Write-Host "  Picking default Port: $WebPort" -ForegroundColor Yellow
        }
        
        if ($BackendApp) {
            $BackendPort = $BackendApp.port
            Write-Host "  Found Backend Port: $BackendPort" -ForegroundColor DarkGray
        }
        else {
            $BackendPort = [int]$WebPort + 1
            Write-Host "  Guessed Backend Port: $BackendPort" -ForegroundColor DarkGray
        }

        # 1. Package name detection
        $ModuleName = $ProjectName -replace "-", "_" # Default guess
        $SrcDir = Join-Path $ProjectRoot "src"
        if (Test-Path $SrcDir) {
            $SubDirs = Get-ChildItem -Path $SrcDir -Directory
            if ($SubDirs.Count -gt 0) {
                # Pick the most likely package (ignores .egg-info)
                $LikelyPkg = $SubDirs | Where-Object { $_.Name -notmatch "egg-info" -and $_.Name -notmatch "__pycache__" } | Select-Object -First 1
                if ($LikelyPkg) {
                    $ModuleName = $LikelyPkg.Name
                }
            }
        }

        # 2. Determine uvicorn entry point
        $EntryPoint = "${ModuleName}.server:app"
        if ($Content -match "server:mcp\.app") { $EntryPoint = "${ModuleName}.server:mcp.app" }
        elseif ($Content -match "web_bridge:app") { $EntryPoint = "${ModuleName}.web_bridge:app" }
        elseif ($Content -match "webapp\.backend\.main:app") { $EntryPoint = "webapp.backend.main:app" }
        elseif ($ModuleName -eq "llm_txt_mcp") { $EntryPoint = "llm_txt_mcp.main:app" }
        
        # Refine for src/ layout
        if (Test-Path (Join-Path $SrcDir $ModuleName)) {
            if (Test-Path (Join-Path $SrcDir (Join-Path $ModuleName "server.py"))) {
                $EntryPoint = "${ModuleName}.server:app"
            }
            elseif (Test-Path (Join-Path $SrcDir (Join-Path $ModuleName "web_bridge.py"))) {
                $EntryPoint = "${ModuleName}.web_bridge:app"
            }
        }

        $SOTATemplate = @"
# Webapp Start - Standardized SOTA (Auto-Repaired V2.5)
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

# Use TRIPLE backtick to ensure `$env:PYTHONPATH reaches the REAL shell
`$backendCmd = "```$env:PYTHONPATH = '$ProjectRoot;$(Join-Path $ProjectRoot 'src')'; Set-Location '$ProjectRoot'; uv run uvicorn $EntryPoint --host 127.0.0.1 --port `$BackendPort --log-level info"

Start-Process powershell -ArgumentList "-NoExit", "-Command", `$backendCmd -WindowStyle Normal

# 4. Run server (Vite dev)
Write-Host "Starting Vite frontend on port `$WebPort ..." -ForegroundColor Green
npm run dev -- --port `$WebPort --host
"@

        $SOTATemplate | Out-File $Script.FullName -Encoding utf8
    }
}

Write-Host "Mass repair V2.5 complete." -ForegroundColor Green
