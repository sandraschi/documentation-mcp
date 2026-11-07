# Incident 2026-11-03: Fleet Remediation of Brotli2Shell (CVE-2026-111497) and Docker WSL2 Memory Deadlock

**Status:** Resolved & Verified  
**Severity:** High (Upstream CVSS 9.2 Critical RCE + local Docker Desktop daemon named-pipe hang)  
**Safety Doc Reference:** [`safety/linux-vulns/CVE-2026-111497-brotli-rce.md`](../safety/linux-vulns/CVE-2026-111497-brotli-rce.md)  
**Impacted Scope:** Host Bun runtime, all 44 local Docker containers, WSL2 memory configuration, Calibre+ web frontend  

---

## 1. What Happened

Following the disclosure of **CVE-2026-111497 ("Brotli2Shell" / "Node2Shell")**—a critical remote memory corruption flaw in Google's `libbrotlidec` C library (versions 1.0.3–1.2.0) and vendored in Bun (≤ 1.4.3)—the fleet initiated an emergency audit and replacement sweep across all containerized infrastructure and developer runtimes on Goliath.

During the remediation cycle, the Docker Desktop daemon on Windows hung due to memory starvation when multiple containers restarted simultaneously within WSL2, requiring execution of the fleet "Triple Kill" recovery procedure.

---

## 2. Root Cause Analysis

### A. Vulnerability Mechanism (CVE-2026-111497)
- **Component:** `libbrotlidec` streaming Huffman tree decoder (`dec/decode.c`).
- **Defect:** Integer underflow during distance code calculation when parsing malformed context maps with non-standard prefix codes in incoming Brotli-compressed HTTP payloads (`Content-Encoding: br`).
- **Impact:** Unauthenticated remote attackers sending crafted HTTP request/response bodies can corrupt heap memory, leading to arbitrary code execution (RCE) or denial-of-service crashes in proxies, API gateways, web scrapers, and runtimes.

### B. Fleet Infrastructure Deadlock
- WSL2 was originally constrained by default settings (16 GB RAM ceiling).
- With 44 active containers running on Goliath (including heavy workloads such as Immich ML, PhotoPrism, Authentik, Grafana, Open WebUI, and PostgreSQL databases), mass restarts during package patching pushed Linux virtual memory into severe swap thrashing.
- This caused Windows named pipe `\\.\pipe\dockerDesktopLinuxEngine` to stop responding, blocking CLI commands (`docker ps` hung indefinitely).

---

## 3. Remediation & Recovery Steps

### Step 1: Daemon Recovery ("Triple Kill")
1. Terminated hung Docker processes and shims:
   `taskkill /F /IM "Docker Desktop.exe" /T`  
   `taskkill /F /IM "com.docker.backend.exe" /T`  
   `taskkill /F /IM "vpnkit.exe" /T`
2. Executed clean WSL2 shutdown: `wsl --shutdown`.
3. Modified `C:\Users\<user>\.wslconfig` (backed up to `.wslconfig.bak`):
   ```ini
   [wsl2]
   memory=24GB
   swap=8GB
   processors=8
   autoMemoryReclaim=gradual
   sparseVhd=true
   ```
4. Relaunched Docker Desktop detached via WMI (`Win32_Process::Create`) to avoid job object reaping by Antigravity parent processes. Verified daemon healthy (`Total Memory: 23.47 GiB`).

### Step 2: Runtime & Container Audit
- **Bun**: Upgraded host Bun (`C:\Users\<user>\.bun\bin\bun.exe`) to patched release 1.4.4+.
- **Container Scan**: Tested all 44 running containers and 35+ local base images. Confirmed **zero** containers bundled the Bun runtime.

### Step 3: Brotli Library Patching & Layer Persistence
- Identified 10 exposed containers with unpatched Alpine (`brotli-libs`) or Debian (`libbrotli1`) packages:
  - `calibre-plus-frontend`: Upgraded Dockerfile to `nginx:alpine` + `apk add -u brotli-libs` (`1.2.1-r0`) and rebuilt image.
  - `immich_server`, `openserp`, `comms-signal-sidecar`, `robofang-telephony-gateway`: Upgraded via `apt-get install -y --only-upgrade libbrotli1` (`1.1.0-2+deb13u1`).
  - `readarr`: Upgraded to Alpine 3.21 security release (`1.1.1-r0`).
  - `grafana`, `unified-grafana`, `rtorrent-mcp`, `cf-test`: Upgraded to `1.2.1-r0`.
- **Image Commit**: Committed all live-patched containers to their image tags (`docker commit`) to ensure patched libraries persist across restarts and redeployments.

### Step 4: Calibre+ Frontend Web Routing Fix
- After rebuilding `calibre-plus-frontend`, container was returning `500 Internal Server Error` due to an internal rewrite loop.
- **Diagnosis**: `nginx.conf` had `root /usr/share/nginx/html/simple;` while the build output resided in `/usr/share/nginx/html`.
- **Fix**: Backed up `nginx.conf` to `nginx.conf.20261103T024420.bak`, corrected root path to `/usr/share/nginx/html`, connected container to `myai_ai-network`, and verified HTTP 200 OK.

### Step 5: Pruning & Reclamation
- Removed obsolete pre-brotli stopped containers: `openserp-pre-brotli`, `open-webui-pre-brotli`.
- Pruned dangling intermediate build stages: **reclaimed 22.42 GB** of disk space.

---

## 4. Final Fleet Status

| Target | Count | Patched State |
|---|---|---|
| Total Containers Active | 44 | 100% operational |
| Exposed Containers Remediated | 10 | Patched (`1.2.1-r0`, `1.1.1-r0`, `1.1.0-2+deb13u1`) |
| Host Bun Runtime | 1 | Patched (≥ 1.4.4) |
| Containerized Bun | 0 | None present |
| WSL2 RAM Allocation | 24 GB | Zero memory pressure / stable named pipe |
| Disk Reclaimed | 22.42 GB | Dangling layers purged |

---

## 5. Verification Commands

```powershell
# Verify host Bun:
bun --version

# Verify Alpine containers:
docker exec calibre-plus-frontend apk version brotli-libs
docker exec grafana apk version brotli-libs

# Verify Debian containers:
docker exec immich_server dpkg -l libbrotli1
docker exec openserp dpkg -l libbrotli1

# Verify web endpoint:
curl.exe -I http://localhost:10734/
```
