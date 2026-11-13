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

## Next 3 steps

1. Add comments thread to the issue inspector drawer.
2. Integrate with `devcraft.safe_commit_and_snapshot` to auto-link commits upon snapshot.
3. democraft recipes (`task/blocker-gate`, `task/git-close`).

## Verdict

Grade A-: complete sovereign issue tracker workstation. The store enforces hard workflow invariants, the MCP server provides complete agentic access, and the native egui desktop app offers a fluid, interactive experience replacing Linear/Jira for small sovereign teams.
