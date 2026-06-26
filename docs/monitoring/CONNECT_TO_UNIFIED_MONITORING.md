# Connect Any Repo to Unified Monitoring

Unified stack: `mcp-central-docs/monitoring` — Grafana **12000**, Prometheus **12001**, Loki **12002**.

## 1. Metrics (Prometheus)

### A. Expose `/metrics` (preferred)

Add a Prometheus text endpoint on your backend port, then register in `prometheus/prometheus.fleet.yml`:

```yaml
  - job_name: my-repo-mcp
    static_configs:
      - targets: ["host.docker.internal:YOUR_PORT"]
        labels:
          app: my-repo-mcp
    metrics_path: /metrics
    scrape_interval: 30s
```

Re-run `start-unified-monitoring.ps1` (merges fleet into `prometheus.yml`) or:

```powershell
.\scripts\merge-prometheus-config.ps1
docker compose -p monitoring -f docker-compose.unified-monitoring.yml restart prometheus
```

**Local overrides (gitignored):** copy `prometheus/prometheus.fleet.local.example.yml` → `prometheus.fleet.local.yml`.

### B. Health only (blackbox)

If you only have `/health` or `/api/health`, add a target under `blackbox-fleet-http` in `prometheus.fleet.yml`:

```yaml
          - http://host.docker.internal:YOUR_PORT/health
```

Relabel `job` in the same file (copy an existing `regex` / `replacement` pair).

### Already wired

| Repo | Port | Scrape |
|------|------|--------|
| mcp-central-docs (MCD / RAG) | 10795 | `/metrics`, `/api/status` (blackbox) |
| devices-mcp | 10717 | blackbox `/api/health`; Ring `:8001` if running |
| calibre-mcp | 10720 | `/metrics`, `/health` |
| calibre-plus (MyAI) | 10736 | `/metrics`, `/health` |
| plex-mcp | 10740 | blackbox `/health` |
| avatar-mcp | 10790 | `/metrics` |
| mcp-studio | 8330 | `/api/v1/health/metrics` |

Host processes must listen on `127.0.0.1` (Docker Desktop uses `host.docker.internal`).

## 2. Logs (Loki / Promtail)

**Docker is not required.** Host-run MCPs must write logs to **files** Promtail can read (stdout tee or app file logging).

### Host processes (uvicorn, `just start`, NSSM)

1. Promtail mounts:
   - `monitoring/logs/host/` → `/host-logs/`
   - repo root `D:\Dev\repos` → `/repos/` (e.g. `mcp-central-docs/debug.log`)
   - `%USERPROFILE%\.local\share` → `/host-user-local/` (devices-mcp default log dir)

2. Start with fleet tee (recommended):

```powershell
cd D:\Dev\repos\mcp-central-docs\monitoring
.\scripts\Invoke-FleetLoggedCommand.ps1 -JobName docs-mcp `
  -WorkingDirectory D:\Dev\repos\mcp-central-docs `
  -Command "uv run python -m uvicorn docs_mcp.server:app --host 127.0.0.1 --port 10795 --log-level info"
```

Or use `web_sota/start.ps1` (tees to `monitoring/logs/host/docs-mcp/uvicorn.log`).

3. Grafana → Explore → Loki:

```logql
{job="docs-mcp", platform="host"}
```

Extra globs: `promtail/promtail.host.local.yml` (see `.example`).

### Docker containers (optional)

In `docker-compose.yml`:

```yaml
services:
  my-mcp:
    labels:
      monitoring.unified: "true"
      monitoring.job: "my-repo-mcp"
```

Promtail job `fleet-mcp-labeled` ships stdout to Loki. Filter in Grafana: `{job="my-repo-mcp"}`.

### Name-based (no label)

Containers whose names match `devices`, `plex`, `calibre`, `avatar`, `tailscale`, `calibre-plus`, etc. are picked up by `fleet-mcp-containers`.

## 3. Docker network (optional)

To scrape by **service name** instead of host ports, attach the app to the unified network:

```yaml
networks:
  unified-monitoring:
    external: true
    name: monitoring_unified-monitoring
```

Then use targets like `calibre-mcp:10720` in `prometheus.fleet.yml` (only works for containers on that network).

## 4. Grafana

- Open http://localhost:12000 (admin/admin).
- Dashboards auto-load from `grafana/dashboards/`.
- **Provisioned boards:** `mcd-rag-fleet`, `devices-mcp`, `plex-mcp`, `calibre-mcp`, `mcp-studio-dashboard`, tailscale-* (legacy).

## 5. Do not run per-repo Grafana/Prometheus

Remove duplicate monitoring sidecars (e.g. tailscale-mcp `:3000` stack) once unified covers your targets — avoids port fights and duplicate TSDBs.
