---
title: "Handover via SFB Discord Dispatch"
category: project
status: draft
audience: internal
skill_candidate: false
related:
  - HANDOVER_STANDARD.md
  - HANDOVER_ROLLOUT_PLAN_2026-08.md
last_updated: 2026-08-30
---

# Handover via SFB Discord Dispatch

**Idea (Sandra, 2026-08-30):** use the existing SFB Discord server as the venue for
getting a Fable-authored plan in front of a "lesser" execution agent (opencode on
ds4, Antigravity) — Fable makes the plan under Claude Desktop's Fable usage quota,
the plan goes into Discord, a running supervisor agent reads it and dispatches.

**Status: deferred, 2026-08-30.** Sandra scoped the handover work down to plain
repo-root `HANDOVER.md` files for now (see `HANDOVER_STANDARD.md` § Rollout). This
design stays written up for when the hub-restart reliability issue is addressed and
there's appetite to wire it up — nothing below should be built until then.

## Reuse, don't reinvent

Fritz (fleet-agent-mcp) already has exactly this machinery:

- **Hub board is source of truth**, SFB Discord (guild "Sandra's Fleet HQ", channels
  `#sfb-work` / `#sfb-thoughts` / `#sfb-alerts`) is a **sanitized best-effort mirror**
  — not the other way round.
- **v0.2.3** (shipped 2026-08-29) already does `[agent]`-attributed posting and
  involuntary lifecycle events: workflow start/completed → `#sfb-work`, BLOCKED →
  `#sfb-alerts`.
- **ds4 local brain tier** is already on Fritz's own 2026H2 improvement plan
  (`docs/improvement-plan-2026h2.md`) — the "lesser agent" execution tier this idea
  wants already has a name and a roadmap slot.
- There's a **standing requirement** that fleet agents be surveilable through their
  comms, specifically because ad hoc agent-invented message channels were a past
  problem. A plan posted straight into Discord by Fable, bypassing the hub board,
  recreates exactly that anti-pattern.

**So: Fable's plan should go into the hub board as a new workflow (tagged `[fable]`
via the existing attribution mechanism, targeted at the `ds4` tier), not straight into
a Discord channel.** The already-shipped lifecycle posting then mirrors it to
`#sfb-work` for free — no new posting code needed for that hop.

## The reliability gap is real, not hypothetical

Two independent signals, both from today:

1. `fritz-agent.md`'s own known-open-issue list: **fleet-hub restarting every ~20
   minutes.**
2. Live in this session: `discord-mcp:message_watcher_status_tool` timed out after 4
   minutes with no response — the watcher itself was unreachable when checked.

A plan that only exists as a Discord message posted while the supervisor happens to
be up is a plan that can silently vanish into scrollback. "Hopefully running" is the
correct level of trust for this today, and the design has to route around that, not
paper over it.

## Where `HANDOVER.md` comes in

The fix is the same durability argument as the fleet-agent HANDOVER standard itself:
**the plan needs a copy that doesn't depend on the hub or Discord being up.**

Concretely: whatever entrypoint Fable uses to submit the plan to the hub board should
*also* write/update `HANDOVER.md` in the target repo — `status: in-progress`,
`agent: fable`, the plan itself in **Next step** / **Context the next agent needs**.
That gives three independent paths to the same plan surviving a ~20-minute restart
window:

- Supervisor is up when Fable submits → picks it off the hub board immediately, normal
  path, Discord mirror fires as a bonus visibility signal.
- Supervisor is down/restarting at submit time, comes back later → hub board still has
  the queued workflow (source of truth persists across restarts, that's the whole point
  of it being source of truth) — no loss, just delay.
- Something is wrong with the hub board itself → `opencode-ds4` or any agent opening
  the repo directly still finds the plan in `HANDOVER.md`, with zero dependency on
  Discord, the hub, or any of fleet-agent-mcp being reachable at all.

## What this is *not* asking for

Not proposing a new Discord bot, webhook, or channel. `#sfb-work` already does the job
once the plan goes through the hub board instead of around it. Not proposing changes
to the attribution or lifecycle-posting mechanism — `[fable]` is just a new value for
an already-existing tag.

## Open dependency

The ~20-minute hub-restart issue is a prerequisite worth fixing on its own merits, not
just for this idea — it undermines "hub board is source of truth" generally, not only
the Fable-dispatch case. Flagging it here as a blocker to *trusting* this flow, but the
`HANDOVER.md` fallback above means the idea is usable even before that's fixed, just
with "supervisor may pick this up late" as an accepted risk instead of "may never see
it."
