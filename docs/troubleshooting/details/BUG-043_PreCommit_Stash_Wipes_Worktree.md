# BUG-043 — Pre-commit Stash Cycle Silently Wipes Tracked Modifications

- **ID**: `BUG-043`
- **Severity**: `P1` (silent worktree data loss; recovered, see below)
- **Date**: 2026-09-20
- **Repo/Component**: `resonite-mcp` — stock `pre-commit` hook flow
  (`ruff`, `ruff-format`, `biome`, whitespace/yaml/size checks) during a
  multi-commit `commit all` sequence
- **Status**: Work recovered byte-identical; root trigger not isolated —
  insurance rule added to GIT_REPOSITORY_SAFETY.md §7 instead of a fix
  claim

## Symptom

Mid-sequence (`git add` + `git commit` on 4 tracked files), the commit
produced no commit and afterwards **every tracked modification in the repo
was gone from disk**: `git status` showed only untracked files, and content
greps confirmed session work (backend endpoints, page rewrites, docs) had
vanished. Zero errors from git or any hook. An earlier commit in the same
sequence had already landed fine, which made the empty tree look almost
plausible — the loss was caught only because the next `git add` staged
nothing.

## Root Cause (not fully isolated — read carefully)

`git commit` with unstaged files present makes pre-commit stash the
unstaged work, run hooks, then pop the stash. This sequence ran that cycle
repeatedly (hook-failure → reformat → re-stage → retry), and at some point
a pop restored an empty/older state instead of the stashed work. Suspects,
not proven: a pop applied after the index had already moved (the landed
commit between attempts), compounded by an unrelated killed subprocess in
the same shell session minutes earlier. No evidence of user-side
`checkout`/`restore`/`reset` — none was run.

## Recovery (worked, byte-identical)

pre-commit leaves its stash patches on disk even when the pop goes wrong:

```powershell
Get-ChildItem C:\Users\<user>\.cache\pre-commit\ -Recurse -File |
  Sort-Object LastWriteTime -Descending
```

The two patches from the failed runs (146KB + 149KB) contained every lost
diff. Restored with `git apply` (minus one hunk already present in the
worktree), then proved integrity: content greps hit on every feature and
the full suite passed **118/118** before recommitting.

## Never-again rule (now GIT_REPOSITORY_SAFETY.md §7)

1. **Snapshot before every commit while unstaged changes exist**:
   `git stash create` — creates the stash commit WITHOUT touching index
   or worktree, prints the hash. Keep the hash until the push succeeds.
   If the tree ever looks wrong: `git stash apply <hash>`.
2. **Verify after every git op**: `git status` path counts + one content
   grep before moving on. The loss here survived unnoticed across a
   command boundary because nobody re-checked.
3. **Expect the stash dance**: any `git commit` with unstaged files
   present triggers it. Prefer staging exactly the commit's files (already
   the 5-file rule) AND snapshotting first — belt and suspenders.

## Secondary finding (same session, same hooks)

The hook env's `ruff-format` reformats what the project's pinned ruff
calls clean (and vice versa) — i.e. hook toolchain and project toolchain
have drifted versions. Harmless here (whitespace-only diffs, reviewed),
but it means "ruff clean" is version-dependent. Follow-up: pin the hook
rev to the project's ruff version.

## Related

- Same silence class as BUG-042 (tooling lies by omission, no error) but
  destructive rather than confusing — hence P1.
- Cousin of the chip-design-mcp 0-byte incident in GIT_REPOSITORY_SAFETY:
  both are "work evaporates with no error"; this one had a recovery path
  only because pre-commit's debris happened to survive.

## Second occurrence — 2026-09-24, advanced-memory-mcp (variant mechanism)

Same class, different trigger path — this one isolates the loss mechanism
better than the first:

- Setup: `git add <5 files>; git commit` with *other* modified files left
  unstaged (deliberate small commits), so every attempt entered pre-commit's
  stash/pop path.
- The `ruff-format` hook kept reporting "2 files reformatted" and aborting.
  Each retry re-ran stash → hooks → conflict → "Stashed changes conflicted
  with hook auto-fixes... Rolling back fixes... Restored changes".
- After several cycles, previously-written tracked content was gone from
  disk: telemetry hooks (`adn_skills.py`), a full HTTP router block
  (`management_router.py`), a page rewrite (`SkillStudio.tsx`), API methods
  (`api.ts`) — while `git status` showed clean and zero errors appeared
  anywhere. Proven live first (browser test passed against the UI, API
  served the routes), gone later: not a write failure, a revert.
- Recovery: full rewrite from scratch (no usable patch debris this time —
  leftover `.cache\pre-commit\patch*` files were all 818 bytes of format
  residue). Cost: one full rewrite session.
- New evidence vs first occurrence: the loss hits files that were never
  staged in the failing commits (only *present* as unstaged changes during
  the stash cycles), and the "Rolling back fixes" path is implicated
  directly — not just a bad pop. The stash/pop + auto-mutating-hook
  combination is confirmed lossy under retry, not merely suspected.

## Hardened never-again (extends §7 — learn from both occurrences)

1. **One failed hook-commit = stop and audit.** Never retry the same commit
   more than once without `git status` + content spot-checks. Both
   occurrences involved 3+ blind retries; the loss compounded each cycle.
2. **Run hooks before staging, not during commit**: `pre-commit run` (or
   the raw `ruff check`/`ruff format`) until green, *then* `git add` +
   commit. A green tree never enters the mutate-and-retry loop at all.
3. **One ruff version everywhere.** Hook rev, venv dev dep, and system ruff
   disagreed here (0.16.0 vs 0.15.16) — format rules drift between versions,
   which manufactures exactly the fail-fix-fail cycle that triggers repeated
   stash/pop runs. Pin all three to the same version.
4. **Consider check-only hooks.** `ruff --fix` and `ruff-format` mutate the
   tree mid-commit by design; a check-only hook fails without touching
   anything, which removes the entire loss surface (at the cost of one
   manual fix-up step agents must run first — which rule 2 already requires).
