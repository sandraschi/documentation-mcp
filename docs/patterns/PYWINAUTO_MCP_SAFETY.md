# windows-computer-use-mcp (formerly windows-computer-use-mcp): safety model vs vendor “My Computer” apps

**Status:** Fleet pattern · **Last updated:** 2026-04-10  
**Audience:** Operators of **windows-computer-use-mcp**, OpenManus / sampling-capable hosts, **server farms**

---

## New users: what to install

| If you need… | Install |
|--------------|---------|
| Desktop UI automation on **your** Windows session | **windows-computer-use-mcp** — read **`docs/SAFETY.md`** in that repo first |
| **Windows Sandbox / VM** provisioning + disposable installs | **Also install `virtualization-mcp`** — windows-computer-use-mcp **does not** replace Sandbox lifecycle |

**Full sandbox isolation** = **both** servers in the MCP client: **virtualization-mcp** for box + assets; **pywinauto** (or tests) **inside** the guest — not host pywinauto clicking the Sandbox window.

---

## OpenManus, openmanus-mcp, OpenClaw, Manus-class (multiplicative risk)

**windows-computer-use-mcp** is **not** like a browser MCP: it can move the **real cursor** and send **real keys** to **whatever has focus** on the host.

**Why the combo matters:**

| Layer | Risk |
|-------|------|
| **OpenManus** | Long tool loops, **optional MCP fan-in**, **sampling** — see [SAMPLING_API_RISKS.md](../standards/SAMPLING_API_RISKS.md). |
| **openmanus-mcp** | Fleet **bridge + dashboard** — makes OpenManus easier to **orchestrate from more hosts**; does not add desktop safety by itself. |
| **OpenClaw / RoboFang / Manus-class** | Autonomy + channels narratives — **more** pressure to “just automate” without isolation. |
| **windows-computer-use-mcp** | **OS-level** UI automation — **uniquely dangerous** in the fleet. |

**Fleet rule:** Treat **OpenManus + pywinauto + openmanus-mcp** + any **OpenClaw**-style gateway as **production-root** territory: **VM / spare user**, **kill switch** on pywinauto, **virtualization-mcp** for Sandbox workflows, **client step caps**, and **no** pywinauto in default IDE chains for web work. **Canonical narrative:** [integrations/openmanus.md](../integrations/openmanus.md) (Caution block).

---

## Why this exists

Products such as **Manus “My Computer”** (and similar Meta-style narratives) ship **closed guardrails**: allowlists, confirmation steps, and telemetry tuned for their runtime. Our stack is **self-hosted**: **windows-computer-use-mcp** exposes **Win32 UIAutomation** plus **pointer injection** via an in-repo **`win32_mouse`** path (**`SetCursorPos`** / **`mouse_event`**, DPI-aware) and **PyAutoGUI** mainly for **keyboard** and legacy paths — all reachable from any MCP client. That is **full session leverage** if the model or sampling loop misbehaves.

**FastMCP 3.1 sampling + long agentic workflows** can multiply tool calls per user turn. Combined with desktop automation, that can **hammer production hosts** or **spiral on the wrong HWND** (see [FLEET_COMPUTER_USE_MCP.md](./FLEET_COMPUTER_USE_MCP.md) IDE warning).

This document describes **defense in depth**: what the server implements, what you must configure, and what vendors still do better.

---

## Layers in windows-computer-use-mcp (current)

| Layer | Mechanism | Notes |
|--------|-----------|--------|
| **Human-in-the-loop (HITL)** | `approve_automation` + time window; **mouse** / **keyboard** portmanteau require approval for mutating ops | **Not** wired to every portmanteau yet — extend over time. |
| **Pointer failsafe (`win32_mouse`)** | Upper-left **screen corner** aborts injected pointer ops (aligned with PyAutoGUI semantics) | **`PYWINAUTO_MCP_BYPASS_HITL=1`** disables this corner check (and HITL (human-in-the-loop)) for controlled demos/CI. **Not** a permission model. |
| **PyAutoGUI** | Keyboard / some paths; **`FAILSAFE`** for mouse when PyAutoGUI is used | Helps accidental runs; **not** a permission model. |
| **Server rate / kill / dry-run** | `PYWINAUTO_MCP_*` env vars + `automation_safety` tool | Rolling **60s** window; blocks or no-ops before **mutating** input on **mouse** / **keyboard** paths (including **`win32_mouse`**). |
| **Invasive monitoring (opt-in)** | **`global_keylogger`** only if **`PYWINAUTO_MCP_ENABLE_KEYLOGGER=1`** | Same **`gate_invasive_monitoring()`** / kill-switch / dry-run stack as other sensitive tools; see upstream **`docs/SAFETY.md` §6**. |

---

## Environment variables

| Variable | Effect |
|----------|--------|
| `PYWINAUTO_MCP_KILL_SWITCH=1` | **Blocks** all mutating mouse/keyboard actions (after HITL (human-in-the-loop)). Use for emergency stop. |
| `PYWINAUTO_MCP_MAX_ACTIONS_PER_MINUTE` | Default **120** — max **mutating** actions per **rolling 60s** (separate from HITL (human-in-the-loop)). |
| `PYWINAUTO_MCP_DRY_RUN=1` | Counts mutations but **does not** execute pyautogui / **`win32_mouse`** input (returns `dry_run` status). |
| `PYWINAUTO_MCP_ENABLE_KEYLOGGER=1` | Registers **`global_keylogger`** (session keyboard capture). Default **off**; see upstream **`docs/SAFETY.md` §6**. |

Inspect counters: tool **`automation_safety`** (`operation=status` | `reset_counters`).

---

## Fleet rules (non-negotiable)

1. **Do not** ship pywinauto in **default IDE MCP chains** for web-only work — [WEBAPP_STANDARDS.md](../standards/WEBAPP_STANDARDS.md) §7.
2. **Server / CI hosts:** prefer **kill switch default on** unless running an isolated desktop session; use **dry-run** in staging.
3. **Sampling + agentic:** cap **steps** in the **client** (OpenManus / Cursor) **and** use **`automation_safety`** + rate limits in the **server**.
4. Treat **vendor** products as having **more** policy layers (telemetry, remote kill, signed binaries). We are **not** parity; we **document** and **layer** env + HITL (human-in-the-loop) + rates.

---

## Sandboxed / isolated execution (Windows Sandbox & VMs)

A **“sandboxed pywinauto”** product sounds simple: spin up **Windows Sandbox**, install the **testee**, then **click around inside** the sandbox. In practice it splits into **two different problems**:

| Approach | What happens | Verdict |
|----------|----------------|--------|
| **Host pywinauto** driving the **Sandbox window** | You automate the **container window** on the host desktop, not the **guest** HWND tree. Focus, DPI, and “which surface receives input” get **fragile** fast — same class of bug as IDE vs Chrome. | **Poor** default for serious UI tests. |
| **Guest-side automation** | **PyWinAuto / pyautogui runs inside the sandbox session** (or a full VM), after the testee is installed. The automation sees the **real** Win32 tree for that session. | **Correct** isolation model. |

**Fleet composition (already available):** **virtualization-mcp** (fleet repo; see its README and `assets/sandbox/`) exposes **Windows Sandbox launch**, mapped **host assets** → `C:\Assets`, optional **full dev setup** (winget + toolchain), **AIRGAP**, optional **host Ollama** from the guest. Use that to **provision** the disposable desktop; run **tests or a small Python script inside the guest** that uses pywinauto locally — or a **headless** runner pushed with the assets folder.

**Why we do not ship a single merged “sandboxed pywinauto” tool in windows-computer-use-mcp (for now):**

- **Orchestration** belongs next to **Sandbox XML / VM lifecycle** (virtualization-mcp), not inside every UI tool.
- **MCP inside the guest** (stdio/HTTP forwarded to the host) is doable but **operationally heavy** (port mapping, health, two servers). Treat as a **phase-2** pattern if you need agent-driven UI **inside** the box.
- **Simpler win:** `virtualization-mcp` **launch** + **guest script** that runs pytest/pywinauto with **no** host desktop automation.

**Summary:** Prefer **virtualization-mcp for sandbox/VM**, **windows-computer-use-mcp only on the host** when you accept host risk — or run **pywinauto in the guest** without MCP until you need the extra complexity.

---

## Related docs

- [FLEET_COMPUTER_USE_MCP.md](./FLEET_COMPUTER_USE_MCP.md) — role split, mitigations, IDE warning  
- [VERIFICATION_STANDARDS.md](../standards/VERIFICATION_STANDARDS.md) §2.4 — browser vs desktop tools  
- [SAMPLING_API_RISKS.md](../standards/SAMPLING_API_RISKS.md) — sampling amplification  
- **virtualization-mcp** (fleet) — Windows Sandbox launch, `assets/sandbox`, dev-setup APIs (compose with guest-side tests)  
- [integrations/openmanus.md](../integrations/openmanus.md) — Caution block (OpenManus + pywinauto + openmanus-mcp + OpenClaw / Manus-class)  
- Upstream repo: `windows-computer-use-mcp` README — Safety section

---

*Tags: #pywinauto #safety #sampling #fleet #mcp*
