#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Universal propagation tool for SOTA scripts
    
.DESCRIPTION
    Pushes a standardized set of SOTA scripts from mcp-central-docs to all 
    discovered MCP repositories in D:\Dev\repos.
    
.EXAMPLE
    .\scripts\propagate-all-sota.ps1 -DryRun
#>

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "`nâ•"â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Cyan
Write-Host "â•'     ðŸš€ Universal SOTA Script Propagation Engine ðŸš€      â•'" -ForegroundColor Cyan
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Cyan

# 1. Configuration: Define SOTA Scripts and their sources
$sotaScripts = @(
    @{
        Name   = "backup-repo.ps1"
        Source = Join-Path $PSScriptRoot "..\backup-system\backup-repo.ps1"
    },
    @{
        Name   = "check-repo-standards.ps1"
        Source = Join-Path $PSScriptRoot "..\repo-standards\check-repo-standards.ps1"
    },
    @{
        Name   = "sync-sota.ps1"
        Source = Join-Path $PSScriptRoot "..\..\templates\scripts\sync-sota.ps1"
    }
)

# 2. Validation
foreach ($script in $sotaScripts) {
    if (-not (Test-Path $script.Source)) {
        Write-Host "âŒ Error: Source script not found: $($script.Source)" -ForegroundColor Red
        exit 1
    }
}

# 3. Discovery: Find all MCP repos
$reposRoot = "D:\Dev\repos"
$mcpRepos = Get-ChildItem -Path $reposRoot -Directory | Where-Object {
    $_.Name -match 'mcp' -and 
    $_.Name -notmatch 'central-docs' -and 
    $_.Name -notmatch 'copy|backup|old|archive|restored'
} | Sort-Object Name

Write-Host "ðŸŽ¯ Targeting $($mcpRepos.Count) repositories`n" -ForegroundColor Green

$stats = @{
    Updated = 0
    Created = 0
    Skipped = 0
    Failed  = 0
}

# 4. Processing
foreach ($repo in $mcpRepos) {
    Write-Host "ðŸ" Processing $($repo.Name)..." -ForegroundColor White
    $repoPath = $repo.FullName
    $scriptsDir = Join-Path $repoPath "scripts"
    
    if (-not (Test-Path $scriptsDir)) {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would create scripts/ directory" -ForegroundColor Yellow
        }
        else {
            New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
            Write-Host "  âœ... Created scripts/ directory" -ForegroundColor Green
        }
    }

    foreach ($script in $sotaScripts) {
        $targetFile = Join-Path $scriptsDir $script.Name
        
        if (Test-Path $targetFile) {
            $sourceHash = (Get-FileHash $script.Source -Algorithm SHA256).Hash
            $targetHash = (Get-FileHash $targetFile -Algorithm SHA256).Hash
            
            if ($sourceHash -eq $targetHash) {
                Write-Host "  â­ï¸  $($script.Name) is already SOTA" -ForegroundColor Gray
                $stats.Skipped++
            }
            else {
                if ($DryRun) {
                    Write-Host "  [DRY RUN] Would update $($script.Name)" -ForegroundColor Yellow
                }
                else {
                    Copy-Item $script.Source $targetFile -Force
                    Write-Host "  ðŸ"„ Updated $($script.Name) to SOTA" -ForegroundColor Green
                    $stats.Updated++
                }
            }
        }
        else {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would install $($script.Name)" -ForegroundColor Yellow
            }
            else {
                Copy-Item $script.Source $targetFile -Force
                Write-Host "  âœ¨ Installed $($script.Name)" -ForegroundColor Cyan
                $stats.Created++
            }
        }
    }
    Write-Host ""
}

# 5. Summary
Write-Host "â•"â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Cyan
Write-Host "â•'              ðŸ"Š Propagation Summary ðŸ"Š                 â•'" -ForegroundColor Cyan
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Cyan

if ($DryRun) { Write-Host "ðŸ" DRY RUN: No files were touched.`n" -ForegroundColor Yellow }

Write-Host "  Total Repos:     $($mcpRepos.Count)"
Write-Host "  Scripts Updated: $($stats.Updated)" -ForegroundColor Green
Write-Host "  Scripts Created: $($stats.Created)" -ForegroundColor Cyan
Write-Host "  Already SOTA:    $($stats.Skipped)" -ForegroundColor Gray
Write-Host ""
