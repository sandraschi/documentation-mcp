# Handover Standard — Rollout Plan

**Date:** 2026-08-30
**For:** opencode (local ds4) or Antigravity — pick up from Phase 2
**Depends on:** `mcp-central-docs/standards/HANDOVER_STANDARD.md` (read this first, it's short)

## Why this exists

Sandra switches between Claude, opencode-on-ds4, and Antigravity on the same repos in
the same day. None of them share session memory. `HANDOVER.md` is the agreed common
handoff spot — see the standard doc for the schema and rules. This plan is just the
propagation work: get it out of one pilot repo and into the fleet, wired into existing
sync/gate infrastructure rather than bolted on separately.

## Phase 0 + 1 — DONE (by Claude, 2026-08-30)

- [x] `mcp-central-docs/standards/HANDOVER_STANDARD.md` — the standard itself
- [x] `mcp-central-docs/templates/HANDOVER.md` — drop-in template
- [x] `D:\Dev\repos\arxiv-mcp\HANDOVER.md` — real pilot instance (live in-progress state,
      not a placeholder — read it as the reference example of what "good" looks like)

Nothing further needed here unless the schema itself needs revision after Phase 2-3
surface problems with it in practice.

## Phase 2 — Wire into the existing project sync

`mcp-central-docs/projects/{repo}/` already mirrors each repo's README.md, TODO.md,
CHANGELOG.md, INSTALL.md, and `docs/*.md` (flattened to `docs_*.md`) — see
`mcp-central-docs/projects/arxiv-mcp/metadata_sync.json` for the per-project sync
record (`last_sync`, `github_url`, `id`, `path`). Locate whatever script performs this
sync (likely under `mcp-central-docs/scripts/` or a `justfile` recipe — check
`justfile` and `scripts/` first) and extend it to also copy `{repo}/HANDOVER.md` →
`mcp-central-docs/projects/{id}/HANDOVER.md` on the same cadence as the other synced
docs. If `HANDOVER.md` doesn't exist in the source repo yet, skip it silently (Phase 3
will seed it) rather than erroring the whole sync run.

**Acceptance:** run the sync for `arxiv-mcp` and confirm
`mcp-central-docs/projects/arxiv-mcp/HANDOVER.md` appears and matches the repo-root copy.

## Phase 3 — Fleet-wide seeding

Do **not** seed all ~335 directories under `mcp-central-docs/projects/` — most of those
are scaffolds, archived, or dead (see `_archives/`, `_junk/`, `backups/`, `quarantine/`
siblings in that same listing). Scope to repos under `D:\Dev\repos\` with real recent
activity — e.g. a git commit or file modification in the last 30 days is a reasonable
filter, but sanity-check against `mcp-central-docs/projects/FLEET_INDEX.md` and
`ACTIVE_PROJECTS_UPDATE_TABLE.md` since those already track what's actually alive.

For each qualifying repo missing `HANDOVER.md`:
1. Copy `templates/HANDOVER.md` to `{repo}/HANDOVER.md`.
2. Fill `tags:` from the repo name (matches the `[repo-name, technology, priority]`
   convention already used in Sandra's basic-memory notes).
3. Set `agent: sandra`, `status: in-progress` as the honest default (an empty
   `HANDOVER.md` with no real content is worse than none — flag these for Sandra to
   fill in on next touch rather than pretending they're populated).
4. Do not overwrite an existing `HANDOVER.md` — Phase 1's arxiv-mcp instance and any
   repo an agent has already touched under the new standard must survive re-runs.

**Acceptance:** a dry-run listing of which repos would get a new `HANDOVER.md`, shown to
Sandra for a sanity check, before actually writing 50+ files across the fleet.

## Phase 4 — Staleness gate (stretch, do after 2-3 land and stick)

`gitops:fleet_ops` already has a `docs_gate` operation and a `full_suite` that bundles
checks — see `QUALITY_GATES.md` in `standards/` for how the existing gates are framed.
Add a `HANDOVER.md` check to that same family rather than inventing a parallel
mechanism: flag any active repo where `HANDOVER.md` is missing, or where `updated:` is
more than 3 days old *and* `status: in-progress` (a `status: ready-for-review` or
`blocked` file sitting for a while isn't necessarily a problem — an `in-progress` one
going stale usually means it was silently abandoned mid-task, which is exactly the
failure mode the whole standard exists to catch).

**Acceptance:** `fleet_ops(operation="docs_gate")` output includes a handover-staleness
section alongside whatever it already reports.

## Related: Discord/SFB dispatch idea

Sandra's proposal to route Fable-authored plans through the SFB hub board / Discord
mirror (rather than posting directly to Discord) is written up separately —
`HANDOVER_DISCORD_DISPATCH_2026-08.md`. It depends on this standard for its durability
fallback (a plan submitted while the fleet-hub is mid-restart still survives in
`HANDOVER.md` even if the hub-board submission or Discord mirror is delayed). Read it
before wiring anything Discord-related into the fleet-agent-mcp side of this rollout.

## Non-goals

- Not replacing `STATUS.md` or `TODO.md` — those keep their existing jobs, see the
  standard doc's comparison table.
- Not retrofitting every dormant/archived project dir — see scoping note in Phase 3.
- Not adding this to onboarding flow (`ONBOARDING_STANDARD.md`) — that's about
  wrappee/account setup for end users, unrelated to agent-to-agent handoff.
