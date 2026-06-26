# Local Fine-Tuning on the 4090: RLHF, DPO, and the Dojo Learning Loop
## What's Actually Feasible for Skill Training on Consumer Hardware

**Created:** 2026-03-08  
**Status:** TECHNICAL REFERENCE  
**Related:** `COMPUTE_LIMITS_SINGLE_GPU.md`, `RESONITE_DOJO_FECHTBUCH.md`

> *Full pre-training: out. RLHF-style fine-tuning: largely in, with caveats.*  
> *The 4090 with 24GB VRAM can run meaningful preference learning on models up to ~20B.*

---

## 1. The Spectrum from Inference to Training

There is no binary between "pure inference" and "full training." The relevant spectrum:

```
INFERENCE ONLY          SOFT ADAPTATION         HARD ADAPTATION         FULL TRAINING
(no weight change)      (no weight change)       (weight change)         (weight change)
      |                       |                        |                       |
System prompt           RAG / retrieval          LoRA / QLoRA            Pre-training
Episodic memory         Skill library            DPO / RLAIF             From scratch
Inner monologue         In-context learning      Full fine-tune (SFT)
      |                       |                        |                       |
  Always feasible        Always feasible          Feasible on 4090        Not feasible
  on 4090                on 4090                 up to ~20B              (38,000 years)
```

The dojo architecture as currently designed lives in the left two columns. The question is whether we can push it into the third column — actually updating model weights from combat experience.

---

## 2. The Techniques: What They Actually Are

### SFT — Supervised Fine-Tuning
Train on (input → correct output) pairs. "Here are 500 examples of good swordfighting decisions. Learn to produce these." Straightforward, stable, well-understood. Requires curated labeled data.

### LoRA — Low-Rank Adaptation
Instead of updating all model weights (billions of parameters), insert small adapter matrices into the attention layers and train only those. ~0.1–1% of parameters. Result: dramatically lower VRAM, comparable quality to full fine-tuning for most tasks.

Fine-tuning a 20B model on a 24GB consumer GPU is possible via LoRA + quantization. This is demonstrated, not theoretical.

### QLoRA — Quantized LoRA
Run the frozen base model in 4-bit quantization (NF4), train only LoRA adapters in full precision. Halves the VRAM again vs. LoRA alone. Enables fine-tuning of 7B–13B models on 8GB GPUs; 70B models on 48GB setups. On the 4090 (24GB): 7B–20B range comfortably, 34B with care.

### DPO — Direct Preference Optimization
The most practically important development. Classical RLHF requires: base model + reward model + reference model + PPO training loop — four models in memory simultaneously, complex and fragile. DPO eliminates the reward model entirely, training directly on preference pairs (chosen response vs. rejected response) using a simpler binary cross-entropy loss.

DPO removes the explicit RL loop, is simpler, faster, and produces comparable results to classical RLHF in most scenarios.

For the dojo: "Bot chose action X, lost the exchange. Bot chose action Y in the same situation, won. Prefer Y." This is a DPO training pair. The post-round Nachschlag analysis generates these pairs automatically.

### RLAIF — RL from AI Feedback
Replace human preference annotators with another LLM acting as judge. The judge evaluates outputs and produces the preference signal. For the dojo this is natural: the fight outcome is the ground truth (win/lose), and the 72B analysis model can produce richer preference annotations ("action Y was better because it exploited the opponent's habitual guard drop after Zwerchau").

### GRPO / REINFORCE++ (2024–2025)
Newer RL algorithms that are more stable than PPO for LLM fine-tuning. DeepSeek-R1 was trained with GRPO. More memory-efficient than PPO. OpenRLHF implements PPO, REINFORCE++, GRPO, RLOO and supports multi-agent systems via the MARTI fork. Single-GPU support exists for smaller models.

---

## 3. What the 4090 Can Run

### Feasible (comfortable):

| Task | Model size | VRAM used | Time estimate |
|------|-----------|-----------|---------------|
| QLoRA fine-tune | 7B | ~10 GB | Hours per dataset |
| QLoRA fine-tune | 13B | ~16 GB | Hours–overnight |
| DPO on preference pairs | 7B | ~12 GB | Hours |
| DPO on preference pairs | 13B | ~18 GB | Overnight |
| SFT (LoRA) | 7B | ~10 GB | Hours |
| SFT (LoRA) | 20B | ~22 GB | Overnight |

### Feasible (tight):

| Task | Model size | VRAM used | Notes |
|------|-----------|-----------|-------|
| QLoRA fine-tune | 20B | ~22 GB | Tight, reduce batch size |
| DPO | 20B | ~22 GB | Tight |
| Classical RLHF (PPO) | 7B | ~22 GB | Needs base + reward model + reference |

### Not feasible on 24GB:

| Task | Why |
|------|-----|
| DPO on 70B | ~80GB needed even quantized |
| Classical RLHF on 13B+ | 3 model instances simultaneously |
| Any fine-tuning of 34B+ | VRAM wall |

**Practical conclusion:** DPO on 7B–13B models is comfortably within reach. This covers the dojo combat models exactly. The 72B post-round analysis model cannot be fine-tuned locally — but it doesn't need to be, since it's playing the judge/observer role, not the agent role.

---

## 4. The Dojo Learning Loop with DPO

The full architecture with actual weight updates:

```
COMBAT PHASE (runtime, both bots)
    ↓
Two Qwen-7B instances run combat
Each action logged: [state, guard, distance, action_chosen, outcome]
    ↓
ROUND END

NACHSCHLAG PHASE (post-round, ~30 seconds)
    ↓
Qwen-72B (CPU offload) analyzes full round log
For each significant decision point, produces:
  - chosen: the action that worked / should have been taken
  - rejected: the action that failed / was suboptimal
  - reasoning: why (for episodic memory)
Output: preference pairs dataset (appended to rolling dataset)
    ↓
SLEEP PHASE (nightly or after N rounds)
    ↓
DPO fine-tuning run on accumulated preference pairs
  - Base: Qwen-7B (combat model)
  - Dataset: preference pairs from last N rounds
  - Method: QLoRA + DPO
  - Duration: 1–4 hours on 4090
  - Result: updated LoRA adapter, merged or kept separate
    ↓
NEXT SESSION: bot runs with updated weights
```

This is a genuine learning loop with weight updates. The bot after 1,000 rounds is not the same model as after 10 rounds — it has different weights, not just different context.

### Data volume reality check

For DPO to produce meaningful updates:
- Minimum viable: ~200–500 preference pairs
- Good signal: 1,000–3,000 pairs
- At ~10–20 significant decision points per round: 50–150 rounds to minimum dataset

So the first fine-tuning run happens after roughly 50–150 rounds of combat, with nightly updates thereafter. This is a realistic timeline.

---

## 5. The Fechtbuch Integration

DPO pairs derived from Fechtbuch knowledge vs. combat experience:

**Type A — Source-derived pairs (bootstrap dataset):**
Generated before combat begins. For each technique in the database, generate scenarios where it's the correct choice vs. alternatives.

```python
# Example DPO pair
{
  "prompt": "You are in Alber (fool's guard). Opponent strikes Oberhau. Distance: measure.",
  "chosen": "Execute Zornhau — the master strike that defeats the upper strike",
  "rejected": "Retreat to vom Tag — surrenders initiative, opponent presses advantage"
}
```

500–1,000 such pairs can be generated from the Fechtbuch database before the first combat round. The bot starts with Talhoffer-informed weights, not a blank slate.

**Type B — Combat-derived pairs (ongoing):**
Generated by Qwen-72B Nachschlag from actual fight outcomes. Bot A tried Absetzen (deflect and thrust) at close distance, got hit. Should have transitioned to Ringen (grappling). That's a pair.

**Type C — Novel-derived pairs (emergent):**
Bot A discovers that Bot B consistently drops its guard after a particular sequence. The Nachschlag notes this: "After Zwerchau → Zwerchhau repetition, opponent predictably shifts to Alber. Exploit with immediate Nachreisen." This pattern isn't in the Fechtbuch — it's learned from Bot B specifically. Whether it generalizes is the research question.

---

## 6. Caveats and Known Failure Modes

**Catastrophic forgetting:** Fine-tuning on combat data may degrade the model's general capabilities. Mitigations: LoRA (doesn't touch base weights), careful learning rate, merge-and-test before deployment.

**Reward hacking:** If the reward signal is "win the round," the bot may learn to exploit bugs in the Resonite physics or the combat interface rather than learning genuine technique. Mitigation: the 72B judge evaluates *technique quality* not just outcome. "Bot won by getting the opponent stuck in geometry — rejected. Bot won with clean Zornhau counter — chosen."

**Overfitting to opponent:** Bot A fine-tuned against only Bot B learns Bot B's specific patterns, not general swordfighting. Mitigation: periodically fight a fresh bot (no fine-tuning, pure Fechtbuch), and include those rounds in the training data.

**DPO instability:** RLHF systems are notoriously fragile — failures often manifest as subtle behavioral regressions rather than crashes or errors. DPO is more stable than classical RLHF but still requires monitoring. Run evaluation rounds against a held-out baseline after each fine-tuning update.

**The 7B quality ceiling:** The combat model is 7B for latency reasons. DPO can improve it within its capability class, but it cannot push it past what a 7B model can do. The ceiling isn't the training — it's the model architecture. Accept this and design for it.

---

## 7. Tools

**Unsloth:** Currently the fastest QLoRA/DPO implementation on consumer hardware. 2–5× faster than baseline HuggingFace. Supports Qwen, Llama, Mistral families. Active development, good 4090 support. First choice for the dojo training loop.

**TRL (HuggingFace):** The reference implementation for DPO, PPO, RLAIF. Slightly slower than Unsloth but more flexible and better documented. Good for experimentation.

**OpenRLHF:** Full RLHF pipeline including GRPO and multi-agent extensions (MARTI fork). Designed for multi-GPU but has single-GPU modes for smaller models. Relevant if the project evolves past DPO toward full RL training loops.

**Axolotl:** Configuration-driven fine-tuning pipeline. Good for running reproducible experiments with different hyperparameters. Wraps TRL/HuggingFace with cleaner config management.

---

## 8. What This Enables That Episodic Memory Alone Doesn't

The distinction matters:

**Episodic memory + retrieval (current architecture):**
- Bot remembers "Nachreisen worked against Bot B in situation X"
- Retrieves this at inference time and uses it
- Resets if memory is cleared
- Doesn't transfer to new contexts automatically
- No change to underlying weights

**DPO fine-tuning:**
- Bot's *weights* encode that Nachreisen is good in situation X
- No retrieval needed — it's part of the model's intuition
- Persists even if episodic memory is cleared
- May generalize to new opponents (the research question)
- Weight change is permanent (unless you revert to base adapter)

Both are useful and complementary. Episodic memory is fast, explicit, inspectable, and reversible. DPO weight updates are slow, implicit, harder to inspect, but more robust and potentially generalizing.

The full architecture uses both: episodic memory for session-level adaptation, DPO fine-tuning for persistent skill accumulation across sessions.

---

*Tags: [fine-tuning, rlhf, dpo, qlora, lora, 4090, dojo, resonite, fechtbuch, skill-learning, training, technical, high]*
