# Configuration

## Environment Variables

### Web Authentication (REQUIRED for web UI)

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_WEB_USER` | Web UI username | (required) |
| `MCP_WEB_PASSWORD` | Web UI password | (required) |

### Monitoring Endpoints

| Variable | Description | Default |
|----------|-------------|---------|
| `MONITORING_MCP_GRAFANA_URL` | Grafana server URL | `http://localhost:3000` |
| `MONITORING_MCP_PROMETHEUS_URL` | Prometheus server URL | `http://localhost:9090` |
| `MONITORING_MCP_LOKI_URL` | Loki server URL | `http://localhost:3100` |

### Grafana Authentication

| Variable | Description |
|----------|-------------|
| `MONITORING_MCP_GRAFANA_API_KEY` | Grafana API key (recommended) |
| `MONITORING_MCP_GRAFANA_USERNAME` | Grafana username (alternative) |
| `MONITORING_MCP_GRAFANA_PASSWORD` | Grafana password (alternative) |

### Performance

| Variable | Description | Default |
|----------|-------------|---------|
| `MONITORING_MCP_REQUEST_TIMEOUT` | HTTP request timeout (s) | `30` |
| `MONITORING_MCP_MAX_CONCURRENT_REQUESTS` | Max concurrent API calls | `10` |
| `MONITORING_MCP_MAX_RESULTS_LIMIT` | Max query results | `1000` |
| `MONITORING_MCP_ENABLE_SAMPLING` | Auto-sample large datasets | `true` |
| `MONITORING_MCP_SAMPLING_THRESHOLD` | Row count to trigger sampling | `10000` |
| `MONITORING_MCP_SAMPLING_RATE` | Fraction to sample | `0.1` |

### Storage

| Variable | Description | Default |
|----------|-------------|---------|
| `MONITORING_MCP_STORAGE_PATH` | Persistent data directory | `~/.monitoring-mcp` |

### Transport (MCP mode)

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_TRANSPORT` | `stdio`, `http`, or `sse` | `stdio` |
| `MCP_PORT` | HTTP listening port | `10851` |
| `MCP_HOST` | Bind address | `127.0.0.1` |
| `MCP_PATH` | HTTP endpoint path | `/mcp` |

### Frontend

| Variable | Description | Default |
|----------|-------------|---------|
| `MONITORING_PORT` | Backend port for uvicorn | `12007` (or `MCP_PORT`) |
| `MONITORING_HOST` | Backend bind address | `127.0.0.1` |

## .env File

Copy `.env.example` to `.env` at the repo root:

```bash
cp .env.example .env
```

## Ports

| Port | Service |
|------|---------|
| 10850 | Frontend (Vite dev) |
| 10851 | Backend (FastAPI + MCP HTTP) |
