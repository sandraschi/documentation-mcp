# Docker Desktop Zombie State: Diagnosis and Recovery

## 🔴 The Problem: "Locked" Docker
When using Docker Desktop on Windows (WSL2 Architecture), the system can enter a state where the GUI reports everything is running, but:
1.  **CLI hangs**: `docker ps` or `docker version` never return.
2.  **Connection Refused**: Your browser shows `ERR_CONNECTION_REFUSED` for mapped ports (e.g., 7333, 7777).
3.  **404 Errors**: Nginx might respond with 404 because the internal routing (`vpnkit`) has collapsed.

This is known as the **Zombie State**.

## 🧠 Root Causes
- **Named Pipe Deadlock**: The Windows Client and WSL2 Engine communicate via `//./pipe/docker_engine`. This pipe can hang during network churn (Tailscale, VPNs) or power state changes.
- **vpnkit Routing Failure**: The process responsible for host-to-container networking (`vpnkit.exe`) zombifies, refusing to forward packets while still appearing "Running" in Task Manager.
- **Disk I/O Latency**: Antivirus scanning the virtual disk file (`ext4.vhdx`) can freeze the daemon.

---

## ⚡ 1. The "Quick Fix" (Force Reset)
If standard "Restart Docker" from the tray fails, run this in an **Administrator PowerShell**:

```powershell
# Stop the main UI and backend
taskkill /F /IM "Docker Desktop.exe" /T

# Kill the networking bridge (Common culprit for ERR_CONNECTION_REFUSED)
taskkill /F /IM "vpnkit.exe" /T

# Kill the backend daemon process
taskkill /F /IM "com.docker.backend.exe" /T

# (Optional) Verify all pipes are cleared
# Then Re-open Docker Desktop
```

## 🛠 2. Long-Term Stability Hardening
For mission-critical apps (Security, MyAI, VLA), consider these adjustments:

### A. Disable Windows Fast Startup
Windows "Fast Startup" hibernates the kernel and system state, which frequently corrupts the WSL2/Docker clock and networking state upon wake.
- **Fix**: Settings -> System -> Power & Sleep -> Additional Power Settings -> Choose what power buttons do -> **Uncheck "Turn on fast startup"**.

### B. Antivirus Exclusions
Exclude the Docker substrate from real-time scanning to prevent I/O deadlocks:
- **Path**: `%LOCALAPPDATA%\Docker\wsl`
- **File**: `ext4.vhdx` (the virtual disk)

### C. Dedicated Linux Mini-PC (SOTA Setup)
For 24/7 availability (Home Security, Tapo Cameras), move the Docker stack off the Windows Workstation onto a dedicated Linux host (Ubuntu/Debian). This removes the Windows Named Pipe and WSL-VM translation layers entirely.

---

## 🔍 Verification Checklist
- [ ] `docker version` reports Client AND Server details.
- [ ] `netstat -ano | findstr :PORT` shows `LISTENING`.
- [ ] `docker compose ps` shows `Running (healthy)`.

**Last Updated**: 2026-01-01
**Context**: Result of VLA Stack Debugging Session
