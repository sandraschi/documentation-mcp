# Docker Daemon Unresponsiveness: AI Workload Optimization

**Problem:** Docker daemon hangs/becomes unresponsive during AI inference (LLMs, embeddings, model serving). Commands timeout, `docker ps` freezes, entire system becomes sluggish.

**Root Cause:** Resource exhaustion (RAM, disk) + log explosion + lack of resource limits on containers.

**Last Updated:** January 2026

---

## Quick Diagnosis

Run this to see if you have the problem:

```powershell
# If this hangs or takes >5 seconds: daemon is starving
docker ps

# Check memory usage
docker stats --no-stream

# Check disk bloat
docker system df
```

**Symptoms:**
- ✅ `docker ps` hangs or times out
- ✅ `docker logs` never returns
- ✅ GUI slow, high CPU/memory usage
- ✅ LLM inference randomly stops responding
- ✅ Container suddenly exits with exit code 137 (OOM killed)

---

## 1. Resource Exhaustion (Primary Culprit)

### Root Cause
Large language models consume **8GB - 128GB+ RAM** depending on model size. Without explicit resource limits, a single model container can consume all host memory, starving the Docker daemon itself.

### Symptoms
- Container runs fine for 30 seconds, then suddenly dies
- `docker inspect <container>` shows exit code 137 (Out of Memory)
- System becomes unresponsive (swapping to disk)

### Solution A: Set Resource Limits in Docker Compose

**docker-compose.yml:**
```yaml
services:
  llm-server:
    image: ollama:latest
    deploy:
      resources:
        limits:
          memory: 12g          # 👈 Hard limit (kill if exceeded)
          cpus: '4'            # 👈 Max 4 CPUs
        reservations:
          memory: 8g           # 👈 Minimum guaranteed
          cpus: '3'            # 👈 Minimum guaranteed
    environment:
      - OLLAMA_NUM_GPU=1       # Use GPU if available
```

**Benefits:**
- Container killed gracefully at 12GB (not entire system)
- Docker daemon remains responsive
- Other containers can still operate

### Solution B: Docker Run with Flags

```bash
docker run --memory 12g --cpus 4 \
  --memory-swap 16g \
  ollama:latest
```

---

## 2. Disk Exhaustion

### Root Cause
- Old dangling image layers pile up (especially multi-stage builds)
- Container logs grow unbounded
- Stopped containers never cleaned up

### Check Current Usage

```powershell
# See image/container/volume breakdown
docker system df

# See largest images
docker images --no-trunc --quiet | xargs docker inspect --format='{{.RepoTags}} {{.Size}}' | sort -k2 -rn | head -10

# See log files taking space
dir "$env:LOCALAPPDATA\Docker\containers" -Recurse -Filter "*-json.log" | Sort-Object Length -Descending | Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}} -First 10
```

### Solution A: Configure Log Rotation

**Edit `%APPDATA%\Docker\daemon.json`:**
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```

Then restart Docker Desktop.

**Benefits:**
- Old logs automatically deleted
- Only 3 × 100MB = 300MB per container max
- Prevents 50GB+ log files

### Solution B: Aggressive Cleanup

```powershell
# Remove exited containers
docker container prune -f

# Remove unused images (dangling + unreferenced)
docker image prune -a -f

# Remove unused volumes
docker volume prune -f

# Clear build cache
docker builder prune -a -f

# Everything at once
docker system prune -a -f --volumes
```

---

## 3. Docker Desktop VM Configuration (macOS/Windows)

### The Issue
Docker Desktop's internal Linux VM has fixed memory/CPU allocation. If set too low, the daemon starves.

### Check Current Settings

**PowerShell:**
```powershell
$settings = Get-Content "$env:APPDATA\Docker\settings.json" | ConvertFrom-Json
Write-Host "Memory: $($settings.memoryMiB) MB"
Write-Host "CPUs: $($settings.cpus)"
Write-Host "Swap: $($settings.memorySwapMiB) MB"
```

### Increase Allocation

1. Click Docker icon in system tray
2. Settings > Resources
3. **Memory**: Set to 12 GB or more (16 GB if running multiple models)
4. **CPUs**: Set to 4+ cores
5. **Swap**: Set to 4-8 GB
6. **Disk image size**: Ensure >100 GB available
7. Click "Apply & Restart"

---

## 4. Stale Processes & Containers

### Problem
- Stopped containers still hold memory
- Orphaned volumes consume disk
- Stale networks cause communication delays

### Solution

```powershell
# List all stopped containers
docker ps -a | Select-String "Exited"

# Remove all stopped containers
docker container prune -f

# List unused volumes
docker volume ls --filter dangling=true

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f
```

---

## 5. Enable Debug Logging

### When You're Stuck
Sometimes you need to see what the daemon is doing.

**Edit `%APPDATA%\Docker\daemon.json`:**
```json
{
  "debug": true,
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
```

Restart Docker Desktop, then check logs:

**Windows:**
```powershell
# Real-time logs
Get-Content "$env:APPDATA\Docker\log\vm\dockerd.log" -Tail 100 -Wait

# Search for hangs
Select-String "timeout|hang|blocked" "$env:APPDATA\Docker\log\vm\dockerd.log"
```

---

## 6. Automated Fix Script

### Run This Weekly

Run elevated (right-click → "Run as Administrator"):

```powershell
.\fix-docker-daemon.ps1
```

This script:
- ✅ Stops all running containers
- ✅ Removes exited containers
- ✅ Prunes unused images/volumes/networks
- ✅ Clears build cache
- ✅ Configures log rotation in daemon.json
- ✅ Recommends Docker Desktop memory boost

**Dry-run mode (preview changes):**
```powershell
.\fix-docker-daemon.ps1 -DryRun
```

**Skip aggressive pruning:**
```powershell
.\fix-docker-daemon.ps1 -SkipPrune
```

---

## 7. Real-World AI Workload Configuration

### Multi-Model Server with Resource Isolation

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Fast inference model
  fast-llm:
    image: ollama:latest
    container_name: fast-llm
    deploy:
      resources:
        limits:
          memory: 4g
          cpus: '2'
        reservations:
          memory: 2g
          cpus: '1'
    environment:
      - OLLAMA_NUM_GPU=0  # CPU only
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    restart: always

  # Heavy inference model
  heavy-llm:
    image: ollama:latest
    container_name: heavy-llm
    deploy:
      resources:
        limits:
          memory: 24g
          cpus: '8'
        reservations:
          memory: 16g
          cpus: '6'
    environment:
      - OLLAMA_NUM_GPU=1  # Use GPU if available
    volumes:
      - ollama_heavy:/root/.ollama
    ports:
      - "11435:11434"
    restart: always
    depends_on:
      - fast-llm

  # Embedding model (light)
  embeddings:
    image: ollama:latest
    container_name: embeddings
    deploy:
      resources:
        limits:
          memory: 2g
          cpus: '1'
    environment:
      - OLLAMA_NUM_GPU=0
    volumes:
      - ollama_embed:/root/.ollama
    ports:
      - "11436:11434"
    restart: always

  # Redis for caching
  redis:
    image: redis:alpine
    container_name: redis
    deploy:
      resources:
        limits:
          memory: 1g
          cpus: '1'
    ports:
      - "6379:6379"
    restart: always

volumes:
  ollama_data:
  ollama_heavy:
  ollama_embed:
```

**Why this works:**
- Each model has isolated limits (won't starve others)
- Docker daemon can still respond to queries
- Light models run fast (CPU)
- Heavy models get GPU + extra RAM
- Embeddings separate (always available)

---

## 8. Monitoring During Development

### Live Dashboard (Recommended)

```powershell
# Real-time stats for all containers
docker stats

# Pretty output with custom format
docker stats --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}\t{{.Status}}"

# One-time snapshot
docker stats --no-stream
```

### Alert on Exit Code 137 (OOM Kill)

```powershell
# Check for containers killed by OOM
docker ps -a --filter "exited=137" --format "table {{.Names}}\t{{.ExitCode}}\t{{.CreatedAt}}"

# View exit code in logs
docker inspect <container_name> | findstr ExitCode
```

### Log Monitoring

```powershell
# Follow logs in real-time
docker logs -f <container_name>

# Last N lines
docker logs --tail 100 <container_name>

# Search for errors
docker logs <container_name> | Select-String "ERROR|error|Exception"
```

---

## 9. Troubleshooting Checklist

### Daemon Still Hanging After Steps 1-7?

1. **Check for ghost processes:**
   ```powershell
   Get-Process | Select-String "docker|wsl"
   ```
   If stuck processes exist: kill and restart Docker Desktop

2. **Check WSL2 health (Windows only):**
   ```powershell
   wsl --list --verbose
   wsl --shutdown  # Graceful reset
   ```

3. **Check disk space (root filesystem):**
   ```powershell
   # In WSL2
   wsl -e df -h /
   # If <10% free: expand disk image in Docker settings
   ```

4. **Check for file lock issues:**
   ```powershell
   # Exclude Docker directories from antivirus
   # Settings > Exclude Folders > Add:
   # %APPDATA%\Docker
   # %LOCALAPPDATA%\Docker\wsl
   ```

5. **Nuclear option (last resort):**
   ```powershell
   # Reset WSL2
   wsl --unregister Docker-Desktop
   
   # Then restart Docker Desktop (will reinit)
   ```

---

## 10. Prevention: Weekly Maintenance

### Script to Add to Task Scheduler

**Create `maintenance.ps1`:**
```powershell
# Weekly Docker maintenance
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Write-Host "[$timestamp] Starting Docker maintenance..."

# Cleanup
docker container prune -f | Out-Null
docker image prune -a -f | Out-Null
docker volume prune -f | Out-Null
docker builder prune -a -f | Out-Null

# Report
$diskUsage = docker system df
Write-Host $diskUsage

Write-Host "[$timestamp] Maintenance complete"
```

**Add to Task Scheduler (Admin PowerShell):**
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
  -Argument "-ExecutionPolicy Bypass -File C:\path\to\maintenance.ps1"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 02:00AM

Register-ScheduledTask -TaskName "Docker Maintenance" `
  -Action $action -Trigger $trigger -RunLevel Highest
```

---

## 11. For Production / 24/7 AI Services

### Recommended Setup
- **Move to Linux host** (not Windows WSL2)
- **Use Kubernetes or Docker Swarm** for multi-container orchestration
- **Enable resource limits** on all containers
- **Set up monitoring** (Prometheus, Grafana)
- **Enable log aggregation** (ELK, Loki)
- **Use dedicated GPU servers** for large models

### Temporary: Docker Compose with Health Checks

```yaml
services:
  llm:
    image: ollama:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: on-failure:5  # Restart up to 5 times on failure
    deploy:
      resources:
        limits:
          memory: 24g
          cpus: '8'
```

---

## Quick Action List

**Right now:**
1. ✅ Run `docker system df` and check disk usage
2. ✅ Run `docker stats --no-stream` and check memory
3. ✅ Set resource limits on AI containers (deploy.resources.limits)

**This week:**
1. ✅ Run `fix-docker-daemon.ps1` script
2. ✅ Increase Docker Desktop memory to 12GB+ (Settings > Resources)
3. ✅ Configure log rotation in daemon.json

**This month:**
1. ✅ Monitor with `docker stats` during model inference
2. ✅ Set up Task Scheduler for weekly cleanup
3. ✅ Add health checks to docker-compose.yml

---

## References

- Docker Container Resource Limits: https://docs.docker.com/config/containers/resource_constraints/
- Docker Compose Deploy Section: https://docs.docker.com/compose/compose-file/#deploy
- Docker Desktop Settings: https://docs.docker.com/desktop/settings/windows/
- Docker Daemon Configuration: https://docs.docker.com/engine/daemon/
- Docker Stats: https://docs.docker.com/reference/cli/docker/stats/

---

**Last Updated:** January 2026
**Author:** Gordon AI (Docker)
**Context:** Recurring issue in MCP/AI workload development with models running on Docker
