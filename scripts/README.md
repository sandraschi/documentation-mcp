# Scripts Directory

Utility scripts for MCP Central Docs management and Docker optimization.

---

## Docker Management

### fix-docker-daemon.ps1
**PowerShell script (recommended)**

Comprehensive Docker daemon maintenance for AI workloads. Fixes unresponsive daemon, resource exhaustion, disk bloat during LLM inference.

**Usage (run as Administrator):**
```powershell
.\fix-docker-daemon.ps1
```

**Options:**
```powershell
# Dry-run mode (preview changes without executing)
.\fix-docker-daemon.ps1 -DryRun

# Skip aggressive image pruning
.\fix-docker-daemon.ps1 -SkipPrune
```

**What it does:**
- Stops all running containers
- Removes exited containers
- Prunes unused images, volumes, networks
- Clears build cache
- Configures log rotation in daemon.json (prevents 50GB+ logs)
- Recommends Docker Desktop memory boost

**Output:**
- Colored status messages (SUCCESS/INFO/WARN/ERROR)
- Before/after disk usage comparison
- Step-by-step next actions

---

### fix-docker-daemon.bat
**Batch script (legacy/older Windows compatible)**

Same functionality as PowerShell version, simpler syntax for batch environments.

**Usage (run as Administrator):**
```cmd
fix-docker-daemon.bat
```

**Differences from .ps1:**
- No parameters
- Less robust error handling
- Simpler console output

---

## Scheduling Maintenance

### Run Weekly (Task Scheduler - Windows)

**Create scheduled task (Admin PowerShell):**
```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
  -Argument "-ExecutionPolicy Bypass -File $(pwd)\fix-docker-daemon.ps1"

$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 02:00AM

Register-ScheduledTask -TaskName "Docker Maintenance" `
  -Action $action -Trigger $trigger -RunLevel Highest
```

**Or edit Task Scheduler GUI:**
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Docker Maintenance"
4. Trigger: Weekly, Sunday 02:00 AM
5. Action: Start PowerShell script
   - Program: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "D:\Dev\repos\mcp-central-docs\scripts\fix-docker-daemon.ps1"`
6. Conditions: Run with highest privileges

---

## Related Documentation

See `../docker/DOCKER_DAEMON_AI_WORKLOADS.md` for:
- Complete troubleshooting guide
- Real-world configuration examples
- Multi-model LLM setup with resource isolation
- Monitoring and alerting
- Production recommendations

---

## Quick Diagnosis

Before running fix script, check current state:

```powershell
# Check memory/CPU usage
docker stats --no-stream

# Check disk usage
docker system df

# Check for containers killed by OOM (exit code 137)
docker ps -a --filter "exited=137" --format "table {{.Names}}\t{{.ExitCode}}\t{{.CreatedAt}}"
```

---

## Common Issues

### Script won't run
```
ERROR: This script must run as Administrator
```
**Solution:** Right-click PowerShell → "Run as Administrator"

### Script times out during prune
This is normal with large image repos. Script will retry. Wait 2-3 minutes.

### Docker daemon still unresponsive after script
1. Run again (sometimes requires 2 passes)
2. Increase Docker Desktop memory: Settings > Resources > Memory (12GB+)
3. Check disk space: `docker system df`
4. See DOCKER_DAEMON_AI_WORKLOADS.md section 9 (Troubleshooting Checklist)

---

## Repository Structure

```
mcp-central-docs/
├── scripts/
│   ├── fix-docker-daemon.ps1      ← Run this for daemon issues
│   ├── fix-docker-daemon.bat      ← Alt: Windows batch version
│   ├── README.md                  ← You are here
│   ├── ollama scripts/            ← LLM model utilities
│   └── ...other scripts
├── docker/
│   ├── DOCKER_DAEMON_AI_WORKLOADS.md    ← Full guide
│   ├── DOCKER_DEV_GUIDE.md
│   ├── DOCKER_ZOMBIE_RECOVERY.md
│   └── README.md
└── ...
```

---

**Last Updated:** January 15, 2026
**Maintained by:** Gordon AI (Docker)
