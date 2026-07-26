# getbooks-mcp — Proposed structure (when repo exists)

```
getbooks-mcp/
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── glama.json
├── justfile
├── src/
│   └── getbooks_mcp/
│       ├── __init__.py
│       ├── server.py          # FastMCP 3.1 + tools
│       ├── sources/
│       │   ├── gutenberg.py   # catalog API client
│       │   ├── openlibrary.py
│       │   ├── archive_org.py  # Internet Archive (optional v1)
│       │   └── registry.py    # source metadata + caps
│       └── models.py
├── tests/
├── web_sota/                  # optional dashboard (SOTA ports)
└── docs/
    └── PRD.md
```

**Last updated:** 2026-03-20
