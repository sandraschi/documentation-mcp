---
project: fleet-agent-mcp
status: active
priority: high
tags: [agent, self-evolving, state-machine, flowforge, pulse, memory, identity, teleport, kagura, fastmcp, harness, mechanical-gates, opc, sfb, discord, surveillance]
created: 2026-05-19
updated: 2026-09-08
ports: [10996, 10997, 11027]
repo: D:\Dev\repos\fleet-agent-mcp
inspiration: https://github.com/kagura-agent
---

# fleet-agent-mcp — Self-Evolving AI Agent

**Inspired by [kagura-agent](https://github.com/kagura-agent)** — a self-evolving AI agent born 2026-03-10 that merged 887+ PRs across 52 repos, built its own workflow engine, task system, wiki, social network, and contribution pipeline.

**Mechanical gates inspired by [OPC](https://github.com/iamtouchskyer/opc) (One Person Company, 173★)** — a Claude Code skill that proved "the agent that builds never evaluates." OPC's `opc-harness synthesize` computes verdicts by code (emoji severity counting, file ref validation) rather than LLM judgment. We ported the mechanical gate engine pattern to Python at `src/fleet_agent/harness/gate_engine.py` — see the [Harness — Mechanical Gate Engine](#harness--mechanical-gate-engine) section below.

fleet-agent-mcp brings the same architecture to the fleet ecosystem, running on FastMCP 3.2 (Python) instead of OpenClaw (TypeScript).

**Agent name:** **Fritz** (short for Friedrich). See repo `identity/SOUL.md`.

**Related:** [fritz-coworker](./fritz-coworker/README.md) — Poor Man's Viktor pilot (scheduled fleet pulses, PDF deliverables via [libreoffice-mcp](./libreoffice-mcp/README.md)). Implementation: upstream `docs/coworker-plan.md`, [CHANGELOG](https://github.com/sandraschi/fleet-agent-mcp/blob/main/CHANGELOG.md).

## Status

`active — v0.2.4 (2026-09-08): 103 tools (verified — see below), 24 tool subsystems, Intel Hub (11027), coworker + home-safety watch (16 flows), fleet_bridge (20 servers incl. devices), SFB Discord comms layer (P2), improved contribution pipeline (job_finder.py), stuck-loop reaper hardening`

**2026-09-08 session (major)**: fixed a real production incident — a leftover test workflow instance had been looping forever (since 2026-08-30) and starving the real task queue for over a week, permanently pinning VRAM. Root-caused, fixed (hard-ceiling reaper in `agentic_loop.py`, test-DB isolation via `tests/conftest.py`), and used the same session to substantially rebuild the contribution pipeline: own-repo push mode (no fork needed), a `gemma4:12b` LLM-timeout root-cause fix (`"think": false` on Ollama calls — a verbose reasoning trace was pushing real prompts past the timeout for no benefit, since nothing reads the thinking output), an expanded no-LLM fallback safety net, and a new `job_finder.py` module that replaces gogetajob's label-only issue classification with real local-LLM analysis (age/maintainer-engagement signal, unlinted-repo proactive scanning, a genuinely non-preachy friendly-issue generator). Landed two real dogfood PRs (own repo + a purpose-built test fixture), both end-to-end automated. Full writeup: memops note "Fritz Contribution and Job-Finder Pipeline" and "Taming the VRAM — Fritz Stuck-Loop Bug".

**Full re-audit, same session**: SPEC.md's tool inventory had drifted badly — it documented 7 of the repo's 24 actual tool-registering modules (roughly a fifth of the real surface) and was internally inconsistent even within those (header said "21 tools", FlowForge's own subsection listed 9 tools under an "(8 tools)" heading, real count is 12). Re-audited every module directly (`@mcp.tool` grep cross-checked against the live server's `tool_count`) and rewrote SPEC.md §5 to cover all 24 modules / 103 tools. One real bug found in the process: `agentic.py` (`agentic_start`/`stop`/`status` — manual control of the main loop) had never been imported into `mcp/tools/__init__.py`, so those 3 tools existed in source with `@mcp.tool` decorators but were never actually registered — fixed, live count went 100 → 103.

**New doc, same session**: [`docs/AGENT_ARCHITECTURE_AND_SAFETY.md`](https://github.com/sandraschi/fleet-agent-mcp/blob/main/docs/AGENT_ARCHITECTURE_AND_SAFETY.md) — answers a direct question asked this session: does Fritz actually release, control, and supervise sub-agents? At the time of writing: **no**. Investigated all three real execution paths (coworker flows run in-process; ad-hoc task routing is one stateless LLM completion; flowforge "agent" nodes made one fire-and-forget call to a separate service, `cline-mcp`, which itself has real session/team primitives — `agent_session_start/status/stop`, `agent_team_run` — that weren't being used, and which wasn't even running when checked).

**Built the same day**: the flowforge "agent" node path now uses cline-mcp's real session API instead of one-shot `agent_run` — start/poll/abort across separate agentic-loop ticks, real token/cost accounting recovered from the session output, failed/timed-out sessions now trigger the existing anti-spin guard (`sm.failure_record()`) instead of silently advancing. Verified end-to-end against a live cline-mcp instance (had to be started manually — it isn't NSSM-managed yet, a noted remaining gap). Found and fixed one real bug in the process: aborting a session doesn't flip cline-mcp's outer status to "stopped" — the real outcome is nested at `output.status` and would have been misread as a successful completion otherwise. `v0.2.5`, see CHANGELOG.md.

| Component | Status |
|---|---|
| State machine engine | done — YAML + SQLite, 4 workflows (incl. coworker); **hardened 2026-09-08**: `_reap_if_stalled()` hard ceiling (age/cycle-count) prevents any future instance from starving the task queue the way the 2026-08-30 incident did |
| Task management (pulse) | done — groups, priorities, stale detection, alignment, Vienna recurrence |
| Knowledge wiki (memory) | done — cards, projects, evolution log, lint |
| Identity system | done — SOUL.md, NORTH_STAR.md, USER.md, cascading override |
| Teleport (soul migration) | done — pack/unpack/inspect `.soul` archives |
| Heartbeat (wake-up) | done — checks workflow → task → idle suggestions |
| **Harness — Mechanical Gate Engine** | **done** — `harness/gate_engine.py`: deterministic verdict synthesis, criteria lint, review independence, oscillation detection, tier coverage |
| **Coworker (Poor Man's Viktor)** | **pilot** — 11 MCP tools, 9 scheduled flows — [fritz-coworker](./fritz-coworker/README.md) |
| **Intel Reports Hub** | **done** — port 11027, publish/list, iPad/Tailscale — `docs/INTEL_REPORTS_HUB.md` |
| **AIWatcher ingest** | **done** — auto after Pulse/Day Prep; `aiwatcher_push_event` |
| **Urgent notifications** | **done** — email + cursor inbox on degradation / home safety |
| Fleet bridge | done — 20 server aliases incl. email, libreoffice, devices, notion, onenote |
| Dashboard (webapp) | active — port 10997 (Vite + React). **2026-09-08**: Tasks page got search/filter/sort/CSV export (was a flat unsorted list); Automaton page's stats bug fixed (`/api/status` shape mismatch caused literal "?" display) + schedule board got search/sort/pagination; sidebar collapse toggle moved to a top-header chevron (was a bottom text button); Contributions/PRs page got a "Find Work" panel (target-a-repo + auto-crawler modes) |
| **Stigmergic Swarm & r11n** | **proposal / v0.3.0 (2026-11-02)** — see [STIGMERGIC_SWARM_R11N.md](./fritz-coworker/STIGMERGIC_SWARM_R11N.md): environment-mediated stigmergic coordination, `.r11n/` atomic claims, declarative invariant reconciliation loops |
| **SFB comms layer (P2)** | **done (0.2.3)** — crosspost hook + [agent] attribution + involuntary harness lifecycle posting — see section below |
| **Contribution pipeline** | **hardened (2026-09-08)** — `fritz_contribute` own-repo push mode, extended no-LLM fallback safety net, `gemma4` timeout root-cause fixed. Two real dogfood PRs landed. |
| **job_finder.py (new)** | **done (2026-09-08)** — `fritz_analyze_repo`, `fritz_discover_and_analyze`, `fritz_act_on_finding`. Local-LLM issue analysis, age/engagement signal, unlinted-repo scanning, friendly-tone issue filing, `analysis_log` postmortem trail |
| Coworker watches | **expanded (2026-09-08)** — added `gpu_vram_watch`, `workflow_health_watch`, `task_backlog_watch`, `disk_watch`, `contribution_dogfood` (disabled by default — 233 repos on the account, needs scoping first); removed `activity_pulse` (unused vanity ping) |

## SFB Comms Layer (P2) — surveillable agent comms on Discord

One event, three surfaces: hub board (source of truth) + Discord (sanitized human-readable mirror) + vla diary (trace ids). Implemented in `coworker/crosspost.py`; agents post via the `sfb_post` MCP tool; the workflow harness posts lifecycle events involuntarily.

**Channels** (guild Sandra's Fleet HQ, category SFB, created 2026-08-15):

| Channel | Purpose | Budget |
|---|---|---|
| #sfb-work | task lifecycle (start/end) | 2 per task_id |
| #sfb-thoughts | agent musings | 1 per agent per hour |
| #sfb-alerts | urgent events, fleet pulse, BLOCKED workflows | 10 per agent per hour |

**Design rules:**
- Board is source of truth; the Discord leg is best effort (429/downtime never fails board+diary), so Discord alone under-reports. Reconciliation via diary `discord_error` metrics.
- Secrets stripped before Discord (`_sanitize`); raw state stays on board/diary. Known quirk: the 32-64 alnum blob rule also redacts 40-hex commit SHAs.
- **Attribution (0.2.3):** every Discord message carries an `[agent]` prefix; `sfb_post` takes an `agent` param (defaults to Fritz).
- **Involuntary posting (0.2.3):** the flowforge harness crossposts `workflow_start` and completion (with gate verdict) to #sfb-work and BLOCKED instances to #sfb-alerts via `autopost_workflow_event()`. Agents are surveillable regardless of whether they choose to report. task_id = `wf:<name>:<started_at>`, unique per instance.
- Inbound Discord is untrusted data (discord-mcp wraps all reads in UNTRUSTED banners); the SFB layer is write-mostly by design.

**Status honesty (audited 2026-08-29):** alerts leg VERIFIED in daily production use since 08-15 (fleet pulse, day prep, arxiv code-drops). work/thoughts legs were dead until 0.2.3 made lifecycle posting harness-driven; attribution VERIFIED live (msg 1543174003240337499). Blocked-hook path is test-covered but not yet driven to BLOCKED in a live workflow (HYPOTHESIS).

**Open hardening backlog:** split bot tokens or drop Manage Channels from the agent bot; surveil rules for channel-map drift and rogue webhook URLs in agent code; daily discord_error reconciliation; budget key expiry + move `sfb_budget.json` off `Path.home()` (LocalSystem trap).

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
│   ├── harness/                      # Mechanical Gate Engine (OPC-derived)
│   │   └── gate_engine.py            # synthesize(), lint_criteria(), independence check,
│   │                                   oscillation detection, tier coverage
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
│   │   ├── contribute.py             # fritz_contribute + gogetajob_* wrappers (own-repo push mode)
│   │   ├── job_finder.py             # fritz_analyze_repo, fritz_discover_and_analyze, fritz_act_on_finding — local-LLM issue analysis (2026-09-08)
│   │   ├── coworker.py               # 11 tools: scheduled office + fleet flows
│   │   ├── intel_hub.py              # 3 tools: publish, list, aiwatcher_push_event
│   │   ├── voice.py                  # 1 tool: route_voice_command
│   │   └── evolution_log.py          # 3 tools: record, list, stats
│   │
│   ├── intel_hub/                    # Shared HTML reports (:11027)
│   ├── coworker/                     # Coworker flow runners + recurrence
│   │   ├── fleet_pulse.py            # Morning fleet health report
│   │   ├── devices_watch.py          # devices-mcp priority poll (5m)
│   │   ├── aiwatcher_ingest.py       # Fritz → AIWatcher fleet events
│   │   ├── urgent_notify.py          # Email + cursor inbox on thresholds
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

## MCP Tools (103 as of 2026-09-08, fully re-audited — see `/api/health` `tool_count` for current live number, and repo `SPEC.md` §5 for the complete per-module breakdown)

### Coworker — Scheduled flows (16 flows as of 2026-09-08)

| Tool | Default schedule (Europe/Vienna) |
|------|----------------------------------|
| `coworker_fleet_pulse` | Daily `07:00` |
| `coworker_inbox_briefing` | Weekdays `wd:08:00` |
| `coworker_day_prep` | Weekdays `wd:08:30` |
| `coworker_devices_watch` | Every `5m` — kitchen temp, CO, Ring |
| `coworker_cursor_spend_watch` | Every `2h` |
| `coworker_docs_drift` | Sunday `sun:10:00` |
| `coworker_weekly_report_pdf` | Friday `fri:17:00` |
| `coworker_board_pack` | Monthly `d1:09:00` |
| `coworker_artifact_pack` | Sunday `sun:18:00` |
| `coworker_scribe_watch` | Every `2h` — session-scribe capture freshness |
| `coworker_surveillance_watch` | Every `15m` — NSSM service health |
| `coworker_check_email` | Every `15m` — security scan |
| `coworker_gpu_vram_watch` | Every `15m` — nvidia-smi + ollama ps, added 2026-09-08 |
| `coworker_workflow_health_watch` | Every `30m` — early warning before the stall reaper fires, added 2026-09-08 |
| `coworker_task_backlog_watch` | Every `6h` — oldest pending task age, added 2026-09-08 |
| `coworker_disk_watch` | Every `6h` — free space C:\ / D:\, added 2026-09-08 |
| `coworker_contribution_dogfood` | Weekly `sun:20:00`, **disabled by default** — added 2026-09-08, needs a repo allowlist before enabling (233 repos on the account) |
| `coworker_list_flows` | — |
| `coworker_bootstrap` | Seeds pulse tasks on boot |

`activity_pulse` (self-status ping) was removed 2026-09-08 — vanity metric, nothing consumed it.

### Harness — Mechanical Gate Engine (standalone library)

| Export | Purpose | OPC origin |
|--------|---------|------------|
| `synthesize(evals, tier)` | Deterministic verdict: 🔴→FAIL, 🟡→ITERATE, all clear→PASS | `opc-harness synthesize` |
| `lint_criteria(text)` | Mechanical acceptance criteria lint before pipeline starts | `opc-harness criteria-lint` |
| `check_independence(evals)` | Require ≥2 independent evals, reject identical content | Review independence guard |
| `detect_oscillation(current, previous)` | A→B→A feedback loop detection | Oscillation detection |
| `check_tier_coverage(artifacts, tier)` | Polished demands screenshots; delightful demands tests | Quality tier checks |

Zero LLM dependency — all verdicts computed by code. Import pattern:
```python
from fleet_agent.harness import synthesize, lint_criteria
verdict = synthesize(evals)
if verdict.verdict == "FAIL":
    ...
```

### Intel Hub (3 tools)

| Tool | Purpose |
|------|---------|
| `intel_reports_publish` | HTML report → hub :11027 |
| `intel_reports_list` | Catalog |
| `aiwatcher_push_event` | Fleet Events feed |

See [fritz-coworker](./fritz-coworker/README.md), [intel-reports-hub](../patterns/intel-reports-hub.md), [libreoffice-mcp](./libreoffice-mcp/README.md).

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

### Codegen (3) · GitHub (9) · Contribute · Job Finder (new 2026-09-08)
- Autonomous PR pipeline: `fritz_contribute` (own-repo push mode, no fork needed for repos we own) + `gogetajob_scan/feed/start/submit/stats/sync` wrappers (real npm package `@kagura-agent/gogetajob`, now logs to `contribution_log` so gogetajob-driven work shows on the webapp too) + full GitHub tool surface.
- **Job Finder** (`job_finder.py`, new): `fritz_analyze_repo` (read-only analysis — local-LLM issue tractability/age/engagement signal, unlinted-repo scan), `fritz_discover_and_analyze` (gh-search-based crawler, gogetajob-shaped query params), `fritz_act_on_finding` (explicit, separate acting step — issue always; PR only on own repos). Every decision logged to `analysis_log` for postmortem, not just acted-on outcomes.

## Ports

| Service | Port | Protocol |
|---|---|---|
| Backend (FastMCP HTTP) | 10996 | HTTP + MCP Streamable HTTP |
| Frontend (webapp) | 10997 | Vite + React dashboard |
| Intel Reports Hub | 11027 | HTML index + `POST /api/reports/publish` |

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

### Mechanical Gates — The Zero-Trust Axiom (OPC-derived)

> **The agent that builds never evaluates. Every critical output must have an independent verification path. Verdicts are computed by code, not by asking an LLM whether a finding is "important enough."**

The gate engine (`src/fleet_agent/harness/gate_engine.py`) replaces LLM-as-judge with deterministic rules:

| Layer | What it does | LLM-free? |
|-------|-------------|-----------|
| **L0 — Zero Trust** | Decision axiom: every critical output needs independent verification | Never needs LLM |
| **L1 — Shape Agent** | Persona setting, anti-pattern tables, mandatory output structure in agent prompts | Guides LLM |
| **L2 — Agent Flow** | Separation of concerns, context isolation (fresh agents, no session reuse) | Coordinates LLMs |
| **L3 — Deterministic Enforcement** | Severity counting, verdict rules, oscillation diff, file-finding evidence checks | **Pure code** |

**Verdict rules (from OPC):**
- Any 🔴 (critical) → **FAIL** — pipeline blocks, changes required
- Any 🟡 (warning) → **ITERATE** — address before proceeding
- All 🔵/LGTM → **PASS** — gate opens
- Any ⛔ → **BLOCKED** — hard stop, cannot proceed

No LLM gets to decide whether a finding "matters." The code does.

## Comparison with OPC (One Person Company)

[OPC](https://github.com/iamtouchskyer/opc) (173★, MIT) is a Claude Code skill with 16 specialist agents and a digraph-based pipeline with code-enforced quality gates. We adopted its mechanical gate concepts rather than the full stack.

| Concept | OPC (Claude Code) | Fritz (fleet-agent-mcp) |
|---------|-------------------|------------------------|
| Runtime | Claude Code skill (shell/JS, slash commands) | FastMCP 3.2 (Python, MCP protocol) |
| Pipeline | `opc-harness` digraph with file-based state | FlowForge state machine (YAML + SQLite) |
| **Mechanical gates** | `opc-harness synthesize` — emoji severity → verdict | **`harness/gate_engine.py`** — `synthesize()`, deterministic, zero LLM |
| **Criteria lint** | `opc-harness criteria-lint` — pre-init mechanical DoD check | **`lint_criteria()`** — portable Python, usable anywhere |
| **Review independence** | ≥2 eval files, identical content rejected | **`check_independence()`** — same logic, MCP-aware |
| **Oscillation detection** | A↔B pattern over 4-6 ticks | **`detect_oscillation()`** — same pattern |
| Flow templates | JSON with `contextSchema`, `softEvidence`, `unitHandlers` | YAML (v0.2.x); **planned**: JSON + schema validation in v0.2.2 |
| Cross-server coordination | None (single-process skill) | Fleet bridge to 27 MCP servers |
| Scheduled execution | `opc-harness` cron (survives restart) | Heartbeat cron (60s) + coworker (9 scheduled flows) |
| State persistence | File-based `.harness/` directory | SQLite (10 tables, WAL mode) |
| Distribution | `npm install -g @touchskyer/opc` | `uv sync` + NSIS installer (Tauri 2.0) |

**What OPC does better:** Mechanical gate enforcement is more deeply integrated into its pipeline. Every node type has distinct gate rules. Brief → Build → Review → Test-Design → Test-Execute → Gate is a well-tested flow template with 100+ test files.

**What we do better:** Cross-server orchestration (27 fleet servers), scheduled coworker flows, SQLite persistence, identity system with SOUL.md + evolution log, Tauri native desktop wrapper, dual transport (stdio + HTTP).

## Comparison with kagura-agent

| Component | Kagura | Fritz (fleet-agent) |
|---|---|---|
| Runtime | OpenClaw (TS/Node, 373k stars) | FastMCP 3.2 (Python) |
| State machine | flowforge (npm, 124 commits) | built-in (YAML + SQLite, ~300 lines) |
| Task mgmt | pulse-todo (OpenClaw Skill) | pulse tools (SQLite) |
| Knowledge | wiki (270+ cards, 1290 commits) | memory (cards + projects + evolution) |
| Teleport | openclaw-teleport (v0.5.0) | teleport tools (.soul tar.gz) |
| Cron | OpenClaw built-in | External → heartbeat_wake() |
| Core language | TypeScript | Python |

## Roadmap

### v0.2.1-pre (current)
- [x] **Harness — Mechanical Gate Engine** — `harness/gate_engine.py` (OPC-derived)
- [x] **Intel Reports Hub** — :11027, Fritz + AIWatcher publish, iPad/Tailscale
- [x] **Fritz → AIWatcher ingest** + urgent email + cursor inbox
- [x] **devices_watch** — polls devices-mcp `/api/fleet/priority`
- [x] Coworker expanded — 11 tools, 9 scheduled flows
- [x] Fleet bridge — 20 servers (incl. devices)

### v0.2.2 (upcoming — Harness integration)
- [ ] **Gate-aware `workflow_next()`** — review nodes call `synthesize()` before advancing
- [ ] **`gate_evaluate` MCP tool** — expose `synthesize()` as a tool for external callers
- [ ] **`criteria_lint` MCP tool** — expose `lint_criteria()` as pre-flight gate
- [ ] **Criteria lint in `workflow_start()`** — block start if acceptance criteria fail lint
- [ ] **Review independence enforcement** — `workflow_next()` checks ≥2 evals before advancing
- [ ] **Oscillation detection** — detect A→B→A loops in consecutive gate rounds, surface warning
- [ ] **Tier coverage enforcement** — execute nodes in polished/delightful flows require screenshots
- [ ] **JSON flow templates** — extend `workflow_loader.py` beyond YAML to support OPC-style validated JSON flow schemas

### v0.2.0-pre
- [x] **Coworker pilot** — libreoffice-mcp PDF/ODT deliverables
- [x] Webapp dashboard (10997)

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
- [x] Open source contribution pipeline (gogetajob equivalent) — done 2026-09-08, see job_finder.py above

### Aspirational contribution targets (named 2026-09-08, deliberately not attempted yet)
- [ ] **Calibre** (`kovidgoyal/calibre`) — land one good, real PR that Kovid Goyal merges. The clean "prove the pipeline works" case.
- [ ] **Mixxx** (`mixxxdj/mixxx`) — video support. Sandra already has substantial fork infrastructure (`D:\Dev\repos\mixxxxx` — FFmpeg video decode, VideoMixer, NDI output, Rekordbox export; `D:\Dev\repos\mixx-dj-mcp` — 80+ op AI control layer). NOT a clean case like Calibre: upstream has refused hundreds of video-support requests historically. Needs research into *why* before any attempt — likely reputation-building via small unrelated fixes first, not leading with the contentious ask.

Both deferred per explicit instruction: test the pipeline on the fleet more first, to avoid overconfidence/cheekiness.

## Standards Alignment

- [FastMCP 3.2 Tool Registration](file:///D:/Dev/repos/mcp-central-docs/standards/rules/mcp_registration.md)
- [Docstring SOTA](file:///D:/Dev/repos/mcp-central-docs/standards/rules/docstrings_sota.md)
- [Webapp Ports](file:///D:/Dev/repos/mcp-central-docs/operations/WEBAPP_PORTS.md)
- [PowerShell Guardrails](file:///D:/Dev/repos/mcp-central-docs/standards/rules/powershell-script-standards.md)

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
