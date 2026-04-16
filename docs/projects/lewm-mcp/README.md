# LeWM-MCP — Central project documentation

**Repo path:** `D:/Dev/repos/lewm-mcp`  
**Status:** scaffold + MCP tools + dashboard + fleet registration (upstream train/infer **wiring** is the next milestone)  
**Paper:** [arXiv:2603.19312](https://arxiv.org/abs/2603.19312) — *LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels*

## Mission

Provide a **standards-compliant** MCP bridge so the fleet can:

1. **Train** LeWM using the **official** codebase ([lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)) — single GPU, compact footprint.
2. **Infer** / plan / evaluate surprise in line with the paper — without pretending this repo reimplements the architecture.
3. **Prepare agentic loops** (SEP-1577): `lewm_agentic_workflow`, prompts, and `skill://lewm-mcp/SKILL.md`.

## Ports & layout

| Service | Port |
|---------|------|
| FastAPI (`/api/*`) + MCP HTTP (`/mcp`) | **10927** |
| Vite (glass dashboard) | **10928** |

`webapp/start.ps1` kills squatters, starts **uvicorn** on 10927, then **Vite** on 10928.

## Standards compliance

- **FastMCP 3.1+:** stdio for IDEs; HTTP streamable for local mesh; structured dict returns.
- **WEBAPP_STANDARDS:** ports in fleet reservoir; `start.ps1` + `start.bat`; dark glass UI baseline.
- **TOOL_DESIGN_STANDARDS:** portmanteau `lewm_world` to avoid tool explosion.
- **Implementation honesty:** tools return **prepare** / **health** until subprocess or Python hooks into `le-wm` are implemented; no fake metrics.

## Roadmap (suggested)

1. **Vendor path:** submodule or documented pin of `lucas-maes/le-wm` under `external/le-wm`.
2. **Train:** optional `LEWM_TRAIN_CMD` or Python entry that invokes upstream training with fleet env.
3. **Infer:** load checkpoint, expose rollout / surprise via tools (GPU mutex inside process).
4. **Sampling:** optional Anthropic sampling handler (same pattern as email-mcp) for headless plan refinement.

## Related docs

- Integration catalog: [integrations/lewm-mcp.md](../../integrations/lewm-mcp.md)
- Port registry: [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md)

---

*Maintained with the MCP Central Docs fleet — 2026-03-27*
