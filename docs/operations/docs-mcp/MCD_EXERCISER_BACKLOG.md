# MCD exerciser CLI ergonomics

**Priority:** P1  
**Repo:** mcp-central-docs  
**File:** `scripts/mcd_exerciser.py`

---

- ASCII spinner (`|/-\`) via `--ascii-spinner` or auto when stdout encoding is not UTF-8.
- `--tier {turbo,standard,intel}` on `ask` and `report`.
- `--json` structured output: topic, tier_used, model, duration_s, answer, sources[].
- `--max-context <n>` and `--limit <n>` on `report` (currently hardcoded to 10).
