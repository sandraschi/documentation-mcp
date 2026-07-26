# Docker Documentation

**Last Updated:** 2026-01-15
**Status:** Consolidated + Hot-Reload Patterns + AI Workload Optimization

---

## Overview

Docker guides for MCP servers, fullstack apps, monitoring stacks, and AI inference workloads.

---

## Documentation

### Development Workflow (START HERE!)

**[DOCKER_DEV_GUIDE.md](DOCKER_DEV_GUIDE.md)**
**Stop wasting 8+ hours per project on Docker rebuilds!**

**Contents:**
- Hot-reload development (1 second iterations)
- The --no-cache trap (never use for code changes!)
- Volume mount best practices
- BuildKit cache optimization
- Time savings analysis (8-25 hours per project)
- Real-world examples
- Troubleshooting

**Key Takeaway**: Use volume mounts + `--reload` flag = instant code updates without rebuilds!

---

### AI Workload Optimization (NEW - Jan 15, 2026)

**[DOCKER_DAEMON_AI_WORKLOADS.md](DOCKER_DAEMON_AI_WORKLOADS.md)** NEW
**Fix unresponsive Docker daemon during LLM inference and heavy AI workloads.**

**Problem**: Docker daemon hangs, containers randomly exit (code 137 OOM), entire system sluggish

**Contents:**
- Diagnosis: Quick tests to identify resource exhaustion
- Resource limits in docker-compose.yml
- Disk cleanup (dangling images, old logs)
- Docker Desktop VM configuration (12GB+ memory)
- Log rotation setup (prevents 50GB log files)
- Automated fix script (fix-docker-daemon.ps1)
- Real-world multi-model configuration
- Monitoring during development
- Weekly maintenance automation
- Production recommendations

**Key Takeaway**: Set resource limits + increase Docker Desktop memory to 12GB+ + run weekly cleanup = daemon always responsive!

**Also includes**: Pre-built PowerShell script (`fix-docker-daemon.ps1`) that automates all fixes and can be scheduled weekly.

---

### Infrastructure & Reliability

**[DOCKER_ZOMBIE_RECOVERY.md](DOCKER_ZOMBIE_RECOVERY.md)**
**Emergency procedures for when Docker "locks up" or zombifies on Windows.**

**Contents:**
- Force-kill commands for orphaned pipes
- Diagnosis of vpnkit routing failures
- Stability hardening (Fast Startup, AV exclusions)
- SOTA high-availability recommendations

**Key Takeaway**: Use `taskkill /F /IM "Docker Desktop.exe" /T` if standard restarts fail.

---

### Build & Optimization

**[BUILD_OPTIMIZATION.md](BUILD_OPTIMIZATION.md)**
Smart Docker caching strategies for when rebuilds are necessary.

**Contents:**
- Layer caching best practices
- Dockerfile structure optimization
- Build scripts (PowerShell)
- Performance comparisons (18-90x faster)
- .dockerignore patterns

**Note:** This guide focuses on optimizing builds. For **avoiding rebuilds** (better approach), see DOCKER_DEV_GUIDE.md above.

**Key Takeaway**: Order Dockerfile layers from least to most frequently changing.

---

### Monitoring Stack

**[MONITORING_STACK.md](MONITORING_STACK.md)**
Dockerized monitoring with Grafana, Prometheus, Loki, Promtail.

**Contents:**
- Complete monitoring stack setup
- Service configuration
- Health checks
- Port allocation
- Troubleshooting

---

## Docker Desktop Update & Recovery

### Check Docker Status

**Quick health check (shows daemon, images, containers, disk, resources, config):**
```powershell
.\check-docker-status.ps1
```

Reports:
- ✓ Daemon running/responsive
- ✓ Images count
- ✓ Running/stopped containers list
- ✓ Disk usage breakdown
- ✓ Resource stats (memory, CPU)
- ✓ Docker Desktop config (memory/CPU allocation)
- ⚠️ Warnings if memory <12GB or CPUs <4 (AI workload minimum)

---

### Update Elevation Error

**Error:** `fork/exec ... Docker Desktop Installer: The requested operation requires elevation`

Run elevated (as Administrator):

**PowerShell:**
```powershell
# Use -FullWipe for aggressive reset (clears all Docker data)
.\update-docker-desktop.ps1

# Or full wipe mode:
.\update-docker-desktop.ps1 -FullWipe
```

**Batch (legacy):**
```cmd
update-docker-desktop.bat
```

Both scripts:
- Stop Docker daemon gracefully
- Clear update temp folder (fixes elevation error)
- Restart Docker Desktop
- Verify daemon is responsive
- Prompt to retry update in Settings

**Optional:** Use `-FullWipe` flag (PowerShell) to also clear Docker app data for complete reset.

---

## Quick Reference

### When Docker Daemon is Unresponsive (AI Workloads)

**Immediate action:**
```powershell
# 1. Check resource usage
docker stats --no-stream

# 2. Check disk bloat
docker system df

# 3. Run automated fix (as Administrator)
.\fix-docker-daemon.ps1

# 4. Increase Docker Desktop memory
# Settings > Resources > Memory: 12 GB or more
```

**Why this happens:**
- LLM containers consume 8-128GB RAM
- Without limits, they starve the daemon
- Old logs and dangling images consume disk
- Docker Desktop VM memory too low (default 2-4GB)

**Prevention:**
- Set resource limits in docker-compose.yml
- Configure log rotation in daemon.json
- Run weekly cleanup (automated script provided)

---

### Standard Build Pattern

```powershell
# Fast incremental build (code changes only)
docker compose build

# Full rebuild (dependency changes)
docker compose build --no-cache

# Rebuild and start
docker compose down
docker compose build
docker compose up -d
```

### When to Use `--no-cache` (RARELY!)

**Use `--no-cache` when (1% of time):**
- Dependencies changed AND regular build failed mysteriously
- Final production build before deployment
- Suspected cache corruption (very rare)

**DON'T use `--no-cache` for (99% of time):**
- Regular code changes (CSS, JS, Python) - Use hot-reload instead!
- Quick iterations during development - Use hot-reload!
- "Just to be safe" - Wastes 15 minutes downloading entire internet!

**Real cost:** Regular build = 30 sec | --no-cache = 15 min | You waste 14.5 minutes!

---

## Dockerfile Best Practices

### Python Projects with Resource Limits (AI Models)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1. System deps (rarely change)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy requirements (changes less frequently)
COPY requirements.txt .

# 3. Install packages (cached until requirements change)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy code last (changes most frequently)
COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
```

**docker-compose.yml with resource limits:**
```yaml
services:
  ai-model:
    build: .
    deploy:
      resources:
        limits:
          memory: 24g      # Kill if exceeds
          cpus: '8'
        reservations:
          memory: 16g      # Minimum guaranteed
          cpus: '6'
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "3"
```

### Node.js Projects

```dockerfile
FROM node:20-alpine

WORKDIR /app

# 1. Copy package files
COPY package*.json ./

# 2. Install dependencies (cached until package.json changes)
RUN npm ci --only=production

# 3. Copy code last
COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
```

---

## Related Documentation

- **Root**: `FASTMCP_3.1.1+_MIGRATION.md` - FastMCP Docker considerations
- **Monitoring**: `../monitoring/` - Full monitoring stack setup
- **Projects**: `../projects/*/STRUCTURE.md` - Project-specific Docker setups

---

## Troubleshooting Quick Links

| Issue | Solution | Doc |
|-------|----------|-----|
| Daemon hangs during AI inference | Resource limits + memory boost | DOCKER_DAEMON_AI_WORKLOADS.md |
| Slow rebuilds | Use hot-reload (volume mounts) | DOCKER_DEV_GUIDE.md |
| Disk space filled | Log rotation + cleanup script | DOCKER_DAEMON_AI_WORKLOADS.md |
| Docker won't restart | Force kill zombie processes | DOCKER_ZOMBIE_RECOVERY.md |
| Containers randomly exit (code 137) | OOM - increase memory limits | DOCKER_DAEMON_AI_WORKLOADS.md |
| Port conflicts | Change port mapping in compose | DOCKER_DEV_GUIDE.md |

---

## Scripts

- **`check-docker-status.ps1`** — Comprehensive health check (daemon, images, containers, disk, resources, config)
- **`update-docker-desktop.ps1`** — Update recovery with optional `-FullWipe` for aggressive reset
- **`update-docker-desktop.bat`** — Batch version (legacy Windows compatible)
- **`fix-docker-daemon.ps1`** — Daemon stability & cleanup (from [DOCKER_DAEMON_AI_WORKLOADS.md](DOCKER_DAEMON_AI_WORKLOADS.md))
- **`fix-docker-daemon.bat`** — Batch daemon cleanup

### Justfile Shortcuts (from repo root)

Add to `justfile` for quick access:
```bash
just docker-status      # Run health check
just docker-update      # Fix update elevation error
just docker-update-full # Full wipe + update
just docker-fix         # Daemon cleanup (AI workloads)
```

---

**Location**: `D:/Dev/repos/mcp-central-docs/docker/`
**Purpose**: Centralize all Docker-related documentation for MCP projects, development, and AI inference workloads
