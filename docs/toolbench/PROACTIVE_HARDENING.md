# Proactive ToolBench hardening (user-friendly flow)

Goal: reduce surprise low grades by treating ToolBench as an early warning signal, not a once-a-quarter audit.

## Short answer

- **Do not** try to crawl all of ToolBench.
- **Do** track a small fixed rule set (methodology/improve/patterns), then apply a repeatable checklist across your own repos.

This is safer, lower-noise, and actually actionable.

## What to collect (and why)

1. **Methodology page**: scoring weights and dimension definitions.
2. **Improve page**: ecosystem issue categories and common misses.
3. **Patterns page**: implementation expectations for tool design.
4. **Your own report pages**: concrete repo-level criticism.

Use script: `toolbench/scripts/scrape_toolbench_reference_pages.py` for 1-3, and
`scrape_toolbench_assessments.py scrape` with your own `urls.txt` for 4.

## Is central docs collecting properly right now?

Mostly yes, but it was spread across multiple files and depended on manual reading.
Now it is clearer:

- Existing docs already covered methodology, improve loop, and batch tactics.
- New reference snapshot script adds a repeatable capture path for rules/pattern drift.
- This file defines a single operator-friendly flow.

## Weekly workflow (30-60 min)

1. Run reference snapshot script.
2. Run drift report script to compare latest two snapshots.
3. If wording changed, update:
   - `standards/TOOL_DESIGN_STANDARDS.md` (if required)
   - `toolbench/FLEET_ALIGNMENT.md`
   - `toolbench/improvements/BATCH_WORKFLOW.md`
4. For repos at risk, run targeted passes:
   - strict enums/`Literal` for finite operations
   - stronger docstrings (returns/errors/recovery)
   - transport and annotations parity
5. Request ToolBench rescan after merge and record result.

Scripts:

- `toolbench/scripts/scrape_toolbench_reference_pages.py`
- `toolbench/scripts/report_reference_drift.py`

## Practical anti-"F" checklist

- Operation fields are constrained (`Literal` / schema enums), not free-form strings.
- Tool docs describe failure modes and recovery options.
- Return payload shape is stable and documented.
- Destructive tools are explicit and constrained.
- Repo supportability is visible (README, CHANGELOG, tags, release hygiene).

## Scope guardrails

- Focus on your own fleet and your own assessment pages.
- Keep delays/jitter and avoid parallel scraping.
- Prefer official API access for large-scale automation when approved.

