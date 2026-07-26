# Tailscale MCP

**Repo:** `tailscale-mcp` · FastMCP 3.1+ · Webapp **10820/10821** · v2.0.2
**Status:** Active. This page replaces a stale Feb-2026 draft that described tool names and config shapes not present in the actual codebase — everything below is verified against `src/tailscalemcp/` as of 2026-06-20.

---

## What it actually is

`tailscale-mcp` wraps the [Tailscale Admin API](https://tailscale.com/api) as MCP tools: device/user management, MagicDNS and network policy, Tailscale Services, monitoring, Funnel, Taildrop, backups, security audit, reporting, integrations, and an optional SEP-1577 agentic workflow tool. 24 public tool names total, organized as portmanteau tools (one tool, many `operation` values) rather than one tool per action — the fleet-standard pattern used to avoid tool-list explosion.

Feature concepts (Funnel vs. Taildrop vs. Services vs. Peer Relays — easy to confuse) are covered in depth in [`tailscale-mcp/docs/FEATURES.md`](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/FEATURES.md). This page is the fleet-integration overview; that doc is the feature reference.

## Real tool surface (24 public names)

Source of truth: `src/tailscalemcp/tools/mcp_tool_names.py`.

| Tool | Domain |
|---|---|
| `manage_tailnet_devices` | Devices, users, auth keys (Admin API) |
| `manage_tailnet_network` | DNS, MagicDNS, ACL-ish policy hooks, **Tailscale Services** |
| `monitor_tailnet` | Metrics, Prometheus text, health, Grafana export |
| `manage_taildrop` | Taildrop file transfers (still alpha upstream — see FEATURES.md) |
| `manage_funnel` | Funnel — public HTTPS exposure (still beta upstream) |
| `run_tailnet_security` | Device posture audit |
| `run_tailnet_automation` | Workflows, scripts, batch operations |
| `manage_tailnet_backups` | Config backup/restore/schedule |
| `analyze_tailnet_performance` | Latency, bandwidth, baseline, capacity |
| `generate_tailnet_reports` | Reports, exports, analytics |
| `manage_tailnet_integrations` | Webhooks, Slack/Discord/PagerDuty/Datadog |
| `manage_tailnet_invites` | Device and user invites |
| `manage_posture_attributes` | Device posture attribute CRUD |
| `manage_device_keys` | Key expiry, IP assignment |
| `manage_tailnet_logging` | Audit logs, network flow logs, log streaming |
| `manage_tailnet_webhooks` | Native Tailscale webhook management |
| `manage_tailnet_settings` | Tailnet-wide settings |
| `manage_tailnet_contacts` | Contact preferences |
| `get_help` | Structured help (overview, examples, troubleshooting, funnel, sampling) |
| `get_tailnet_status` | System status, optional Mermaid topology diagram |
| `summarize_partner_tailnets` | Members vs. shared users, devices by login |
| `get_lm_link` | LM Link (Tailscale + LM Studio remote local LLM) info/readiness |
| `run_agentic_tailnet_workflow` | SEP-1577 multi-step sampling with tools |
| `run_agentic_tailnet_workflow_sampling` | Deprecated alias for the above |

**Not yet a dedicated tool:** Peer Relays (GA Feb 2026) — configure via Tailscale CLI/admin console for now; see FEATURES.md for why this matters for hard-NAT scenarios.

## Credentials

```bash
TAILSCALE_API_KEY=tskey-api-...   # from https://login.tailscale.com/admin/settings/keys
TAILSCALE_TAILNET=your-tailnet-name
```

Loaded once via `python-dotenv` at process startup — **not** re-read per call. If a long-lived server process's key goes stale (rotated after the process started), tools return a structured 401 with `recovery_options` distinguishing "restart the process" from "the key on disk is actually bad" — see [`TRAPS_AND_PITFALLS.md` §6](../../standards/TRAPS_AND_PITFALLS.md#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error) for the full writeup and [`AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md`](../../operations/AUTH_ERROR_SURFACING_FLEET_ROLLOUT.md) for the fleet-wide rollout this repo is the reference implementation for.

## Architecture (actual, not aspirational)

```
src/tailscalemcp/
├── mcp_server.py          # TailscaleMCPServer — FastMCP instance, lifespan, manager init
├── server.py               # FastAPI mount for the webapp (separate process from stdio)
├── config.py                # TailscaleConfig (pydantic-settings) + load_dotenv
├── device_management.py    # AdvancedDeviceManager — device CRUD, backed by operations/devices.py
├── client/api_client.py    # TailscaleAPIClient — actual HTTP calls, 401/404/429 handling
├── operations/             # NetworkOperations, PolicyOperations, AuditOperations, KeyOperations, etc.
├── tools/                  # One file per portmanteau tool (device_tool.py, network_tool.py, ...)
│   ├── _base.py             # ToolContext — dependency bag passed to every register_*_tool()
│   ├── _helpers.py          # Shared logic incl. auth-error recovery (is_auth_error, build_auth_error_response)
│   ├── _tool_types.py       # Literal[...] operation enums per domain — the actual schema source
│   └── portmanteau_tools.py # Wires ToolContext + calls every register_*_tool()
├── funnel.py, taildrop.py, magic_dns.py, monitoring.py, grafana_dashboard.py
└── sampling.py              # TailscaleSamplingHandler for SEP-1577
```

**Important distinction this old page missed:** there are **two separate server processes** that can both be running simultaneously — a stdio-spawned instance (launched by Claude Desktop/Cursor/etc. per `claude_desktop_config.json`) and a webapp-mounted FastAPI instance (`server.py`, serving `/api/v1/*` + `/mcp`). Each has its own `TailscaleMCPServer()` instance with independently-loaded credentials. Restarting one does not refresh the other.

## Real MCP registration (Claude Desktop)

```json
{
  "mcpServers": {
    "tailscale-mcp": {
      "command": "uv",
      "args": ["--directory", "D:/Dev/repos/tailscale-mcp", "run", "tailscale-mcp"],
      "env": {
        "TAILSCALE_API_KEY": "tskey-api-...",
        "TAILSCALE_TAILNET": "your-tailnet-name"
      }
    }
  }
}
```

(The previous version of this page showed `python -m tailscale_mcp.server` with a `TAILNET_NAME` env var — neither matches the real package layout or env var name. Corrected above.)

## Webapp

React/Vite dashboard, dark glass-style layout. Pages include My tailnet (Mermaid topology), Partner tailnets, Funnels, Services, Settings, Tool Explorer, Logs (SSE live tail), Help (now includes a Funnel/Taildrop/Services/Peer Relays explainer card). Ports **10820** (frontend) / **10821** (backend), following fleet adjacency convention.

## Doc index

- [docs/FEATURES.md](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/FEATURES.md) — Funnel/Taildrop/Services/Peer Relays deep dive
- [docs/INSTALL.md](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/INSTALL.md)
- [docs/WHAT_IS_TAILSCALE.md](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/WHAT_IS_TAILSCALE.md)
- [docs/TAILSCALE_MCP_PORTMANTEAU_TOOLS.md](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/TAILSCALE_MCP_PORTMANTEAU_TOOLS.md) — operation-level reference
- This directory's [PORTMANTEAU_TOOLS.md](PORTMANTEAU_TOOLS.md) — fleet-side summary, refreshed 2026-06-20 to match real tool names

---

*Refreshed 2026-06-20 against the live `tailscale-mcp` codebase. Other files in this directory (`API_REFERENCE.md`, `BEST_PRACTICES.md`, `INTEGRATION_GUIDE.md`, `MCP_INTEGRATION.md`, `MONITORING_INTEGRATION.md`, `NETWORK_ARCHITECTURE.md`, `PERFORMANCE_OPTIMIZATION.md`, `SECURITY_GUIDE.md`, `SYNC_SUMMARY.md`, `TROUBLESHOOTING.md`) have not yet been re-verified against the current codebase — treat them with the same skepticism this page deserved before today.*
