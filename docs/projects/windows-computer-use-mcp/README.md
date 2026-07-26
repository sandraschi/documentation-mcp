# windows-computer-use-mcp (fleet note)

**Upstream repo:** `D:\Dev\repos\windows-computer-use-mcp` (formerly pywinauto-mcp)

Windows **desktop UI automation** via PyWinAuto. **High risk** — real cursor/keyboard; read upstream **`docs/SAFETY.md`** first. Pair with **virtualization-mcp** for Sandbox/VM isolation when you need disposable hosts.

**Version:** **0.5.4** (see upstream `pyproject.toml`). **FastMCP 3.2+** (`fastmcp>=3.2,<4`).

**Python:** 3.12+

## Tools (15 portmanteau + 2 opt-in)

| Tool | Description |
|------|-------------|
| `automation_windows` | Window lifecycle (list, find, focus, close, position) |
| `automation_elements` | UIA element interaction (click, type, list, wait) |
| `automation_mouse` | Mouse control (move, click, drag, scroll) |
| `automation_keyboard` | Keyboard input (type, hotkey, press) |
| `automation_visual` | Screenshots, OCR, template matching |
| `automation_assert` | UI verification (hash, diff, wait_stable, asserts) |
| `automation_dialog` | File dialog path entry |
| `automation_shortcut` | Semantic app shortcuts (VRoid, etc.) |
| `automation_task` | Closed-loop task runner with retry |
| `automation_system` | System utilities (clipboard, processes, host info) |
| `get_desktop_state` | Full desktop UI tree capture |
| `get_window_state` | Per-window snapshot with SOM/vision/ax modes |
| `analyze_winapp` | App crawler: UI tree + screenshots + element map + report. Shows CUA HUD. |
| `automation_face` (opt-in) | Face recognition |
| `global_keylogger` (opt-in) | Session keyboard capture. Shows CUA HUD. |

## CUA HUD

Long-running operations (`analyze_winapp`, `global_keylogger`) show a blinking red "CUA at work" overlay with e-stop button. Target window is auto-refocused before each action.

## Web dashboard (`web_sota`)

| Role | Port |
|------|------|
| Vite (frontend) | **10788** |
| FastAPI + MCP HTTP (backend) | **10789** |

**Start:** repo-root **`start.ps1`** or **`web_sota/start.ps1`**.
**New page:** `/crawler` — start crawls, view history, explore element tree.

## Cross-connection: autohotkey-mcp

| Need | Use |
|------|-----|
| UIA element tree, OCR, structured UI automation | windows-computer-use-mcp |
| Raw input recording/replay, hotkey macros | autohotkey-mcp |
| Both repos show "CUA at work" HUD during operations | |

## Cua Driver parity

- [CUA_DRIVER_AND_PYWINAUTO.md](../../patterns/CUA_DRIVER_AND_PYWINAUTO.md)
- Upstream roadmap: `windows-computer-use-mcp/docs/CUA_PARITY_ROADMAP.md` · operator: `docs/CUA_PARITY.md`

## Fleet safety docs

- [PYWINAUTO_MCP_SAFETY.md](../../patterns/PYWINAUTO_MCP_SAFETY.md)
- [WEBAPP_STANDARDS.md §7](../../standards/WEBAPP_STANDARDS.md)

## See also

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)
- [fleet.md](../fleet.md)
