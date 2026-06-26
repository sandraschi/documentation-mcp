# Cua Driver and pywinauto-mcp

**Status:** Architecture pattern  
**Last updated:** 2026-06-01  
**Audience:** Fleet operators, agent builders, pywinauto-mcp maintainers

**Upstream Cua docs:** [What is Cua Driver?](https://cua.ai/docs/cua-driver/guide/getting-started/introduction) · [Comparison (vendor)](https://cua.ai/docs/cua-driver/guide/getting-started/comparison) · [GitHub trycua/cua](https://github.com/trycua/cua)

**Fleet desktop finger:** [pywinauto-mcp](../projects/pywinauto-mcp/README.md) · [PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md) · [FLEET_COMPUTER_USE_MCP.md](./FLEET_COMPUTER_USE_MCP.md)

**Parity roadmap (implementation):** `D:\Dev\repos\pywinauto-mcp\docs\CUA_PARITY_ROADMAP.md`

---

## What Cua Driver is

Cua Driver is an **MIT-licensed, host-native computer-use driver** from [trycua/cua](https://github.com/trycua/cua). It ships as a **single binary** (`cua-driver`) that can run as:

- MCP server over **stdio**
- Long-running **daemon** (Windows: interactive session via named pipe; avoids Session 0)
- One-shot **CLI** (same tools as MCP)

It targets **macOS** and **Windows** as released platforms; **Linux** is pre-release (AT-SPI + X11/XWayland; native Wayland-only apps are out of scope).

Core product promise: the **no-foreground contract** — the user's frontmost app, real cursor position, z-order, and macOS Space should **not** change because the agent clicked, typed, or re-snapshotted. Background drive is the default, not a special mode.

---

## Agent loop (Cua)

Stable tool names across OS backends:

1. `list_windows` — discover targets
2. `get_window_state` — observe (`pid`, `window_id`, optional `capture_mode`)
3. `click` / `type_text` / `hotkey` — act using **`element_index`** from the last snapshot
4. Re-snapshot to verify

Example (from Cua docs):

```text
cua-driver launch_app '{"bundle_id":"com.apple.calculator"}'
cua-driver get_window_state '{"pid":844,"window_id":10725}'
cua-driver click '{"pid":844,"window_id":10725,"element_index":14}'
```

### Capture modalities (`capture_mode`)

| Mode | Returns | When to use |
|------|---------|-------------|
| `som` (default) | Accessibility tree **plus** annotated screenshot (set-of-mark) | Labels repeat or are empty; vision disambiguation |
| `ax` | Tree only | Structured loops; no screen-recording cost |
| `vision` | Window image only | Vision-first models; no `element_index` path |

Configuration: `cua-driver config set capture_mode som`.

### Dispatch (Windows blog / comparison)

Default **`background`**: UIA + `PostMessage` where possible; returns **`background_unavailable`** instead of silently stealing focus. Caller may opt into **`dispatch: "foreground"`** per action for canvas/game/Electron edge cases.

Agent cursor: optional **overlay** cursor (click-through layered window) so the **physical** pointer stays where the user left it.

---

## What pywinauto-mcp is (fleet)

**pywinauto-mcp** is Sandra's **FastMCP 3.2+** Windows UI server: portmanteau tools (`automation_windows`, `automation_elements`, …), **`get_desktop_state`**, optional webapp **10788/10789**, and a **strong safety layer** (HITL, kill switch, dry-run, rate limits) documented in [PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md).

Historical default: **foreground-first** — [OPERATOR_PROTOCOL](file:///D:/Dev/repos/pywinauto-mcp/docs/OPERATOR_PROTOCOL.md) tells the human to keep the target app focused because PyWinAuto historically moves the **real cursor** and activates windows for screenshots.

---

## Side-by-side comparison

| Dimension | Cua Driver | pywinauto-mcp (fleet) |
|-----------|------------|------------------------|
| **License** | MIT (Rust binary) | MIT (Python / PyWinAuto) |
| **Transport** | stdio MCP + CLI + daemon | stdio + HTTP `/mcp` (10789) |
| **Host vs VM** | Real host only | Real host; pair with **virtualization-mcp** for Sandbox |
| **Focus model** | No-foreground **default** | Foreground **default**; Cua-style modes **opt-in** (parity roadmap) |
| **Discovery** | `get_window_state(pid, window_id)` | `get_desktop_state` (whole desktop) → **`get_window_state`** (scoped, parity) |
| **Element addressing** | `element_index` from snapshot | `control_id` / `auto_id` / coords → **`element_index` + `snapshot_id`** (parity) |
| **Vision** | `som` / `ax` / `vision` | `use_vision` / `use_ocr` → **`capture_mode`** (parity) |
| **Safety** | Light in intro; host trust | HITL, kill switch, dry-run, fleet IDE warnings |
| **Extras** | Trajectory capture, Claude CU compat | OCR, template match, webapp, `automation_mission`, face/keylogger opt-in |
| **Excel + IDE scenario** | **Design target** (background UIA) | **Partial** after parity Phase 1–2; not guaranteed for all controls |

Neither replaces **browser MCP** for DOM work. Neither replaces **winops** / **windows-operations-mcp** for OS admin.

---

## “Excel while I work in Cursor” — what is actually true?

### Same machine, same session (typical)

Both products run on **your real Windows desktop session**. You do **not** need a second physical monitor for the concept to apply.

- **Cua (intent):** Agent drives Excel (or any HWND) **in the background** while Cursor stays frontmost. Your **real mouse** should not jump; Excel does not need to become the foreground window for every click.
- **pywinauto-mcp (today → parity):** Default behavior still **can** steal focus and move the **physical** cursor. After parity work, set **`PYWINAUTO_MCP_DISPATCH=background`** and use **`get_window_state` → `element_index` click** for the Cua-shaped loop — with the same caveats as Cua (some apps only accept foreground input).

### Virtual / second monitor?

- **Not required.** A second monitor helps **you** see Excel while Cursor is on another display; the agent does not need a “virtual screen” product feature.
- **Windows Virtual Desktops:** Cua explicitly avoids dragging your **current desktop/Space** to follow the target. pywinauto does not replicate that yet; treat cross-desktop behavior as **undefined** until tested.
- **Windows Sandbox / VM:** That is **isolation**, not background drive on the host. Use **virtualization-mcp** + guest-side automation — see [PYWINAUTO_MCP_SAFETY.md § Sandboxed execution](./PYWINAUTO_MCP_SAFETY.md).

### Excel specifically

Office UIA coverage is generally good for ribbons and many dialogs, but:

- Some interactions still need **foreground** (`dispatch: foreground` in Cua terms).
- **Protected view**, modal dialogs, and GPU-heavy views may fail background dispatch.
- Fleet rule: keep **pywinauto out of default IDE MCP chains** for web work; use a **dedicated computer-use profile** when driving Excel alongside Cursor ([WEBAPP_STANDARDS §7](../standards/WEBAPP_STANDARDS.md#7-mcp-capability-boundaries-web-vs-desktop-ui)).

---

## Cross-connect with fleet-agent-mcp

**Yes — already wired at the registry level.**

[fleet-agent-mcp](file:///D:/Dev/repos/fleet-agent-mcp) exposes **`fleet_bridge`** tools that call other fleet MCP servers over Streamable HTTP. The built-in registry includes:

| Alias | URL | Role |
|-------|-----|------|
| `pywinauto` | `http://127.0.0.1:10788/mcp` | Windows UI automation |

Typical orchestration:

1. **Lumen** (fleet-agent) plans a coworker task (“refresh Excel pivot”, “click through installer”).
2. **`fleet_bridge_call`** (or equivalent) targets server **`pywinauto`**, tool **`get_window_state`** / **`automation_elements`**.
3. Results return to fleet memory / task state; optional **`docs`** server for MCD search.

Requirements:

- **pywinauto-mcp** running with HTTP transport on **10789** (webapp `start.ps1` or `just serve`).
- Fleet agent config must not block automation category tools for that workflow.
- Same **safety** rules: fleet-agent amplification + pywinauto = [PYWINAUTO_MCP_SAFETY](./PYWINAUTO_MCP_SAFETY.md) + [FLEET_COMPUTER_USE_MCP](./FLEET_COMPUTER_USE_MCP.md).

**Cua Driver is not in `FLEET_SERVERS` today.** Options:

- Run **`cua-driver mcp`** as a **separate** stdio MCP server in Cursor (alongside pywinauto), or
- Add a fleet-bridge entry after you standardize port/HTTP for Cua (if upstream exposes streamable HTTP).

For Sandra's fleet, **pywinauto parity** is the preferred integration surface (one safety model, one webapp, existing bridge alias).

---

## When to use which

| Choose **Cua Driver** | Choose **pywinauto-mcp** |
|----------------------|---------------------------|
| You want upstream **Rust** driver and Cua ecosystem (bench, sandbox products) | You want **fleet safety**, HITL, HTTP bridge, webapp |
| macOS + Windows binary install is fine | Python/uv fleet workflow already standard |
| Experimenting with vendor **no-foreground** contract on host | Production **OpenManus / fleet-agent** delegation to `pywinauto` alias |
| No need for OCR/template/HITL extras | Need **OCR**, **find_image**, **virtualization-mcp** pairing |

Running **both** on the same host session is possible but **redundant and risky** unless profiles are separated (different MCP configs, kill switches, explicit target HWND).

---

## Parity program (pywinauto-mcp)

Implementation tracking: **`pywinauto-mcp/docs/CUA_PARITY_ROADMAP.md`**.

| Phase | Deliverable | Status |
|-------|-------------|--------|
| **1** | `capture_mode`, `get_window_state`, `snapshot_id` + `element_index`, `PYWINAUTO_MCP_DISPATCH` | Done (pywinauto-mcp) |
| **2** | `background_unavailable`, no foreground on read paths, window-scoped capture, `OFFICE_BACKGROUND_MATRIX.md` | Done |
| **3** | Trajectory JSONL, `pywinauto-mcp mcp-config`, fleet-agent [pywinauto-cua-loop.md](file:///D:/Dev/repos/fleet-agent-mcp/docs/pywinauto-cua-loop.md) | Done |
| **4** | Agent overlay, PostMessage clicks, `cua_computer_use_screenshot` | Done |
| **E2E** | LibreOffice Calc loop (`pytest -m e2e`) — pairs with **libreoffice-mcp** | Done |

Run e2e: `cd pywinauto-mcp; uv run pytest -m e2e -v --no-cov`

---

## Related

- [integrations/cua-driver.md](../integrations/cua-driver.md) — short hub link
- [FLEET_COMPUTER_USE_MCP.md](./FLEET_COMPUTER_USE_MCP.md)
- [PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md)

*Tags: #cua-driver #pywinauto #computer-use #fleet-agent #background-automation*
