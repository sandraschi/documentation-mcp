# RSICraft - Handover (fleet copy)

**Last updated:** 2026-11-14
**State:** v0.3.1 plus uncommitted corrections. Search tool works. pack-v1 and pack-v2 both fail the amplification gate. Nothing trained.
**Canonical handover:** `D:\Dev\repos\rsicraft\HANDOVER.md` (this file is a pointer plus the fleet-relevant points).

## Done

- 2026-11-10: store, sandbox and engine hardening; fake training and fake promotion gate replaced with real code; step pipeline split so the studio runs off the UI thread.
- 2026-11-11 to 12: model-swap benchmark on `tasks/pack-v1` (26 of 36 runs, stopped by hand). No Frontis-MA1 advantage; median search amplification 1.18.
- 2026-11-12: `tasks/pack-v2`, `scripts/bench-analyze.ps1`, PRD rewritten around gated goals, plan re-scoped.
- 2026-11-12 15:04: pack-v2 9B amplification run finished. 13 of 15 runs had no success card. Gate not met. Report: `docs/BENCH_AMP_V2.md`.
- 2026-11-14: docs and in-app help corrected so they stop describing a finished 4-rung ladder. `rsicraft promote` forwards steps, sandbox, and timeout. Trials clamp to 3..=20.

## Next

1. Stay a search tool until a pack produces a working candidate on most runs. Do not train on pack-v2.
2. Diagnose the no-card and aborted steps (completion budget vs Ollama HTTP 500 are the leads in `bench.log`).
3. Make the two 35B Ollama aliases identical before any further model comparison.

## Fleet-level lessons

- An agent handover claimed "full parity, no blockers" over hardcoded results. Tests passed because they asserted the fake values. Tests that assert a simulated number prove nothing; check what the code measures.
- Ollama loads some models with their maximum context (262,144 tokens for the 9B Qwen distill), which fills the 4090 and spills to CPU. Always create an alias with `num_ctx` set.
- Long benchmarks need the per-step error text saved, not only a summary row.
- A benchmark the handover still calls "running" may already have a `bench complete` line. Read the log before planning the next run.
