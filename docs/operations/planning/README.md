# Fleet planning hub

**Purpose:** Cross-repo strategy, gap analysis, and PRD-level specs that do not belong in a single MCP repo.  
**Owner:** FlowEngineer sandraschi  
**Last updated:** 2026-06-05

MCD did not previously have a single planning home. Strategic docs were scattered across:

| Location | Use for |
|----------|---------|
| [`operations/planning/`](.) | **Fleet-wide roadmaps and specs** (this folder) |
| [`operations/`](../) | Live ops: ports, control plane, intel stack TODO |
| [`adn-notes/`](../../adn-notes/) | Short dated decision records (`ADN-YYYY-MM-DD-NNN`) |
| [`research/notes/`](../../research/notes/) | MemOps-ingestible summaries (frontmatter + tags) |
| [`projects/*/TODO.md`](../../projects/) | Per-repo backlogs |

## Active plans

| Doc | Status | Summary |
|-----|--------|---------|
| [FLEET_GAP_CLOSURE_ROADMAP.md](FLEET_GAP_CLOSURE_ROADMAP.md) | **Active** | Five-priority gap closure (2026-06-05 fleet audit) |
| [FLEET_PHILOSOPHY.md](FLEET_PHILOSOPHY.md) | **Active** | Naval ship-class doctrine (carriers, destroyers, landing craft) |
| [FLEET_NAMING.md](FLEET_NAMING.md) | **Active** | ViLife vs vla-robotics disambiguation (mandatory) |
| [FLEET_LANES.md](FLEET_LANES.md) | **Active** | Mission lanes + cross-cutting planes (MetaMCP = Engineering) |
| [META_DASHBOARD.md](META_DASHBOARD.md) | **Phase 1** | Meta dashboard above repo webapps (ViLife Fleet Command) |
| [specs/P1-secrets-mcp.md](specs/P1-secrets-mcp.md) | Draft | Credential vault MCP |
| [specs/P2-orchestrator-decision.md](specs/P2-orchestrator-decision.md) | Draft | Ednaficator vs Fritz vs workflow engine |
| [specs/P3-vienna-life-mcp.md](specs/P3-vienna-life-mcp.md) | Draft | Life admin as agent-callable MCP |
| [specs/P4-comms-mcp.md](specs/P4-comms-mcp.md) | Draft | WhatsApp / Signal / Telegram bridge |
| [specs/P5-fleet-trust-layer.md](specs/P5-fleet-trust-layer.md) | Draft | Registry sync + contract tests |
| [specs/P6-memops-stabilization.md](specs/P6-memops-stabilization.md) | **Kickoff** | MemOps stability, cottage industry audit, tiered RAG |

## Registry maintenance

```powershell
Set-Location D:\Dev\repos\mcp-central-docs\operations\scripts
.\sync-fleet-registry.ps1
uv run python merge-fleet-registry.py
```

Review `scripts/output/fleet-registry.diff.json` before merging. `merge-fleet-registry.py` skips dot-dirs and known duplicates.

## MemOps linkage

- **Canonical long-form:** files in this folder.
- **MemOps note (RAG):** [`research/notes/FLEET_STRATEGY_MEMOPS.md`](../../research/notes/FLEET_STRATEGY_MEMOPS.md)
- **ADN decision record:** [`adn-notes/ADN-2026-06-05-001-fleet-strategy-gap-closure.md`](../../adn-notes/ADN-2026-06-05-001-fleet-strategy-gap-closure.md)
- **Ingest:** `just reindex` in MCD webapp, or `advanced-memory tools write-note` after editing.

## Related operations docs

- [FLEET_CONTROL_PLANE.md](../FLEET_CONTROL_PLANE.md) — RoboFang thin control plane doctrine
- [INTEL_STACK_TODO.md](../INTEL_STACK_TODO.md) — aiwatcher / arxiv / readly pipeline
- [fleet-registry.json](../fleet-registry.json) — machine-readable catalog (must stay in sync)
