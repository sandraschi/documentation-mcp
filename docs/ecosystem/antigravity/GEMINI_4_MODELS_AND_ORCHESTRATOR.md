# Gemini 4 Lineup: Carbon, Argon, Hydrogen & Antigravity Orchestrator

**Updated:** 2026-11-15  
**Focus:** Model comparison and practical usage in **Antigravity (`agy`) on a Google AI Pro account**.

---

## 1. Model Comparison

All three Gemini 4 models share a **1,048,576-token (1M) unified context window** (input + thinking + output) and **65,536-token default sync output** (scaling up to 1M with long decode).

| Model | Role | Thinking Levels | API Pricing (per 1M tokens) | Antigravity Pro Access | Antigravity Ultra Access |
|---|---|---|---|---|---|
| **Gemini 4 Carbon** (`gemini-4-carbon`) | Heaviest flagship reasoning (deep architecture, long-horizon logic, science) | `low`, `medium` (default), `high` | $2 in / $10 out through 2026-11-30; **$4 / $20** from 2026-12-01 (no free tier) | **No** | **Yes** |
| **Gemini 4 Argon** (`gemini-4-argon`) | Frontier reasoning (complex SWE, math, autonomous multi-step agents) | `low`, `medium`, `high` | $2 in / $10 out through 2026-11-30; **$4 / $20** from 2026-12-01 (no free tier) | **Yes** | **Yes** |
| **Gemini 4 Hydrogen** (`gemini-4-hydrogen`) | Fast, lightweight execution model (everyday coding, debugging, worker steps) | `low`, `medium`, `high` (default), `xhigh` | **$1.50 in / $7.50 out** (free tier in AI Studio) | **Yes** | **Yes** |

---

## 2. What Antigravity Orchestrator Does

Instead of running one heavy model from start to finish, **Orchestrator** hot-swaps between two models inside a single Antigravity session:

1. **Planner phase (read-only):** A frontier model (**Argon** or **Carbon**) inspects the codebase, resolves dependencies, and writes the implementation plan.
2. **Execution phase:** **Gemini 4 Hydrogen** performs the bulk edits, writes code, and runs tests at low latency.
3. **Fallback loop:** If tests fail or unexpected edge cases appear, control returns to the planner to revise the strategy.

**Reported impact (Google):** Near-frontier task success rates with roughly **24% less quota consumed** and **19% faster completion** compared to running a single frontier model end-to-end.

| Orchestrator Variant | Pairing | Pro Account | Ultra Account |
|---|---|---|---|
| **Orchestrator (Argon)** | Argon (planner) + Hydrogen (executor) | **Yes** (direct paid Pro; some partner promo bundles excluded) | **Yes** |
| **Orchestrator (Carbon)** | Carbon (planner) + Hydrogen (executor) | **No** | **Yes** |

---

## 3. Practical Guide for Antigravity on a Pro Account

Pro accounts operate under a dual-limit quota (**rolling 5-hour window** + **weekly rate limit**) based on compute/work performed rather than flat message count.

### When to pick each option on Pro

- **`Orchestrator (Argon)` — Default for real features & refactors:**  
  Best balance of capability and quota. Argon handles the architecture/planning upfront, while Hydrogen does the multi-file edits and test loops without burning frontier quota on routine code generation.
- **Gemini 4 Hydrogen (`low` / `medium` / `high` / `xhigh`) — Fast iteration & quota preservation:**  
  Use directly for well-scoped edits, boilerplate, quick debugging, or when your 5-hour/weekly quota is getting tight. At `high` or `xhigh` thinking, Hydrogen handles surprisingly hard execution tasks while staying cheaper and faster than standalone Argon.
- **Gemini 4 Argon (standalone) — Pure deep reasoning:**  
  Use when you want sustained frontier reasoning across the entire turn (e.g., tricky root-cause analysis, subtle concurrency/security review, or design trade-offs where you aren't doing large mechanical edits).
- **Gemini 4 Carbon / `Orchestrator (Carbon)`:**  
  Not available on Pro; requires **Google AI Ultra** (or Enterprise).

### Summary rule of thumb (Pro)

| Task | Pick |
|---|---|
| Multi-file feature / refactor | **Orchestrator (Argon)** |
| Quick fix, single-file edit, test iteration | **Hydrogen** (`medium` or `high`) |
| Hard bug / design review (no bulk edits) | **Argon** (or Hydrogen `xhigh`) |
| Deepest frontier architecture (needs Ultra) | **Orchestrator (Carbon)** / **Carbon** |

---

## Related

- [Antigravity Ecosystem Overview](README.md)
- [Antigravity 2.0 — SDK & CLI](ANTIGRAVITY_2.0_SDK_CLI.md)
- [Multi-Account Switching](MULTI_ACCOUNT_SWITCHING.md)
