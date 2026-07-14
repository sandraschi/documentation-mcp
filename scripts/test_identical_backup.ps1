#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test script for identical backup detection
#>

param(
    [switch]$SaveIdent = $false
)

Write-Host "ðŸ§ª Testing Identical Backup Detection`n" -ForegroundColor Cyan

# Create test directory
$testDir = "C:\Temp\IdenticalBackupTest"
if (-not (Test-Path $testDir)) {
    New-Item -ItemType Directory -Path $testDir -Force | Out-Null
}

# Test with a small repo - rustdesk-mcp
$repoPath = "d:\Dev\repos\rustdesk-mcp"
if (Test-Path $repoPath) {
    Write-Host "ðŸ“¦ Testing with rustdesk-mcp repository..." -ForegroundColor Yellow
    
    Push-Location $repoPath
    
    # First backup
    Write-Host "`nðŸ”„ === FIRST BACKUP ===" -ForegroundColor Green
    $timestamp1 = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $backupName1 = "rustdesk-mcp_test_${timestamp1}.zip"
    $backupPath1 = Join-Path $testDir $backupName1
    
    Write-Host "  ðŸ“‚ Creating first backup: $backupName1" -ForegroundColor Gray
    
    # Create temporary backup script
    $tempScript1 = Join-Path $env:TEMP "rustdesk-test-backup-1.ps1"
    $scriptContent1 = @"
#!/usr/bin/env pwsh
# Test backup 1 for rustdesk-mcp

# Define enhanced exclusions for locked files
`$exclusions = @(
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
    # Rust-specific exclusions
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

Write-Host "ðŸš« Excluding locked files and problematic patterns..." -ForegroundColor Gray

# Get all files and filter
`$allFiles = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    -not (`$_.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
}

`$backupFiles = `$allFiles | Where-Object {
    `$file = `$_
    `$shouldExclude = `$false
    
    foreach (`$excl in `$exclusions) {
        `$pattern = `$excl -replace '\*', '.*' -replace '\.', '\.'
        if (`$file.FullName -match `$pattern -or `$file.FullName -match [regex]::Escape(`$excl)) {
            `$shouldExclude = `$true
            break
        }
    }
    
    -not `$shouldExclude
}

Write-Host "ðŸ“Š Found `$(`$backupFiles.Count) files to backup" -ForegroundColor Green

# Create ZIP
if (`$backupFiles.Count -gt 0) {
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        `$zip = [System.IO.Compression.ZipFile]::Open(`$backupPath1, [System.IO.Compression.ZipArchiveMode]::Create)
        
        `$filesAdded = 0
        `$filesFailed = 0
        
        foreach (`$file in `$backupFiles) {
            try {
                `$relativePath = `$file.FullName.Substring((Get-Location).Path.Length + 1)
                `$zipEntryPath = `$relativePath -replace '\\', '/'
                
                [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                    `$zip, 
                    `$file.FullName, 
                    `$zipEntryPath, 
                    [System.IO.Compression.CompressionLevel]::Optimal
                ) | Out-Null
                
                `$filesAdded++
            }
            catch {
                `$filesFailed++
                Write-Host "âš ï¸  Failed to add: `$(`$file.Name)" -ForegroundColor Yellow
            }
        }
        
        `$zip.Dispose()
        
        if (Test-Path `$backupPath1) {
            `$size = [math]::Round((Get-Item `$backupPath1).Length / 1MB, 2)
            Write-Host "âœ… Backup created: `$size MB (`$filesAdded files, `$filesFailed failed)" -ForegroundColor Green
        } else {
            Write-Host "âŒ Backup file not created" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "âŒ Backup failed: `$(`$_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "âš ï¸  No files to backup" -ForegroundColor Yellow
}
"@
    
    $scriptContent1 | Out-File -FilePath $tempScript1 -Encoding UTF8
    & $tempScript1
    Remove-Item $tempScript1 -Force -ErrorAction SilentlyContinue
    
    # Wait a moment to ensure different timestamps
    Start-Sleep -Seconds 2
    
    # Second backup
    Write-Host "`nðŸ”„ === SECOND BACKUP ===" -ForegroundColor Green
    $timestamp2 = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $backupName2 = "rustdesk-mcp_test_${timestamp2}.zip"
    $backupPath2 = Join-Path $testDir $backupName2
    
    Write-Host "  ðŸ“‚ Creating second backup: $backupName2" -ForegroundColor Gray
    Write-Host "  ðŸ”§ SaveIdent: $SaveIdent" -ForegroundColor Gray
    
    # Create second temporary backup script (identical content)
    $tempScript2 = Join-Path $env:TEMP "rustdesk-test-backup-2.ps1"
    $scriptContent2 = @"
#!/usr/bin/env pwsh
# Test backup 2 for rustdesk-mcp

# Define enhanced exclusions for locked files
`$exclusions = @(
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
    # Rust-specific exclusions
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

Write-Host "ðŸš« Excluding locked files and problematic patterns..." -ForegroundColor Gray

# Get all files and filter
`$allFiles = Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    -not (`$_.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
}

`$backupFiles = `$allFiles | Where-Object {
    `$file = `$_
    `$shouldExclude = `$false
    
    foreach (`$excl in `$exclusions) {
        `$pattern = `$excl -replace '\*', '.*' -replace '\.', '\.'
        if (`$file.FullName -match `$pattern -or `$file.FullName -match [regex]::Escape(`$excl)) {
            `$shouldExclude = `$true
            break
        }
    }
    
    -not `$shouldExclude
}

Write-Host "ðŸ“Š Found `$(`$backupFiles.Count) files to backup" -ForegroundColor Green

# Create ZIP
if (`$backupFiles.Count -gt 0) {
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        `$zip = [System.IO.Compression.ZipFile]::Open("$backupPath2", [System.IO.Compression.ZipArchiveMode]::Create)
        
        `$filesAdded = 0
        `$filesFailed = 0
        
        foreach (`$file in `$backupFiles) {
            try {
                `$relativePath = `$file.FullName.Substring((Get-Location).Path.Length + 1)
                `$zipEntryPath = `$relativePath -replace '\\', '/'
                
                [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                    `$zip, 
                    `$file.FullName, 
                    `$zipEntryPath, 
                    [System.IO.Compression.CompressionLevel]::Optimal
                ) | Out-Null
                
                `$filesAdded++
            }
            catch {
                `$filesFailed++
                Write-Host "âš ï¸  Failed to add: `$(`$file.Name)" -ForegroundColor Yellow
            }
        }
        
        `$zip.Dispose()
        
        if (Test-Path "$backupPath2") {
            `$size = [math]::Round((Get-Item "$backupPath2").Length / 1MB, 2)
            Write-Host "âœ… Backup created: `$size MB (`$filesAdded files, `$filesFailed failed)" -ForegroundColor Green
        } else {
            Write-Host "âŒ Backup file not created" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "âŒ Backup failed: `$(`$_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "âš ï¸  No files to backup" -ForegroundColor Yellow
}
"@
    $scriptContent2 | Out-File -FilePath $tempScript2 -Encoding UTF8
    & $tempScript2
    Remove-Item $tempScript2 -Force -ErrorAction SilentlyContinue
    
    # Test identical backup detection
    Write-Host "`nðŸ” === TESTING IDENTICAL DETECTION ===" -ForegroundColor Yellow
    
    if ((Test-Path $backupPath1) -and (Test-Path $backupPath2)) {
        Write-Host "  ðŸ“ Both backups created successfully" -ForegroundColor Green
        
        # Compute hashes
        $hash1 = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.IO.File]::ReadAllBytes($backupPath1))
        $hash1Str = [System.BitConverter]::ToString($hash1) -replace '-', ''
        
        $hash2 = [System.Security.Cryptography.SHA256]::Create().ComputeHash([System.IO.File]::ReadAllBytes($backupPath2))
        $hash2Str = [System.BitConverter]::ToString($hash2) -replace '-', ''
        
        Write-Host "  ðŸ” Hash 1: $hash1Str" -ForegroundColor DarkGray
        Write-Host "  ðŸ” Hash 2: $hash2Str" -ForegroundColor DarkGray
        
        $isIdentical = ($hash1Str -eq $hash2Str)
        
        if ($isIdentical) {
            Write-Host "  âœ… Hashes match - backups are identical" -ForegroundColor Yellow
            
            if (-not $SaveIdent) {
                Write-Host "  ðŸ-‘ï¸  Simulating removal of identical backup..." -ForegroundColor Yellow
                try {
                    Remove-Item $backupPath2 -Force
                    Write-Host "  âœ… Identical backup removed" -ForegroundColor Green
                }
                catch {
                    Write-Host "  âŒ Failed to remove: $($_.Exception.Message)" -ForegroundColor Red
                }
            } else {
                Write-Host "  ðŸ’¾ Preserving identical backup (SaveIdent enabled)" -ForegroundColor Green
            }
        } else {
            Write-Host "  âŒ Hashes differ - backups are different" -ForegroundColor Red
        }
    } else {
        Write-Host "  âŒ One or both backups failed to create" -ForegroundColor Red
    }
    
    # Show final state
    Write-Host "`nðŸ“‹ === FINAL STATE ===" -ForegroundColor Cyan
    $finalBackups = Get-ChildItem -Path $testDir -Filter "*.zip" -File | Sort-Object LastWriteTime -Descending
    Write-Host "  ðŸ“¦ Remaining backups: $($finalBackups.Count)" -ForegroundColor White
    
    foreach ($backup in $finalBackups) {
        $size = [math]::Round((Get-Item $backup.FullName).Length / 1MB, 2)
        Write-Host "    - $($backup.Name) ($size MB)" -ForegroundColor Gray
    }
    
    Pop-Location
} else {
    Write-Host "âŒ Repository not found: $repoPath" -ForegroundColor Red
}

Write-Host "`nðŸ§ª Test finished!" -ForegroundColor Cyan
