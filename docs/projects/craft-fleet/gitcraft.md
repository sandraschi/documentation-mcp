# GitCraft — Assessment

**Repo:** `D:\Dev\repos\gitcraft` · **Date:** 2026-11-05 · **Grade: C**

## What it is

Git + GitHub fleet repository craft workstation. Rebuild-PLAN Wave-1 #6
(from `git-github-mcp` `gitops_*`: `git_core`, `git_branch`, `git_admin`,
`github_ops`, `fleet_*`).

## Model / verbs

- **Model:** repo + PR (+ fleet dirt-map).
- **Verbs (README):** `status log diff pr-list pr-view fleet-dirty` family.
- **Surface:** `cli.py` + `mcp_server.py`, `justfile`, `AGENTS.md`. 2 test files.

## Architecture

Python FastMCP, `.venv`, `pyproject`. Scaffold committed 2026-11-04.

## Strengths

- Read-only-recipe discipline is specified in PLAN (never mutate in bench:
  no commit/push, no `reset --hard`, no force-push) — the right default for git tooling.
- Fleet-dirty across `D:\Dev\repos` is a genuine fleet superpower if kept honest.

## Gaps / risks

- Mutation surface is the danger: a craft that *can* commit/push fleet-wide needs
  confirm-gates and dry-run-first, evidenced in tests — not yet shown.
- `gh auth` absence must degrade to local-only with receipts, not red CI.
- Overlap with `gitops` MCP (the incumbent) needs a shim-or-replace note.

## Next 3 steps

1. Confirm-gate + dry-run proof for every mutating verb (tests assert the gate).
2. 3 read-only recipes: `git/status-clean-check`, `git/log-recent`, `git/pr-list-fleet`.
3. Write the gitops relationship note (shim, replace, or coexist).

## Verdict

Grade C: correct scope, correct read-only default. Trust comes from the
confirm-gate tests — land those before any fleet-wide mutation verb ships.
