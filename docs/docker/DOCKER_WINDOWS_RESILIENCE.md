---
title: "Docker on Windows: Resilience, Alternatives & Observability Consolidation"
category: architecture
status: active
audience: ops
skill_candidate: false
related:
  - docker/DOCKER_ZOMBIE_RECOVERY.md
  - docker/DOCKER_DAEMON_AI_WORKLOADS.md
  - docker/MONITORING_STACK.md
  - docker/docker-daemon-poll.ps1
  - standards/INFRASTRUCTURE_RELIABILITY.md
  - operations/WEBAPP_PORTS.md
last_updated: 2026-05-04
---

# Docker on Windows: Resilience, Alternatives & Observability Consolidation

**Scope**: Strategic analysis of Docker Desktop instability on Windows/WSL2, alternatives evaluation, fleet-wide observability consolidation, and daemon health polling.

**Complements**: [DOCKER_ZOMBIE_RECOVERY.md](DOCKER_ZOMBIE_RECOVERY.md) (tactical emergency procedures) and [DOCKER_DAEMON_AI_WORKLOADS.md](DOCKER_DAEMON_AI_WORKLOADS.md) (AI-specific resource limits).

---

## 1. Root Cause Analysis

### 1.1 Memory Starvation (Primary Failure Mode)

When WSL2 is under memory pressure:

1. The `vsock` bridge between Windows and the WSL2 VM degrades
2. Docker CLI → daemon communication times out
3. `wsl --terminate docker-desktop` hangs (VM thrashing swap)
4. Docker Desktop GUI reports "Docker Engine Stopped" but the WSL VM is stuck

**Diagnosis commands:**

```powershell
# Current WSL2 memory cap
Get-Content "$env:USERPROFILE\.wslconfig"

# Docker daemon viewable memory
docker info 2>$null | Select-String "Total Memory"

# Actual WSL memory usage per distro
wsl --list --verbose

# Containers killed by OOM (exit code 137 = SIGKILL)
docker ps -a --format "{{.Names}}: {{.Status}}" | Select-String "Exited \(137\)"

# Per-container memory
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}"
```

**Exit codes that indicate memory pressure:**
- `137` — SIGKILL (Linux OOM killer)
- `255` — Resource exhaustion / generic Docker error
- `1` — Application crashed (often secondary to OOM)

### 1.2 WSL Configuration

**Recommended `~/.wslconfig`:**

```ini
[wsl2]
memory=16GB          # Minimum for 30+ container fleets
swap=8GB             # Prevents immediate OOM kill
processors=12        # Cap at half of physical cores
localhostForwarding=true
kernelCommandLine=sysctl.vm.max_map_count=262144  # Required by Loki, ES, Weaviate

[experimental]
autoMemoryReclaim=gradual   # Return freed pages to Windows host
sparseVhd=true              # Prevent vhdx ballooning
```

**To apply changes**: `wsl --shutdown` (terminates all WSL distros and containers — plan a maintenance window).

---

## 2. Docker Desktop Alternatives

### 2.1 Rancher Desktop (Recommended)

| Aspect | Docker Desktop | Rancher Desktop |
|--------|---------------|-----------------|
| License | Proprietary (free tier restricted) | Apache 2.0 |
| Container engine | dockerd only | dockerd **or** containerd |
| Kubernetes | Not included | Built-in (k3s) |
| WSL2 integration | Proprietary bridge | Direct WSL2 distro |
| Resource overhead | ~2 GB idle (Electron + services) | ~800 MB idle (Vue UI) |
| GPU passthrough | Proprietary | Standard WSL2 |
| CLI compatibility | Full `docker` CLI | Identical (`dockerd` runtime) |
| Compose compatibility | Full | Full |

**Migration path:**

1. Export compose configs: `docker compose config > backup.yml` (per project)
2. Stop all containers: `docker compose down` (per project)
3. Uninstall Docker Desktop
4. Install Rancher Desktop: `winget install RancherDesktop.RancherDesktop`
5. Select **dockerd (moby)** runtime on first launch
6. Verify: `docker info`, `docker compose up` in a test project
7. No code changes required — identical `docker` and `docker compose` CLI

**What you lose vs Docker Desktop:**
- Docker Scout, Docker Build Cloud, Gordon AI (none used in this fleet)
- Docker Desktop GUI dashboard (Rancher has a lighter alternative)

### 2.2 Native Docker Engine in WSL2 Ubuntu

Install Docker CE directly in your existing WSL2 Ubuntu distro:

```bash
# Inside WSL2 Ubuntu:
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo service docker start
```

Expose to Windows via `~/.docker/config.json`:

```json
{
  "currentContext": "wsl-native"
}
```

```powershell
# Then create the context:
docker context create wsl-native --docker "host=unix:///var/run/docker.sock"
docker context use wsl-native
```

**Pros:** Zero GUI overhead, full control, no license restrictions
**Cons:** No GUI dashboard, manual lifecycle management, no built-in Kubernetes

### 2.3 Podman Desktop

| Aspect | Docker Desktop | Podman Desktop |
|--------|---------------|----------------|
| License | Proprietary | Apache 2.0 |
| Daemon | Required (dockerd) | Daemonless (fork/exec) |
| Rootless | Partial | Full support |
| Compatibility | Native Docker API | Docker-compatible via `podman-docker` |
| Pods | Not native | Native Kubernetes pods |

**Cons:** Some Docker Compose features not fully supported, image compatibility edge cases. Not recommended for fleet migrations where compose is the primary orchestration tool.

### 2.4 Decision Matrix

| Criterion | Docker Desktop | Rancher Desktop | Native WSL2 | Podman Desktop |
|-----------|:---:|:---:|:---:|:---:|
| Zero config migration | ✓ | ✓ | ✗ | ✗ |
| Compose compatibility | ✓ | ✓ | ✓ | Partial |
| Memory baseline | 2 GB | 800 MB | 300 MB | 600 MB |
| GUI dashboard | ✓ | ✓ | ✗ | ✓ |
| Kubernetes | ✗ | ✓ | ✗ | ✓ |
| License risk | Medium | None | None | None |
| Fleet-ready (>30 containers) | Strained | ✓ | ✓ | Untested |

**Recommendation**: Rancher Desktop (dockerd runtime) for the transition. Evaluate native WSL2 Docker if you're comfortable without a GUI.

---

## 3. Observability Consolidation

### 3.1 The Problem: N×M Redundancy

A typical multi-project fleet ends up with one Loki + Prometheus + Grafana stack **per project**. At 4+ projects, this means:

| Resource | Per Stack | ×4 Stacks | Total Waste |
|----------|-----------|-----------|-------------|
| Loki | 0.8-1.5 GB | 3.2-6.0 GB | **3 replicas redundant** |
| Prometheus | 0.5-1.0 GB | 2.0-4.0 GB | **3 replicas redundant** |
| Grafana | 0.3-0.6 GB | 1.2-2.4 GB | **3 replicas redundant** |
| Promtail | 0.1-0.2 GB | 0.4-0.8 GB | **3 replicas redundant** |
| **Total per project** | 1.7-3.3 GB | 6.8-13.2 GB | **5.1-9.9 GB wasted** |

### 3.2 Centralized Architecture

```
┌──────────────────────────────────────────────────────────┐
│                 Central Observability Stack                │
│  Grafana :3100 | Prometheus :9090 | Loki :3101            │
│  (monitoring-mcp, ports 10850-10851)                      │
└────┬──────────────┬──────────────┬───────────────────────┘
     │logs          │metrics       │logs
     ▼              ▼              ▼
┌─────────┐   ┌──────────┐   ┌──────────┐
│Project A│   │ Project B│   │ Project C│
│promtail │   │ /metrics │   │ promtail │
│(scrape) │   │ endpoint │   │(scrape)  │
└─────────┘   └──────────┘   └──────────┘
```

**Per-project changes:**

```yaml
# Remove from each project's docker-compose.yml:
# - grafana, loki, prometheus, promtail services

# Add only Promtail (lightweight, ~100MB):
services:
  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
```

**Central stack receives from all projects:**

```yaml
# monitoring-mcp/docker-compose.yml
services:
  loki:
    image: grafana/loki:latest
    ports: ["3101:3100"]
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
    command: -config.file=/etc/loki/local-config.yaml

  prometheus:
    image: prom/prometheus:latest
    ports: ["9090:9090"]
    deploy:
      resources:
        limits:
          memory: 1G

  grafana:
    image: grafana/grafana:latest
    ports: ["10851:3000"]
    environment:
      - GF_SERVER_HTTP_PORT=3000
    deploy:
      resources:
        limits:
          memory: 512M
```

**Savings**: 5-10 GB RAM, 8-12 fewer containers, single pane of glass for all projects.

---

## 4. Daemon Health Polling

### 4.1 Automated Health Check Script

Located at [`docker-daemon-poll.ps1`](docker-daemon-poll.ps1).

```powershell
# One-shot health check
.\docker-daemon-poll.ps1

# Continuous monitoring with toast notifications
.\docker-daemon-poll.ps1 -Watch -Interval 30 -Notify

# Monitor specific critical containers
.\docker-daemon-poll.ps1 -CriticalContainers "weaviate,traefik,immich_server"
```

**Recovery tiers:**

| Tier | Action | When |
|------|--------|------|
| 1 — Gentle | Launch Docker Desktop if not running | Process missing |
| 2 — Medium | `wsl --terminate docker-desktop` + wait | WSL running, daemon unresponsive |
| 3 — Hard | Kill all Docker processes + full relaunch | Tier 1+2 failed |

### 4.2 Register as Scheduled Task

```powershell
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument '-ExecutionPolicy Bypass -File "D:\Dev\repos\mcp-central-docs\docker\docker-daemon-poll.ps1" -Notify'

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)

Register-ScheduledTask `
    -TaskName "Docker Daemon Poll" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest `
    -Description "Health-checks Docker daemon and attempts auto-recovery"
```

---

## 5. Quick-Reference: Recovery Cheat Sheet

```powershell
# Level 1: Gentle — restart Docker Desktop
& "${env:ProgramFiles}\Docker\Docker\Docker Desktop.exe"

# Level 2: WSL restart (preserves data)
wsl --terminate docker-desktop
wsl --terminate docker-desktop-data

# Level 3: Full "triple kill"
Get-Process "Docker Desktop", "com.docker.backend", "com.docker.build" | Stop-Process -Force
wsl --shutdown
# Wait 10s, relaunch Docker Desktop

# Level 4: Nuclear (rarely needed — clears all Docker data)
wsl --unregister docker-desktop
wsl --unregister docker-desktop-data
# Reinstall Docker Desktop
```

---

## 6. Per-Container Memory Limits

### Compose

```yaml
services:
  loki:
    image: grafana/loki:latest
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M

  postgres:
    image: postgres:14-alpine
    deploy:
      resources:
        limits:
          memory: 512M
    command: postgres -c shared_buffers=128MB -c effective_cache_size=384MB
```

### CLI

```powershell
docker run --memory=512m --memory-swap=1g my-image
docker update --memory=512m --memory-swap=1g container-name  # live update
```

---

## 7. Disk Maintenance

```powershell
# Weekly cleanup (can be scheduled):
docker builder prune -a -f      # Build cache
docker image prune -a -f        # Unused images
docker volume prune -f          # Dangling volumes (with caution)
docker system df                # Check current usage
```

## 9. VHDX Compaction Protocol (When Ballooned)

If the vhdx has already ballooned (101+ GB on a 25 GB filesystem), compaction requires a three-step sequence:

### 9.1 Prune and Trim

```powershell
docker system prune -a --volumes -f
docker builder prune -a -f
```

### 9.2 fstrim Inside WSL2

```powershell
wsl -d docker-desktop -e sh -c "fstrim -v /mnt/docker-desktop-disk"
```
This tells ext4 to release blocks to the vhdx. Typical output: `964 GiB trimmed` on a 1006 GB disk.

### 9.3 Optimize-VHD (Admin Required)

```powershell
# Shutdown WSL first
Get-Process "Docker Desktop","com.docker.backend" -ErrorAction SilentlyContinue | Stop-Process -Force
wsl --shutdown
Start-Sleep 10

# Compact (run in elevated PowerShell)
Optimize-VHD -Path "$env:LOCALAPPDATA\Docker\wsl\disk\docker_data.vhdx" -Mode Full
```

**Expected result**: VHDX shrinks from ~102 GB to ~50 GB. The remaining overhead (~24 GB) is ext4 metadata (journal, inodes, reserved blocks) — not reclaimable.

### 9.4 Prevention — Scheduled Tasks

Two scripts deployed to `%USERPROFILE%\scripts\`:

| Script | Frequency | What It Does | Run Level |
|--------|-----------|-------------|-----------|
| `docker-weekly.ps1` | Sunday 2 AM | `docker system prune -a -f` + `fstrim` | Limited |
| `compact-docker-vhdx.ps1` | 1st of month 3 AM | Full prune + fstrim + `Optimize-VHD -Mode Full` | Highest (admin) |

Register via:
```batch
schtasks /CREATE /SC WEEKLY /D SUN /TN "Docker\WeeklyMaintenance" /TR "'C:\Program Files\PowerShell\7\pwsh.EXE' -NoProfile -File '%USERPROFILE%\scripts\docker-weekly.ps1'" /ST 02:00 /F /RL LIMITED
schtasks /CREATE /SC MONTHLY /D 1 /TN "Docker\MonthlyCompaction" /TR "'C:\Program Files\PowerShell\7\pwsh.EXE' -NoProfile -File '%USERPROFILE%\scripts\compact-docker-vhdx.ps1'" /ST 03:00 /F /RL HIGHEST
```

### 9.5 Docker Daemon Config (Build Cache Cap)

`%USERPROFILE%\.docker\daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "storage-driver": "overlay2",
  "max-concurrent-downloads": 3,
  "max-concurrent-uploads": 3
}
```

Note: `builder.gc` (`defaultKeepStorage`) caused Docker Desktop 29.4.1 to crash on Windows with `io: read/write on closed pipe`. Omit it on this version.

### 9.6 Empirical Results (Goliath, 2026-05-06)

| Metric | Before | After |
|--------|--------|-------|
| docker_data.vhdx | 101.90 GB | 50.14 GB |
| Actual data inside | 25.5 GB | 25.5 GB |
| Overhead (ext4) | 76.4 GB | 24.6 GB |
| pruned build/container debris | — | 9.9 GB |
| VHDX compacted | — | 51.78 GB freed |
| `fstrim` | — | 964 GB blocks released |

---

## Related Documentation

- **[DOCKER_ZOMBIE_RECOVERY.md](DOCKER_ZOMBIE_RECOVERY.md)** — Tactical emergency commands when Docker locks up
- **[DOCKER_DAEMON_AI_WORKLOADS.md](DOCKER_DAEMON_AI_WORKLOADS.md)** — AI-specific resource limits and GPU passthrough
- **[MONITORING_STACK.md](MONITORING_STACK.md)** — Single-project Grafana + Prometheus + Loki setup
- **[WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)** — Port allocation for observability stack
