---
title: "GitHub triage standard (PRs, issues, Dependabot)"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-10-13
---
# GitHub triage standard

**Version:** 1.0 (2026-10-13). **Owner:** Sandra. Applies to every agent
(Claude, Cursor, opencode, Antigravity) acting on `sandraschi` repositories.

## Why

The fleet is being found. By 2026-10-13: 10 open PRs from 8 outside
contributors, some waiting since July, buried under 84 Dependabot PRs.
Contributors who wait two months do not send a second PR. Streamline: fast,
consistent, mostly automatic, with Sandra seeing only what needs her.

## Policy

| Incoming | Action | Who decides |
|---|---|---|
| PR or issue written by an AI | Judge on merit, never on authorship. Welcome. | - |
| Spam, solicitation, marketplace listings, "join our X", SEO links | Close, reason "not planned", one neutral line | agent, no asking |
| Trivial issue: typo, formatting, wrong name/URL, "I can't understand X" in the docs | Make the mini edit, commit with `fixes #N`, push, comment with the commit hash, close | agent, no asking |
| Issue already fixed (e.g. by assfix) but still open | Verify the fix, comment with the commit, close | agent, no asking |
| Easy PR: docs, links, typos, packaging metadata; CI green or CI irrelevant; no behaviour change | Review the diff, merge, thank the contributor | agent |
| Difficult PR: code behaviour, new features, security-relevant, large diffs, unclear intent | Review, run tests in a worktree, write a recommendation; SHOW Sandra; never merge alone | Sandra |
| Real bug or feature request | Label, reproduce if cheap, put on the dashboard; answer within days | Sandra / agent |
| Anti-AI rant | Draft a biting, factual reply and SHOW Sandra; never post unreviewed. No quarter to Butlerites. | Sandra |
| Finished discussion (question answered, decision recorded) | Thank and close | agent, after a last-comment check |

Tone: short, specific, friendly to contributors; reference commits. Never
argue in a contributor's PR; propose changes or explain the decision.

## Close what you fix

Any agent that fixes something reported in an issue (assfix included) closes
that issue in the same session: `fixes #N` in the commit message on the default
branch, plus a comment naming the commit. (2026-10-13: system-admin-mcp#1 was
fixed 2026-10-09 and left open four days.)

## Dependabot

Managed by `scripts/set_fleet_dependabot.py` (max 10 repos per invocation):
weekly, Monday 05:00 Europe/Vienna, at most 3 open PRs per ecosystem,
version updates grouped into one PR per ecosystem and directory, security
updates grouped separately. Only for repos whose `origin` is `sandraschi/...`
and that are not forks of another project (forks: disable Dependabot in the
repo settings instead). Bot PRs: merge when CI is green, weekly, in one pass.

## Visibility

The daily dashboard (`operations/daily/index.html`, see
WIP_COMMIT_STANDARD.md) ranks human PRs first, then held-back files, sweep
failures, fresh CI failures; Dependabot PRs appear grouped per repo as fyi.
