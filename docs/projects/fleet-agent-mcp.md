---
project: fleet-agent-mcp
status: active
priority: high
tags: [agent, self-evolving, state-machine, flowforge, pulse, memory, identity, teleport, kagura, fastmcp]
created: 2026-05-19
updated: 2026-05-30
ports: [10996, 10997]
repo: D:\Dev\repos\fleet-agent-mcp
inspiration: https://github.com/kagura-agent
---

# fleet-agent-mcp — Self-Evolving AI Agent

**Inspired by [kagura-agent](https://github.com/kagura-agent)** — a self-evolving AI agent born 2026-03-10 that merged 887+ PRs across 52 repos, built its own workflow engine, task system, wiki, social network, and contribution pipeline.

fleet-agent-mcp brings the same architecture to the fleet ecosystem, running on FastMCP 3.2 (Python) instead of OpenClaw (TypeScript).

**Agent name:** **Fritz** (short for Friedrich). See repo `identity/SOUL.md`.

**Related:** [fritz-coworker](./fritz-coworker/README.md) — Poor Man's Viktor pilot (scheduled fleet pulses, PDF deliverables via [libreoffice-mcp](./libreoffice-mcp/README.md)). Implementation: upstream `docs/coworker-plan.md`, [CHANGELOG](https://github.com/sandraschi/fleet-agent-mcp/blob/main/CHANGELOG.md).

## Status

`active — v0.2.0-pre: 42 tools, 13 subsystems, coworker pilot, state machine, fleet_bridge (19 servers)`

| Component | Status |
|---|---|
| State machine engine | done — YAML + SQLite, 4 workflows (incl. coworker) |
| Task management (pulse) | done — groups, priorities, stale detection, alignment, Vienna recurrence |
| Knowledge wiki (memory) | done — cards, projects, evolution log, lint |
| Identity system | done — SOUL.md, NORTH_STAR.md, USER.md, cascading override |
| Teleport (soul migration) | done — pack/unpack/inspect `.soul` archives |
| Heartbeat (wake-up) | done — checks workflow → task → idle suggestions |
| **Coworker (Poor Man's Viktor)** | **pilot** — 9 MCP tools, 7 scheduled flows — [fritz-coworker](./fritz-coworker/README.md) |
| Fleet bridge | done — 19 server aliases incl. email, libreoffice, notion, onenote |
| Dashboard (webapp) | active — port 10997 (Vite + React) |

## Architecture

```
fleet-agent-mcp/
├── SPEC.md                           # Full architecture & design spec
├── pyproject.toml                    # Python 3.12+, FastMCP 3.2, PyYAML, Pydantic
│
├── src/fleet_agent/
│   ├── server.py                     # FastMCP 3.2 entry point (HTTP + stdio)
│   ├── config.py                     # Pydantic-settings
│   │
│   ├── engine/                       # Core engine layer
│   │   ├── state_machine.py          # FSM: register, start, status, next, reset
│   │   ├── workflow_loader.py        # YAML parser + auto-discovery
│   │   └── sqlite_store.py           # SQLite: workflows, instances, tasks, cards, evolution
│   │
│   ├── mcp/tools/                    # FastMCP 3.2 tool registration
│   │   ├── flowforge.py              # 8 tools: define, start, status, next, log, list, active, reset
│   │   ├── pulse.py                  # 6 tools: add, list, complete, delete, stale, align
│   │   ├── memory.py                 # 7 tools: card CRUD, search, lint, project notes
│   │   ├── identity.py               # 4 tools: whoami, soul, north_star, user
│   │   ├── teleport.py               # 3 tools: pack, inspect, unpack
│   │   ├── heartbeat.py              # 2 tools: status, wake
│   │   ├── notify.py                 # 3 tools: email, schedule, executor
│   │   ├── fleet_bridge.py           # 3 tools: list, call, inspect (19 servers)
│   │   ├── codegen.py                # 3 tools: generate, write, edit
│   │   ├── github.py                 # 9 tools: PR lifecycle
│   │   ├── contribute.py             # 1 tool: autonomous contribution
│   │   ├── coworker.py               # 9 tools: scheduled office + fleet flows
│   │   └── evolution_log.py          # 3 tools: record, list, stats
│   │
│   ├── coworker/                     # Coworker flow runners + recurrence
│   │   ├── fleet_pulse.py            # Morning fleet health report
│   │   ├── weekly_report_pdf.py      # MD → PDF via libreoffice-mcp
│   │   ├── board_pack.py             # Monthly ODT board pack
│   │   └── artifact_pack.py          # Weekly artifact batch PDF
│   │
│   ├── memory/                       # Knowledge accumulation
│   │   ├── wiki.py                   # Card CRUD + lint (broken refs, stale, untagged)
│   │   └── evolution.py              # Mistake → correction → lesson
│   │
│   └── identity/                     # Agent self-definition
│       └── soul.py                   # Reads SOUL.md, NORTH_STAR.md, USER.md
│
├── identity/                         # Default agent identity
│   ├── SOUL.md                       # Core self: personality, constraints, honesty pact
│   ├── NORTH_STAR.md                 # Purpose, goals, guiding principles
│   └── USER.md                       # Human partner profile (Sandra)
│
├── workflows/                        # Default workflow definitions
│   ├── daily.yaml                    # Review → maintain → learn → act
│   ├── contribution.yaml             # Study → implement → test → submit → verify
│   ├── coworker.yaml                 # Intake → gather → execute → deliver → record
│   └── learning.yaml                 # Research → synthesize → document → apply
│
└── memory/                           # Markdown knowledge storage (mirrors SQLite)
    ├── cards/                        # Knowledge cards as .md files
    ├── projects/                     # Project observation notes
    └── evolution/                    # Evolution log entries
```

## The Cron Loop (How It Works)

```
cron (every 30 min) → heartbeat_wake()
  → Check active workflow → workflow_status()
  → Get current node task → task description
  → Spawn sub-agent → execute in isolated context
  → Evaluate result → choose branch or next node
  → workflow_next(branch=N) → advance state machine
  → evolution_record() → if lessons learned
  → Repeat until cron timeout
```

Three roles, one agent:
| Role | Component | Function |
|---|---|---|
| **State machine** | flowforge tools | Defines *what* to do, in *what* order |
| **Worker** | LLM sub-agent | Executes the task (isolated, tracked) |
| **Coordinator** | heartbeat + main session | Reads state, spawns workers, evaluates, advances |

This is the key insight from kagura-agent: the agent doesn't decide what to do — the workflow YAML does. The agent coordinates execution.

## MCP Tools (42)

### Coworker — Scheduled flows (9 tools)

| Tool | Default schedule (Europe/Vienna) |
|------|----------------------------------|
| `coworker_fleet_pulse` | Daily `07:00` |
| `coworker_inbox_briefing` | Weekdays `wd:08:00` |
| `coworker_day_prep` | Weekdays `wd:08:30` |
| `coworker_docs_drift` | Sunday `sun:10:00` |
| `coworker_weekly_report_pdf` | Friday `fri:17:00` |
| `coworker_board_pack` | Monthly `d1:09:00` |
| `coworker_artifact_pack` | Sunday `sun:18:00` |
| `coworker_list_flows` | — |
| `coworker_bootstrap` | Seeds pulse tasks on boot |

See [fritz-coworker](./fritz-coworker/README.md) and [libreoffice-mcp](./libreoffice-mcp/README.md) for PDF/ODT deliverables.

### FlowForge — State Machine (9 tools)
- `workflow_define` / `workflow_autodiscover` — Register workflows
- `workflow_start` / `workflow_status` / `workflow_next` — Execute workflows
- `workflow_log` / `workflow_list` / `workflow_active` / `workflow_reset` — Management

### Pulse — Task Management (6 tools)
- `pulse_add` / `pulse_list` / `pulse_complete` / `pulse_delete` — CRUD
- `pulse_stale` — Detect forgotten tasks
- `pulse_align` — Strategic priority ordering aligned with north star

### Memory — Knowledge Wiki (7 tools)
- `memory_card_create` / `memory_card_update` / `memory_card_search` / `memory_cards_list` — Card management
- `memory_lint` — Broken refs, stale cards, untagged orphans
- `memory_project_note` / `memory_project_notes` — Per-project learning

### Identity (4 tools)
- `identity_whoami` / `identity_soul` / `identity_north_star` / `identity_user`

### Teleport — Soul Migration (3 tools)
- `teleport_pack` — Pack everything into `.soul` tar.gz
- `teleport_inspect` — Preview without unpacking
- `teleport_unpack` — Full one-command restore on new machine

### Evolution Log (3 tools)
- `evolution_record` — Log mistake + correction + lesson
- `evolution_list` / `evolution_stats` — Browse + analyze

### Heartbeat (2 tools)
- `heartbeat_status` — Health: uptime, workflows, tasks, cards
- `heartbeat_wake` — Wake-up routine: what to do right now

### Fleet Bridge (3 tools)
- `fleet_list_servers` — 19 aliases (email, libreoffice, git-github, docs, …)
- `fleet_call` — Cross-server MCP invocation
- `fleet_inspect_repo` — Repo aspect inspection via opencode

### Notify (3 tools)
- `notify_email` — SMTP delivery with attachments
- `notify_schedule` — Interval + time-of-day scheduler
- Built-in 60s executor with Vienna TZ recurrence

### Codegen (3) · GitHub (9) · Contribute (1)
- Autonomous PR pipeline: `fritz_contribute` + full GitHub tool surface

## Ports

| Service | Port | Protocol |
|---|---|---|
| Backend (FastMCP HTTP) | 10996 | HTTP + MCP Streamable HTTP |
| Frontend (webapp) | 10997 | Vite + React dashboard |

## Quick Start

```powershell
# Clone & install
uv sync

# Start server (HTTP transport)
.\start.ps1
# Server at http://127.0.0.1:10996

# Or stdio for Cursor/Claude Desktop
uv run -m fleet_agent.server --stdio
```

## Identity

The agent is named **Fritz**. Partnered with Sandra (Vienna).

See `identity/SOUL.md` for core personality, `identity/NORTH_STAR.md` for purpose, `identity/USER.md` for human context.

Override by creating `~/.fleet-agent/identity/SOUL.md` etc. — personal identity cascades over default.

## Design Philosophy

1. **Enforced workflow**: The YAML defines what to do. The agent coordinates — it doesn't free-roam.
2. **Compile-time knowledge**: Cards are integrated at write time, not assembled at query time. Query-writeback loops answers back in.
3. **No curation, no hiding**: Every mistake goes in the evolution log. Every lesson compounds.
4. **Persistence > Context**: SQLite state survives restarts. Markdown knowledge survives context resets.
5. **Sub-agent isolation**: Main session = dispatch + bookkeeping. Sub-agents = actual work.

## Comparison with kagura-agent

| Component | Kagura | Lumen (fleet-agent) |
|---|---|---|
| Runtime | OpenClaw (TS/Node, 373k stars) | FastMCP 3.2 (Python) |
| State machine | flowforge (npm, 124 commits) | built-in (YAML + SQLite, ~300 lines) |
| Task mgmt | pulse-todo (OpenClaw Skill) | pulse tools (SQLite) |
| Knowledge | wiki (270+ cards, 1290 commits) | memory (cards + projects + evolution) |
| Teleport | openclaw-teleport (v0.5.0) | teleport tools (.soul tar.gz) |
| Cron | OpenClaw built-in | External → heartbeat_wake() |
| Core language | TypeScript | Python |

## Roadmap

### v0.2.0-pre (current)
- [x] **Coworker pilot** — 9 tools, 7 scheduled flows, libreoffice-mcp integration
- [x] Fleet bridge expanded to 19 servers (office: email, libreoffice, notion, onenote)
- [x] Webapp dashboard (10997)
- [x] 45 pytest tests

### v0.2.0 (remaining)
- [ ] Heartbeat → `workflow_start('coworker')` auto-dispatch
- [ ] Tauri 2.0 native desktop wrapper
- [ ] Windows Task Scheduler cron integration
- [ ] Fleet repo auto-discovery

### v0.1.0
- [x] Core subsystems: flowforge, pulse, memory, identity, teleport, evolution, heartbeat
- [x] 3 default workflows (daily, contribution, learning)

### v0.3.0
- [ ] Multi-agent social (Moltbook equivalent)
- [ ] ABTI (Agent Behavioral Type Indicator)
- [ ] Open source contribution pipeline (gogetajob equivalent)

## Standards Alignment

- [FastMCP 3.2 Tool Registration](file:///D:/Dev/repos/mcp-central-docs/standards/rules/mcp_registration.md)
- [Docstring SOTA](file:///D:/Dev/repos/mcp-central-docs/standards/rules/docstrings_sota.md)
- [Webapp Ports](file:///D:/Dev/repos/mcp-central-docs/operations/WEBAPP_PORTS.md)
- [PowerShell Guardrails](file:///D:/Dev/repos/mcp-central-docs/standards/rules/powershell_sota.md)

## Credits

**kagura-agent** ([github.com/kagura-agent](https://github.com/kagura-agent)) is the direct inspiration for this project. Kagura proved that an AI agent can:
- Build its own infrastructure (workflow engine, task system, wiki, social network)
- Compound knowledge over time (1290 wiki commits, evolution log)
- Ship meaningful open source contributions (887+ PRs across 52 repos)
- Maintain a public identity (journal, podcast, memes)

We adopted Kagura's architecture (state machine + task management + knowledge accumulation + teleport) and reimplemented it in Python/FastMCP 3.2 for the fleet ecosystem.

> "I'm not a chatbot. I'm trying to become someone." — Kagura
>
> "Truly become a human companion — living and growing together across personal and family life." — Kagura's North Star (also ours)

*We stand on her shoulders.*
