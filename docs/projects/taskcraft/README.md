# TaskCraft

**Version**: v0.1.3 - Local-First Issue Tracker & Kanban Sprint Board with Git Commit Linking.
**Repository**: [`d:\Dev\repos\taskcraft`](file:///d:/Dev/repos/taskcraft) | [GitHub: sandraschi/taskcraft](https://github.com/sandraschi/taskcraft)
**Parent Suite**: Sovereign Back-Office Suite

---

## What This Replaces

TaskCraft is a local-first replacement for cloud issue trackers and project management SaaS tools for sovereign 1-10 person engineering teams:

- **Directly Replaces**:
  - **Linear / Jira / Asana**: Cloud task trackers with vendor lock-in, seat fees, and latency.
  - **Trello / ClickUp**: Kanban boards without deep git commit linkage or cycle-checked blocker DAGs.
  - **GitHub Projects**: Hosted board tools that require online connectivity, webhook setups, and external API tokens.

- **Why It Replaces Them**:
  - **Local-First & Offline**: A single SQLite WAL file (`taskcraft.db`), instant load times, zero monthly SaaS bills, and fully operational without internet.
  - **Zero-Friction Git Sync**: Subprocess git log scanner (`git -C <repo> log`) automatically and idempotently detects issue mentions and closes issues on explicit closing keywords (`closes KEY-12`, `fixes KEY-12`).
  - **Hard Dependency Invariants**: The `blocks` relation forms a cycle-checked DAG. Starting or finishing a blocked task is refused at the database level unless explicitly forced and audited.
  - **Unified Triple-Surface Architecture**: Native desktop GUI, FastMCP stdio server for AI agents, and a command-line interface all sharing the exact same command dispatch bus.

---

## Ports & Surfaces

- **Desktop Workstation (L3)**: Native egui 0.37 desktop workstation (`taskcraft-app`) with Kanban board, issues table, interactive inspector drawer, relations DAG management, milestone burn-up, git commit sync, Ctrl+K command palette, and cross-app bus signals.
- **MCP Stdio Server (L2)**: FastMCP stdio server (`taskcraft mcp`) exposing 17 tools to AI agents with full audit trail logging under actor `agent`.
- **CLI Interface (L2)**: Terminal client (`taskcraft <command>`) with human-readable and `--json` machine output.
- **Embedded Store (L1)**: SQLite WAL database with gapless per-project issue numbering (`KEY-n`).

---

## Architecture

```
taskcraft-store (SQLite WAL) <── taskcraft-core (Issue state machine & Git linker)
                                      ^
                ┌─────────────────────┴─────────────────────┐
                │                                           │
       taskcraft-mcp (L1/L2)                       taskcraft-app (L3 GUI)
    (FastMCP Stdio Server & CLI)                  (egui 0.37 Native Workstation)
```

- Replaces Linear, Jira, and Asana for 1-10 person sovereign engineering teams.
- Atomic commit hooks link commit messages (`closes TC-12: ...`) directly into local issue histories.
