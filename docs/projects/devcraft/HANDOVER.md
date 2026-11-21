---
updated: 2026-11-14T11:30:00+01:00
status: cockpit shipped, window not yet looked at by a person this session
tags: [devcraft, cockpit, egui, craft-biz-ui]
---

# Handover - DevCraft

Mirror of `D:\Dev\repos\devcraft\HANDOVER.md`. Read that file if this copy is older than a week.

## What was done

- v0.2.0 replaces the v0.1.0 multi-panel studio. The window is the craft shell: File, Edit, View, Fleet, Window, Help.
- Nine pages: Today, Board, Git, GitHub, Docker, Reports, Craft apps, Claims, Ports.
- Today, Git, and GitHub draw the morning digest (`operations/fleet-status.md`) as bar charts and tables before git finishes.
- A background thread reads sibling checkouts and fills the board. Docker is probed on its own thread. Smoke does not scan.
- Claims, pins, and 24-hour snoozes live in `{workspace}/.devcraft`. Holders are cursor, opencode, agy, and claude.
- There is no listening port. The 11258/11259 pair from v0.1.0 is not bound.
- Commits `14d3349` and `5e61dbf` on `main`. On 2026-11-14: 18 tests, clippy `-D warnings`, and `--smoke` were green.

## Next step

Open `cargo run -p devcraft-app` from `D:\Dev\repos\devcraft` and look at Today. Then Tier 3 in `docs/TIERED_PLAN.md`: holder swimlanes, a commit-age chart, and pages for the time machine, the sandbox, and service restart.

## Deliberately not done

- No 14-day flow chart, commit heatmap, swimlanes, TaskCraft keys, or worktree child cards.
- Time machine, sandbox, and service restart stay CLI and MCP tools. They have no page.
- No golden screenshots. Smoke JSON is not a look at the window.
