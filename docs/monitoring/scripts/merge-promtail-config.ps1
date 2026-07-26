# Merge promtail.unified.yml + promtail.host.yml (+ optional promtail.host.local.yml) -> promtail.yml
param(
    [string]$MonitoringDir = (Split-Path -Parent $PSScriptRoot)
)

$basePath = Join-Path $MonitoringDir "promtail\promtail.unified.yml"
$hostPath = Join-Path $MonitoringDir "promtail\promtail.host.yml"
$localPath = Join-Path $MonitoringDir "promtail\promtail.host.local.yml"
$outPath = Join-Path $MonitoringDir "promtail\promtail.yml"

if (-not (Test-Path $basePath)) {
    Write-Error "Missing $basePath"
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

$baseLines = Get-Content $basePath
$hostLines = Get-ScrapeJobLines $hostPath
$localLines = Get-ScrapeJobLines $localPath

# Keep everything before first scrape job in unified (server, clients, scrape_configs: header)
$headerEnd = -1
for ($i = 0; $i -lt $baseLines.Count; $i++) {
    if ($baseLines[$i] -match '^\s*-\s+job_name:') {
        $headerEnd = $i
        break
    }
}
if ($headerEnd -lt 0) {
    Write-Error "promtail.unified.yml has no scrape jobs"
    exit 1
}

$outLines = [System.Collections.Generic.List[string]]::new()
foreach ($line in $baseLines[0..($headerEnd - 1)]) { [void]$outLines.Add($line) }
foreach ($line in (Get-ScrapeJobLines $basePath)) { [void]$outLines.Add($line) }
if ($hostLines.Count -gt 0) {
    [void]$outLines.Add("")
    [void]$outLines.Add("  # --- host processes (promtail.host.yml) ---")
    foreach ($line in $hostLines) { [void]$outLines.Add($line) }
}
if ($localLines.Count -gt 0) {
    [void]$outLines.Add("")
    [void]$outLines.Add("  # --- host.local ---")
    foreach ($line in $localLines) { [void]$outLines.Add($line) }
}

Set-Content -Path $outPath -Value ($outLines.ToArray()) -Encoding utf8
Write-Host "Merged Promtail config -> $outPath" -ForegroundColor Green
