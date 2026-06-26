# Edge & Chrome Bookmarks MCP

The Bookmarks MCP provides a direct bridge to the browser's bookmarking subsystem, enabling AI agents to manage research libraries, categorize technical resources, and synchronize curated links across the fleet.

## 🚀 Deployment & Browser Integration

### Environment Prerequisites
- **Browsers**: Microsoft Edge (Standard), Google Chrome (Secondary).
- **Strategy**: Direct reading of the `Bookmarks` JSON file in the User Profile directory.
- **Lock Management**: Handles "Browser in Use" states by reading shadowed copies of the database.

### MCP Registration
```json
{
  "bookmarks": {
    "command": "npx",
    "args": ["-y", "edge-bookmark-mcp-server"],
    "env": {
      "BOOKMARKS_PATH": "%LOCALAPPDATA%/Microsoft/Edge/User Data/Default/Bookmarks",
      "BROWSER_TYPE": "edge"
    }
  }
}
```

## 🔖 Library & Search Tools

### Bookmark Orchestration
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `list_bookmarks` | Discovery | Full recursive tree extraction of the browser's bookmark folders. |
| `search_bookmarks` | Retrieval | Keyword and URL-based search for technical reference material. |
| `create_bookmark` | Curation | Automated saving of high-priority research URLs to specialized folders. |

### Categorization
- **`move_bookmark`**: Reorganize research links based on project evolution (e.g., Move from "Inbox" to "Active Project").
- **`delete_bookmark`**: Cleanup of transient or obsolete links during "Zen-Clean" cycles.

## 🛠️ Advanced SOTA Patterns

### Automated Research Archiving
Agents use the Bookmarks MCP to maintain a persistent link library during deep research:
1. **Web Research**: Agent identifies 5 high-value technical articles.
2. **Archive**: Agent saves them to `Bookmarks/Research/2026/[ProjectName]`.
3. **Sync**: Cross-references these links in the **Obsidian** project note.

### Cross-Browser Synthesis
The server can be configured to merge bookmark trees from both Edge and Chrome, providing a unified link-layer for the agentic grid.

## 📊 Performance & Edge Cases
- **Sync Jitter**: Bookmark changes are reflected near-instantly upon file-save by the browser.
- **Large Libraries**: Optimized for trees exceeding 10,000 nodes using fast JSON parsing.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
