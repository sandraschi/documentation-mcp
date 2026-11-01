# Shared Monitoring Stack Guide

**Generated**: 2025-12-02

> **June 2026:** Use host ports **12000–12006**, `start-unified-monitoring.ps1`, and **[MONITORING_CURRENT_SETUP.md](./MONITORING_CURRENT_SETUP.md)**. Below, replace `:3000` / `:9090` / `:3100` with **12000** / **12001** / **12002**.

## Yes, Multiple Apps Can Share the Same Monitoring Stack!

You already have a **unified monitoring stack** configured in `mcp-central-docs/monitoring/`. Here's how to connect all your apps to it.

## Benefits

1. **Resource Efficiency** - One set of containers instead of 20+
2. **Centralized Dashboards** - All apps in one Grafana instance
3. **Unified Logging** - All logs searchable in one Loki instance
4. **No Port Conflicts** - Single set of ports (3000, 9090, 3100)
5. **Easier Management** - One place to configure alerts and dashboards

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Unified Monitoring Stack                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Grafana  │  │Prometheus│  │   Loki   │            │
│  │  :3000   │  │  :9090   │  │  :3100   │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│       ▲              ▲              ▲                 │
└───────┼──────────────┼──────────────┼─────────────────┘
        │              │              │
        └──────────────┴──────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
    ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
    │  myai   │  │  veogen │  │tailscale│
    │   app   │  │   app   │  │   mcp   │
    └─────────┘  └─────────┘  └─────────┘
```

## Setup Method 1: External Docker Network (Recommended)

### Step 1: Start Unified Monitoring Stack

```powershell
cd mcp-central-docs/monitoring/configs
docker compose -f docker-compose.unified-monitoring.yml up -d
```

This creates:
- Network: `configs_unified-monitoring` (or `unified-monitoring` if specified)
- Services: Grafana, Prometheus, Loki, Promtail, Node Exporter, cAdvisor

### Step 2: Connect Your Apps

Modify your app's `docker-compose.yml` to use the external network:

```yaml
# Example: myai/docker-compose.yml (remove existing monitoring services)
services:
  dashboard:
    # ... your existing config ...
    networks:
      - ai-network
      - unified-monitoring  # Add this external network

  document-viewer:
    # ... your existing config ...
    networks:
      - ai-network
      - unified-monitoring  # Add this external network

networks:
  ai-network:
    driver: bridge
  unified-monitoring:  # Add this
    external: true
    name: configs_unified-monitoring  # Match the network name from unified stack
```

### Step 3: Configure Prometheus to Scrape Your Apps

Edit `mcp-central-docs/monitoring/configs/prometheus/prometheus.yml`:

```yaml
scrape_configs:
  # MyAI Services
  - job_name: 'myai-dashboard'
    static_configs:
      - targets: ['myai-dashboard:3060']  # Service name in docker network
        labels:
          app: 'myai'
          service: 'dashboard'

  - job_name: 'myai-document-viewer'
    static_configs:
      - targets: ['document-viewer:5192']
        labels:
          app: 'myai'
          service: 'document-viewer'

  # VeoGen Services
  - job_name: 'veogen-backend'
    static_configs:
      - targets: ['backend:4700']
        labels:
          app: 'veogen'
          service: 'backend'

  # Tailscale MCP
  - job_name: 'tailscale-mcp'
    static_configs:
      - targets: ['tailscale-mcp-server:8080']
        labels:
          app: 'tailscale-mcp'
```

### Step 4: Configure Promtail to Collect Logs

Edit `mcp-central-docs/monitoring/configs/promtail/promtail.yml`:

```yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # MyAI Logs
  - job_name: myai
    static_configs:
      - targets:
          - localhost
        labels:
          job: myai
          __path__: /var/log/myai/*.log  # Mount host logs directory

  # VeoGen Logs
  - job_name: veogen
    static_configs:
      - targets:
          - localhost
        labels:
          job: veogen
          __path__: /var/log/veogen/*.log

  # Docker Container Logs
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
```

Update unified monitoring stack docker-compose to mount log directories:

```yaml
# mcp-central-docs/monitoring/configs/docker-compose.unified-monitoring.yml
services:
  promtail:
    volumes:
      - ./promtail/promtail.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
      # Add your app log directories
      - D:/Dev/repos/myai/logs:/var/log/myai:ro
      - D:/Dev/repos/veogen/backend/logs:/var/log/veogen:ro
      - D:/Dev/repos/tailscale-mcp/logs:/var/log/tailscale:ro
```

### Step 5: Update Grafana Datasources

The unified stack already configures Prometheus and Loki. Add app-specific dashboards in:

```
mcp-central-docs/monitoring/configs/grafana/dashboards/
```

## Setup Method 2: Shared Network (Alternative)

If you prefer everything in one compose file, you can extend the unified stack:

```yaml
# docker-compose.unified.yml (extends unified-monitoring.yml)
services:
  # Include all monitoring services
  grafana:
    extends:
      file: docker-compose.unified-monitoring.yml
      service: grafana

  # Add your app services
  myai-dashboard:
    # ... your config ...
    networks:
      - unified-monitoring

  veogen-backend:
    # ... your config ...
    networks:
      - unified-monitoring
```

## Real-World Example: Connecting myai to Unified Stack

### Current State (myai/docker-compose.yml)
- Has its own Prometheus (port 9191)
- Has its own Grafana (port 3100)
- Has its own Loki (port 3199)
- Has its own Promtail

### Updated Configuration

**Step 1: Remove duplicate monitoring services from myai/docker-compose.yml**

```yaml
# Remove these services:
# - prometheus (lines 585-598)
# - grafana (lines 601-618)
# - loki (lines 620-631)
# - promtail (lines 633-645)

# Keep your app services, just add external network:
services:
  dashboard:
    # ... existing config ...
    networks:
      - ai-network
      - unified-monitoring  # Add this

  document-viewer:
    # ... existing config ...
    networks:
      - ai-network
      - unified-monitoring  # Add this

networks:
  ai-network:
    driver: bridge
  unified-monitoring:
    external: true
    name: configs_unified-monitoring
```

**Step 2: Ensure your apps expose metrics endpoints**

Your apps already do this:
- Dashboard: `http://localhost:3060/api/v1/metrics`
- Document Viewer: `http://localhost:5192/api/metrics`

**Step 3: Update Prometheus config**

Add to `mcp-central-docs/monitoring/configs/prometheus/prometheus.yml`:

```yaml
scrape_configs:
  # Existing configs...
  
  # MyAI Platform
  - job_name: 'myai-platform'
    static_configs:
      - targets:
          - 'myai-dashboard:3060'
          - 'document-viewer:5192'
          - 'bob-and-alice:5188'
          - 'character-conversation:5190'
        labels:
          platform: 'myai'
```

## Networking Details

### Service Discovery

When services are on the same Docker network, they can reach each other by service name:

```yaml
# From unified-monitoring network
prometheus → myai-dashboard:3060  ✅ Works!
grafana → prometheus:9090        ✅ Works!
promtail → loki:3100             ✅ Works!

# From host machine
curl http://localhost:3000       ✅ Grafana
curl http://localhost:9090       ✅ Prometheus
curl http://localhost:3100       ✅ Loki
```

### Network Name Resolution

Docker Compose creates networks with pattern: `{directory}_{network-name}`

If unified stack is in `mcp-central-docs/monitoring/configs/`:
- Network name: `configs_unified-monitoring`

To use custom name, specify in unified stack:

```yaml
# docker-compose.unified-monitoring.yml
networks:
  unified-monitoring:
    name: unified-monitoring  # Explicit name (not prefixed)
    driver: bridge
```

Then apps reference it:
```yaml
networks:
  unified-monitoring:
    external: true
    name: unified-monitoring  # Match the explicit name
```

## Benefits Per App

### Before (Each App Has Own Stack)
```
myai:         Prometheus + Grafana + Loki + Promtail = 4 containers
veogen:       Prometheus + Grafana + Loki + Promtail = 4 containers
tailscale:    Prometheus + Grafana + Loki + Promtail = 4 containers
mywienerlinien: Grafana + Loki + Promtail = 3 containers
---
Total: 15 containers just for monitoring!
```

### After (Shared Stack)
```
Unified Stack: Prometheus + Grafana + Loki + Promtail = 4 containers
Apps: Just add network connection, no monitoring containers needed
---
Total: 4 containers for all monitoring!
```

**Resource Savings**: ~73% fewer containers (15 → 4)

## Port Consolidation

### Before
- Grafana: 3000, 3100, 3140, 4725 (4 instances)
- Prometheus: 9090, 9091, 9191 (3 instances)
- Loki: 3100, 3193, 3199, 4730 (4 instances)

### After (Unified)
- Grafana: 3000 (1 instance)
- Prometheus: 9090 (1 instance)
- Loki: 3100 (1 instance)

## Migration Checklist

For each app you want to migrate:

- [ ] 1. Identify monitoring services in app's docker-compose.yml
- [ ] 2. Remove Prometheus, Grafana, Loki, Promtail services
- [ ] 3. Add `unified-monitoring` external network to app services
- [ ] 4. Update Prometheus scrape configs with app service names
- [ ] 5. Update Promtail configs to mount app log directories
- [ ] 6. Test connectivity: `docker exec unified-prometheus wget -qO- http://myai-dashboard:3060/metrics`
- [ ] 7. Verify in Grafana: Check datasources and test queries
- [ ] 8. Update any hardcoded URLs in app code/configs

## Troubleshooting

### Service Not Reachable

**Problem**: Prometheus can't scrape `myai-dashboard:3060`

**Solution**:
```powershell
# Check if service is on the network
docker network inspect configs_unified-monitoring

# Check service is running
docker ps | Select-String "myai-dashboard"

# Test connectivity from Prometheus container
docker exec unified-prometheus wget -qO- http://myai-dashboard:3060/metrics
```

### Logs Not Appearing in Loki

**Problem**: Promtail can't read log files

**Solution**:
```powershell
# Check volume mounts
docker exec unified-promtail ls -la /var/log/myai/

# Check Promtail config path matches mount
docker exec unified-promtail cat /etc/promtail/config.yml

# Check Promtail is connected to Loki
docker logs unified-promtail
```

### Grafana Can't Query Prometheus

**Problem**: "Error querying Prometheus"

**Solution**:
```powershell
# Verify Grafana datasource config
docker exec unified-grafana cat /etc/grafana/provisioning/datasources/

# Test Prometheus is reachable from Grafana
docker exec unified-grafana wget -qO- http://prometheus:9090/api/v1/status/config
```

## Current Unified Stack Location

Your unified monitoring stack is here:
- **Config**: `mcp-central-docs/monitoring/configs/docker-compose.unified-monitoring.yml`
- **Network**: `configs_unified-monitoring` (or custom name if specified)

## Quick Start Command

```powershell
# Start unified monitoring stack
cd mcp-central-docs/monitoring/configs
docker compose -f docker-compose.unified-monitoring.yml up -d

# Verify it's running
docker ps | Select-String "unified-"

# Access Grafana
# http://localhost:3000 (admin/admin)
```

## Next Steps

1. **Start with one app** (e.g., `myai`) to test the pattern
2. **Verify metrics and logs** appear in unified Grafana/Loki
3. **Create app-specific dashboards** in Grafana
4. **Migrate other apps** one by one
5. **Remove duplicate monitoring stacks** from migrated apps

## Related Documentation

- **Unified Stack Config**: `../monitoring/configs/` (relative to mcp-central-docs root)
- **Unified Monitoring Documentation**: `../monitoring/UNIFIED_MONITORING_STACK.md`
- **Docker Monitoring Guide**: `../docker/MONITORING_STACK.md`
- **Example Connection Guide**: See `devices-mcp/MONITORING_STACK_CONNECTION.md` in devices-mcp repo

