---
title: "Release Discipline — Fleet Standard"
category: standard
status: active
audience: mcp-dev
last_updated: 2026-09-30
---

# Release Discipline — Fleet Standard

The fleet's GitHub org is a storefront, not a workshop. Strangers install
from public HEAD; what they get must work. This doc owns the *when* and
*how-good* of shipping. The *what* lives in `RELEASE_TIERS.md` (T1/T2/T3),
the *mechanics* in `PACKAGING_STANDARDS.md`.

## 1. The three audiences (know who you break)

| Level | Who | Installs via | Freshness contract |
|---|---|---|---|
| L1 | Fellow devs, contributors | `git clone` + `start.ps1` | HEAD builds. Dirty trees and experiments are visible; that is fine, breakage is not. |
| L2 | Technical users (Claude Desktop, opencode) | `.mcpb` bundle, tagged releases | Tagged releases install and run. HEAD should too, but tags are the promise. |
| L3 | Non-technical end users | NSIS installer, one download | Only ever sees tested major releases. Never sees HEAD, never sees a dirty tree. |

Every rule below exists to keep these three contracts unbroken, in that
priority order. L3 must never pay for L1's velocity.

## 2. The core asymmetry (the whole doc in two lines)

- Small feature, refactor, cleanup: **batch it**. No release, no tag, no announcement. Push to HEAD when green and move on.
- Showstopper fix (broken install, broken launch, broken HEAD): **ships immediately**. Not with the next batch, not tomorrow. Now.

Sitting on a known showstopper fix while public HEAD stays broken is the
single worst state a repo can be in: every new visitor's first experience is
failure, and each one costs more trust than any feature earns back.

## 3. Showstopper rule (HARD)

> A known-broken public install outranks all other work. Drop everything,
> fix, verify on a clean path, push, tag if L2/L3 are affected. A fix that
> exists only in your working tree fixes nothing.

- "Broken" means: fresh clone does not install, `start.ps1` does not launch,
  the backend does not answer `/health`, the tagged `.mcpb` does not load,
  the NSIS installer does not complete. If a stranger cannot get running in
  the documented steps, it is a showstopper regardless of how small the code
  defect is.
- Verify the fix the way the stranger does it (clean clone / fresh install /
  naked-PC path per `NAKED_PC_INSTALL_STANDARD.md`), not the way your dev
  box does it. Your box has caches, env vars, and scar tissue the stranger
  lacks.
- After pushing, confirm the remote actually has it (`git status` clean AND
  `git log origin` shows the commit). A fix that never reached the remote is
  the same as no fix. This bit us before — see TRAPS_AND_PITFALLS.md #39-adjacent
  "verify, don't assume" family.

## 4. Commit/push discipline

- Push promptly when green. Small, working increments beat heroic branches.
  A week's unpushed work is a week's unrecoverable risk (disk, greenscreen,
  forgetfulness).
- Max 10 files per commit; 3+ file edits get timestamped `.bak` first.
  Unrelated changes do not ride along in one commit — future-you bisecting a
  regression will thank present-you.
- Conventional messages (`fix(...)`, `feat(...)`, `docs(...)`, `chore(...)`)
  so changelogs and release notes write themselves.
- Never leave the tree dirty at end of session in a shared repo: finish and
  commit, or revert. Someone else's morning starts from your evening's tree.
- Never commit secrets, tokens, `.env`, or OAuth caches (`data/token.json`,
  `oauth_client.json`). Ever. No exceptions, no "I'll remove it later."

## 5. Release checklist (per tier, at tag time)

Run this when cutting any L2/L3-visible release. L1-only pushes need only
section 4.

- [ ] **Install from scratch works**: clean clone (or fresh download), documented steps only, no tribal knowledge. For T3: naked-PC validation per `NAKED_INSTALL_TESTING.md`.
- [ ] **Launch works**: `start.ps1` brings up backend + frontend, `/health` 200s, no instacrash. (The 2026-09-28 `-NoNewWindow`/`-WindowStyle` episode is what happens when nobody runs the launcher before release.)
- [ ] **README lies about nothing**: screenshots match the current UI, install steps match the current scripts, port numbers match the registry, badges/versions are current.
- [ ] **INSTALL.md works**: a stranger following it verbatim ends up running. If it references files, flags, or steps that no longer exist, it is a showstopper (section 3).
- [ ] **Help pages current**: in-webapp Help/Onboarding reflects current behavior and current external consoles (see `patterns/GOOGLE_API_AUTH_SURVIVAL.md` §0: console UX rots quarterly).
- [ ] **`llms.txt` / `llms-full.txt` current**: tool lists match the registered tools. Stale tool lists teach every connected agent to hallucinate.
- [ ] **T3 extras**: `BUILD_LOG.md` entry for this build, CUA smoke test green (`just cua-nsis-test`), NSIS built from a clean tree, installer hash/size sanity-checked.

## 6. Stale-asset ownership

Staleness has no owner by default, so it accrues forever. Assign it:

- Every repo's release checklist run (section 5) refreshes README/INSTALL/screenshots/help as part of the release, not as a separate chore that never gets scheduled.
- `assfix` runs verify doc currency against behavior (README claims vs actual ports/tools/pages) and file drift findings when they diverge — docs that describe a different repo than the code are MEDIUM findings, not cosmetic notes.
- Screenshots older than one UI redesign are worse than no screenshots. Delete rather than display the past.

## 7. Automation hooks (so discipline is not willpower)

- `just gates green` (or equivalent) before every push that touches behavior — lint, typecheck, tests. Red does not ship, not even "just this once."
- Pre-commit hooks stay green and un-bypassed. `--no-verify` is forbidden except to escape a provably-broken hook, and then the hook gets fixed the same day.
- Scheduled rebuilds for containerized repos per `docker-containerization.md` § Image Freshness: weekly cached, monthly `--no-cache`, green-only.
- Morning digest / fleet-status surfaces dirty trees and stale PRs daily — read it; a repo that has been dirty for a week is a showstopper incubator.

## Related

- `RELEASE_TIERS.md` — what to ship per tier, build frequency (MCPB per push, NSIS on tags)
- `PACKAGING_STANDARDS.md` / `MCPB_PACKAGING_STANDARDS.md` — bundle mechanics
- `NAKED_PC_INSTALL_STANDARD.md` / `NAKED_INSTALL_TESTING.md` — the stranger's install path
- `patterns/repo-assess-and-fix.md` Phase 6 — verify-and-push gate
- `patterns/GOOGLE_API_AUTH_SURVIVAL.md` — why external-facing docs rot and how to fight it
