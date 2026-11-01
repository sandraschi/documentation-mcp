# Current Plans — June 2026

## Active

| Repo | Focus | Status |
|------|-------|--------|
| **scraper-mcp** | Grade aggregation, ToolBench/Glama/LobeHub | Add trend chart to dashboard frontend |
| **llm-gateway** | Standalone 28-provider AI gateway at :10916 | Just extracted from local-llm-mcp |
| **local-lll-mcp** | LLM server with gateway wiring | Gateway wired into server.py |
| **aiwatcher-mcp** | Fleet news ingestion, alert hub | Grade drop alerts from scraper-mcp |

## Queued

- **Tauri NSIS rollout** — all webapp repos
  - `mcd/scripts/scaffold-tauri.ps1` with modes: scaffold, dryrun, undo, build, test
  - meta-mcp tool: `scaffold_tauri_nsis` (in scaffolding suite)
  - Plan: meta-mcp webapp "Tauri Build" subpage for one-click build/test
  - Priority: most used/important first
  - Infrastructure tier skips: secrets-mcp, depot-mcp, local-llm-mcp, monitoring-mcp, fleet-agent-mcp
- **Trend chart** in scraper-mcp dashboard (use `/api/trends`)
- More repos adopting `llm-gateway` (email-mcp, aiwatcher-mcp, arr-mcp)

## Cycle

Work on minipc (Desktop-nftmvf1) when goliath retired. Always push before switching.
