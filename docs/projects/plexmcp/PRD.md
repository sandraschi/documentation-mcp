# PlexMCP — product requirements (index)

**Mirror folder:** This `projects/plexmcp/` copy tracks the upstream repo for discovery in MCP Central Docs.

**Canonical PRD:** [docs/PRD.md in plex-mcp](https://github.com/sandraschi/plex-mcp/blob/main/docs/PRD.md) — or locally: `D:\Dev\repos\plex-mcp\docs\PRD.md`

**Snapshot (2026-03-23):**

- **Runtime:** FastMCP **3.1+**, Python **3.12+**, `plexapi`; **uv**-first install (`uv.exe` on PATH on Windows). **PyPI** one-liner documented only **after** package registration/publish.
- **MCP:** Portmanteau tools + `plex_rag`, optional `arr_stack`, `agentic_plex_workflow`, `plex_natural_assistant` (sampling env vars).
- **Webapp:** FastAPI **10740** + Next.js **10741**; MCP at **`/mcp`** on backend.
- **Gaps:** Remote **playback** not reliable across client types (see upstream CHANGELOG Known Issues).
