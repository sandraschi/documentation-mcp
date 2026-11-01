---
title: "WIP commit standard (nightly sweep)"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-10-24
---
# WIP commit standard (nightly sweep)

**Version:** 1.1 (2026-10-24: BUG-089 launcher-zeroing exclusion). **Owner:** Sandra. **Script:**
[`scripts/Invoke-FleetWipSweep.ps1`](../scripts/Invoke-FleetWipSweep.ps1).
**Supersedes:** `scripts/fleet_git_sync_simple.py` (blind `git add .`, one
fixed message, no checks - do not use).

## Why

Work happens in many agents (Claude Code, opencode, Antigravity) across
~100 chats a day. Nobody remembers which session left which edit. Uncommitted
work accumulates for weeks and then dies in a `git checkout` or a disk event
(chip-design-mcp, 2026-05-31). WIP that is wrong is rare; WIP that is lost is
not. Therefore: **all work is committed and pushed every night, whoever made it.**

## Rules

1. **Nothing uncommitted survives the night.** The sweep runs daily at 04:00
   (Task Scheduler `\Fleet\WipSweep`) over every git repo directly under
   `D:\Dev\repos`, commits all WIP and pushes.
2. **Agents commit everything they find, not only their own edits.** "Not
   mine" is not a reason to leave WIP uncommitted. Applies at the end of any
   session in a repo, independent of the nightly sweep.
3. **WIP commits are honest about being WIP.** Message:
   `wip(auto): <date> <time> - <dir> (<n>), ...` plus trailer
   `WIP-Auto: wip-sweep v1`. Agent-made WIP commits use `WIP: <what>`.
   They may be non-atomic; history readers filter with
   `git log --grep "WIP-Auto"`. Squash later if a release needs clean history.
4. **Batch size: 10 files per commit for code, relaxed for harmless changes**
   (owner decision 2026-10-13). The sweep groups files by top-level directory
   and kind:
   - code and config: at most 10 files per commit (fleet batch rule);
   - documentation and help (`.md .markdown .txt .rst .adoc` anywhere, plus
     images/html/css under `docs/`, `doc/`, `help/`): at most 50 per commit
     (`-DocChunkSize`), message tagged `[docs]`;
   - untracking generated dirs committed by mistake (`node_modules`, `venv`,
     `__pycache__`, ...): ONE deletion-only commit per repo,
     `chore(auto): untrack generated dirs (...)`, via `git rm -r --cached`
     (files stay on disk) plus the matching ignore rule.
   Note: the 2026-10-13 first live run applied the untracking exception before
   the owner had approved it; recorded here as a process error.

5. **Quick analysis, not review.** Deterministic checks only, no LLM, seconds
   per repo. A file that fails a check is left uncommitted and reported; the
   rest of the repo is still committed.

| Check | Action |
|---|---|
| Secret-looking content (Google/GitHub/OpenAI/AWS/Slack keys, private-key blocks) or secret filenames (`.env`, `*.pem`, `*.key`, `*.pfx`, `id_rsa*`; `.env.example` allowed) | exclude, report |
| Generated dirs untracked and not ignored (`node_modules`, `.venv`, `venv`, `__pycache__`, `dist`, `build`, `target`, `.pytest_cache`, `.ruff_cache`, `.next`, `.turbo`) | append to `.gitignore` (committed), exclude contents |
| File larger than 50 MB | exclude, report (GitHub rejects 100 MB) |
| Merge-conflict markers in a text file | exclude, report |
| Tracked file truncated to 0 bytes (was >= 100 bytes at HEAD) | exclude, report (chip-design lesson) |
| `fleet-start.config.ps1` modified toward *disabled* (live ports -> 0, live Kind -> `none`) or deleted (BUG-089) | exclude, report - a WIP commit must preserve work, never ratify a disabled launcher; needs human review |
| Generated dirs already tracked in git | untrack in one commit (rule 4 exception), add ignore rule |
| More than 400 files still eligible after the above | skip repo, report as triage (usually a missing ignore rule) |

6. **Repo state gates.** Repos in `-SkipRepos` (test fixtures that must stay
   broken, default `this-is-intentionally-broken-for-testing`) are never touched.
   Skip (and report) when: `.git/index.lock` exists
   (another tool is mid-operation), a merge/rebase/cherry-pick is in progress,
   HEAD is detached.
7. **Snapshot before committing** (BUG-043): `git stash create` hash is
   written to the log before the first commit in a repo; `git stash apply
   <hash>` restores the pre-sweep worktree if a hook ate something.
8. **Hooks.** Commits run pre-commit hooks normally. The 04:00 task runs with
   `-NoVerifyFallback` (owner decision 2026-10-13). If a hook rewrites files
   (formatters), the sweep re-adds and retries once. If hooks still fail, the
   chunk stays uncommitted and is reported - unless the sweep runs with
   `-NoVerifyFallback`, which commits with `--no-verify` and tags the message
   `[hooks-failed]`. Whether the 04:00 task uses `-NoVerifyFallback` is the
   owner's decision (see the task registration in the script header).
9. **Push.** Current branch to its upstream. Behind upstream: `git pull
   --rebase`; on conflict, `git rebase --abort`, keep the local commits,
   report. No upstream but `origin` exists and the branch is the GitHub
   default: `git push -u origin HEAD`. No remote: report (never auto-create
   GitHub repos at 04:00). Never force-push.
10. **Log.** One report per run in
    `mcp-central-docs/operations/session-log/wip-sweep-<date>.md`: repos
    committed, commits, pushed, excluded files with reasons, triage list,
    stash hashes. The sweep commits its own log last.

## Daily dashboard

After the sweep, the same task builds one static page for bookmarks and the
browser start screen (no server needed):

`file:///D:/Dev/repos/mcp-central-docs/operations/daily/index.html`

Prioritised: needs you (failing CI, sweep problems, held-back files, open PRs,
GitHub notifications, uncommitted/unpushed repos, low assfix scores), cooking
(24h), this week, assfix scores with rendered reports, the latest of every
report family (WIP sweep, Fritz sweep, session log, assfix tally, heartbeat,
RAG tally, guide freshness, starts scan, audits, port registry), and the
books. A banner appears when the page is older than 26 hours. Generator:
`scripts/build_daily_dashboard.py` (output gitignored). Add a report family
by appending to `REPORT_FAMILIES` there.

## Running it by hand

```powershell
# read-only preview
powershell -NoProfile -ExecutionPolicy Bypass -File D:\Dev\repos\mcp-central-docs\scripts\Invoke-FleetWipSweep.ps1 -DryRun
# one repo
powershell -NoProfile -ExecutionPolicy Bypass -File ...\Invoke-FleetWipSweep.ps1 -Only on-metacraft
# install the 04:00 task (Task Scheduler \Fleet\WipSweep)
powershell -NoProfile -ExecutionPolicy Bypass -File ...\Invoke-FleetWipSweep.ps1 -Install
```

## Relation to other standards

- [GIT_REPOSITORY_SAFETY.md](./GIT_REPOSITORY_SAFETY.md) section 6 (push gate)
  and 7 (pre-commit insurance) remain in force; this standard is their
  nightly enforcement.
- Batch rule (10 files per commit) is respected by chunking. Committing does
  not modify working files, so the sweep is not a batch *mutation*; the only
  file it writes is `.gitignore`, at most once per repo per run.
