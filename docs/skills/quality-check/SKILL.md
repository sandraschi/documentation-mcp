---
name: quality-check
description: Strategic, qualitative assessment of whether a fleet MCP server repo is worth having -- its originality, difficulty, wrappee, competition, tool surface, fleet integration, and whether to promote, archive, or deprecate it. Trigger when the user says "qualitycheck" followed by a repo name, "is this repo worth it", "should I archive X", or asks for a strategic rather than mechanical review. Do NOT trigger for SOTA compliance, linting, or packaging (that is assfix), nor for auditing a webapp for mock data and dead buttons (that is fakefind).
---

# quality check

Strategic assessment of a single repo. assfix answers "does this repo meet the technical
bar". quality-check answers "does this repo *matter*".

## Canonical procedure

The authoritative rubric is:

    D:\Dev\repos\mcp-central-docs\patterns\QUALITY_CHECK_SOP.md

Read that file first and follow it. Do not substitute a generic code review.

Related macro definition: `mcp-central-docs\standards\rules\agentic_macros.md` -> `qualitycheck`.

## Stance

This is a judgment call, not a checklist with pass/fail boxes. The SOP says it directly
and it is the whole point of the exercise: **be honest, flattery helps no one.**

A perfectly formatted repo wrapping a service nobody needs is still worthless. A scrappy
repo with a unique angle and real integration potential is valuable despite cosmetic
flaws. Say which one you are looking at, plainly, and say why.

If the recommendation is "archive this", say so directly rather than softening it into a
list of improvements. An unclear verdict wastes the assessment.

## Output

Reach an actual verdict: promote, keep, improve, or archive. Give the reasoning, the
strongest counter-argument to your own verdict, and the concrete next step if kept.

## Token discipline

Read enough to judge, not everything. README, entry point, tool surface, and the
integration points usually settle it. Resist reading the whole tree; if you find yourself
opening a tenth file, you are doing an assfix rather than a quality check.

## Relationship to fakefind

These overlap on exactly one dimension: the webapp. Do not re-derive it.

fakefind answers "is this real" with evidence (file, line, severity). quality-check
answers "is this worth having". If a recent fakefind report exists, consume its severity
counts as an input to the verdict rather than re-auditing the frontend yourself. If one
does not exist and the webapp materially affects the verdict, say so and recommend running
fakefind first instead of guessing.

A repo can be entirely real and still not worth keeping. A repo can be full of mock data
and still be the right bet. Keep the two judgments separate.
