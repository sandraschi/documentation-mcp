---
title: "GitHub Hygiene - Issues, PRs, and Contributing for Our Own Repos"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-10-25
---

# GitHub Hygiene Standards

**Scope**: how *our own* fleet repos receive issues and PRs. For how we behave
in *other people's* projects, see `rules/open_source_contributing.md`.

## Why

Inbound attention is arriving (fleet getting noticed, direct user mail). Mail
does not scale, is not searchable, and hides context. Every public fleet repo
must offer structured, low-friction GitHub intake so a stranger's report
becomes a trackable issue with a reproducer attached.

## Required per public repo

1. **Issue forms** (`.github/ISSUE_TEMPLATE/`): `bug_report.yml` + `feature_request.yml`
   (+ `config.yml` with `blank_issues_enabled: true`). Forms, not markdown —
   required fields beat polite requests. The bug form MUST demand a
   reproducer (patch file, query, book, log — whatever makes the report
   replayable in your repo) and version info (repo version/commit + host-app
   version where a wrappee exists).
2. **PR template** (`.github/pull_request_template.md`): linked issue,
   small focused diff, tests, lint, changelog update, maintainer merges.
3. **Contributing guide** (`CONTRIBUTING.md` at root — GitHub surfaces it
   natively; dev-setup detail stays in `docs/DEVELOPMENT.md` per
   `README_STRUCTURE.md`): issues-first, one issue per request, no stubs,
   no GUI automation where banned, repo-specific verification rules
   (e.g. no catalog entries from memory).

## Adopt from the kit

Canonical templates: `templates/github-hygiene/` (with `ADAPT:` markers —
invisible comments showing what to repo-ify). 15-minute operation per repo:
copy `.github/` + `CONTRIBUTING.md`, adapt markers, validate YAML, commit.
Reference implementations: `vcv-rack-mcp` (greenfield), `calibre-mcp`
(migration from legacy `.md` templates — delete the `.md` files, GitHub
shows both otherwise).

## Bot-minted issues (assfix)

Human intake above stays. This section covers issues minted by assfix itself
for deferred findings, so a second human (now: Steve) and issuebot can trust
them without re-reading the full report.

- **When to mint.** Every finding listed as deferred in the assess report must
  exist as 1+ GitHub issues before Phase 6 closes. No deferred-without-URL.
  Easy fixes stay direct commits; only deferreds become issues.
- **Tagging (machine + human readable).** Label `assfix` on every bot-minted
  issue, alongside `bug` / `enhancement` (do not replace them). First body line
  is the fixed banner:
  `> Issue made by assfix on YYYY-MM-DD - SOTA NN/100 - report
  docs/assess-reports/YYYY-MM-DD.md @ <sha>.`
  Last body line is `Assfix deferred reason: <why not fixed now>.`
- **Same hygiene as humans.** One issue, one request. Reproducer + version
  mandatory (file:line at pinned commit, failing gate output, score impact).
  Pin the commit the finding was verified against (`at <sha>`), as in
  `searchstudio-mcp#1`.
- **Dedup before mint.** `issue_list` open + title substring search first.
  Comment on the existing issue instead of opening a duplicate.
- **Cap.** Max 3 new assfix-issues per repo per run. A 60-score runt has more
  than 3 problems; the rest wait for the next run. Cron mode without a cap
  spams the tracker.
- **Ready for issuebot.** Add label `ready` only when the fix is bot-safe
  (small, test-covered, no judgment call). Issuebot ignores `assfix` without
  `ready`. Bot-unsafe deferrals stay `assfix`-only for a human.
- **Template.** Canonical body in `templates/github-hygiene/ASSFIX_ISSUE_TEMPLATE.md`.
  Bot issues bypass the yml forms (`blank_issues_enabled: true` covers them)
  but MUST carry the same required fields as text.
- **Label reservation.** The `assfix` label is reserved for bot-minted issues:
  never apply it to a human-written issue, never remove it from a bot-minted
  one. Absence of the label means human-written — that is how the two are told
  apart. Triage treats labeled issues as bot-sourced context (already
  structured; classify, do not re-ask for a reproducer).

## Policy notes

- **One issue, one request.** Enforce by closing multi-request issues with a
  pointer to split them — in the form text, not just in CONTRIBUTING.
- **No contact links** in `config.yml` unless the channel exists AND is
  monitored. Never link email — the point is to move intake OFF mail.
- **Labels**: keep GitHub defaults (`bug`, `enhancement`) unless the repo
  has a triage workflow that needs more.
- **Maintainer merges.** Contributors do not merge their own PRs.
- Private/experimental repos: exempt until public. On going public, hygiene
  kit is part of the launch checklist.
