# Fleet mergebot (spec)

Automated merging for Sandra's lazy days. The governing principle: **refusal
is the default; merging is the exception that must earn itself every run.**
No LLM anywhere in the merge path — deterministic policy only. A wrong merge
ships unreviewed code to a default branch; a wrong refusal costs nothing.

## What he refuses, unconditionally

- Failing or missing checks (where CI exists — most private fleet repos have
  none, which is why Tier 1 is restricted to verifiable diffs, see below).
- Merge conflicts, requested-changes reviews, unresolved threads,
  `do-not-merge`-style labels, draft PRs.
- PRs from strangers. PRs touching workflows, secrets, ports, submodules.
- Anything outside the explicit per-run scope. Anything when the kill switch
  is set.

## Trust tiers

- **Tier 1 (auto-mergeable):** bot-authored hygiene PRs with a fingerprint
  match — known branch prefix (`fix/github-intake-templates`,
  `intake-sweep` label), diff confined to an allowlisted path set
  (`.github/`, `CONTRIBUTING.md`, README router section), small diff, checks
  green where checks exist, branch up to date with base, open >= 24h (cooling
  period so a human could have objected), zero review comments.
- **Tier 2 (never auto):** everything with code in it, everything from humans
  including Steve, everything large. These get a merge-readiness report,
  never a merge. Lazy days do not extend to code.

Tier 1 verification is cheap precisely because Tier 1 diffs are constrained:
re-list files, assert the path allowlist, yamllint the forms, assert required
markers, confirm mergeable state via API. Code PRs would need full per-repo
gate runs — a different, much slower machine, explicitly out of scope for v1.

## Triggering

- **Manual first:** `mergebot --repos a,b,c` or `--prs owner/repo#N`, or
  `--label intake-sweep` bounded to named repos. Never blanket "all open PRs".
- **Dry run is the default and always comes first.** Two-phase with plan-hash
  binding: `--dry-run` writes the plan (which PRs, why each qualifies,
  verification output per PR); `--execute --plan <hash>` re-verifies
  everything at execution time (still mergeable? no new commits or comments
  since the plan?) and aborts the whole run on any drift. No TOCTOU merges.
- **Cron later, bounded:** Fritz cron only after manual trust is earned —
  Tier 1 only, max 3 merges per run, business-hours only so a bad merge is
  noticed the same day, kill-switch label aborts silently (no writes at all).

## Brakes

- Explicit per-run scope, always. Max 3 merges per run to start.
- Cooling period: nothing merges before 24h open, no exceptions.
- Per-repo opt-out; global kill-switch label; audit trail of every merge
  AND every refusal (with reasons) into `operations/session-log/`.
- `--merge` (merge commits, like the manual flow), delete branch after merge.

## What he will not do, ever

Force-push. Rebase or resolve conflicts (conflicted = refused, human rebase).
Merge red checks. Merge strangers. Merge workflows. Learn from data (no model,
no thresholds tuned on outcomes — tiers are declared, not discovered).

## Rollout

1. Spec (this file) reviewed and merged.
2. Build as a `github_ops` mode in git-github-mcp (`mergebot_plan` /
   `mergebot_execute`), reusing the gh plumbing and the red-shelf confirm
   pattern. Manual CLI use against Tier-1 intake PRs, dry-run first.
3. Graduate the best-behaved batch type to cron. Code stays human-merged
   until fleet CI exists — a separate project, not a mergebot feature.

## Pointers

- Human intake: `standards/GITHUB_HYGIENE_STANDARDS.md`
- Bot-minted issues: same file, "Bot-minted issues (assfix)" section
- Inbound triage: `standards/INBOUND_TRIAGE.md`
- WIP ownership when the bot surfaces stale work: `patterns/AGENT_BRANCH_DISCIPLINE.md` item 5
- Sweep vehicle this bot will eventually drive: `patterns/fleet-intake-sweep.md`
