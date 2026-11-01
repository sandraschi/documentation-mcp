---
name: wrappee-drift
description: Read-only, single-repo audit of a repo's tool coverage against the software it wraps (its current real API/docs, not training-data memory) and against comparable/competing wrappers. Trigger when the user says "wrappee drift" followed by a repo name, "capability audit" followed by a repo name, or asks whether a repo is missing features the wrapped software or a competitor now has. Always scoped to one named repo per invocation -- never trigger this fleet-wide or unprompted; that is explicitly against the SOP. Do NOT trigger for internal fleet-standard compliance (that is drift-scan) or strategic worth/archive decisions (that is quality-check) -- this is specifically about the gap between the repo's tool list and the wrapped software's/competitors' actual current capabilities.
---

# wrappee drift

Single-repo, read-only capability-gap audit. Answers "has the software we wrap moved,
or has a competing wrapper covered ground we haven't, since this repo's tool list was
last touched" -- a question `drift-scan` never asks, because passing every internal
fleet-standard check says nothing about whether the wrapped software itself moved.

## Canonical procedure

The authoritative SOP is:

    D:\Dev\repos\mcp-central-docs\patterns\WRAPPEE_CAPABILITY_DRIFT_SOP.md

Read that file first and follow its four phases. Do not reconstruct the checks from
memory and do not invent additional ones. If the SOP and this skill ever disagree, the
SOP wins.

Related macro definition: `mcp-central-docs\standards\rules\agentic_macros.md` ->
`wrappee drift` (alias `capability audit`).

## Hard rules

- **Always scoped to one named repo.** Never run this across the fleet on your own
  initiative -- unlike `drift-scan`'s cheap file-existence probes, this requires real
  external research per repo (current docs of the wrapped software, current listings
  of comparable wrappers), which is expensive and only worth doing when asked.
- **Never build what you find in the same pass.** This produces a gap report. Building
  a found capability is a separate, explicitly-scoped follow-up task the user decides
  on after reading the report.
- **Check the wrapped software's current real docs/API, not training-data memory of it.**
  The entire point is catching drift since this repo was last touched. An answer drawn
  from memory of "what Blender can do" is exactly as stale as the repo's tool list --
  possibly staler. Fetch or introspect the current version.

## Reporting

Structure per `WRAPPEE_CAPABILITY_DRIFT_SOP.md` Phase 4: gaps because the wrapped
software moved, gaps because a comparable wrapper covers something this repo doesn't,
what this repo already has that comparables don't (for completeness, not action), and
anything found but explicitly not recommended to build, with why.

Persist to `reports/wrappee-drift-{repo}-{date}.md` (gitignored, same convention as
`drift-scan`'s reports).
