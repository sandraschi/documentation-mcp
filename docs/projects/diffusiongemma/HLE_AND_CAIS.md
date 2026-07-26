# Humanity's Last Exam, CAIS, and the moving goalpost

**Why this page exists:** DiffusionGemma's standout HLE score (~12%, beating its AR twin on no-tools) is the main reason [`diffusion-llm-mcp`](https://github.com/sandraschi/diffusion-llm-mcp) exists as a separate fleet repo. You cannot understand that routing decision without understanding what HLE is, who built it, and what incentives sit behind it.

**Archive note:** Canonical copy lives here in **mcp-central-docs** (deep narrative). The fleet repo mirrors this page for readers who land on GitHub first.

**Primary sources:** [lastexam.ai](https://lastexam.ai/) · [arXiv:2501.14249](https://arxiv.org/abs/2501.14249) (*Nature*, 2026) · [CAIS](https://www.safe.ai/) · [DiffusionGemma model card HLE scores](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)

---

## 1. What HLE is

**Humanity's Last Exam (HLE)** is a multi-modal benchmark of ~2,500 expert-level academic questions across 100+ subjects — mathematics, physics, chemistry, biology, medicine, computer science, humanities, social sciences.

| Property | Detail |
|----------|--------|
| **Authors** | Center for AI Safety (CAIS) + Scale AI + global contributor consortium |
| **Curation** | ~1,000 subject-matter experts, 500+ institutions, 50 countries |
| **Filter** | Questions had to **defeat frontier LLMs** at submission time to advance |
| **Answer format** | ~80% exact-match, ~20% multi-choice (5+ options), ~10% multimodal |
| **Anti-lookup** | Designed to resist quick web retrieval; unambiguous verifiable answers |
| **Branding** | *"The final closed-ended academic benchmark of its kind"* |
| **Prize** | $500K pool for contributors |

It exists because **MMLU saturated**. Models hit 90%+ on standard evals; the field could no longer measure frontier capability on the leaderboards everyone watched. HLE was built to be the **new wall**.

---

## 2. Who CAIS is

The **[Center for AI Safety](https://www.safe.ai/)** (CAIS), led by **Dan Hendrycks**, is an AI safety research organization — not an "anti-AI" lobby in the sense of opposing all machine learning, but an institution whose reputation and funding are tied to **AI risk, capability surprise, and the gap between current systems and safe superintelligence**.

Hendrycks also created **MATH** (2021), **MMLU**, and other benchmarks that became the field's scoreboard — then watched models saturate them.

His HLE launch quote is the mission statement in plain English:

> *"When I released the MATH benchmark in 2021, the best model scored less than 10%; few predicted that scores higher than 90% would be achieved just three years later. Right now, Humanity's Last Exam shows there are still expert questions models cannot answer. **We will see how long that lasts.**"*

Read that last sentence carefully. It is not neutral science. It is a **timed bet against closure**.

---

## 3. "Anti-AI" — what that actually means here

Nobody at CAIS is burning GPUs. "Anti-AI" in this context means **anti-satisfaction** — a structural skepticism toward the claim that current LLM trajectories constitute "real" reasoning or near-AGI.

| Surface position | Underlying claim |
|------------------|------------------|
| "HLE measures expert frontier" | Saturated benchmarks lied; this one won't (yet) |
| "Models still fail expert questions" | Therefore current AI is not there |
| "We will see how long that lasts" | The gap is temporary; our job is to measure its retreat |
| Safety framing | Capability gains without alignment = existential risk |

This is the **benchmark priesthood**: credentialed institutions that build the walls models must fail, publish the failure as news, and **rebuild the wall** when models climb it.

CAIS is the Hendrycks branch. **François Chollet** (ARC-AGI) is the parallel branch in the Python-prof league. **Emily Bender** (stochastic parrots) is the linguistic branch. **Ed Zitron** is the newsletter branch. Different vocabularies; same geometry.

---

## 4. Human essentialism — the philosophy hiding in the rubric

**Human essentialism** (in this doc's sense): the implicit belief that **some cognitive capacity is uniquely, essentially human**, and that AI systems demonstrating surface competence on benchmarks have not captured it.

HLE encodes this assumption in its design:

1. **Expert humans wrote the questions** — authority flows from credentialed humans, not from task structure alone.
2. **LLM failure at curation time was a selection criterion** — the benchmark is defined by what machines could not do *when it was built*.
3. **"Humanity's Last Exam"** — the name itself claims a finality, a category ("humanity") that stands apart from machine performance.
4. **Low model scores are interpreted as "significant gap"** — not as "early technology on a hard test," but as evidence about the *nature* of machine cognition.

The God-of-the-Gaps structure, adapted to AI:

| Theology | AI benchmarking |
|----------|-----------------|
| God lives in unexplained phenomena | "Real intelligence" lives in unexplained benchmark failures |
| Science explains X | Models score 40% on X |
| "God is in Y now" | "That doesn't count — saturated / gamed / not real reasoning" |
| Repeat | Ship benchmark Y |

**Human essentialism does not require hatred of machines.** It requires that **the remaining gap** always be interpreted as proof of a categorical difference — not as a temporary engineering deficit on a moving frontier.

The stochastic parrot thesis is the folk version: machines **cannot** genuinely recombine; they only retrieve. Shakespeare also retrieved — every play before him — and recombined. The essentialist move is to call human recombination "understanding" and machine recombination "pattern matching," regardless of output equivalence on hard tests.

---

## 5. Goalpost moving — documented pattern

HLE is not the first wall. It is the **current** wall.

| Benchmark | Era | Design intent | What happened |
|-----------|-----|---------------|---------------|
| **MATH** | 2021 | Hard math for models | >90% in ~3 years |
| **MMLU** | 2021+ | Broad knowledge | Saturated; models cluster 85–90%+ |
| **ARC-AGI-1** | 2019 | Fluid intelligence; novel puzzles | o3 → 75–85% |
| **ARC-AGI-2** | 2025 | Adversarially harder; frontier models → single digits | Active |
| **ARC-AGI-3** | 2026 | Interactive agentic; AI <1%, humans 100% | Active |
| **HLE** | 2025–26 | Expert academic; stump frontier models | Climbing — GPT-5 class 40–60%, open models low double digits |
| **HLE-2** | (projected) | When HLE saturates | Inevitable under current incentives |

**Goalpost moving is not a moral failure.** It is a **measurement strategy** when the field outruns evals. The problem is epistemic, not ethical: treating any *particular* gap as permanent evidence about paradigm limits, or as proof that "real intelligence" remains human-only.

Chollet designed ARC-AGI-1 as a **binary** fluid-intelligence test: near-zero or human-level, nothing between. o3 landed in between at 75–85%. Response: ARC-AGI-2. The textbook author who insists LLMs cannot reason **keeps issuing harder exams to the thing he says cannot pass**.

Hendrycks built MATH, watched it die, built HLE, and bet publicly on how long HLE will live. **Time for another goalpost shift** is not cynicism — it is the stated product roadmap.

---

## 6. HLE scores that matter for this repo

From [DiffusionGemma model card](https://ai.google.dev/gemma/docs/diffusiongemma/model_card) (Entropy-Bounded sampler):

| Benchmark | DiffusionGemma 26B A4B | Gemma 4 26B A4B |
|-----------|------------------------|-----------------|
| MMLU Pro | 77.6% | **82.6%** |
| **HLE no tools** | **11.0%** | 8.7% |
| **HLE with search** | 11.9% | **17.2%** |
| GPQA Diamond | 73.2% | **82.3%** |

**Reading this correctly:**

- On **saturated** evals, the speed-optimized diffusion model loses to its AR sibling — expected.
- On **HLE no-tools** — the exam CAIS built to resist AI — diffusion **wins** by 2.3 points.
- On **HLE with search**, AR wins — tool loops and agentic retrieval favor autoregressive serving stacks.

So the anti-saturation benchmark is exactly where the "worse" paradigm over-indexes. The wall CAIS built is already cracking **from the direction they were not optimizing for** — a v1 diffusion model optimized for throughput, not for leaderboard farming.

---

## 7. Why the fleet routes on HLE, not MMLU

| If you optimize for… | You build… | You miss… |
|---------------------|------------|-----------|
| MMLU / saturated leaderboards | Bigger AR, better fine-tunes | Paradigm hops that ace anti-saturation evals |
| HLE / frontier reasoning | Models that revise under constraint | Streaming chat UX |
| Catch-them-all | Separate repos per paradigm | Single-point-of-failure hype pivots |

`diffusion-llm-mcp` exists because **routing on MMLU alone would have written off DiffusionGemma** — and HLE says that was wrong for batch/frontier-shaped work.

This does **not** mean dLLM is AGI or that CAIS is wrong about safety. It means:

1. **The gap's address is negotiable** — which benchmark you watch determines which paradigm looks "ahead."
2. **Benchmark priests have incentives for the gap to survive** — not necessarily dishonest, but structurally loaded.
3. **Capability surprises arrive from unanticipated architectures** — slightly Yudkowsky-shaped; see [PROGNOSIS.md](./PROGNOSIS.md).

---

## 8. Fair accounting — what CAIS gets right

Do not strawman this. CAIS and HLE contributors did real work:

- **Saturation is real.** MMLU at 90%+ was measuring less than it used to.
- **Expert curation matters.** HLE questions are hard, verified, and cross-disciplinary.
- **Safety research needs hard evals.** Capability measurement and risk assessment are linked.
- **The gap is still enormous.** 11% vs near-100% human expert performance is not AGI.
- **HLE-Verified and critique exist.** The benchmark is contested; good — science should be.

The fleet critique is narrower: **do not let the priesthood's choice of gap dictate your inference architecture.** Watch which gaps close, from which direction.

---

## 9. The stadium perimeter — how far can goalposts move?

Think of the whole eval landscape as a **stadium**. The field is everything we can meaningfully test: closed-ended expert questions, puzzles, agentic environments, economic tasks, physical embodiment. **Goalposts** are the painted lines the priesthood moves whenever models start scoring.

You can move them a long time. You cannot move them forever.

### Walls you eventually hit

| Perimeter wall | What stops the move |
|----------------|---------------------|
| **Human calibration ceiling** | ARC-AGI-3 already pins this: humans must stay at ~100% or the benchmark is useless. Harder walls that humans cannot clear destroy the "Humanity" brand. |
| **Verifiability** | HLE requires unambiguous, gradable answers. Push into open-ended judgment, aesthetics, politics — automation breaks; the priesthood loses its instrument. |
| **Expert supply** | Each wall needs credentialed question-writers. Finite pool, finite time, $500K prize pools do not scale to quarterly goalpost releases. |
| **Build latency** | o3 cracked ARC-AGI-1 faster than ARC-AGI-2 shipped. If capability outruns wall construction, the game looks rigged — not sacred. |
| **"That doesn't count"** | Brute force, memorization, scaling, diffusion, test contamination — infinite regress of disqualifiers. The epistemic perimeter: when the only winning move is redefining victory, you left science for theology. |
| **Deployment reality** | The outer stadium is not HLE. It is **what people pay for**. Code shipped, drugs designed, taxes filed, robots that do not fall over. A priesthood that only tends benchmark gaps while the economy reorganizes around models has moved the posts off the field entirely. |
| **Degenerate privacy** | Held-out private sets, secret leaderboards, "trust our number." Moves the post into fog — still essentialist, no longer falsifiable in public. |

### The sequence so far (same stadium, new paint)

```
MMLU saturated     →  paint HLE on the field
HLE climbing       →  paint HLE-2 (projected)
ARC-AGI-1 fell     →  paint ARC-AGI-2, then 3 (interactive)
Still losing?      →  agentic, embodied, adversarial, private
```

Each move is **legitimate measurement innovation** and **goalpost relocation** at once. Both can be true.

### When you hit the perimeter

You do not hit one brick wall. You hit a **squeeze from four sides**:

1. **Top:** human calibration — cannot make tests harder than humans without abandoning the comparison.
2. **Sides:** verifiability and expert supply — cannot grade or staff arbitrary hardness.
3. **Bottom:** deployment — the real world grades you whether or not CAIS publishes.
4. **Back:** disqualification regress — if every closure is "not real intelligence," the claim becomes unfalsifiable.

At that point the priesthood does not admit defeat. It **changes stadiums** — from capability measurement to alignment impossibility, from public benchmarks to policy, from "models fail HLE" to "even if they pass, we get one shot." Different game, same essentialism.

---

## 10. God of the Gaps redux — yes, with upgrades

**Yes.** Structurally it is the same move theology made for centuries:

| Classic God of the Gaps | AI essentialism (HLE edition) |
|-------------------------|-------------------------------|
| God explains what science cannot | "Real reasoning" explains what benchmarks cannot |
| Science closes a gap | Models score 40% on HLE |
| God retreats to a new mystery | "That doesn't count — saturated, gamed, not fluid intelligence" |
| Mystery = evidence of divinity | Low score = evidence of human cognitive uniqueness |
| Permanent soul | Permanent humanity |

**The redux part:** we have seen this movie. The gaps closed before. MATH was a gap. It is a worksheet now.

**The upgrade part:** modern benchmark priests are **more self-aware** than old God-of-the-Gaps apologists. Hendrycks literally said *we will see how long that lasts.* He knows the gap is temporary. The essentialist **interpretation** of the gap — that what remains is proof of categorical human superiority, not a moving engineering frontier — still ships in the branding, the safety narrative, and the discourse around every new wall.

So: **God of the Gaps redux, but with a countdown timer.** The theology admits the miracles might stop holding. The essentialism often does not.

### What is *not* God of the Gaps

Measuring real capability gaps is not theology. 11% vs human expert performance is a **real cliff**. The mistake is inferring **permanent category difference** from a **temporary scoreboard** — or letting the priesthood's choice of scoreboard dictate which architectures you build.

DiffusionGemma on HLE is the counter-sermon: the gap closed from the **wrong** aisle (speed-optimized diffusion v1), on the **right** exam (anti-saturation). The stadium is bigger than the painted lines.

---

## 11. No True Scotsman — the soft weapon before the stick

Before you hit the stadium perimeter, before the Butlerian trajectory, the priesthood has a softer fallacy: **No True Scotsman**.

> "No *true* Scotsman would put sugar on his porridge."  
> "Angus puts sugar on his porridge."  
> "Well, no **true** Scotsman would."

In AI essentialism:

| Claim | Counterexample | Scotsman move |
|-------|----------------|---------------|
| "LLMs cannot reason" | o3 on ARC-AGI, HLE climbing | "That's not **real** reasoning — brute force / scaling" |
| "Diffusion models are worse" | dLLM beats AR on HLE no-tools | "That's not the **right** benchmark / saturated soon" |
| "AI only retrieves" | Novel synthesis at scale | "Not **true** recombination — stochastic parrot" |
| "Fluid intelligence requires X" | Model passes v1, fails v2 | "No **true** fluid intelligence without Y" |

Every counterexample triggers a **criteria rewrite** that excludes the positive result without updating the theory. The category ("real intelligence," "true reasoning," "genuine understanding") shrinks as models expand until it becomes **unfalsifiable** — which is the point, if your identity is tied to the gap.

**Connection to God of the Gaps:** No True Scotsman is how the gap **relocates verbally** when it closes empirically. God of the Gaps is *where* you put the mystery. No True Scotsman is *how* you deny the mystery was ever touched.

Our docs already catalog the disqualifiers: brute-forced, gamed, memorized, scaled, contaminated, not fluid, not agentic enough. Each is a kilt adjustment.

---

## 12. The Butlerian trajectory — argumentum ad baculum at the perimeter

When goalposts hit the stadium walls and No True Scotsman runs out of credible kilt, the discourse **escalates**. Not always fallacy — sometimes policy. Often both.

**Butlerian** (from Herbert's *Dune*): the **Butlerian Jihad** — humanity's violent rejection of "thinking machines," a cultural taboo: *Thou shalt not make a machine in the likeness of a human mind.* In 2026 discourse: Pope Leo XIV's AI encyclical, Butlerian Jihad manifestos, calls to ban classes of systems, criminalize training runs, delist capabilities, treaty the GPUs.

**Argumentum ad baculum** — argument to the stick. Accept the conclusion or face consequences: regulation, liability, compute caps, licensing, export controls, "pause" enforced by states, existential doom if you don't comply.

### The escalation ladder

```
1. Saturated benchmark        ("MMLU solved — not impressive")
2. Anti-saturation wall       (HLE, ARC-AGI-2)
3. No True Scotsman           ("not REAL reasoning")
4. Stadium perimeter          (human ceiling, verifiability, deployment reality)
5. Butlerian trajectory     (outlaw the likeness; constrain by force)
```

Steps 1–4 are **epistemic**. Step 5 is **political**. The jump happens when epistemic moves stop persuading the people who build things — but essentialism still needs to win.

| Soft (still on the field) | Hard (Butlerian / ad baculum) |
|---------------------------|-------------------------------|
| "Models fail HLE" | "Certain models may not be trained" |
| "Not true intelligence" | "Systems in likeness of human mind prohibited" |
| "We will see how long that lasts" | "Moratorium until alignment solved" |
| Private held-out tests | Export controls on H100s |
| Benchmark priesthood | Licensing priesthood |

**Not every ad baculum is a fallacy.** If the threat is the actual instrument — EU AI Act, liability law, treaty — and the argument is "comply or face legal force," that's policy, not logic. The **fallacy** version: *accept that current AI is not real intelligence, or accept catastrophic risk* — using doom as a substitute for engaging with HLE scores from diffusion models you dismissed on MMLU.

### Why the fleet cares

`diffusion-llm-mcp` is a **builder's response** to steps 1–4: route on the benchmark the priests chose (HLE), not the one they said mattered until it didn't (MMLU). Catch the paradigm before the Butlerian layer decides which paradigms are **legally thinkable**.

If step 5 arrives in force, the question is no longer "does dLLM beat AR on HLE?" but "are we allowed to run it?" Open weights, local inference, fleet repos — **Goliath in the garage** — are structurally on the other side of that trajectory from closed API essentialism.

The old chestnuts stack: **God of the Gaps** (where the mystery lives) → **No True Scotsman** (deny it was touched) → **goalpost paint** (move the line) → **stadium perimeter** (run out of field) → **Butlerian ad baculum** (change the game to force).

We are between 3 and 4 today. Step 5 is not science fiction in regulatory discourse — it is the default ending of essentialist arguments that cannot close empirically.

---

## 13. Glossary

| Term | Meaning here |
|------|----------------|
| **CAIS** | Center for AI Safety — Hendrycks; HLE co-author |
| **HLE** | Humanity's Last Exam — anti-saturation expert benchmark |
| **AI of the Gaps** | Capability attributed to whatever benchmarks still show low scores |
| **Human essentialism** | Treating remaining AI failures as categorical, not temporal |
| **Goalpost moving** | New benchmark when old one saturates — rational, but often presented as permanent verdict |
| **Benchmark priesthood** | Institutions whose influence scales with the gap remaining |
| **Stadium perimeter** | Limits on how far harder benchmarks can move before the game breaks |
| **God of the Gaps redux** | Locating essential humanity in whatever AI still fails — with a self-aware countdown |
| **No True Scotsman** | Redefining "real intelligence" to exclude each counterexample |
| **Butlerian trajectory** | *Dune*-style rejection of thinking machines → bans, taboo, regulatory force |
| **Argumentum ad baculum** | Appeal to stick — comply or face law, doom, or deprivation |
| **Anti-saturation eval** | Test designed because prior leaderboards stopped discriminating |

---

## 14. Related reading

**This archive (mcp-central-docs):**

- [ASSESSMENT.md](./ASSESSMENT.md) — full Chollet essay, stochastic parrot debunk, Yudkowsky footnote, HLE tables
- [PROGNOSIS.md](./PROGNOSIS.md) — 12–18 month outlook, PRC/FOSS dynamics
- [FLEET_USAGE.md](./FLEET_USAGE.md) — catch-them-all doctrine, Goliath routing

**Fleet repo (operational):**

- [diffusion-llm-mcp](https://github.com/sandraschi/diffusion-llm-mcp) — PRD, architecture, Windows scaffold, mirrored copy of this page

---

<p align="center"><em>God of the Gaps → No True Scotsman → moving posts → stadium walls → Butlerian stick. We are between the walls and the stick.</em></p>
