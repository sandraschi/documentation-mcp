# Unified Monitoring Stack

**One Grafana. One Loki. One Prometheus. For the entire fleet.**

This directory contains the **shared observability stack** for all MCP repositories,
MyAI, VeoGen, home infrastructure, and any future projects.
Do **not** spin up per-repo monitoring containers — add dashboards/scrape targets here instead.

---

## Architecture

```
┌──────────────────── unified monitoring stack ──────────────────────┐
│                                                                      │
│  grafana:13.0.1  :12000 ──┬── datasource: Loki  (label filtering)   │
│                            └── datasource: Prometheus (job filter)  │
│                                                                      │
│  loki:3.7.1      :12002 ← Promtail scrapes all containers via       │
│                            Docker socket, streams labelled per repo  │
│                            e.g. {job="plex-mcp"}, {job="calibre"}   │
│                                                                      │
│  prometheus:v3.11.3 :12001 ← scrapes /metrics endpoints per service │
│                                                                      │
│  promtail:3.6.10 :12003 ← log collector (Docker API on Windows)     │
│  node-exporter   :12004 ← host system metrics                       │
│  cadvisor        :12005 ← container metrics                         │
└──────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```powershell
# From this directory (recommended after Docker reinstall):
pwsh -NoProfile -ExecutionPolicy Bypass -File .\start-unified-monitoring.ps1

# Or manually:
docker compose -p monitoring -f docker-compose.unified-monitoring.yml pull
docker compose -p monitoring -f docker-compose.unified-monitoring.yml up -d
docker compose -p monitoring -f docker-compose.unified-monitoring.yml ps
```

**Host ports** default to **12000–12006** (not 3000/9090/3100). Override in `monitoring/.env` (copy from `.env.example`).

**Host logs:** Promtail tails files under `monitoring/logs/host/<job>/` and known paths (e.g. devices-mcp under `%USERPROFILE%\.local\share`). Use `scripts/Invoke-FleetLoggedCommand.ps1` — dockerization not required.

Services after startup:
- **Grafana**: http://localhost:12000 (admin / admin)
- **Prometheus**: http://localhost:12001
- **Loki**: http://localhost:12002/ready
- **Promtail**: http://localhost:12003
- **cAdvisor**: http://localhost:12005
- **node-exporter**: http://localhost:12004/metrics

## Connecting a New MCP Server

See **[CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md)** — opt-in labels, fleet scrape list, blackbox probes, and MCD `/metrics`.

### Quick reference

### Metrics (Prometheus)
Add a scrape job to `prometheus/prometheus.fleet.yml`, then merge (see CONNECT guide):
```yaml
- job_name: 'my-new-mcp'
  static_configs:
    - targets: ['host.docker.internal:YOUR_PORT']
```

### Logs (Loki via Promtail)
Host: tee to `logs/host/<job>/` or use devices-mcp file logging under `%USERPROFILE%\.local\share`.  
Docker: label `monitoring.unified: "true"` and `monitoring.job: "my-new-mcp"`.  
See [CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md).

### Dashboards (Grafana)
Provisioned JSON in `grafana/dashboards/`:

| File | Repo |
|------|------|
| `mcd-rag-fleet.json` | docs-mcp / MCD RAG |
| `devices-mcp.json` | devices-mcp |
| `plex-mcp.json` | plex-mcp |
| `calibre-mcp.json` | calibre-mcp |
| `mcp-studio-dashboard.json` | mcp-studio |
| `tailscale-*.json` | tailscale-mcp (legacy) |

Restart Grafana after adding a board.

## Image Versions

See **[IMAGE_VERSIONS.md](./IMAGE_VERSIONS.md)** — all images are pinned, never `:latest`.

## Updating Images

```powershell
# Pull new images (no downtime):
docker compose -f docker-compose.unified-monitoring.yml pull

# Recreate (~30s downtime on monitoring stack only):
docker compose -f docker-compose.unified-monitoring.yml up -d --force-recreate
```
Then update `IMAGE_VERSIONS.md` with the new tags and date.

## Troubleshooting Docker Desktop

If Docker Desktop hangs or daemon returns 500 errors, use the **Triple Kill**:

```powershell
taskkill /IM "Docker Desktop.exe" /F
taskkill /IM "com.docker.backend.exe" /F
taskkill /IM "vpnkit.exe" /F
```

Then restart Docker Desktop and wait up to 90s for the daemon.
If it persists across restarts, reinstall Docker Desktop (the WSL2 backend corrupts occasionally).
See `D:\Dev\repos\mcp-central-docs\docker\DOCKER_ZOMBIE_RECOVERY.md` for the full procedure.

## Key Documents

| Doc | Purpose |
|---|---|
| **[MONITORING_CURRENT_SETUP.md](./MONITORING_CURRENT_SETUP.md)** | **Canonical — ports, scrape, logs, dashboards, tool metrics** |
| [CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md) | Connect any repo (host or Docker) |
| [UNIFIED_MONITORING_STACK.md](./UNIFIED_MONITORING_STACK.md) | Full architecture deep-dive (some legacy ports) |
| [SHARED_MONITORING_STACK_GUIDE.md](./SHARED_MONITORING_STACK_GUIDE.md) | How to connect any app |
| [IMAGE_VERSIONS.md](./IMAGE_VERSIONS.md) | Pinned image versions + history |
| [MCP_MONITORING_STANDARDS.md](./MCP_MONITORING_STANDARDS.md) | Standards for MCP server instrumentation |
| [LOGURU_APPLICATION_LOGGING.md](./LOGURU_APPLICATION_LOGGING.md) | Python app logging vs Loki |
| [QUICK_START.md](./QUICK_START.md) | Step-by-step onboarding |
