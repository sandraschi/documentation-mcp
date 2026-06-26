# Database Operations MCP

**FastMCP 3.1** server for professional database and bookmark management on Windows. Supports MCP prompts and a bundled database-expert skill.

## ✨ Core Features

### 🗄️ Database Management
- **SQLite Specialized**: Optimization, schema analysis, and high-performance queries.
- **Windows App DBs**: Automated backup/restore for common Windows applications.
- **Full-Text Search**: Ranking and highlighting support.
- **Agentic Workflows**: Sampling-enabled sampling for complex query optimization.

### 🔖 Bookmark Management
- **Universal Interface**: Unified support for Firefox, Chrome, Edge, and Brave.
- **Cross-Browser Sync**: Automated synchronization between browser families.
- **Age Analysis**: Identification of "old" or "forgotten" bookmarks.
- **Tagging**: Automated tagging and organization strategies.

## 🛠️ Portmanteau Tools
- `db_connection`: Unified connection management.
- `db_operations`: Transactions, batching, and sampling.
- `db_schema`: Depth-oriented schema introspection.
- `browser_bookmarks`: Single interface for all installed browsers.
- `sync_bookmarks`: Logic-based cross-browser synchronization.
- `db_sampling_workflow`: Agentic orchestration for complex DB tasks.

## FastMCP 3.1: Prompts and skills

- **Prompt `database_expert`**: Call `get_prompt("database_expert", arguments={"focus": "general"|"sql"|"connections"|"export"})` to get instruction text to inject so the LLM acts as a database expert using this server's tools.
- **Skill `database-expert`**: Exposed as `skill://database-expert/SKILL.md`. Clients that support MCP resources can read it for the same expert guidance. Bundled in the server; no user install required.

See [FastMCP 3.1 Features](../../fastmcp/3.1-features.md) for framework docs.
