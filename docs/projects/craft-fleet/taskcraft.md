# TaskCraft - Assessment

**Repo:** `D:\Dev\repos\taskcraft` (local, not pushed) - **Date:** 2026-11-10 - **Grade: A-** (Tier 1 Store/Core/MCP + L3 egui Workstation; tested) - **Origin:** fleet-owned

## What it is

Local-first issue tracker for a 1-10 person team (Linear/Jira/Asana replacement), with git commit linking.
Second app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.2).
Shared kernel: `craft-biz` (bus, MCP loop, confinement).

## What it replaces

- **Linear, Jira, Asana, ClickUp**: Replaces multi-tenant cloud SaaS trackers with a sovereign, local-first single-file SQLite WAL tracker.
- **Trello, GitHub Projects**: Replaces cloud Kanban boards with an instant 60fps native egui desktop app featuring cycle-checked dependency DAGs, automatic git log commit linking, and AI agent integration over FastMCP.

## Model / verbs

- **Crates:** `taskcraft-store` (SQLite WAL: projects, KEY-n issues, milestones, relations, commit links, event history), `taskcraft-core` (command bus, `gitsync.rs`, bus inbox, demo), `taskcraft-mcp` (`taskcraft` binary: CLI + FastMCP), `taskcraft-app` (native egui desktop workstation).
- **17 MCP tools / CLI verbs:** status, project create/list, issue create/list/show/update/move, relation add/remove, milestone create/list/close, board, git_sync, inbox_drain, demo_seed.
- **Desktop Workstation (taskcraft-app):**
  - **Kanban Board**: Drag-and-drop cards, live blocker rules, column `+` creation, priority/assignee swimlanes, and live filter toolbar.
  - **Interactive Inspector**: In-place title/description editing, status changer, priority/assignee pills, due date helpers, milestone selector, interactive label chips with instant removal/addition.
  - **Relations & Blockers**: DAG visualization with clickable issue links, instant relation unlinking, and add-relation form with cycle detection.
  - **Multiple Views**: Kanban Board, sortable Issues Table with CSV export, Milestone burn-up with progress bars, Git commit history with clickable issue references, and Project Audit Log event stream.
  - **Global Shell**: Ctrl+K Command Palette, cross-app Signals Dock, project switcher, New Project and New Milestone modals, and dark/light theme toggle.

## Strengths

- Blocker gate: start/finish of a blocked issue is refused unless `force`; `blocks` edges are cycle-checked (BFS) at insert.
- Full history per issue with actor (`agent`, OS user, `git:<author>`, `bus:<app>`), so agent edits are auditable.
- Git sync tested end to end against a real temporary repo: links mentions, closes only on closes/fixes/resolves, respects blockers, idempotent on re-sync, refuses repos outside `--allow-path`. Smoke-run against the real buchcraft repo.
- Bus inbox handles `ticket.escalated` and `contract.deadline`; unknown kinds are rejected to `failed/`, not dropped.
- Complete L3 native egui desktop workstation with rich interactive controls, zero panics, high-contrast dark/light theme tokens, and zoom controls.
- 20 automated tests passing across the workspace; clean clippy and fmt checks.

## Gaps / risks

- No comments or file attachments on issues yet (description and audit history only).
- No sprints / cycles; capacity is shown from teamcraft, not planned against.
- Git sync is on demand only (no hook/watcher); no GitHub/GitLab cloud import.

## Planned improvements (scope extension 2026-11-14)

Sandra asked for a real SaaS replacement for a startup or small company. taskcraft grows from issue tracker into project management. All of it is planned, none of it built. Specs in the repo: `docs/TIERED_PLAN.md` (Tiers 5-10), `docs/PM_SPEC.md` (schema v2-v7, test criteria, hand-computed CPM fixtures), `HANDOVER.md`.

| Tier | What | Days |
|---|---|---|
| 4b | Skills + in-app chat, fleet pilot of `standards/rust-artcraft/CRAFT_SKILLS_AND_CHAT_STANDARD.md` | 0.25 here, after 2-2.5 shared |
| 5 | Migration runner (v1 store refuses other versions), people table, comments, attachments, epics/subtasks, templates, custom fields, saved views | 1-1.5 |
| 6 | Sprints planned against teamcraft capacity, burndown, velocity | 1-1.5 |
| 7 | Own CPM scheduler (FS/SS/FF + lag, AT calendar), Gantt widget, baselines, forecast | 2-3 |
| 8 | Portfolio, programs, workload heatmap, actual hours, health, `timesheet.approved` to billcraft | 1.5-2 |
| 9 | Importers (Jira, Linear, Asana, Trello, ClickUp, GitHub), MS Project XML, .ics, PDF reports | 1.5-2 |
| 10 | Team sharing, option A (decided): `taskcraft serve` single-writer host + egui clients | 2-3 |

Bus corrections from reading the code: no `leave.approved` (teamcraft capacity already subtracts leave; teamcraft re-emits `capacity.changed` instead), no `time.billable` (billcraft already consumes `timesheet.approved`).

Gantt: no usable egui Gantt or CPM crate exists (checked 2026-11-14). Plan: a standalone `egui_gantt` crate (egui only, publishable to crates.io) wrapped by `craft-biz-ui::gantt`, reusable by contractcraft, hirecraft, teamcraft.

## Next steps

1. Close Tier 4 (Insert/Modify/Commands menus, File items, exe release assets).
2. Tier 5 starts with the migration runner and a committed v1 fixture DB.
3. Carried over: democraft recipes (`task/blocker-gate`, `task/git-close`); devcraft snapshot commit linking.

## Verdict

Grade A-: complete sovereign issue tracker workstation. The store enforces hard workflow invariants, the MCP server provides complete agentic access, and the native egui desktop app offers a fluid, interactive experience replacing Linear/Jira for small sovereign teams.
