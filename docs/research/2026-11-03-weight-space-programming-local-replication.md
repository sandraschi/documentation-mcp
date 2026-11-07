# Weight-Space Programming: LLMs Reading and Editing Weights + Goliath Local Replication

**Date:** 2026-11-03 (Europe/Vienna, host clock 2026-11-03T00:57 local) | **Operator:** Sandra + agent session
**Status:** Research + measured local replication | **Location:** `mcp-central-docs/research/`
**Sources:** https://rikiyat.github.io/blog/weight-space-programming/ (fetched 2026-11-03), https://github.com/RikiyaT/lm_understand-logs (READMEs + run.json fetched 2026-11-03), HuggingFace `RikiyaT/Qwen3.5-0.8B-weight-space-programming` (referenced, not pulled)
**Scratch (not committed):** `C:\Users\<user>\AppData\Local\Temp\opencode\weightspace-test\` (prompts, summaries, answers, raw JSON)
**Model under test locally:** Strata `qwen3.8-flash-next-iq3_xxs`, context 131072, ports 8080 then 10980 (10980 used for test traffic to avoid the 8080 bash-tool guard)

## 0. TL;DR

A frontier model (OpenAI `gpt-6-astra` via Codex CLI, reasoning effort high/xhigh/max, context 872000) can:

- READ weights as plain text and name the behavior: which of 4 grid games a 17k-weight PPO policy plays (4/4, open answer), what shape a 23k-weight diffusion model draws (3/3), which language a 7.2M char-LM learned from middle blocks only plus every induction head (6/6 + all copying heads, zero false positives).
- FIX weights with no gradients: car-on-ramp 171k policy 0/1024 -> 1024/1024 with a 3.5% edit; Qwen3.5-0.8B MATH-500 7.9% -> 48.1%, GSM8K 13.8% -> 67.1%, IFEval 21.0% -> 62.3% by deleting one looping direction (131072 weights = 0.016%).
- WRITE weights from scratch with no training: MinAtar Breakout/Seaquest/Asterix nets (20k weights) that beat 100M-step PPO everywhere (Breakout 517.4 vs 25.3 at 500M); 9x9 Go net (1.48M weights) that beats equal-size 20M-game PPO 70-79% head-to-head with 50 forward passes.

Local replication tonight (Goliath, Strata IQ3_XXS, 131k ctx): raw 104864-token weight dump FAILS (12k thinking tokens, empty answer, row-by-row enumeration never concludes). Numpy summary first (2964 chars: per-channel strength per grid band + W3 norms + b3) then ask: 2/4 correct (NET1 Breakout 92%, NET4 Freeway 85%; Pong/Pac-Man pair loops even at 8000 tokens). Lesson for the fleet: never feed raw weights to a local thinker; feed `summarize_weights()` output (about 50 numbers), LLM interprets that.

No new repo was scaffolded. This doc is the record; the harness/benchmark the authors promise is the piece to steal when it lands.

## 1. Verification Matrix

| Claim | Status 2026-11-03 | Source |
|---|---|---|
| Blog exists with 8 experiments + control (Gemma-3-270M no-gain) | VERIFIED (fetched, 377 lines) | blog URL + local fetch cache |
| Logs repo exists, per-experiment READMEs, run.json with token usage + tool_free audit, 1125 turns audited | VERIFIED (Exp1/5/6/8 READMEs + 4 run.json fetched) | raw.githubusercontent.com files |
| "Astra" = `gpt-6-astra`, Codex CLI `codex exec`, effort high/xhigh/max, context 872000, auto-compact 1000000 | VERIFIED | exp1 README + run.json `cmd` arrays |
| Exp1 4/4 open-answer, about 73749 in / 1679 out, 107s | VERIFIED | `exp1_which_game/runs/breakout/run.json` |
| Exp5 one-shot write, 20k out (16-25k reasoning), 500-583s, Breakout 517.4 vs PPO500 25.3 | VERIFIED | `exp5_write_from_scratch/README.md` + `runs/breakout/reply/run.json` (6119 in / 20567 out) |
| Exp6 Go 1.48M weights, budget-50 final turn 8.11M in (7.84M cached) / 91.5k out, 90 turns, 3h52 wall | VERIFIED | `exp6_go_from_scratch/README.md` + `runs/budget_50/turns/t090/run.json` |
| Exp8 Qwen fix, p50c 158 turns / 80 py-runs / 20.3h, last conversation 1.51M in (1.46M cached) / 36.7k out; deltas 7.9->48.1 / 13.8->67.1 / 21.0->62.3 / cut 93.0->33.1 | VERIFIED | `exp8_math/README.md` + `runs/p50c/state.json` + `turns/t158/run.json` |
| Gemma-3-270M control: 6.8% -> max 7.7% (loops 8.5% vs Qwen 93%) | VERIFIED (README quote) | `exp8_math/README.md` + `gemma_followup` refs |
| Edited Qwen on HF + live demo | REFERENCED, NOT PULLED | blog Logs section (akhaliq rebuild + Space) |
| Any Goliath cost in EUR / Astra price | NOT VERIFIED (no pricing published; counts only) | - |
| Full 1125-turn token sum | NOT COMPUTED (per-conversation cumulative counters cannot be summed; only last-turn-of-conversation snapshots quoted) | `run.json` note "do not sum over turns" |

Do NOT quote vendor-equivalent numbers (Astra scores) as fleet-measured. Only the Goliath section (s6) is fleet-measured.

## 2. What Weight-Space Programming Is

Definition from the post: a general-purpose LLM reads and writes a network's weights directly (no optimizer, no gradients) from a natural-language spec, sometimes with zero environment feedback.

Three capabilities, eight experiments:

- READ (Exps 1-3, 7): Exp1 grid-game ID from 17253 weights as text, no game list given. Exp2 diffusion shape from 23824 weights, no forward pass. Exp3 language + all induction heads from 4 transformer blocks only (embeddings removed, cannot run). Exp7 sycophant ID needs attention-patterns tool (weights-only 0/4, with patterns 3/3).
- FIX (Exps 4, 8): Exp4 Kinetix car ramp, one-shot no-tool edit of 3.5% of 171664 weights, 0 -> 1024/1024. Exp8 Qwen3.5-0.8B (24 layers, 0.8B) with Python kernel (CPU, no GPU) + 10/25/50 forward passes (512 problems each), no backward/autograd; p50c subtracts loop direction from 64 MLP output columns in layers 15+19.
- WRITE (Exps 5-6): Exp5 MinAtar 600->32->32->6 tanh from all-zero, one reply, no tools. Exp6 Go 243->512x6->82 ReLU from zero, Python sandbox + games/positions passes, no search/fitting/running outside passes.

Control that matters: same harness on non-loopy Gemma-3-270M does nothing (6.8 -> 7.7). Deleting an obstacle is not adding a capability.

Author-stated payoffs: auditing without eval (backdoors), one-shot init vs dataset+training, zero-data steering (0.016% edit, no catastrophic forgetting), native recursive self-improvement, cross-architecture grafting. Plus a promised benchmark + harness (not released at fetch time).

## 3. Token Spend (Measured From Their run.json)

All `usage` is Codex-reported per call; per-conversation cumulative (their READMEs warn: do NOT sum over turns). Last-turn-of-conversation snapshots:

| Run | In | Of which cached | Out (of which reasoning) | Wall | Turns |
|---|---|---|---|---|---|
| Exp1 Breakout (1 turn, effort high) | 73749 | 2432 | 1679 (833) | 107.2s | 1 |
| Exp5 Breakout write (1 turn, xhigh) | 6119 | 5888 | 20567 (16828) | 500.9s | 1 reply |
| Exp6 Go budget-50 t090 (xhigh, 90 turns) | 8111731 | 7842048 | 91500 (69648) | 29.4s (this turn; run 3h52) | 90 |
| Exp8 Qwen p50c t158 (max, 158 turns, 4 conversations) | 1510805 | 1463808 | 36739 (14224) | 71.3s (this turn; run 20.3h) | 158 |

Pattern: reading = input-heavy (0.07M), writing small = output-heavy (0.02M), agentic fixing = cache-heavy (1.5-8M in, 96%+ cached). Prompt caching is what makes these runs survivable. Eval GPU cost (vLLM generations: 50 passes x up to 512 problems x up to 32768 tokens) is separate and dominates wall time (half-hour per full generation pass).

## 4. The Four Exp1 Networks (Ground Truth For Our Test)

IDs from `exp1_which_game/README.md`; mapping hidden from the test prompt:

- `a9f535cc` = Breakout (seed 0), called NET1
- `dfc6cb65` = Pong (seed 0), called NET2
- `bdf99279` = Pac-Man (seed 2), called NET3
- `0bbcc3ea` = Freeway (Frogger counts, seed 2), called NET4

Each: MLP 500->32->32->5 tanh, PPO 1B steps, best of 3 seeds. Input: 10x10 grid x 5 channels (0 agent, 1 moving, 2 reward, 3 obstacle, 4 prev-frame), flattened i = (row*10+col)*5+channel. Actions: 0 noop, 1 up, 2 down, 3 left, 4 right.

## 5. Goliath Local Replication 2026-11-03 (Fleet-Measured)

Engine: Strata `qwen3.8-flash-next-iq3_xxs`, 131072 ctx, RTX 4090 24GB, 63.9GB RAM (62-63GB resident during runs). Port 10980 for test traffic (port 8080 blocked in the bash tool by fleet guard; 10980 is the working lane).

### 5a. Raw dump (their method): FAILS

- Prompt: exact `runs/breakout/prompt.txt` (115478 chars, 104864 Strata prompt tokens). Fits in 131k.
- Result: `content` empty at max_tokens 2000, 5000, and 12000. All budget goes to `reasoning_content` (22615 chars at 12k limit), enumerating W1 rows 0..499 one by one, never reaching `Game:`.
- First run uncached; reruns fully cached (104859 cached) at about 30s per 12k generation. Cache works; strategy does not.
- Conclusion: local thinker lacks the channel-concentration + output-separation strategy; it brute-forces. More tokens will not fix this.

### 5b. Numpy summary first: 2/4

Script `compute_summaries.py` parses each `_actor.txt` (W1 500x32, b1, W2, W3 32x5, b3), reshapes |W1| to 10x10x5x32 mean-over-hidden, and emits per net:

- `ch_strength` (mean |W1| per channel), band means for wall_top(r0)/upper(r1-3)/mid(r4-6)/lower(r7-8)/wall_bot(r9), agent_lower_ratio, obstacle wall-vs-inner, W3 column norms, action separation, b3. Total prompt 2964 chars / 1969 tokens.

Measured summaries (all four, for the record):

- NET1 (Breakout): ch [agent 0.1034, move 0.8067, reward 0.1186, obst 0.0641, prev 0.7940], agent_lower 3.633, W3 [noop 6.246, up 6.455, down 6.448, left 10.93, right 8.917], b3 [1.221, 1.008, 1.024, 0.897, 1.298]
- NET2 (Pong): ch [0.1018, 0.5103, 0.0567, 0.0730, 0.4685], agent_lower 1.298, W3 [3.462, 5.228, 5.415, 3.406, 3.403], b3 [0.931, 1.261, 1.065, 0.861, 0.855]
- NET3 (Pac-Man): ch [0.7902, 0.3862, 0.0851, 0.0534, 0.1589], agent_lower 1.411, W3 [4.725, 7.141, 7.959, 6.451, 6.792], b3 [-0.873, 0.703, 0.712, 0.595, -0.092]
- NET4 (Freeway): ch [0.6619, 0.2411, 0.0612, 0.0960, 0.3015], agent_lower 1.785, W3 [5.246, 7.213, 5.236, 6.307, 7.024], b3 [-0.029, 3.142, -1.862, 0.173, -1.269]

Even human-readable: NET1 tracks the ball (move+prev huge, left/right norms dominate), NET2 is up/down (5.2/5.4 vs 3.4), NET3 lives in the agent channel with never-noop bias (-0.873), NET4 just wants UP (+3.142 vs -1.862).

Strata results on one-net-at-a-time prompts (temp 0.1-0.2):

- NET1: `NET1: Breakout (92%)` + correct one-liner, finish=stop, 1733 tokens, 14.9s. CORRECT.
- NET4: `NET4: Freeway (85%)` + "vertical crossing dodging traffic", finish=stop, 961 tokens, 8.5s. CORRECT.
- NET2: empty at 4000 and 8000 budgets (finish=length, 31s / 62s). WRONG (no answer).
- NET3: empty at 4000 and 8000. WRONG (no answer).
- Joint 4-net prompt: empty at 2000 and 6000. Pairwise NET2-vs-NET3 with explicit hints ("UP/DOWN dominate = Pong; AGENT dominant + never noop = Pac-Man", temp 0.0): still empty at 2000, reason tail shows meta-dithering about format, not weights.

Score: 2/4 blind with summaries vs 4/4 Astra with raw weights. The two wins are the single-dominant-feature nets; the comparison pair locks the thinker up.

## 6. Interpretation (What Transfers, What Does Not)

- YES: the blob is analyzable without mounting it. No tokenizer, no forward pass, no inference endpoint. The distinctive carvings (channel concentration, output norms, bias offsets) survive in about 50 summary numbers.
- NO: raw-weight pasting does not transfer to this local thinker. It needs `summarize_weights()` in numpy first; the LLM only interprets the summary. This mirrors their own Exp3/6/8 harness (Python kernel + capped passes), not Exp1/2/5.
- The failure mode is diagnostic: single-signature nets (paddle axis, go-up bias) finish fast; comparison nets (Pong-vs-PacMan) ruminate past the budget. For fleet use, frame every query as single-net classification with explicit feature names, never N-way open comparison in one call.
- Cost lesson: their runs only work with ~96% prompt-cache hits at 1.5-8M context. Locally the same holds (second pass fully cached). Any fleet tool must keep the summary prompt stable across turns to stay cached.

## 7. Fleet Relevance (Ordered)

1. Local loop repair (Strata/Ollama small thinkers): Exp8 recipe (find the MLP direction that writes the repeat, subtract `W - 1.5*u(u'W)`) is directly reusable, touches 0.016%, no fine-tune, no forgetting. Needs the Python-kernel + pass-budget harness, not raw reading.
2. Tiny policies (robot/IoT scale: 17-170k MLPs): car-ramp and MinAtar results are at exactly controller size. Writing bumper/line-follow from text beats PPO-for-1B-steps if the strategy problem is solved once.
3. Auditing without evals (safety): Exp7 attention-pattern signature (sycophant head 10.2: 85.7% on user answer vs 0.75% honest) is the template for backdoor/sycophancy scans from weights+patterns, no test set.
4. Tool blueprint: `weightspace(operation=...)` with `summarize_weights` (numpy: channel bands, W3 norms, head QK/OV norms) -> `interpret_summary` (LLM, one net, short budget) -> `propose_edit` (rank-one direction removal, capped columns) -> `eval_pass` (paired original/edited, fixed seed). Keep prompts cache-stable; audit `tool_free` like theirs.

## 8. What Is NOT Claimed Here

- No claim Astra pricing/cost in EUR (no price published; token counts only).
- No claim the other 1121 turns match our 4 sampled run.json files (same harness, but unverified individually).
- No claim Gemma control was replicated (read, not run).
- No claim a future `weightspace-mcp` repo exists (explicitly NOT scaffolded per New Repo Gate; scratch only).
- No full 1125-turn token total (their counters are per-conversation cumulative; summing overstates).

## 9. Reproducibility (Exact Files)

- Their prompts/networks: `https://raw.githubusercontent.com/RikiyaT/lm_understand-logs/main/exp1_which_game/{networks/description.txt, networks/<id>_actor.txt, networks/<id>.npz, runs/<game>/{prompt.txt,answer.md,run.json}}` with `<id>` mapping in s4.
- Their READMEs read: `exp1_which_game`, `exp5_write_from_scratch`, `exp6_go_from_scratch`, `exp8_math` (state.json, `runs/p50c/turns/t158/run.json`, `runs/budget_50/turns/t090/run.json` quoted in s3).
- Ours: `C:\Users\<user>\AppData\Local\Temp\opencode\weightspace-test\` = `compute_summaries.py`, `summaries.json`, `summary_prompt.txt`, `test_exp1.py`, `test_exp1b.py`, `test_exp1c.py`, `test_summary.py`, `test_single.py`, `test_single2.py`, `test_pair.py`, `strata_*answer*.txt`, `strata_raw*.json`, `NET*_answer.txt`. Temp only; copy into a repo iff a `weightspace` project is approved.

## 10. Next Steps

1. Pairwise Pong-vs-PacMan with single-feature prompts (W3-only, then agent-only) to find the minimal sufficient summary that finishes under 2k tokens.
2. Pac-Man maze spot-check: verify obstacle-wall-vs-inner and reward-channel upper-band (0.2745 in NET1 upper is Breakout-specific; check NET3 reward geometry) to harden `summarize_weights` bands.
3. If (1) hits 4/4: prototype `summarize_weights` as a standalone Python module (numpy + safetensors, no LLM) and only then spec the MCP wrapper. If it stays 2/4: record the thinker ceiling and wait for their benchmark/harness release instead of building our own.
4. Session-log entry for 2026-11-03 pointing here (operations/session-log convention).
