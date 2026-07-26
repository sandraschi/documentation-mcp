# PlexMCP — project structure

**Last updated:** 2026-03-23  
**Source repo:** `D:\Dev\repos\plex-mcp`

---

## Layout (summary)

```
plex-mcp/
├── src/
│   └── plex_mcp/
│       ├── server.py              # FastMCP app, entry
│       ├── config/                # Settings / env
│       ├── models/                # Pydantic models
│       ├── services/              # Plex, RAG, sampling, etc.
│       └── tools/
│           └── portmanteau/       # plex_library, plex_* , plex_rag, arr_stack, …
├── webapp/
│   ├── backend/                   # FastAPI (10740), /api/*, /mcp mount
│   └── frontend/                  # Next.js (10741)
├── docs/                          # Hub: README.md, INSTALL, PRD, TOOLS, …
├── tests/
├── pyproject.toml
├── uv.lock
└── justfile
```

---

## Integration

- **MCP clients:** stdio via `uv run plex-mcp-advanced` (or equivalent).  
- **Browser:** webapp `start.ps1`; MCP also at `http://127.0.0.1:10740/mcp` when backend runs.  
- **RAG:** Optional dependency on mcp-central-docs **Python** package path (`docs_mcp.backend.rag_core`), not the MCP server process.

---

## Related

- Upstream: [docs/DEVELOPMENT.md](https://github.com/sandraschi/plex-mcp/blob/main/docs/DEVELOPMENT.md) — large layout edits belong in the repo; this mirror stays short.
