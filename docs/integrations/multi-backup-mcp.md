# Multi Backup MCP Integration

## Overview

Multi Backup MCP (multi-backup-mcp) is **FastMCP 3.1** compliant: Hasleo Backup Suite, repository archival (SOTA-pruned zips), Git/GitHub tools, and an **agentic workflow tool**. Single-backend: REST + MCP at `/mcp`.

**Repository**: [multi-backup-mcp](https://github.com/sandraschi/multi-backup-mcp)  
**Status**: Alpha  
**Framework**: FastMCP 3.1  
**Web**: FastAPI app at `multi_backup_mcp.server:app`; MCP at `/mcp` (e.g. port 10799).

## Capabilities

- **Hasleo Backup Suite**: System/disk/partition backups, scheduling, progress, restore.
- **Repository archival**: Pruned zips of dev repos (excludes node_modules, venv, etc.); multi-destination.
- **Git/GitHub**: Repo init, GitHub repo creation, push via GitHub CLI.
- **Agentic workflow** `backup_workflow`: One-call flows — `repo_archive`, `repo_to_github`, `hasleo_scheduled`.
- **Web**: FastAPI REST + MCP at `/mcp`; dashboard, API docs, health.

## ASGI / Web startup

Use:

- `uvicorn multi_backup_mcp.server:app --host 0.0.0.0 --port 10799`
- Or the project’s SOTA web stack (e.g. `Webapp`) which loads `multi_backup_mcp.server:app`.

## References

- [Multi Backup MCP README](https://github.com/sandraschi/multi-backup-mcp#readme)
- [MCP Central – WEBAPP_PORTS](../docs/operations/WEBAPP_PORTS.md) (port 10700–10800 range)

---

*Last updated: 2026-03; FastMCP 3.1; backup_workflow agentic tool; single-backend /mcp mount.*
