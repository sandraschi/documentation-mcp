# Fork Trawl SOP — Classify GitHub Forks by Signal

**Phase**: Read-only analysis. Never modify forks. Report findings for user action.

## Purpose

Given a repo (ours or a third-party project), enumerate its GitHub forks and classify each as **real work**, **autoscraped**, or **derivative**. Real-work forks may contain patterns worth adopting (custom conventions, bug fixes, features). Autoscraped forks are noise.

## Signals

| Classification | Signals |
|---|---|
| **Real work** | > 1 substantive commit (not just mirror), code changes beyond config/docs, has branches, issues, PRs, or recent activity |
| **Autoscraped** | 0-1 commits (just the initial fork mirror), no changes, no branches, 1 contributor, stale |
| **Derivative** | Light changes only: README translation, CI config tweaks, `.gitignore` additions, dependency bumps |

## Procedure

### Phase 1: Enumerate forks

```
gh repo list <owner>/<repo> --fork --limit 50 --json name,owner,forkCount,createdAt,updatedAt
```

### Phase 2: Gather per-fork signals

For each fork, batch-request:

```
gh api repos/<owner>/<fork>/commits?per_page=5
gh api repos/<owner>/<fork> --json defaultBranch,openIssueCount,openPrCount,forksCount,pushedAt
```

### Phase 3: Classify

| Signal | Real work | Autoscraped | Derivative |
|---|---|---|---|
| Commits beyond initial mirror | Yes | No | Maybe (1-2 trivial) |
| Changed non-doc, non-config files | Yes | No | No |
| Has branches | Often | No | No |
| Open issues or PRs | Sometimes | No | Rarely |
| Recency (< 6 months) | Usually | Can be either | Usually |
| > 1 contributor | Sometimes | No | No |
| Changed `src/` or `lib/` | Yes | No | No |

**Hard rule**: If a fork has zero changed files beyond `.gitignore`, `.github/`, or `README.*`, classify as **autoscraped** regardless of commit count.

### Phase 4: For real-work forks, extract signal

For each real-work fork, run:

```
gh api repos/<owner>/<fork>/compare/main...<default-branch>
```

Then for meaningful patterns:

1. Read changed files for novel conventions, bug fixes, or architecture decisions
2. Check if any patterns are worth upstreaming or adopting fleet-wide
3. Record the fork URL and key findings. Do NOT clone, file issues, open PRs, or contact the fork author. That is the user's call.

### Phase 5: Report

Output table:

```
| Fork | Owner | Classification | Commits | Changed files | Last push | Key finding |
|------|-------|---------------|---------|---------------|-----------|-------------|
| memops | otherdev | Real work | 12 | 47 (src/) | 2026-06 | Per-dir INFO.md pattern |
| calibre-mcp | copymirror | Autoscraped | 1 | 0 | 2026-01 | — |
```

Include:
- Total forks scanned
- Real work count (with URLs)
- Autoscraped count
- Derivative count
- Top 1-2 patterns worth investigating

## Anti-Patterns

- **Do not clone forks** — read-only API queries only unless the user explicitly asks
- **Do not open issues/PRs** against forks — that's the user's decision, not the agent's
- **Do not judge by star count** — a fork with 0 stars can be a goldmine; a famous fork can be autoscraped
- **Do not spend time on autoscraped forks** — check commit count first, skip the deep analysis

## Verification

- Every fork is classified
- For each "real work" fork, at least one key finding is recorded (even if "nothing novel")
- The report includes both positive (real work) and negative (autoscraped) results — a report that only shows real work is cherry-picked
