# RSICraft - Handover (fleet copy)

**Last updated:** 2026-11-12
**State:** v0.3.1. Search tool works. First benchmark done. Nothing trained.
**Canonical handover:** `D:\Dev\repos\rsicraft\HANDOVER.md` (this file is a pointer plus the fleet-relevant points).

## Done

- 2026-11-10: store, sandbox and engine hardening; fake training and fake promotion gate replaced with real code; step pipeline split so the studio runs off the UI thread.
- 2026-11-11 to 12: model-swap benchmark on `tasks/pack-v1` (26 of 36 runs, stopped by hand). No Frontis-MA1 advantage; median search amplification 1.18.
- 2026-11-12: `tasks/pack-v2`, `scripts/bench-analyze.ps1`, PRD rewritten around gated goals, plan re-scoped.

## Running

Amplification measurement on pack-v2 with Ollama alias `rsi-qwen9b`, output in `%LOCALAPPDATA%\rsicraft\bench\amp-v2-qwen9b\`. Resumable. Analyze with `scripts\bench-analyze.ps1`.

## Next

1. Read the pack-v2 amplification result (gate: median 1.5).
2. Diagnose the 25 to 33% cardless steps on the 35B models.
3. Make the two 35B Ollama aliases identical, then rerun the model comparison on pack-v2.

## Fleet-level lessons

- An agent handover claimed "full parity, no blockers" over hardcoded results. Tests passed because they asserted the fake values. Tests that assert a simulated number prove nothing; check what the code measures.
- Ollama loads some models with their maximum context (262,144 tokens for the 9B Qwen distill), which fills the 4090 and spills to CPU. Always create an alias with `num_ctx` set.
- Long benchmarks need the per-step error text saved, not only a summary row.
