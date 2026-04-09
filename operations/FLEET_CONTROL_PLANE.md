---
title: "Fleet control plane (RoboFang + MCP fleet)"
category: operations
status: active
audience: mcp-dev
related:
  - operations/WEBAPP_PORTS.md
  - standards/AGENT_PROTOCOLS.md
last_updated: 2026-03-23
---

# Fleet control plane

**Problem:** Copying every MCP server into `robofang/tools/` does not “turbocharge” RoboFang — it creates **version drift**, **merge debt**, and **unclear ownership**. The fleet stays strong when each server is an independent release unit and RoboFang remains a **thin control plane**.

**Principle:** **Source of truth = each MCP repo.** RoboFang = **orchestration, catalog, install/launch, health, routing hints** — not a monorepo of duplicated servers.

---

## Architecture (three phases)

### Phase 1 — Discover & index (no duplication)

| Layer | Responsibility | Examples |
|--------|----------------|----------|
| **Public / curated indexes** | Optional third-party org mirrors, registries | GitHub org lists, MCP Registry API |
| **Local catalog artifact** | JSON (or DB) with stars, topics, categories, URLs, last fetch | `iflow-mcp-catalog` → `data/catalog.json` |
| **Fleet manifest** | What *you* actually install | RoboFang `fleet_manifest.yaml`, bridge catalog API |

**RoboFang `tools/`** here: **only** indexers, validators, port-registry sync scripts — **not** full server code.

**Plug-in:** `D:\Dev\repos\iflow-mcp-catalog` (or any path) produces **`catalog.json`** + optional HTML report. RoboFang (or a cron job) can **read** that file to enrich “suggested hands” or research views — **no need to vendor the Python package inside RoboFang** unless you want a git submodule or documented path dependency.

### Phase 2 — Install & lifecycle (`hands/`)

| Concept | Role |
|---------|------|
| **`hands/`** | Runtime clones of MCP repos the user chose to install (default under RoboFang folder). |
| **Bridge** | `git clone`, manifest updates, optional `start.ps1`, discovery (`/api/fleet/discover`, add-from-external). |
| **Metadata** | Repo-root `robofang.json`, `INTEGRATION.md` snippets — already documented in RoboFang `docs/MCP_FLEET.md`. |

**Do not** mirror full server trees into `robofang/tools/` to “back them up.” Use **manifest + clone path**.

### Phase 3 — Operate & route (future-friendly)

| Capability | Purpose |
|------------|---------|
| **Health / readiness** | Per-hand process or HTTP ping; surface in hub UI. |
| **Capability map** | Tool names + short descriptions from MCP `list_tools` (cached). |
| **Routing hints** | Policy: which hand for which task class (optional LLM-facing rules). |
| **Preflight** | Port clear, token present, backend up — before agent runs a heavy workflow. |

This is where “turbocharge” actually lands: **fast answers about what exists and whether it is alive**, not **more copies of code**.

---

## What belongs where

| Location | Put here | Do **not** put here |
|----------|-----------|---------------------|
| **Each MCP repo** | Server, tests, webapp, `glama.json`, packaging | RoboFang-specific hacks without upstreaming or doc |
| **`robofang/tools/`** | Thin scripts: analyze fleet, bump ports, validate manifest | Full MCP server implementations |
| **`hands/<repo>/`** | Installed clone of a hand | Edits you intend to lose on reinstall unless forked |
| **mcp-central-docs** | Cross-repo standards, port registry, patterns | Per-server secrets |

---

## Optional wiring diagram (mental model)

```text
[ Registries / GitHub orgs ]     [ MCP Registry API ]
         |                              |
         v                              v
   indexer (optional)              bridge /discover
         |                              |
         +------------>  catalog / manifest  <------------+
         |                              |                |
         v                              v                v
              local JSON / YAML              hands/ clones
                         |
                         v
                  hub UI + bridge APIs
```

---

## Notes & decisions log

- **2026-03-23:** Initial doc. Aligns with RoboFang model: `hands/` = installed servers; bridge = discovery + add-from-external; avoid fleet duplication in `robofang/tools/`.
- **iflow-mcp-catalog:** Treat as **optional research/index satellite**; integrate by **consuming `catalog.json`** or linking the webapp (ports **10808/10809** per `WEBAPP_PORTS.md`), not by copying the package tree into RoboFang.

---

## See also

- RoboFang: `docs/MCP_FLEET.md` (external MCP, metadata files).
- Stammtisch / demo ideas (Cursor community): [CURSOR_STAMMTISCH_DEMO_KIT.md](../research/agentic-ide/CURSOR_STAMMTISCH_DEMO_KIT.md).
