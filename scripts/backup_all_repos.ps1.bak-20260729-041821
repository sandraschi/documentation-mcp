#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Advanced backup script for all repositories with MCP filtering
    
.DESCRIPTION
    Iterates through all repositories and runs the SOTA backup-repo.ps1 script.
    Features MCP-only filtering by default, with option to include all repos.
    
.PARAMETER ReposRoot
    Root directory containing all repos (default: D:\Dev\repos)
    
.PARAMETER MCPOnly
    Only backup MCP-related repositories (default: true)
    
.PARAMETER DryRun
    Show what would be backed up without actually running backups
    
.PARAMETER IncludeBuild
    Pass IncludeBuild flag to individual backup scripts
    
.EXAMPLE
    .\backup_all_repos.ps1
    # Backs up only MCP repos (default behavior)
    
.EXAMPLE
    .\backup_all_repos.ps1 -MCPOnly $false
    # Backs up all repositories
    
.EXAMPLE
    .\backup_all_repos.ps1 -DryRun
    # Shows which repos would be backed up
    
.EXAMPLE
    .\backup_all_repos.ps1 -IncludeBuild
    # Backs up MCP repos including build artifacts
#>

param(
    [string]$ReposRoot = "D:\Dev\repos",
    [bool]$MCPOnly = $true,
    [switch]$DryRun = $false,
    [switch]$IncludeBuild = $false,
    [string]$TargetDir = "",
    [switch]$Help = $false,
    [switch]$SaveIdent = $false
)

# Show help if requested
if ($Help) {
    Write-Host "`nðŸ“‹ BACKUP_ALL_REPOS.PS1 HELP`n" -ForegroundColor Cyan
    Write-Host "ðŸ”§ PARAMETERS:" -ForegroundColor White
    Write-Host "  -ReposRoot     Root directory containing all repos (default: D:\Dev\repos)" -ForegroundColor Gray
    Write-Host "  -MCPOnly       Only backup MCP-related repositories (default: true)" -ForegroundColor Gray
    Write-Host "  -IncludeBuild  Include build artifacts in backups (default: false)" -ForegroundColor Gray
    Write-Host "  -TargetDir     Override default backup targets with single directory (default: none)" -ForegroundColor Gray
    Write-Host "  -SaveIdent     Save identical ZIP files in consecutive runs (default: false)" -ForegroundColor Gray
    Write-Host "  -DryRun        Show what would be backed up without executing (default: false)" -ForegroundColor Gray
    Write-Host "  -Help          Show this help message (default: false)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "ðŸ“- EXAMPLES:" -ForegroundColor White
    Write-Host "  .\backup_all_repos.ps1" -ForegroundColor Green
    Write-Host "  # Backs up only MCP repos to default locations (Desktop, N: Drive, OneDrive)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  .\backup_all_repos.ps1 -MCPOnly `$false" -ForegroundColor Green
    Write-Host "  # Backs up all repositories" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  .\backup_all_repos.ps1 -TargetDir 'C:\CustomBackups'" -ForegroundColor Green
    Write-Host "  # Backs up MCP repos to custom directory only" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  .\backup_all_repos.ps1 -SaveIdent" -ForegroundColor Green
    Write-Host "  # Save identical ZIP files (prevents duplicate backups)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  .\backup_all_repos.ps1 -DryRun" -ForegroundColor Green
    Write-Host "  # Shows which repos would be backed up" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  .\backup_all_repos.ps1 -IncludeBuild" -ForegroundColor Green
    Write-Host "  # Backs up MCP repos including build artifacts" -ForegroundColor Gray
    Write-Host ""
    Write-Host "ðŸŽ¯ MCP RECOGNITION:" -ForegroundColor White
    Write-Host "  Repositories are identified as MCP-related if they contain:" -ForegroundColor Gray
    Write-Host "  - Names matching MCP patterns (mcp, docker, email, notion, etc.)" -ForegroundColor Gray
    Write-Host "  - 'mcp' or 'MCP' in pyproject.toml or package.json files" -ForegroundColor Gray
    Write-Host ""
    Write-Host "ðŸ’¾ IDENTICAL BACKUP HANDLING:" -ForegroundColor White
    Write-Host "  When -SaveIdent is false (default): Identical backups are skipped and removed" -ForegroundColor Gray
    Write-Host "  When -SaveIdent is true: Identical backups are preserved with timestamps" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

Write-Host "`nâ•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor Magenta
Write-Host "â•‘     ðŸ“¦ ADVANCED BACKUP - All Repositories ðŸ“¦           â•‘" -ForegroundColor Magenta
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor Magenta

Write-Host "ðŸ“‹ Configuration:" -ForegroundColor Cyan
Write-Host "  Repos Root:      $ReposRoot" -ForegroundColor White
Write-Host "  MCP Only:        $MCPOnly" -ForegroundColor White
Write-Host "  Include Build:   $IncludeBuild" -ForegroundColor White
Write-Host "  Target Dir:      $(if ($TargetDir) { $TargetDir } else { 'Default locations' })" -ForegroundColor White
Write-Host "  Save Identical:  $SaveIdent" -ForegroundColor White
Write-Host "  Dry Run:         $DryRun" -ForegroundColor White
Write-Host ""

# Define MCP-related patterns
$mcpPatterns = @(
    'mcp',
    'tapo-camera',
    'fastsearch',
    'filesystem',
    'memory',
    'playwright',
    'puppeteer',
    'readly',
    'sequential-thinking',
    'docker',
    'database',
    'email',
    'notion',
    'obsidian',
    'ocr',
    'onenote',
    'plex',
    'rustdesk',
    'ring',
    'tailscale',
    'unity3d',
    'virtualdj',
    'vrchat',
    'web-development',
    'windows-operations',
    'winrar',
    'calibre',
    'gimp',
    'handbrake',
    'immich',
    'obs',
    'reaper',
    'resolume',
    'sonos',
    'suno',
    'unitree-robotics',
    'vroidstudio'
)

# Function to check if repo is MCP-related
function Test-MCPRepository {
    param([string]$RepoName)
    
    if (-not $MCPOnly) {
        # When MCPOnly is false, we still want to classify repos for display
        # but we won't filter them out
    }
    
    foreach ($pattern in $mcpPatterns) {
        if ($RepoName -like "*$pattern*") {
            return $true
        }
    }
    
    # Also check for common MCP indicators in repo structure
    $repoPath = Join-Path $ReposRoot $RepoName
    if (Test-Path (Join-Path $repoPath "pyproject.toml")) {
        $content = Get-Content (Join-Path $repoPath "pyproject.toml") -Raw -ErrorAction SilentlyContinue
        if ($content -match "mcp|MCP") {
            return $true
        }
    }
    
    if (Test-Path (Join-Path $repoPath "package.json")) {
        $content = Get-Content (Join-Path $repoPath "package.json") -Raw -ErrorAction SilentlyContinue
        if ($content -match "mcp|MCP") {
            return $true
        }
    }
    
    return $false
}

# Find all repositories (excluding junk/external and hidden folders)
$excludePattern = 'copy|backup|old|archive|restored|junk|external|tmp|temp|\.trash|\.cursor|\.vscode'
$allRepos = Get-ChildItem -Path $ReposRoot -Directory | Where-Object {
    $_.Name -notmatch $excludePattern -and $_.Name -notmatch '^\.'
} | Sort-Object Name

# Filter repos based on MCPOnly setting
if ($MCPOnly) {
    $repos = $allRepos | Where-Object { Test-MCPRepository -RepoName $_.Name }
} else {
    $repos = $allRepos
}

Write-Host "ðŸŽ¯ Found $($allRepos.Count) total repositories" -ForegroundColor Gray
if ($MCPOnly) {
    Write-Host "ðŸŽ¯ Filtered to $($repos.Count) MCP repositories`n" -ForegroundColor Green
} else {
    Write-Host "ðŸŽ¯ Processing all $($repos.Count) repositories`n" -ForegroundColor Green
}

# Display repositories to be processed
if ($DryRun) {
    Write-Host "ðŸ” DRY RUN MODE - Repositories to backup:`n" -ForegroundColor Yellow
    foreach ($repo in $repos) {
        $isMCP = Test-MCPRepository -RepoName $repo.Name
        $type = if ($isMCP) { "MCP" } else { "Other" }
        $color = if ($isMCP) { "Green" } else { "Cyan" }
        Write-Host "  âœ… $($repo.Name) ($type)" -ForegroundColor $color
    }
    Write-Host "`nâœ… Dry run complete - $($repos.Count) repositories would be backed up`n" -ForegroundColor Yellow
    exit 0
}

# Get the SOTA backup script path
$sotaBackupScript = Join-Path $ReposRoot "mcp-central-docs\sota-scripts\backup-system\backup-repo.ps1"
if (-not (Test-Path $sotaBackupScript)) {
    Write-Host "âŒ SOTA backup script not found: $sotaBackupScript" -ForegroundColor Red
    Write-Host "Please ensure the mcp-central-docs repository is available with the SOTA backup script." -ForegroundColor Red
    exit 1
}

# Define backup targets
function Get-BackupTargets {
    if ($TargetDir) {
        # Custom target directory only
        return @(@{ Name = "Custom"; Path = $TargetDir })
    } else {
        # Default targets
        $desktopTarget = Join-Path ([Environment]::GetFolderPath("Desktop")) "repo backup"
        $networkTarget = "N:\backup\dev\repo-backups"
        $oneDriveTarget = Join-Path (Join-Path $env:OneDrive "Backup") "repo-backups"
        
        return @(
            @{ Name = "Desktop"; Path = $desktopTarget },
            @{ Name = "Network"; Path = $networkTarget },
            @{ Name = "OneDrive"; Path = $oneDriveTarget }
        )
    }
}

$success = 0
$failed = 0
$skipped = 0
$startTime = Get-Date
$backupTargets = Get-BackupTargets

foreach ($repo in $repos) {
    Write-Host "â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”â”" -ForegroundColor Gray
    Write-Host "ðŸ“¦ Repository: $($repo.Name)" -ForegroundColor Cyan
    
    $isMCP = Test-MCPRepository -RepoName $repo.Name
    $type = if ($isMCP) { "MCP" } else { "Other" }
    Write-Host "  ðŸ·ï¸  Type: $type" -ForegroundColor Gray
    
    try {
        Push-Location $repo.FullName
        
        # Check if it's a valid repository
        $isValidRepo = (Test-Path ".git") -or (Test-Path "pyproject.toml") -or (Test-Path "package.json")
        if (-not $isValidRepo) {
            Write-Host "  â­ï¸  Not a valid repository (no .git, pyproject.toml, or package.json) - skipping" -ForegroundColor Yellow
            $skipped++
            continue
        }
        
        # Generate backup filename
        $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
        $backupName = "$($repo.Name)_backup_${timestamp}.zip"
        
        # Create backup in primary target only
        $primaryTarget = $backupTargets[0]
        $primaryBackupPath = Join-Path $primaryTarget.Path $backupName
        
        Write-Host "  ðŸ”„ Creating backup in primary target: $($primaryTarget.Name)" -ForegroundColor Gray
        Write-Host "  ðŸ“‚ Primary path: $primaryBackupPath" -ForegroundColor DarkGray
        
        # Ensure primary target directory exists
        if (-not (Test-Path $primaryTarget.Path)) {
            New-Item -ItemType Directory -Path $primaryTarget.Path -Force | Out-Null
        }
        
        # Create temporary backup script that only saves to primary target
        $tempBackupScript = Join-Path $env:TEMP "temp-backup-$($repo.Name)-$timestamp.ps1"
        $backupScriptContent = @"
#!/usr/bin/env pwsh
# Temporary backup script for $($repo.Name)
# Modified to only save to primary target: $($primaryTarget.Name)
# Enhanced with locked file exclusions

# Import the real backup script but override destinations and exclusions
`$script:BackupDestinations = @(
    @{ Name = "$($primaryTarget.Name)"; Path = "$($primaryTarget.Path)"; BackupPath = "$primaryBackupPath"; Enabled = `$true }
)

# Enhanced exclusions for locked files
`$script:Exclusions = @(
    ".venv", "venv", "env", ".env",
    "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache", "htmlcov",
    "node_modules",
    "*.pyc", "*.pyo", "*.pyd",
    ".DS_Store", "Thumbs.db",
    ".windsurf", ".cursor", ".snapshots",
    "*.log", "*.bak", "*.backup", "*.tmp", "*.temp",
    ".vbox", "*.vdi", "*.vmdk", "*.vhd", "*.vbox-prev",
    "MagicMock", "sandboxes", "quarantine", "analysis", "backups",
    "*.dxt", "*.db-shm", "*.db-wal",
    "gtfs_data", "gtfs_output", "extracted_data",
    "*.csv", "*.tsv", "*.txt", "*.bin", "*.dat",
    # Rust-specific exclusions (CRITICAL for rustdesk repos)
    "target", "Cargo.lock",
    # Additional locked file exclusions
    "*.exe", "*.dll", "*.pdb", "*.so", "*.dylib",
    "rustdesk.exe", "hbbs.exe", "hbbr.exe",
    "target/debug/*.exe", "target/release/*.exe",
    "target/*/deps/*.rlib",
    "*.db", "*.sqlite", "*.sqlite3",
    "*.lock", "*.pid", "*.pidfile",
    "*.swp", "*.swo", "*.cache", "*.lockfile",
    "docker-compose.override.yml",
    "Procfile"
)

# Run the real backup script with enhanced exclusions
& "$sotaBackupScript" -WhatIf:`$DryRun $(if ($IncludeBuild) { "-IncludeBuild" })
"@
        
        $backupScriptContent | Out-File -FilePath $tempBackupScript -Encoding UTF8
        
        # Run the modified backup script
        & $tempBackupScript
        
        # Clean up temp script
        Remove-Item $tempBackupScript -Force -ErrorAction SilentlyContinue
        
        if ($LASTEXITCODE -eq 0 -or $null -eq $LASTEXITCODE) {
            Write-Host "  âœ… Primary backup created: $($repo.Name)" -ForegroundColor Green
            
            # Copy to additional targets if not using custom TargetDir
            if (-not $TargetDir -and $backupTargets.Count -gt 1) {
                Write-Host "  ðŸ“‹ Copying to additional targets..." -ForegroundColor Gray
                
                for ($i = 1; $i -lt $backupTargets.Count; $i++) {
                    $target = $backupTargets[$i]
                    $targetBackupPath = Join-Path $target.Path $backupName
                    
                    try {
                        # Ensure target directory exists
                        if (-not (Test-Path $target.Path)) {
                            New-Item -ItemType Directory -Path $target.Path -Force | Out-Null
                        }
                        
                        # Copy the backup file
                        Copy-Item $primaryBackupPath $targetBackupPath -Force
                        Write-Host "    âœ… Copied to $($target.Name): $($target.Path)" -ForegroundColor Green
                    }
                    catch {
                        Write-Host "    âŒ Failed to copy to $($target.Name): $($_.Exception.Message)" -ForegroundColor Red
                    }
                }
            }
            
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

Write-Host "â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•-" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "â•‘           ðŸ“¦ BACKUP OPERATION COMPLETE! ðŸ“¦                â•‘" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })
Write-Host "â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•`n" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Yellow" })

Write-Host "ðŸ“Š Summary:" -ForegroundColor White
Write-Host "  Total repos found:    $($allRepos.Count)" -ForegroundColor Gray
Write-Host "  Repos processed:      $($repos.Count)" -ForegroundColor White
Write-Host "  Successful:           $success" -ForegroundColor Green
Write-Host "  Failed:               $failed" -ForegroundColor Red
Write-Host "  Skipped:              $skipped" -ForegroundColor Yellow
Write-Host "  Duration:             $([math]::Round($duration.TotalMinutes, 1)) minutes`n" -ForegroundColor Cyan

Write-Host "ðŸŽ¯ Filtering:" -ForegroundColor Cyan
Write-Host "  MCP Only:             $MCPOnly" -ForegroundColor White
if ($MCPOnly) {
    Write-Host "  MCP repos found:      $($repos.Count)" -ForegroundColor Green
    Write-Host "  Non-MCP repos skipped: $($allRepos.Count - $repos.Count)" -ForegroundColor Gray
}
Write-Host ""

Write-Host "ðŸ’¾ Backup locations:" -ForegroundColor Cyan
if ($TargetDir) {
    Write-Host "  Custom:              $TargetDir" -ForegroundColor White
} else {
    Write-Host "  Primary:             $($backupTargets[0].Path)" -ForegroundColor Green
    if ($backupTargets.Count -gt 1) {
        for ($i = 1; $i -lt $backupTargets.Count; $i++) {
            Write-Host "  Copy target #$($i):     $($backupTargets[$i].Path)" -ForegroundColor White
        }
    }
}
Write-Host ""

if ($failed -gt 0) {
    Write-Host "âš ï¸  Some backups failed. Check output above for details." -ForegroundColor Yellow
    exit 1
}
elseif ($skipped -gt 0) {
    Write-Host "âœ… Backup process completed with some repos skipped.`n" -ForegroundColor Green
    exit 0
}
else {
    Write-Host "âœ… All backups completed successfully!`n" -ForegroundColor Green
    exit 0
}
