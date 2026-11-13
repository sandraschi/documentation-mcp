# RSICraft

**Version:** v0.3.1 | **Updated:** 2026-11-12
**Repository:** [`D:\Dev\repos\rsicraft`](file:///d:/Dev/repos/rsicraft) | [GitHub: sandraschi/rsicraft](https://github.com/sandraschi/rsicraft)
**Family:** Rust craft apps (3-crate ArtCraft standard: `rsicraft-core`, `rsicraft-mcp`, `rsicraft-app`)

## What it is

An LLM-guided evolutionary program search tool: a local model proposes code, a sandbox scores it, a utility function picks parents for the next step. CLI, MCP stdio server (26 tools) and an egui desktop studio share one command bus.

It is also the bench for one research question: how far the Frontis-MA1 / OpenRSI self-improvement ladder (`arXiv:2607.28568`) can be climbed on one RTX 4090.

## What it is not

Not recursive self-improvement. No model generation has been trained with it. The name describes the question, not a result. Release notes and older docs that say "4-rung ladder implemented" are wrong.

## State (2026-11-12)

| Area | State |
| :--- | :--- |
| Evolution loop, store, Docker and local sandboxes | Real, verified against live local models |
| Desktop studio | Runs steps off the UI thread, live run panel; not yet checked on screen |
| Task packs | `tasks/pack-v1` (algorithm speed), `tasks/pack-v2` (heuristics and library-free ML, quality-scored) |
| Benchmark scripts | `scripts/bench-models.ps1` (resumable), `scripts/bench-analyze.ps1` |
| Promotion gate | Real A/B between two served models (Welch t of 2 or more) |
| LoRA training | Code path exists, never run end to end |
| Adapter serving, held-out split in the store, token accounting, agentic steps | Missing |

## First benchmark result

Model swap on pack-v1, 26 runs on the 35B models:
- Frontis-MA1-35B showed no advantage over its base model on these tasks (one complete trial, tasks outside its training domain).
- Search amplification (final best / first working candidate) was 1.18 at the median, inside trial noise. On tasks a large model already solves from memory, search adds almost nothing, so a training loop would have nothing to learn from.
- Consequence: an amplification gate (median of 1.5 or more) is now mandatory before any training. pack-v2 was built to pass it and is being measured.

## Estimates (judgment, 2026-11-12)

- Solid search tool: about 90%.
- One trained generation that beats its predecessor on held-out tasks, from its own traces: about 25%, more if pack-v2 passes the gate.
- Sustained recursion over several generations: under 5%.

## Where to read

In the repo: `docs/FRONTIS_PARITY_PLAN.md` (state table and phases), `docs/BENCH_MODELSWAP_V2.md` (data), `docs/PRD.md` section 5 (gated goals), `HANDOVER.md`.

## Notes for agents

- The plan's state table is the source of truth. Do not claim a rung it marks as missing.
- Report results with trial count and spread. Training on a larger model's traces is distillation, not self-improvement.
- OpenRSI code is CC BY-NC 4.0 and must not be copied into this MIT/Apache repo. Frontis-MA1 weights are CC BY-NC 4.0.
- On Goliath use `--llama-url http://127.0.0.1:11434`; port 8081 belongs to Docker. Cap `num_ctx` on Ollama aliases (16384) or models spill to CPU.
- Relation to AICraft: separate apps. Planned link: rsicraft uses `aicraft-core` routing and telemetry; AICraft gets an "Improvement Lab" pane driving rsicraft over MCP.
