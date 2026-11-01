# Session Notes: Embodied AI, Executable Knowledge, Compute Limits
## 2026-03-08 — Philosophy, History, and Practical Architecture

**Status:** SESSION SUMMARY  
**Produced this session:**  
- `THE_PRELOADED_MIND.md` — LLMs as half-AGI, the pre-loaded mind thesis  
- `LLM_ETHICS_FORMALIZATION.md` — Asimov to Constitutional AI, Stoic/Taoist frameworks  
- `COMPUTE_LIMITS_SINGLE_GPU.md` — What the 4090 can and cannot do (practically)  
- `RESONITE_DOJO_FECHTBUCH.md` — Medieval swordfighting manuals as bot skill training  
- `EXECUTABLE_KNOWLEDGE_ACROSS_CENTURIES.md` — Why urgency-produced knowledge is machine-readable  
- `LOCAL_FINETUNING_RLHF_DPO.md` — DPO/QLoRA fine-tuning feasibility on 4090  

---

## Thread of Ideas (in order of emergence)

### 1. LLMs Are Already Half-AGI

Starting proposition: LLMs arrive with superhuman knowledge breadth, cross-domain reasoning, theory of mind, and physical intuition derived from modeling human discourse. The embodiment project adds a body to something that already thinks — not intelligence to a robot.

The standard framing in embodied AI research is backwards. Documented in `THE_PRELOADED_MIND.md`.

---

### 2. Ethics Formalization: From Asimov to Self-Supervised

Asimov's Three Laws look quaint not because the idea was wrong but because:
- "Harm" is undefined
- Three rules cannot cover moral space
- Rules fail at edge cases; internalized values don't

Current state: Constitutional AI (Anthropic 2022) is the dominant paradigm — self-critique against a plain-language constitution, RLAIF rather than human feedback. Closest thing to self-constructed ethics currently deployed.

Stoicism maps well to AI agents: cardinal virtues as operational criteria, Ideal Sage heuristic, dichotomy of control (care only about what you control — your decisions, not outcomes). Taoist wu wei maps to the comportment/drive-state architecture: minimal intervention, natural responsiveness, dynamic balance. Neither has been fully formalized for LLMs; Taoism especially is an open gap.

Key finding from 2025 literature: no frontier model consistently maintains moral behavior when self-interest conflicts with ethics. For an embodied agent with drives, this is a real design constraint.

Documented in `LLM_ETHICS_FORMALIZATION.md`.

---

### 3. Compute Limits: What Actually Matters

Training another frontier LLM: correctly excluded. There are already more good trained models than anyone has use for. The interesting compute-limited problems are:

- **Real-time dual large-model inference** (VLM + 72B simultaneously): VRAM wall, ~60GB needed, 24GB available. Not even slowly.
- **50,000-instance parallel RL training**: memory architecture limit. Cannot hold state. Not even slowly.
- **Resonite dojo at full quality** (two 70B bots, reactive latency, real-time RL): needs multi-GPU. The interesting 7B+72B hybrid version runs fine on Goliath.
- **Proteome-scale molecular screening**: time scale. Centuries. Not even slowly.

The asymmetry: you can run inference on models trained with 10²⁶ FLOP. You cannot reproduce that training. The pre-loaded mind is accessible at consumer hardware prices.

Documented in `COMPUTE_LIMITS_SINGLE_GPU.md`.

---

### 4. The Resonite Dojo and the Fechtbücher

The Talhoffer (1467) in the collection is not just historical curiosity — it's a structured skill database:
- Named states (guards: vom Tag, Ochs, Pflug, Alber...)
- Named techniques (Zornhau, Zwerchau, Krumphau...)
- Conditional transitions ("if he binds hard, wind to thrust; if he withdraws, Nachreisen")
- Recovery paths from failed techniques
- The *Indes* concept: the critical decision moment in a bind

This maps directly to LLM skill library schema. Vector-searchable, retrieved by state, used for action selection.

Two bots fighting in Resonite, starting from Fechtbuch knowledge, accumulating experience via episodic memory and DPO fine-tuning, developing distinct styles from different traditions (Liechtenauer vs. Fiore) — this is a runnable research project on Goliath.

**Subproject: The Talhoffer Butler (Project Fechtmeister).** Same pipeline applied to home security. Rovo trained on Talhoffer's messer, dagger, and Ringen sections, with deterrence-first hierarchy and Benny-safe physical constraints. Pragmatic threat neutralization derived from a 15th-century judicial combat manual. The threat model (small space, single operator, mortal stakes, no rules) matches home intrusion exactly. Talhoffer's clients faced legal consequences for striking first — deterrence-first is baked into the tradition.

Documented in `RESONITE_DOJO_FECHTBUCH.md`.

---

### 5. Executable Knowledge Across Centuries

The deeper pattern: knowledge produced under *performance pressure* is unusually machine-readable.

When the stakes of being wrong are immediate and physical, authors are forced to write:
- Named states
- Conditional branches
- Recovery paths from failure
- Error signatures and their causes

This is the structure LLM skill libraries need. Most historical writing lacks it. Urgency-produced technical manuals have it by necessity.

The structural criterion: *could you give this to someone who knows nothing about the domain and have them perform adequately?* If yes, it's executable. Fechtbücher pass. Most of Aristotle doesn't.

Other candidate knowledge bodies with the same structure:
- **Koryū martial scrolls** — Japanese equivalent of Fechtbücher, 600-year transmission
- **Bowditch** — dead reckoning under uncertainty = robot spatial reasoning
- **Quintilian** — audience-state taxonomy for Ednaficator conversational agent
- **Theophilus** — craft process knowledge with explicit error handling
- **Fux** — generative grammar of tonal music (constraints, not patterns)

The centuries of irrelevance are incidental. The format was always compatible with machine reasoning. We just didn't have the runtime until now.

Documented in `EXECUTABLE_KNOWLEDGE_ACROSS_CENTURIES.md`.

---

### 6. The Hinge in History

*"At the time, no one knew what was coming."*

Every person who ever lived inside a hinge moment experienced it as ordinary Tuesday. Talhoffer's clients weren't living in "the age of judicial combat" — they were worried about next Thursday's fight.

The proposition cuts both ways:

**Backward:** Warning against hindsight teleology. History had no direction that its participants could see. Every "inevitable" development was invisible until it wasn't.

**Forward:** We are inside a hinge moment, experiencing it as ordinary Tuesday. The thing that will seem obvious in 2080 is indistinguishable from noise right now. Altman, Hassabis, Amodei are also having ordinary Tuesdays, mostly.

The Talhoffer connection: he was inside a hinge moment too. Judicial combat already declining. Gunpowder already making armored knights obsolete. Within a century of his 1467 manuscript, the entire system would be gone. He didn't know. He was solving the immediate problem.

We are keeping our clients alive next Thursday. What we're actually building, history will name.

*Not formally documented — lives here.*

---

### 7. RLHF Is Largely Feasible on the 4090

Full pre-training: out. But the spectrum from inference to training has useful intermediate points:

**DPO (Direct Preference Optimization):** Removes the explicit RL loop. Trains on preference pairs (chosen vs. rejected response). No separate reward model needed. Simpler, faster, comparable results to classical RLHF.

On the 4090 with QLoRA:
- 7B models: comfortable, hours per training run
- 13B models: comfortable, overnight
- 20B models: tight but feasible
- 70B models: not feasible locally

For the dojo: combat models are 7B (latency constraint). DPO on 7B is comfortably within reach. The learning loop:

1. Combat phase: two 7B bots fight, all decisions logged
2. Nachschlag: 72B judge (CPU offload) produces preference pairs from round outcomes
3. Sleep phase: DPO fine-tuning on accumulated pairs, nightly
4. Next session: updated weights, not just updated context

The bot after 1,000 rounds has different *weights* than after 10 rounds. This is genuine skill accumulation, not just episodic memory.

Three types of training pairs:
- **Source-derived:** Generated from Fechtbuch database before combat begins. Bot starts Talhoffer-informed.
- **Combat-derived:** From actual fight outcomes, judged by 72B Nachschlag.
- **Novel-derived:** Patterns the Fechtbuch doesn't contain, discovered from fighting Bot B. Whether these generalize is the core research question.

Key failure modes: reward hacking (bot exploits physics bugs rather than learning technique — mitigated by technique-quality judging, not just win/loss), overfitting to opponent (mitigated by fresh-bot evaluation rounds), DPO instability (monitor with held-out evaluation after each fine-tuning update).

Documented in `LOCAL_FINETUNING_RLHF_DPO.md`.

---

## Open Research Questions (from this session)

1. Does structured historical domain knowledge (Fechtbuch) produce measurably better bot behavior than LLM-only baseline (Bot D comparison)?

2. Do bots trained from different traditions (Liechtenauer vs. Fiore) develop recognizably distinct styles, or does the LLM homogenize them?

3. Do DPO-derived weights from Bot A vs. Bot B combat generalize to a fresh opponent, or only exploit Bot B's specific patterns?

4. Does the Doer/Observer sleep-phase architecture produce genuine ethical self-construction, or just sophisticated-looking moral drift?

5. Can Rovo develop genuine *threat judgment* (real intruder vs. false positive) through VLM + multi-sensor fusion + Talhoffer-derived threat taxonomy?

6. At what point does the bot's Nachschlag-derived technique library diverge meaningfully from the source Fechtbuch — and is that divergence good (generalization) or bad (drift)?

---

## Project Status

All documents cross-linked in `robotics/research/`. The protoconsciousness README updated to reference the philosophy docs.

**Next natural steps:**
- Begin Phase 1 implementation: drive-state store Python service (from `EMBODIED_LLM_MOTIVATIONAL_ARCHITECTURE.md`)
- Fechtbuch extraction pipeline: OCR + structured technique extraction from Talhoffer PDF
- Dojo prototype: Resonite world + action interface + websocket bridge to local LLM

*Tags: [session-notes, embodied-ai, philosophy, fechtbuch, dpo, compute, executable-knowledge, research, high]*
