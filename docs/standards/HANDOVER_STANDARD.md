---
title: "Repo Handover Standard"
category: standard
status: active
audience: all
skill_candidate: false
related:
  - AGENT_PROTOCOLS.md
  - AGENTS.md
  - FRONTMATTER_STANDARD.md
last_updated: 2026-08-30
---

# Repo Handover Standard

**Version:** 1.0
**Status:** Active
**Applies to:** Every active repo in `D:\Dev\repos\` that more than one agent/tool touches
  (Claude, opencode on local ds4, Antigravity, or Sandra directly).

---

## Purpose

Sandra works across multiple agent runtimes on the same repo in the same day: Claude
(this chat, with MCP tool access), opencode running against the local DS4/DeepSeek V4
Flash model, and Antigravity (the memops/adn_system fleet). None of these share session
memory with each other. Without a common handoff point, every agent switch means Sandra
re-explains current state from scratch.

**`HANDOVER.md` is that common handoff point.** It answers exactly one question for
whichever agent opens the repo next: *"What do I need to know to keep going without
asking Sandra to repeat herself?"*

This is deliberately narrow. It is **not**:

| Not this | That's... |
|---|---|
| A backlog of future work | `TODO.md` |
| A dated log of shipped changes | `CHANGELOG.md` |
| A narrative status report with addenda | `STATUS.md` (see mcp-central-docs/STATUS.md - useful, but grows forever and mixes history with current state) |
| Fleet-wide plans | `mcp-central-docs/projects/*.md` |

`HANDOVER.md` holds **only current, live, mid-task state**. It gets fully overwritten,
never appended to (this is the opposite of the `STATUS.md` addendum pattern, which is
fine for a narrative log but wrong for a handoff spot - nobody wants to read six months
of history to find out what's happening right now).

---

## Location

- **Canonical copy:** `{repo}/HANDOVER.md` at repo root, git-tracked, plain markdown.
  Plain markdown is mandatory - no MCP tool-call syntax, no memory-system references,
  nothing that only Claude can read. opencode and Antigravity read repo files directly;
  they do not have Claude's memory tools.
- **Mirrored copy:** `mcp-central-docs/projects/{repo}/HANDOVER.md`, synced the same way
  README.md/TODO.md/CHANGELOG.md/docs_*.md already are (see `metadata_sync.json` per
  project). This lets an agent starting cold in mcd discover which repos have live
  in-progress work without opening every repo individually.

## Schema

```yaml
---
updated: 2026-08-30T14:00:00+02:00      # required, ISO 8601 with offset (Vienna = +02:00 / +01:00)
agent: claude                            # required - claude | opencode-ds4 | antigravity | sandra
status: in-progress                      # required - see Statuses below
tags: [repo-name, technology, priority]  # required - same tagging discipline as basic-memory notes
---
```

### Statuses

| Value | Meaning |
|---|---|
| `in-progress` | Actively being worked, mid-task |
| `blocked` | Stalled on something external (waiting on Sandra, a credential, an upstream fix) |
| `ready-for-review` | Agent believes it's done; needs Sandra's eyes before merge/ship |
| `stale` | Nobody has picked this up in a while - see Staleness rule below |

### Body (fixed sections, always present, keep it short)

```markdown
## What's happening right now
One to three sentences, present tense. Not a changelog entry - what is the actual
current state of the work.

## Last concrete action
What was actually done last (file paths, commands run, commits). Specific enough that
the next agent can verify it happened rather than take it on faith.

## Next step
ONE thing. The single most important next action. Not a list - if there are five
things, TODO.md is where the other four live. This field answers "what do I do first."

## Blockers
What's stopping progress, or "None."

## Context the next agent needs
Decisions made and why, gotchas, things that look wrong but aren't. Link to STATUS.md
or CHANGELOG.md for full detail rather than duplicating it here - this section is for
what would cause a wrong turn if omitted, not a full history.
```

---

## Staleness rule

If `updated:` is more than **3 days** old when an agent opens `HANDOVER.md`, treat its
contents with suspicion. Verify against actual repo state (`git log`, `TODO.md`,
current file contents) before acting on it - do not assume it still reflects reality.
Stale handovers that get trusted blindly are worse than no handover at all.

(This is not a hypothetical: `mcp-central-docs/NEXT.md` currently says "Current Plans -
June 2026" while being read in August. That is exactly the failure mode this rule
guards against - undated or stale-and-unflagged state gets treated as current by an
agent with no way to tell the difference.)

## Overwrite discipline

Every agent that finishes a work session touching a repo overwrites `HANDOVER.md` in
full before ending the session. Before overwriting, ask: does anything in the current
file need to survive?
- A durable decision or gotcha → fold into `STATUS.md` or a comment in code, not into
  the next `HANDOVER.md`.
- A shipped, verified change → belongs in `CHANGELOG.md`, not here.
- Anything else → let it go. `HANDOVER.md` is a snapshot, not an archive.

## Agent-agnostic requirement

This is the actual point of the standard, so it's worth stating directly: any agent
that can read a text file in the repo root must be able to use `HANDOVER.md` with zero
additional tooling. No MCP calls, no memory-system syntax, no assumed context from a
prior Claude conversation. If a section only makes sense to one agent runtime, it
doesn't belong in `HANDOVER.md` - put it in that runtime's own state instead.

## Rollout

See `mcp-central-docs/projects/HANDOVER_ROLLOUT_PLAN_2026-08.md` for the propagation
plan (sync-script wiring, fleet-wide seeding, staleness check). `arxiv-mcp` is the
pilot repo - see `D:\Dev\repos\arxiv-mcp\HANDOVER.md` for a real instance.

**Scope decision (2026-08-30):** for now, `HANDOVER.md` is a plain repo-root file only
- written and read directly by whichever agent (Claude, opencode-ds4, Antigravity, or
Sandra) is actively working the repo. No hub-board submission, no Discord posting, no
automated wiring of any kind. The SFB/hub-board dispatch idea in
`HANDOVER_DISCORD_DISPATCH_2026-08.md` is a real design, not abandoned, but explicitly
deferred - don't build it unless/until that file's status changes from draft.

**Amendment (2026-10-02):** one-way, informational *work reports* to Discord `#sfb-work`
are now permitted under `WORK_REPORT_STANDARD.md` (Sandra reads Discord; all agents use the
same format). This does not lift the deferral above: dispatching plans to other agents
still goes through the hub board, not Discord.
