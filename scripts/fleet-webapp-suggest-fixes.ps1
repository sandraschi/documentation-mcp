<#
.SYNOPSIS
  Read fleet-webapp-report.json and suggest fixes for failed entries (from BUGFIX_LOG patterns).
.DESCRIPTION
  For each result where outcome is not health_ok, matches errorMessage and logExcerpt against
  known antipatterns and outputs repo + suggested fix. Use after running fleet-webapp-start-probe.ps1.
.EXAMPLE
  .\scripts\fleet-webapp-suggest-fixes.ps1
  .\scripts\fleet-webapp-suggest-fixes.ps1 -ReportPath "D:\Dev\repos\mcp-central-docs\scripts\out\fleet-webapp-report.json"
#>
[CmdletBinding()]
param(
    [string]$ReportPath = "scripts/out/fleet-webapp-report.json"
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
if (-not (Test-Path $repoRoot)) { $repoRoot = Get-Location }
$reportFull = Join-Path $repoRoot $ReportPath

if (-not (Test-Path $reportFull)) {
    Write-Error "Report not found: $reportFull. Run fleet-webapp-start-probe.ps1 first."
    exit 1
}

$report = Get-Content $reportFull -Raw | ConvertFrom-Json
$failed = @($report.results | Where-Object { $_.outcome -ne "health_ok" })
if ($failed.Count -eq 0) {
    Write-Host "No failed entries. All health_ok."
    exit 0
}

# Pattern -> suggested fix (from BUGFIX_LOG)
$patterns = @(
    @{ Pattern = "app.*not found|Attribute.*app.*not found|no asgi"; Fix = "ASGI: expose app from FastMCP http_app() in module referenced by uvicorn (BUGFIX_LOG No ASGI app)" }
    @{ Pattern = "uv sync|package not found|running from repo root|PYTHONPATH"; Fix = "CWD/uv: use uv run --project `$ProjectRoot and Set-Location `$PSScriptRoot in start.ps1 (BUGFIX_LOG Backend CWD)" }
    @{ Pattern = "Port.*did not respond|Connection refused|ECONNREFUSED"; Fix = "Backend not listening in time: check ASGI/CWD first; add wait-for-backend loop in start.ps1 if needed" }
    @{ Pattern = "HTTP 4|HTTP 5"; Fix = "Health endpoint returned error: check healthPath and backend route" }
)

$suggestions = @()
foreach ($r in $failed) {
    $text = "$($r.errorMessage) $($r.logExcerpt)"
    $suggest = "Unknown: review logExcerpt and BUGFIX_LOG"
    foreach ($p in $patterns) {
        if ($text -match $p.Pattern) {
            $suggest = $p.Fix
            break
        }
    }
    $suggestions += [PSCustomObject]@{ repo = $r.repo; outcome = $r.outcome; suggestedFix = $suggest }
}

Write-Host "Suggested fixes ($($suggestions.Count) failed):"
Write-Host ""
foreach ($s in $suggestions) {
    Write-Host "[$($s.repo)] $($s.outcome)"
    Write-Host "  -> $($s.suggestedFix)"
    Write-Host ""
}
$suggestions | ConvertTo-Json -Depth 2
