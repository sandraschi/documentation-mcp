---
title: "Agent Branch Discipline — Scope of Unsupervised Work"
category: pattern
status: active
audience: mcp-dev
related:
  - standards/GIT_REPOSITORY_SAFETY.md
  - patterns/FLEET_MESHING_PHILOSOPHY.md
last_updated: 2026-10-25
---

# Agent Branch Discipline

**Status**: Active
**Origin**: 2026-09-25, observed directly while fixing an unrelated bug in `aiwatcher-mcp` — its working tree had seven modified, uncommitted files (`interests.json`, `pyproject.toml`, `src/aiwatcher_mcp/bundle_presets.py`, `src/aiwatcher_mcp/gmail_ingestion.py`, `uv.lock`, `native/build.ps1`, `src-tauri/build.ps1`) with no attributable owner, no commit, and no indication anyone intended to finish or revert them.

---

## 1. The antipattern

Multiple agents (Claude Code, opencode, Cursor, Antigravity, and their various sub-sessions and worktrees) can touch the same fleet repo independently, on their own timelines, with no shared awareness of each other. This is fine and expected — it's the whole point of running several tools against the same fleet. The failure mode is specific: **an agent modifies files toward some goal, doesn't finish, and ends its turn without either completing the change (commit) or discarding it (revert/stash-and-say-so).** The next agent to touch that repo sees files it didn't change, can't explain, and — correctly — won't commit, because committing someone else's half-finished, unreviewed edit under your own name is worse than leaving it alone.

Repeat this a few times across a few sessions and a repo accumulates a permanent, ownerless layer of dirty state: N files perpetually `git status`-modified, nobody willing to touch them, no way to tell if they're abandoned experiments, in-progress work about to resume, or something already superseded elsewhere. This is worse than either extreme (a clean tree, or a deliberately-committed WIP branch) because it's invisible drift with no expiry.

## 2. Scope: what unsupervised agent work is fine for

| Category | Unsupervised multi-agent work | Why |
|---|---|---|
| Documentation | Fine | Additive, low blast radius, easy to review/merge, conflicts are usually just merge-friendly prose |
| Prettifying / formatting | Fine | Mechanical, reversible, low risk of behavior change |
| Extending plans / specs | Fine | Same as docs — proposals, not commitments |
| Writing tests | Mostly fine | Additive by default; only risky if it touches fixtures/conftest shared with other in-flight test work |
| **Source code an agent doesn't intend to finish and commit in the same session** | **Not fine** | This is the actual failure mode — half-applied refactors, second-guessed approaches abandoned mid-way, speculative rewrites left dangling |
| Shared infra config (NSSM, ports, CI, scaffold templates) | Not fine without explicit scope and a finished, committed change | Blast radius extends to every other agent/service depending on it — see `FLEET_MESHING_PHILOSOPHY.md` for what happens when shared infra drifts uncoordinated |

The line isn't "agents shouldn't work independently" — it's **"don't leave source in a state nobody chose."** A file is either finished and committed, or it's reverted. There is no third state that's acceptable to leave behind.

## 3. The rule

**Before ending a turn that touched source files in a shared fleet repo:**

1. If the change is complete and verified (tests pass, builds, whatever this repo's gate is): commit it. Don't defer "I'll commit later" — later is how the aiwatcher-mcp pile happened.
2. If the change is incomplete and won't be finished this session: **revert it** (`git checkout -- <file>` / `git restore <file>`) rather than leaving it dirty. An abandoned idea should leave no trace, not a landmine for the next agent.
3. If the change is intentionally a checkpoint for a longer-running task that will resume later (legitimate case): commit it anyway, with a `wip:` prefix and a clear message saying so, so the next agent can see it was deliberate and attributable, not orphaned. An uncommitted WIP pile and a committed `wip:` checkpoint look identical in `git status` until someone reads the log — commit it.
4. **Never assume dirty files found at the start of a session are yours to resolve.** Per the pattern observed here: don't stage, commit, or discard files you didn't touch this session unless the user explicitly asks you to clean them up. Flag them, don't silently absorb or silently ignore them.
5. **Whose WIP it is decides what you may do with it.** Do not treat all dirty state identically:
   - *Your own other session* (another Sandra chat/session/agent run, especially days old — day-end close is the standard, so a days-old pile is abandoned, not in flight): fair game. Finish it: commit and push when the target repo is ours and the change is good (attribute honestly; `backlog:` prefix when it predates this run); revert when it is superseded or sits where it should not (fleet edits inside an upstream checkout, for example). Never push to a remote you do not own.
   - *A collaborator's WIP* (Steve's branch, Steve's draft, anything clearly his): hands off entirely. Flag it, do not edit it, do not quality-drive-by it. Harmony outranks tidy trees.
   - *Upstream checkouts* (`_upstream/`, submodules pointing at other owners): read-only. Local modifications there have no pushable home — revert to pristine (noting the content first when it looked intentional) rather than committing into someone else's tree.

## 4. Why this is a *branch* discipline question, not just a git-hygiene one

Most fleet repos are worked on directly on `main`/`master` rather than feature branches (see `GIT_REPOSITORY_SAFETY.md` — checkpoint commits, push-immediately). That makes the antipattern worse than it would be on isolated branches: dirty uncommitted state on the trunk blocks every subsequent operation that needs a clean tree (rebase, `git stash` for a *different* legitimate reason, a clean-clone verification, a release tag) for every agent and every human, not just whoever left it. A branch-per-task convention would contain this — but per the user's explicit position, ad-hoc agent branches for exploratory/second-guessing work are exactly what's *not* wanted either, since that produces its own failure mode (conflicting parallel WIP nobody reconciles). The resolution isn't "more branches," it's discipline on the trunk: finish or revert, every time, every agent.

## 5. Related: stash/restore/force-push danger

Separately from the dirty-WIP problem, `git stash`, `git restore`, and force-push are individually dangerous operations that have already cost this fleet real work — see `GIT_REPOSITORY_SAFETY.md` §7 (BUG-043): a pre-commit hook's own stash/pop cycle has silently wiped a full session of tracked edits at least twice. That section's "snapshot first, verify after every op" discipline reduces the danger but doesn't eliminate it — the safest position is still to have as little uncommitted state lying around as possible when any of these operations might run, which is the same conclusion as §2-3 above from a different angle: commit or revert, don't let things sit dirty.
