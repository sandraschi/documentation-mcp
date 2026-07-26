---
name: ship
description: Final release gate for a fleet MCP server repo under D:\Dev\repos -- run all quality gates, build the release artifact, verify it, commit, push, and cut a GitHub release. Trigger this whenever the user says "ship it", "ship" followed by a repo name, "release" followed by a repo name, or asks to finalize and publish work that's already been done in a repo. This is the terminal step after assfix/nsis-build, not a substitute for them -- if the repo hasn't been assessed recently, say so before shipping rather than shipping blind.
---

# ship — final release gate

Claude Desktop / Cowork port of the opencode `ship` macro
(`mcp-central-docs/standards/rules/agentic_macros.md`). This is deliberately the
*last* thing that happens to a repo in a work session — it assumes the actual
feature/fix work is already done and reviewed. If the user says "ship it" right
after describing new work you haven't verified yet, that's a signal to run the
gates for real (Phase 1 below), not to rubber-stamp and push.

## Phase 0 — Nopublish check

`Glob` for `.nopublish` at the repo root. If it exists, **stop immediately** and
report "repo is marked .nopublish — no artifact build, no git push, no release."
This is a hard stop, not a warning to note and continue past — `.nopublish` exists
specifically so private repos never accidentally get pushed or released.

## Phase 1 — Gates (abort on any failure)

Via `winops_cmd_powershell`, from the repo root:

```powershell
uv run ruff check src/ --quiet
uv run ruff format src/ --check --quiet
uv run pytest tests/ -q
```

If a webapp exists, also `npx tsc --noEmit`. **Any non-zero exit aborts the ship —**
do not build or push a repo with failing gates. Report exactly which gate failed and
its output; don't just say "gates failed" and stop, since the person needs to know
whether it's a one-line lint fix or a real test failure blocking release.

This is a check, not a fix pass — if something's broken, that's the `assfix` skill's
job (Phase 2/3), not this one's. Point the user at it rather than trying to fix
things inline here; `ship` should stay fast and predictable.

## Phase 2 — Build the release artifact

Detect which artifact this repo produces:

- **Has `native/` (Tauri)** → run the `nsis-build` skill's Phase 2–3 (build + size
  gate). The artifact is `native/target/release/bundle/nsis/*-setup.exe`.
- **No `native/`, has `pyproject.toml` with `fastmcp`** → MCPB package per
  `PACKAGING_STANDARDS.md` / the `assfix` skill's Phase 5. The artifact is
  `dist/{name}-v{version}.mcpb`.
- **Neither** → ask the user what "ship" means for this repo rather than guessing;
  not every repo in the fleet produces a packaged artifact (some are library-only or
  infra daemons with no distributable).

## Phase 3 — Verify artifact

Confirm the file exists and has a plausible size (NSIS installer: >=1 MB; `.mcpb`:
non-trivial, more than a few KB — an empty or near-empty bundle means the pack step
silently failed to include `src/`). Report the exact path and size. Do not proceed
to Phase 4 on an artifact you haven't actually confirmed exists on disk.

## Phase 4 — Version bump check

Before committing, check whether `pyproject.toml`'s `version` differs from the
latest git tag (`git describe --tags --abbrev=0` via `winops_cmd_powershell`). If it
does, a GitHub release should be cut in Phase 6. If it doesn't, this is a patch/fix
ship with no new release — that's fine, just skip Phase 6's release creation and say
so rather than creating a release with a duplicate or stale version tag.

## Phase 5 — Commit and push

```powershell
git add -A
git status --porcelain   # read this before committing -- see note below
```

**Read the status output before committing.** A repo can have unrelated in-progress
changes from another session (this happened mid-fleet this session — `classroom-mcp`
had 27 staged `.bak` files and multiple modified core files that had nothing to do
with the work being shipped). If `git status` shows changes you don't recognize as
part of what you were asked to ship, stop and ask rather than sweeping them into the
release commit.

```powershell
git commit -m "ship {repo}: {one-line summary}"
git push
```

**If `git commit` or `git status` hangs** (confirmed reproducible on at least one
fleet repo, `mcp-central-docs`) — don't wait it out repeatedly. Use the plumbing
fallback instead:

```powershell
$tree = git write-tree
$parent = git rev-parse HEAD
# write the commit message to a file with the Write tool first, not PowerShell
# string interpolation -- avoids the BOM/here-string traps in TRAPS_AND_PITFALLS.md
$newCommit = git commit-tree $tree -p $parent -F $msgFile
git update-ref refs/heads/main $newCommit $parent
git push
```

If `git push` itself fails or hangs (e.g. running from a sandboxed session with no
outbound git credentials configured), don't report the ship as complete — say
explicitly that the commit exists locally but push needs to happen from the user's
own machine, and give the exact commit sha so they can verify nothing was lost.

## Phase 6 — GitHub release (only if version bumped in Phase 4)

Use `gitops`'s `github_ops` tool (API-based — confirmed reliable this session, unlike
`git_core` which can hang on local git subprocess calls) to create a release from the
new tag:

1. Tag the commit: `git tag v{version}` then `git push --tags` (or fold into the
   push above).
2. Create the release via `github_ops` pointing at that tag, with release notes
   pulled from the relevant `CHANGELOG.md` entry for this version if one exists —
   don't write generic "various fixes" notes when a real changelog entry is sitting
   right there.
3. Attach the built artifact (NSIS `.exe` or `.mcpb`) to the release if the tool
   supports asset upload; otherwise note in the release body where to find it.

## Phase 7 — Report

State plainly: gates (pass/fail per gate), artifact (path + size), commit (sha),
push (succeeded / needs manual push + sha), release (created / skipped + why). This
is the terminal step of a work session — the report should let the user close the
laptop confident about exactly what state the repo is in, not just "done!".
