@echo off
REM Docker Desktop Update & Recovery Script
REM Run as Administrator to fix update elevation errors
REM Usage: Right-click and select "Run as Administrator"

setlocal enabledelayedexpansion

REM Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must run as Administrator
    echo Right-click cmd.exe or PowerShell and select "Run as Administrator"
    pause
    exit /b 1
)

echo.
echo ========== Docker Desktop Update & Recovery ==========
echo.

REM 1. Stop Docker Desktop
echo [1/5] Stopping Docker Desktop...
taskkill /IM "Docker Desktop.exe" /F >nul 2>&1
taskkill /IM "com.docker.backend.exe" /F >nul 2>&1
taskkill /IM "vpnkit.exe" /F >nul 2>&1
timeout /t 2 /nobreak >nul

REM 2. Clear update temp folder
echo [2/5] Clearing Docker update temp folder...
if exist "%LOCALAPPDATA%\Temp\DockerDesktopUpdates" (
    rmdir /S /Q "%LOCALAPPDATA%\Temp\DockerDesktopUpdates"
    echo Removed: %LOCALAPPDATA%\Temp\DockerDesktopUpdates
) else (
    echo Already clean
)

REM 3. Clear Docker app data cache (optional - uncomment for full wipe)
REM echo [3/5] Clearing Docker app data...
REM if exist "%APPDATA%\Docker" (
REM     rmdir /S /Q "%APPDATA%\Docker"
REM )

REM 4. Restart Docker Desktop
echo [3/5] Restarting Docker Desktop...
echo Please wait while Docker reinitializes...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
timeout /t 5 /nobreak >nul

REM 5. Check status
echo.
echo [4/5] Checking Docker daemon status...
for /L %%A in (1,1,10) do (
    docker version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [SUCCESS] Docker daemon is responsive
        goto :success
    )
    echo Attempt %%A/10 - waiting for daemon...
    timeout /t 3 /nobreak >nul
)

echo [WARN] Docker daemon not responding yet - may still be starting
echo Check Docker Desktop icon in system tray

:success
echo.
echo [5/5] Update & recovery complete!
echo.
echo Next steps:
echo 1. Wait 30 seconds for Docker Desktop to fully start
echo 2. Open Docker Desktop Settings
echo 3. Go to Settings ^> Check for Updates
echo 4. Install any available updates
echo.
echo If update still fails:
echo - Restart Windows
echo - Download fresh installer from https://hub.docker.com/
echo.
echo ========================================
echo.
pause
