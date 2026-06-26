# LeWM-MCP — Central project documentation

**Repo path:** `D:/Dev/repos/lewm-mcp`  
**Status:** v0.2.1 — real upstream train/eval subprocess bridge + fleet SOTA webapp  
**Paper:** [arXiv:2603.19312](https://arxiv.org/abs/2603.19312) — *LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels*  
**Depot:** ingest via `lewm-mcp/tools/ingest_lewm_paper.ps1` → search in **arxiv-mcp**

## Mission

Provide a **standards-compliant** MCP bridge so the fleet can:

1. **Train** LeWM using the **official** codebase ([lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)) — single GPU, compact footprint.
2. **Eval** pretrained PushT policy via supervised `eval.py` jobs.
3. **Prepare agentic loops** (SEP-1577): `lewm_agentic_workflow`, prompts, and `skill://lewm-mcp/SKILL.md`.

## Ports & layout

| Service | Port |
|---------|------|
| FastAPI (`/api/*`) + MCP HTTP (`/mcp`) | **10927** |
| Vite (glass dashboard) | **10928** |

`start.bat` → `webapp/start.ps1`: uv sync, smoke import, health wait on `/api/health`, Vite on 10928.

## Standards compliance

- **FastMCP 3.2:** stdio for IDEs; HTTP streamable on backend `/mcp`; structured dict returns.
- **WEBAPP_STANDARDS:** fleet ports; `webapp/start.ps1` + root `start.bat`; dark glass UI.
- **TOOL_DESIGN_STANDARDS:** portmanteau `lewm_world`.
- **Paper repos:** arxiv-mcp ingest script for 2603.19312.

## Operations

| Script | Purpose |
|--------|---------|
| `tools/bootstrap_upstream.ps1` | Clone le-wm + Python 3.10 venv |
| `tools/download_pusht_assets.ps1` | HF checkpoint + convert to `lewm_object.ckpt` |
| `tools/ingest_lewm_paper.ps1` | arxiv-mcp depot |
| `webapp/start.ps1` | Full stack launcher |

## Roadmap (v0.3+)

- Rollout / surprise tools wired to upstream
- Optional sampling handler for agentic workflow
- google-ai-mcp proxy hardening

## Related docs

- Integration catalog: [integrations/lewm-mcp.md](../../integrations/lewm-mcp.md)
- Port registry: [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)
- Repo docs: `lewm-mcp/docs/PRD.md`

---

*Maintained with the MCP Central Docs fleet — 2026-06-06*
