# Beyond Compare: Deep Differential Orchestration

The Beyond Compare MCP provides an industry-standard diffing and merging engine for the fleet. It enables AI agents to perform sub-byte file comparisons, directory synchronization, and three-way merging with surgical precision.

## 🚀 Deployment & Scripting

### Engine Configuration
- **Software**: Beyond Compare 4/5 (Studio Edition).
- **CLI Engine**: `BComp.exe` / `BCompare.exe`.
- **Scripting**: Utilizes Beyond Compare's internal `.bcscript` language for automated sync tasks.

### MCP Registration
```json
{
  "beyondcompare": {
    "command": "python",
    "args": ["-m", "beyondcompare_mcp.server"],
    "cwd": "D:/Dev/repos/beyondcompare-mcp",
    "env": {
      "BC_EXECUTABLE": "C:/Program Files/Beyond Compare 4/BCompare.exe",
      "SYNC_LOG_DIR": "D:/Dev/repos/logs/sync"
    }
  }
}
```

## 🔍 Differential & Sync Tools

### Comparison Ops
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `compare_files` | Analysis | Byte-for-byte differential analysis with syntax-aware highlighting. |
| `sync_directories` | Maintenance | Rule-based synchronization of local and remote repository clones. |
| `generate_report` | Documentation | Automated creation of HTML/Text diff reports for project audits. |

### Rule-Based Logic
- **`ignore_metadata`**: Compare code logic while ignoring timestamps and artifact metadata (essential for SOTA audits).
- **`filter_extensions`**: Targeted comparison of `.py`, `.ts`, or `.md` files while skipping compiled binaries.

## 🛠️ Advanced SOTA Workflows

### Repo-Divergence Audit
Agents use Beyond Compare to resolve complex "ahead/behind" branch states:
1. **Audit**: Agent detects divergence between local and upstream `clawdbot`.
2. **Analyze**: `compare_directories` identifies the exact files requiring manual intervention.
3. **Merge**: Agent triggers a graphical merge session for the user when automatic conflict resolution fails.

### Media Consistency Check
Beyond Compare can be used to verify integrity across the media fleet (Immich cluster ↔ Backup nodes) by comparing file sizes and spectral data.

## 📊 Integrity & Governance
- **Safety First**: Synchronization operations default to `dry-run` unless explicitly overridden.
- **Reporting**: Every sync task generates a timestamped log in the `SYNC_LOG_DIR`.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
