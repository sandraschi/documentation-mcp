#!/usr/bin/env pwsh
<#
⚠️ DEPRECATED - This script has been moved to SOTA location ⚠️

NEW LOCATION: sota-scripts/propagation-tools/propagate-backup-script.ps1
MIGRATION: This script has been moved to the State-of-the-Art scripts directory
           for better organization and maintenance.

Use the new location instead: sota-scripts/propagation-tools/propagate-backup-script.ps1

.SYNOPSIS
    Propagate SOTA backup script to all MCP repositories
    
.DESCRIPTION
    Copies the state-of-the-art backup-repo.ps1 from templates/scripts/
    to all MCP server repositories, excluding backup/copy/archive repos
    
.EXAMPLE
    .\scripts\propagate-backup-script.ps1
    # Copies backup script to all MCP repos
    
.EXAMPLE
    .\scripts\propagate-backup-script.ps1 -DryRun
    # Shows what would be copied without making changes
#>

param(
    [switch]$DryRun = $false
)

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     📦 SOTA Script Propagation: backup-repo.ps1 📦     ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Source script
$sourceScript = Join-Path $PSScriptRoot "..\templates\scripts\backup-repo.ps1"

if (-not (Test-Path $sourceScript)) {
    Write-Host "❌ Error: Source script not found: $sourceScript" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Source: $sourceScript" -ForegroundColor White
Write-Host ""

# Find all repositories (excluding junk/external and hidden folders)
$reposRoot = "D:\Dev\repos"
$excludePattern = 'copy|backup|old|archive|restored|junk|external|tmp|temp'
$mcpRepos = Get-ChildItem -Path $reposRoot -Directory | Where-Object {
    $_.Name -notmatch $excludePattern -and $_.Name -notmatch '^\.'
} | Sort-Object Name

Write-Host "🎯 Found $($mcpRepos.Count) repositories to evaluate`n" -ForegroundColor Green

$updated = 0
$skipped = 0
$created = 0

foreach ($repo in $mcpRepos) {
    $repoPath = $repo.FullName
    $scriptsDir = Join-Path $repoPath "scripts"
    $targetScript = Join-Path $scriptsDir "backup-repo.ps1"
    
    # Check if scripts directory exists
    if (-not (Test-Path $scriptsDir)) {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would create: $scriptsDir" -ForegroundColor Yellow
            Write-Host "  [DRY RUN] Would copy to: $($repo.Name)" -ForegroundColor Yellow
        }
        else {
            New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
            Copy-Item $sourceScript $targetScript -Force
            Write-Host "  ✅ Created scripts/ and copied: $($repo.Name)" -ForegroundColor Green
            $created++
        }
        continue
    }
    
    # Check if backup script exists
    if (Test-Path $targetScript) {
        # Compare files
        $sourceHash = (Get-FileHash $sourceScript -Algorithm MD5).Hash
        $targetHash = (Get-FileHash $targetScript -Algorithm MD5).Hash
        
        if ($sourceHash -eq $targetHash) {
            Write-Host "  ⏭️  Already up-to-date: $($repo.Name)" -ForegroundColor Gray
            $skipped++
        }
        else {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would update: $($repo.Name)" -ForegroundColor Yellow
            }
            else {
                Copy-Item $sourceScript $targetScript -Force
                Write-Host "  ✅ Updated: $($repo.Name)" -ForegroundColor Green
                $updated++
            }
        }
    }
    else {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would copy to: $($repo.Name)" -ForegroundColor Yellow
        }
        else {
            Copy-Item $sourceScript $targetScript -Force
            Write-Host "  ✅ Copied to: $($repo.Name)" -ForegroundColor Green
            $created++
        }
    }
}

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              📦 Propagation Complete! 📦               ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No changes made`n" -ForegroundColor Yellow
}

Write-Host "📊 Summary:" -ForegroundColor White
Write-Host "  Total repos:      $($mcpRepos.Count)" -ForegroundColor White
Write-Host "  Updated:          $updated" -ForegroundColor Green
Write-Host "  Newly created:    $created" -ForegroundColor Cyan
Write-Host "  Already current:  $skipped" -ForegroundColor Gray
Write-Host ""

if (-not $DryRun -and ($updated -gt 0 -or $created -gt 0)) {
    Write-Host "✅ Done! Updated $(($updated + $created)) repositories" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Test backup script in one repo: .\scripts\backup-repo.ps1" -ForegroundColor White
    Write-Host "  2. Commit changes to affected repos if satisfied" -ForegroundColor White
}

