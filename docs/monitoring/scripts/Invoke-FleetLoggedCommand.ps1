<#
.SYNOPSIS
  Run a host MCP / dev server and tee stdout+stderr into unified monitoring log paths.

.EXAMPLE
  .\Invoke-FleetLoggedCommand.ps1 -JobName docs-mcp -WorkingDirectory D:\Dev\repos\mcp-central-docs `
    -Command "uv run python -m uvicorn docs_mcp.server:app --host 127.0.0.1 --port 10795 --log-level info"
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$JobName,
    [Parameter(Mandatory = $true)]
    [string]$Command,
    [string]$WorkingDirectory = (Get-Location).Path,
    [string]$MonitoringDir = (Join-Path (Split-Path -Parent $PSScriptRoot) "")
)

$ErrorActionPreference = "Stop"
$logDir = Join-Path $MonitoringDir "logs\host\$JobName"
New-Item -ItemType Directory -Path $logDir -Force | Out-Null
$logFile = Join-Path $logDir "stdout.log"

Write-Host "Fleet log: $logFile" -ForegroundColor Cyan
Write-Host "Command: $Command" -ForegroundColor DarkGray

$env:FLEET_LOG_JOB = $JobName
$env:FLEET_LOG_DIR = $logDir

Push-Location $WorkingDirectory
try {
    Invoke-Expression "$Command 2>&1 | Tee-Object -FilePath $logFile -Append"
}
finally {
    Pop-Location
}
