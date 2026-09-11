# One-way content sync: private mcp-central-docs (mcd) -> public documentation-mcp/docs.
#
# mcd is the source of truth; docs/ here is a generated, curated export. Never edit
# synced files in documentation-mcp directly - edit in mcd and re-run this script.
#
# Safety: always runs the hygiene gate (scripts/hygiene-gate.ps1) against the SOURCE
# shelves before copying, and against the DESTINATION after copying. A dirty source
# blocks the copy unless -Force is passed; a dirty destination always blocks commit
# (the script never commits or pushes - that stays a manual, reviewed step).
#
# Usage:
#   .\scripts\sync-from-mcd.ps1                 # dry run - lists what would change
#   .\scripts\sync-from-mcd.ps1 -Apply           # actually copies
#   .\scripts\sync-from-mcd.ps1 -Apply -Force    # copy even if source hygiene gate is dirty

param(
    [string]$McdRoot = "D:\Dev\repos\mcp-central-docs",
    [switch]$Apply,
    [switch]$Force
)

$DocsRoot = Join-Path $PSScriptRoot "..\docs"

if (-not (Test-Path $McdRoot)) {
    Write-Host "ERROR: mcd root not found: $McdRoot" -ForegroundColor Red
    exit 1
}

# Shelf = any docs/<name> subfolder that also exists as mcp-central-docs/<name>.
# Adding a new shelf to vendor: create the matching empty folder under docs/ first.
$Shelves = Get-ChildItem -Path $DocsRoot -Directory |
    Where-Object { Test-Path (Join-Path $McdRoot $_.Name) } |
    Select-Object -ExpandProperty Name

# Sub-paths to never vendor, even inside an otherwise-synced shelf.
# Mirrors mcp-central-docs/archive/retired-plans/WEED_MANIFEST.md §1.
$ExcludeDirs = @(
    "docs-private", "backups", "backup", "archive", "_archive", "_junk", "junk",
    "adn-notes", "agentic chats", ".obsidian", ".cursor", "node_modules",
    "__pycache__", ".venv", "venv", "dist", "htmlcov", "temp", "egg-info"
)

Write-Host "Shelves to sync: $($Shelves -join ', ')"
Write-Host ""

Write-Host "--- Pre-flight hygiene gate on mcd source ---"
$sourceClean = $true
foreach ($shelf in $Shelves) {
    $src = Join-Path $McdRoot $shelf
    & "$PSScriptRoot\hygiene-gate.ps1" -Path $src -ReportPath (Join-Path $PSScriptRoot "..\hygiene-report-source-$shelf.txt")
    if ($LASTEXITCODE -ne 0) { $sourceClean = $false }
}

if (-not $sourceClean -and -not $Force) {
    Write-Host ""
    Write-Host "Source hygiene gate failed. Fix the hits in mcp-central-docs, or rerun with -Force." -ForegroundColor Red
    exit 1
}

if (-not $Apply) {
    Write-Host ""
    Write-Host "Dry run only - rerun with -Apply to copy. Robocopy preview (/L):" -ForegroundColor Yellow
    foreach ($shelf in $Shelves) {
        $src = Join-Path $McdRoot $shelf
        $dst = Join-Path $DocsRoot $shelf
        $xd = $ExcludeDirs | ForEach-Object { Join-Path $src $_ }
        robocopy $src $dst /E /L /NFL /NDL /NJH /XD $xd | Select-Object -Last 6
    }
    exit 0
}

Write-Host ""
Write-Host "--- Copying ($($Shelves.Count) shelves) ---"
foreach ($shelf in $Shelves) {
    $src = Join-Path $McdRoot $shelf
    $dst = Join-Path $DocsRoot $shelf
    $xd = $ExcludeDirs | ForEach-Object { Join-Path $src $_ }
    # /E mirrors additions+updates, does not delete dest-only files (no /MIR - docs-only
    # pages authored directly in documentation-mcp must survive a sync).
    robocopy $src $dst /E /XD $xd /NFL /NDL /NJH | Select-Object -Last 6
}

Write-Host ""
Write-Host "--- Post-copy hygiene gate on docs/ ---"
& "$PSScriptRoot\hygiene-gate.ps1" -Path $DocsRoot -ReportPath (Join-Path $PSScriptRoot "..\hygiene-report-dest.txt")
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Destination is dirty after copy. Do NOT commit - fix hits in mcd and re-sync." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Sync complete and clean. Review 'git status' / 'git diff' before committing - this script never commits or pushes." -ForegroundColor Green
