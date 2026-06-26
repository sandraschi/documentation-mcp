# WinRAR Archive Orchestration

The WinRAR MCP integration provides a specialized CLI bridge to the industry-standard compression engine, enabling AI agents to manage large-scale archival, synchronization, and secure extraction within the fleet's data grid.

## 🚀 Deployment & CLI Integration

### Engine Configuration
- **Binary**: `WinRAR.exe` / `Rar.exe` (Windows SOTA).
- **Format Standard**: `.rar` v5 (Maximum recovery protection) or `.zip` (Universal compat).
- **Core Function**: High-performance batch compression and encrypted archival.

### MCP Registration
```json
{
  "winrar": {
    "command": "python",
    "args": ["-m", "winrar_mcp.server"],
    "cwd": "D:/Dev/repos/winrar-mcp",
    "env": {
      "WINRAR_EXECUTABLE": "C:/Program Files/WinRAR/WinRAR.exe",
      "TEMP_ARCHIVE_DIR": "D:/Dev/repos/temp/archives"
    }
  }
}
```

## 📦 Archival & Security Tools

### Extraction & Compression
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `archive_files` | Execution | Batch compression of project directories with optional password protection. |
| `extract_archive` | Retrieval | Recursive extraction of RAR/ZIP assets into designated project subtrees. |
| `repair_archive` | Maintenance | Automated use of recovery records to fix corrupted project archives. |

### Data Integrity
- **`add_recovery_record`**: Essential SOTA step for long-term cold storage of the fleet's neural data.
- **`lock_archive`**: Prevent accidental modification of sensitive project logs.

## 🛠️ Advanced SOTA Workflows

### Automated Project Snapshots
Agents use the WinRAR MCP to create immutable project backups:
1. **Milestone**: Agent identifies a major project completion in `task.md`.
2. **Compress**: Agent creates a `[ProjectName]_SOTA_v12.1_Archive.rar` with a 3% recovery record.
3. **Store**: Agent moves the archive to the **30TB HDD array** for long-term persistence.

### Secure Log Distribution
For multi-node fleet synchronization, agents can create password-encrypted RAR volumes that are safe to transmit over Tailscale or public cloud bridges.

## 📊 Performance & Governance
- **Compression Level**: Default set to "Normal" for speed; "Best" for archiving inactive projects.
- **Thread Count**: Utilizes the 24-core Ryzen's multi-threading for rapid batch processing.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
