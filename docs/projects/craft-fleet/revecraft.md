# ReveCraft — Assessment

**Repo:** `D:\Dev\repos\revecraft` · **Date:** 2026-11-05 · **Grade: C**

> Spelling note: repo dir is `revecraft` (single-v). Rebuild PLAN §5 uses both
> `revecraft` and `reversingcraft`; the short name wins — keep `revecraft`
> everywhere and fix PLAN references opportunistically.

## What it is

Binary and reverse-engineering craft workstation. Rebuild-PLAN Wave-1 #3
(from `reversing-mcp` `revops_*`: `analyze_binary`, `extract_strings`,
`analyze_entropy`, `analyze_pe_file`, `engine die/capa/frida`, `ghidra`,
`digibib`, `hercules*`).

## Model / verbs

- **Model:** binary file (+ DKI volume for the Directmedia thread).
- **Verbs (README):** `strings entropy pe-info die capa` + `dki-decode` + `snapshot`.
- **Surface:** `cli.py` + `mcp_server.py`, `justfile`, `AGENTS.md`. 2 test files.

## Architecture

Python FastMCP, `.venv`, `pyproject`. Scaffold committed 2026-11-04.

## Strengths

- Correct engine-gating inherited from PLAN: capa is slow (42 min on 4.7 MB),
  frida executes the target (`confirm=True` + `accept_local=True`, never in default CI).
- DKI thread preserves the Directmedia/DigiBib reversing investment.
- SearchStudio receipt discipline (`down`, not silent zeros) is the right pattern.

## Gaps / risks

- Engine-heavy verbs without engines installed = red CI unless every recipe
  skips-with-receipt. Discipline must be in tests from day one.
- Frida-exec in a *craft* is the fleet's sharpest tool-safety edge; the
  confirm-gate needs code + tests, not just docs.
- Ghidra/ReVa session lifecycle (JVM boot, analyze-then-query) is unproven in this scaffold.

## Next 3 steps

1. Engine-presence gates with `down`-receipt tests (no engine → skip, never fail, never fake).
2. 3 recipes: `rev/strings-entropy`, `rev/die-capa-smoke`, `rev/dki-decode` (DKI fixture → UTF-8).
3. Frida confirm-gate in code + test (default CI never executes a target).

## Verdict

Grade C: the most dangerous craft if gated wrong, the most valuable forensics
asset if gated right. Gates first, recipes second, no exceptions.
