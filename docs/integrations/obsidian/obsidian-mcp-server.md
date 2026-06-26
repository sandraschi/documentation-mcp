# Obsidian MCP Server: The Agentic Control Layer

The Obsidian MCP server enables the Antigravity agent to read from and write to the local Obsidian vault via the Local REST API plugin.

## 🚀 Server Registration

```json
{
  "obsidian": {
    "command": "python",
    "args": ["-m", "obsidian_mcp.server"],
    "cwd": "D:/Dev/repos/obsidian-mcp",
    "env": {
      "OBSIDIAN_API_KEY": "${ENV:OBSIDIAN_REST_API_KEY}",
      "OBSIDIAN_VAULT_PATH": "D:/Dev/repos/sandras-vault"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `create_note` | Memory | Spawns a new markdown file with standardized YAML frontmatter. |
| `append_to_note` | Progress | Adds a new entry to an existing log or technical report. |
| `search_vault` | Retrieval | Executes a full-text search across all notes in the vault. |
| `get_recent_modified` | Telemetry | Identifies which files have been updated in the last 24 hours. |

## 📊 Interaction Principles

- **YAML Frontmatter**: Every note created by an agent MUST include a `created`, `updated`, and `author: Antigravity` field.
- **Link Integrity**: Agents should prioritize WikiLinks (`[[Note]]`) for internal connectivity.

---
*Last updated: 2026-02-14*
