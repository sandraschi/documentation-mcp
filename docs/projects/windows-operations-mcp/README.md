# windows-operations-mcp (fleet note)

**Upstream repo:** `D:\Dev\repos\windows-operations-mcp` | [GitHub](https://github.com/sandraschi/windows-operations-mcp)

Windows system control plane for MCP clients: portmanteau tools (services, event logs, performance, registry, accounts, network, apps, environment, automation, archives, JSON, permissions, command execution, etc.), **FastMCP 3.2** (sampling, prompts, **SkillsDirectoryProvider** `skill://…`, optional **prefab** UI with `[apps]` extra).

**Version:** Runtime reports **14.2.0** in `windows_operations_mcp.__version__`; `pyproject.toml` may show a patch line — treat **`__init__.py`** as the user-facing version string when they differ.

**Python:** 3.12+ | **Deps:** `fastmcp>=3.2,<4`, uv + hatchling, MCPB.

## Web dashboard (`web_sota`)

| Role | Port |
|------|------|
| FastAPI + MCP HTTP (backend) | **10748** |
| Vite (frontend) | **10749** |

**Start:** repo `web_sota/start.ps1` (or equivalent). Vite proxies `/api` to **10748**. Follow **[WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md) §1.2** (backend readiness before Vite where applicable).

## Detailed status

See **[STATUS.md](STATUS.md)** in this folder.

## See also

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — fleet port matrix
- [fleet.md](../fleet.md) — fleet table row
