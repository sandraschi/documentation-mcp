# TaskCraft - Assessment

**Repo:** `D:\Dev\repos\taskcraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic data only) - **Origin:** fleet-owned

## What it is

Local-first issue tracker for a 1-10 person team (Linear/Jira/Asana replacement), with git commit linking.
Second app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.2).
Shared kernel: `craft-biz` (bus, MCP loop, confinement).

## Model / verbs

- **Crates:** `taskcraft-store` (SQLite WAL: projects, KEY-n issues, milestones, relations, commit links, event history), `taskcraft-core` (command bus, `gitsync.rs`, bus inbox, demo), `taskcraft-mcp` (`taskcraft` binary).
- **17 MCP tools / CLI verbs:** status, project create/list, issue create/list/show/update/move, relation add/remove, milestone create/list/close, board, git_sync, inbox_drain, demo_seed.

## Strengths

- Blocker gate: start/finish of a blocked issue is refused unless `force`; `blocks` edges are cycle-checked (BFS) at insert.
- Full history per issue with actor (`agent`, OS user, `git:<author>`, `bus:<app>`), so agent edits are auditable.
- Git sync tested end to end against a real temporary repo: links mentions, closes only on closes/fixes/resolves, respects blockers, idempotent on re-sync, refuses repos outside `--allow-path`. Smoke-run against the real buchcraft repo.
- Bus inbox handles `ticket.escalated` and `contract.deadline`; unknown kinds are rejected to `failed/`, not dropped.
- Live stdio probe of the release binary: pure JSON-RPC on stdout. Found and fixed a fleet-wide issue on the way: PowerShell pipes a UTF-8 BOM, which the shared MCP loop now strips.

## Gaps / risks

- No egui window: the board exists only as CLI text and JSON.
- No comments, attachments, sprints or time tracking.
- Git sync is on demand only (no hook/watcher); no GitHub/GitLab import.
- Event producers deskcraft and contractcraft do not exist yet (synthetic events in tests). teamcraft `capacity.changed` works end to end since v0.1.1 and shows in `status`.

## Next 3 steps

1. egui app: board with lanes, issue detail with history, milestone burn-up; screenshot mode like buchcraft.
2. Comments on issues (needed before real team use).
3. democraft recipes (`task/blocker-gate`, `task/git-close`).

## Verdict

Grade C+: solid, tested Tier 1 core with the workflow invariants in the store; not usable by a non-CLI person until the GUI lands.
