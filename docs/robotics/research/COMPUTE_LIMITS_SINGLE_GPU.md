# Compute Limits: What a Single 4090 Cannot Do (That Matters)
## Practical Analysis for AI Research on Consumer Hardware

**Created:** 2026-03-08  
**Status:** REFERENCE / ANALYSIS  
**Context:** Goliath server — 24-core AMD, 64GB RAM, RTX 4090 (24GB VRAM)  
**Related:** `THE_PRELOADED_MIND.md`, `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md`

> *The question: is there a useful AI activity that needs orders of magnitude more compute — not slowly, but qualitatively out of reach?*  
> *The framing matters: "useful" excludes training another frontier LLM (there are plenty already), re-running Waterloo in Resonite (no one wants this), and other academically interesting but practically irrelevant scale problems.*
> *Focus: what would you actually want to do, that you actually can't?*

---

## 1. The Hardware

| Spec | Value |
|------|-------|
| BF16 compute | ~82 TFLOPS |
| VRAM | 24 GB |
| Memory bandwidth | ~1 TB/s |
| System RAM | 64 GB (useful for CPU offload) |
| GPU vs H100 | ~24× slower at matrix math |

Gap between Goliath and a serious training cluster: **6–8 orders of magnitude** in effective compute. This is relevant for training; mostly irrelevant for inference and experimentation.

---

## 2. The Key Asymmetry: Training vs. Inference

The most important fact about the 4090 in the current AI landscape:

**You can run the output of 10²⁶ FLOP of training on it. You cannot reproduce that training.**

This is the pre-loaded mind principle applied to compute. GPT-4, Qwen-72B, Llama-3-70B — models trained with hundreds of millions of dollars of compute — run on your 4090 via quantization. The trained knowledge is accessible. The training process is not reproducible locally, and there is no reason to want to reproduce it.

Training another LLM from scratch is therefore correctly excluded from the problem space. There are already more good trained models than anyone has use for.

---

## 3. What's Actually Interesting and Compute-Limited

### 3.1 Multi-Agent Self-Play in Resonite — The Dojo Problem

**The scenario:** Two LLM-driven avatars in a Resonite dojo. They fight, they lose, they learn. Over time they develop distinct fighting styles, exploit each other's weaknesses, build skill repertoires. This is actually interesting.

**What it requires:**
- Two agents running simultaneously, each with their own model instance
- Each agent needs: action selection (fast, <500ms for fluid combat) + reasoning/learning (slow, deliberative)
- A shared world state they both read and write
- A learning signal: what worked, what didn't, how to update behavior
- Enough iterations to see actual skill development (hundreds to thousands of rounds)

**What the 4090 can do:**
Running two 7B model instances simultaneously: ~14GB — fits in 24GB. Workable. Latency for action selection at 7B: 200–500ms, acceptable for turn-based or slow-paced combat.

**Where it breaks:**
- **Quality floor:** 7B models produce noticeably worse tactical reasoning than 70B models. The "learning" may be shallow pattern matching rather than genuine strategy development.
- **Learning loop compute:** Updating behavior from experience requires either: (a) in-context learning (works, but resets each session), (b) LoRA fine-tuning between rounds (takes minutes per update — breaks combat pacing), or (c) external memory + retrieval (feasible, this is the right approach).
- **Simultaneous 70B agents:** Two Qwen-72B instances = ~80GB VRAM. Impossible on 24GB. The interesting high-quality version requires either quantization compromise or a multi-GPU setup.

**Practical path:** Hybrid architecture — 7B fast models for in-combat action selection, 70B deliberative model (CPU offload, slower) for post-round analysis and skill update. The dojo works. It's just not running both agents at full quality simultaneously.

**What would need 10× more compute:** Two agents, each running a 70B model, at reactive latency (<200ms), with continuous RL-style skill updating between rounds. This needs ~4× H100 minimum. Genuinely interesting, genuinely out of reach.

---

### 3.2 Real-Time Embodied Agent with Full Perception

**The scenario:** Rovo (the physical Yahboom robot) with:
- VLM continuously processing camera feed (~10 fps)
- Full 70B reasoning model for decision-making
- <500ms latency for reactive behavior (avoid obstacles, respond to Benny)

**Memory arithmetic:**
```
LLaVA-34B (VLM, Q4):   ~20 GB VRAM
Qwen-72B (reasoning, Q4): ~40 GB VRAM
Total required:           ~60 GB VRAM
4090 available:           24 GB VRAM
```

This is not a speed problem. 24GB cannot hold 60GB. Not even slowly.

**What actually works on the 4090:**

| Config | VRAM | Action latency | Quality |
|--------|------|----------------|---------|
| LLaVA-7B + Qwen-7B simultaneous | ~8 GB | <500ms | Acceptable for slow robot |
| LLaVA-13B + Qwen-13B simultaneous | ~16 GB | 500ms–1s | Good |
| Qwen-72B alone (Q4, CPU offload) | ~24 GB | 3–8s | High, deliberative only |
| LLaVA-34B + Qwen-72B simultaneous | ~60 GB | impossible | — |

**Practical conclusion:** The Rovo architecture is designed around this constraint. Small-fast model for reactive decisions, larger model for deliberative reasoning with acceptable latency. Not a compromise — a design choice forced by hardware that turns out to produce better architecture anyway (matches how biological cognition works: fast System 1 + slow System 2).

**What would need 10× more compute:** Full-quality real-time embodied reasoning. This is what Google DeepMind runs for their robotics research. 8×H100 minimum for serious work.

---

### 3.3 Large-Scale Molecular / Drug Screening

This one is less personally relevant but genuinely illustrates the compute gap.

**Single prediction:** AlphaFold3 for one protein structure — minutes to an hour on a 4090. Entirely feasible.

**The useful scientific work:**
- All mutations of a protein family: ~10⁶ variants → months on the 4090
- Proteome-scale interaction screen: ~10⁹ pairs → centuries
- Drug candidate vs. target (iterative): effectively intractable

This is the most dramatic example of "not even slowly" for a genuinely useful task. A single 4090 can do meaningful research (one protein, a small family). It cannot do what a pharmaceutical company's AI pipeline does (10⁹ candidates screened in hours). The gap isn't engineering — it's physics.

**Relevance to the project:** If the Ednaficator or any of the health-adjacent projects ever needed molecular work, this is where the ceiling is.

---

### 3.4 Massively Parallel RL Training (Robot or Game Agent)

**What's needed for serious RL:** 10,000–100,000 parallel environment instances running simultaneously. Each instance has state, physics, rendering. The RL signal comes from aggregate experience across all instances.

**The memory wall:** Holding 50,000 parallel Mujoco environments in GPU memory requires hundreds of GB of VRAM simultaneously. 24GB cannot hold the state. This is not a speed problem — it's architectural. You can run 1 environment, or 10. You cannot run 50,000.

**Why this matters for the dojo scenario:** If you want the two Resonite bots to learn via genuine RL (not just LLM reasoning), you'd ideally run thousands of parallel dojo simulations and aggregate the signal. This is how AlphaGo / AlphaZero worked. On the 4090, you run one simulation at a time. Learning is much slower, requiring either very long runtime or a different approach.

**Practical path:** Use LLM reasoning + episodic memory as the learning mechanism instead of RL. The bots remember what worked, reason about it, and update behavioral intentions. Slower convergence to skill than RL, but doesn't require parallel simulation. This is what the cognitive architecture doc already proposes.

---

### 3.5 The Inference Scaling Frontier

Recent work (2024–2025) established that generating many candidate solutions and verifying them scales performance dramatically — "coverage" (fraction of hard problems solved) scales log-linearly with sample count over four orders of magnitude.

For hard coding problems, mathematical proofs, or scientific reasoning: generating 10,000 candidate solutions and picking the best one reliably outperforms one careful attempt with a larger model.

**On the 4090:** You can generate 100 candidates in reasonable time. 10,000 takes 100× longer — hours to days depending on problem and model size. Labs running inference scaling use thousands of GPUs in parallel, getting 10,000 candidates in the same time you'd get 1.

**Where this matters for the project:** For difficult reasoning tasks (complex code generation, hard debugging, scientific analysis), there's a quality ceiling on the 4090 that isn't about model size — it's about how many reasoning attempts you can practically run. This is addressable by overnight batch runs but not real-time.

---

## 4. Summary: What Actually Matters

| Task | 4090 Status | Practical path |
|------|-------------|---------------|
| LLM inference (≤13B, real-time) | ✅ Fully capable | Direct use |
| LLM inference (70B, deliberative) | ✅ With latency | CPU offload via llama.cpp |
| Fine-tuning 7–13B (LoRA/QLoRA) | ✅ Fully capable | Standard workflow |
| Resonite dojo (7B agents) | ✅ Workable | 2× 7B fits in 24GB |
| Resonite dojo (70B agents) | ⚠️ Compromised | Sequential or CPU offload |
| Resonite dojo (70B + real-time RL) | ❌ VRAM wall | Need multi-GPU |
| Rovo: small VLM + small LLM | ✅ Real-time capable | 7B+7B fits fine |
| Rovo: large VLM + large LLM | ❌ VRAM wall | ~60GB needed |
| Single protein prediction | ✅ Feasible | Minutes–hours |
| Proteome-scale screening | ❌ Time scale | Centuries |
| 50,000-instance RL training | ❌ Memory architecture | Can't hold state |
| Inference scaling (100 samples) | ✅ Practical | Hours max |
| Inference scaling (10,000 samples) | ⚠️ Overnight batch | Not real-time |
| Training another frontier LLM | N/A | Nobody should want this |

---

## 5. The Dojo in More Detail

Since this is the most concretely interesting scenario:

**Two LLM bots fighting in Resonite, developing genuine skills over time.**

Architecture that works on the 4090:

```
Bot A (attacker archetype)          Bot B (defender archetype)
    |                                    |
 Qwen-7B (action, ~500ms)           Qwen-7B (action, ~500ms)
    |                                    |
 Episodic memory (SQLite)           Episodic memory (SQLite)  
    |                                    |
 Skill library (retrieval)          Skill library (retrieval)
    |                                    |
    +------------- Resonite world state ----+
                        |
              Post-round analysis
              (Qwen-72B via CPU offload, ~10s)
                        |
              Update both skill libraries
              Update behavioral intentions
```

Both bots run simultaneously on separate 7B instances during combat (fast). After each round, a single 72B model instance (slow, CPU-offloaded) analyzes what happened and writes updates to both skill libraries. This is the Doer/Observer architecture from the cognitive doc applied to competitive learning.

**What you'd see over time:**
- Round 1–10: Generic behavior, lots of mistakes
- Round 50–100: Recognizable styles starting to emerge (Bot A rushes, Bot B circles)
- Round 200–500: Actual counter-strategies developing as each bot's skill library accumulates
- Round 1000+: Whether genuine skill or just converged patterns depends on whether the episodic memory + reasoning approach produces real generalization

The honest answer is: we don't know if this produces genuine skill development or sophisticated-looking pattern memorization. That's actually the interesting research question, and the 4090 is entirely sufficient to run it and find out.

**What would need 10× more compute:** Running both bots at 70B quality with real-time reactive latency, plus simultaneous RL fine-tuning between rounds. This is what a well-resourced lab would do. It would produce faster and higher-quality skill development. It's not necessary to run the experiment — just to run it faster and at higher quality.

---

*Tags: [compute, hardware, 4090, resonite, dojo, multi-agent, robotics, embodied-ai, reference, medium]*
