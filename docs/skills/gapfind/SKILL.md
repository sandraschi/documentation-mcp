---
name: gapfind
description: Read-only audit of which backend capabilities (REST routes, MCP tools) a repo's webapp never surfaces, plus webapp calls to routes that do not exist. Trigger when the user says "gapfind" followed by a repo name, or asks "are there api endpoints or mcp tools in the backend that are not surfaced / used in webapp pages", or what the backend can do that the UI does not show. Report and propose only, never auto-fix. Do NOT trigger for mock data / dead buttons (that is fakefind), fleet-standard compliance (drift-scan / assfix), or coverage against the wrapped software's API (wrappee-drift).
---

# gapfind

Find backend services the webapp forgot. Most fleet repos were built MCP-server-first and
got a webapp later, so useful endpoints and tools often have no page.

## Canonical procedure

Read first and follow its phases, status meanings and classification categories:

    D:\Dev\repos\mcp-central-docs\patterns\GAPFIND_AUDIT_SOP.md

Run the script, do not reason from memory:

    uv run --project D:\Dev\repos\<repo> python D:\Dev\repos\mcp-central-docs\scripts\gapfind.py D:\Dev\repos\<repo> --out D:\Dev\repos\<repo>\reports\gapfind-<yyyy-mm-dd>.md

Date from the real clock. Check the detection notes at the top of the output before
trusting anything below them.

## Hard rules

**Read-only. Report and propose only.** Fixes are a separate, approved pass.

**Code truth, not a skim.** Route and tool lists come from the live objects. Never answer
the question by sampling a few files.

**0 routes detected = detection failure, not a clean result.** Rerun with
`--app module:attr` / `--syspath DIR`.

**Classify every non-`used` row** as SURFACE / HEADLESS / ADMIN / DEAD / DUPLICATE /
REVERSE (definitions in the SOP). The script's status column is a heuristic; `via-REST?`
twins in particular must be confirmed by reading the route handler.

## Output

The script report, then a classification table, then a prioritized fix list: existing
endpoints that only need UI first (cheapest user value), new backend work last. Suggest
`.gapfind-headless` entries for everything classified HEADLESS so reruns stay clean.
