# GitHub Fleet Audit — SOP

**Trigger**: `ghaudit`
**Reference macro**: `agentic_macros.md` → `ghaudit`
**Scope**: Fleet-wide GitHub hygiene scan. Check issues, PRs, CI status, repo metadata, stale branches, cross-reference known bugs. All from CLI — no browser needed.

---

## Why ghaudit

GitHub repos drift silently: topics go missing, descriptions become stale, old issues pile up, CI starts failing and nobody notices, branches rot. `ghaudit` surfaces all of it in one report. Run it weekly to keep the fleet visible.

**Rule**: Report, never touch. Do not close issues, merge PRs, or update repo settings. Present findings for the user to decide.

---

## Phase 1 — Auth & context

```powershell
gh auth status
```

If not authenticated, stop and report. The entire audit depends on the GitHub CLI.

Determine the org/user: `sandraschi` (fleet repos are under this account). If fleet repos span multiple orgs, detect from repo remotes.

---

## Phase 2 — Per-repo probes

For each repo in `D:\Dev\repos` that has a `.git` directory and a GitHub remote:

### 2A. Open issues

```powershell
gh issue list --repo sandraschi/{repo} --limit 20 --json number,title,state,createdAt,labels,updatedAt
```

| Signal | Flag |
|--------|------|
| Any issues without labels | LOW — untriaged |
| Issues older than 30 days with no activity | MEDIUM — stale |
| Issues older than 90 days with no activity | HIGH — abandoned |
| Issues mentioning "bug" or "crash" in title | MEDIUM — potential bug |

### 2B. Open PRs

```powershell
gh pr list --repo sandraschi/{repo} --state open --limit 20 --json number,title,headRefName,createdAt,updatedAt,reviews,statusCheckRollup
```

| Signal | Flag |
|--------|------|
| PRs older than 14 days with no activity | MEDIUM — stale |
| PRs with failing CI checks | HIGH — broken |
| PRs with no reviews requested | LOW — unreviewed |
| PRs with `draft` status older than 30 days | LOW — abandoned draft |

### 2C. CI status

```powershell
gh run list --repo sandraschi/{repo} --limit 5 --json conclusion,displayTitle,createdAt,event
```

| Signal | Flag |
|--------|------|
| Latest run failed | HIGH — CI broken |
| Last 3 runs all failed | CRITICAL — CI consistently broken |
| No runs in the last 14 days | MEDIUM — CI disabled or no pushes |
| No CI workflow at all (`.github/workflows/` missing) | MEDIUM — no automation |

### 2D. Repo metadata

```powershell
gh repo view sandraschi/{repo} --json name,description,repositoryTopics,primaryLanguage,isArchived,isFork,isPrivate,stargazerCount,forkCount,watcherCount,hasWikiEnabled
```

| Signal | Flag |
|--------|------|
| Description empty or default | HIGH — missing description |
| Description is placeholder ("Fleet MCP server" only) | LOW — too generic |
| Fewer than 3 topics | MEDIUM — undiscoverable |
| No `mcp` topic tag | MEDIUM — won't appear in MCP ecosystem searches |
| Archived or fork | INFO — note in report |
| **Private** (not public) | HIGH — users can't find it. Fleet MCP servers should be public unless there's a specific reason (secrets, unreleased product). Flag for review. |
| **Stars** = 0 and repo is >3 months old | LOW — no community traction |
| **Stars** dropped by >10% in 30 days | MEDIUM — unusual (check for controversy) |
| **Forks** = 0 and repo is public | INFO — nobody is building on it |
| **Watchers** = 0 | INFO — nobody is watching for releases |
| **Wiki disabled** on a public repo | LOW — wiki off by default; consider enabling if docs are complex |
| **Forks >> stars** (forks > 3x stars, or forks > 10 and stars < 5) | HIGH — scrapers, not humans. Real repos don't get 20 forks and 5 stars unless they're being bulk-cloned by bots. Check if the repo has genuine community engagement (issues, discussions) or just fork noise. |
| **Stars >> forks** (e.g. 100 stars but 0 forks) | INFO — popular but not forkable (private?) |

For repos with significant community signal, track the trend:
```powershell
# Compare with previous report if one exists
Select-String -Path "docs/ghaudit-reports/*.md" -Pattern "{repo}" -SimpleMatch
```
Flag repos where star count dropped since last report.

### 2E. Stale branches

```powershell
gh api repos/sandraschi/{repo}/branches --paginate --jq '.[] | select(.commit.commit.author.date | fromdate < now - 90*86400) | .name'
```

| Signal | Flag |
|--------|------|
| Branches with no commit in 90+ days | LOW — stale, candidate for cleanup |
| Branches with no commit in 180+ days | MEDIUM — should be pruned |

### 2F. README quality check

```powershell
# Read the first 80 lines of the README
gh repo view sandraschi/{repo} --json name,description | ConvertFrom-Json
# Also fetch the README content to check structure
gh api repos/sandraschi/{repo}/readme --jq '.content' | [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_))
```

| Signal | Flag |
|--------|------|
| README is just the default GitHub template | CRITICAL — no custom content |
| No badges at top (just, ruff, python, fastmcp version) | MEDIUM — missing standard fleet badges per `README_STRUCTURE.md` |
| No quick-start section (how to install and run) | HIGH — user can't figure out how to use it |
| No `llms.txt` or `llms-full.txt` link | MEDIUM — LLM can't discover the tool surface |
| No screenshot or demo GIF | LOW — visual preview missing (recommended for wrapper MCPs per `README_WEBAPP_SCREENSHOTS.md`) |
| No port information | MEDIUM — user doesn't know what ports to expect |
| No env var table | MEDIUM — user doesn't know what to configure |
| No Claude Desktop config snippet | MEDIUM — user can't integrate |
| README shorter than 20 lines | HIGH — almost certainly a runt |
| README longer than 200 lines but no table of contents | LOW — hard to navigate |
| Spelling or grammar errors in the first paragraph | LOW — first impression matters |
| **Beauty check**: does the README look good rendered? | Subjective — flag if: no section breaks, walls of text, inconsistent heading levels, no code blocks for CLI examples, no emoji or icon use for visual hierarchy. A README that is functional but ugly is better than a README that is missing, but a beautiful README signals quality. |

### 2G. Search visibility

```powershell
# Search for the repo by name on GitHub
gh search repos "{repo}" --limit 30 --json name,stargazerCount,updatedAt,owner
```

Check where this repo ranks when searching for its own name:

| Signal | Flag |
|--------|------|
| Repo does not appear in the first 30 results when searching by its exact name | HIGH — something is wrong (private? indexed under different name? deleted?) |
| Repo appears but not in the top 5 | LOW — SEO could be better (description + topics + README all feed into search ranking) |

Then search for the category:

```powershell
# Search by primary topic
gh search repos "topic:{primary_topic}" --sort stars --limit 10 --json name,stargazerCount,description,owner
```

| Signal | Flag |
|--------|------|
| Repo does not appear in top 10 when searching by its primary topic (e.g. `mcp-server`, `arxiv`) | MEDIUM — crowded category, needs better SEO |
| Star count relative to top 3: is the repo in the same order of magnitude? | INFO — if top result has 5000 stars and this repo has 3, that's reality-check data, not actionable. Too depressing to flag formally, but note it for the user's awareness. |
| No `mcp` or `mcp-server` topic tag | MEDIUM — won't appear in `topic:mcp-server` searches at all |

### 2H. Release audit

```powershell
gh release list --repo sandraschi/{repo} --limit 10 --json tagName,isLatest,createdAt,publishedAt,name,body
```

| Signal | Flag |
|--------|------|
| No releases at all | HIGH — never shipped. Is this repo production-ready or still experimental? |
| Only one release, created during initial scaffold | MEDIUM — shipped once, never updated. Likely abandoned after the initial `mcpb init`. |
| Last release >6 months ago | MEDIUM — stale. If the repo has recent commits but no releases, development continues but no one has cut a release. |
| Last release >12 months ago | HIGH — abandoned. No releases and no commits in 12mo = dead repo. |
| No release with `.mcpb` artifact | MEDIUM — no MCPB bundle published. Users can't install via Claude Desktop one-click. |
| No release with `*-setup.exe` (NSIS) and `native/` exists | MEDIUM — desktop installer exists in repo but never shipped. |
| Release body is empty or just the tag name | LOW — no release notes. Users don't know what changed. |
| Release body doesn't reference CHANGELOG.md | LOW — changelog exists in repo but releases don't link to it. |
| Release body is clearly autogenerated (tags only, no context) | LOW — better than nothing, but users appreciate human-readable notes. |

Fleet release note standard (recommended, not enforced):

```
## {Version} — {YYYY-MM-DD}

### Added
- {new feature} ({PR #123})
- {new feature}

### Fixed
- {bug fix} ({issue #456})

### Changed
- {breaking change} ({PR #789})

**Artifacts:**
- MCPB: `{name}-{version}.mcpb`
- NSIS: `{name}-{version}-x64-setup.exe` (Windows)
```

This mirrors the `CHANGELOG.md` format from `PACKAGING_STANDARDS.md`. Releases that follow this format get a ✅ in the report. Releases that paste the raw git log get a ⚠️.

### 2I. Known bugs cross-reference

Check the repo's open issues against `mcp-central-docs/troubleshooting/BUGS_DEPOT.md`:

```powershell
Select-String -Path "mcp-central-docs/troubleshooting/BUGS_DEPOT.md" -Pattern "{repo}" -SimpleMatch
```

| Signal | Flag |
|--------|------|
| Bug in depot but no open issue in repo | MEDIUM — known bug not tracked |
| Bug in depot and matching open issue | INFO — tracked |

---

## Phase 3 — Aggregate report

Build a fleet-wide table:

```
=== GHAUDIT: {date} ===

| Repo | Issues | PRs | CI | Description | Topics | Branches | Bugs tracked |
|------|--------|-----|----|-------------|--------|----------|--------------|
| arxiv-mcp | 3 open, 1 stale | 2 open, CI ✅ | ✅ passing | "arXiv research tools" | 5 | 2 stale | 1/1 |
| calibre-mcp | 0 open | 1 stale draft | ❌ failing | "Calibre ebook library" | 2 | 0 stale | 0/2 ✗ |
| ...

Summary:
  Repos scanned:      42
  Repos with CI fail:  3 ⚠️
  Stale PRs:           7
  Stale issues:       12
  Missing topics:      5
  Missing desc:        2
  Untracked bugs:      8 ✗
```

Sort worst-first (CI failures at top, then missing descriptions, then stale issues).

### Phase 4 — Write report

Persist the report to `reports/ghaudit-{YYYY-MM-DD}.md` in the repo root:

```powershell
$reportDir = Join-Path $RepoRoot "reports"
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null
$reportPath = Join-Path $reportDir "ghaudit-$(Get-Date -Format 'yyyy-MM-dd').md"
Set-Content -Path $reportPath -Value $reportText
Write-Host "Report saved: $reportPath" -ForegroundColor Green
```

Also write a lightweight timestamp marker that IS committed (for fleet-wide tracking):

```powershell
$summary = @{
  timestamp = (Get-Date -Format "o")
  repo = $repo
  high = $highCount
  medium = $mediumCount
  low = $lowCount
  ci_pass = $ciPassing
  last_release = $lastReleaseDate
} | ConvertTo-Json
Set-Content -Path ".ghaudit-timestamp" -Value $summary
```

The `reports/` directory MUST be in `.gitignore` — report files are regenerable snapshots, not source code, and committing them creates noise. If it's not in `.gitignore`, add it before writing the report. The first report may remain committed as a baseline; all subsequent reports are gitignored.

The `.ghaudit-timestamp` file IS committed — it's the lightweight audit trail that `assfixstat`-style tools scan fleet-wide.

### Phase 5 — Diff against previous run

Before writing the new report, check if a previous one exists:

```powershell
$prevReports = Get-ChildItem -Path $reportDir -Filter "ghaudit-*.md" | Sort-Object Name -Descending
if ($prevReports.Count -gt 0) {
    $prev = $prevReports[0].FullName
    Write-Host "Previous report: $prev"
    # Key diffs to highlight:
    # - Star/fork/watcher count changes
    # - New issues since last report
    # - CI status change (was passing, now failing — or vice versa)
    # - New release since last report
    # - README changes (if tracked)
}
```

Include a "Since last report" section showing what improved, what regressed, and what stayed the same.

---

## Anti-patterns

| Anti-pattern | Why it fails |
|-------------|-------------|
| **Fixing during scan** | Closing an issue might be right; closing it without context might be wrong. Report only. |
| **Ignoring rate limits** | GitHub API has a 5000 req/hr limit for authenticated users. At ~12 API calls per repo, 42 repos = 504 calls. Fine for a single scan, but running back-to-back will hit the limit. |
| **Not saving the report** | The user needs to act on findings. Write the report to a file or show it in a way they can reference later. |
| **Checking every repo every time** | Focus on repos that change frequently. Repos with no commits in 6 months don't need weekly scans. |
