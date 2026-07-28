---
name: fakefind
description: Read-only audit of a repo's webapp for hardcoded mock data, dead buttons, fake stats, placeholder content, and UI that pretends to work but does not. Trigger when the user says "fakefind" followed by a repo name, "find fakes" followed by a repo name, or asks whether a UI is real, whether buttons actually do anything, or to hunt for gaslighting/mock data in a frontend. Report only, never auto-fix. Do NOT trigger for strategic worth ("is this repo worth keeping") -- that is quality-check -- or for SOTA compliance and packaging -- that is assfix.
---

# fakefind

Hunt for UI that lies. Hardcoded mock data, buttons with no handler, progress bars driven
by `setTimeout`, stats rendered as real that came from a literal, panels with no API
behind them.

## Canonical procedure

The authoritative rubric, severity table, and audit phases are in:

    D:\Dev\repos\mcp-central-docs\patterns\FAKEFIND_AUDIT_SOP.md

Read that file first and follow its phases and severity levels. Do not invent your own
severity scheme; CRITICAL/HIGH/MEDIUM/LOW are defined there and the definitions matter.

Related macro definition: `mcp-central-docs\standards\rules\agentic_macros.md` -> `fakefind`.

## Hard rules

**Read-only. Report only. Never auto-fix.** The SOP was explicitly revised on 2026-07-25
to remove auto-fixing. Propose fixes, wait for approval, then fix in a separate pass. An
audit that edits while it reads cannot be trusted, because you can no longer tell what
was already broken.

**Be brutally honest and do not soften.** The entire value of this audit is that it names
things that pretend to work. A stub reported as "partially implemented" defeats the
purpose. If a button does nothing, say the button does nothing.

Do not accept a component as real because it looks complete. Trace the data: find the API
call, confirm the endpoint exists, confirm it returns what the UI renders. A plausible
render with no source is exactly the thing being hunted.

## Output

Group by severity, worst first. Per finding give file, line, what it pretends to do, and
what it actually does. Finish with a count per severity, since the total is what tells you
whether this is a tidy-up or a rewrite.

## Token discipline

Scan by pattern before reading whole files. `Grep` for `onClick={()` with empty bodies,
`setTimeout`, hardcoded arrays feeding tables, `mock`/`dummy`/`placeholder`/`TODO`, and
API-less components. Open a file only when a hit needs confirming in context.
