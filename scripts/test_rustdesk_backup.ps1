#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Test script for rustdesk backup with locked file handling
#>

param(
    [string]$TargetDir = "C:\Temp\RustdeskTest"
)

Write-Host "🧪 Testing Rustdesk Backup with Locked File Handling`n" -ForegroundColor Cyan

# Create test directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# Test just rustdesk-mcp
$repoPath = "d:\Dev\repos\rustdesk-mcp"
if (Test-Path $repoPath) {
    Write-Host "📦 Testing rustdesk-mcp backup..." -ForegroundColor Yellow
    
    Push-Location $repoPath
    
    # Create enhanced backup script with locked file exclusions
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $backupName = "rustdesk-mcp_test_${timestamp}.zip"
    $backupPath = Join-Path $TargetDir $backupName
    
    Write-Host "  📂 Target: $backupPath" -ForegroundColor Gray
    
    # Create temporary backup script
    $tempScript = Join-Path $env:TEMP "rustdesk-test-backup.ps1"
    $scriptContent = @"
#!/usr/bin/env pwsh
# Enhanced backup for rustdesk-mcp with locked file handling

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
    # Rustdesk-specific locked files
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

Write-Host "🚫 Excluding locked files and problematic patterns..." -ForegroundColor Gray
foreach (`$excl in `$exclusions) {
    Write-Host "  - `$excl" -ForegroundColor DarkGray
}

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

Write-Host "📊 Found `$(`$backupFiles.Count) files to backup (excluded `$(`$allFiles.Count - `$backupFiles.Count) files)" -ForegroundColor Green

# Create ZIP
if (`$backupFiles.Count -gt 0) {
    try {
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        `$zip = [System.IO.Compression.ZipFile]::Open(`$backupPath, [System.IO.Compression.ZipArchiveMode]::Create)
        
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
                Write-Host "⚠️  Failed to add: `$(`$file.Name)" -ForegroundColor Yellow
            }
        }
        
        `$zip.Dispose()
        
        if (Test-Path `$backupPath) {
            `$size = [math]::Round((Get-Item `$backupPath).Length / 1MB, 2)
            Write-Host "✅ Backup created: `$size MB (`$filesAdded files, `$filesFailed failed)" -ForegroundColor Green
        } else {
            Write-Host "❌ Backup file not created" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "❌ Backup failed: `$(`$_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "⚠️  No files to backup" -ForegroundColor Yellow
}
"@
    
    $scriptContent | Out-File -FilePath $tempScript -Encoding UTF8
    
    # Run the test backup
    & $tempScript
    
    # Cleanup
    Remove-Item $tempScript -Force -ErrorAction SilentlyContinue
    
    Pop-Location
    
    Write-Host "`n✅ Test complete!" -ForegroundColor Green
    if (Test-Path $backupPath) {
        $size = [math]::Round((Get-Item $backupPath).Length / 1MB, 2)
        Write-Host "📦 Backup file: $backupPath ($size MB)" -ForegroundColor Cyan
    }
} else {
    Write-Host "❌ Repository not found: $repoPath" -ForegroundColor Red
}

Write-Host "`n🧪 Test finished!" -ForegroundColor Cyan
