# ASSFIX issue template (bot-minted, bypasses yml forms)

> Issue made by assfix on YYYY-MM-DD - SOTA NN/100 - report docs/assess-reports/YYYY-MM-DD.md @ <sha>.

## Finding (one request only)

What failed, with severity (CRITICAL / HIGH / MEDIUM / LOW).

## Evidence

- File:line at pinned commit: `path/to/file.py:123 @ <sha>`
- Failing gate output (ruff / pytest / tsc / biome), pasted, not paraphrased
- Score impact: -N points under `patterns/repo-assess-and-fix.md` scoring

## Suggested fix

Concrete, small, test-covered. Link the checklist row or standard.

## Repro

Commands to replay (exact, from repo root). No repro = not bot-safe, no `ready` label.

## Assfix deferred reason

Why this was not fixed in the run (risk, scope, needs judgment, needs wrappee, etc.).

---
Labels: `assfix` + `bug` or `enhancement`. Add `ready` only when bot-safe.
