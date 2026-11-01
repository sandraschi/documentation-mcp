# ADN-2026-06-05-001 — Fleet strategy gap closure

**Decision:** Stop breadth-first MCP additions until trust + glue + life APIs land.  
**Author:** Cursor fleet audit session  
**Status:** Accepted

## Context

Fleet at ~200 repos with exceptional domain coverage (robotics, CAD, media, VR, research). Agents cannot reliably operate daily life or chained workflows. MemOps (advanced-memory) underused for strategy persistence.

## Decision

1. Create MCD **`operations/planning/`** as canonical planning home (was scattered).
2. Execute five priorities: P5 → P1 → P2 → P3/P4 parallel.
3. **Orchestrator:** Hybrid — Fritz YAML workflows + revive ednaficator as conversational launcher (not second engine). Decision gate **2026-06-20**.
4. **Quarantine** runts in registry: sdr-mcp, vbox-mcp, mcp-links-service.
5. **MemOps:** Every planning change gets `research/notes/FLEET_STRATEGY_MEMOPS.md` update + ADN.

## Consequences

- New domain MCPs require P1+P5 Phase 1 complete (policy, not tooling block).
- vienna-life-assistant gains `/mcp` surface instead of new life repo.
- comms-mcp Telegram-first; WhatsApp deferred.

## Links

- [FLEET_GAP_CLOSURE_ROADMAP.md](../operations/planning/FLEET_GAP_CLOSURE_ROADMAP.md)
- [FLEET_STRATEGY_MEMOPS.md](../research/notes/FLEET_STRATEGY_MEMOPS.md)
