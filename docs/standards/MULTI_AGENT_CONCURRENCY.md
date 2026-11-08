---
title: "Multi-agent concurrent editing (conflict-avoidance standard)"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-11-02
---
# Multi-agent concurrent editing

**Status:** v1.0, adopted 2026-11-02. **Owner:** Sandra.
**Kit:** [`templates/agent_kit/`](../templates/agent_kit/) (`AGENTS.md`, `.githooks/pre-commit`). **Helpers:** `scripts/Set-LfEndings.ps1`, `scripts/Invoke-FleetWipSnapshot.ps1`.

## Why

Several agents (Claude Code, Claude Desktop, OpenCode, Cursor, Windsurf, Antigravity) edit the
same repos from different chats and IDEs, often at once, none aware of the others. Git was
designed for people who talk to each other. Agents do not, so the failure modes are mechanical
and predictable.

Incident that motivated this (gamecraft, 2026-11-02): one session ran a commit-all while another
had uncommitted `Cargo.toml` edits naming a crate that existed only on disk. The edits went into a
release commit and a pushed tag (`v0.13.0`). The pushed tree did not build from a clean clone.
Nobody did anything unreasonable by their own context; the process allowed it.

## Failure modes

| # | Mode | Example |
|---|---|---|
| F1 | Sweep: commit-all captures another agent's half-done work | `git commit -a` swept manifest edits into a release |
| F2 | Torn change: manifest committed without the files it names | member crate untracked, clean clone fails |
| F3 | Lost update: two agents edit one file, last writer wins | both rewrite `README.md` |
| F4 | Stale base: agent works on a tree another agent has since changed | rebase/merge surprises |
| F5 | Published mistake: tag or release made from a dirty or unverified tree | `v0.13.0` |
| F6 | Silent history rewrite: force-push, tag move, amend of pushed commits | repairs break other clones |
| F7 | No trail: nobody knows who did what or why | needs forensic reconstruction |
| F8 | Line-ending churn: CRLF/LF mix trips hooks (see Line endings) | repeated fix-retry loops |

## Rules

Each rule names the failure mode it prevents.

### Isolate (F1, F3, F4)

1. **One agent, one branch or worktree** for anything longer than a quick fix:
   `agent/<tool>-<topic>`; a worktree (`git worktree add ../<repo>-<topic> -b agent/<tool>-<topic>`)
   if another agent may be active in the main checkout. Merge to the default branch when the work
   is finished and verified.
2. **Look before you touch**: `git status` and `git log -5` at session start. A dirty tree you did
   not make means someone else is active. Do not clean, reset, stash or "tidy" it.
3. **Claim hot files** (README, CHANGELOG, workspace manifests, lockfiles) by noting the claim in
   the worklog, or edit them last, in a small commit, after pulling.

### Commit narrowly (F1, F2)

4. Never `git add -A`, `git add .`, `git commit -a`, `git commit -am`. Name paths:
   `git add <paths>` then `git commit -m "..." -- <paths>`.
5. Check `git diff --cached --stat` before every commit. Every file listed must be yours.
6. **Manifest and referents travel together.** A commit that adds or changes a workspace member or
   path dependency includes the referenced crate. Enforced by the pre-commit hook.
7. Do not use `--no-verify`.

### Publish carefully (F5, F6)

8. No tag or release from a dirty tree. Before tagging: `git status` clean, clean clone of the
   exact commit builds and tests pass (see RELEASE_DISCIPLINE section 3).
9. Never move, delete or re-create a published tag. Never force-push a shared branch. Fix forward
   with a new commit and a new tag; deprecate the bad one in release notes.
10. Do not push commits you did not make and did not read.

### Leave a trail (F7)

11. Commit messages: what and why. Agent commits carry the tool's trailer.
12. Non-trivial or multi-session work leaves a line in the repo's worklog (`docs/WORKLOG_*.md` or
    the plan file): who (tool/session), what, what is unfinished.
13. At session end: commit own work, push if asked or if the repo's policy says so, and say what is
    left uncommitted and whose it appears to be.

### Line endings (F8)

| # | Mode | Example |
|---|---|---|
| F8 | CRLF/LF mix trips hooks and wastes retry loops | `fileops write_file` writes CRLF, global `core.autocrlf=true`, `#!/bin/sh\r` fails, format hooks rewrite files and fail twice |

14. Repo text files are LF, UTF-8 without BOM (`.bat`/`.cmd` may be CRLF). Hooks and `#!` scripts are always LF.
15. Editing an existing file keeps its endings. Never read-all and rewrite-all with different endings.
16. After writing files with `fileops write_file`, `Set-Content`, `Out-File` or `>`, run
    `scripts/Set-LfEndings.ps1 -Path <files>` (or `-Changed`) before committing.
17. A hook that rewrites files and fails gets one `git add <own paths>` and one retry. Second failure:
    stop and report. No loops.
18. Every repo should carry `.gitattributes` with `* text=auto eol=lf` (kit installs `.githooks/* text eol=lf`
    at minimum). Renormalizing a whole repo is a deliberate single commit by the owner, never an agent side effect.
19. Machine (owner): `git config --global core.autocrlf input`, `core.safecrlf false`. Current value is `true`, which is
    why Windows tools keep producing CRLF working trees.

Known gap: the `fileops` tool itself still writes CRLF; the helper script is the workaround until it gets an
`eol` option.
## Enforcement

| Layer | Mechanism | Catches |
|---|---|---|
| Written rule | `AGENTS.md` at repo root (Claude Code, OpenCode, Cursor and Codex read it) | F1, F3, F4, F6, F7 by instruction |
| Git hook | `.githooks/pre-commit` (Cargo variant; ports for package.json / pyproject welcome) | F2 mechanically |
| Release gate | clean-clone build before tag | F5 |
| Branch protection | no force-push, no tag deletion on default branch and `v*` | F6 on the server |

Hooks live in `.githooks/` and are enabled per clone with `git config core.hooksPath .githooks`.
`core.hooksPath` is not versioned, so a fresh clone must run it once; the fleet bootstrap scripts
should do so.

Honest limits: instruction files are advisory and an agent that never read them is not bound; the
hook only catches the manifest/referent class; two agents editing the same file in one working tree
at the same time is not prevented by anything here, only avoided by rule 1.

## Reconciliation with existing standards (applied 2026-11-02, owner approved)

| Standard | Was | Now |
|---|---|---|
| GIT_REPOSITORY_SAFETY s3 and Multi-PC | agents `git add -A` for checkpoint commits | named paths; `add -A` only in a tree the agent alone owns |
| WIP_COMMIT_STANDARD | nightly sweep commits everything on the default branch, pushes, `--no-verify` fallback | retired. `Invoke-FleetWipSnapshot.ps1` stores snapshots at `refs/wip/<host>/<date>`; no branch commits, no hooks |
| RELEASE_DISCIPLINE s4 | "commit or revert" | commit your own work, never revert others'; release checklist gains a clean-clone gate |

The principle: **a backup must never be a commit on a branch someone can tag.** Work is protected by
a ref nobody releases from; history on branches contains only work an agent chose to commit.
## Could this become a fleet standard?

Yes, with these steps: (1) owner approves the reconciliation table; (2) kit copied into
`templates/agent_kit/` and into each actively developed repo by a script; (3) `core.hooksPath`
set by the bootstrap; (4) add a `git-hooks` check to the daily dashboard (repos missing
`AGENTS.md` or with `core.hooksPath` unset); (5) port the hook for JS and Python manifests.
Work is a day or two of AI-assisted effort, most of it the port and the dashboard check.
