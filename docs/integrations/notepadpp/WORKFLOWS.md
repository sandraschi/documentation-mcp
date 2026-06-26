# Notepad++ Workflows: Rapid Text Manipulation

These workflows define the automated text processing patterns in the Sandra ecosystem.

## 📋 Workflow: "The Config Drift Detection"

Identifying changes in robot configuration files.

1.  **Retrieval**: Agent pulls the active `.yaml` config from a **Unitree** robot via SSH.
2.  **Comparison**: Agent opens the local "Golden Standard" config in Tab 1 and the remote config in Tab 2.
3.  **Visualization**: Agent triggers the `Compare` plugin via `npp_mcp`.
4.  **Reporting**: Agent highlights the differences to the user for final approval.

## 🔍 Workflow: "Pattern-Based Log Extraction"

Filtering massive logs for specific technical anomalies.

1.  **Ingestion**: Agent opens a 500MB log file in a new tab.
2.  **Extraction**: `notepadpp_mcp` applies a bookmark-based regex to find all `FATAL` and `CRITICAL` errors.
3.  **Synthesis**: Agent copies all bookmarked lines to a new "Audit Note.txt" tab.
4.  **Review**: The filtered result is presented to the user for analysis.

---
*Last updated: 2026-02-14*
