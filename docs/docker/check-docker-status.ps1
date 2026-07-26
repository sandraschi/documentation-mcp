# Docker Status Checker Script (PowerShell)
# Comprehensive health check for Docker Desktop installation and daemon
# Detects hanging daemon and attempts recovery
# Shows last 10 images and containers
# Usage: .\check-docker-status.ps1

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

Write-Host "`n========== Docker Status Checker ==========" -ForegroundColor Cyan
Write-Host "Comprehensive health check + hang detection`n" -ForegroundColor Gray

# 1. Check if Docker is installed
Write-Host "[1/10] Checking Docker installation..." -ForegroundColor Cyan
$dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
if (Test-Path $dockerPath) {
    Write-Status "Docker Desktop found at: $dockerPath" "SUCCESS"
} else {
    Write-Status "Docker Desktop not installed" "ERROR"
    Write-Host "Install from: https://hub.docker.com/" -ForegroundColor Yellow
    exit 1
}

# 2. Check if Docker daemon is running (with hang detection via timeout)
Write-Host "`n[2/10] Checking Docker daemon (with hang detection)..." -ForegroundColor Cyan

$daemonHealthy = $false
$daemonHanging = $false

# Test with 5-second timeout (if hangs longer = daemon is stuck)
$job = Start-Job -ScriptBlock { 
    $ErrorActionPreference = "SilentlyContinue"
    docker version 2>$null
} -Timeout 5

# Wait for job with timeout
$completed = Wait-Job -Job $job -Timeout 5
if ($completed) {
    $result = Receive-Job -Job $job
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Docker daemon is running and responsive (no hang detected)" "SUCCESS"
        $daemonHealthy = $true
    } else {
        Write-Status "Docker daemon not responding - will attempt restart" "WARN"
    }
    Remove-Job -Job $job -Force -ErrorAction SilentlyContinue
} else {
    # Timeout = daemon is hanging
    Write-Status "⚠️  DAEMON HANGING DETECTED (command timeout after 5s)" "ERROR"
    $daemonHanging = $true
    Remove-Job -Job $job -Force
    
    # Auto-recovery: kill hung processes and restart
    Write-Host "`nAttempting automatic recovery..." -ForegroundColor Yellow
    Write-Status "Killing hung Docker processes" "WARN"
    
    taskkill /IM "Docker Desktop.exe" /F >$null 2>&1
    taskkill /IM "com.docker.backend.exe" /F >$null 2>&1
    taskkill /IM "vpnkit.exe" /F >$null 2>&1
    Start-Sleep -Seconds 3
    
    Write-Status "Restarting Docker Desktop" "INFO"
    & $dockerPath
    Start-Sleep -Seconds 8
    
    # Retry daemon check after restart
    Write-Status "Verifying daemon after restart..." "INFO"
    $retryJob = Start-Job -ScriptBlock { 
        $ErrorActionPreference = "SilentlyContinue"
        docker version 2>$null
    } -Timeout 5
    
    $retryCompleted = Wait-Job -Job $retryJob -Timeout 5
    if ($retryCompleted) {
        $retryResult = Receive-Job -Job $retryJob
        if ($LASTEXITCODE -eq 0) {
            Write-Status "✅ Docker daemon recovered successfully (no longer hanging)" "SUCCESS"
            $daemonHealthy = $true
            $daemonHanging = $false
        } else {
            Write-Status "❌ Daemon still unresponsive after restart" "ERROR"
        }
    } else {
        Write-Status "❌ Daemon STILL HANGING after restart attempt" "ERROR"
        Write-Host "`nDaemon is unrecoverable. Try full reset:" -ForegroundColor Red
        Write-Host "   .\\update-docker-desktop.ps1 -FullWipe`n" -ForegroundColor Yellow
    }
    Remove-Job -Job $retryJob -Force -ErrorAction SilentlyContinue
}

# If daemon isn't healthy and wasn't hanging, try starting it
if (-not $daemonHealthy -and -not $daemonHanging) {
    Write-Status "Docker daemon not responding - attempting start..." "WARN"
    & $dockerPath
    Start-Sleep -Seconds 5
    docker version >$null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Docker daemon started successfully" "SUCCESS"
        $daemonHealthy = $true
    } else {
        Write-Status "Docker daemon failed to start" "ERROR"
    }
}

# 3. Check Docker version
Write-Host "`n[3/10] Docker version..." -ForegroundColor Cyan
if ($daemonHealthy) {
    $dockerInfo = docker version --format "{{.Server.Version}}"
    Write-Host "  Docker: $dockerInfo" -ForegroundColor Gray
}

# 4. Check last 10 built images
Write-Host "`n[4/10] Last 10 built images..." -ForegroundColor Cyan
if ($daemonHealthy) {
    $images = docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" | Select-Object -Skip 1 -First 10
    if ($images) {
        Write-Status "Recent images:" "SUCCESS"
        $images | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    } else {
        Write-Status "No images found" "INFO"
    }
} else {
    Write-Status "Skipped (daemon not healthy)" "WARN"
}

# 5. Check last 10 containers (all states)
Write-Host "`n[5/10] Last 10 containers (all states)..." -ForegroundColor Cyan
if ($daemonHealthy) {
    $containers = docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}" | Select-Object -Skip 1 -First 10
    if ($containers) {
        Write-Status "Recent containers:" "SUCCESS"
        $containers | ForEach-Object {
            Write-Host "  $_" -ForegroundColor Gray
        }
    } else {
        Write-Status "No containers found" "INFO"
    }
} else {
    Write-Status "Skipped (daemon not healthy)" "WARN"
}

# 6. Check running containers summary
Write-Host "`n[6/10] Running containers summary..." -ForegroundColor Cyan
if ($daemonHealthy) {
    $runningCount = (docker ps -q | Measure-Object).Count
    $stoppedCount = (docker ps -a -q | Measure-Object).Count - $runningCount
    Write-Status "$runningCount running, $stoppedCount stopped total" "SUCCESS"
} else {
    Write-Status "Skipped (daemon not healthy)" "WARN"
}

# 7. Check disk usage
Write-Host "`n[7/10] Docker disk usage..." -ForegroundColor Cyan
if ($daemonHealthy) {
    $systemDf = docker system df
    Write-Host $systemDf | ForEach-Object {
        Write-Host "  $_" -ForegroundColor Gray
    }
} else {
    Write-Status "Skipped (daemon not healthy)" "WARN"
}

# 8. Check system resources (running containers only)
Write-Host "`n[8/10] System resources (current)..." -ForegroundColor Cyan
if ($daemonHealthy) {
    if ($runningCount -gt 0) {
        $stats = docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}\t{{.NetIO}}" 2>$null
        if ($stats) {
            Write-Status "Container resource usage:" "SUCCESS"
            $stats | ForEach-Object {
                Write-Host "  $_" -ForegroundColor Gray
            }
        }
    } else {
        Write-Status "No running containers" "INFO"
    }
} else {
    Write-Status "Skipped (daemon not healthy)" "WARN"
}

# 9. Check Docker Desktop settings
Write-Host "`n[9/10] Docker Desktop configuration..." -ForegroundColor Cyan
$settingsPath = "$env:APPDATA\Docker\settings.json"
if (Test-Path $settingsPath) {
    try {
        $settings = Get-Content $settingsPath | ConvertFrom-Json
        $memMB = $settings.memoryMiB
        $cpus = $settings.cpus
        $swapMB = $settings.memorySwapMiB
        
        Write-Status "Memory: $memMB MB | CPUs: $cpus | Swap: $swapMB MB" "INFO"
        
        # Check if adequate for AI workloads
        if ($memMB -lt 8192) {
            Write-Status "⚠️  Memory allocation is low for AI workloads (recommend 12GB+)" "WARN"
        }
        if ($cpus -lt 4) {
            Write-Status "⚠️  CPU allocation is low (recommend 4+ cores)" "WARN"
        }
    }
    catch {
        Write-Status "Could not read settings: $_" "WARN"
    }
} else {
    Write-Status "Settings file not found" "WARN"
}

# 10. Summary
Write-Host "`n[10/10] Summary..." -ForegroundColor Cyan
Write-Host "`n========== Status Summary ==========" -ForegroundColor Cyan

if ($daemonHanging) {
    Write-Host "⚠️  DAEMON WAS HANGING - Recovery attempted" -ForegroundColor Yellow
    if ($daemonHealthy) {
        Write-Host "✅ Daemon recovered and is now responsive" -ForegroundColor Green
    } else {
        Write-Host "❌ Daemon recovery failed - manual intervention needed" -ForegroundColor Red
    }
} else {
    Write-Host "✅ Docker daemon responsive (no hangs detected)" -ForegroundColor Green
}

if ($daemonHealthy) {
    Write-Host "✅ $runningCount container(s) running, $stoppedCount stopped" -ForegroundColor Green
    Write-Host "✅ Images and volumes accessible" -ForegroundColor Green
} else {
    Write-Host "❌ Daemon not healthy - some checks skipped" -ForegroundColor Red
}

Write-Host "`n========================================`n" -ForegroundColor Cyan

Write-Host @"
Quick commands:
- View running: docker ps
- View all: docker ps -a
- View images: docker images
- View logs: docker logs <container>
- View resources: docker stats
- Cleanup: .\\fix-docker-daemon.ps1
- Update: .\\update-docker-desktop.ps1
- Prune unused: docker system prune -a

For hung daemon recovery:
.\\check-docker-status.ps1 (auto-recovers with timeout detection)

For AI workload daemon issues, see:
D:\Dev\repos\mcp-central-docs\docker\DOCKER_DAEMON_AI_WORKLOADS.md

"@ -ForegroundColor Gray
