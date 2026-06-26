---
title: Fleet strategy — gap closure and operating model (2026-06-05)
status: active
tags: [fleet, strategy, memops, planning, robofang, secrets, orchestrator, vienna-life, comms, trust, gap-closure]
source: operations/planning/FLEET_GAP_CLOSURE_ROADMAP.md
related:
  - operations/planning/specs/P1-secrets-mcp.md
  - operations/planning/specs/P2-orchestrator-decision.md
  - operations/planning/specs/P3-vienna-life-mcp.md
  - operations/planning/specs/P4-comms-mcp.md
  - operations/planning/specs/P5-fleet-trust-layer.md
---

# Fleet strategy — MemOps note

## One-line thesis

~120 MCP servers = personal AI OS; **missing glue, trust, and life APIs** — not more domain tools.

## Operating model shift

| Before | After (2026 H2) |
|--------|-----------------|
| Add MCP per discovered app | Depth over breadth gate |
| Credentials in config.yaml | secrets-mcp refs + audit |
| Agents improvise multi-step | Fritz YAML + ednaficator UI |
| VLA = human webapp only | vienna_life MCP tools |
| MemOps underused | Note after every fleet planning session |

## Five priorities (ordered)

1. **P5 trust** — registry sync, mcp-test-suite, quarantine runts (start now)
2. **P1 secrets-mcp** — Bitwarden CLI, audit_fleet, no values in tool returns
3. **P2 orchestrator** — revive ednaficator as chat shell; Fritz owns YAML workflows; decision gate 2026-06-20
4. **P3 vienna-life MCP** — calendar/todos/expenses/shopping as `vienna_life` portmanteau on existing backend
5. **P4 comms-mcp** — Telegram v0.1, then Signal/Slack, WhatsApp later

## Quarantine now

`sdr-mcp`, `vbox-mcp`, `mcp-links-service`; `ednaficator` → reviving pending P2.

## Golden workflows (Fritz)

- **WF-001** morning brief: glance → aiwatcher → vienna_life → pulse → memops
- **WF-002** media: plex/jellyfin → arr → play
- **WF-003** research: arxiv → readly match → aiwatcher → calibre

## Phase 2 deferred

Meta-knowledge hub, health-mcp, spotify-mcp, at-egov-mcp, iac-mcp, ios-bridge.

## Registry facts (2026-06-05)

- ~195 top-level dirs, ~167 meaningful repos, ~121 *-mcp
- fleet-registry.json: 119 entries (~58 gap)
- Gold Standard: advanced-memory, devices-mcp, virtualization-mcp

## Naval doctrine (2026-06-05)

- **Carriers:** vienna-life-assistant (human flag), robofang (agent ops), meta_mcp (engineering)
- **Destroyers:** domain MCPs (plex, blender, devices, …)
- **Landing craft:** Fritz workflows (WF-001..003)
- **Minesweepers:** mcp-test-suite, sync-fleet-registry.ps1, secrets-mcp (planned)
- **Meta dashboard:** VLA `/fleet` — L3 above individual web_sota (L2)

## MemOps hygiene (reminder)

After significant fleet work, write ADN + this note pattern. Ingest: MCD `just reindex` or `advanced-memory tools write-note`. Wire RoboFang `journal_bridge` → advanced-memory when running council sessions.

## Relations

- implements [[FLEET_CONTROL_PLANE]] thin orchestration doctrine
- blocks [[devices-mcp]] credential cleanup until P1
- unblocks [[fleet-agent-mcp]] WF-001 when P3 ships
