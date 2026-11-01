# Reversing MCP — status (fleet)

**Source of truth:** [sandraschi/reversing-mcp](https://github.com/sandraschi/reversing-mcp) · local `D:\Dev\repos\reversing-mcp`

## Snapshot (2026-10-12)

- **MCP:** FastMCP 3.4.8; **17 tools** (triage, PE, DKI, system, Prefab card, REA, Gym).
  **Does not ship ReVa tools** — ReVa is another server.
- **Gym G1:** job runner + stages 0/1/4, 6 REST endpoints, `gym` MCP tool, `/gym` page.
  Proven on Digibib5 (amber verdict). Stages 2,3,5-8 refuse honestly (pending-spec).
- **Assfix:** 0 → 86 SOTA (self-assessed) 2026-10-11; fakefind 6/6 fixed; ghaudit first
  run (0 HIGH); release v0.4.0 live (bundle + installer). Cold rescore still open.
- **Providers (verified):** Hopper unsupported on win32; Ghidra 12.0 present, 12.1 upgrade
  pending for REA; IDA BYO. Engine-free REA kinds unaffected.
- **Tier 3:** static correlation shipped (Digibib5 map, 171 hits); live tour = Gym stage 3.
- **TEXT.DKI:** resolved (Opus + Ghidra) — decoder/spec/gate in directmedia-mcp, whose
  webapp reads texts + book + TOC (RAG/polish phase there).
- **Vision:** [PRD.md](https://github.com/sandraschi/reversing-mcp/blob/main/PRD.md) (Gym product, G1-G4).

## Fleet docs in this folder

| File | Role |
|------|------|
| [README.md](./README.md) | Hub and upstream links |
| [STATUS.md](./STATUS.md) | This snapshot |
| [NEXT_STEPS.md](./NEXT_STEPS.md) | Current next steps |
| [CHANGELOG.md](./CHANGELOG.md) | Doc sync log for central-docs only |
| [DIGIBIB_STATUS.md](./DIGIBIB_STATUS.md) | **Mirror** of `reversing-mcp/docs/status.md` — Digibib5 / `Text.dki` notes |
