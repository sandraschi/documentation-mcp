---
name: drift-scan
description: Read-only fleet-wide gap analysis across every repo under D:\Dev\repos. Trigger whenever the user says "drift", "drift scan", "which repos need fixing", "fleet triage", or asks how badly repos deviate from current fleet standards. This is the fleet-wide TRIAGE tool that decides which repos to assfix; it is not itself a fix. Do NOT trigger for single-repo work ("assess and fix X", "lint this repo") -- that is the assfix skill.
---

# drift scan

Fleet-wide, read-only gap analysis. Answers "which repos need work, and how badly",
so an assfix campaign can be prioritised instead of guessed at.

## Canonical procedure

The authoritative checklist is:

    D:\Dev\repos\mcp-central-docs\patterns\DRIFT_SCAN_SOP.md

Read that file first and follow it. Do not reconstruct the checks from memory and do
not invent additional ones. If the SOP and this skill ever disagree, the SOP wins.

Related macro definition: `mcp-central-docs\standards\rules\agentic_macros.md` -> `drift`.

## Hard rule

**Never fix anything during a drift scan.** Note every gap, touch no files. Fixing is
assfix's job, and mixing the two makes the triage output untrustworthy because you can
no longer tell what was already broken.

## Reporting

Rank repos worst-first. For each, state the specific gaps rather than a score alone,
since the point of the scan is deciding what to do next.

End with a recommended assfix order and a rough effort estimate per repo. Use realistic
AI-assisted timelines (days, not weeks).

## Token discipline

This scan touches many repos, so read selectively. Prefer targeted `Grep`/`Glob` and
file-existence checks over reading whole files. Only open a file when its content
actually decides a check. Summarise per repo as you go rather than accumulating full
file contents in context.
