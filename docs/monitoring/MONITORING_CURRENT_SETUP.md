# Unified monitoring — current setup (June 2026)

**Canonical reference.** Older docs (`HOW_TO_USE.md`, `UNIFIED_MONITORING_ANSWER.md`, port `3000` examples) are historical — use this file first.

## What runs where

| Service | Host port | Container port | URL |
|---------|-----------|----------------|-----|
| Grafana | **12000** | 3000 | http://localhost:12000 |
| Prometheus | **12001** | 9090 | http://localhost:12001 |
| Loki | **12002** | 3100 | http://localhost:12002 |
| Promtail | **12003** | 9080 | http://localhost:12003 |
| node-exporter | **12004** | 9100 | http://localhost:12004/metrics |
| cAdvisor | **12005** | 8080 | http://localhost:12005 |
| blackbox-exporter | **12006** | 9115 | (internal probes) |
| OTel Collector | **4317** (gRPC), **4318** (HTTP) | 4317, 4318 | OTLP receiver for fleet traces + metrics |
| Tempo | **3200** | 3200 | http://localhost:3200 (trace query API) |

Override ports in `monitoring/.env` (see `.env.example`). Registered in `operations/WEBAPP_PORTS.md` under **Unified observability stack**.

**Do not** bind 3000 / 9090 / 3100 on the host — other stacks (tailscale-mcp, teleconference-mcp, etc.) already use them.

## Start / stop

```powershell
Set-Location D:\Dev\repos\mcp-central-docs\monitoring
pwsh -NoProfile -ExecutionPolicy Bypass -File .\start-unified-monitoring.ps1
```

The script:

1. Creates `logs/host/<job>/` directories  
2. Merges `prometheus.core.yml` + `prometheus.fleet.yml` → `prometheus.yml`  
3. Merges `promtail.unified.yml` + `promtail.host.yml` → `promtail.yml`  
4. `docker compose -p monitoring up -d`

Stop:

```powershell
docker compose -p monitoring -f docker-compose.unified-monitoring.yml down
```

## Prometheus — what is scraped today

**In-stack:** Grafana, Prometheus, Loki, Promtail, node-exporter, cAdvisor.

**Fleet (host processes via `host.docker.internal`)** — edit `prometheus/prometheus.fleet.yml`, then:

```powershell
.\scripts\merge-prometheus-config.ps1
docker compose -p monitoring -f docker-compose.unified-monitoring.yml restart prometheus
```

| Job | Port | Notes |
|-----|------|--------|
| `docs-mcp` | 10795 | `/metrics` — RAG gauges (`docs_index_*`) |
| `docs-mcp-rag` | 10795 | blackbox `/api/status` |
| `devices-mcp` | 10717 | blackbox `/api/health` |
| `devices-mcp-ring-metrics` | 8001 | Ring Prometheus (when Ring stack runs) |
| `calibre-mcp` | 10720 | `/metrics`, `/health` |
| `calibre-plus` | 10736 | MyAI Docker backend |
| `plex-mcp` | 10740 | blackbox `/health` |
| `avatar-mcp-metrics` | 10790 | |
| `mcp-studio-host` | 8330 | |

Machine-specific targets: `prometheus.fleet.local.yml` (gitignored).

## Logs (Loki) — host + Docker

**Docker:** Promtail discovers containers with `monitoring.unified=true` or names matching `devices`, `plex`, `calibre`, `immich`, etc.

**Host (no container required):** logs must exist as **files**:

| Path on host | Inside Promtail | Content |
|--------------|-----------------|---------|
| `monitoring/logs/host/<job>/*.log` | `/host-logs/<job>/` | Tee from `Invoke-FleetLoggedCommand.ps1` or `web_sota/start.ps1` |
| `mcp-central-docs/debug.log` | `/repos/mcp-central-docs/debug.log` | Docs MCP `log_to_file()` |
| `%USERPROFILE%\.local\share\devices-mcp\` | `/host-user-local/devices-mcp/` | devices-mcp default file logging |

```powershell
.\scripts\Invoke-FleetLoggedCommand.ps1 -JobName plex-mcp `
  -WorkingDirectory D:\Dev\repos\plex-mcp `
  -Command "uv run uvicorn plex_mcp.server:app --host 127.0.0.1 --port 10740 --log-level info"
```

Grafana Explore:

```logql
{job="docs-mcp", platform="host"}
{job="devices-mcp", platform="host"}
```

## Grafana dashboards (provisioned)

| Dashboard | UID | Repo / scope |
|-----------|-----|----------------|
| MCD / RAG & Fleet probes | `mcd-rag-fleet` | docs-mcp, fleet blackbox |
| devices-mcp | `devices-mcp-fleet` | devices-mcp |
| plex-mcp | `plex-mcp-fleet` | plex-mcp |
| calibre-mcp | `calibre-mcp-fleet` | calibre-mcp + calibre-plus |
| mcp-studio | (see JSON) | mcp-studio |
| unified-monitoring-overview | | Legacy multi-job overview |
| tailscale-* (5 boards) | | tailscale-mcp (legacy; prefer unified) |

Add JSON under `grafana/dashboards/` and restart Grafana.

## MCP tool-call monitoring (no log line required)

**Loki alone cannot see tool calls** unless the server logs each `tools/call` (or you parse access logs).

**Prometheus can**, if the server exports metrics (recommended fleet pattern):

| Metric | Labels | Meaning |
|--------|--------|---------|
| `mcp_tool_calls_total` | `tool_name`, `status` | Count per tool (success/error) |
| `mcp_tool_duration_seconds` | `tool_name` | Histogram of latency |
| `mcp_errors_total` | `tool_name`, `error_type` | Optional detail |

Implement once per repo (middleware or decorator on FastMCP tools), expose on the same `/metrics` HTTP server as the webapp, add scrape job in `prometheus.fleet.yml`. Template: `QUICK_START.md` § Prometheus metrics + `MCP_MONITORING_STANDARDS.md`.

**Without instrumentation you only get:**

- Process up/down and blackbox `/health`
- Coarse HTTP traffic if uvicorn access logging is enabled and tailed to Loki
- **Not** per-tool names, latency, or error breakdown

**Now live:** OpenTelemetry tracing (OTel Collector + Tempo on :4317/:3200). Canary: winrar-mcp. See `patterns/OPENTELEMETRY_FLEET_ROLLOUT.md`.

## observability-mcp (`D:\Dev\repos\observability-mcp`)

**Not a second PLG stack** — it is an **MCP control plane** (Grafana/Loki/Prometheus API tools, fleet health, correlation). The unified stack in this folder is the **single** Prometheus/Loki/Grafana store (ports **12000–12006**).

| Role | Port | Notes |
|------|------|--------|
| MCP HTTP (uvicorn) | **12007** | `observability_mcp.server:app` — agents connect here |
| Web UI | **12008** | `web_sota/start.ps1` |
| Process `/metrics` exporter | **12009** (`PROMETHEUS_PORT`) | **Not** the Prometheus *server* — do not confuse with unified **12001** |

**Bundled `docker-compose.yml` in observability-mcp** binds Grafana **3000**, Prometheus **9091**, Loki **3100** — same conflicts as tailscale-mcp / teleconference-mcp. **Do not run it** when unified monitoring is up.

**Recommended wiring:**

1. Start unified stack: `.\start-unified-monitoring.ps1` (this repo).
2. Point observability-mcp at unified endpoints (copy `observability-mcp/.env.unified-monitoring.example` → `.env`):

   - `GRAFANA_URL=http://127.0.0.1:12000`
   - `LOKI_URL=http://127.0.0.1:12002`
   - `PROMETHEUS_SERVER_URL=http://127.0.0.1:12001` (API / queries; not `PROMETHEUS_PORT`)

3. Scrape observability-mcp process metrics from unified Prometheus (`prometheus.fleet.yml` job `observability-mcp-process` on host **12009**).
4. Use **observability-mcp tools** for cross-repo dashboards/log search; use **per-repo `/metrics`** (devices **10717**, calibre **10720**, plex **10740**, docs **10795**) for `mcp_tool_*` series.

Template for tool metrics middleware: `monitoring/templates/fleet_tool_metrics.py` (wired in devices-mcp, plex-mcp, calibre-mcp).

## Related docs

| Doc | Use when |
|-----|----------|
| [CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md) | Wiring a new repo |
| [MCP_MONITORING_STANDARDS.md](./MCP_MONITORING_STANDARDS.md) | Instrumentation checklist |
| [QUICK_START.md](./QUICK_START.md) | Copy-paste metrics middleware |
| [IMAGE_VERSIONS.md](./IMAGE_VERSIONS.md) | Pin upgrades |
| [LOGURU_APPLICATION_LOGGING.md](./LOGURU_APPLICATION_LOGGING.md) | Python logging → files → Loki |

Historical / deep-dive (may mention old ports): `UNIFIED_MONITORING_STACK.md`, `SHARED_MONITORING_STACK_GUIDE.md`, `HOW_TO_USE.md`.


