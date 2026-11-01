---
title: "OpenTelemetry Fleet Rollout"
category: pattern
status: draft
audience: mcp-dev
skill_candidate: false
related:
  - patterns/CONTAINER_ORCHESTRATION_STRATEGY.md
  - monitoring/docker-compose.unified-monitoring.yml
  - troubleshooting/BUGS_DEPOT.md
last_updated: 2026-07-12
---

# OpenTelemetry Fleet Rollout

**Status:** Phase 1-2 implemented (otel-collector + Tempo in stack, fleet_otel_bootstrap.py live). Phase 3 partial (winrar-mcp canary).
**Audit date:** 2026-07-12 (updated)
**Reference impl:** `observability-mcp` (partial — Prometheus export only)

---

## Current State

The fleet has **no operating OpenTelemetry pipeline**. An audit of 50+ repos found:

| Aspect | Status |
|--------|--------|
| OTel SDK as direct dependency | 1 repo (`observability-mcp`) |
| OTel SDK wired (TracerProvider + MeterProvider) | 1 repo (`observability-mcp`) |
| OTLP exporter configured | 0 repos |
| OTLP collector in monitoring stack | Not present |
| Defensive shims (prevent frozen-build crash, not use OTel) | 6 repos |
| `opentelemetry-instrument` CLI usage | 0 repos |

OTel dependencies exist fleet-wide because **FastMCP 3.2+ internally imports `opentelemetry.trace` and `opentelemetry.context`**. Every repo that builds a PyInstaller frozen binary must shim OTel to survive freezing. These shims are the artifact of a transitive dependency, not an observability strategy.

The unified monitoring stack (`monitoring/docker-compose.unified-monitoring.yml`) has Prometheus, Loki, Grafana, and Blackbox — but no OTel Collector. Prometheus scrapes a handful of `/metrics` endpoints directly; there is no trace ingestion, no span propagation, and no centralized OTLP gateway.

---

## Architecture

### Dual-Zone Frontpage

```
┌─────────────────────────────────────────────────────┐
│                  MCP Fleet (50+ servers)             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ arxiv-mcp    │  │ email-mcp   │  │ plex-mcp   │…│
│  │ (FastMCP)    │  │ (FastMCP)   │  │ (FastMCP)  │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                 │                 │        │
│         └─────────┬───────┴─────────┬───────┘        │
│                   │                 │                 │
│            OTLP gRPC/HTTP     OTLP gRPC/HTTP          │
└───────────────────┼─────────────────┼─────────────────┘
                    │                 │
         ┌──────────▼─────────────────▼──────────┐
         │     OTel Collector (otel-collector)    │
         │  :4317 (gRPC)  :4318 (HTTP)           │
         │                                        │
         │  Pipeline: traces → Loki (tempo)       │
         │            metrics → Prometheus         │
         └──────────┬──────────────────┬──────────┘
                    │                  │
         ┌──────────▼──┐    ┌─────────▼──────────┐
         │  Prometheus  │    │  Loki (+ Tempo)    │
         │  :12001      │    │  :12002            │
         └──────┬───────┘    └─────────┬──────────┘
                │                      │
         ┌──────▼──────────────────────▼──────┐
         │           Grafana :12000            │
         │  Zone 1: Engineering Telemetry      │
         │  - Real-time health grid            │
         │  - Latency spike detection          │
         │  - Tool call volume heatmaps        │
         │  - Cross-server trace waterfall     │
         └─────────────────────────────────────┘

         ┌─────────────────────────────────────┐
         │  Vite SPA Dashboard (separate port) │
         │  Zone 2: Human-Readable Directory    │
         │  - Server registry & status          │
         │  - Tool schema browser               │
         │  - Hourly-synced changelogs          │
         │  - LanceDB RAG search bar            │
         └─────────────────────────────────────┘
```

### Why OTel Instead of Direct Prometheus Scraping

| Concern | Prometheus-native (current) | OTel (proposed) |
|---------|----------------------------|-----------------|
| Traces | Not supported | Full span tracing |
| Metrics | Pull-only | Pull + push via OTLP |
| Cross-server context | None | Propagated via W3C traceparent |
| Overhead per server | Scrape interval | Gated by batch processor |
| One-time collector config | Per-server scrape job | Single OTLP endpoint env var |

The fleet's main gap is **trace context** — when `arxiv-mcp` calls `calibre-mcp` via the federation router, there is zero visibility into the request chain. OTel's W3C trace propagation fills this.

---

## Implementation Phases

### Phase 1: OTel Collector in Monitoring Stack

Add an `otel-collector` container to `docker-compose.unified-monitoring.yml`:

```yaml
otel-collector:
  image: otel/opentelemetry-collector-contrib:0.120.0
  container_name: unified-otel-collector
  ports:
    - "${UNIFIED_OTEL_HOST_PORT:-4317}:4317"   # gRPC
    - "${UNIFIED_OTEL_HTTP_PORT:-4318}:4318"   # HTTP
  volumes:
    - ./otel-collector/config.yml:/etc/otel-collector/config.yml:ro
  networks:
    - unified-monitoring
  restart: unless-stopped
```

Config (`monitoring/otel-collector/config.yml`):

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  attributes:
    actions:
      - key: fleet.cluster
        value: sandraschi-mcp
        action: upsert

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: mcp_fleet
    resource_to_telemetry_conversion:
      enabled: true
  otlp/loki:
    endpoint: loki:3100
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp/loki]
    metrics:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [otlp/loki]
```

Then add the OTel collector scrape target to `prometheus.yml`:

```yaml
- job_name: otel-collector
  static_configs:
    - targets: ["otel-collector:8889"]
      labels:
        app: opentelemetry
        service: fleet-collector
```

### Phase 2: Fleet-Wide OTel Bootstrap Module

Replace the 6 defensive shims with a single shared module. The module auto-detects whether an OTLP endpoint is configured; if not, it installs no-op providers (preserving frozen-build survival without the entry_points workaround).

**Add to `mcp-central-docs/scripts/fleet-otel-bootstrap.py`:**

```python
"""Fleet OTel bootstrap — single source of truth for all MCP servers.

Auto-detects OTEL_EXPORTER_OTLP_ENDPOINT. When set, configures real
TracerProvider + MeterProvider exporting to the collector. When unset,
installs no-op providers for frozen-build survival.

FastMCP 3.2+ internally imports opentelemetry.trace and opentelemetry.context.
Without this bootstrap, PyInstaller frozen binaries crash on import with
StopIteration from entry_points() discovery.

Usage:
    # In run_server.py, first import:
    import fleet_otel_bootstrap  # side-effect: configures OTel

    # Or via --runtime-hook in .spec:
    runtime_hooks=['scripts/fleet-otel-bootstrap.py']
"""

import os
import sys


def _bootstrap() -> None:
    otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")

    # Always set context propagation mode to contextvars (required for FastMCP)
    os.environ.setdefault("OTEL_PYTHON_CONTEXT", "contextvars_context")

    if not otel_endpoint:
        # Frozen build survival: inject no-op modules before FastMCP imports them
        import types

        _noop_modules = {
            "opentelemetry": types.ModuleType("opentelemetry"),
            "opentelemetry.trace": types.ModuleType("opentelemetry.trace"),
            "opentelemetry.context": types.ModuleType("opentelemetry.context"),
        }
        for name, mod in _noop_modules.items():
            if name not in sys.modules:
                sys.modules[name] = mod
        return

    # Real OTel pipeline
    service_name = os.environ.get("OTEL_SERVICE_NAME", "unknown-mcp")

    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    resource = Resource(attributes={SERVICE_NAME: service_name})
    tracer_provider = TracerProvider(resource=resource)
    span_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=f"{otel_endpoint}/v1/traces")
    )
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Metrics
    from opentelemetry import metrics
    from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
        OTLPMetricExporter,
    )
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{otel_endpoint}/v1/metrics"),
        export_interval_millis=15000,
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)


_bootstrap()
```

### Phase 3: Per-Server Wiring

Each MCP server that should export telemetry needs:

1. **Add deps to `pyproject.toml`:**
   ```toml
   [project.optional-dependencies]
   otel = [
       "opentelemetry-sdk>=1.28.0",
       "opentelemetry-exporter-otlp-proto-grpc>=1.28.0",
       "opentelemetry-api>=1.28.0",
   ]
   ```

2. **Import bootstrap in `run_server.py`:**
   ```python
   import fleet_otel_bootstrap  # noqa: F401
   ```

3. **Set env vars (in `start.ps1` or `.env`):**
   ```powershell
   $env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"
   $env:OTEL_SERVICE_NAME = "arxiv-mcp"
   ```

4. **Remove old defensive shims:**
   - Remove `hooks/runtime-opentelemetry.py` (if present)
   - Remove inline `sys.modules` stubs from `run_server.py`
   - Remove `opentelemetry-` from `_keep_dist` in `.spec` (no longer needed)

5. **Add FastMCP tracing (optional but recommended):**
   ```python
   from opentelemetry import trace

   tracer = trace.get_tracer(__name__)

   @mcp.tool()
   async def search_papers(query: str, ctx: Context) -> dict:
       with tracer.start_as_current_span("search_papers") as span:
           span.set_attribute("query", query)
           span.set_attribute("result_count", len(results))
           # ... tool logic
   ```

### Phase 4: Grafana Dashboards

Provision dashboards as JSON in `monitoring/grafana/dashboards/`:

| Dashboard | Purpose |
|-----------|---------|
| `fleet-health-grid.json` | Per-server status: 5xx rate, p99 latency, tool call volume, uptime |
| `fleet-traces.json` | Span waterfall explorer — cross-server request chains |
| `fleet-tool-usage.json` | Heatmap of tool call frequency by server and operation type |
| `fleet-errors.json` | Error rate spikes with trace context linking to the failing span |

The health grid is the primary "frontpage" — it should be the Grafana home dashboard.

### Phase 5: Vite SPA Documentation Directory

The second zone of the dual-zone frontpage: a lightweight **Vite + Tailwind** single-page app (per fleet standard) that:

- Lists all 50+ servers with current health status (polled from Prometheus or OTel metrics)
- Displays tool schemas synced hourly from each server's `/api/v1/diagnostics` endpoint
- Renders markdown changelogs from a cron-compiled JSON payload
- Has a LanceDB RAG search bar at the top for "which server handles X?"
- Is served behind Nginx on a dedicated internal port

This is the human-readable complement to Grafana's engineering-focused dashboard.

---

## Server Rollout Priority

| Phase | Servers | Rationale |
|-------|---------|-----------|
| 1 | `observability-mcp` | Already has SDK wired — add OTLP export |
| 2 | Federation router (`universal-actuator-mcp`, `fleet-agent-mcp`) | Trace propagation starts here |
| 3 | High-traffic servers (`arxiv-mcp`, `email-mcp`, `plex-mcp`, `calibre-mcp`) | Most tool call volume |
| 4 | Media servers (`jellyfin-mcp`, `godot-mcp`, `reaper-mcp`) | Latency-critical streaming |
| 5 | All remaining user-facing MCP servers | Bulk rollout |
| Skip | Infrastructure daemons (`depot-mcp`, `monitoring-mcp` stubs) | No end-user tool calls |

---

## Per-Repo Checklist

```markdown
- [ ] `pyproject.toml`: added `otel` optional deps (opentelemetry-sdk, exporter-otlp-proto-grpc)
- [ ] `run_server.py`: `import fleet_otel_bootstrap` as first import
- [ ] `start.ps1`: set `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_SERVICE_NAME`
- [ ] Removed old defensive shim (`hooks/runtime-opentelemetry.py` or inline stubs)
- [ ] `.spec` file: removed `opentelemetry-` from `_keep_dist` (no longer needed)
- [ ] Verify: `uv sync --extra otel && uv run python run_server.py`
- [ ] Verify: spans appear in Grafana Explore > Tempo
- [ ] Verify: metrics appear in Prometheus target list
```

---

## Anti-Patterns

- **Shim proliferation**: Do not create per-repo variants of the bootstrap. One module, one location.
- **OTEL_PYTHON_CONTEXT per-repo hacks**: Currently `aiwatcher-mcp`, `giskard-mcp`, `pywinauto-mcp`, `virtualization-mcp` each set this env var independently. The bootstrap sets it once.
- **Removing `opentelemetry-` from `_keep_dist` before the bootstrap is in place**: The spec `_keep_dist` entry is redundant once the bootstrap no-ops OTel on frozen builds without metadata. Only remove after the bootstrap lands.
- **Mixing Prometheus-native and OTel metrics on the same server**: Either a server exports a `/metrics` Prometheus endpoint OR OTLP, not both. The OTel collector proxies metrics to Prometheus.

---

## Reference

- [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)
- [FastMCP 3.2+ internal OTel dependency](https://github.com/jlowin/fastmcp) — transitive `opentelemetry.trace` import
- Current monitoring stack: `monitoring/docker-compose.unified-monitoring.yml`
- Current defensive shim pattern: `pywinauto-mcp/hooks/runtime-opentelemetry.py` (old — to be replaced)
