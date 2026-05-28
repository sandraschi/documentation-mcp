# documentation-mcp — Agent Guide

## Overview
Public MCP Documentation Server - Federated RAG for the MCP ecosystem

## Entry Points

- `uv run docs-mcp` → `docs_mcp.server:main`
- `uv run docs-mcp-ui` → `docs_mcp.starts_ui.asgi:main`

## Standards
- FastMCP 3.2+ portmanteau tool pattern — tools use `operation` enum param
- Responses: structured dicts with `success`, `message`, domain-specific fields
- Dual transport: stdio (Claude Desktop) + HTTP (`MCP_TRANSPORT=http`)
- See [mcp-central-docs](https://github.com/sandraschi/mcp-central-docs) for fleet-wide coding standards

## Key Files
- `README.md` — full documentation
- `pyproject.toml` — build config and entry points
- `CLAUDE.md` — Claude Code context (if present)
