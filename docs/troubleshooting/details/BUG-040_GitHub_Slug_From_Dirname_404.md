# BUG-040 — GitHub Slug Derived From Local Dirname 404s Renamed Repos

- **ID**: `BUG-040`
- **Severity**: `P2` (non-blocking: scan continues, errors collected per repo)
- **Date**: 2026-09-18
- **Repo/Component**: `git-github-mcp` — `services/fleet_catalog.py::registry_to_github_slugs`
  (consumers: `fleet_health.op_ci_pulse`, `op_dependabot_digest`,
  `fleet_catalog.op_quarantine_report`)
- **Status**: Fixed, pushed as `3a53432`. Live on next 10713 backend restart.

## Symptom

Breakfast scan log after an elevated 10713 restart:

```text
git-github-mcp.response ERROR Tool error: failed to get runs: HTTP 404: Not Found
  (https://api.github.com/repos/sandraschi/meta_mcp/actions/runs?per_page=8&exclude_pull_requests=true)
  [workflow_runs]
git-github-mcp.response ERROR Tool error: failed to get runs: HTTP 404: Not Found
  (https://api.github.com/repos/sandraschi/avatar-mcp/actions/runs?per_page=8&exclude_pull_requests=true)
  [workflow_runs]
```

Neither `sandraschi/meta_mcp` nor `sandraschi/avatar-mcp` exists on GitHub.

## Root Cause

`registry_to_github_slugs` fell back to the bare registry id (== local directory
name) whenever an entry had no explicit `github_repo` field. Local dir names
drift from GitHub names on renames, and the fleet has 14 such drifts (audit
2026-09-18, dirname vs `git remote get-url origin`):

| Local dir | Origin (truth) |
|---|---|
| `meta_mcp` | `sandraschi/meta-hypertools` |
| `avatar-mcp` | `sandraschi/avatarmcp` |
| `ag-gazebo-bridge` | `sandraschi/gazebo-mcp` |
| `calibre-mcp` | `sandraschi/calibremcp` |
| `docker-mcp` | `sandraschi/dockermcp` |
| `fritz-test-work` | `sandraschi/fritz-test` |
| `handbrake-mcp` | `sandraschi/handbrakemcp` |
| `multi-backup-mcp` | `sandraschi/hasleo-backup-mcp` |
| `obsidian-mcp` | `sandraschi/obsidianmcp` |
| `plex-mcp` | `sandraschi/plexmcp` |
| `pywinauto-mcp` | `sandraschi/windows-computer-use-mcp` |
| `videogen-mcp` | `sandraschi/ittybittyvideos` |
| `vroidstudio-mcp-backup-20260607-231839` | `sandraschi/vroidstudio-mcp` |
| `winrar-mcp` | `sandraschi/winrarmcp` |

## Resolution

Precedence in `registry_to_github_slugs`, via new `_origin_slug()` helper that
parses the local clone's `origin` URL (https + ssh, optional `.git`):

1. explicit `github_repo` registry field (unchanged escape hatch — wins),
2. clone `origin` remote owner/repo (ground truth),
3. bare registry id (old behavior, last resort).

Verified by executing the resolver, not by reading the diff: 3/3 remote-derived
slugs correct, missing-dir falls back to dirname, explicit field wins,
`ruff check` + `ruff format --check` clean. One file, 41+/2-.

## Detection Next Time

Any `HTTP 404` on `repos/<owner>/<repo>/actions/runs` or
`repos/<owner>/<repo>/dependabot/alerts` inside a fleet scan means the slug is
wrong, not that GitHub is down. Re-run the audit one-liner:

```powershell
Get-ChildItem -LiteralPath "D:\Dev\repos" -Directory | ForEach-Object {
  $u = & "C:\Program Files\Git\cmd\git.exe" -C $_.FullName remote get-url origin 2>$null
  if ($u -match 'github\.com[:/]([^/]+)/([^/]+?)(\.git)?/?$' -and $Matches[2] -cne $_.Name) {
    Write-Output ($_.Name + " -> " + $Matches[1] + "/" + $Matches[2])
  }
}
```

## Related

- Same class as BUG-021/024 (silent wrong-source data), but inverted: here the
  failure is loud (404 in the log) while the cause (stale name mapping) is quiet.
- Follow-up candidate: `workflow_runs` fetches
  `databaseId,name,status,conclusion,headBranch,createdAt,url` only — ci_pulse
  shows failed runs but not failure reasons. Per-run `gh run view --json jobs`
  would add the why.
