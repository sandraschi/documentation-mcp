# Tailscale Neural Network Orchestration

The Tailscale MCP provides a secure, encrypted overlay network for the entire fleet. It enables AI agents to monitor node connectivity, manage access controls, and orchestrate remote service discovery across the **AMD Ryzen**, **RTX 4090**, and remote Apple/Mobile nodes.

## 🚀 Deployment & Tailnet Integration

### Core Configuration
- **Software**: Tailscale v1.6x (SOTA).
- **Protocol**: WireGuard-based Mesh VPN.
- **Node Discovery**: Automated mapping of the fleet via the Tailscale API.

### MCP Registration
```json
{
  "tailscale": {
    "command": "python",
    "args": ["-m", "tailscale_mcp.server"],
    "cwd": "D:/Dev/repos/tailscale-mcp",
    "env": {
      "TAILSCALE_API_KEY": "tskey-auth-your-key",
      "TAILNET_NAME": "sandra-network.tailnet"
    }
  }
}
```

## 🌐 Network & Connectivity Tools

### Node Orchestration
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `list_nodes` | Discovery | Real-time status of all fleet members (Online/Offline/Last Seen). |
| `get_node_status` | Telemetry | Detailed IP, OS, and latency metrics for a specific Tailscale node. |
| `authorize_node` | Security | Automated approval of new fleet members (e.g., temporary robot nodes). |

### Service Discovery
- **`identify_services`**: Discover exposed MCP endpoints on remote nodes (HTTP/stdio).
- **`check_connectivity`**: End-to-end ping and throughput validation between Vienna Main and remote nodes.

## 🛠️ Advanced SOTA Workflows

### The "Global Fleet Bridge"
Agents use the Tailscale MCP to orchestrate work across physically separated hardware:
1. **Detection**: Agent notices the **RTX 4090** node is offline.
2. **Re-route**: Agent identifies an alternative **macOS** node via `list_nodes`.
3. **Execution**: Agent tunnels the task through the Tailscale overlay to the backup node.

### Secure File Transfers
Integrating with **Filesystem MCP**, agents can move multi-gigabyte project archives via `tailscale cp` patterns, ensuring zero-exposure to the public internet.

## 📊 Performance & Security
- **Latency**: WireGuard provides < 1ms overhead; optimal for real-time robotics telemetry.
- **ACLs**: Automated rotation and enforcement of Tailscale ACLs to ensure "Sandra-only" access.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
