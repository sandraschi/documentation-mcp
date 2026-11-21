---
title: "Craft Fleet Rules"
category: standard
status: active
audience: all agents (Claude Code, opencode, agy, Cursor)
last_updated: 2026-11-19
---
# Craft Fleet Rules

Applies to every `*craft*` repo (pure-Rust ArtCraft apps: L1 core, L2 CLI + MCP, L3 egui).
Companion to [RUST_ARTCRAFT_STANDARD.md](./RUST_ARTCRAFT_STANDARD.md). Active plan:
[CRAFT_CONSOLIDATION_PLAN_2026-11.md](../projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md).

These rules are repeated verbatim in `C:\Users\<user>\.claude\CLAUDE.md` (Claude Code and
opencode), `C:\Users\<user>\.gemini\antigravity\gemini.md` (agy) and
`.cursor/rules/craft-fleet.mdc` (Cursor). Change them here first, then sync the copies.

## 1. Freeze and scope

- No new `*craft*` repo until the consolidation plan's Phase 4 exits. After that, only via
  the admission gate (plan section 7).
- No feature work in a craft during the consolidation unless Sandra asked for it in the
  current session. Consolidation, tests, stub removal, honesty and hygiene only.

## 2. Coordination

- Claim before touching: `devcraft_claim`, or a claim file
  `operations/session-log/craft-claim-<agent>-<date>.md` if DevCraft is down. One agent per
  repo at a time. Release the claim when done.
- Before starting, read the session log entries of the last 3 days for the repos you will
  touch. Another agent may have changed them.
- Never verify your own work. Phase exits are ticked by a different agent.

## 3. Git

- Single trunk: work on `main` (or the repo's existing default). A short-lived branch is
  allowed only if merged and deleted in the same session. Never leave agent branches.
- LF only. Every repo has `.gitattributes` with `* text=auto eol=lf`.
- Checkpoint commit and push before any multi-file change. Max 10 files per commit.
- Never commit build output. `.gitignore` must cover `target/`, `dist/`, `*.exe`, `*.zip`,
  `*.mcpb`, `*.pdb`, `*.bak`, `*.bak.*`, `.env`. This also applies to WIP snapshot refs
  (`refs/wip/*`): the 2026-11 shopcraft bloat (72 MB on GitHub) came from `dist/` binaries
  inside pushed WIP refs, not from `main`.
- Destructive actions need Sandra's explicit go recorded in the session log: force-push,
  history rewrite, deleting branches, tags, refs, releases or repos. Archiving per the
  plan's decision table is allowed.

## 4. Releases

- Assets are plain executables. No zip-only releases. craft-launcher may add a
  `-portable.zip` beside the exes, never instead of them.
- Release gate: T1 craft >= 20 tests, T2 craft >= 50 tests, CI green, no `todo!()` or
  `unimplemented!()` reachable from CLI, MCP or egui entry points, README feature matrix
  present. Otherwise the release is marked pre-release.
- Versions stay below 1.0 until T2 and a week of real use by Sandra.

## 5. Honesty

- Every README has a feature matrix: `Implemented`, `Partial` or `Planned`. Nothing implied.
- An unbuilt code path returns an explicit `not_implemented` error, never fake success.
- Report test counts as measured (`cargo test --workspace` output), not estimated.

## 6. egui

- High contrast in both themes. Never light grey text on white in light mode.
- Ctrl + mouse wheel zoom works in every window.

## 7. Paperwork

- Every work block ends with a session-log entry (repo, what changed, test count before and
  after, what is left) and a tick in the plan, both committed in mcp-central-docs.
- No em dash character anywhere: code, docs, commit messages, chat.
