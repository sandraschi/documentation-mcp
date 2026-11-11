# Fleet intake sweep (SOP)

Roll `templates/github-hygiene/` v2 (issue forms, PR template) plus the
calibre-style intake package (README Bugs router, CONTRIBUTING hub doc) out
to every fleet repo that lacks it. Pilot: 4 merged PRs (canonical
mcp-central-docs#6, searchstudio-mcp#3, git-github-mcp#5, mcp-central-docs#7).

## Status quo (measured 2026-10-25)

- ~319 own dirs, 23 with issue templates, 18 with a PR template, 59 with CONTRIBUTING — filesystem count, UNDERCOUNTS (repos without a local clone are invisible; wave 1 proved it with calibremcp).
- Storytold upstream checkouts have none either (only dependabot/actionlint/FUNDING) — no gap to close there, nothing to copy.
- Wave 1 (2026-10-25): 7 PRs opened (aiwatcher, ai-games, arr-mcp, avatar, deepfang, arxiv, email) + 3 correct skips (advanced-memory dirty tree; calibremcp already has forms; devices-mcp legacy .md = upgrade track).

## Package per repo (one commit, one PR each — never bundled across repos)

1. `.github/ISSUE_TEMPLATE/bug_report.yml` — adapted repro artifact + env (see ADAPT markers).
2. `.github/ISSUE_TEMPLATE/feature_request.yml` — adapted use-case placeholder.
3. `.github/ISSUE_TEMPLATE/config.yml` — slug replaced (4 places).
4. `.github/PULL_REQUEST_TEMPLATE.md` — gates adapted (pytest/ruff; biome/tsc only if a webapp exists; docs repos use their defined gate).
5. `README.md` — `## Bugs` router section before License (calibre-style; relative `../../issues` links).
6. `CONTRIBUTING.md` — only if missing; adapted hub doc pointing at the templates + repo hard rules. Never overwrite an existing one.

Step 0 per repo: enable GitHub Discussions via API (reversible one-liner) so the router's Q&A link resolves. Verify with `discussion_categories`.

## Batching (waves, not a flood)

- Waves of 10 repos: one tracking checklist, one PR per repo (bot-authored, uniform message, `intake-sweep` label). Maintainer merges per wave — never auto-merge, never batch repos into one PR (one concern per PR cuts both ways: one repo per PR keeps reverts clean).
- Order: active repos first (open PRs/issues), then alphabetical. `_archives/` frozen repos excluded. `_upstream/` third-party clones excluded (read-only).
- Enumerate from the GitHub API (`users/sandraschi/repos`, paginated), never from the local filesystem: repos without a local clone are invisible to a directory scan (wave 1 missed calibremcp this way).
- Skip + list (do not force): repo with an open intake PR, repo whose README has no License anchor (flag for human placement), dirty local tree (someone's WIP — hands off per the ownership rule).
- Legacy intake is UPGRADE, not done: markdown-form `.md` issue templates or a lowercase-only PR template get the full v2 package like any missing repo (wave 1: devices-mcp). A repo only counts as done when it has yml forms + router + CONTRIBUTING.

## Verification per repo (gates, not eyeballs)

- `yamllint` clean on all three yml files (relaxed, max line length 160).
- Required markers present: reproducer required, version required, private-data checkbox, tiny-fix rule, pre-approval checkbox.
- Contact links resolve: Discussions enabled (API check), advisory link present.
- No secrets in any added file; `.bak` files from adaptation removed before commit.
- 5-files-per-commit cap holds trivially (4 new + README edit, or + CONTRIBUTING = 6 → split README router into the same commit only if it fits; otherwise two commits).

## Tracking (one issue, not 290)

One tracking issue in mcp-central-docs (`intake-sweep` label): wave checklist with per-repo checkboxes, pilot evidence linked, skip-list with reasons. Waves close checkboxes, never open per-repo issues — the per-repo PR *is* the unit of work. Assfix-style per-issue minting does NOT apply here (that rule is for deferred findings, not rollout checklists).

## Rollout vehicle

Fritz cron, one wave per run, weekly until done. Each run: pick next 10 unscanned repos from the tracking issue, apply package, open 10 PRs, update checklist, append session-log entry. Stop conditions: tracking issue complete, or maintainer `intake-sweep-pause` label on the tracking issue (kill switch). First wave is manual (this SOP's proof run); cron takes over from wave 2.

## Done looks like

Every non-excluded fleet repo has working issue forms (verified: open the New-issue page, all three options render), a PR template, a Bugs router, and a CONTRIBUTING hub — or a recorded reason why not.
