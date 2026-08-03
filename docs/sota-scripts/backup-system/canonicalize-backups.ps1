#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Canonicalize backup scripts across all repositories by replacing them with symbolic links.
    
.DESCRIPTION
    Iterates through all repositories in D:\Dev\repos and replaces any physical 
    scripts/backup-repo.ps1 with a symbolic link to the central SOTA version.
    
.PARAMETER ReposRoot
    Root directory containing all repos (default: D:\Dev\repos)
    
.PARAMETER CanonicalScript
    Path to the canonical SOTA backup script.
    
.PARAMETER DryRun
    Show what would be changed without making any changes.
#>

param(
    [string]$ReposRoot = "D:\Dev\repos",
    [string]$CanonicalScript = "D:\Dev\repos\mcp-central-docs\sota-scripts\backup-system\backup-repo.ps1",
    [switch]$DryRun = $false
)

Write-Host "`nâ•"â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Cyan
Write-Host "â•'        ðŸ"- CANONICALIZE BACKUPS - Symlink Fleet ðŸ"-       â•'" -ForegroundColor Cyan
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Cyan

if (-not (Test-Path $CanonicalScript)) {
    Write-Host "âŒ Error: Canonical script not found at $CanonicalScript" -ForegroundColor Red
    exit 1
}

$excludePattern = 'copy|backup|old|archive|restored|junk|external|tmp|temp'
$repos = Get-ChildItem -Path $ReposRoot -Directory | Where-Object {
    $_.Name -notmatch $excludePattern -and $_.Name -notmatch '^\.'
} | Sort-Object Name

Write-Host "ðŸŽ¯ Found $($repos.Count) repositories to examine.`n" -ForegroundColor Green

$linked = 0
$skipped = 0
$errors = 0

foreach ($repo in $repos) {
    $scriptDir = Join-Path $repo.FullName "scripts"
    $targetPath = Join-Path $scriptDir "backup-repo.ps1"
    
    Write-Host "Checking $($repo.Name)..." -NoNewline
    
    if (-not (Test-Path $scriptDir)) {
        Write-Host " skipped (no scripts dir)" -ForegroundColor Gray
        $skipped++
        continue
    }

    $existing = Get-Item $targetPath -ErrorAction SilentlyContinue
    
    if ($null -eq $existing) {
        # Optional: Setup backup script if it doesn't exist? 
        # For now, let's just skip unless there's an existing one to "fix"
        Write-Host " skipped (no backup-repo.ps1)" -ForegroundColor Gray
        $skipped++
        continue
    }

    if ($existing.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        Write-Host " already linked" -ForegroundColor DarkGray
        $skipped++
        continue
    }

    # Physical file found - link it!
    Write-Host " FOUND physical script" -ForegroundColor Yellow
    
    if ($DryRun) {
        Write-Host "    [DRY RUN] Would replace with symlink to canonical script" -ForegroundColor White
    }
    else {
        try {
            # 1. Take a temporary backup just in case
            $bakPath = $targetPath + ".bak"
            Move-Item $targetPath $bakPath -Force
            
            # 2. Create symbolic link
            New-Item -ItemType SymbolicLink -Path $targetPath -Target $CanonicalScript -Force | Out-Null
            
            # 3. If successful, remove backup
            Remove-Item $bakPath -Force
            
            Write-Host "    âœ... Successfully linked to canonical SOTA script" -ForegroundColor Green
            $linked++
        }
        catch {
            Write-Host "    âŒ Error creating symlink: $($_.Exception.Message)" -ForegroundColor Red
            $errors++
            # Try to restore backup if failed
            if (Test-Path $bakPath) {
                Move-Item $bakPath $targetPath -Force
            }
        }
    }
}

Write-Host "`nðŸ Summary:" -ForegroundColor White
Write-Host "  Repos examined:  $($repos.Count)" -ForegroundColor White
Write-Host "  Symlinks created: $linked" -ForegroundColor Green
Write-Host "  Already linked:   $skipped" -ForegroundColor Gray
Write-Host "  Errors:           $errors" -ForegroundColor Red
Write-Host ""
