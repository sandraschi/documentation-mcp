# monitoring-mcp

[![CI](https://github.com/sandraschi/monitoring-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sandraschi/monitoring-mcp/actions)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.2-purple)](https://github.com/jlowin/fastmcp)
[![Grafana](https://img.shields.io/badge/Grafana-Supported-orange)](https://grafana.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-Supported-orange)](https://prometheus.io)
[![Loki](https://img.shields.io/badge/Loki-Supported-green)](https://grafana.com/oss/loki/)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue)](https://python.org)

An MCP server that connects AI assistants to your Grafana + Prometheus + Loki
observability stack (local, Docker, or remote). Query metrics, search logs,
manage dashboards, and correlate incidents across all three — through natural
language.

> **Docs**: [INSTALL.md](INSTALL.md) · [Configuration](docs/CONFIGURATION.md) · [Tools](docs/TOOLS.md) · [Development](docs/DEVELOPMENT.md) · [Troubleshooting](docs/TROUBLESHOOTING.md)

## Features

- **Grafana** — list, create, update dashboards; query datasources; analyze panels
- **Prometheus** — run PromQL queries (instant + range), check targets, list alerts
- **Loki** — LogQL search, tail, anomaly detection, error correlation, request tracing
- **Cross-system correlation** — root cause analysis across metrics + logs + dashboards
- **Health monitoring** — system health, connectivity tests, configuration validation
- **AI chat** — ask questions in natural language via the web UI or Claude Desktop

## Quick Install

```powershell
git clone https://github.com/sandraschi/monitoring-mcp
cd monitoring-mcp
just
```

Or drag the `.mcpb` bundle into Claude Desktop. See [INSTALL.md](INSTALL.md) for all options.

## What You Can Do

| You say | The server does |
|---------|----------------|
| "Check system health" | Hits Grafana/Prometheus/Loki APIs; returns status per component |
| "Show my top 5 error log sources" | LogQL query across Loki; groups by label |
| "List Grafana dashboards tagged prod" | Searches Grafana API; filters by tag |
| "Correlate the 5xx spike at 14:30" | Cross-references Prometheus error rates with Loki error logs |

## Quick Start (Code)

```python
await monitoring_status(operation="system_health")
await prometheus_monitoring(operation="query_metrics", query='up')
await loki_logging(operation="query_logs", query='{job="api"} |= "ERROR"')
await grafana_management(operation="list_dashboards")
```

## Project Structure

```
├── src/monitoring_mcp/       # Python MCP server
│   ├── tools/                # Portmanteau tools (grafana, prometheus, loki, correlation, status)
│   ├── config.py             # Pydantic v2 settings
│   ├── server.py             # ASGI entry point
│   └── web.py                # REST endpoints (/api/chat, /api/health, /api/tools)
├── web_sota/                 # React/Vite/Tailwind dashboard
├── native/                   # Tauri 2.0 NSIS wrapper
└── docs/                     # Reference documentation
```
