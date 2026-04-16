# STRUCTURE - NotionMCP

## Directory Layout

```text
notion-mcp/
├── notion_mcp/          # Core Python Package (SOTA)
│   ├── rag/             # RAG & Vector Search Logic
│   │   ├── orchestrator.py  # RAG Sync & Discovery
│   │   └── database.py      # LanceDB connectivity
│   ├── client.py        # Notion API Wrapper
│   └── tools/           # Modular MCP Tools
├── web_sota/            # Premium Web Dashboard
│   ├── src/             # React 19 Source Code
│   ├── start.ps1        # Port-aware startup script
│   └── start.bat        # Windows launcher
├── data/                # Local Persistence
│   └── lancedb/         # Vector Database Storage
├── server.py            # FastMCP 3.1 Entry Point
├── pyproject.toml       # SOTA 2026 Dependencies (UV)
└── .env                 # Environment Configuration
```

## Architectural Design

- **Decoupled RAG Core**: The RAG pipeline is separate from the MCP server logic to allow for independent scaling.
- **Dual Transport**: Supports both stdio (MCP) and HTTP (FastAPI) for flexible integration.
- **Async Lifespan**: Clean startup/shutdown cycles for database connections.
- **Fleet Alignment**: Port 10810/10811 reserved for the ecosystem.
