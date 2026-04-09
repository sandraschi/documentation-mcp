# Check read/write access to all repos under D:\Dev\repos.
# Run from PowerShell to verify which repos are accessible from your environment.
# Usage: .\scripts\check-repos-access.ps1 [-ReposRoot "D:\Dev\repos"]

param(
    [string] $ReposRoot = "D:\Dev\repos"
)

$ErrorActionPreference = "Continue"

if (-not (Test-Path -LiteralPath $ReposRoot -PathType Container)) {
    Write-Error "Repos root not found: $ReposRoot"
    exit 1
}

$dirs = Get-ChildItem -LiteralPath $ReposRoot -Directory | Sort-Object Name
$results = @()

foreach ($dir in $dirs) {
    $name = $dir.Name
    $path = $dir.FullName
    $readOk = $false
    $writeOk = $false
    $readError = ""
    $writeError = ""

    # Test read: try to get child items (or read a common file)
    try {
        $null = Get-ChildItem -LiteralPath $path -ErrorAction Stop
        $readOk = $true
    } catch {
        $readError = $_.Exception.Message
    }

    # Test write: create and delete a temp file in repo root (skip if not writable by design, e.g. read-only mount)
    $testFile = Join-Path $path ".access-check-temp-delete-me"
    try {
        Set-Content -LiteralPath $testFile -Value "access check" -ErrorAction Stop
        Remove-Item -LiteralPath $testFile -Force -ErrorAction Stop
        $writeOk = $true
    } catch {
        $writeError = $_.Exception.Message
    }

    $results += [PSCustomObject]@{
        Repo    = $name
        Path    = $path
        ReadOk  = $readOk
        WriteOk = $writeOk
        ReadErr = $readError
        WriteErr = $writeError
    }
}

# Report
$pad = ($results.Repo | ForEach-Object { $_.Length } | Measure-Object -Maximum).Maximum
if ($pad -lt 4) { $pad = 4 }

Write-Host ""
Write-Host ("{0,-$pad}  Read   Write" -f "Repo")
Write-Host ("{0,-$pad}  ----   -----" -f "----")
foreach ($r in $results) {
    $readStr  = if ($r.ReadOk)  { "OK  " } else { "FAIL" }
    $writeStr = if ($r.WriteOk) { "OK  " } else { "FAIL" }
    Write-Host ("{0,-$pad}  {1}  {2}" -f $r.Repo, $readStr, $writeStr)
}
Write-Host ""

$readFail  = ($results | Where-Object { -not $_.ReadOk }).Count
$writeFail = ($results | Where-Object { -not $_.WriteOk }).Count
if ($readFail -gt 0 -or $writeFail -gt 0) {
    Write-Host "Details (failures):"
    foreach ($r in $results) {
        if (-not $r.ReadOk)  { Write-Host "  $($r.Repo) READ:  $($r.ReadErr)" }
        if (-not $r.WriteOk) { Write-Host "  $($r.Repo) WRITE: $($r.WriteErr)" }
    }
}

Write-Host ""
Write-Host "Total repos: $($results.Count). Read OK: $($results.Count - $readFail). Write OK: $($results.Count - $writeFail)."
