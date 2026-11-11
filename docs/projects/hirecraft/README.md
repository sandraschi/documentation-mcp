# HireCraft

**Version**: v0.1.0 (2026-11-10) — Sovereign Applicant Tracking System (ATS), blind scorecards, and automated employee onboarding engine.

## Ports

| Port | Service |
|------|---------|
| — | Native desktop GUI (`hirecraft-app`) & Stdio JSON-RPC MCP server (`hirecraft-mcp`) |

## Architecture

```
hirecraft-store (SQLite WAL) <--- hirecraft-core (Pipeline & Onboarding Cascade)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
         hirecraft-mcp (L1/L2)                       hirecraft-app (L3 GUI)
```

## Tools

| Tool | Ops | Covers |
|------|-----|--------|
| `hire_status` | Query | Overview of open requisitions and candidate counts |
| `hire_req_create` | Mutation | Job requisition creation with headcount & salary |
| `hire_req_list` | Query | List active job requisitions |
| `hire_candidate_create` | Mutation | Candidate profile intake |
| `hire_candidate_show` | Query | Candidate stage history and scorecard ratings |
| `hire_candidate_stage` | Mutation | Funnel stage progression |
| `hire_candidate_hire` | Mutation | Transition to Hired, trigger fleet onboarding |
| `hire_scorecard_add` | Mutation | Blind quantitative scorecard evaluation |

## Quick Start

```powershell
# Smoke check
mcp-central-docs\starts\hirecraft-start.bat --smoke

# Launch native desktop app
mcp-central-docs\starts\hirecraft-start.bat
```

## Status

- **v0.1.0** — Shipped. Pure Rust 4-crate workspace, blind scorecards, automated onboarding cascade.

## Links

- **Repository**: [hirecraft](file:///D:/Dev/repos/hirecraft)
- **Spoke Assessment**: [hirecraft.md](../craft-fleet/hirecraft.md)
