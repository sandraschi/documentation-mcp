---
title: "Infrastructure Reliability & Disaster Recovery"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-06-26
# status: review -- added in bulk 2026-09-18; category is inferred and the
# content has NOT been verified against the current codebase. Change to
# active once someone has actually checked it.
---
# Infrastructure Reliability & Disaster Recovery

## 1. High-Availability Docker Guidelines

### 1.1. Windows/WSL2 Stability
Docker Desktop on Windows is a **Tier-2 host**. Always anticipate `vpnkit` or Named Pipe instability.

#### The "Docker Zombie" Force-Reset triplet:
If `docker ps` hangs, run:
```powershell
taskkill /F /IM "Docker Desktop.exe" /T
taskkill /F /IM "vpnkit.exe" /T
taskkill /F /IM "com.docker.backend.exe" /T
```

### 1.2. Edge Server (Mini-PC) Hardening
- ✅ **Disable Fast Startup**: Prevents WSL2 clock-skew.
- ✅ **AV Exclusions**: Exclude `%LOCALAPPDATA%\Docker\wsl`.
- ✅ **Tailscale Coordination**: Verify Docker stability after VPN reconnects.

## 2. Monitoring & Health Checks

- **Health Checks**: Every `docker-compose.yml` MUST include health checks for DB dependencies.
- **Failover**: Ports and paths should match documented standards across primary and backup nodes.
