# Docker Desktop Update & Recovery Script (PowerShell)
# Run as Administrator to fix update elevation errors
# Usage: Right-click PowerShell and select "Run as Administrator"
# Then: .\update-docker-desktop.ps1

param(
    [switch]$FullWipe  # Use -FullWipe to also clear Docker app data (more aggressive)
)

function Write-Status {
    param([string]$Message, [string]$Status = "INFO")
    $color = @{
        "INFO"    = "Cyan"
        "SUCCESS" = "Green"
        "WARN"    = "Yellow"
        "ERROR"   = "Red"
    }
    Write-Host "[$Status] $Message" -ForegroundColor $color[$Status]
}

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check admin
if (-not (Test-Admin)) {
    Write-Status "ERROR: This script must run as Administrator" "ERROR"
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n========== Docker Desktop Update & Recovery ==========" -ForegroundColor Cyan
Write-Status "Running as Administrator" "SUCCESS"

if ($FullWipe) {
    Write-Status "FULL WIPE MODE: Will also clear Docker app data" "WARN"
}

# 1. Stop Docker Desktop
Write-Host "`n[1/5] Stopping Docker Desktop..." -ForegroundColor Cyan
try {
    Stop-Process -Name "Docker Desktop" -Force -ErrorAction SilentlyContinue
    Stop-Process -Name "com.docker.backend" -Force -ErrorAction SilentlyContinue
    Stop-Process -Name "vpnkit" -Force -ErrorAction SilentlyContinue
    Write-Status "Docker Desktop stopped" "SUCCESS"
    Start-Sleep -Seconds 2
}
catch {
    Write-Status "Docker was not running (OK)" "INFO"
}

# 2. Clear update temp folder
Write-Host "`n[2/5] Clearing Docker update temp folder..." -ForegroundColor Cyan
$tempPath = "$env:LOCALAPPDATA\Temp\DockerDesktopUpdates"
if (Test-Path $tempPath) {
    try {
        Remove-Item -Path $tempPath -Recurse -Force
        Write-Status "Removed: $tempPath" "SUCCESS"
    }
    catch {
        Write-Status "Could not remove temp folder: $_" "WARN"
    }
} else {
    Write-Status "Temp folder already clean" "INFO"
}

# 3. Optional: Clear Docker app data (full wipe)
if ($FullWipe) {
    Write-Host "`n[3/5] Clearing Docker app data..." -ForegroundColor Cyan
    
    $appDataPath = "$env:APPDATA\Docker"
    if (Test-Path $appDataPath) {
        try {
            Remove-Item -Path $appDataPath -Recurse -Force
            Write-Status "Removed: $appDataPath" "SUCCESS"
        }
        catch {
            Write-Status "Could not remove app data: $_" "WARN"
        }
    }
    
    $localAppPath = "$env:LOCALAPPDATA\Docker"
    if (Test-Path $localAppPath) {
        try {
            Remove-Item -Path $localAppPath -Recurse -Force
            Write-Status "Removed: $localAppPath" "SUCCESS"
        }
        catch {
            Write-Status "Could not remove local app: $_" "WARN"
        }
    }
} else {
    Write-Host "`n[3/5] Skipping app data wipe (use -FullWipe for aggressive reset)" -ForegroundColor Gray
}

# 4. Restart Docker Desktop
Write-Host "`n[4/5] Restarting Docker Desktop..." -ForegroundColor Cyan
try {
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        & $dockerPath
        Write-Status "Docker Desktop started" "SUCCESS"
        Write-Host "Waiting for daemon to initialize..." -ForegroundColor Gray
        Start-Sleep -Seconds 5
    } else {
        Write-Status "Docker Desktop not found at expected location" "ERROR"
        Write-Host "Install Docker Desktop from: https://hub.docker.com/" -ForegroundColor Yellow
        exit 1
    }
}
catch {
    Write-Status "Could not start Docker: $_" "ERROR"
    exit 1
}

# 5. Check daemon status
Write-Host "`n[5/5] Checking Docker daemon status..." -ForegroundColor Cyan
$maxAttempts = 15
$attempt = 1

while ($attempt -le $maxAttempts) {
    try {
        $version = docker version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Docker daemon is responsive" "SUCCESS"
            Write-Host "`nDocker version info:" -ForegroundColor Gray
            docker version
            goto :success
        }
    }
    catch {}
    
    Write-Host "  Attempt $attempt/$maxAttempts - waiting for daemon..." -ForegroundColor Gray
    Start-Sleep -Seconds 2
    $attempt++
}

Write-Status "Docker daemon not responding after $maxAttempts attempts" "WARN"
Write-Host "Docker may still be initializing. Check Docker Desktop icon in system tray." -ForegroundColor Yellow

:success
Write-Host "`n========== Recovery Complete ==========" -ForegroundColor Cyan

Write-Host @"

Next steps:
1. Wait 30 seconds for Docker Desktop to fully start
2. Open Docker Desktop Settings (gear icon in tray)
3. Go to Settings > Check for Updates
4. Install any available updates

If update still fails:
- Restart Windows: `restart-computer`
- Download fresh installer: https://hub.docker.com/
- Or use full wipe next time: .\update-docker-desktop.ps1 -FullWipe

Troubleshooting:
- Check logs: `docker logs <container>`
- Check disk space: `docker system df`
- Check daemon: `docker ps`

"@ -ForegroundColor Cyan

Write-Host "========================================`n" -ForegroundColor Cyan
