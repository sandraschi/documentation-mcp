# openmanus-mcp — Integration

How **openmanus-mcp** connects to the **sandraschi MCP fleet**, **upstream OpenManus**, and **central security / factory** docs.

---

## 1. Upstream OpenManus (required brain)

| Item | Detail |
|------|--------|
| **Repo** | [FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus) |
| **Config** | `config.toml` — **Ollama**, **LM Studio**, OpenAI-compatible locals |
| **MCP role** | OpenManus is an **MCP client** — `config/mcp.json` lists **servers** it calls |
| **Central doc** | **[integrations/openmanus.md](../../integrations/openmanus.md)** |

**openmanus-mcp** does **not** replace OpenManus; it **exposes** bridge + UI + fleet helpers so **hosts** (Cursor, etc.) can orchestrate without reimplementing the agent.

---

## 2. MCP hosts (Cursor, Claude, Glama)

- **Transport:** **stdio** from repo root (see source **[INSTALL.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/INSTALL.md)** for `cwd` and command).
- **Tool:** **`openmanus_bridge`** — portmanteau operations.

---

## 3. Sibling fleet servers (composition)

Typical **desktop automation** stack:

| Server | Role |
|--------|------|
| **OpenManus** | Planning, tool choice, local LLM |
| **pywinauto-mcp** | Win32 UI automation — **uniquely dangerous**; see **[PYWINAUTO_MCP_SAFETY.md](../../patterns/PYWINAUTO_MCP_SAFETY.md)** § *OpenManus, openmanus-mcp, OpenClaw, Manus-class* |
| **ocr-mcp** / others | Capture, ops |

**Warning:** **OpenManus + openmanus-mcp + pywinauto-mcp** + anything **OpenClaw / Manus-class** is **multiplicative** risk (sampling, long loops, OS-wide input). Add **virtualization-mcp** for Sandbox/VM; use **pywinauto** `docs/SAFETY.md` env limits.

Wire via **OpenManus** `mcp.json`, **not** by merging tools into openmanus-mcp. Pattern: **[FLEET_COMPUTER_USE_MCP.md](../../patterns/FLEET_COMPUTER_USE_MCP.md)**.

**Fleet onboarding UI** in openmanus-mcp helps **clone** catalog entries into **`fleet/`**; each member remains its **own** process and repo.

---

## 4. DTU (Dark Twin Universe) — dark-app-factory

**Twin / shadow** hardening for agent workflows is documented and implemented in org repo **[dark-app-factory](https://github.com/sandraschi/dark-app-factory)**.  
Cross-reference in source: **[REPO_HYGIENE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/REPO_HYGIENE.md)**.

Central flagship docs (if present in this checkout): [projects/dark-app-factory/README.md](../dark-app-factory/README.md), [DTU_PROTOCOL](../dark-app-factory/DTU_PROTOCOL.md).

---

## 5. Agent gateways (prompt injection)

**Bastio** and similar gateways address **prompt injection** / **indirect instruction** in tool args and retrieved content. Pointer: **[bastio.com](https://www.bastio.com/)** — see **REPO_HYGIENE** arms-race section for naming caveats.

---

## 6. RoboFang / OpenClaw / OpenFang (roadmap alignment)

Source **[ARCHITECTURE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/ARCHITECTURE.md)** maps **phased** adoption:

- Heartbeat / liveness  
- Comms connectors (OpenClaw-class)  
- Skill bundles (OpenFang-class adapters)  
- Multi-agentic local orchestration  

**RoboFang** and other hubs may appear as **peers** later — no monolithic merge implied.

---

## 7. Central standards

| Standard | Link |
|----------|------|
| Agent protocols / tool returns | [AGENT_PROTOCOLS](../../standards/AGENT_PROTOCOLS.md) |
| Webapp ports | [WEBAPP_PORTS](../../operations/WEBAPP_PORTS.md) |
| Webapp UX | [WEBAPP_STANDARDS](../../standards/WEBAPP_STANDARDS.md) |

---

## 8. Glama / registry

- Source **`glama.json`**
- Central **[webapp-registry.json](../../operations/webapp-registry.json)** for ops dashboards

---

← [README.md](./README.md) · [STATUS.md](./STATUS.md) · [STRUCTURE.md](./STRUCTURE.md)
