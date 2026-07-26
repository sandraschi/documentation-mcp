# Fritz Coworker — Poor Man's Viktor

> **Status: PILOT (v0.2.1-pre)** — 9 scheduled flows + 11 MCP tools; Intel Hub + home-safety watch shipped 2026-06-07.

**Canonical agent:** [fleet-agent-mcp](../../fleet-agent-mcp.md) (**Fritz**, port **10996**)
**Source repo:** `D:\Dev\repos\fleet-agent-mcp`
**Inspiration:** [Viktor](https://viktor.com) (AlphaSignal Deep Dive 2026) — Slack-native AI coworker with cloud compute and 3,000+ SaaS integrations
**Decision:** Viktor's ideas are strong; **$50/mo entry is misleading** for recurring automation (~$200–750/mo realistic). Replicate the execution model on the existing MCP fleet instead of renting it.

---

## What Viktor Does (that we want)

| Viktor capability | Our equivalent (existing or planned) |
|---|---|
| One message → many tools | `fleet_bridge` → chain MCP calls across fleet |
| Ships artifacts (PDF, dashboard, PR) | `codegen` + `github_*` + `web-development-mcp` |
| Persistent team memory ("skills") | `memory_card_*` + `advanced-memory-mcp` · [Hermes borrowings map](https://github.com/sandraschi/fleet-agent-mcp/blob/main/docs/hermes-borrowings.md) (run FTS, curator, anti-spin) |
| Scheduled / proactive work | `notify` scheduler + `pulse` recurrence + `heartbeat_wake` |
| Slack / Teams interface | `discord-mcp` today; Slack optional later |
| Confirmation before high-stakes actions | Workflow branches + SOUL policy (new) |
| Cloud computer for code | Local: Fritz codegen + Docker via `fileops` / `docker-mcp` |

**What we skip:** Viktor's 3,000 generic OAuth integrations, shared-workspace privacy model, credit-metered SaaS billing.

---

## Architecture (preliminary)

```
┌─────────────────────────────────────────────────────────────┐
│  Surface: Discord (#fritz) · Cursor · Fritz webapp (10997)  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  Fritz (fleet-agent-mcp :10996)                             │
│  heartbeat_wake → workflow "coworker" | "daily" | "pulse"   │
│  flowforge YAML enforces steps (Viktor free-roams; we don't)│
└───────────────────────────┬─────────────────────────────────┘
                            │ fleet_bridge
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   git-github          discord/emailops      docs/arxiv
   plex/calibre        robofang              meta-mcp (health)
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
              Deliverable: markdown report · email · Discord · PR · Intel Hub HTML (:11027)
```

**Cost model:** API tokens (Ollama local where possible) + electricity. No per-task credit markup.

---

## Pilot workflows (Phase 1)

Build these before anything else. Each maps to a Viktor marketing example but uses fleet-native data.

### 1. Morning Fleet Pulse

**Trigger:** `pulse` recurrence `0 7 * * *` or `notify` schedule `07:00`

**Steps:**
1. `meta_mcp` / robofang — MCP server health, stale repos
2. `git-github` — open PRs, failing CI on watched repos
3. `docs` — any TODO spikes in mcp-central-docs
4. Synthesize → `memory_project_note("fleet-pulse", …)`
5. Deliver → Discord `#fleet` or email via `notify_email`

**Viktor analog:** "Live business pulse" — but for **fleet ops**, not Stripe MRR.

### 2. Docs Drift Audit

**Trigger:** weekly Sunday 10:00

**Steps:**
1. `fleet_inspect_repo` on 5–10 priority repos (README, CHANGELOG, ports)
2. Compare against `WEBAPP_PORTS.md` / `fleet-registry.json`
3. Output markdown checklist; optional `github_create_issue` for gaps

**Viktor analog:** stakeholder PDF report — we ship markdown + optional issue tickets.

### 3. Contribution Ship (already partially built)

**Trigger:** manual or `pulse_add` from heartbeat

**Steps:** `workflows/contribution.yaml` — study → implement → test → submit → verify

**Test repos:**
| Repo | Role |
|------|------|
| `fritz-test` | Bug target for autonomous fix |
| `fritz-test-work` | Working clone during contribute flow |
| `fritz-pipeline-test` | End-to-end driver (`scripts/fritz_pipeline_test.py`) |

**Viktor analog:** "Opens PR with full context" — **this is our strongest parity path**.

---

## Phase 2 (partial — office deliverables shipped)

| Feature | Status |
|---|---|
| **Weekly PDF report** | Done — `coworker_weekly_report_pdf` + [libreoffice-mcp](./libreoffice-mcp/README.md) |
| **Monthly board pack** | Done — `coworker_board_pack`, recurrence `d1:09:00` |
| **Artifact pack** | Done — `coworker_artifact_pack`, `batch_pack`, `sun:18:00` |
| **Skills** (Viktor learned context) | Planned — `memory_card_create(type=skill)` + tags |
| **Proactive offers** | Planned — repeated manual ask → `pulse_add` |
| **Slack surface** | Planned — Slack Events → Fritz `/mcp` |
| **RBAC / private mode** | Planned — per-user SQLite namespace |

### Scheduled flows (Europe/Vienna defaults)

| Flow | Recurrence | MCP tool |
|------|------------|----------|
| Morning Fleet Pulse | `07:00` | `coworker_fleet_pulse` |
| Inbox Briefing | `wd:08:00` | `coworker_inbox_briefing` |
| Office Day Prep | `wd:08:30` | `coworker_day_prep` |
| Docs Drift Audit | `sun:10:00` | `coworker_docs_drift` |
| Weekly Report PDF | `fri:17:00` | `coworker_weekly_report_pdf` |
| Monthly Board Pack | `d1:09:00` | `coworker_board_pack` |
| Artifact Pack | `sun:18:00` | `coworker_artifact_pack` |
| Cursor Spend Watch | `2h` | `coworker_cursor_spend_watch` |

Recurrence also supports cron monthly (`0 9 1 * *`). Seed with `coworker_bootstrap()`.

**Cursor Spend Watch** calls [cursor-mcp](../cursor-mcp/README.md) `cursor_usage(alert_check)` — emails only on warn/critical (runaway cloud agents, hourly spend spike).

---

## Gaps vs Viktor (honest)

| Gap | Mitigation |
|---|---|
| No 3,000 SaaS connectors | Fleet covers Sandra's stack; add OAuth wrappers only on demand |
| No managed cloud sandbox | Local + Docker; acceptable for single-operator fleet |
| No polished "hire" UX | Fritz webapp + Discord; good enough for technical operator |
| Heartbeat doesn't auto-start workflows yet | Wire `heartbeat_wake` → `workflow_start('coworker')` in scheduler config |

---

## Success criteria (preliminary)

- [x] `coworker_fleet_pulse` tool + scheduler wiring (v0.1)
- [x] Morning Fleet Pulse task seeded on boot (`coworker-fleet-pulse`, `07:00` Vienna)
- [x] Office flows: inbox briefing, day prep, docs drift + `coworker_*` MCP tools
- [x] Fleet bridge aliases: `email`, `libreoffice`, `libreoffice-ext`, `notion`, `onenote`
- [x] Weekly Report PDF flow (`coworker_weekly_report_pdf`, libreoffice-mcp)
- [x] Board Pack flow (`coworker_board_pack`, scheduled `d1:09:00` monthly)
- [x] Artifact Pack flow (`coworker_artifact_pack`, scheduled `sun:18:00`)
- [x] Devices Watch (`coworker_devices_watch`, 5m poll of devices-mcp `/api/fleet/priority`)
- [x] Cursor Spend Watch (`coworker_cursor_spend_watch`, 2h)
- [x] Intel Reports Hub (:11027) + Fritz → AIWatcher ingest + urgent notifications
- [ ] Morning Fleet Pulse runs 7 days without manual intervention
- [ ] Deliverable lands in Discord or inbox by 07:15 Vienna time
- [ ] `fritz_pipeline_test.py` green end-to-end on `fritz-pipeline-test`
- [ ] Monthly API cost **< $20** (local LLM default) or documented if cloud
- [ ] Zero shared OAuth tokens across unrelated integrations

---

## Related docs

| Location | Content |
|---|---|
| [fleet-agent-mcp.md](../fleet-agent-mcp.md) | Fritz agent hub (v0.2.1-pre) |
| [intel-reports-hub](../patterns/intel-reports-hub.md) | Shared HTML reports pattern |
| [devices-mcp](./devices-mcp/README.md) | Fritz priority API producer |
| [aiwatcher-mcp](./aiwatcher-mcp/README.md) | Fleet ingest + digest hub consumer |
| [CHANGELOG](./CHANGELOG.md) | Pilot changelog |
| `fleet-agent-mcp/docs/coworker-plan.md` | Implementation detail + tool call recipes |
| [libreoffice-mcp](./libreoffice-mcp/README.md) | FOSS office layer — PDF/ODT for coworker deliverables |
| `fleet-agent-mcp/workflows/coworker.yaml` | YAML workflow (preliminary) |
| `fleet-agent-mcp/scripts/fritz_pipeline_test.py` | E2E contribution test driver |

---

## Ideas stolen from Viktor (keep regardless of build)

1. **Proactive cron suggestions** — agent notices repeat work and offers to schedule it
2. **Skills as first-class memory** — not just chat history
3. **Single-thread multi-tool execution** — one ask, many APIs, one deliverable
4. **Confirmation gates** — send email / merge PR / deploy requires explicit branch in workflow
5. **Usage transparency** — log token/time per task in Fritz logger (not opaque credits)

---

*Tags: #fritz #fleet-agent #viktor #coworker #orchestration #pilot*
