# Using the unified monitoring stack

> **Stale content removed.** Use **[MONITORING_CURRENT_SETUP.md](./MONITORING_CURRENT_SETUP.md)** for ports, scrape targets, host logs, dashboards, and tool-call monitoring.

## 60-second start

```powershell
Set-Location D:\Dev\repos\mcp-central-docs\monitoring
pwsh -NoProfile -ExecutionPolicy Bypass -File .\start-unified-monitoring.ps1
```

Open http://localhost:12000 (Grafana, admin/admin).

## Wire a host MCP

1. **Metrics** — add job to `prometheus/prometheus.fleet.yml`, run `.\scripts\merge-prometheus-config.ps1`, restart prometheus.  
2. **Logs** — tee stdout to `logs/host/<job>/` via `.\scripts\Invoke-FleetLoggedCommand.ps1` (see [CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md)).  
3. **Dashboard** — add `grafana/dashboards/<repo>.json`, restart Grafana.  
4. **Per-tool visibility** — add `mcp_tool_calls_total` / `mcp_tool_duration_seconds` on `/metrics` (see [QUICK_START.md](./QUICK_START.md)); logs alone are not enough.

## Deep dives (optional)

- [CONNECT_TO_UNIFIED_MONITORING.md](./CONNECT_TO_UNIFIED_MONITORING.md)  
- [MCP_MONITORING_STANDARDS.md](./MCP_MONITORING_STANDARDS.md)  
- [UNIFIED_MONITORING_STACK.md](./UNIFIED_MONITORING_STACK.md) — architecture history  
