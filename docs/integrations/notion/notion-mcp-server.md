# Notion MCP Server: The Agentic Control Layer (SOTA 2026)

The Notion MCP server is a high-performance, FastMCP 3.1 compliant orchestration layer designed for comprehensive Notion workspace management. It integrates structured data manipulation with an advanced RAG (Retrieval-Augmented Generation) pipeline using LanceDB.

## 🚀 Server Architecture & Registration

The server supports dual transport modes (Stdio and HTTP) and is fully optimized for the **Antigravity** environment.

### Registration Configuration
```json
{
  "mcpServers": {
    "notion-mcp": {
      "command": "uv",
      "args": ["run", "python", "server.py", "--http"],
      "cwd": "D:/Dev/repos/notion-mcp",
      "env": {
        "NOTION_TOKEN": "${ENV:NOTION_API_KEY}",
        "NOTION_VERSION": "2025-09-03",
        "LANCEDB_PATH": "./data/vector_db",
        "EMBEDDING_MODEL": "all-MiniLM-L6-v2"
      }
    }
  }
}
```

## 🧩 September 2025 API Transition (2025-09-03)
> [!IMPORTANT]
> Since version `2025-09-03`, Notion has transitioned from the **Database** primitive to **Data Sources**. 

- **Data Source IDs**: All tools requiring a workspace target now use `data_source_id`.
- **Parent Objects**: When creating database entries, the parent must be specified as `{"type": "data_source_id", "data_source_id": "..."}`.
- **Search Filters**: Search operations now filter by `value: "data_source"` instead of `value: "database"`.

## 🛠️ Advanced Tool Catalog (Portmanteau Design)

| Tool | Capability | SOTA Feature |
| :--- | :--- | :--- |
| `manage_notion_data` | **CRUD** | Consolidated operation handler for Data Sources and Pages. |
| `search_notion_knowledge` | **RAG** | Vector search powered by LanceDB across all indexed workspace content. |
| `sync_rag_index` | **Sync** | Context-aware indexing of blocks, pages, and data sources. |
| `query_data_source` | **Analytics** | High-speed retrieval of structured records with complex filters. |
| `orchestrate_automation` | **Agentic** | Triggers workspace-wide synchronization and reporting workflows. |

## 🧠 RAG & Local LLM Integration
The Notion MCP server features a local intelligence hub that:
1. **Discovers Local LLMs**: Auto-detects Ollama and LM Studio instances.
2. **Context Injection**: Automatically injects relevant Notion fragments into LLM prompts via the RAG pipeline.
3. **Telemetry Dashboard**: A SOTA 10810-range webapp providing real-time stats on workspace health and LLM availability.

## 📊 Operational Principles
- **Austrian Efficiency**: Minimum API calls, maximum data density.
- **Privacy First**: All vector embeddings and data caching remain local.
- **Safety Guard**: Schemas are immutable by default to prevent structural corruption.

---
*Last updated: 2026-03-07*
*Compliant with FastMCP 3.1 & Notion 2025-09-03 Standards*
