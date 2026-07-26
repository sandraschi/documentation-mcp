#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Run backup script in all MCP repositories
    
.DESCRIPTION
    Loops through all MCP repositories and runs their backup-repo.ps1 script.
    Creates backups in repos2 directory with proper folder structure.
    
.PARAMETER ReposRoot
    Root directory containing all repos (default: D:\Dev\repos)
    
.PARAMETER DryRun
    Show what would be backed up without actually running backups
    
.EXAMPLE
    .\scripts\mass-backup-all-repos.ps1
    # Backs up all MCP repos
    
.EXAMPLE
    .\scripts\mass-backup-all-repos.ps1 -DryRun
    # Shows which repos would be backed up
#>

param(
    [string]$ReposRoot = "D:\Dev\repos",
    [switch]$DryRun = $false
)

Write-Host "`nâ•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Magenta
Write-Host "â•‘        ðŸ“¦ MASS BACKUP - All MCP Repositories ðŸ“¦         â•‘" -ForegroundColor Magenta
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Magenta

# Find all actual git repositories (exclude junk/external and hidden folders)
$excludePattern = 'copy|backup|old|archive|restored|junk|external|tmp|temp'
$repos = Get-ChildItem -Path $ReposRoot -Directory | Where-Object {
    $_.Name -notmatch $excludePattern -and
    $_.Name -notmatch '^\.' -and
    (Test-Path (Join-Path $_.FullName ".git"))
} | Sort-Object Name

Write-Host "ðŸŽ¯ Found $($repos.Count) MCP repositories`n" -ForegroundColor Green

if ($DryRun) {
    Write-Host "ðŸ” DRY RUN MODE - Listing repos to backup:`n" -ForegroundColor Yellow
    $centralScript = Join-Path $PSScriptRoot "backup-repo.ps1"
    if (-not (Test-Path $centralScript)) {
        $centralScript = Join-Path $PSScriptRoot "..\sota-scripts\backup-system\backup-repo.ps1"
    }
    $hasCentral = Test-Path $centralScript

    foreach ($repo in $repos) {
        $hasLocal = Test-Path (Join-Path $repo.FullName "scripts\backup-repo.ps1")
        if ($hasLocal) {
            Write-Host "  âœ… $($repo.Name) (local script)" -ForegroundColor Green
        }
        elseif ($hasCentral) {
            Write-Host "  ðŸ“¦ $($repo.Name) (central fallback)" -ForegroundColor Cyan
        }
        else {
            Write-Host "  â­ï¸  $($repo.Name) (no script available)" -ForegroundColor Gray
        }
    }
    Write-Host "`nâœ… Dry run complete`n" -ForegroundColor Yellow
    exit 0
}

$success = 0
$failed = 0
$skipped = 0
$startTime = Get-Date

foreach ($repo in $repos) {
    Write-Host "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”" -ForegroundColor Gray
    Write-Host "ðŸ“¦ Repository: $($repo.Name)" -ForegroundColor Cyan
    
    # Canonical logic: Always try to use the central SOTA script first to avoid stale local copies
    $centralScript = Join-Path $PSScriptRoot "backup-repo.ps1"
    if (-not (Test-Path $centralScript)) {
        $centralScript = Join-Path $PSScriptRoot "..\sota-scripts\backup-system\backup-repo.ps1"
    }
    
    $backupScript = $centralScript
    $usingFallback = $true
    
    # Only fall back to local script if central is COMPLETELY missing (emergency fallback)
    if (-not (Test-Path $backupScript)) {
        $backupScript = Join-Path $repo.FullName "scripts\backup-repo.ps1"
        $usingFallback = $false
        if (Test-Path $backupScript) {
            Write-Host "  âš ï¸  Central script missing - falling back to LOCAL version" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host "  ðŸ“¦ Using canonical SOTA script" -ForegroundColor Cyan
    }
    
    if (-not (Test-Path $backupScript)) {
        Write-Host "  âŒ No backup script available (local or central) - skipping" -ForegroundColor Red
        $skipped++
        continue
    }
    
    try {
        Push-Location $repo.FullName
        
        # Run backup script
        Write-Host "  ðŸ”„ Executing backup..." -ForegroundColor Gray
        & $backupScript
        
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            Write-Host "  âœ… Backup complete: $($repo.Name)" -ForegroundColor Green
            $success++
        }
        else {
            Write-Host "  âŒ Backup failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            $failed++
        }
        
    }
    catch {
        Write-Host "  âŒ Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
        
    }
    finally {
        Pop-Location
    }
    
    Write-Host ""
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Green
Write-Host "â•‘           ðŸ“¦ MASS BACKUP COMPLETE! ðŸ“¦                   â•‘" -ForegroundColor Green
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Green

Write-Host "ðŸ“Š Summary:" -ForegroundColor White
Write-Host "  Total repos:      $($repos.Count)" -ForegroundColor White
Write-Host "  Successful:       $success" -ForegroundColor Green
Write-Host "  Failed:           $failed" -ForegroundColor Red
Write-Host "  Skipped:          $skipped" -ForegroundColor Yellow
Write-Host "  Duration:         $([math]::Round($duration.TotalMinutes, 1)) minutes`n" -ForegroundColor Cyan

Write-Host "ðŸ’¾ Backup locations:" -ForegroundColor Cyan
Write-Host "  Desktop:          C:\Users\$env:USERNAME\Desktop\repo backup" -ForegroundColor White
Write-Host "  Network:          N:\backup\dev\repo-backups\" -ForegroundColor Green
Write-Host "  OneDrive:         $env:OneDrive\Backup\repo-backups\`n" -ForegroundColor Cyan

if ($failed -gt 0) {
    Write-Host "âš ï¸  Some backups failed. Check output above for details." -ForegroundColor Yellow
}
else {
    Write-Host "âœ… All backups created successfully!`n" -ForegroundColor Green
}

