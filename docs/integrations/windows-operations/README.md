# Windows Operations: Low-Level OS Orchestration

The Windows Operations MCP provides a specialized bridge to Windows-specific APIs, enabling AI agents to manage system configurations, registry states, and shell integration for the **Windows 11 Pro** nodes in the fleet.

## ðŸš€ Deployment & API Support

### Infrastructure Core
- **Framework**: FastMCP 3.1.1+.4+ (SOTA).
- **Target OS**: Windows 11 Pro.
- **Dependencies**: `pywin32`, `winshell`, `psutil`.

### MCP Registration
```json
{
  "windows_ops": {
    "command": "python",
    "args": ["-m", "windows_ops.server"],
    "cwd": "D:/Dev/repos/windows-operations-mcp",
    "env": {
      "ELEVATION_POLICY": "require_user_confirm",
      "REGISTRY_ACCESS": "unrestricted"
    }
  }
}
```

## ðŸ–¥ï¸ System & Management Tools

### OS Configuration Tools
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `manage_registry` | Configuration | Read/Write/Delete operations for Windows Registry keys (e.g., Environment variables). |
| `control_services` | Management | Lifecycle control of Windows Services (Start, Stop, Restart). |
| `manage_shortcuts` | UI/UX | Automated creation or removal of desktop and start menu shortcuts for fleet apps. |

### Shell Integration
- **`empty_recycle_bin`**: Maintenance step during "Zen-Clean" functional simplicity cycles.
- **`get_system_uptime`**: Diagnostic metric for calculating fleet reliability scores.

## ðŸ› ï¸ Advanced SOTA Workflows

### The "SOTA Environment Optimizer"
Agents use the Windows Operations MCP to ensure the physical workstation remains optimized for high-performance development:
1. **Audit**: Agent checks registry for non-standard path configurations.
2. **Correct**: Agent uses `manage_registry` to align environment variables with the fleet's `AGENT_PROTOCOLS.md`.
3. **Notify**: Agent confirms the update to the user.

### Automated Workspace Setup
When creating a new MCP repository, the agent uses `manage_shortcuts` to add the project folder to the Windows Explorer "Quick Access" bar.

## ðŸ“Š Performance & Governance
- **Security**: Registry operations are audited and logged with a mandatory `REASON` field.
- **Elevation**: Certain operations require Administrative privileges; the server detects and prompts for elevation via the `pywinauto` bridge.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*

