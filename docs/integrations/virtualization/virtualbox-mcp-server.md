# VirtualBox MCP: The Agentic Control Layer

The VirtualBox MCP server provides a wrapper around the `VBoxManage` CLI, enabling programmatic VM lifecycle management.

## 🚀 Server Registration

```json
{
  "virtualbox": {
    "command": "python",
    "args": ["-m", "vbox_mcp.server"],
    "cwd": "D:/Dev/repos/vbox-mcp",
    "env": {
      "VBOX_PATH": "C:/Program Files/Oracle/VirtualBox/VBoxManage.exe"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `start_vm` | Orchestration | Powers on a specific VM ID (Headless or GUI). |
| `take_snapshot` | Backup | Creates a restorable state of the VM before a risky operation. |
| `clone_vm` | Scaling | Creates an identical copy of a pre-configured dev environment. |
| `get_guest_status` | Telemetry | Monitors heartbeat and IP address of the guest OS. |

## 📊 Interaction Principles

- **Headless Default**: Agents should prioritize `headless` mode to conserve GPU resources for **Unity3D**.
- **Snapshots**: A snapshot MUST be taken before executing any agent-authored system scripts inside the guest.

---
*Last updated: 2026-02-14*
