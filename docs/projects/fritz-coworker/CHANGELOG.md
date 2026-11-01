# fritz-coworker — Changelog

Design + pilot implementation for Poor Man's Viktor on fleet MCP.

## 2026-08-25 — Hermes Borrowings & Anti-Spin Hardening (fleet-agent-mcp 0.2.2)

### Added
- **Flowforge Anti-Spin Failure Limit Guard** — `failure_limit: 2` (default) auto-blocks workflow instances on repeated node execution failures to prevent token spin-loops. Added `workflow_failure_record` and `workflow_unblock` FastMCP tools, `heartbeat_wake` block detection, and `speechops` TTS / urgent report alerts.
- **External `SKILL.md` Importer** — `import_external_skill` FastMCP tool parses standard YAML frontmatter (`name`, `description`, `tags`) and Markdown content from OpenClaw, Anthropic, or Hermes skill files into `card_type: skill` cards.
- **Prompt Cache Alignment** — dynamic memory cards and prior node outputs injected into turn history immediately preceding execution, preserving static system prompt KV-caching.
- **Multi-Provider Fallback Cascade Engine** — `llm_fallback_providers` configuration in `Settings`; `run_agent_step` automatically cascades from primary cloud LLM to local Ollama models (`muse-glimmer` / `llama3`) on network or API failures.

## 2026-06-07 — Intel Hub + home safety (fleet-agent-mcp 0.2.1-pre)

### Added

| Flow | Recurrence | MCP tool |
|------|------------|----------|
| Devices Watch | every 5m | `coworker_devices_watch` |
| Cursor Spend Watch | every 2h | `coworker_cursor_spend_watch` |

- **Intel Reports Hub** — port 11027; `intel_reports_publish`, `intel_reports_list`, `aiwatcher_push_event`
- **Fritz → AIWatcher ingest** — auto after Pulse / Day Prep
- **Urgent notifications** — email + cursor inbox (Pulse degradation, hot intel, devices critical, cursor spend)
- **devices-mcp** — `GET /api/fleet/priority` (kitchen temp, CO, smoke, Ring)

Docs: `fleet-agent-mcp/docs/INTEL_REPORTS_HUB.md`, `patterns/intel-reports-hub.md`, `devices-mcp/docs/FLEET_INTEGRATION.md`

## 2026-05-30 — Pilot shipped (fleet-agent-mcp 0.2.0-pre)

### Scheduled flows (Europe/Vienna defaults)

| Flow | Recurrence | MCP tool |
|------|------------|----------|
| Morning Fleet Pulse | `07:00` daily | `coworker_fleet_pulse` |
| Inbox Briefing | `wd:08:00` | `coworker_inbox_briefing` |
| Office Day Prep | `wd:08:30` | `coworker_day_prep` |
| Docs Drift Audit | `sun:10:00` | `coworker_docs_drift` |
| Weekly Report PDF | `fri:17:00` | `coworker_weekly_report_pdf` |
| Monthly Board Pack | `d1:09:00` | `coworker_board_pack` |
| Artifact Pack | `sun:18:00` | `coworker_artifact_pack` |

### Infrastructure

- Coworker scheduler wired to `notify` 60s loop + `recurrence_due` (incl. monthly `dN:HH:MM`)
- `coworker_bootstrap()` seeds pulse tasks on server boot
- Fleet bridge office aliases: email, libreoffice, libreoffice-ext, notion, onenote
- [libreoffice-mcp](../libreoffice-mcp/README.md) for styled PDF/ODT

### Still open (pilot soak)

- 7-day unattended pulse run
- `fritz_pipeline_test.py` green
- Heartbeat → `workflow_start('coworker')` auto-dispatch

## 2026-05-30 — Design (initial)

- MCD project page, Viktor ROI analysis, `workflows/coworker.yaml`, `docs/coworker-plan.md`
