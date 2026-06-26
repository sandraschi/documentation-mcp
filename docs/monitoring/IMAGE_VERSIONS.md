# Unified Monitoring Stack — Image Version Pins

> **Rule:** Never use `:latest` tags in production. Pin explicitly. Update deliberately.

## Current Versions

| Image | Tag | Released | Pulled |
|---|---|---|---|
| `grafana/grafana` | `13.0.1` | 2026-04-17 | 2026-04-28 |
| `grafana/loki` | `3.7.1` | 2026-03-26 | 2026-04-28 |
| `grafana/promtail` | `3.7.1` | 2026-03-26 | 2026-04-28 |
| `prom/prometheus` | `v3.11.3` | 2026-04-27 | 2026-04-28 |
| `prom/node-exporter` | `v1.9.1` | 2025 stable | 2026-04-28 |
| `gcr.io/cadvisor/cadvisor` | `v0.49.2` | 2025 stable | 2026-04-28 |

> **Promtail must always match Loki's minor version** (both `3.7.x`).

## How to Update

```powershell
# 1. Edit image tags in docker-compose.unified-monitoring.yml
# 2. Pull new images (no downtime yet)
docker compose -f docker-compose.unified-monitoring.yml pull

# 3. Recreate containers (~30s downtime on monitoring only)
docker compose -f docker-compose.unified-monitoring.yml up -d --force-recreate

# 4. Update the table above with new versions + pulled date
```

## Version History

| Date | Component | Old | New | Reason |
|---|---|---|---|---|
| 2026-04-28 | All | various `:latest` / `2.9.7` | See table above | Stale images after Docker Desktop reinstall; Loki was 2 major versions behind |
