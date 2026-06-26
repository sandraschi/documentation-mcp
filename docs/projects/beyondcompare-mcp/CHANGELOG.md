# Changelog (fleet mirror)

**Source of truth:** `D:/Dev/repos/beyondcompare-mcp/CHANGELOG.md`

This copy exists for MCP Central Docs search and RAG. Edit the repo file first, then align this summary.

## [0.1.2] - 2026-04-24 (summary)

- **FastMCP 3.2.x** unified **FastAPI** gateway on port **10841** (REST + MCP `/mcp`).
- REST: **`GET /api/v1/health`**, **`GET /api/capabilities`**, **`GET /api/v1/logs`**, LLM/Ollama settings endpoints.
- MCP **prompts**, **`skill://beyondcompare-mcp/SKILL.md`**, **agentic** tools (`beyondcompare_agentic_workflow`, `beyondcompare_sampling_hint`).
- **`web_sota`** dashboard on **10840** with Vite proxy to the gateway; React Query–backed pages.
- Docs: **`docs/FLEET_GATEWAY.md`** in the repo; **`just test`**; **`tests/test_gateway.py`**.
- Legacy gold / mocked pytest modules **skipped** until refreshed for FastMCP 3.x introspection.

Prior releases: see upstream `CHANGELOG.md` in the repository.
