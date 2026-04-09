<#
.SYNOPSIS
  Start each fleet webapp from the manifest, probe health, capture failures, then stop.
  Writes a single report for AI-driven batch fix (see docs/operations/FLEET_WEBAPP_PROBE.md).
.DESCRIPTION
  Reads scripts/fleet-webapp-manifest.json. For each entry: start start.ps1 in background,
  wait for port (up to timeoutSec), probe health URL, stop process. Records outcome and
  log excerpt. No Linux syntax; PowerShell only.
.EXAMPLE
  .\scripts\fleet-webapp-start-probe.ps1
  $env:FLEET_REPOS_ROOT = "D:\Dev\repos"; .\scripts\fleet-webapp-start-probe.ps1
#>
[CmdletBinding()]
param(
    [string]$ManifestPath = "scripts/fleet-webapp-manifest.json",
    [string]$ReportDir = "scripts/out",
    [int]$LogTailLines = 80,
    [string]$RepoFilter = ""
)

$ErrorActionPreference = "Stop"
$reposRoot = if ($env:FLEET_REPOS_ROOT) { $env:FLEET_REPOS_ROOT } else { "D:\Dev\repos" }

# Resolve paths from repo root (script may run from mcp-central-docs root)
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptRoot
if (-not (Test-Path $repoRoot)) { $repoRoot = Get-Location }
$manifestFull = Join-Path $repoRoot $ManifestPath
$reportDirFull = Join-Path $repoRoot $ReportDir

if (-not (Test-Path $manifestFull)) {
    Write-Error "Manifest not found: $manifestFull"
    exit 1
}

$manifest = Get-Content $manifestFull -Raw | ConvertFrom-Json
if ($RepoFilter) {
    $manifest = @($manifest | Where-Object { $_.repo -eq $RepoFilter })
    if ($manifest.Count -eq 0) { Write-Error "RepoFilter '$RepoFilter' matched no manifest entry."; exit 1 }
    Write-Host "Filtering to repo: $RepoFilter"
}
New-Item -ItemType Directory -Force -Path $reportDirFull | Out-Null

$results = @()
$generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

foreach ($entry in $manifest) {
    $repo = $entry.repo
    $startPath = $entry.startPath
    $port = [int]$entry.port
    $healthPath = $entry.healthPath
    $timeoutSec = if ($entry.timeoutSec) { [int]$entry.timeoutSec } else { 90 }

    $repoPath = Join-Path $reposRoot $repo
    $startScriptPath = Join-Path $repoPath $startPath
    # Resolve to absolute path so child PowerShell never receives ".\start.ps1" (fails when cwd differs)
    $startScriptPath = [System.IO.Path]::GetFullPath((Resolve-Path -LiteralPath $startScriptPath).Path)
    $workDir = Split-Path -Parent $startScriptPath

    $r = [PSCustomObject]@{
        repo       = $repo
        startPath  = $startPath
        port       = $port
        healthPath = $healthPath
        outcome    = "skip"
        healthStatus = $null
        errorMessage = ""
        logExcerpt  = ""
    }

    if ($port -le 0) {
        $r.errorMessage = "Port not set (fill from repo start.ps1 BackendPort/WebPort)"
        $results += $r
        Write-Host "[$repo] SKIP (port not set)"
        continue
    }

    if (-not (Test-Path $repoPath)) {
        $r.errorMessage = "Repo path not found: $repoPath"
        $results += $r
        Write-Host "[$repo] SKIP (repo not found)"
        continue
    }
    if (-not (Test-Path $startScriptPath)) {
        $r.errorMessage = "Start script not found: $startScriptPath"
        $results += $r
        Write-Host "[$repo] SKIP (start script not found)"
        continue
    }

    $outFile = [System.IO.Path]::GetTempFileName()
    $errFile = [System.IO.Path]::GetTempFileName()
    $p = $null
    try {
        $p = Start-Process -FilePath "powershell.exe" -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "`"$startScriptPath`"" -WorkingDirectory $workDir -RedirectStandardOutput $outFile -RedirectStandardError $errFile -PassThru -NoNewWindow

        $deadline = (Get-Date).AddSeconds($timeoutSec)
        $healthOk = $false
        while ((Get-Date) -lt $deadline) {
            Start-Sleep -Seconds 3
            try {
                $uri = "http://127.0.0.1:$port$healthPath"
                $resp = Invoke-WebRequest -Uri $uri -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                $r.healthStatus = $resp.StatusCode
                if ($resp.StatusCode -ge 200 -and $resp.StatusCode -lt 400) {
                    $r.outcome = "health_ok"
                    $healthOk = $true
                } else {
                    $r.outcome = "health_failed"
                    $r.errorMessage = "HTTP $($resp.StatusCode)"
                }
                break
            } catch {
                # Connection refused or timeout - keep waiting
            }
        }

        if (-not $healthOk -and $r.outcome -eq "skip") {
            $r.outcome = "start_failed"
            $r.errorMessage = "Port $port did not respond within $timeoutSec s"
        }
    } catch {
        $r.outcome = "start_failed"
        $r.errorMessage = $_.Exception.Message
    } finally {
        if ($p -and -not $p.HasExited) { $p.Kill() }
        Start-Sleep -Seconds 1
        if ($r.outcome -eq "start_failed" -or $r.outcome -eq "health_failed") {
            $errContent = Get-Content $errFile -Tail $LogTailLines -ErrorAction SilentlyContinue
            $r.logExcerpt = ($errContent | Out-String).Trim()
        }
        Remove-Item $outFile -Force -ErrorAction SilentlyContinue
        Remove-Item $errFile -Force -ErrorAction SilentlyContinue
    }

    $results += $r
    Write-Host "[$repo] $($r.outcome)"
}

$report = @{
    generatedAt = $generatedAt
    reposRoot   = $reposRoot
    results     = @($results)
}
$reportJson = Join-Path $reportDirFull "fleet-webapp-report.json"
$report | ConvertTo-Json -Depth 5 | Set-Content -Path $reportJson -Encoding utf8

$mdLines = @("# Fleet webapp probe report", "", "Generated: $generatedAt", "Repos root: $reposRoot", "")
foreach ($r in $results) {
    $mdLines += "## $($r.repo)"
    $mdLines += "- Outcome: $($r.outcome)"
    if ($r.healthStatus) { $mdLines += "- Health status: $($r.healthStatus)" }
    if ($r.errorMessage) { $mdLines += "- Error: $($r.errorMessage)" }
    if ($r.logExcerpt) { $mdLines += '```'; $mdLines += $r.logExcerpt; $mdLines += '```' }
    $mdLines += ""
}
$reportMd = Join-Path $reportDirFull "fleet-webapp-report.md"
$mdLines | Set-Content -Path $reportMd -Encoding utf8

Write-Host "Report: $reportJson"
Write-Host "Report (MD): $reportMd"
