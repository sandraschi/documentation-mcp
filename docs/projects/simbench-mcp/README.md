# simbench-mcp — Cross-Simulator Benchmark Layer

**Status:** Build brief ready — repo NOT yet created
**Priority:** P4 (after mathops-mcp, codecad-mcp)

| Item | Details |
|------|---------|
| **Repo** | `D:\Dev\repos\simbench-mcp` (not yet scaffolded) |
| **Brief source** | `architecture/FLEET_GAP_ANALYSIS_2026-07.md` §6 |
| **Stack** | FastMCP 3.2+, SQLite, YAML task definitions |
| **Depends on** | mathops-mcp (success predicate eval), all 5 sim servers (as HTTP/MCP clients) |
| **Consumed by** | Boomy nav (sim-to-real validation) |

## Why

Five sim servers (mujoco, gazebo, isaac, unitree, limx) share the 14-tool pattern but nothing runs the same task across two of them, and results evaporate. This layer turns sims from viewers into instruments — a shared task definition, results database, and cross-sim comparison report.

## Design

```
simbench-mcp
  ├── tasks/*.yaml        — Shared task definitions
  ├── adapters/           — One module per sim (calls its HTTP /mcp interface)
  ├── results.db          — SQLite: run id, task, sim, metrics, artifacts
  └── reports/            — Generated markdown comparison reports
```

Task schema: robot description ref, initial state, success predicate (expression over observable state), metrics (time-to-success, energy proxy, path length), timeout, per-sim adapter hints.

Adapters translate generic task schema into each sim's job submission format. Missing capability (e.g. a sensor a sim lacks) → structured `SKIPPED(reason)`, never fake pass.

## Tools

| Tool | Ops |
|------|-----|
| `bench_task` | list, validate, create |
| `bench_run` | task × sim matrix as background jobs |
| `bench_results` | query, compare, export CSV |
| `bench_report` | generate markdown comparison report |

## Seed Tasks (v0.1 — 5)

1. `pendulum_swing_up` — classic, all sims
2. `go2_stand` — unitree
3. `tron1_balance` — limx
4. `pick_free_fall` — object drop + settle; physics determinism probe (expect cross-sim divergence, that's the point)
5. `wheeled_line_follow` — transfers conceptually to Boomy (§7 N1)

## Acceptance

`bench_run pendulum_swing_up --sims mujoco,gazebo` produces a comparison report with both entries populated from REAL sim runs (verify by artifact presence). CI runs task validation only (sims not in CI).
