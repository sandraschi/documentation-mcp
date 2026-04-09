# Docker Daemon Fix Script (PowerShell) - Run as Administrator
# Comprehensive cleanup and optimization for unresponsive daemon (AI workloads)

param(
    [switch]$SkipPrune,
    [switch]$DryRun
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

function Invoke-DockerCommand {
    param([string]$Command, [bool]$Critical = $false)
    
    try {
        if ($DryRun) {
            Write-Status "DRY RUN: docker $Command" "INFO"
            return
        }
        
        $result = Invoke-Expression "docker $Command" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Success: $Command" "SUCCESS"
            return $result
        } else {
            if ($Critical) {
                Write-Status "FAILED (critical): $Command - $result" "ERROR"
                exit 1
            } else {
                Write-Status "WARNING: $Command - $result" "WARN"
            }
        }
    }
    catch {
        if ($Critical) {
            Write-Status "ERROR: $($_.Exception.Message)" "ERROR"
            exit 1
        } else {
            Write-Status "WARNING: $($_.Exception.Message)" "WARN"
        }
    }
}

# ============================================================================
# Main Script
# ============================================================================

Write-Host "`n========== Docker Daemon Fix Script ==========" -ForegroundColor Cyan

# Check admin
if (-not (Test-Admin)) {
    Write-Status "ERROR: This script must run as Administrator" "ERROR"
    exit 1
}

Write-Status "Running as Administrator" "SUCCESS"

if ($DryRun) {
    Write-Status "DRY RUN MODE - no changes will be made" "WARN"
}

# 1. Check Docker daemon status
Write-Host "`n--- Step 1: Docker Daemon Status ---" -ForegroundColor Cyan
try {
    $daemon = docker version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Docker daemon is responsive" "SUCCESS"
    } else {
        Write-Status "Docker daemon appears unresponsive - attempting restart" "WARN"
        Restart-DockerDesktop
    }
}
catch {
    Write-Status "Cannot reach Docker daemon - ensure Docker Desktop is running" "ERROR"
    exit 1
}

# 2. System disk usage
Write-Host "`n--- Step 2: Current Disk Usage ---" -ForegroundColor Cyan
$diskUsage = docker system df 2>&1
Write-Host $diskUsage -ForegroundColor Gray

# 3. Stop all containers (before cleanup)
Write-Host "`n--- Step 3: Stopping All Containers ---" -ForegroundColor Cyan
$runningContainers = docker ps -q 2>/dev/null
if ($runningContainers) {
    Write-Status "Found running containers - stopping gracefully" "INFO"
    if (-not $DryRun) {
        docker stop $(docker ps -q) 2>&1 | Out-Null
    }
    Start-Sleep -Seconds 2
} else {
    Write-Status "No running containers" "SUCCESS"
}

# 4. Remove exited containers
Write-Host "`n--- Step 4: Removing Exited Containers ---" -ForegroundColor Cyan
Invoke-DockerCommand "container prune -f" $false

# 5. Remove unused images
if (-not $SkipPrune) {
    Write-Host "`n--- Step 5: Removing Unused Images ---" -ForegroundColor Cyan
    Invoke-DockerCommand "image prune -a -f" $false
}

# 6. Remove unused volumes
Write-Host "`n--- Step 6: Removing Unused Volumes ---" -ForegroundColor Cyan
Invoke-DockerCommand "volume prune -f" $false

# 7. Prune build cache
Write-Host "`n--- Step 7: Clearing Build Cache ---" -ForegroundColor Cyan
Invoke-DockerCommand "builder prune -a -f" $false

# 8. Full system prune
if (-not $SkipPrune) {
    Write-Host "`n--- Step 8: Full System Prune ---" -ForegroundColor Cyan
    Invoke-DockerCommand "system prune -a -f --volumes" $false
}

# 9. Configure daemon.json for optimal AI workload performance
Write-Host "`n--- Step 9: Configuring Docker Daemon Settings ---" -ForegroundColor Cyan
$daemonJsonPath = "$env:APPDATA\Docker\daemon.json"

$daemonConfig = @{
    "log-driver" = "json-file"
    "log-opts"   = @{
        "max-size" = "100m"
        "max-file" = "3"
    }
    "storage-driver" = "overlay2"
    "storage-opts"   = @("overlay2.override_kernel_check=true")
    "debug"          = $false
}

if (-not $DryRun) {
    try {
        # Read existing config if present
        if (Test-Path $daemonJsonPath) {
            $existing = Get-Content $daemonJsonPath | ConvertFrom-Json
            # Merge configs (new values override)
            $daemonConfig.PSObject.Properties | ForEach-Object {
                $existing | Add-Member -NotePropertyName $_.Name -NotePropertyValue $_.Value -Force
            }
            $daemonConfig = $existing
        }
        
        $daemonConfig | ConvertTo-Json | Set-Content $daemonJsonPath
        Write-Status "Updated daemon.json with log rotation and performance settings" "SUCCESS"
    }
    catch {
        Write-Status "Could not update daemon.json: $($_.Exception.Message)" "WARN"
    }
}

# 10. Check Docker Desktop resource settings
Write-Host "`n--- Step 10: Docker Desktop Resource Recommendations ---" -ForegroundColor Cyan
$settingsPath = "$env:APPDATA\Docker\settings.json"
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath | ConvertFrom-Json
    $currentMem = $settings.memoryMiB
    $currentCpu = $settings.cpus
    
    Write-Status "Current Memory: $currentMem MB | Current CPUs: $currentCpu" "INFO"
    
    if ($currentMem -lt 8192) {
        Write-Status "RECOMMENDED: Increase memory to at least 12288 MB (12GB) for AI workloads" "WARN"
        Write-Status "RECOMMENDED: Increase CPUs to at least 4 cores" "WARN"
        Write-Host "  Edit: $settingsPath and update memoryMiB and cpus values, then restart Docker Desktop" -ForegroundColor Yellow
    } else {
        Write-Status "Memory allocation is adequate" "SUCCESS"
    }
} else {
    Write-Status "Could not read Docker Desktop settings - manually verify: Settings > Resources > Memory (12GB+)" "WARN"
}

# 11. Network prune
Write-Host "`n--- Step 11: Removing Unused Networks ---" -ForegroundColor Cyan
Invoke-DockerCommand "network prune -f" $false

# 12. Final status
Write-Host "`n--- Final Status ---" -ForegroundColor Cyan
$finalDiskUsage = docker system df 2>&1
Write-Host $finalDiskUsage -ForegroundColor Gray

Write-Status "Cleanup complete!" "SUCCESS"

# Restart recommendation
Write-Host "`n--- Next Steps ---" -ForegroundColor Cyan
Write-Host @"
1. Restart Docker Desktop for daemon settings to take effect:
   - Click Docker icon in system tray > Restart Docker Desktop

2. Monitor performance during AI workloads:
   - Open PowerShell and run: docker stats --no-stream

3. Set resource limits on your AI containers in docker-compose.yml:
   services:
     ai-service:
       deploy:
         resources:
           limits:
             memory: 12g
             cpus: '4'
           reservations:
             memory: 8g
             cpus: '3'

4. Run this script periodically (weekly recommended) for maintenance
"@ -ForegroundColor Cyan

Write-Host "`n========================================`n" -ForegroundColor Cyan
