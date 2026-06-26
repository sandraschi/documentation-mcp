# Monitoring Dockerized Fullstack Apps with Grafana / Prometheus / Loki / Promtail

**Updated:** 2025-11-11  
**Scope:** MyAI platform workflow & general containerized stacks

## Overview
Building reliable observability for Dockerized services requires a cohesive monitoring suite. Grafana renders dashboards, Prometheus scrapes metrics, Loki stores logs, and Promtail ships them. This guide distills the working patterns from MyAI’s monitoring stack alongside warnings about common pitfalls.

## Core Components
- **Prometheus**: Metrics collector. Expose service metrics over HTTP (`/metrics`), map host port (e.g., 9191) to container `9090`, and keep scrape configs in `monitoring/prometheus.yml`.
- **Grafana**: Dashboard and alerting UI. Bind to a predictable host port (MyAI uses `3100`) and provision dashboards via `monitoring/grafana/provisioning`.
- **Loki**: Log aggregation. For lightweight setups use `grafana/loki:2.9.x`; disable WAL or mount a writable volume to avoid `mkdir wal: permission denied`.
- **Promtail**: Log shipper. Point to Loki’s internal container DNS (e.g., `http://myai-loki:3100/loki/api/v1/push`). Tail host log directories (`./logs:/var/log:ro`) and the Docker socket when needed.

## Do’s
- **Pin Versions**: Lock Loki/Promtail to compatible releases (2.9.x) to avoid schema incompatibilities introduced in 3.x unless you upgrade storage to TSDB.
- **Reserve Ports**: Document reserved monitoring ports (e.g., 9191, 3100, 3199) in `.cursorrules`. Stop conflicting containers ahead of `docker compose up`.
- **Expose `/metrics`**: Ensure each service exports a Prometheus-compatible endpoint; verify with `curl` before enabling scrapes.
- **Define Health Checks**: Add Compose `healthcheck` entries or Dockerfile `HEALTHCHECK` commands for monitoring services (Grafana, Prometheus, Loki).
- **Use Named Volumes**: Persist Prometheus (`prometheus_data`), Grafana (`grafana_data`), Loki (`loki_data`) to avoid data loss and permission issues.
- **Provision Grafana**: Store JSON dashboards in source control and auto-provision them. Include panels for mock-mode gauges and container resource metrics.
- **Automate Readiness Checks**: Include `Invoke-WebRequest` or `curl` commands for `/ready` endpoints and a sample Prometheus query in release scripts.
- **Precommit Config Validation**:
  - `promtool check config monitoring/prometheus.yml`
  - `docker run --rm -v %cd%/monitoring/loki-config.yml:/etc/loki/local-config.yaml grafana/loki:2.9.8 -verify-config`
  - `yamllint monitoring/*.yml`

## Don’ts
- **Don’t rely on `latest` images**: Upstream changes can break config (e.g., Loki 3.x schema requirements). Pin versions and upgrade intentionally.
- **Don’t hardcode `localhost`**: Promtail should reference Loki by Compose service name; Prometheus should scrape container hostnames, not host ports.
- **Don’t leave WAL enabled without storage**: Either provide a volume mount (`/wal`) or disable the WAL feature (`wal.enabled: false`).
- **Don’t forget Docker network aliases**: Loki and Promtail must share the same network (e.g., `ai-network`) for DNS resolution.
- **Don’t ignore port collisions**: Use `Get-NetTCPConnection`/`docker ps` to identify existing services before deploying monitoring stack.

## Release Checklist
1. Stop conflicting demo containers using monitoring ports.
2. `docker compose up -d prometheus grafana loki promtail`.
3. Check Prometheus readiness: `http://localhost:9191/-/ready`.
4. Check Grafana: `http://<host>:3100/login`.
5. Wait for Loki readiness (`http://localhost:3199/ready`) – requires ~20 sec after start.
6. Confirm Promtail logs show successful pushes (no `no such host` errors).
7. Hit dashboard metrics: `curl http://localhost:3060/metrics` and verify mock-mode gauge.
8. Query Prometheus: `http://localhost:9191/api/v1/query?query=service_mock_mode`.
9. Open Grafana “Mock Mode Overview” panel and confirm data.

## Useful Panels & Dashboards
- **Mock Mode Table**: Prometheus query `service_mock_mode` with custom thresholds, linking to remediation docs.
- **Container Resource Panels**: For CPU/memory display, scrape cAdvisor or Node Exporter metrics if available.
- **Log Explorer**: Provide saved queries in Grafana Explore for each service (`{job=\"myai-platform\"}`).

## Troubleshooting
- **Port already allocated**: `Get-NetTCPConnection -LocalPort <port>` then `Stop-Process -Id <PID>` or `docker stop <container>`.
- **Loki schema errors**: Downgrade to 2.9.x or migrate to TSDB schema (v13) before re-enabling structured metadata.
- **Promtail DNS failure**: Ensure Compose service name matches (e.g., `myai-loki`) and containers share the same network.
- **Dashboard import errors**: Use environment variable `PYTHONPATH=/app:/myai` (or equivalent) when running FastAPI inside containers so shared libraries resolve.

## Reference Links
- Grafana provisioning docs: https://grafana.com/docs/grafana/latest/administration/provisioning/
- Loki configuration (2.x): https://grafana.com/docs/loki/latest/configuration/
- Promtail configuration: https://grafana.com/docs/loki/latest/clients/promtail/configuration/
- Prometheus configuration: https://prometheus.io/docs/prometheus/latest/configuration/configuration/

