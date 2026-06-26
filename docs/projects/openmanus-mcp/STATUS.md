# openmanus-mcp — Status

**Last updated:** 2026-03-19  
**Source repo:** [sandraschi/openmanus-mcp](https://github.com/sandraschi/openmanus-mcp)  
**Local path:** `D:/Dev/repos/openmanus-mcp`

---

## Release channel

| Field | Value |
|-------|--------|
| **PyPI / version** | **0.1.0b1** (beta) |
| **npm (Webapp)** | **0.1.0-beta.1** |
| **Trove** | Development Status :: 4 - Beta |
| **Tags** | `v0.1.0b1` style per [RELEASING.md](https://github.com/sandraschi/openmanus-mcp/blob/main/RELEASING.md) |

---

## What is production-usable today

- **stdio MCP** — **`openmanus_bridge`** with **`status`**, **`validate`**, **`run_prompt`**, **`run_prompt_async`**, **`job_status`**.
- **Computer use** — **`computer`** tool: mouse/keyboard/screenshot via win32 API (confirmation gated).
- **Bash** — **`bash`** tool: full terminal with security denylist + obfuscation detection.
- **FastAPI** — **`/api/v1/health`**, **`/api/v1/status`**, fleet routes, **`/api/capabilities`** introspection.
- **Vite dashboard** — glass shell, dashboard cards, **Fleet** page, **Status & Audit**, **Chat**, **API Docs**.
- **Fleet catalog** — `fleet_catalog.json` + onboard + optional Windows webapp launch.
- **Security hardening** — bash denylist, Python restricted globals, computer use gate, API auth, workspace scoping.
- **CI** — Ruff, pytest, `Webapp` production build (see `.github/workflows/` in source).
- **Docs** — **SECURITY.md**, staggered `docs/*`, **REPO_HYGIENE**, **CONTRIBUTING** + PR template.

---

## Explicit gaps (honest)

| Area | State |
|------|--------|
| **`run_prompt`** | **Implemented** — subprocess + `main.py --prompt` or stdin; **`run_flow.py`** via stdin; REST + webapp **Run** page |
| **ORB** | **Planned** — design thread in source Issues |
| **Health aggregation** | Partial — deeper fleet liveness is roadmap |
| **Job store** | **FIFO-capped** completed async jobs (`OPENMANUS_JOB_STORE_MAX_COMPLETED`); MCP vs API separate processes |

---

## Central registry

- [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — **10768** backend, **10769** frontend.
- [webapp-registry.json](../../operations/webapp-registry.json) — start commands + repo path.

---

## Related central docs

- [integrations/openmanus.md](../../integrations/openmanus.md) — upstream deep dive + fleet positioning.
- [patterns/FLEET_COMPUTER_USE_MCP.md](../../patterns/FLEET_COMPUTER_USE_MCP.md) — desktop composition.
- [README.md](./README.md) — full project picture.
