# Fleet “Computer Use” via MCP (OpenManus + pywinauto)

**Status:** Architecture pattern · **Last updated:** 2026-03-21  
**Audience:** Fleet architects, OpenManus / openmanus-mcp operators

> [!CAUTION]
> **Amplification:** **windows-computer-use-mcp** is **uniquely dangerous** among MCP servers (host-wide Win32 / pyautogui, not a tab sandbox). **OpenManus** + **sampling** + **openmanus-mcp** (bridge) + **OpenClaw / Manus-class** autonomy narratives = **multiplicative** risk. Vendor products add **extra guardrails** we do not replicate. Read **[PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md)** § *OpenManus, openmanus-mcp, OpenClaw, Manus-class* before composing this stack.

---

## Intent

Replicate the **desktop agent** narrative of vendor products (e.g. Meta / Manus **“My Computer”**): an LLM-driven loop that **observes and acts on the local machine** — without shipping a closed binary or a mandatory cloud “how to” tier.

**Our substrate:** any MCP-capable orchestrator (especially **OpenManus** with `config/mcp.json`) + **this fleet’s MCP servers**.

---

## IDE / webapp work: do **not** keep pywinauto in the MCP chain

**windows-computer-use-mcp** is **Win32 desktop UI automation** (clicks/type/focus on *whatever window* matches). It is **not** a browser sandbox. If it is enabled alongside **Cursor**, **Antigravity**, **VS Code**, or any **Webapp** / Vite dashboard workflow, the model may **choose** it for “click on UI” tasks — including when the intent was **in-browser** verification only.

**Observed failure mode:** runaway **OS-level** input (wrong focused window → IDE chrome, loops, **phantom cursor**, session takeover). This is **predictable** once the tool exists in the union of capabilities.

**Fleet rule:**

| Context | windows-computer-use-mcp |
|--------|----------------|
| **Default IDE MCP config** (daily dev, webapp verification, Antigravity) | **OFF / removed** — use **browser MCP** (Playwright, **cursor-ide-browser**, etc.) only. |
| **Dedicated “computer use”** session (OpenManus, explicit desktop automation) | **ON** only when **isolated** (VM, spare user, or non-production host) and with mitigations below. |

Treat pywinauto in a **Kinderzimmer** IDE chain like a **hand grenade** in a toy box: **don’t leave it there.**

---

## Role split (recommended)

| Layer | Fleet component | Role |
|--------|-----------------|------|
| **Brain** | OpenManus (local LLM in `config.toml`) + optional **openmanus-mcp** | Planning, tool choice, memory, guardrails |
| **Finger (Win32 UI)** | **[windows-computer-use-mcp](../projects/windows-computer-use-mcp/README.md)** | Click, type, focus windows, traverse controls, visual/OCR-style ops via portmanteau tools — **primary “clicker/scraper”** for apps without APIs |
| **OS / shell** | **windows-operations-mcp**, **winops**, **system-admin-mcp** (as needed) | Services, processes, filesystem edges outside a single HWND tree |
| **Pixels / documents** | **ocr-mcp**, capture pipelines | When UI automation needs text from arbitrary bitmaps or PDFs |
| **Browser** | OpenManus **BrowserUseTool** / Playwright, or dedicated browser MCP | Web vs native Win32 — different failure modes |

Compose these by **attaching servers in OpenManus** `config/mcp.json` (same model as Claude Desktop).

---

## Why windows-computer-use-mcp is the default “finger”

- **Deep Win32 coverage** for legacy and proprietary UIs (DAWs, CAD, internal tools).
- Already **fleet-standard**: portmanteau design, webapp **10788 / 10789** per [WEBAPP_PORTS](../operations/WEBAPP_PORTS.md).
- Pairs naturally with **OpenManus** `AskHuman` and step caps for **human-in-the-loop** on risky branches.

---

## Danger profile (non-negotiable honesty)

**Power:** A model with **UI automation + filesystem + browser** can approach **full interactive user capability** on that session.

**Failure modes:**

- Destructive clicks (delete, send, purchase, publish).
- **Credential exfiltration** (copy fields, screenshots, clipboard).
- **Runaway loops** (sampling + many tool calls) — see [SAMPLING_API_RISKS](../standards/SAMPLING_API_RISKS.md).

This is **not** “safe by default”; it is **powerful by design**.

---

## Mitigations (SOTA minimum)

1. **Isolate:** Dedicated Windows user, **VM**, or non-admin host for agent sessions.
2. **Allowlist:** Expose only the MCP servers and tools needed; avoid mounting **git-github**, **email**, **backup** in the same session as pywinauto unless required.
3. **Human gates:** Use OpenManus **AskHuman** (or equivalent) before irreversible actions.
4. **Logging:** Persist tool traces (openmanus-mcp webapp logger panel + server logs).
5. **No elevation** unless explicitly required; document when UAC paths are used ([windows-operations integration](../integrations/windows-operations/README.md) notes elevation patterns).
6. **Rate / cost:** Local LLM avoids vendor PCM; still cap steps and watch **cloud** fallbacks if any tool calls outbound APIs.
7. **Disposable desktop (untrusted UI tests):** Use **virtualization-mcp** to launch **Windows Sandbox** (or a VM), install the testee, then run **automation inside the guest** — not host pywinauto “clicking at” the Sandbox window. See [PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md) § *Sandboxed / isolated execution*.

---

## Cua Driver vs pywinauto (background Excel + Cursor)

Vendor **[Cua Driver](https://cua.ai/docs/cua-driver/guide/getting-started/introduction)** targets **no-foreground** host automation. Fleet **windows-computer-use-mcp** is adopting a **Cua-shaped** API (`get_window_state`, `snapshot_id`, `element_index`, `capture_mode`) while keeping **HITL / kill switch**. Full comparison, Excel/Cursor FAQ, and **fleet-agent-mcp** bridge notes: **[CUA_DRIVER_AND_PYWINAUTO.md](./CUA_DRIVER_AND_PYWINAUTO.md)**.

## Related docs

- **[CUA_DRIVER_AND_PYWINAUTO.md](./CUA_DRIVER_AND_PYWINAUTO.md)** — Cua Driver vs windows-computer-use-mcp; background loop; fleet-agent cross-connect
- **[PYWINAUTO_MCP_SAFETY.md](./PYWINAUTO_MCP_SAFETY.md)** — HITL vs env kill switch / rate limits / dry-run; **FastMCP 3.1 sampling** amplification; server-farm rules
- [OpenManus integration](../integrations/openmanus.md) — FOSS CLI, local LLM, `mcp.json`
- [windows-computer-use-mcp README](../projects/windows-computer-use-mcp/README.md)
- [AGENT_PROTOCOLS](../standards/AGENT_PROTOCOLS.md) · [VERIFICATION_STANDARDS](../standards/VERIFICATION_STANDARDS.md)
- [AutoHotkey vs pywinauto](../languages/ahk/README.md) — reflex vs brain split

---

*Tags: #computer-use #pywinauto #openmanus #fleet #risk*
