# Tailscale MCP — Portmanteau Tools (Fleet Reference)

**Refreshed:** 2026-06-20, against `tailscale-mcp` `src/tailscalemcp/tools/` directly. Previous version of this page (dated October 2025) described tool names like `tailscale_device`, `tailscale_security(operation="scan")`, and a generic `OperationRouter`/`TailscaleWorkflowComposer` pattern that don't exist anywhere in the actual codebase — that content has been replaced entirely rather than patched, since it would have been faster to write fiction around the real tools than to untangle which parts of the old page were salvageable.

For *what each Tailscale feature does* (Funnel vs. Taildrop vs. Services vs. Peer Relays), see [`tailscale-mcp/docs/FEATURES.md`](https://github.com/sandraschi/tailscale-mcp/blob/main/docs/FEATURES.md). This page covers *how the MCP tool surface is shaped* — the portmanteau pattern itself and the real operation enums.

---

## The actual pattern

Every tool takes an `operation: Literal[...]` parameter (a closed enum, not a free string — FastMCP 3.1+ derives the JSON Schema from the type annotation, so clients see the full set of valid values, not just prose). The enum source of truth is `src/tailscalemcp/tools/_tool_types.py`. A response always includes an `"operation"` key echoing back which sub-operation ran, plus operation-specific payload keys.

```python
# Real shape, from device_tool.py
@ctx.mcp.tool(name=MANAGE_TAILNET_DEVICES)
async def tailscale_device(
    operation: DeviceOperation,   # Literal["list", "get", "authorize", ...]
    device_id: str | None = None,
    name: str | None = None,
    # ... every parameter any operation in this domain might need
) -> dict[str, Any]:
    try:
        if operation == "list":
            ...
        elif operation == "get":
            ...
        # ...
        else:
            raise TailscaleMCPError(f"Unknown operation: {operation}")
    except Exception as e:
        # See the auth-error-recovery note below
        ...
```

Real tool function names are internal (`tailscale_device`, `tailscale_network`, etc.) — the **MCP name** exposed to clients is set via `@ctx.mcp.tool(name=...)` from constants in `mcp_tool_names.py`, and is verb-first without a redundant `tailscale_` prefix (the server is Tailscale-only, so the prefix would be noise). Don't write code or prompts assuming the Python function name is also the MCP tool name — they differ on purpose.

## Real operation enums by domain

Pulled directly from `_tool_types.py` — these are the actual `Literal[...]` values, not approximations.

### `manage_tailnet_devices` — `DeviceOperation`
`list`, `get`, `authorize`, `rename`, `tag`, `delete`, `search`, `stats`, `exit_node`, `subnet_router`, `user_list`, `user_details`, `auth_key_list`, `auth_key_create`, `auth_key_revoke`

### `manage_tailnet_network` — `NetworkOperation`
`dns_config`, `magic_dns`, `dns_record`, `resolve`, `search_domain`, `policy`, `stats`, `cache`, `services_list`, `services_get`, `services_create`, `services_update`, `services_delete`

(Note: Tailscale Services live inside this tool, not a separate one — easy to miss if you're looking for a `manage_services` tool that doesn't exist.)

### `monitor_tailnet` — `MonitorOperation`
`status`, `metrics`, `prometheus`, `topology`, `health`, `dashboard`, `export`

### `manage_taildrop` — `FileOperation`
`send`, `receive`, `list`, `cancel`, `status`, `stats`, `cleanup`

### `manage_funnel` — `FunnelOperation`
`funnel_enable`, `funnel_disable`, `funnel_status`, `funnel_list`, `funnel_certificate_info`

### `run_tailnet_security` — `SecurityOperation`
`audit` — that's the only one. The old page's `scan`, `compliance`, `threat_detect`, `ip_block`, `quarantine` operations were invented; the Tailscale Admin API has no endpoints for those, and the real tool's own docstring says so explicitly: *"Tailscale's Admin API provides no security scanning, compliance, quarantine, alert, or threat detection endpoints."*

### `run_tailnet_automation` — `AutomationOperation`
`workflow_create`, `workflow_execute`, `workflow_schedule`, `workflow_list`, `workflow_delete`, `script_execute`, `script_template`, `batch`, `dry_run`

### `manage_tailnet_backups` — `BackupOperation`
`backup_create`, `backup_restore`, `backup_schedule`, `backup_list`, `backup_delete`, `backup_test`, `restore_test`, `recovery_plan`

### `analyze_tailnet_performance` — `PerformanceOperation`
`latency`, `bandwidth`, `optimize`, `baseline`, `capacity`, `utilization`, `scaling`, `threshold`

### `generate_tailnet_reports` — `ReportingOperation`
`generate`, `usage`, `custom`, `schedule`, `export`, `analytics`, `behavior`, `security`, `template`

### `manage_tailnet_integrations` — `IntegrationOperation`
`webhook_create`, `webhook_test`, `webhook_list`, `webhook_delete`, `slack`, `discord`, `pagerduty`, `datadog`, `test`

### `manage_tailnet_invites` — device/user invite operations
Device: `list`, `create`, `get`, `delete`, `resend`, `accept`. User: `list`, `create`, `get`, `delete`, `resend` (no `accept` for user invites).

### `manage_posture_attributes` — `PostureAttributeOperation`
`get`, `set`, `delete`, `batch_update`

### `manage_device_keys` — `DeviceKeyOperation`
`expire`, `update_key_expiry`, `set_ip`

### `manage_tailnet_logging` — `LoggingOperation`
`configuration_audit_logs`, `network_flow_logs`, `stream_status`, `stream_config_get`, `stream_config_set`

### `manage_tailnet_webhooks` — `WebhookOperation`
`list`, `create`, `get`, `update`, `delete`, `rotate_secret`

### `manage_tailnet_settings` / `manage_tailnet_contacts`
Both just `get` / `update`.

## Real usage examples

```python
# List online devices only
manage_tailnet_devices(operation="list", online_only=True)

# Check Funnel status
manage_funnel(operation="funnel_status")

# Run a security audit on one device
run_tailnet_security(operation="audit", device_id="device-id-here")

# Get tailnet status with a Mermaid topology diagram
get_tailnet_status(component="overview", include_mermaid_diagram=True)

# SEP-1577 agentic workflow — server picks tools and executes them
run_agentic_tailnet_workflow(
    workflow_prompt="List all offline devices and check if any have pending posture issues",
    available_tools=["manage_tailnet_devices", "manage_posture_attributes"],
    max_iterations=5,
)
```

## Auth-error recovery (worth knowing if a tool 401s)

Every tool module's exception boundary distinguishes two causes of an HTTP 401 rather than collapsing them into a flat "Invalid API key" string: a genuinely bad/expired key, versus a long-running server process holding a stale key it cached at startup (the more common case in practice — see [`TRAPS_AND_PITFALLS.md` §6](../../standards/TRAPS_AND_PITFALLS.md#6-stale-in-process-api-credentials-surfacing-as-a-flat-invalid-api-key-error)). The response's `details.recovery_options` field tells you which is more likely and what to do about it, rather than making you guess.

## Where the real registration wiring lives

`src/tailscalemcp/tools/portmanteau_tools.py`'s `TailscalePortmanteauTools._register_tools()` calls every `register_*_tool(ctx)` function — that's the actual list of what's live, useful to check if this page or `mcp_tool_names.py` ever drift apart again.

---

*This page intentionally does not include generic "how to build a portmanteau tool" tutorial content (validator patterns, tool composition classes, generic router patterns) — that belongs in [`TOOL_DESIGN_STANDARDS.md`](../../standards/TOOL_DESIGN_STANDARDS.md) as a fleet-wide pattern, not duplicated per-integration with invented examples.*
