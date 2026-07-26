# DiffusionGemma Assessment

## What It Actually Is

DiffusionGemma is a **26B total / 3.8B active** Mixture-of-Experts model on the Gemma 4 backbone. It does **not** generate left-to-right one token at a time. Instead it uses **block-autoregressive discrete diffusion**:

1. Initialize a 256-token canvas with random vocabulary tokens (uniform state diffusion).
2. Run the backbone in **bidirectional decoder mode** for up to 48 denoising steps.
3. Sample candidate tokens at every position; keep positions that stabilize (entropy-bounded sampler).
4. When the block stops changing, run **causal encoder mode** to commit the block into KV cache.
5. Repeat for the next 256-token block.

The same weights serve dual attention modes — causal for encode/prefill, bidirectional for denoise. That is genuine engineering, not "apply image diffusion to text" as a superficial metaphor.

### Architecture Numbers

| Parameter | Value |
|-----------|-------|
| Total params | 25.2B |
| Active params (inference) | 3.8B |
| Experts | 8 active / 128 total + 1 shared |
| Canvas (block) size | 256 tokens |
| Context | Up to 256K |
| Modalities in | Text, image, video |
| Modalities out | Text |
| Denoising steps (EB sampler) | ≤48, adaptive early stop |
| Temperature schedule | 0.8 → 0.4 linear decay |

---

## Speed vs Quality — Honest Numbers

### Where the hype is real

| Condition | Throughput |
|-----------|------------|
| FP8, batch=1, single H100 | ~1,008 tok/s (Google/vLLM) |
| H200 vs AR baseline | ~6× |
| RTX 4090, Q4_K_M (community) | ~200–400 tok/s |
| Qwen 2.5 32B Q4 on 4090 (AR, comparison) | ~40–60 tok/s |

DiffusionGemma shifts the decode bottleneck from **memory bandwidth** to **compute**. On a single-user local GPU with spare FLOPs, that trade pays off.

### Where the hype stops

Google is explicit: **DiffusionGemma scores below standard Gemma 4 AR on most published benchmarks** at matched scale. The speed is not free — it is purchased with quality on the broad eval suite.

**Exception — Humanity's Last Exam (HLE):** DiffusionGemma posts a standout **~12%** on this brutal frontier exam and actually **beats its own AR sibling** on the no-tools setting:

| HLE variant | DiffusionGemma 26B A4B | Gemma 4 26B A4B | Delta |
|-------------|------------------------|-----------------|-------|
| No tools | **11.0%** | 8.7% | +2.3 pp ✅ |
| With search | 11.9% | 17.2% | −5.3 pp |

On a benchmark where GPT-5-class models score 40–60% and most open models sit in single digits, ~12% is genuinely strong — and the no-tools win over Gemma 4 AR is the one published head-to-head where diffusion is *better*, not just faster.

### Why HLE matters more than most of the table above

HLE is not another leaderboard column. It belongs in a different weight class from MMLU Pro, MMMLU, and the other saturated evals where models cluster within a few points of each other and tell you almost nothing about frontier reasoning.

**Who built it and why:** [Humanity's Last Exam](https://lastexam.ai/) was commissioned by the **Center for AI Safety (CAIS)** — Dan Hendrycks' shop — and **Scale AI**. ~1,000 subject-matter experts across 500+ institutions submitted questions explicitly designed to **stump frontier models**. Submissions were filtered: only questions that defeated contemporary LLMs advanced to human review. The paper describes HLE as *"the final closed-ended academic benchmark of its kind"* — a deliberate attempt to build something current AI **cannot** ace, published in *Nature* ([arXiv:2501.14249](https://arxiv.org/abs/2501.14249)).

Hendrycks said the quiet part out loud when HLE launched:

> *"When I released the MATH benchmark in 2021, the best model scored less than 10%; few predicted that scores higher than 90% would be achieved just three years later. Right now, Humanity's Last Exam shows there are still expert questions models cannot answer. We will see how long that lasts."*

That is the same energy as ARC-AGI — benchmark designers who wanted a wall, not a speed bump.

**Chollet — the textbook god who put LLMs in and framed them as a dead end:** François Chollet wrote *the* Python deep learning bible. He created Keras. *Deep Learning with Python* is what the entire Python ML establishment learned from. The third edition (2025, co-authored with Matthew Watson) **does** include LLM material — transformer chapters, build-your-own-GPT projects, the full curriculum the market demands. He did not ignore the paradigm; he taught it.

But read the framing. Even the technical LLM chapters are presented through Chollet's lens: Transformers as an **"interpolative database,"** next-token prediction as memorizing vector programs, not reasoning. The hands-on content is there; the ontology is hostile. Then Chapter 19 — *"The Future of AI"* — delivers the final analysis: LLMs as "cognitive cartoons," scaling as cramming more answers into a static curve, prompt engineering as keyword search in latent space, RLHF as whack-a-mole. The book structure says: here is how to build them; here is why they are not intelligence. Compliance on coverage, contempt on conclusion.

Underneath the Keras-creator vocabulary, he is basically **parroting the stochastic parrot argument** — Bender et al., FAccT 2021: LLMs as flashy remixers with no understanding, regurgitating training data without grounding. Chollet upgrades the metaphor to "lookup table" and "vector program fetch," but the claim is the same: **it cannot find new stuff, only retrieve what it has seen.** Pretty debunked by now.

The debunking is not complicated:

1. **Combining old stuff yields new stuff.** That is not a bug; it is the mechanism. Humans do exactly this — Shakespeare read every play that came before him. Newton stood on giants. Scientific discovery is recombination under constraints, not ex nihilo invention. Chollet's *own* theory of intelligence centers on recombination and program synthesis — then he denies LLMs can recombine, which is incoherent at scale.

2. **Empirical gaps are closing.** Reasoning models, HLE at ~12% for DiffusionGemma (beating its AR twin no-tools), code generation at production scale, novel theorem proving, drug candidate proposals — these are not lookup hits on memorized Q&A pairs. Imperfect, yes. Lookup table, no.

3. **Diffusion sharpens the point.** Bidirectional canvas denoising explicitly revises partial solutions — the opposite of left-to-right commitment. If the stochastic-parrot critique is "it can only fetch, never revise," diffusion LM is architecturally aimed at the counterargument. HLE results suggest it works, at least partially.

The stochastic parrot was a useful 2021 warning about hype, environmental cost, and benchmark gaming. As a *timeless* theory of capability limits, it aged badly — much like calling databases "just filing cabinets" because they store rows you typed in, missing that query composition produces answers no row contains.

He is, in the Python prof league, what Ed Zitron is in tech media: the credentialed insider who engages the thing he opposes on its own terms, then lands the negative verdict anyway. Zitron covers AI constantly to call it a bubble; Chollet teaches GPT construction while recycling stochastic-parrot logic in professor dialect. Different vocabularies, same structural position — **the gap must remain**, because closing it would retire the critique. Chollet is the more serious mind (actual theory of intelligence — which makes his denial of LLM recombination harder to excuse). Zitron is the more entertaining one. Both are benchmark priests in the AI-of-the-Gaps church.

The irony Chollet cannot escape: he designed ARC-AGI-1 to be a binary test — zero fluid intelligence or human-level, nothing in between. o3 scored 75–85%. So he shipped ARC-AGI-2. Then ARC-AGI-3. The textbook author who insists LLMs cannot reason keeps building harder exams for the thing he says cannot pass. Hendrycks does the same with HLE. The gaps close; the priests ordain new ones.

**The ARC-AGI parallel (2024 → 2026):** François Chollet's ARC-AGI (2019) was explicitly designed to test fluid intelligence on novel puzzles, not memorized patterns. For years it looked unbeatable. Then reasoning models arrived: OpenAI o3 scored 75–85% on ARC-AGI-1. Response? **ARC-AGI-2** — adversarially recalibrated so frontier models score single digits while humans still solve every task. o3 broke v1 → they shipped v2. Now **ARC-AGI-3** (2026) moves to interactive agentic environments where frontier AI scores **<1%** and humans hit 100%. Classic goalpost shift: the benchmark moves faster than the victory lap.

HLE is earlier in that cycle. Models are still in single digits to low double digits. But the trajectory is obvious — when frontier models push HLE past ~30–40%, CAIS/Scale will either declare saturation and publish HLE-2, or pivot to held-out private sets and harder modalities. **Time for another goalpost shift.**

### The AI of the Gaps

Theology has *God of the Gaps* — the habit of placing divinity in whatever science has not yet explained, then quietly moving God to the next unexplained corner as science advances. AI benchmarking has the same structure, stripped of the theology:

| God of the Gaps (theology) | AI of the Gaps (benchmarking) |
|----------------------------|-------------------------------|
| "Science can't explain X" | "AI can't solve benchmark X" |
| Science explains X | Frontier model scores 40% on X |
| "Well, science can't explain Y" | "That doesn't count — benchmark X is saturated / gamed / brute-forced" |
| Repeat | Ship benchmark Y, harder modality, interactive variant |
| God retreats to the remaining mystery | "Real intelligence" retreats to the remaining unsolved eval |

The benchmark designer's God lives in the gap between current model scores and human performance. The gap is real — HLE at ~12% vs humans near 100% is a genuine capability cliff. But the *identity* of the gap is negotiable. MATH was the gap until it wasn't. ARC-AGI-1 was the gap until o3. HLE is the gap now. ARC-AGI-3 interactive is already the next gap.

This is not an argument that benchmarks are useless. Gaps are how you measure progress. The mistake is treating any particular gap as **permanent evidence** that the paradigm is wrong — or, symmetrically, treating closing one gap as proof of AGI. Both sides do it:

- **Skeptics:** "Models fail HLE → not real reasoning." (Gap = last word.) Chollet: "LLMs are interpolative databases." Hendrycks: "We will see how long that lasts."
- **Boosters:** "Models pass MMLU → basically solved." (Gap already closed, move on.)
- **Reality:** Models close gaps. Designers open new ones. The frontier is a moving target, not a wall and not a mirage. The benchmark priests — Chollet in the Python prof league, Hendrycks at CAIS, Zitron in the newsletter economy — each have structural incentives for the gap to survive.

DiffusionGemma is interesting precisely because it closes a different gap than expected. Everyone assumed the speed-optimized diffusion model would be worse *everywhere*. It is worse on most saturated evals — but it **widened the gap the other direction** on HLE no-tools vs its own AR sibling. The AI-of-the-Gaps lesson: **watch which gaps close, not just which gaps remain.** A paradigm that wins on the anti-saturation benchmark while losing on the saturated ones is telling you where the next ceiling is — and it may not be where the benchmark priests expected.

**What DiffusionGemma's HLE result actually signals:**

| Benchmark type | What it measures | DiffusionGemma story |
|----------------|------------------|----------------------|
| Saturated (MMLU, etc.) | Knowledge retrieval, mostly memorized patterns | Behind AR sibling — expected for speed-first model |
| Anti-saturation (HLE) | Expert reasoning on questions that stumped frontier LLMs at design time | **~12%, beats Gemma 4 AR no-tools** — the interesting number |

A model that loses on MMLU but punches above its AR sibling on HLE is not uniformly "worse." It may be **better at the thing the frontier skeptics actually care about** — multi-step reasoning under constraint, where canvas refinement beats left-to-right commitment. That is exactly the Sudoku/infill advantage, scaled to graduate-level academic questions.

Plausible mechanism: HLE questions require holding partial solutions, revising when new constraints emerge, and converging on unambiguous answers — bidirectional denoising is built for this. AR models commit token-by-token and cannot unwind. With search tools enabled, AR's agentic tool-loop advantage reasserts itself (11.9% vs 17.2%), which is its own telling result.

**Fleet implication:** Do not write off DiffusionGemma based on MMLU deltas alone. For Ednaficator-style reasoning pipelines and hard constraint tasks, HLE is the benchmark that actually matters — and this model over-indexes on it relative to its AR twin.

**Second-order implication — Yudkowsky (slightly) more plausible:** Eliezer Yudkowsky's core capability worry was never "transformers specifically" — it was that **general intelligence arrives faster, from more directions, and with less warning than the gradualist consensus expects.** He lost specific bets (hand-coded seed AI, RSI-before-foom timing, early calendar dates). He may be gaining on the meta-bet: *capability discontinuities from unexpected architectures.*

DiffusionGemma is a **v1 speed-optimized diffusion LLM** — explicitly below Gemma 4 AR on most benchmarks, shipped six months after the paradigm went open-weights. It is the thing Chollet would dismiss and Hendrycks built HLE to stump. And it already beats its AR sibling on the no-tools frontier exam.

If the anti-saturation benchmark — the one designed by people who wanted something AI cannot solve — cracks first on a **quality-sacrificed experimental architecture** rather than on the flagship autoregressive model, that is a Yudkowsky-shaped data point:

| Comfort narrative | What HLE suggests |
|-------------------|-----------------|
| Progress tracks saturated benchmarks (MMLU, etc.) | Frontier capability can leap on evals nobody optimized for |
| One paradigm (AR scaling) is the only path | Parallel architectures unlock different capability profiles |
| We will see AGI coming because it will ace the benchmarks we watch | The variant you wrote off may ace the benchmark the priests cared about |
| Decades of gradual Hanson-style diffusion | Architectural phase shifts produce discontinuities |

**Slightly** more plausible — not validated. Yudkowsky's alignment doom thesis does not follow from HLE scores. Neither does hard takeoff in hours. What follows, weakly: the **capability surprise** leg of his worldview. When a speed-hack diffusion v1 over-indexes on Humanity's Last Exam, the stochastic parrots and benchmark priests are not the epistemically safe side to bet on. The gap closed from an unexpected direction. That is the thing Yudkowsky has been saying for twenty years — usually too loudly and too early, but not always wrong about the shape of the surprise.

| Trade-off | Detail |
|-----------|--------|
| Factual accuracy | Higher error rate vs Gemma 4 AR on most benchmarks; HLE no-tools is the outlier |
| Streaming UX | None — 256-token blocks appear at once |
| High-concurrency serving | AR wins at batch 32+ via KV cache reuse |
| Bidirectional attention | Cannot share KV across concurrent requests the way AR serving stacks do |

### Genuine capability advantage

Autoregressive models fail on **strict multivariable constraints** (classic example: Sudoku) because they cannot revise committed left-to-right tokens. Diffusion models evaluate the full canvas and can backtrack within a block. Same class of win as **code infill** and **in-line editing** — domains where global consistency matters more than fluent prose.

---

## Analogy: Early Image Diffusion (The "14-Finger Hands" Era)

This is the most useful mental model for where diffusion LLMs sit in 2026.

### Image diffusion ~2022–2023

Stable Diffusion 1.x/2.x and early DALL·E iterations produced images that were:

- **Globally plausible** — composition, lighting, style often worked.
- **Locally broken** — extra fingers, melted faces, illegible text, wrong object counts.
- **Fast to iterate on** — seconds per image vs hours of manual art.
- **Structurally different failures** from GANs or autoregressive image models (PixelCNN, etc.).

The community did not abandon diffusion because hands looked wrong. They treated it as a **solvable artifact phase** while the paradigm's throughput advantage was already obvious. Fixes came from better samplers, ControlNet, fine-tunes, SDXL, FLUX, and years of RLHF/DPO on human preference — not from going back to autoregression for images.

### Text diffusion ~2025–2026 (now)

DiffusionGemma exhibits the **same artifact profile**, transposed to language:

| Image diffusion artifact (2022) | Text diffusion artifact (2026) |
|--------------------------------|--------------------------------|
| Extra fingers | Factual hallucination within blocks |
| Melted faces | Coherence breaks across block boundaries |
| Wrong object count | Constraint violations (counts, formatting) |
| Illegible text in image | Token-level fluency without global factual lock |
| Fast but scary | Fast but benchmark-lagging |

| Image diffusion strength (2022) | Text diffusion strength (2026) |
|--------------------------------|--------------------------------|
| Global composition in one pass | Global block consistency (Sudoku, infill) |
| Parallel denoise = fast iteration | Parallel denoise = 4–10× tok/s locally |
| Self-correction within steps | Uniform state re-noising fixes bad tokens |
| Weird failures ≠ useless | Quality gap ≠ useless for batch workloads |

### What the analogy predicts

1. **Do not judge the paradigm by v1 quality alone.** LLaDA already showed MDMs can approach LLaMA3-8B; DiffusionGemma regresses vs its own AR sibling because Google optimized for speed first.
2. **Artifact types will shrink** as samplers mature (EB → better schedules), block size tuning, and preference optimization (LLaDA 1.5 VRPO is the template).
3. **The UX problem is real and different from images.** Nobody needed streaming from an image generator. Chat users expect token-by-token output. Block diffusion is a product problem, not just a research problem.
4. **Niche-first adoption** — exactly like early SD was for mood boards and concept art, not final deliverables. Batch synthetic data, MCP tool output, Ednaficator pipelines: the mood-board tier.

---

## Goliath-Specific Assessment

| Criterion | Verdict |
|-----------|---------|
| VRAM (Q4_K_M) | ✅ ~15–18 GB model + ~3 GB desktop overhead fits in 24 GB |
| VRAM (Q8_0) | ❌ ~26–28 GB — does not fit |
| NVFP4 path | ⚠️ Skip — Blackwell-optimized; 4090 is Ada |
| RAM for load | ✅ 64 GB sufficient |
| LM Studio today | ❌ Awaiting upstream llama.cpp merge |
| Ollama today | ❌ Not supported |
| llama-diffusion-cli | ✅ Runnable with PR branch build |
| Expected speed | 200–400 tok/s (conservative); community highs ~500+ |

**Recommendation tier:** Secondary speed model for offline batch generation. Not a replacement for the primary autoregressive local model until quality gap closes and streaming UX is solved.

---

## Comparison Matrix: DiffusionGemma vs Fleet Alternatives

| Model class | Speed (4090) | Quality | Streaming | Fleet tooling |
|-------------|-------------|---------|-----------|---------------|
| DiffusionGemma 26B Q4 | ★★★★★ | ★★★☆☆ (★★★★ on HLE) | ✗ (256-token blocks) | Bleeding edge |
| Qwen 2.5 32B Q4 (AR) | ★★☆☆☆ | ★★★★☆ | ✓ | LM Studio, Ollama |
| Gemma 4 26B AR | ★★☆☆☆ | ★★★★★ | ✓ | Transformers |
| LLaDA 8B (MDM) | ★★★☆☆ | ★★★★☆ (8B tier) | Partial | Research |
| Cloud API (Gemini etc.) | N/A | ★★★★★ | ✓ | `google-ai-mcp` |

---

*See [RESEARCH.md](./RESEARCH.md) for paper trail, [FLEET_USAGE.md](./FLEET_USAGE.md) for deployment fit.*
