# pywinauto-mcp (fleet note)

**Upstream repo:** `D:\Dev\repos\pywinauto-mcp`

Windows **desktop UI automation** via PyWinAuto (and related paths). **High risk** — real cursor/keyboard; read upstream **`docs/SAFETY.md`** first. Pair with **virtualization-mcp** for Sandbox/VM isolation when you need disposable hosts.

**Version:** **0.4.2** (see upstream `pyproject.toml`). **FastMCP 3.2+** (`fastmcp>=3.2,<4`).

**Python:** 3.12+

## Web dashboard (`web_sota`)

| Role | Port |
|------|------|
| Vite (frontend) | **10788** |
| FastAPI + MCP HTTP (backend) | **10789** |

**Start:** repo-root **`start.ps1`** or **`web_sota/start.ps1`**. Scripts wait for the **API port** (or health) before Vite so the proxy does not hit **`ECONNREFUSED`** on cold **`uv run`**. See **[WEBAPP_STANDARDS.md](../../standards/WEBAPP_STANDARDS.md) §1.2**.

## Cua Driver parity

- [CUA_DRIVER_AND_PYWINAUTO.md](../../patterns/CUA_DRIVER_AND_PYWINAUTO.md) — comparison, Excel+Cursor FAQ, fleet-agent bridge
- Upstream roadmap: `pywinauto-mcp/docs/CUA_PARITY_ROADMAP.md` · operator: `docs/CUA_PARITY.md`
- New tools (Phase 1): **`get_window_state`**, `capture_mode`, `snapshot_id` + `element_index` on **`automation_elements`**

## Fleet safety docs

- [PYWINAUTO_MCP_SAFETY.md](../../patterns/PYWINAUTO_MCP_SAFETY.md)
- [WEBAPP_STANDARDS.md §7](../../standards/WEBAPP_STANDARDS.md) — do not mix desktop MCP with routine webapp verification chains

## See also

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)
- [fleet.md](../fleet.md)
