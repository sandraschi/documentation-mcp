# LeWM-MCP Integration (LeWorldModel)

## Overview

**LeWM-MCP** is a **FastMCP 3.2** fleet server that bridges **LeWorldModel (LeWM)** — a **Joint Embedding Predictive Architecture (JEPA)** world model trained **end-to-end from pixels** — into agentic IDEs and the glass dashboard.

**Primary literature:** Maes, Le Lidec, Scieur, LeCun, Balestriero — *LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels*, arXiv **[2603.19312](https://arxiv.org/abs/2603.19312)**.

**Upstream implementation:** [lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)  
**Project site:** [le-wm.github.io](https://le-wm.github.io/)  
**Repository:** `D:/Dev/repos/lewm-mcp`  
**Paper depot:** run `tools/ingest_lewm_paper.ps1` then query **arxiv-mcp** (`search_depot_corpus`)

## Why this matters

- **Compact:** ~15M parameters, single-GPU training (per paper).
- **Stable JEPA from pixels:** minimal loss set; planning and surprise evaluation.
- **MCP role:** orchestrates real `train.py` / `eval.py` subprocesses in upstream Python 3.10 venv — does not reimplement the model.

## Webapp & ports (fleet)

| Role | Port |
|------|------|
| FastAPI + MCP HTTP mount (`/mcp`) | **10927** |
| Vite dashboard (dev) | **10928** |

**Start:** `D:/Dev/repos/lewm-mcp/start.bat` or `webapp/start.ps1`.

## MCP surface

| Tool | Role |
|------|------|
| `lewm_world` | `health`, `train_prepare`, `train_run`, `infer_prepare`, `eval_run`, `checkpoint_list`, `job_status`, `job_stop`, `job_logs` |
| `lewm_status` | Device, upstream path, checkpoint flags |
| `lewm_agentic_workflow` | SEP-1577 planning (sampling when available) |

**Skill:** `skill://lewm-mcp/SKILL.md`

## Configuration

| Variable | Purpose |
|----------|---------|
| `LEWM_UPSTREAM_ROOT` | Path to `lucas-maes/le-wm` clone |
| `LEWM_STABLEWM_HOME` / `STABLEWM_HOME` | Checkpoints + datasets |
| `LEWM_DEVICE` | e.g. `cuda:0` |
| `LEWM_DRY_RUN` | `1` for test/CI without spawning GPU jobs |
| `LEWM_API_PORT` | Default **10927** |
| `LEWM_FRONTEND_PORT` | Default **10928** |

## Assets

1. `bootstrap_upstream.ps1` — upstream venv
2. `download_pusht_assets.ps1` — HF `quentinll/lewm-pusht` → `pusht/lewm_object.ckpt`
3. `download_pusht_assets.ps1 -WithDataset` — expert H5 for eval (~13 GB)
4. `ingest_lewm_paper.ps1` — arxiv-mcp corpus

## Central project doc

**[projects/lewm-mcp/README.md](../projects/lewm-mcp/README.md)**

## References

- [arXiv:2603.19312](https://arxiv.org/abs/2603.19312)
- [WEBAPP_PORTS registry](../operations/WEBAPP_PORTS.md)
- [Fleet registry JSON](../operations/fleet-registry.json)

---

*Last updated: 2026-06-06 · FastMCP 3.2 · fleet AI lane*
