# tailscale-mcp — ToolBench alignment notes

**Upstream:** [sandraschi/tailscale-mcp](https://github.com/sandraschi/tailscale-mcp)  
**Example report:** [ToolBench — tailscale-mcp](https://toolbench.arcade.dev/tools/cmmiudisr04w1fqqwpdizyebc) (IDs may change if rescanned).

## Issues addressed (definition / protocol)

1. **Input schemas** — Central [`_tool_types.py`](https://github.com/sandraschi/tailscale-mcp/blob/main/src/tailscalemcp/tools/_tool_types.py) with `Literal` enums for every portmanteau `operation` and `Annotated` + `Field` for bounded integers (ports, TTL, iterations, etc.).
2. **Docstrings** — Expanded tool docstrings (especially **`manage_tailnet_devices`**) with **Returns** key overview and recovery guidance; help/status tightened.
3. **Verb-first MCP tool names** — Public MCP names no longer use the redundant `tailscale_` prefix; FastMCP `@mcp.tool(name=...)` maps to stable strings in [`mcp_tool_names.py`](https://github.com/sandraschi/tailscale-mcp/blob/main/src/tailscalemcp/tools/mcp_tool_names.py). **Breaking (v2.1.0):** clients must use the new names (see README / CHANGELOG in-repo).

## Name migration (v2.0.x → v2.1.0)

| Old MCP name | New MCP name |
|--------------|----------------|
| `tailscale_device` | `manage_tailnet_devices` |
| `tailscale_network` | `manage_tailnet_network` |
| `tailscale_monitor` | `monitor_tailnet` |
| `tailscale_file` | `manage_taildrop` |
| `tailscale_funnel` | `manage_funnel` |
| `tailscale_security` | `run_tailnet_security` |
| `tailscale_automation` | `run_tailnet_automation` |
| `tailscale_backup` | `manage_tailnet_backups` |
| `tailscale_performance` | `analyze_tailnet_performance` |
| `tailscale_reporting` | `generate_tailnet_reports` |
| `tailscale_integration` | `manage_tailnet_integrations` |
| `tailscale_help` | `get_help` |
| `tailscale_status` | `get_tailnet_status` |
| `tailscale_partner_tailnets` | `summarize_partner_tailnets` |
| `tailscale_lm_link` | `get_lm_link` |
| `tailscale_agentic_workflow` | `run_agentic_tailnet_workflow` |
| `tailscale_sampling` | `run_agentic_tailnet_workflow_sampling` (deprecated alias) |

## Remaining / benchmark conflicts

- **Portmanteau** — Still used for domain grouping; ToolBench may still prefer atomic tools. Mitigation: typed `operation` + schema + docs.
- **Supportability** — GitHub stars/releases are external; not a focus of in-repo fixes.

## Rescan

After release, request a **rescan** on ToolBench and update this doc with the new grade and date.
