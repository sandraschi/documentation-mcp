# leanforge-mcp -- STATUS

**Updated:** 2026-07-09 (Claude Desktop / Sonnet 5 sprint session, continuing a Fable 5 session earlier the same day)
**Version:** Unreleased (Phase B complete; 0.1.0 was Phase A scaffold)
**Repo:** `D:\Dev\repos\leanforge-mcp` -- GitHub: `sandraschi/leanforge-mcp`
**Ranked #1 in fleet Fable-worthiness assessment:** `mcd\projects\FABLE5_WORK_RANKING_2026-07.md` -- the only fleet project where the underlying problem (adversarial verification of LLM-generated Lean proofs) is genuinely frontier-hard, not just plumbing.

## What it is

MCP server implementing Agent A from DeepMind's AlphaProof Nexus paper (arXiv:2605.22763): submit a Lean 4 theorem with a `sorry` placeholder, N parallel LLM agents loop propose-compile-feedback until one produces a sorry-free, compiler-verified proof. Three-tier LLM escalation (local Ollama -> DeepSeek -> Claude/Fable) so cheap models handle mechanical fill-in and expensive models are reserved for genuinely stuck sessions. FastMCP 3.4 server + FastAPI/React webapp sharing one SQLite job store.

## Current state -- honest summary

**Phase A (core loop) and Phase B (correctness hardening) are both DONE.** Every P1 correctness bug and P2-4 (stateless prompting) from the June assessment is fixed, tested, and confirmed on real hardware: `uv run pytest tests/ -v` on Goliath (Windows, Python 3.13.5) -- **56/56 passed in 79.18s**, zero regressions. This closes out the entire correctness-bug backlog that had been blocking sustained proof runs.

**What Phase B fixed, honestly:**

| ID | Bug | Fix |
|----|-----|-----|
| P1-1 | Helper-lemma tamper guard conflict -- adding a legitimate helper lemma (which the system prompt explicitly invites) got rejected as tampering, because the guard hashed all signatures concatenated together | Name-keyed comparison: every original declaration must keep its exact signature under its original name; new names are unrestricted. Also closes a decoy-duplicate attack a naive "is the text present anywhere" fix would miss. |
| P1-2 | `extract_statement` truncated at the first `:=` in the file -- a default-arg binder's own `:=` (e.g. `(n : Nat := 0)`) was mistaken for the proof-start `:=`, leaving the real return type unprotected | New `core/lean_lexer.py`: bracket/comment/string-aware scanner finds the terminating `:=` at the correct nesting depth. |
| P1-4 | Webapp restart falsely marked live MCP-server jobs as interrupted | `owner_pid`/`owner_started_at` columns (creation-timestamp comparison guards against OS PID reuse); startup sweep only interrupts jobs whose owner is confirmed dead via `psutil`. |
| P1-6 | Cross-process cancel was a no-op (`Runner.cancel()` only checked its own process's in-memory task dict) | `cancel_requested` DB flag any process can set; agent loop polls it once per turn via an injected callable, same pattern as the existing `on_attempt` hook. |
| P2-4 | Stateless prompting -- each turn was a fresh LLM call with no memory, so the model could loop on the same failing tactic | Exact repeated-edit detection (skips a real ~30-60s Lean recompile on an exact resend) + a rolling summary of (tactic, error-class) pairs injected into the prompt, capped at 8. |

Full detail and the "fixed in this session" ledger per item: `docs/ASSESSMENT_2026-06-24.md` in the repo.

**Verification discipline this session:** every fix was proven with real pytest execution, not inspection. During development, the pure-Python parts (no Lean/Mathlib dependency) were mirrored into scratch Linux container packages and run there -- this caught and fixed several bugs *in my own test assertions* before they could give false confidence. The final confirmation was `uv run pytest tests/ -v` on the actual Windows/Goliath target, which is the number that matters.

**What's genuinely NOT yet verified:** none of this has been run against a *live* LLM + Lean compile end to end this cycle. The 56 passing tests use stub `llm`/`lean` objects that prove the control flow (tamper guard, cancel poll, repeated-edit skip, prompt construction) is correct -- they do not prove a real DeepSeek/Ollama call plus a real Lean compile actually produces a proof. That's TODO.md's C1, and it's the natural next step before anything else in Phase C.

## Mathlib workspace

**DONE and verified**, after one false start worth remembering: an earlier attempt landed at a typo'd directory name (`leanforge_worskpace`) and only partially cached (6 `.olean` files -- just the cache tool's own bootstrap, not real Mathlib). Redone correctly at `D:\Dev\repos\leanforge-mcp\workspace\leanforge_workspace`. Discovered along the way: `lake new leanforge_workspace math` triggers Mathlib's post-clone hook, which auto-runs the equivalent of `cache get` during project creation -- 8542 files, 100% attempted, fully decompressed. Verified on disk (not just trusting the log): 1200+ real `.olean` files under `mathlib\.lake\build\lib`.

## Open work (Phase C -- see TODO.md for full detail)

Gates any batch/overnight run:

- **C1 (do first):** live end-to-end smoke run -- nothing in Phase C matters if the real pipeline doesn't work; Phase B's tests only prove control-flow correctness against stubs.
- **C2:** REPL worker pool (P2-1) -- the actual performance bottleneck. Every turn currently pays a full `import Mathlib` elaboration (~30-60s) via a fresh `lake env lean` subprocess, even though Mathlib's environment doesn't change turn to turn.
- **C3:** LLM client timeout/retry hardening (P2-2) -- no `asyncio.wait_for` anywhere in the loop; one hung HTTP call stalls a subagent indefinitely.
- **C4:** Token/cost accounting (P2-3) -- **hard gate before any batch run.** Tier 3 is Fable at ~$50/M output tokens; an overnight batch without a spend meter is a real risk against the ~€100/month AI tools budget.

Phase D+ (population-based agent, EVOLVE-BLOCK markers, fleet integration, erdosproblems.com scraper) is scoped but not detailed -- see TODO.md's archive section.

## Docs updated this session

- `README.md` -- status badge (Phase A -> Phase B complete), roadmap table renumbered (Phase C is now "performance and safety", pushing the old C-K down to D-K), prose section re-synced with the new lettering.
- `CHANGELOG.md` -- full Unreleased entry for the Phase B fix list; Planned section updated to Phase C/D+ split.
- `TODO.md` -- full rewrite. Old Phase 1/2/3 numbering clashed with `ASSESSMENT_2026-06-24.md`'s own P1-x/P2-x IDs (same numbers, unrelated bugs) -- new tasks use fresh C1-C4 IDs, old content archived in a collapsed section rather than deleted.
- `docs/ASSESSMENT_2026-06-24.md` -- every fixed item struck through with a "Fixed 2026-07-09" note and a summary of the actual fix; real-hardware pytest confirmation noted at the top.
- This STATUS.md (new).

## Verification checklist (next session)

1. **C1 first** -- live smoke test against real Ollama/DeepSeek + real Lean compile. This is the one thing pytest can't prove.
2. If C1 passes cleanly, proceed to C2 (REPL pool) for the performance win, or C4 (cost accounting) if a batch run is the near-term goal -- C4 is the harder gate.
3. `docs/BENCHMARK_RESULTS.md` is still an empty tracking template -- worth a first real entry once C1 produces a proof.

## Session log

- **2026-06-10:** Phase A scaffold complete (0.1.0). Initial P0 fixes (lifespan AttributeError, Ollama `/v1` suffix).
- **2026-06-24:** Full assessment written (`docs/ASSESSMENT_2026-06-24.md`) -- 3 P1 correctness items, 3 P2 performance/safety items, hygiene items.
- **2026-07-09 (Fable 5, then Sonnet 5 continuing same-day):** Mathlib workspace provisioned (after one typo'd false start). Phase B fully closed: P1-1, P1-2, P1-4, P1-6, P2-4 all fixed with 42 new tests. Confirmed on real hardware: 56/56 passing. README/CHANGELOG/TODO/ASSESSMENT docs updated; this STATUS.md created.
