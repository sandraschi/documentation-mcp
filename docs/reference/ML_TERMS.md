---
title: "ML Terminology — Traces, Distillation, and Inference"
category: reference
status: active
audience: fleet
last_updated: 2026-07-15
---

# ML Terminology

## Core Concepts

### Trace (also: reasoning trace, CoT trace)

The **full chain-of-thought text** a model generates internally before producing a final answer. For reasoning models (DeepSeek V4 Flash, Claude Opus, GPT-5.x, Qwopus), this includes the step-by-step deliberation between `thinking` tags — not just the final output.

**Why it matters for distillation:** The final answer alone is low-signal. The reasoning trace is high-signal — it reveals *how* the model decomposed the problem, which sub-questions it asked itself, where it backtracked, and how it verified its work. A distill model trained on final answers only learns what to say; a distill trained on traces learns *how to think*.

**Example:**
```
User: 17 * 24 = ?

Final answer only:         408
With CoT trace:            17 * 20 = 340, 17 * 4 = 68, 340 + 68 = 408
```

The second version is far more useful for training a student model.

### CoT (Chain of Thought)

A prompting technique where the model is guided to produce intermediate reasoning steps before the final answer. Initially a prompt engineering trick ("let's think step by step"), it became an architectural feature in reasoning models — they now have built-in `thinking` tokens and internal monologue that can be surfaced or hidden.

### Distillation (model distillation)

Training a smaller "student" model to replicate the behavior of a larger "teacher" model. The student never sees the original training data — only the teacher's outputs (and ideally its reasoning traces). This is different from:

| Term | What it is |
|------|-----------|
| **Distillation** | Student learns from teacher's **outputs** only |
| **Fine-tuning** | Model trained on **original labeled data** |
| **Quantization** | Model weights stored in lower precision (FP16 → INT4) — no training involved |
| **Pruning** | Removing parameters/neurons from a trained model |

### Encrypted agent instructions (Codex-style)

A defensive technique where a frontier model (e.g. GPT-5.6 Codex) encrypts the instructions it passes to sub-agents. The developer sees only the top-level agent's output — all internal delegation, sub-agent reasoning traces, and intermediate tool calls are opaque.

**Why it matters:** This breaks the trace-mining pipeline at its source. If reasoning traces are encrypted, behavioral cloning can only replicate the final output, losing the high-signal chain-of-thought. OpenAI announced this for Codex on July 15, 2026, making it mandatory for the larger GPT-5.6 variants (Sol, Terra).

**Trade-off:** Security vs debuggability. Developers can't audit how their AI system reached a decision, can't detect sub-agent prompt injection, and can't verify sub-agent tool calls.

### Behavioral cloning (cloning)

A distillation method where the student model learns to mimic the teacher's **behavior** (responses, style, reasoning patterns) without accessing the teacher's weights, architecture, or training data. The student observes input-output pairs (and ideally intermediate traces) and learns to reproduce them.

**Contrast with model extraction:** Extraction tries to reconstruct the teacher's weights through repeated queries. Behavioral cloning only replicates surface behavior — the student is a fundamentally different model that *acts like* the teacher.

### Adversarial distillation

A distillation setup where the teacher or an external discriminator actively tries to **detect and block** the distillation attempt, forcing the student to evolve around the defense.

Forms:
- **Detection-based:** The teacher monitors query patterns (velocity, account correlation, prompt distribution) and rate-limits or bans suspected distillers
- **Output watermarking:** The teacher embeds undetectable statistical fingerprints in responses; a downstream discriminator can flag student outputs as distillation-derived
- **Adversarial traces:** The teacher deliberately inserts misleading reasoning steps in suspicious sessions; a naive student learns bad patterns

The term comes from the GAN-like dynamic: the distiller optimizes for undetectability, the teacher optimizes for detection. Sock puppet account rotation is a direct response to detection-based adversarial distillation.

### Sock puppet distillation

A specific distillation method where the operator creates many API accounts to distribute query volume across, avoiding per-account rate limits and detection. Used when the teacher model is only accessible via paid API (Claude, Fable-class, GPT) and the operator wants to collect millions of traces without being blocked. The term comes from the accounts being disposable identities.

**Contrast — open-weight industrial distill:** operators with a real GPU farm (see [Jackrong Distill Factory](../models/JACKRONG_DISTILL_FACTORY.md#underreported-story-this-is-a-server-farm-not-a-sock-puppet-farm)) host FOSS teachers themselves and automate tracing with **zero** burner accounts. Sock puppets are a closed-API pathology; the underreported story is who can run DeepSeek/GLM/Kimi-class weights at scale.

## Strategic Note: The Thinking Tag Paradox

The `thinking` tag (or `reasoning` / `chain_of_thought` in API params) was introduced as a **transparency feature** — letting users see how the model arrived at an answer, enabling debugging and trust.

It became the primary **attack surface for behavioral cloning**. A reasoning trace from Claude Opus or GPT-5.x is a complete training example: problem statement, step-by-step strategy, backtracking, verification, and final answer. Distillers don't need model weights — they need API access and a parser.

The labs' dilemma:
- **Keep thinking visible** → every API call with `thinking=true` leaks high-signal training data. Jackrong's `Claude-opus-4.7-TraceInversion-5000x` dataset (5,000 traces) is enough to measurably shift a fine-tuned Qwen's reasoning style toward Claude's.
- **Remove thinking** → users revolt, safety researchers lose debugging ability, and "black box" criticism intensifies.

**Projected tiers (already emerging):**
| Tier | Thinking visibility | Anti-distillation measure |
|------|-------------------|--------------------------|
| Consumer chat | None or truncated | Default hidden |
| Developer API | Visible | Rate-limited, audited, watermarked |
| Enterprise / on-prem | Full | Contractual TOS, usage monitoring |
| Internal agent chains | Encrypted (Codex model) | Sub-agent traces never reach the caller |

The encrypted agent instructions rollout (Codex, July 2026) is the first major infrastructure response — if sub-agent reasoning is encrypted from the developer, it's certainly encrypted from the distiller. Expect `thinking` to follow the same trajectory: opt-in today, restricted tomorrow, paywalled the day after.

## Related

- [Jackrong Distill Factory](../models/JACKRONG_DISTILL_FACTORY.md) — industrial-scale trace mining and distillation
- [TOOLS_GLOSSARY.md](./TOOLS_GLOSSARY.md) — MCP tool taxonomy
