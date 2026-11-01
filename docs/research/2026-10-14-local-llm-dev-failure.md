# Fully-local LLM dev on Goliath: failure writeup

**Date:** 2026-10-14 (Europe/Vienna)
**Box:** Ryzen 9 5900X, RTX 4090 24GB VRAM, 64GB DDR5 (Goliath)
**Status:** all four local lanes (glimmer, qwopus, strata, bonsai) failed for real
opencode dev work. Cloud (`meta/muse-spark-1.3-contributor`) remains the daily
driver: cheap, not free. This file records what is known, what is analysis
(labeled), and what could change the equation now vs later.

## 1. What was attempted

User statement 2026-10-14: repeated attempts to switch opencode to fully local
dev with muse glimmer, qwopus, strata, and bonsai all did NOT work. Recorded
traces in the fleet log:

- 2026-09-25: "Local Ollama on Goliath is broken install-wide
  (llama-server.exe missing) - local inference fails for every repo."
  Foundation-level breakage, not a model-quality issue.
- 2026-09-27: "Bonsai 2 27B PQ2_0 primary brain, Glimmer fallback, cheap cloud
  midlevels fallback-only" - the brain-swap attempt. Did not stick.
- 2026-10-05: Strata local-125B lane added to doctrine as UNVERIFIED candidate.
- 2026-10-14: "opencode Ollama Strata-custom-provider plausible, not tested."

The doctrine-planned A/B (qwen3.8-27B vs muse-glimmer, planned 2026-08-17) has
no recorded result. It never ran. Every champion claim since is provisional.

## 2. Box state right now (verified 2026-10-14 ~13:25)

- Ollama app process running (started 11:23), but `ollama list` timed out:
  CLI found the existing instance, then "timed out waiting for server to
  start." The daemon may be wedged; at minimum the CLI path is unhealthy.
- GPU nearly idle: 2441 MiB / 24564 MiB, 9%. No model loaded. The 4090 is
  doing nothing while cloud tokens burn.
- Strata: clone PRESENT at `D:\Dev\repos\_upstream\Strata` (correction 13:30 -
  an earlier revision of this file wrongly declared it absent after checking
  only `D:\Dev\Strata`; see the _upstream rule in `standards/AGENTS.md`
  section 10). Verified: `engine\strata.exe` built, `.venv` python present,
  `strata-iq2_xs.json` configured (131072 max-context, kv int8, kv-resident
  32768, MTP dir), `run-iq2_xs.bat` serves on port **11235** (not 8080).
  Missing: model weights (`_upstream\Strata-data\models\IQ2_XS` absent - the
  60-110GB download never landed), no strata process running. The opencode MCP
  `strata` entry points at `D:\Dev\Strata\.venv` + `tools\strata_mcp.py` - a
  stale path; the real tree is `_upstream\Strata`. No strata research doc
  found under `research/` (doctrine cites one that is not there).
- Global opencode config already contains the mitigation architecture:
  `bonsai-lean` and `strata-lean` deny-list workers, `local` Ollama agent,
  `compaction-local` profile. The harness for local-first exists. The models
  could not carry the work.

## 3. The doctrine-vs-reality gap

`LOCAL_LLM_FIRST_DOCTRINE.md` (Aug 2026) asserts "tool calling verified working
against muse-glimmer-65k" and positions qwen3.8-27B as champion candidate on
vendor numbers (SWE-bench Pro 61.7, Terminal Bench 73.0 - vendor, never
independently confirmed in-fleet). Three of the four failed lanes postdate the
docs: qwopus and bonsai appear nowhere in doctrine; strata is a four-line
UNVERIFIED row. The fleet has been operating on an August theory of local
models against October reality. Nothing below blames the docs - they say
"provisional until the A/B" - but nobody ran the A/B, so provisional hardened
into assumed.

## 4. Failure analysis (analysis, not incident log)

These are structural causes consistent with the observed failures, ordered by
leverage. Each ends with a checkable prediction.

**(a) The agent loop was built for frontier models.** opencode's loop - long
horizons, error recovery, re-planning after tool output, holding a 15-20K
token fleet preamble (CLAUDE.md + 13 standards + repo context) - assumes a
model that degrades gracefully. 27B-class models do not degrade gracefully;
they fall off: dropped tool calls, schema-shaped text instead of calls,
lost thread past ~30K tokens. A model that scores 61.7 on a benchmark can
still fail a 40-step fleet task at step 12. Prediction: local succeeds on
short-horizon tasks (lint-fix, rename, single-file edits), fails on
multi-phase work. The hybrid ladder already encodes this; the failure was
attempting a binary switch instead of task-class routing.

**(b) Tool-surface bloat eats the local context first.** A fleet session
exposes dozens of MCP tools; each schema costs tokens before the first user
message. Cloud absorbs this with 1M context. Local pays from a 32-65K
budget, and degraded-sooner-than-rated (see today's arxiv bank: SCOUT cut
PayPal tool tokens 140K -> 1.3K; Cartograph 374 tools -> 3 proxy tools).
Prediction: the same local model performs measurably better behind a
`tool_search`/`execute_tool` gateway than behind the full schema dump. This
is the highest-leverage experiment available (section 5).

**(c) The OpenAI-compat shim tax.** Verified 2026-08-16 and still true in
shape: per-model knobs differ (`think: true` for glimmer, `reasoning_effort`
for qwen, silently ignored otherwise), thinking lands in `message.reasoning`,
`num_ctx` must be set explicitly (base tags default ~4K), tool schemas
truncate without enough context and the model returns text instead of calls.
Every local lane adds a shim-behavior matrix the cloud lane does not have.
Prediction: a runbook that pins per-model knob + num_ctx + limit (like the
config already does for ollama models) eliminates a class of "model is dumb"
reports that are actually "shim misconfigured."

**(d) Foundation breaks first, models get blamed.** 09-25: llama-server.exe
missing install-wide. Today: daemon running, CLI timing out, GPU idle.
Unverified: whether any given failure was model-quality or infra. Prediction:
re-running any failed task after `ollama list` works + a loaded model +
`just gpu-status` clean will flip some "model failures" to passes. Never
evaluate a model on a sick stack.

**(e) VRAM fights and one-at-a-time swaps.** InvokeAI holds up to 8GB
(`max_cache_vram_gl := 8`); 18GB weights + 3.4GB KV + 2GB OS leaves ~0.5GB.
Anything (browser GPU, second model, InvokeAI) tips 27B-class into DDR5 swap
and tokens/s collapses - which reads as "model is slow/dumb." The
`just gpu-free / invokeai-up / gpu-status` arbitration exists for exactly
this. Prediction: failures cluster when the 4090 is shared; check `gpu-status`
in the failure record (section 5 asks for this field).

**(f) Strata and Bonsai are infrastructure projects, not model swaps.**
Strata needs its weights downloaded (60-110GB, the actual missing piece -
engine + venv + 11235 config are already built), a port claim (11235 is in
the run-bat but NOT in `operations/WEBAPP_PORTS.md` - unclaimed), and the
opencode MCP entry repointed from stale `D:\Dev\Strata` to
`_upstream\Strata`. Bonsai needs its :11436 sidecar kept healthy. Both add a
second runtime to operate. A model swap takes minutes; a runtime takes days
to shake down. They were attempted at model-swap cost. Prediction: the Strata
lane works once the weights land and the two path/port corrections are made -
that is a download plus paperwork, not research. But that job has never been
scheduled.

## 5. What could fix it now (Goliath as-is)

1. **Sick-stack check first.** `ollama list` must work, a model must load,
   `nvidia-smi` must show it resident, `just gpu-status` must show no
   InvokeAI fight. Record all four in every failure report. Do not evaluate
   models until the stack is green - today it is not (CLI timeout, GPU idle).
2. **Run the missing A/B.** Doctrine planned it 2026-08-17. Real fleet tasks,
   three classes (mechanical edit / multi-file refactor / multi-phase audit),
   pass-fail + tokens + wall time, one model at a time, same tasks. Two
   evenings of work; ends two months of vibes.
3. **Tool-surface experiment (highest leverage).** Stand up a `tool_search` +
   `execute_tool` gateway (SCOUT pattern, paper 2608.23992 in today's bank)
   in front of one lean agent and re-run the failed tasks. If local passes
   behind the gateway, the bottleneck was context, not intelligence.
4. **Task-class routing, honestly applied.** Local owns mechanical/high-volume
   (lint, renames, single-file, overnight sweeps where retries are free).
   Cloud owns architecture/dissertation/adversarial. The ladder in
   TOOLING_COST_MODEL sec 3 already says this - the fix is using it instead
   of retrying the binary switch.
5. **Per-model runbook.** Pin knob + num_ctx + limit + expected tok/s for each
   of glimmer/qwen/qwopus in one place (config has most of it; promote to a
   checklist). Kills shim-misconfig reports.
6. **Finish the Strata job or delete the lane.** Remaining work is concrete:
   download the IQ2_XS weights to `_upstream\Strata-data\models\IQ2_XS`,
   claim port 11235 in `operations/WEBAPP_PORTS.md`, repoint the opencode MCP
   `strata` entry from `D:\Dev\Strata` to `_upstream\Strata`, smoke the MCP
   tools, then dev tasks. If nobody schedules it, remove the dead config
   entries - dead entries teach agents to distrust the config.

## 6. Near future (months, not years)

- **DeepSeek V4 Q4_K_M fitting 24GB** (doctrine ETA late 2026 / early 2027):
  frontier-distilled weights at local cost would move the ceiling, not just
  the floor. Re-check quarterly.
- **Weekly crown cadence continues.** Qwen/Meta ship monthly; re-check HF
  before any long commitment. The next champion candidate obsoletes section 5
  row 2 - that is normal, plan for it.
- **64GB DDR5 is the underused asset.** The 4090 caps weights at ~20GB, but
  64GB   RAM allows big-KV and GPU+RAM offload combos (Strata's whole bet:
  125B MoE at ~100+ tok/s via offload). The local ceiling is not 27B-dense; it is
  whatever 24GB VRAM + 64GB RAM can serve together.
- **Tool-calling small models are the fastest-moving part.** Vision+tools at
  27B matured Aug-Oct; MCP Atlas-style orchestration scores keep climbing.
  The (a) gap narrows from both ends: smaller capable models + leaner tool
  surfaces.
- **Agentic-RL-trained GUI/coding models** (DART, ComputerRL in today's bank)
  suggest the next local generation will be explicitly trained for tool loops
  rather than adapted to them. That is the structural fix for (a).

## 7. Recommendation

Stop attempting "fully local dev" as a binary switch - it has failed four
lanes running and each retry costs a frustrated evening. Instead:

1. Green the stack (5.1), run the A/B (5.2), try the gateway experiment (5.3).
2. Until then: ladder discipline - local for mechanical/volume/overnight,
   muse-spark for everything else. Cheap-but-metered beats free-but-broken.
3. Every local failure gets a record: model + task class + `ollama list` state
   + `gpu-status` + tokens + where it fell off. No record, no lesson; the
   fifth lane will fail the same way.

Related: `standards/LOCAL_LLM_FIRST_DOCTRINE.md`,
`standards/TOOLING_COST_MODEL.md`, `opencode/AGENTS_AND_MODELS.md`,
`opencode/TROUBLESHOOTING.md`, session-log 2026-09-25/2026-09-27/2026-10-14.
