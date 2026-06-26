# Obsidian Workflows: Knowledge Synthesis

These workflows define the automated documentation patterns in the Sandra ecosystem.

## 🧠 Workflow: "The Automated Daily Review"

Synthesizing progress from disparate project logs.

1.  **Aggregation**: Agent uses `get_recent_modified` to identify active project files.
2.  **Summarization**: Agent reads the logs and generates a high-level summary.
3.  **Archiving**: `obsidian_mcp` creates a new note in the `daily-logs/` folder with the summary.
4.  **Linking**: The note is cross-linked to the relevant project master documents.

## 🏛️ Workflow: "Technical Debt Tracking"

Maintaining an up-to-date registry of system anomalies.

1.  **Discovery**: Agent finds a BUG or FIXME marker in the codebase.
2.  **Logging**: `obsidian_mcp` appends the issue to the central `Technical Debt` note.
3.  **Visualization**: Agent updates the Obsidian Canvas diagram to show the relationship between the debt and the affected module.

---
*Last updated: 2026-02-14*
