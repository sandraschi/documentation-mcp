# CI Check SOP — Workflow Health Pulse

**Phase**: Read-only. Never re-run or cancel workflows. Report status for user action.

## Purpose

Given a repo (fleet or third-party), check the latest CI workflow runs and report pass/fail per workflow, with failure details. Useful before shipping, before opening a PR, or when a CI notification arrives.

## Procedure

### Phase 1: List recent workflow runs

```powershell
gh run list --repo <owner>/<repo> --limit 15 --json name,conclusion,status,headBranch,createdAt,displayTitle,workflowName
```

This returns the most recent runs across all workflows. Flags:
- `conclusion`: `success`, `failure`, `cancelled`, `null` (in progress)
- `status`: `completed`, `in_progress`, `queued`, `pending`

### Phase 2: Get failure details

For each failed run, get the annotated log:

```powershell
gh run view <run-id> --repo <owner>/<repo> --log --jq '.steps[] | select(.conclusion == "failure") | {name, number, conclusion}'
```

Extract:
- Which step failed (test, build, lint, deploy, etc.)
- The job name
- The branch the failure is on

### Phase 3: Summarize

```
| Workflow | Branch | Status | Conclusion | Failed step | Age |
|----------|--------|--------|------------|-------------|-----|
| CI       | main   | completed | ✅ success | — | 2h |
| Lint     | feature/x | completed | ❌ failure | ruff check | 15m |
| Deploy   | main   | in_progress | ⏳ running | — | 5m |
```

### Phase 4: For fleet repos, cross-reference

If the repo is a fleet repo (`sandraschi/<repo>`), additionally check:

1. Whether the failure is pre-existing (was the last green run before the user's changes)
2. Whether the failing workflow is on the default branch (main) — indicates a broken gate
3. Whether the failure is a CI infrastructure issue (runner unavailable, timeout, cache miss) vs a real test failure

## Reporting

Report:
- Total workflows checked
- Pass/fail counts
- For each failure: workflow name, branch, failed step, and a one-line hint (e.g., "Likely pre-existing — last green was 3d ago on commit abc123")
- If all green: "All CI workflows green."

## Anti-Patterns

- **Do not re-run failed workflows** — the user decides when to re-trigger
- **Do not cancel running workflows** — let them complete
- **Do not open PRs to fix CI** — report the failure, let the user decide
- **Do not interpret CI logs beyond the failed step name** — log content may contain secrets or irrelevant noise

## Verification

- Every failed run has a failed step identified
- Every failing workflow notes which branch it's on (main vs feature — important for determining "is this pre-existing?")
- Report distinguishes between CI infrastructure failures (runner offline, out of disk) and code failures
