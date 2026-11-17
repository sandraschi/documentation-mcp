# Cursor First-Party Models: Grok (4.5–4.7) vs. Composer (2.5)

**Added:** 2026-11-15

Both **Grok** and **Composer** draw from Cursor's shared first-party usage pools on paid plans, but they are tuned for very different jobs.

---

## Side-by-Side Comparison

| Dimension | **Grok (4.5 – 4.7)** | **Composer (2.5)** |
|---|---|---|
| **Role** | Flagship frontier reasoning (xAI/SpaceX tie-in) | Fast, specialized agentic coding model |
| **Context Window** | Up to **500k** tokens | **200k** tokens |
| **Effort Controls** | Adjustable (`low`, `medium`, `high`, `xhigh`) | Fixed/fast coding loop |
| **Relative Cost / Quota Burn** | Higher (~$2/M input equivalent) | **~4× cheaper** (~$0.50/M input equivalent) |
| **Speed** | Slower (deliberate reasoning + self-verification) | **Very fast** (tight edit/terminal feedback loop) |
| **Best At** | Ambiguous multi-file refactors, architecture, deep debugging, unfamiliar codebases | Everyday feature building, well-scoped edits, rapid iteration, test-fix loops |

---

## Which One Should You Use?

- **Default to `Composer 2.5`** for 80% of daily coding: implementing well-defined features, UI tweaks, single-to-few-file edits, and fast iterative loops where latency and quota preservation matter.
- **Switch to `Grok (4.6 / 4.7)`** when:
  - You're touching an unfamiliar or sprawling codebase (>200k context helps).
  - The task is ambiguous, architectural, or a subtle bug that `Composer` keeps misdiagnosing.
  - You want heavy self-verification before committing.
- **Best combo (manual "Orchestrator" pattern):**  
  Use **Grok** in **Plan** mode to map the codebase and write the plan, then switch to **Composer 2.5** in **Agent** mode to execute the edits quickly without burning Grok-level quota on routine codegen.

---

## Related

- [Cursor Ecosystem Overview](README.md)
- [Agentic Coding Comparison (Nov 2026)](../AGENTIC_CODING_COMPARISON_NOV_2026.md)
