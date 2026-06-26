# OneNote MCP: Enterprise Knowledge Bridge

The OneNote MCP provides a localized and cloud-sync bridge to the Microsoft OneNote ecosystem. It enables AI agents to interact with notebook hierarchies, page contents, and rich-text media using the **Microsoft Graph API**.

## 🚀 Deployment & Auth Configuration

### Environment Setup
- **API Engine**: Microsoft Graph API (v1.0).
- **Authentication**: Azure AD / Entra ID Application (Client Secret + Scopes).
- **Scopes**: `Notes.Read.All`, `Notes.ReadWrite.All`.

### MCP Registration
```json
{
  "onenote": {
    "command": "python",
    "args": ["-m", "onenote_mcp.server"],
    "cwd": "D:/Dev/repos/onenote-mcp",
    "env": {
      "ONENOTE_CLIENT_ID": "your-azure-app-id",
      "ONENOTE_CLIENT_SECRET": "your-encrypted-secret",
      "ONENOTE_TENANT_ID": "common"
    }
  }
}
```

## 📓 Notebook & Page Orchestration

### Hierarchy & Content Tools
| Tool | Operation | Description |
| :--- | :--- | :--- |
| `list_notebooks` | Discovery | Recursive listing of notebooks, sections, and section groups. |
| `get_page_content` | Extraction | Retrieval of page HTML/Markdown for agentic synthesis. |
| `create_page` | Execution | High-fidelity page creation with support for table and image blocks. |

### Technical Ingestion
- **`search_notes`**: Global keyword search across all synced notebooks for research retrieval.
- **`update_page`**: Patching existing pages with new technical data or task updates.

## 🛠️ Advanced SOTA Workflows

### Cross-Ecosystem Sync
Agents use the OneNote MCP to bridge corporate knowledge with the local "Sandra Vault":
1. **Discover**: Agent finds relevant technical specs in a OneNote notebook.
2. **Transform**: Agent converts the content into SOTA-compliant markdown.
3. **Persist**: Agent writes the result to **Obsidian** or **Notion**.

### Automated Meeting Summaries
Integrating with **Email MCP** and **Reaper**, the agent can:
- Transcribe audio walkthroughs.
- Summarize the transcript.
- Automatically create a "Meeting Note" in a dedicated OneNote section.

## 📊 Performance & Rate Limiting
- **Sync Latency**: Expect 300ms-800ms for Graph API roundtrips.
- **Media Handling**: Large image/PDF attachments are processed asynchronously to prevent MCP timeout.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
