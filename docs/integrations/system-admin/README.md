# System Admin: Fleet Health & Diagnostic Orchestration

The System Admin MCP is the primary telemetry and "Watchtower" server for the fleet. It provides high-resolution monitoring of hardware resources, process trees, and OS-level diagnostics for the **24-core AMD Ryzen** and **RTX 4090** node.

## ðŸš€ Deployment & Diagnostic Engine

### Infrastructure Focus
- **Framework**: FastMCP 3.1.1+.4+ (SOTA).
- **Telemetry**: Sub-second sampling of CPU, RAM, GPU, and Disk metrics.
- **Core Function**: Fleet observability and automated incident response.

### MCP Registration
```json
{
  "system_admin": {
    "command": "python",
    "args": ["-m", "system_admin_mcp.server"],
    "cwd": "D:/Dev/repos/system-admin-mcp",
    "env": {
      "LOG_RETENTION_DAYS": "30",
      "ALERT_THRESHOLD_CPU": "90",
      "ALERT_THRESHOLD_RAM": "95"
    }
  }
}
```

## ðŸ¥ Health & Telemetry Tools

### Hardware & Process Monitoring
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `get_health_snapshot` | Telemetry | Unified view of CPU load, Memory pressure, and Temp metrics. |
| `list_processes` | Analysis | Deep-dive into active tasks with parent-child relationship tracking. |
| `get_gpu_stats` | Performance | Real-time monitoring of the **RTX 4090** (Util, VRAM, Power). |

### Log & Diagnostic Analysis
- **`extract_system_logs`**: Filtered retrieval of Windows Event Logs or system-level journal entries.
- **`analyze_crashes`**: Automated investigation of process terminations or BSOD events.

## ðŸ› ï¸ Advanced SOTA Workflows

### The "SOTA Self-Healing" Grid
Agents use the System Admin MCP to maintain peak performance:
1. **Detection**: Agent notices a "Zombie" process hogging 100% of a Ryzen core.
2. **Intervention**: Agent uses `terminate_process` to clean up the noise.
3. **Verification**: Agent re-runs `get_health_snapshot` to confirm the fix (Zen-Clean).

### Resource-Aware Task Routing
The agent checks GPU utilization via `get_gpu_stats` before deciding whether to run a heavy **Blender** render or an **Ollama** 70B inference job locally or remotely.

## ðŸ“Š Governance & Security
- **Least Privilege**: Only authorized agentic identities can trigger process terminations.
- **Archive Policy**: Critical health telemetry is compressed and archived weekly via **WinRAR MCP**.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*

