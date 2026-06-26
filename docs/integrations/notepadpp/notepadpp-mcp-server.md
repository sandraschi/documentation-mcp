# Notepad++ MCP Server: The Agentic Control Layer

The Notepad++ MCP server provides the Antigravity agent with a direct bridge to the Npp object model, enabling remote editing, tab management, and text manipulation.

## 🚀 Server Registration

```json
{
  "notepadpp": {
    "command": "python",
    "args": ["-m", "npp_mcp.server"],
    "cwd": "D:/Dev/repos/notepadpp-mcp",
    "env": {
      "NPP_PATH": "C:/Program Files/Notepad++/notepad++.exe"
    }
  }
}
```

## 🛠️ Tool Catalog

| Tool | Action | Use Case |
| :--- | :--- | :--- |
| `open_file_in_tab` | Visualization | Opens a specific file for the user to review. |
| `insert_text_at_cursor` | Editing | Injects code snippets or logs at the active cursor position. |
| `get_current_tab_content` | Retrieval | Reads the text currently being viewed by the user. |
| `apply_regex_replace` | Transformation | Batch cleans logs or reformats data across all open tabs. |

## 📊 Interaction Principles

- **Focus Non-Disturbance**: The agent should avoid switching tabs unless requested.
- **Safety**: Always create a backup of a file before performing a regex replace via `notepadpp_mcp`.

---
*Last updated: 2026-02-14*
