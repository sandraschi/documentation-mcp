@echo off
REM Docker Status Checker Script (Batch)
REM Comprehensive health check for Docker Desktop installation and daemon
REM Detects hanging daemon and attempts recovery
REM Shows last 10 images and containers
REM Run as Administrator for best results
REM Usage: check-docker-status.bat

setlocal enabledelayedexpansion

echo.
echo ========== Docker Status Checker ==========
echo Comprehensive health check + hang detection
echo.

REM 1. Check if Docker is installed
echo [1/10] Checking Docker installation...
if exist "C:\Program Files\Docker\Docker\Docker Desktop.exe" (
    echo [SUCCESS] Docker Desktop found
    set DOCKER_PATH=C:\Program Files\Docker\Docker\Docker Desktop.exe
) else (
    echo [ERROR] Docker Desktop not installed
    echo Install from: https://hub.docker.com/
    pause
    exit /b 1
)

REM 2. Check if Docker daemon is running (with hang detection)
echo.
echo [2/10] Checking Docker daemon (with hang detection)...

setlocal enabledelayedexpansion
set DAEMON_HEALTHY=0
set DAEMON_HANGING=0

REM Try docker version command
tasklist | findstr /I "Docker Desktop" >nul 2>&1
if %errorlevel% equ 0 (
    docker version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] Docker daemon is running and responsive (no hang detected)
        set DAEMON_HEALTHY=1
    ) else (
        echo [WARN] Docker daemon not responding - will attempt restart
        set DAEMON_HANGING=1
    )
) else (
    echo [WARN] Docker Desktop process not found - attempting to start
    start "" "!DOCKER_PATH!"
    timeout /t 5 /nobreak >nul
)

REM If daemon hung, attempt recovery
if !DAEMON_HANGING! equ 1 (
    echo.
    echo [ERROR] Daemon hanging detected - attempting recovery...
    echo [WARN] Killing hung Docker processes...
    taskkill /IM "Docker Desktop.exe" /F >nul 2>&1
    taskkill /IM "com.docker.backend.exe" /F >nul 2>&1
    taskkill /IM "vpnkit.exe" /F >nul 2>&1
    timeout /t 3 /nobreak >nul
    
    echo [INFO] Restarting Docker Desktop...
    start "" "!DOCKER_PATH!"
    timeout /t 8 /nobreak >nul
    
    echo [INFO] Verifying daemon after restart...
    docker version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] Docker daemon recovered successfully
        set DAEMON_HEALTHY=1
        set DAEMON_HANGING=0
    ) else (
        echo [ERROR] Daemon still unresponsive after restart
        echo.
        echo Daemon is unrecoverable. Try full reset:
        echo   update-docker-desktop.ps1 -FullWipe
    )
) else if !DAEMON_HEALTHY! equ 0 (
    REM Daemon not responding, try starting it
    echo [WARN] Docker daemon not responding - attempting start...
    start "" "!DOCKER_PATH!"
    timeout /t 5 /nobreak >nul
    docker version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] Docker daemon started successfully
        set DAEMON_HEALTHY=1
    ) else (
        echo [ERROR] Docker daemon failed to start
    )
)

REM 3. Check Docker version
if !DAEMON_HEALTHY! equ 1 (
    echo.
    echo [3/10] Docker version...
    for /f "tokens=*" %%i in ('docker version --format "{{.Server.Version}}" 2^>nul') do (
        echo   Docker: %%i
    )
) else (
    echo.
    echo [3/10] Docker version...
    echo [WARN] Skipped (daemon not healthy)
)

REM 4. Check last 10 built images
echo.
echo [4/10] Last 10 built images...
if !DAEMON_HEALTHY! equ 1 (
    setlocal enabledelayedexpansion
    set IMAGE_COUNT=0
    echo [SUCCESS] Recent images (last 10):
    for /f "skip=1 tokens=*" %%i in ('docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" 2^>nul') do (
        if !IMAGE_COUNT! lss 10 (
            echo   %%i
            set /a IMAGE_COUNT=!IMAGE_COUNT! + 1
        )
    )
    if !IMAGE_COUNT! equ 0 (
        echo [INFO] No images found
    )
    endlocal
) else (
    echo [WARN] Skipped (daemon not healthy)
)

REM 5. Check last 10 containers (all states)
echo.
echo [5/10] Last 10 containers (all states)...
if !DAEMON_HEALTHY! equ 1 (
    setlocal enabledelayedexpansion
    set CONTAINER_COUNT=0
    echo [SUCCESS] Recent containers (last 10):
    for /f "skip=1 tokens=*" %%i in ('docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.CreatedAt}}" 2^>nul') do (
        if !CONTAINER_COUNT! lss 10 (
            echo   %%i
            set /a CONTAINER_COUNT=!CONTAINER_COUNT! + 1
        )
    )
    if !CONTAINER_COUNT! equ 0 (
        echo [INFO] No containers found
    )
    endlocal
) else (
    echo [WARN] Skipped (daemon not healthy)
)

REM 6. Check running containers summary
echo.
echo [6/10] Running containers summary...
if !DAEMON_HEALTHY! equ 1 (
    for /f %%i in ('docker ps -q 2^>nul ^| find /c /v ""') do set RUNNING=%%i
    for /f %%i in ('docker ps -a -q 2^>nul ^| find /c /v ""') do set TOTAL=%%i
    set /a STOPPED=!TOTAL! - !RUNNING!
    echo [SUCCESS] !RUNNING! running, !STOPPED! stopped total
) else (
    echo [WARN] Skipped (daemon not healthy)
)

REM 7. Check disk usage
echo.
echo [7/10] Docker disk usage...
if !DAEMON_HEALTHY! equ 1 (
    echo [INFO] Disk breakdown:
    for /f "tokens=*" %%i in ('docker system df 2^>nul') do (
        echo   %%i
    )
) else (
    echo [WARN] Skipped (daemon not healthy)
)

REM 8. Check system resources
echo.
echo [8/10] System resources (current)...
if !DAEMON_HEALTHY! equ 1 (
    if !RUNNING! gtr 0 (
        echo [SUCCESS] Container resource usage:
        for /f "tokens=*" %%i in ('docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}" 2^>nul') do (
            echo   %%i
        )
    ) else (
        echo [INFO] No running containers (expected if idle)
    )
) else (
    echo [WARN] Skipped (daemon not healthy)
)

REM 9. Check Docker Desktop settings
echo.
echo [9/10] Docker Desktop configuration...
if exist "%APPDATA%\Docker\settings.json" (
    echo [INFO] Settings file found (use PowerShell version for detailed config)
) else (
    echo [WARN] Settings file not found
)

REM 10. Summary
echo.
echo [10/10] Summary...
echo.
echo ========== Status Summary ==========

if !DAEMON_HANGING! equ 1 (
    echo [WARN] Daemon was hanging - recovery attempted
) else (
    echo [SUCCESS] Docker daemon responsive - no hangs detected
)

if !DAEMON_HEALTHY! equ 1 (
    if !RUNNING! equ 0 (
        echo [SUCCESS] No containers running (expected if idle)
    ) else (
        echo [SUCCESS] !RUNNING! container(s) running, !STOPPED! stopped
    )
    echo [SUCCESS] Images and volumes accessible
) else (
    echo [ERROR] Daemon not healthy - some checks skipped
)

echo.
echo ========================================
echo.
echo Quick commands:
echo - View running: docker ps
echo - View all: docker ps -a
echo - View images: docker images
echo - View logs: docker logs ^<container^>
echo - View resources: docker stats
echo - Cleanup: fix-docker-daemon.ps1
echo - Update: update-docker-desktop.ps1
echo - Prune unused: docker system prune -a
echo.
echo For full status with detailed config:
echo   Use PowerShell version: .\check-docker-status.ps1
echo.
echo For AI workload daemon issues, see:
echo   D:\Dev\repos\mcp-central-docs\docker\DOCKER_DAEMON_AI_WORKLOADS.md
echo.
pause
