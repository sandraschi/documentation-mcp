@echo off
REM Docker Daemon Fix Script (Batch) - Run as Administrator
REM Comprehensive cleanup and optimization for unresponsive daemon (AI workloads)

setlocal enabledelayedexpansion

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must run as Administrator
    echo Right-click and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo ========== Docker Daemon Fix Script ==========
echo.

REM 1. Check Docker daemon status
echo --- Step 1: Docker Daemon Status ---
docker version >nul 2>&1
if %errorLevel% equ 0 (
    echo [SUCCESS] Docker daemon is responsive
) else (
    echo [ERROR] Docker daemon is unresponsive
    echo Please ensure Docker Desktop is running
    pause
    exit /b 1
)

REM 2. Show current disk usage
echo.
echo --- Step 2: Current Disk Usage ---
docker system df

REM 3. Stop all running containers
echo.
echo --- Step 3: Stopping All Containers ---
for /f "tokens=*" %%i in ('docker ps -q 2^>nul') do (
    echo Stopping container: %%i
    docker stop %%i >nul 2>&1
)
timeout /t 2 /nobreak

REM 4. Remove exited containers
echo.
echo --- Step 4: Removing Exited Containers ---
docker container prune -f

REM 5. Remove unused images
echo.
echo --- Step 5: Removing Unused Images ---
docker image prune -a -f

REM 6. Remove unused volumes
echo.
echo --- Step 6: Removing Unused Volumes ---
docker volume prune -f

REM 7. Prune build cache
echo.
echo --- Step 7: Clearing Build Cache ---
docker builder prune -a -f

REM 8. Full system prune
echo.
echo --- Step 8: Full System Prune ---
docker system prune -a -f --volumes

REM 9. Network prune
echo.
echo --- Step 9: Removing Unused Networks ---
docker network prune -f

REM 10. Configure daemon.json
echo.
echo --- Step 10: Configuring Docker Daemon Settings ---
set DAEMON_JSON=%APPDATA%\Docker\daemon.json

REM Create daemon.json with optimal settings for AI workloads
(
echo {
echo   "log-driver": "json-file",
echo   "log-opts": {
echo     "max-size": "100m",
echo     "max-file": "3"
echo   },
echo   "storage-driver": "overlay2",
echo   "storage-opts": [
echo     "overlay2.override_kernel_check=true"
echo   ],
echo   "debug": false
echo }
) > "%DAEMON_JSON%"

if %errorLevel% equ 0 (
    echo [SUCCESS] Updated daemon.json with log rotation and performance settings
) else (
    echo [WARNING] Could not update daemon.json
)

REM 11. Final status
echo.
echo --- Final Disk Usage ---
docker system df

echo.
echo [SUCCESS] Cleanup complete!

REM 12. Instructions
echo.
echo --- Next Steps ---
echo 1. Restart Docker Desktop for daemon settings to take effect:
echo    - Right-click Docker icon in system tray and select "Restart Docker Desktop"
echo.
echo 2. Increase Docker Desktop memory allocation (if needed):
echo    - Open Docker Desktop
echo    - Go to Settings ^> Resources
echo    - Set Memory to at least 12 GB (16 GB for larger models)
echo    - Set CPUs to at least 4 cores
echo    - Click "Apply & Restart"
echo.
echo 3. Monitor performance during AI workloads:
echo    - Open PowerShell and run: docker stats --no-stream
echo.
echo 4. Set resource limits on your AI containers in docker-compose.yml:
echo    Example:
echo      services:
echo        ai-service:
echo          deploy:
echo            resources:
echo              limits:
echo                memory: 12g
echo                cpus: '4'
echo.
echo 5. Run this script periodically (weekly) for maintenance
echo.
echo ========================================
echo.
pause
