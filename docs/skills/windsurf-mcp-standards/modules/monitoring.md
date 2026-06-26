# Monitoring Standards

## Overview
Comprehensive monitoring standards using Prometheus, Grafana, and Loki for observability, alerting, and performance tracking in MCP server ecosystems.

## Monitoring Architecture

### Core Components
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Servers   │    │   Prometheus    │    │     Grafana     │
│                 │    │                 │    │                 │
│ • Metrics       │───▶│ • Time Series   │    │ • Dashboards    │
│ • Health Checks │    │ • Alerting      │    │ • Visualizations│
│ • Custom Events │    │ • Service       │    │ • Alerts        │
└─────────────────┘    │   Discovery     │    └─────────────────┘
                       └─────────────────┘             │
┌─────────────────┐    ┌─────────────────┐             │
│      Loki       │    │   AlertManager  │             │
│                 │    │                 │             │
│ • Log           │◀───│ • Alert Routing │◀────────────┘
│   Aggregation   │    │ • Notifications │
│ • Querying      │    │ • Silencing     │
└─────────────────┘    └─────────────────┘
```

### Infrastructure Setup
```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--storage.tsdb.retention.time=200h'
      - '--web.enable-lifecycle'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3100:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - ./monitoring/grafana/dashboards:/var/lib/grafana/dashboards

  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki/local-config.yaml:/etc/loki/local-config.yaml
      - loki_data:/loki
    command: -config.file=/etc/loki/local-config.yaml

  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./monitoring/promtail/promtail-config.yaml:/etc/promtail/config.yaml
      - /var/log:/var/log:ro
    command: -config.file=/etc/promtail/config.yaml

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager/alertmanager.yml:/etc/alertmanager/config.yml
    command:
      - '--config.file=/etc/alertmanager/config.yml'
      - '--storage.path=/alertmanager'

volumes:
  prometheus_data:
  grafana_data:
  loki_data:
```

## Metrics Collection

### MCP Server Metrics
```python
# src/mcp_server/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info
import time
from typing import Dict, Any


class MCPMetrics:
    """Prometheus metrics for MCP servers."""

    def __init__(self):
        # Request metrics
        self.requests_total = Counter(
            'mcp_requests_total',
            'Total number of MCP requests',
            ['method', 'endpoint', 'status']
        )

        self.request_duration = Histogram(
            'mcp_request_duration_seconds',
            'Request duration in seconds',
            ['method', 'endpoint'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
        )

        # Tool metrics
        self.tool_executions_total = Counter(
            'mcp_tool_executions_total',
            'Total number of tool executions',
            ['tool_name', 'status']
        )

        self.tool_execution_duration = Histogram(
            'mcp_tool_execution_duration_seconds',
            'Tool execution duration in seconds',
            ['tool_name'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
        )

        # Resource metrics
        self.resources_total = Gauge(
            'mcp_resources_total',
            'Total number of MCP resources',
            ['resource_type']
        )

        # Health metrics
        self.health_status = Gauge(
            'mcp_health_status',
            'Health status of MCP server (1=healthy, 0=unhealthy)'
        )

        # Version info
        self.build_info = Info(
            'mcp_build_info',
            'Build information',
            ['version', 'commit', 'branch']
        )

    def record_request(self, method: str, endpoint: str, status: str, duration: float):
        """Record an API request."""
        self.requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        self.request_duration.labels(method=method, endpoint=endpoint).observe(duration)

    def record_tool_execution(self, tool_name: str, success: bool, duration: float):
        """Record a tool execution."""
        status = "success" if success else "failure"
        self.tool_executions_total.labels(tool_name=tool_name, status=status).inc()
        self.tool_execution_duration.labels(tool_name=tool_name).observe(duration)

    def set_resource_count(self, resource_type: str, count: int):
        """Set resource count."""
        self.resources_total.labels(resource_type=resource_type).set(count)

    def set_health_status(self, healthy: bool):
        """Set health status."""
        self.health_status.set(1 if healthy else 0)

    def set_build_info(self, version: str, commit: str, branch: str):
        """Set build information."""
        self.build_info.info({
            'version': version,
            'commit': commit,
            'branch': branch
        })


# Global metrics instance
metrics = MCPMetrics()
```

### Metrics Integration
```python
# src/mcp_server/api/metrics_endpoint.py
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from ..metrics import metrics

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint."""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    # Perform health checks
    is_healthy = await perform_health_checks()

    # Update metrics
    metrics.set_health_status(is_healthy)

    status_code = 200 if is_healthy else 503
    return {"status": "healthy" if is_healthy else "unhealthy"}, status_code

async def perform_health_checks() -> bool:
    """Perform comprehensive health checks."""
    checks = [
        check_database_connection(),
        check_external_services(),
        check_disk_space(),
        check_memory_usage()
    ]

    results = await asyncio.gather(*checks, return_exceptions=True)

    # All checks must pass
    return all(not isinstance(r, Exception) for r in results)
```

## Prometheus Configuration

### Service Discovery
```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'mcp-servers'
    scrape_interval: 5s
    static_configs:
      - targets:
        - 'mcp-server-1:8000'
        - 'mcp-server-2:8000'
    metrics_path: '/metrics'
    params:
      format: ['prometheus']

  - job_name: 'mcp-databases'
    scrape_interval: 30s
    static_configs:
      - targets:
        - 'postgres:9187'  # Postgres exporter
        - 'redis:9121'     # Redis exporter

  - job_name: 'system-metrics'
    scrape_interval: 15s
    static_configs:
      - targets:
        - 'node-exporter:9100'
```

### Alert Rules
```yaml
# monitoring/prometheus/alert_rules.yml
groups:
  - name: mcp-server-alerts
    rules:
      - alert: MCPServerDown
        expr: up{job="mcp-servers"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "MCP Server {{ $labels.instance }} is down"
          description: "MCP Server {{ $labels.instance }} has been down for more than 1 minute."

      - alert: MCPHighErrorRate
        expr: rate(mcp_requests_total{status=~"5.."}[5m]) / rate(mcp_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value | printf \"%.2f\" }}% for the last 5 minutes."

      - alert: MCPToolTimeout
        expr: histogram_quantile(0.95, rate(mcp_tool_execution_duration_seconds_bucket[5m])) > 30
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "MCP tool execution is slow"
          description: "95th percentile of tool execution duration is {{ $value }}s."

      - alert: MCPMemoryUsage
        expr: (1 - system_memory_available / system_memory_total) > 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85%."
```

## Grafana Dashboards

### MCP Server Overview Dashboard
```json
{
  "dashboard": {
    "title": "MCP Server Overview",
    "tags": ["mcp", "monitoring"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mcp_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(mcp_requests_total{status=~\"5..\"}[5m]) / rate(mcp_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      },
      {
        "title": "Tool Execution Duration",
        "type": "heatmap",
        "targets": [
          {
            "expr": "rate(mcp_tool_execution_duration_seconds_bucket[5m])",
            "legendFormat": "{{le}}"
          }
        ]
      },
      {
        "title": "Server Health",
        "type": "stat",
        "targets": [
          {
            "expr": "mcp_health_status",
            "legendFormat": "Health Status"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {
                "options": {
                  "1": {
                    "text": "Healthy",
                    "color": "green"
                  },
                  "0": {
                    "text": "Unhealthy",
                    "color": "red"
                  }
                },
                "type": "value"
              }
            ]
          }
        }
      }
    ]
  }
}
```

### Performance Dashboard
```json
{
  "dashboard": {
    "title": "MCP Performance Metrics",
    "panels": [
      {
        "title": "Response Time Percentiles",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.5, rate(mcp_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          },
          {
            "expr": "histogram_quantile(0.95, rate(mcp_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.99, rate(mcp_request_duration_seconds_bucket[5m]))",
            "legendFormat": "99th percentile"
          }
        ]
      },
      {
        "title": "Tool Performance",
        "type": "table",
        "targets": [
          {
            "expr": "rate(mcp_tool_execution_duration_seconds_sum[5m]) / rate(mcp_tool_execution_duration_seconds_count[5m])",
            "legendFormat": "{{tool_name}}"
          }
        ]
      }
    ]
  }
}
```

## Loki Log Aggregation

### Promtail Configuration
```yaml
# monitoring/promtail/promtail-config.yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: 'mcp-server-logs'
    static_configs:
      - targets:
        - localhost
        labels:
          job: mcp-server
          __path__: /var/log/mcp-server/*.log

  - job_name: 'system-logs'
    static_configs:
      - targets:
        - localhost
        labels:
          job: system
          __path__: /var/log/syslog

  - job_name: 'docker-logs'
    static_configs:
      - targets:
        - localhost
        labels:
          job: docker
          __path__: /var/lib/docker/containers/*/*-json.log
    pipeline_stages:
      - json:
          expressions:
            log: log
            stream: stream
            time: time
      - labels:
          stream:
      - timestamp:
          source: time
          format: RFC3339Nano
      - output:
          source: log
```

### Loki Configuration
```yaml
# monitoring/loki/local-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  instance_addr: 127.0.0.1
  path_prefix: /tmp/loki
  storage:
    filesystem:
      chunks_directory: /tmp/loki/chunks
      rules_directory: /tmp/loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

query_range:
  results_cache:
    cache:
      embedded_cache:
        enabled: true
        max_size_mb: 100

schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: index_
        period: 24h

ruler:
  alertmanager_url: http://alertmanager:9093
```

## Alert Management

### AlertManager Configuration
```yaml
# monitoring/alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@company.com'
  smtp_auth_username: 'alerts@company.com'
  smtp_auth_password: 'your-password'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'team-pager'
  routes:
  - match_re:
      severity: critical
    receiver: 'team-pager'
  - match_re:
      severity: warning
    receiver: 'team-email'

receivers:
- name: 'team-pager'
  pagerduty_configs:
  - service_key: 'your-pagerduty-key'

- name: 'team-email'
  email_configs:
  - to: 'team@company.com'
    from: 'alerts@company.com'
    smarthost: smtp.gmail.com:587
    auth_username: 'alerts@company.com'
    auth_password: 'your-password'
    require_tls: true
```

## Custom Dashboards and Alerts

### MCP-Specific Dashboards
- **Server Performance**: Request latency, throughput, error rates
- **Tool Analytics**: Most used tools, execution times, failure rates
- **Resource Usage**: Memory, CPU, disk usage trends
- **User Activity**: Authentication attempts, API usage patterns
- **Business Metrics**: MCP server adoption, user satisfaction

### Custom Alert Rules
```yaml
# Additional alert rules
groups:
  - name: mcp-business-alerts
    rules:
      - alert: LowMCPServerAdoption
        expr: mcp_active_users < 10
        for: 1h
        labels:
          severity: warning
        annotations:
          summary: "Low MCP server adoption"
          description: "Only {{ $value }} active users in the last hour."

      - alert: MCPToolFailureSpike
        expr: increase(mcp_tool_executions_total{status="failure"}[10m]) > 5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Spike in MCP tool failures"
          description: "{{ $value }} tool failures in the last 10 minutes."
```

## Integration with Development Workflow

### CI/CD Integration
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to staging
      run: |
        kubectl set image deployment/mcp-server mcp-server=${{ github.sha }}

    - name: Wait for rollout
      run: kubectl rollout status deployment/mcp-server

    - name: Run smoke tests
      run: |
        # Health check
        curl -f http://staging.mcp.company.com/health

        # Basic functionality test
        curl -f http://staging.mcp.company.com/api/tools

    - name: Update staging metrics
      run: |
        curl -X POST https://api.datadoghq.com/api/v1/events \
          -H "Content-Type: application/json" \
          -d '{
            "title": "MCP Server Deployed to Staging",
            "text": "Version ${{ github.sha }} deployed successfully",
            "tags": ["env:staging", "service:mcp-server"]
          }'
```

## Next Steps
After monitoring implementation, consider:
1. [Performance Optimization](./performance.md)
2. [Scaling Standards](./scaling.md)
3. [Incident Response](./incident-response.md)