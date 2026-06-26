# chip-design-mcp

**Type:** MCP Server + Webapp  
**Status:** Active — Fleet SOTA 2026  
**Version:** 0.1.0 (unreleased enhancements on `master`)  
**Ports:** Backend **11022** / Frontend **11023**  
**Repo:** `D:\Dev\repos\chip-design-mcp`  
**GitHub:** https://github.com/sandraschi/chip-design-mcp (private)  
**Domain standard:** [chip_design_cad_sota.md](../../standards/rules/chip_design_cad_sota.md)  
**Last assessed:** 2026-05-31

---

## Description

**Superyacht magazine for silicon** — educate what is *possible* with FOSS RTL→GDSII (sky130 shuttles, open EDA, KiCad boards for packages). Real FastMCP orchestration (Yosys, cocotb/iverilog, OpenLane Docker, Magic, netgen, OpenSTA); honest failures; explicit “do not do this at home” warnings. See repo **`docs/DREAMING_IN_SILICON.md`**.

SkyWater 130nm, GF180MCU, and IHP SG13G2 PDKs via **volare**. PCB story: **kicad-mcp**, not this server.

---

## Install (operator)

**Windows naked-PC:** `.\start.bat` only (git + winget assumed).

| Step | Action |
|------|--------|
| 1 | winget: uv, just, Node, npm |
| 2 | `uv sync --extra eda` |
| 3 | **`scripts/install-eda.ps1`** — Docker + OpenLane image, WSL apt EDA, volare sky130 |
| 4–6 | Webapp + backend |

Canonical doc: repo **`INSTALL.md`**. Product scope: **`docs/PRD.md`**.

```powershell
cd D:\Dev\repos\chip-design-mcp
.\start.bat
# MCD shortcut:
# D:\Dev\repos\mcp-central-docs\just-starts\chip-design-mcp-start.bat
```

---

## Architecture

```
MCP / REST client → FastAPI + FastMCP (11022) → subprocess / Docker
                                              → work dir (%TEMP%\chip_design_mcp_work)
Vite React dashboard (11023) → proxies /api, /mcp, /sse → 11022
```

| Layer | Technology |
|-------|------------|
| MCP | FastMCP 3.2, stdio + HTTP/SSE |
| REST | `/api/v1/*`, `/api/capabilities`, `/api/v1/help/{slug}` |
| Webapp | React 19, Vite 6, Tailwind, Bun/npm |
| Python | **uv**, `uv.lock`, optional **`eda`** extra (volare, cocotb) |
| EDA (Win) | WSL shims in `bin/`, Docker OpenLane image |

---

## MCP surface (32+ tools)

| Domain | Examples |
|--------|----------|
| Synthesis | `syn_run`, `syn_stats` |
| Simulation | `sim_run_testbench` |
| Place & route | `pr_run_flow`, `pr_export_gds` |
| Verification | `verify_drc`, `verify_timing` |
| Standard cells | `cells_list`, `cells_search` |
| Depot | `depot_init` |
| System | `chip_status`, `chip_agentic` |
| Prefab | `show_chip_status_card`, … |

---

## Documentation stack

| Layer | Path |
|-------|------|
| README | `README.md` (cover + humor + warnings) |
| **Editorial** | **`docs/DREAMING_IN_SILICON.md`** |
| **Install** | **`INSTALL.md`** |
| FOSS CAD / RTL catalogs | `docs/FOSS_EDA_ECOSYSTEM.md`, `docs/FOSS_RTL_SOURCES.md` |
| **PRD** | **`docs/PRD.md`** |
| Changelog | `CHANGELOG.md` |
| Tool catalog | `docs/TOOLS.md` |
| Per-domain | `docs/tools/*.md` |
| Fabrication | `docs/FABRICATION_AND_FABS.md` |
| Webapp Help | `/help` + domain Overview/Help tabs |

---

## Fleet compliance checklist

| Requirement | Status |
|-------------|--------|
| `uv` + `uv.lock` + `justfile` | Yes |
| `llms.txt` + `llms-full.txt` | Yes |
| `webapp/start.ps1` + automated EDA (`install-eda.ps1`) | Yes |
| `just-starts/chip-design-mcp-start.bat` | Yes |
| Git + GitHub remote | Yes |
| [GIT_REPOSITORY_SAFETY](../../standards/GIT_REPOSITORY_SAFETY.md) | Documented (post-incident) |
| `GET /api/capabilities` + Prefab | Yes |
| CI + pre-commit | Yes |
| MCD project entry | This file |

---

## Related fleet repos

- **kicad-mcp** — PCB netlist bridge  
- **mcp-central-docs** — `chip_design_cad_sota.md`, `WEBAPP_PORTS.md` (11022/11023), `GIT_REPOSITORY_SAFETY.md`
