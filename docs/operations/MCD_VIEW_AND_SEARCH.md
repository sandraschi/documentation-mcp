# How to view MCD content and run semantic search

**Last updated:** 2026-06-06  
**Problem this solves:** Confusion between **mcp-central-docs** (private MCD), **documentation-mcp** (public extract), **docs_mcp** (Python package), and **web_sota** (Vite UI).

---

## Mental model (one diagram)

```text
mcp-central-docs/          ← PRIVATE corpus (nvidia/, standards/, projects/, …)
├── src/docs_mcp/          ← Backend: LanceDB RAG, FastMCP tools, Starlette API
├── web_sota/              ← Frontend: Vite/React (NOT fleet SOTA webapp template)
├── scripts/mcd_exerciser.py
└── data/lancedb/          ← Vector index (under src/docs_mcp/data after ingest)

documentation-mcp/         ← PUBLIC GitHub repo (golden docs + fleet registry)
├── src/documentation_mcp/   ← Same idea, different package name
└── web_sota/              ← ports **11032 / 11033** (public hub)

```

| Name | What it is |
|------|------------|
| **MCD** | The **markdown tree** in `mcp-central-docs/` (read in Cursor, or via RAG). |
| **docs_mcp** | Python module in **`mcp-central-docs/src/docs_mcp`** only. |
| **docs-mcp** | PyPI-style project name in `pyproject.toml` (same private repo). |
| **documentation-mcp** | Separate repo for **public** publish; federated RAG + thinner `docs/`. |

**Ports (deduplicated Jun 2026):** **mcp-central-docs** **10794/10795**; **documentation-mcp** **11032/11033** — both can run together. See [WEBAPP_PORTS.md](WEBAPP_PORTS.md).

---

## Recommended paths (pick one)

### A. Fastest — CLI semantic search (no webapp)

From **`D:\Dev\repos\mcp-central-docs`**:

```powershell
Set-Location D:\Dev\repos\mcp-central-docs
just search "RTX Spark GB10"
just semantic "What is OpenShell on Windows?"
just stats
just mcd-sync
```

- **`search`** — vectors only (LanceDB + BGE), no Ollama.
- **`semantic`** / **`report`** — needs **Ollama** running; see `scripts/README.md`.
- Indexes **this repo’s** docs after `mcd-sync`.

**Best for:** daily work, agents, no broken Vite UI.

---

### B. Read markdown directly (no server)

Open folder in Cursor:

`D:\Dev\repos\mcp-central-docs\nvidia\` (and the rest of the tree).

No index required. New docs (e.g. Computex notes) are visible immediately.

---

### C. MCP in Cursor (stdio tools)

Enable **one** server pointing at the **private** repo (your full MCD):

```json
"docs-mcp": {
  "command": "uv",
  "args": [
    "--directory",
    "D:/Dev/repos/mcp-central-docs",
    "run",
    "python",
    "-m",
    "docs_mcp.stdio_main"
  ],
  "env": {
    "PYTHONPATH": "D:/Dev/repos/mcp-central-docs;D:/Dev/repos/mcp-central-docs/src"
  }
}
```

(Adjust entry if your `pyproject.toml` defines a different script; check `[project.scripts]`.)

Tools: `search_docs`, `get_document`, `ask_docs`, etc. — same backend logic as HTTP **10795**.

**documentation-mcp** in `MASTER_MCP_CONFIG.json` is the **public** clone; use it only when you intentionally want that smaller corpus.

---

### D. Web dashboard (10794) — when you want UI

**Use private MCD only** (unless you are developing the public repo):

```powershell
Set-Location D:\Dev\repos\mcp-central-docs
pwsh -NoProfile -ExecutionPolicy Bypass -File web_sota\start.ps1 -NoBrowser
```

Then open **http://127.0.0.1:10794** (frontend). API: **http://127.0.0.1:10795**.

| Port | Role |
|------|------|
| **10794** | Vite dev server (proxy `/api` → 10795) |
| **10795** | `docs_mcp` Starlette + `/api/execute`, `/health`, `/mcp` |

**Backend-only** (API / MaaS / debugging):

```powershell
pwsh -File web_sota\start.ps1 -BackendOnly
```

**First-time slow?** Run `just mcd-sync` once (embedding ingest). Backend loads FastEmbed model on first query.

**Why it feels like a “runt” webapp:** `web_sota` predates current **WEBAPP_STANDARDS** (Biome shell, prefab-ui, portmanteau dashboard). It works but is not the fleet chrome template. **CLI + Cursor** are the supported happy path until webapp Phase 5 refresh.

---

### E. HTTP MaaS from another repo

With backend up on **10795**:

```powershell
$body = @{ name = "search_docs"; arguments = @{ query = "MCP port allocation"; limit = 5 } } | ConvertTo-Json -Depth 5
Invoke-RestMethod -Uri "http://127.0.0.1:10795/api/execute" -Method POST -Body $body -ContentType "application/json"
```

See **[DOCS_MCP_MAAS.md](DOCS_MCP_MAAS.md)**.

---

## documentation-mcp vs mcp-central-docs

| | **mcp-central-docs** | **documentation-mcp** |
|---|----------------------|------------------------|
| **Visibility** | Private fleet hub | Public GitHub |
| **Content** | Full MCD + `not-mcp-related/`, projects, nvidia, … | `docs/` golden set + federation hooks |
| **Python pkg** | `docs_mcp` | `documentation_mcp` |
| **Ports** | **10794** frontend / **10795** backend | **11032** frontend / **11033** backend |
| **Start** | `web_sota\start.ps1` from **mcp-central-docs** | `web_sota\start.ps1` or `just serve` from **documentation-mcp** |

**Rule:** For **your** nvidia notes and fleet docs → **mcp-central-docs** only. **documentation-mcp** is for publishing / external consumers, not a second copy of private MCD.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Empty search / no nvidia hits | `just mcd-sync` from **mcp-central-docs** |
| 10794 loads, search 500 | Backend not on 10795 — check `http://127.0.0.1:10795/health` |
| Port in use | Check which stack: MCD **10794/10795** vs public hub **11032/11033**; stop stale `start.ps1` jobs |
| `just mcd-ui` fails | Fleet recipe calls missing `start-webapp` — use `web_sota\start.ps1` or `just start-webapp` after recipe added |
| Slow first start | FastEmbed download + LanceDB open; normal |
| Stale RAG answers | Known issue — see `STATUS.md`; prefer `search` + read cited files |

---

## Quick reference

```powershell
Set-Location D:\Dev\repos\mcp-central-docs
just search "DGX Spark FP4"
just mcd-sync
pwsh -File web_sota\start.ps1
```

**Fleet webapp health:** Cold-start probe (full fleet / single repo / **Broken\*** retry) — [FLEET_WEBAPP_PROBE.md](../docs/operations/FLEET_WEBAPP_PROBE.md). MetaMCP → Fleet Status → Cold start. Reports: `mcp-central-docs/scripts/out/fleet-webapp-report.json`.

**New content you added:** `nvidia/COMPUTEX_2026_ASSESSMENT.md` — visible in Cursor immediately; in RAG after `just mcd-sync`.
