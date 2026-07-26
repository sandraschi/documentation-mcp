# PlexMCP — status

**Last updated:** 2026-03-23  
**Source repo:** `D:\Dev\repos\plex-mcp` · [GitHub](https://github.com/sandraschi/plex-mcp)  
**Package:** `plex-mcp-advanced` · **Framework:** FastMCP **3.1+** · **Python:** **3.12+**  
**Product status:** **Alpha** (see upstream [CHANGELOG](https://github.com/sandraschi/plex-mcp/blob/main/CHANGELOG.md), [PRD](https://github.com/sandraschi/plex-mcp/blob/main/docs/PRD.md))

---

## Summary

PlexMCP is an MCP server for **Plex Media Server**: portmanteau tools for libraries, media, search, playlists, server health, optional ***arr** read-only status, **RAG** (`plex_rag`), and **agentic** / **natural assistant** flows with sampling. A **webapp** (FastAPI + Next.js) provides a browser UI; the same MCP app is mounted at **`/mcp`** on the backend.

---

## Health (high level)

| Area | Status | Notes |
|------|--------|--------|
| MCP / stdio | OK | `plex-mcp-advanced` entry point |
| Portmanteau tools | OK | See upstream [docs/TOOLS.md](https://github.com/sandraschi/plex-mcp/blob/main/docs/TOOLS.md) |
| Webapp | OK | Backend **10740**, frontend **10741** |
| RAG | Conditional | Requires LanceDB + optional mcp-central-docs `docs_mcp` on `PYTHONPATH` |
| Playback control | Limited | **Known issue:** remote play/pause not reliable for all clients (upstream CHANGELOG) |

---

## Documentation (upstream)

- [README.md](https://github.com/sandraschi/plex-mcp/blob/main/README.md) — short overview + doc table  
- [docs/README.md](https://github.com/sandraschi/plex-mcp/blob/main/docs/README.md) — hub  
- [docs/INSTALL.md](https://github.com/sandraschi/plex-mcp/blob/main/docs/INSTALL.md) — uv, PATH, PyPI when published  
- [docs/PRD.md](https://github.com/sandraschi/plex-mcp/blob/main/docs/PRD.md) — scope  

**Central mirror:** [README.md](./README.md) · [PRD.md](./PRD.md) · [CHANGELOG.md](./CHANGELOG.md)

---

## Ports (fleet)

| Service | Port |
|---------|------|
| Webapp backend | 10740 |
| Webapp frontend | 10741 |

See [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md).
