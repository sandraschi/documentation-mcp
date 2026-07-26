# Merge prometheus.core.yml + prometheus.fleet.yml (+ optional fleet.local) → prometheus.yml
param(
    [string]$MonitoringDir = (Split-Path -Parent $PSScriptRoot)
)

$corePath = Join-Path $MonitoringDir "prometheus\prometheus.core.yml"
$fleetPath = Join-Path $MonitoringDir "prometheus\prometheus.fleet.yml"
$localPath = Join-Path $MonitoringDir "prometheus\prometheus.fleet.local.yml"
$outPath = Join-Path $MonitoringDir "prometheus\prometheus.yml"

if (-not (Test-Path $corePath)) {
    Write-Error "Missing $corePath"
    exit 1
}

function Get-ScrapeJobLines {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return @() }
    $lines = Get-Content $Path
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^\s*-\s+job_name:') {
            $start = $i
            break
        }
    }
    if ($start -lt 0) { return @() }
    return $lines[$start..($lines.Count - 1)]
}

$coreLines = Get-Content $corePath
$fleetLines = Get-ScrapeJobLines $fleetPath
$localLines = Get-ScrapeJobLines $localPath

$outLines = [System.Collections.Generic.List[string]]::new()
foreach ($line in $coreLines) { [void]$outLines.Add($line) }
if ($fleetLines.Count -gt 0) {
    [void]$outLines.Add("")
    [void]$outLines.Add("  # --- fleet (prometheus.fleet.yml) ---")
    foreach ($line in $fleetLines) { [void]$outLines.Add($line) }
}
if ($localLines.Count -gt 0) {
    [void]$outLines.Add("")
    [void]$outLines.Add("  # --- fleet.local ---")
    foreach ($line in $localLines) { [void]$outLines.Add($line) }
}

Set-Content -Path $outPath -Value ($outLines.ToArray()) -Encoding utf8
Write-Host "Merged Prometheus config -> $outPath" -ForegroundColor Green
