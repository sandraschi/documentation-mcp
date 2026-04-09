#!/usr/bin/env pwsh
<#
⚠️ DEPRECATED - This script has been moved to SOTA location ⚠️

NEW LOCATION: sota-scripts/propagation-tools/propagate-standards-checker.ps1
MIGRATION: This script has been moved to the State-of-the-Art scripts directory
           for better organization and maintenance.

Use the new location instead: sota-scripts/propagation-tools/propagate-standards-checker.ps1

.SYNOPSIS
    Propagate SOTA standards checker to all MCP repositories
    
.DESCRIPTION
    Copies check-repo-standards.ps1 from templates/scripts/ to all MCP repos
    
.EXAMPLE
    .\scripts\propagate-standards-checker.ps1
#>

param([switch]$DryRun = $false)

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   📦 SOTA Script Propagation: check-repo-standards 📦  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$sourceScript = Join-Path $PSScriptRoot "..\templates\scripts\check-repo-standards.ps1"

if (-not (Test-Path $sourceScript)) {
    Write-Host "❌ Error: Source script not found" -ForegroundColor Red
    exit 1
}

Write-Host "📋 Source: $sourceScript`n" -ForegroundColor White

# Find all MCP repos
$reposRoot = "D:\Dev\repos"
$mcpRepos = Get-ChildItem -Path $reposRoot -Directory | Where-Object {
    $_.Name -match 'mcp' -and 
    $_.Name -notmatch 'central-docs' -and 
    $_.Name -notmatch 'copy|backup|old|archive|restored'
} | Sort-Object Name

Write-Host "🎯 Found $($mcpRepos.Count) MCP repositories`n" -ForegroundColor Green

$updated = 0
$created = 0
$skipped = 0

foreach ($repo in $mcpRepos) {
    $scriptsDir = Join-Path $repo.FullName "scripts"
    $targetScript = Join-Path $scriptsDir "check-repo-standards.ps1"
    
    if (-not (Test-Path $scriptsDir)) {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would create scripts/ and copy to: $($repo.Name)" -ForegroundColor Yellow
        } else {
            New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
            Copy-Item $sourceScript $targetScript -Force
            Write-Host "  ✅ Created scripts/ and copied: $($repo.Name)" -ForegroundColor Green
            $created++
        }
        continue
    }
    
    if (Test-Path $targetScript) {
        $sourceHash = (Get-FileHash $sourceScript -Algorithm MD5).Hash
        $targetHash = (Get-FileHash $targetScript -Algorithm MD5).Hash
        
        if ($sourceHash -eq $targetHash) {
            Write-Host "  ⏭️  Already up-to-date: $($repo.Name)" -ForegroundColor Gray
            $skipped++
        } else {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would update: $($repo.Name)" -ForegroundColor Yellow
            } else {
                Copy-Item $sourceScript $targetScript -Force
                Write-Host "  ✅ Updated: $($repo.Name)" -ForegroundColor Green
                $updated++
            }
        }
    } else {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would copy to: $($repo.Name)" -ForegroundColor Yellow
        } else {
            Copy-Item $sourceScript $targetScript -Force
            Write-Host "  ✅ Copied to: $($repo.Name)" -ForegroundColor Green
            $created++
        }
    }
}

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║            📦 Propagation Complete! 📦                 ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "📊 Summary:" -ForegroundColor White
Write-Host "  Total repos:      $($mcpRepos.Count)" -ForegroundColor White
Write-Host "  Updated:          $updated" -ForegroundColor Green
Write-Host "  Newly created:    $created" -ForegroundColor Cyan
Write-Host "  Already current:  $skipped" -ForegroundColor Gray
Write-Host ""

if (-not $DryRun -and ($updated -gt 0 -or $created -gt 0)) {
    Write-Host "✅ Done! Updated $(($updated + $created)) repositories" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Next: Run check-repo-standards.ps1 in any repo to analyze!" -ForegroundColor Yellow
}

