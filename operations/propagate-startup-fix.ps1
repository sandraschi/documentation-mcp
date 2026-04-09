# SOTA Startup Propagation Tool: Template-Based
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

$report = Import-Csv $AuditFile | Where-Object { $_.BackendSync -eq "False" -or $_.PidStable -eq "False" }

foreach ($row in $report) {
    if ($row.WebPort -eq "Unknown") { continue }
    
    $scriptPath = Join-Path $ReposRoot $row.ScriptPath
    $projectRootPath = Split-Path (Split-Path $scriptPath -Parent) -Parent
    
    # Discovery
    $pkgName = $row.Repo.Replace("-mcp", "").Replace("-", "_")
    if ($row.Repo -eq "avatar-mcp") { $pkgName = "avatarmcp" }
    
    $checkPaths = @("src\$pkgName\http_server.py", "src\$pkgName\main.py", "src\$pkgName\server.py", "$pkgName\http_server.py", "$pkgName\main.py")
    $bEntry = $null
    foreach ($p in $checkPaths) {
        if (Test-Path (Join-Path $projectRootPath $p)) {
            $bEntry = $p.Replace("src\", "").Replace(".py", "").Replace("\", ".") + ":app"
            break
        }
    }

    Write-Host "Fixing $($row.Repo)..."
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
