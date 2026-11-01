# Fleet Frontpage / Internal Control Cockpit — Corrected Concept

**Date:** 2026-07-12
**Status:** CONCEPT — not yet started
**Tags:** [mcp-federation-hub, fleet-dashboard, architecture, concept, medium]
**Origin:** Assessment of a Gemini-generated proposal (three-pattern "SOTA Observability / Docs Directory / Live Client Cockpit" writeup). Broad strokes were right (local, dynamic, no public static hosting); specifics were wrong for this fleet. This doc is the corrected plan.

---

## 1. Corrections to the original proposal

| Claim in proposal | Reality |
|---|---|
| Fleet of "50+" servers behind "universal-actuator-mcp" | 145+ servers. `universal-actuator-mcp` **does exist** (Federation Gateway v1.1.0, RoboFang-scoped) — but the fleet-wide router this concept extends is **mcp-federation-hub**. Note: the fleet has FOUR overlapping orchestration layers (mcp-federation-hub, universal-actuator-mcp, robofang supervisor, fleet-agent-mcp/Fritz) — hierarchy decision needed, see FLEET_GAP_ANALYSIS_2026-07.md §8. |
| FastMCP OTel pipeline: OTLP → Prometheus/Loki → Grafana | FastMCP OTel is **trace-first** (OTel API, always-on instrumentation, no-op without SDK). Prometheus is pull-based and cannot scrape ephemeral stdio child processes. Correct shape: OTLP → collector → **Tempo/Jaeger**, metrics derived via spanmetrics connector. Loki needs a Windows log shipper (Alloy) — not worth it. |
| Generative UI is "FastMCP 3.3+, `@mcp.tool(app=True)`" | Prefab/GenerativeUI landed in **3.2** (prefab-ui >= 0.14.0). Decorator syntax in the proposal is wrong. Fleet already ships prefab cards (arxiv-mcp, winops). |
| Standing Grafana LGTM stack as primary frontpage | Sized for team production traffic. This fleet is solo, on-demand, mostly-dormant stdio servers. A 24/7 health grid would mostly show "not running" — correct but useless. |
| Next.js + Docker + Nginx docs SPA, hourly cron rebuild | Contradicts fleet standards. Frontends are **Vite + Tailwind + Bun**, served directly on WEBAPP_PORTS ports, no containers. Metadata changes on commit, not hourly — rebuild on git hook / on demand. |
| "Static frontpage with LanceDB search bar" | Internally contradictory — vector search needs a live API process. That process should be the federation hub, not a new sidecar. |

## 2. Core insight

**The backend for this already exists.** mcp-federation-hub already supervises HTTP backends and knows about the fleet. The frontpage is not a new system — it is three thin faces on the hub:

```
                          ┌─ Vite dashboard (human directory, WEBAPP_PORTS)
[145+ repos] ─ scan ──► [mcp-federation-hub] ── HTTP/JSON
                          │  - registry endpoint          └─ any other consumer
                          │  - health probe scheduler
                          │  - metadata compiler
                          │  - (opt) LanceDB search route
                          └─ MCP face: prefab status cards (in-chat cockpit)
```

## 3. Components

### 3.1 Hub extensions (mcp-federation-hub)

- **Registry endpoint** (`GET /registry`): server list with name, repo path, transport, port (from WEBAPP_PORTS.md), version, tool count, last-probe result. Compiled from repo scans + FLEET_INDEX.md.
- **Cold-start health probes**: for stdio servers, "health" means *starts cleanly*, not *is running*. Scheduled probe: launch → `initialize` → `tools/list` → clean exit. Record duration, tool count, pass/fail, stderr tail. FastMCP 3.2 startup probes are the hook. Run staggered (e.g. full fleet sweep nightly, or chunked N-per-hour) — never launch 145 processes at once.
- **Probe opt-out (DECIDED)**: servers with startup side effects (OBS, Resonite, robot control like yahboom-mcp/robofang, anything spawning Docker containers or touching hardware) must be excluded from automated probes. Mechanism: `"probe": false` flag in the repo's mcpb.json, plus a denylist in hub config as a safety net. Opted-out servers show "manual probe only" in the dashboard instead of a stale pass/fail.
- **Metadata compiler**: walks `D:\Dev\repos\`, extracts README frontmatter, tool schemas (from probe results), CHANGELOG_LATEST.md, mcpb.json version. Emits one `fleet-registry.json`. Trigger: on demand + git hook, **not** cron.
- **Optional LanceDB search route** (`GET /search?q=`): embed tool descriptions + README summaries; answers "which server handles X?". Pattern already proven in arxiv-mcp depot RAG.

### 3.2 Human directory (new thin frontend)

- Vite + Tailwind + Bun SPA per fleet frontend standard, one page:
  - health grid (last-probe status, not liveness),
  - server directory with tool listings and links to repo/GitHub/webapp port,
  - search bar hitting the hub search route,
  - changelog feed from CHANGELOG_LATEST.md aggregation.
- Served directly on a WEBAPP_PORTS-registered port. No Docker, no Nginx, no public exposure. Remote access via existing Tailscale.

### 3.3 In-chat cockpit (prefab)

- `fleet_status` portmanteau tool on the hub's MCP face (or tiny fleet-status-mcp) rendering prefab cards: fleet health summary, per-server drill-down, last probe failures. Same JSON source as the dashboard. Fleet already has the prefab card pattern — this is reuse, not new ground.

### 3.4 Telemetry (dev-time only, explicitly NOT standing infra)

- When debugging a specific server: `opentelemetry-instrument fastmcp run server.py` → **otel-desktop-viewer** (single binary, OTLP :4317, UI :8000) or Jaeger all-in-one in Docker.
- Justfile recipe candidate: `just trace` per repo to launch viewer + instrumented server.
- Revisit a standing Tempo/Grafana stack only if a real recurring need appears. Default answer: no.

## 4. Non-goals

- No public hosting (Cloudflare Pages, Tiiny Host, etc.) — internal only.
- No standing Prometheus/Loki/Grafana stack.
- No Docker/Nginx wrapping of the dashboard.
- No liveness monitoring of stdio servers (meaningless for on-demand child processes).

## 5. Build plan (AI-assisted, realistic)

| Phase | Scope | Effort |
|---|---|---|
| 1 | Hub: registry endpoint + metadata compiler (repo scan → fleet-registry.json) | 1 day |
| 2 | Hub: cold-start probe scheduler (chunked, SQLite-persisted results) | 1 day |
| 3 | Vite dashboard (grid, directory, changelog feed) | 1–2 days |
| 4 | Prefab `fleet_status` cards on hub MCP face | 0.5 day |
| 5 | Optional: LanceDB search route + dashboard search bar | 1 day |
| — | Dev-time tracing justfile recipe | 0.5 day, anytime |

Total core (1–4): **~4 days**. Search (5) is a bolt-on.

## 6. Open decisions

- Dashboard port: pick and register in `operations\WEBAPP_PORTS.md`.
- Probe cadence: nightly full sweep vs. chunked rolling (recommend chunked — 10–15 servers/hour avoids load spikes and gives fresher data).
- Where probe results persist: hub SQLite (recommended) vs. flat JSON.
- Whether `fleet_status` lives on the hub MCP face or a separate micro-server (recommend hub face — one less repo).
