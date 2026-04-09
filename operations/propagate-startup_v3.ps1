# SOTA Startup Propagation Tool: Stable Edition
$ReposRoot = "D:\Dev\repos"
$AuditFile = "$ReposRoot\mcp-central-docs\operations\startup_audit_report.csv"

$Template = @'
# Webapp Start - Standardized SOTA
$WebPort = [[WEB_PORT]]
$BackendPort = $WebPort + 1
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# 1. Kill any process squatting on the ports
Write-Host "Checking for port squatters on $WebPort and $BackendPort..." -ForegroundColor Yellow
$pids = Get-NetTCPConnection -LocalPort $WebPort, $BackendPort -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -gt 4 } | Select-Object -ExpandProperty OwningProcess -Unique
foreach ($p in $pids) {
    Write-Host "Found squatter (PID: $p). Terminating..." -ForegroundColor Red
    try { Stop-Process -Id $p -Force -ErrorAction Stop } catch { Write-Host "Warning: Could not terminate PID $p." -ForegroundColor Gray }
}

# 2. Setup
Set-Location $PSScriptRoot
if (-not (Test-Path "node_modules")) { npm install }

# 3. Start the Python backend in a new window
[[BACKEND_SECTION]]

# 4. Run server (Vite dev)
Write-Host "Starting Vite frontend on port $WebPort ..." -ForegroundColor Cyan
npm run dev -- --port $WebPort --host
'@

$BackendTemplate = @'
Write-Host "Starting Python backend on port $BackendPort ..." -ForegroundColor Cyan
$env:PYTHONPATH = "$ProjectRoot;$(Join-Path $ProjectRoot 'src')"
$backendCmd = "Set-Location '$ProjectRoot'; uv run uvicorn [[BACKEND_ENTRY]] --host 127.0.0.1 --port $BackendPort --log-level info"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Normal

# Give backend a moment to bind
Start-Sleep -Seconds 2
'@

$report = Import-Csv $AuditFile | Where-Object { $_.WebPort -ne "Unknown" }

foreach ($row in $report) {
    $scriptPath = Join-Path $ReposRoot $row.ScriptPath
    $projectRootPath = Split-Path (Split-Path $scriptPath -Parent) -Parent
    
    # Recursive Discovery
    $bEntry = $null
    $srcPath = Join-Path $projectRootPath "src"
    if (Test-Path $srcPath) {
        $foundFiles = Get-ChildItem -Path $srcPath -Filter "*.py" -Recurse | Where-Object { 
            $_.Name -match "^(http_server|main|server|app)\.py$" 
        }
        
        foreach ($f in $foundFiles) {
            $fContent = Get-Content $f.FullName -Raw
            if ($fContent -match "FastMCP|FastAPI|uvicorn") {
                $relPath = $f.FullName.Replace($srcPath, "").TrimStart("\")
                $bEntry = $relPath.Replace(".py", "").Replace("\", ".") + ":app"
                break
            }
        }
    }

    # Fallback to non-src
    if (-not $bEntry) {
        $foundFiles = Get-ChildItem -Path $projectRootPath -Filter "*.py" | Where-Object { 
            # Limit depth naturally by avoiding Recurse here
            $_.Name -match "^(http_server|main|server|app)\.py$" 
        }
        foreach ($f in $foundFiles) {
            $fContent = Get-Content $f.FullName -Raw
            if ($fContent -match "FastMCP|FastAPI|uvicorn") {
                $bEntry = $f.Name.Replace(".py", "") + ":app"
                break
            }
        }
    }

    Write-Host "Applying Fix: $($row.Repo)... (Backend: $($bEntry ?? 'None'))"
    $content = $Template.Replace("[[WEB_PORT]]", $row.WebPort)
    
    if ($bEntry) {
        $bSection = $BackendTemplate.Replace("[[BACKEND_ENTRY]]", $bEntry)
        $content = $content.Replace("[[BACKEND_SECTION]]", $bSection)
    }
    else {
        $content = $content.Replace("[[BACKEND_SECTION]]", 'Write-Host "No local backend service detected. Starting in frontend-only mode." -ForegroundColor Gray')
    }

    $content | Out-File $scriptPath -Encoding utf8
}

Write-Host "--- Fleet Optimization Complete ---" -ForegroundColor Green
