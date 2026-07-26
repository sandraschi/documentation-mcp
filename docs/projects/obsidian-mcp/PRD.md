# Obsidian MCP — Product Requirements

## Executive summary

Obsidian MCP is a fleet knowledge server that exposes Obsidian vault operations to AI agents via FastMCP 3.2, with an optional FastAPI gateway and React dashboard for humans. It supports multi-vault management, LanceDB semantic search, canvas tooling, and live integration with Obsidian Desktop through the MCP Bridge plugin.

## Why now

- Fleet knowledge stack needs a vault-native MCP with stable ports (backend **10915**, frontend **10890**).
- Users want persistent vault configuration without hardcoded paths.
- RAG over all vaults aligns with mcp-central-docs LanceDB patterns used across the fleet.

## Goals

1. Programmatic vault CRUD, search, and link analysis for agents.
2. Semantic search (LanceDB) across all configured vaults.
3. Web dashboard for status, settings, vault browser, tools reference, and API docs.
4. MCPB bundle for Claude Desktop with prompts and lean staging build.

## Non-goals

- Replace Obsidian Desktop or sync engine.
- Host vault data in the cloud.
- Require Obsidian CLI for core file-vault operations.

## Architecture

| Layer | Technology | Notes |
|-------|------------|-------|
| MCP server | FastMCP 3.2, stdio/HTTP | `src/obsidian_mcp/server.py` |
| Gateway | FastAPI, port 10915 | REST for webapp; `/health`, `/api/*` |
| Webapp | React + Vite, port 10890 | Fleet SOTA layout, proxy to gateway |
| RAG | LanceDB + sentence-transformers | Global index under app data dir |
| Plugin | Obsidian MCP Bridge | Live insert-at-cursor, open-note URI |

## Tool surface

- **Vault**: list/create/read/update/delete/move notes
- **Search**: full-text, tags, wikilinks
- **Links**: backlinks, outlinks, orphans
- **Efficiency**: today's notes, quick capture, vault stats
- **Canvas**: list/read/create/edit/delete canvases (JSON Canvas 1.0)
- **RAG**: `rag_status`, `index_vault`, `semantic_search_vault`

## Fleet integration

- Registered in `fleet-webapp-manifest.json` (10915 / 10890).
- Launcher: `start.bat` delegates to self-contained `web_sota/start.ps1` (no external doc hub).
- MCPB: `scripts/build-mcpb.ps1` → `dist/obsidian-mcp-v{version}.mcpb`.

## Constraints

- Vault path stored in platform app settings (`%APPDATA%/obsidian-mcp` on Windows).
- `OBSIDIAN_VAULT_PATH` env overrides persisted settings.
- Gateway starts without vault; vault endpoints return 503 until configured.
- No secrets in repo; `.env` gitignored.

## Success metrics

- `uv run pytest` and `web_sota` lint/build/vitest/e2e pass in CI.
- `mcpb validate` + pack succeeds via `just mcpb-pack`.
- Dashboard loads all fleet routes; API proxy works without `VITE_API_URL`.
