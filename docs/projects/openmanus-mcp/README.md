# openmanus-mcp — Fleet MCP server + dashboard for OpenManus (FOSS)

[![GitHub](https://img.shields.io/badge/GitHub-sandraschi%2Fopenmanus--mcp-181717?logo=github)](https://github.com/sandraschi/openmanus-mcp)
[![Beta](https://img.shields.io/badge/status-beta-yellowgreen)](https://github.com/sandraschi/openmanus-mcp/blob/main/RELEASING.md)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/INSTALL.md)
[![FastMCP](https://img.shields.io/badge/FastMCP-3.1%2B-8b5cf6)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-22c55e)](https://github.com/sandraschi/openmanus-mcp/blob/main/LICENSE)

**Central project documentation** for **openmanus-mcp** in MCP Central Docs.  
**Canonical source repo:** [github.com/sandraschi/openmanus-mcp](https://github.com/sandraschi/openmanus-mcp) · **Local clone:** `D:/Dev/repos/openmanus-mcp`

| Doc in this folder | Purpose |
|--------------------|---------|
| [README.md](./README.md) (this file) | Full picture: architecture, APIs, fleet, security, links |
| [STATUS.md](./STATUS.md) | Maturity, shipped vs stub, CI, release channel |
| [STRUCTURE.md](./STRUCTURE.md) | Directory layout vs central standards |
| [INTEGRATION.md](./INTEGRATION.md) | Fleet wiring, upstream OpenManus, DTU / Bastio pointers |

**Upstream agent (separate repo):** [FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus) — deep integration narrative: **[integrations/openmanus.md](../../integrations/openmanus.md)**.

> [!CAUTION]
> **If you also use pywinauto-mcp:** OpenManus + **sampling** + this **openmanus-mcp** bridge + **pywinauto** is a **high-amplification** stack (see **[PYWINAUTO_MCP_SAFETY.md](../../patterns/PYWINAUTO_MCP_SAFETY.md)** § *OpenManus, openmanus-mcp, OpenClaw, Manus-class*). **OpenClaw / Manus-class** autonomy increases pressure to run unattended desktop automation. **pywinauto-mcp** `docs/SAFETY.md` and **virtualization-mcp** for **Windows Sandbox** are **not optional** for safe disposable-desktop workflows.

---

## 1. What this project is

**openmanus-mcp** is a **sandraschi fleet** package that:

1. Exposes a **FastMCP 3.1+** server over **stdio** so **Cursor**, **Claude**, **Glama**, and other MCP hosts can call a single portmanteau tool (**`openmanus_bridge`**) that **bridges** to the local **OpenManus** workspace.
2. Runs a **FastAPI** backend on **10768** and a **Vite + React 19** dashboard on **10769** (adjacent ports per [WEBAPP_PORTS](../../operations/WEBAPP_PORTS.md)).
3. Provides **fleet onboarding** (curated catalog, `git clone` / optional `uv` install, UI + REST) so operators can pull sibling MCP repos into a local **`fleet/`** workspace without merging tool namespaces into one process.
4. **Webapp (WEBAPP_STANDARDS-aligned):** **Iron Shell** sidebar + topbar, **Run** (sync/async OpenManus + activity presets), **SOTA Chat** (local LLM + skills), **Logger**, **Help**, **Dashboard** + **Fleet**.

**It is not Manus.im.** Vendor **Manus** is a subscription product; **OpenManus** is **FOSS**. This repo is **$0** to that vendor; you bring **Ollama**, **LM Studio**, or other endpoints via upstream `config.toml`. See **[MANUS](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/MANUS.md)** in the source repo.

---

## 2. Why it exists (fleet rationale)

| Problem | How openmanus-mcp helps |
|--------|-------------------------|
| OpenManus is an **MCP client** (`config/mcp.json`), not an MCP **server** | FastMCP wrapper gives hosts a **stable stdio** tool surface |
| Operators want a **glass UI** + health, not only CLI | **10769** dashboard + **10768** API |
| Many repos in the **MCP + React** pattern | **Fleet** catalog + onboard + optional Windows webapp launch |

Larger fleet story: **[FLEET_CONTEXT](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/FLEET_CONTEXT.md)** (source repo).

---

## 3. Architecture (high level)

```text
┌─────────────────┐     stdio      ┌──────────────────┐
│  MCP client     │◄──────────────►│  openmanus_mcp   │
│  (Cursor, etc.) │                │  FastMCP server  │
└─────────────────┘                └────────┬─────────┘
                                            │
                     ┌──────────────────────┼──────────────────────┐
                     │                      │                      │
                     ▼                      ▼                      ▼
            ┌──────────────┐       ┌─────────────────┐    ┌──────────────┐
            │  .env /      │       │  FastAPI        │    │  Future:     │
            │  OPENMANUS_  │       │  :10768         │    │  subprocess  │
            │  ROOT probe  │       │  /api/v1/*      │    │  OpenManus   │
            └──────────────┘       └────────┬────────┘    └──────────────┘
                                            │ HTTP (Vite proxy /api)
                                            ▼
                                   ┌─────────────────┐
                                   │  Vite React     │
                                   │  :10769         │
                                   │  Dashboard+Fleet│
                                   └─────────────────┘
```

**Flows:**

1. **MCP** — JSON-RPC over stdio → **`openmanus_bridge`** → settings / validation / runner (`run_prompt`, async job store).
2. **Dashboard** — Browser → **10769**; **`/api/v1/*`** proxied to **10768**.
3. **Fleet** — `GET/POST /api/v1/fleet/*` → clone under **`fleet/`**, state in **`.fleet_state.json`** (gitignored).
4. **Chat + skills** — `POST /api/v1/chat/completions` (Ollama / LM Studio) with optional **compact skill index** and **`skill_ids`** full `SKILL.md` injection — **[SKILLS_OPENCLAW.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SKILLS_OPENCLAW.md)**.
5. **Supervisor** — optional background tick + **interval schedules** → async OpenManus runs; **connector** catalog REST — **[SUPERVISOR.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SUPERVISOR.md)**.
6. **Run page** — sync/async runner + **comms / robots / media** activity presets (fleet MCP hints, not outbound calls from this API).

Full diagram and roadmap: **[ARCHITECTURE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/ARCHITECTURE.md)**.

---

## 4. Version and stack

| Item | Value |
|------|--------|
| **Package version** | **0.1.0b1** (PEP 440 beta) |
| **Python** | **≥ 3.12** |
| **MCP** | **FastMCP** 3.1+ (repo pins **&lt; 4**) |
| **API** | **FastAPI**, **uvicorn** |
| **UI** | **Vite 6**, **React 19** |
| **Quality** | **Ruff**, **pytest**, **pre-commit**, GitHub Actions |

**Forbidden dev ports** (org rule): 3000, 5173, 8000, 8080 — this project uses **10768 / 10769** only.

---

## 5. MCP tool surface

| Tool | Operations | Notes |
|------|------------|--------|
| **`openmanus_bridge`** | `status`, `validate`, `run_prompt`, `run_prompt_async`, `job_status` | Subprocess runner, async job store, persistent FIFO queue |
| **`bash`** | *(via OpenManus agent)* | Full terminal with command denylist + obfuscation detection |
| **`computer`** | *(via OpenManus agent)* | Windows-native mouse/keyboard/screenshot (win32 API, confirmation gated) |
| **`python_execute`** | *(via OpenManus agent)* | Python execution with restricted builtins |
| **`browser_use`** | *(via OpenManus agent)* | Playwright-based browser automation |
| **`str_replace_editor`** | *(via OpenManus agent)* | File editing scoped to workspace root |

Docstrings follow **[AGENT_PROTOCOLS](../../standards/AGENT_PROTOCOLS.md)** (enhanced responses, portmanteau pattern).

---

## 6. REST API (selected)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/status` | OpenManus path / probe |
| GET | `/api/v1/fleet/catalog` | Curated fleet + onboard state |
| GET | `/api/v1/fleet/members` | Member detail |
| POST | `/api/v1/fleet/onboard` | Clone + optional install |
| POST | `/api/v1/fleet/webapp/start` | Windows PowerShell launch helper |
| POST | `/api/v1/run`, `/api/v1/run/async` | OpenManus subprocess (sync / queued) |
| POST | `/api/v1/chat/completions` | Local LLM proxy + optional skills |
| GET | `/api/v1/skills`, `/api/v1/skills/{id}` | Skill catalog + full `SKILL.md` |
| GET | `/api/v1/supervisor/*`, `/api/v1/connectors` | Supervisor + connector metadata |

**Registry:** [webapp-registry.json](../../operations/webapp-registry.json) — entries `openmanus-mcp-backend`, `openmanus-mcp-frontend`.

---

## 7. Fleet onboarding and desktop “computer use”

- **Catalog:** versioned **`src/openmanus_mcp/data/fleet_catalog.json`** (curated list).
- **Workspace:** clones live under **`fleet/`** (gitignored except `.gitkeep`); optional **`OPENMANUS_FLEET_ROOT`**.
- **Bootstrap script:** **`scripts/Bootstrap-Fleet.ps1`** — see **[FLEET.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/FLEET.md)**.

For **Win32 desktop agents**, compose **OpenManus** + **pywinauto-mcp** (+ OCR, etc.) via upstream **`mcp.json`** — **high risk**. Pattern: **[FLEET_COMPUTER_USE_MCP.md](../../patterns/FLEET_COMPUTER_USE_MCP.md)**.

---

## 8. Security, hygiene, and arms-race context

**Security hardening applied in this fleet fork (2026-05):**

| Layer | What | Where |
|-------|------|-------|
| Bash denylist | Regex patterns block rm -rf /, sudo, dd, useradd, chmod 4777, fork bombs, cryptominers | `app/tool/bash.py` |
| Obfuscation detection | Hex/octal/printf/ANSI-C decoding before denylist match | `app/tool/bash.py` |
| Python restricted globals | Only safe builtins; os/subprocess/socket imports blocked; eval/exec blocked | `app/tool/python_execute.py` |
| Computer use gate | Keyboard/screenshot require interactive `y/N` confirmation; blocked in headless | `app/tool/local_computer_use.py` |
| Workspace scoping | str_replace_editor rejects paths outside `config.workspace_root` | `app/tool/str_replace_editor.py` |
| API auth | Optional `OPENMANUS_MCP_API_KEY` Bearer token on REST endpoints | `src/openmanus_mcp/api/app.py` |
| Key auto-generation | Random hex key generated if none set; written to `.api_key` | `src/openmanus_mcp/api/app.py` |

Source repo ships **[SECURITY.md](https://github.com/sandraschi/OpenManus/blob/main/SECURITY.md)** and **[REPO_HYGIENE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/REPO_HYGIENE.md)**.

**Operational safety** (fleet, pywinauto): **[SAFETY.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SAFETY.md)**.

---

## 9. Documentation map (source repository)

Staggered docs (start at **[docs/README.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/README.md)**):

| Doc | Topic |
|-----|--------|
| [INSTALL.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/INSTALL.md) | Clone, `uv`, `.env`, MCP `cwd`, `start.ps1` |
| [TECH.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/TECH.md) | Layout, env, Glama, CI |
| [MANUS.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/MANUS.md) | Manus.im vs OpenManus vs this repo |
| [OPENMANUS.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/OPENMANUS.md) | Upstream agent, `OPENMANUS_ROOT`, local LLM |
| [ARCHITECTURE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/ARCHITECTURE.md) | Workflows, roadmap, OpenClaw-style shipped vs planned |
| [SUPERVISOR.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SUPERVISOR.md) | Schedules, heartbeat, connector catalog |
| [SKILLS_OPENCLAW.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SKILLS_OPENCLAW.md) | AgentSkills-style `SKILL.md`, chat injection |
| [SAFETY.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/SAFETY.md) | Risk model |
| [FLEET.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/FLEET.md) | Windows fleet bootstrap |
| [FLEET_CONTEXT.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/FLEET_CONTEXT.md) | sandraschi MCP fleet narrative |
| [HOW_WE_BUILD.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/HOW_WE_BUILD.md) | Process, zeropaid, toolchains |
| [GLAMA.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/GLAMA.md) | Registry metadata |

**Root:** [README.md](https://github.com/sandraschi/openmanus-mcp/blob/main/README.md) · [CONTRIBUTING.md](https://github.com/sandraschi/openmanus-mcp/blob/main/CONTRIBUTING.md) · [RELEASING.md](https://github.com/sandraschi/openmanus-mcp/blob/main/RELEASING.md) · [glama.json](https://github.com/sandraschi/openmanus-mcp/blob/main/glama.json) · [justfile](https://github.com/sandraschi/openmanus-mcp/blob/main/justfile)

---

## 10. Glama and discovery

- **`glama.json`** — MCP package metadata + `mcpServers` block (stdio + webapp URLs when published).
- Central ops: [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md), [webapp-registry.json](../../operations/webapp-registry.json).

---

## 11. Roadmap (short)

From **[ARCHITECTURE.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/ARCHITECTURE.md)**:

- **Subprocess runner** for upstream OpenManus + streaming logs in UI.
- **Cursor snippet** generation from `fleet/` paths.
- **ORB-class** integration (planned).
- **OpenClaw / OpenFang**-style phases (heartbeat → connectors → skills → multi-agentic).
- **Hierarchical local agents** (arXiv-informed) — design open.
- **My robots** — toy rovers → vacuums → humanoids; virtual ∥ real tracks.

---

## 12. Quick start (pointers)

1. Clone [openmanus-mcp](https://github.com/sandraschi/openmanus-mcp) and follow **[INSTALL.md](https://github.com/sandraschi/openmanus-mcp/blob/main/docs/INSTALL.md)**.
2. Clone [FoundationAgents/OpenManus](https://github.com/FoundationAgents/OpenManus) and set **`OPENMANUS_ROOT`** (or equivalent probe path).
3. Register MCP with **`cwd`** at the **openmanus-mcp** repo root (see INSTALL).
4. Run API + UI: **`web_sota/start.ps1`** or **`just start-web`** / **`just api`** per **[justfile](https://github.com/sandraschi/openmanus-mcp/blob/main/justfile)**.

---

*Tags: #openmanus-mcp #openmanus #fastmcp #mcp #fleet #local-llm #sandraschi*  
*Last updated: 2026-03-19 (MCP Central Docs project mirror)*
