---
title: "Hard Budget Caps and the Fleet Cost-Explosion Failsafe"
category: research
status: active
audience: all-agents
last_updated: 2026-10-04
source: "https://simonwillison.net/2026/Oct/3/default-hard-budget-caps/ (2026-10-03)"
related:
  - "standards/LOCAL_LLM_FIRST_DOCTRINE.md"
  - "standards/TOOLING_COST_MODEL.md"
  - "standards/LLM_AND_INSTALL_TIERS.md"
  - "standards/ONBOARDING_STANDARD.md"
---

# Hard Budget Caps and the Fleet Cost-Explosion Failsafe

## 1. Source

Simon Willison, 2026-10-03: "default hard budget caps".

Thesis: every pay-by-usage service needs a **hard** cap - "after $X/month, cut this thing off and return errors". Soft caps ("after $X, send a warning email") do not cut it, because coding agents and personal agents remove the friction of spinning up billable things, and nobody wants to wake up to a midnight warning email plus several hundred more dollars burned while they slept.

Two data points he cites:

- AWS launched spend limits with the new Builder Experience on 2026-09-16: "If a project's usage reaches its spend limit, your project is paused for that month." Currently limited rollout, docs at Create a spend limit in AWS Settings.
- Google Cloud launched Spend Caps in July 2026: monthly financial cap on specific services within a project.

His product ask: hard caps **on by default**, removal as explicit opt-in with a prominent checkbox: "Remove the budget cap. My application will not be shut down if I exceed the configured budget limit, and I will be responsible for subsequent charges." Plus: agents should bias toward recommending providers with hard caps and warn builders against deploying on uncapped services.

## 2. TL;DR for the fleet

Local models zero out the **token** meter. They do not zero out the **hands** meter. A free local brain driving paid tools (cloud LLM fallback, embeddings API, provisioned infra, hosted webapp, storage/compute) can still produce the exact $10k surprise Simon describes, with $0 in the LLM column.

After the vendor LLM step lands on every repo (Tier B cloud path everywhere: OpenCode serve, DeepSeek, OpenRouter, OpenAI-compatible), **every single repo becomes external-token capable**. That is precisely when a fleet-wide cost-explosion failsafe stops being nice-to-have and becomes a ship gate. This file is the writeup plus the integration plan.

## 3. Why "local = free" does not make this irrelevant

1. **Brains are free, hands cost money.** Our agents do not just emit tokens. They call `container_ops`, provision VMs, deploy webapps, write to hosted storage, hit paid APIs. Token cost zero does not cap action cost. The failure mode survives the move to Ollama on Goliath unchanged.
2. **Local has fixed costs and slow-burn costs.** 4090 at ~350W is ~$0.06/hr, ~$0.50 per 8h run, ~$36/month always-on (see TOOLING_COST_MODEL sec 4). Cheap, not zero. Worse: a weak local model that loops for 9 hours to do what a frontier model does in 3 calls costs little in dollars and a lot in time, power, and stuck-VRAM Goliath contention.
3. **The vendor step reintroduces the meter everywhere.** LLM_AND_INSTALL_TIERS requires Tier B (cloud API with key + base URL) documented with the same prominence as Ollama, and the webapp must work out of the box with key only. Once that is done fleet-wide, any repo can burn external tokens the moment local is offline or the user picks cloud in Settings. No per-repo failsafe means N new surprise-bill surfaces.

Conclusion: local-first shrinks the blast radius for LLM bills but does not remove the need for hard caps on the action side and the token side. Both need the same pattern Simon asks for: default-on hard stop, explicit opt-out.

## 4. How this maps to existing fleet doctrine

- LOCAL_LLM_FIRST_DOCTRINE: "Local is the default. Cloud is an explicit opt-in, a line item on budget." The failsafe is the enforcement mechanism for that sentence. Today it is policy; after this plan it is code.
- TOOLING_COST_MODEL (three pricing models): sunk-cost local / capped subscription / usage-metered. The failsafe converts model 3 into model 2 by default: every metered path ships with a cap that makes it behave like a subscription until the user opts out.
- LLM_AND_INSTALL_TIERS Tiers A-D: Tier B is the risk surface. INSTALL.md and CONFIGURATION.md already require `OPENAI_API_BASE` / `OPENAI_API_KEY` docs. They do not yet require a budget section. They should.
- ONBOARDING_STANDARD (MOCK-until-onboarded): the natural home for the cap UI - big red onboarding-adjacent cue, MOCK-badged spend widget until a real provider + budget is configured, clears after onboarding.

## 5. Failsafe v1 spec (same shape in every repo)

Keep it boring and identical everywhere so assfix can check it mechanically.

**Config (env + Settings, both):**

- `FLEET_LLM_MONTHLY_BUDGET_USD` (default: 10.00)
- `FLEET_LLM_HARD_CAP` (default: 1 = on; 0 = user explicitly opted out)
- `FLEET_LLM_SPENT_DB` (default: `data/llm_spend.sqlite3`, gitignored, one row per call: ts, provider, model, prompt_tokens, completion_tokens, est_usd)

**Backend middleware (FastMCP + Starlette/FastAPI):**

- Single wrapper around every outbound OpenAI-compatible call (chat, embeddings, sampling passthrough, skill-driven calls). Counts prompt/completion tokens, applies a small per-model price table (checked-in JSON, pessimistic defaults when model unknown), accumulates month-to-date USD.
- On cap breach: stop hard. Return 402 with a plain message: "LLM budget cap hit ($X of $Y for YYYY-MM). Raise FLEET_LLM_MONTHLY_BUDGET_USD or disable the hard cap in Settings. No further external calls will be made this month." No silent fallback to a more expensive provider. Local Ollama path keeps working.
- Health/probe surface exposes `llm_budget: { spent, budget, hard_cap, blocked }` so Dashboard and assfix can read it without credentials.

**Webapp (catch-them-all pages):**

- Settings -> Budget section: numeric budget input, hard-cap toggle behind the explicit opt-out checkbox using Simon's wording verbatim. Persist provider + budget in localStorage, mirror to backend env where the backend is local.
- Dashboard hero KPI: `LLM spend $A / $B (resets Nov 1)` with green/amber/red state and a visible HARD CAP ON badge. Before onboarding succeeds, show MOCK-badged sample values per ONBOARDING_STANDARD, cleared after real config.
- Logs page: every blocked call logged with timestamp and would-have-cost estimate.

**Agent behavior:**

- When recommending a deploy target or LLM provider, prefer ones with native hard caps (AWS spend limits, GCP Spend Caps) and say so in one line.
- Before deploying anything to a provider with no hard cap, emit the warning Simon asks for: uncapped, estimated worst case unknown, suggest setting the fleet cap first. This applies to sampling agents and to chat skills that scaffold infra.

## 6. Integration plan (fleet rollout)

**Phase 0 - Standard draft (this file -> standard).**
Promote the v1 spec above to `standards/COST_EXPLOSION_FAILSAFE_STANDARD.md` (normative, short, checklist-style). Add cross-refs from TOOLING_COST_MODEL, LOCAL_LLM_FIRST_DOCTRINE sec 6 audit checklist, LLM_AND_INSTALL_TIERS validation checklist, and NEW_REPO_BUILD_COMPLETE assfix-zero self-check. No code yet, just the gate definition so new repos build to it.

**Phase 1 - Reference implementation (1 pilot repo, 1 PR).**
Pick one LLM-heavy repo (suggestion: local-llm-mcp or fleet-agent-mcp). Implement backend wrapper + SQLite + 402 path + Settings Budget section + Dashboard KPI + INSTALL/CONFIGURATION docs + `just ci` coverage. Prove by running: set budget $0.01, fire a cloud call, observe the block, screenshot Dashboard + Logs. No other repos touched in this phase.

**Phase 2 - Couple to the vendor LLM step.**
The vendor step is what makes every repo meter-capable, so the failsafe rides the same PR per repo: vendor provider dropdown + keys in Settings lands together with Budget section + middleware + docs. Update the shared INSTALL template (`templates/INSTALL.md`) and the README-structure checker (`scripts/check-readme-structure.ps1`) to warn when an LLM-capable repo lacks the Budget section. From this point on, "vendor LLM done, failsafe missing" is a gate fail.

**Phase 3 - Fleet sweep (mechanical, batched).**
- `drift-scan` to enumerate all repos with LLM features (chat page, embeddings, sampling, provider Settings).
- `assfix` in batches of max 5 repos per invocation (fleet batch rule), each with timestamped `.bak` for 3+ file edits, per-repo `just ci` + budget-block proof run.
- Track in `operations/fleet-status.md`: per-repo columns `vendor-llm` / `failsafe-v1` / `proof-run`.

**Phase 4 - Docs and promotion.**
INSTALL.md Tier B gains a Budget subsection everywhere ("Cloud costs real money; the hard cap is on by default at $10"). `docs/CONFIGURATION.md` gains the three env vars. FLEET_PROMOTION-relevant: public-facing READMEs state the cap behavior in one line so downstream users know the agent will stop rather than bankrupt them.

## 7. Open questions (decided in Phase 0, not deferred)

- Default budget: $10/month per repo is the strawman. Too low breaks Tier B weak-PC users; too high defeats the purpose. Needs one decision, applied uniformly.
- Price table source: checked-in static JSON with pessimistic unknown-model rate vs live fetch from provider. Static wins for offline determinism; revisit yearly.
- Scope of the monthly accumulator: per-repo SQLite is simple and matches per-repo data dirs. Cross-repo Goliath-wide rollup (one number for the whole box) is the real user question ("how much did my fleet spend?") and belongs in mcp-central-docs operations dashboard later, not in v1 per-repo code.
- Subscription rung (Claude Pro $20/mo) has no API meter to cap; the failsafe there is rate-window awareness in agent loops (stop and report rather than hammering), documented but not enforced in code.

## 8. Acceptance

- New standard file exists and is linked from the four doctrine files above.
- Pilot repo blocks a $0.01-budget cloud call with 402 + Dashboard red state + Logs entry (screenshots or CUA run).
- Template + checker updated so future vendor-LLM PRs without the failsafe fail loudly.
- Sweep tracker shows every LLM-capable repo as `failsafe-v1` + `proof-run`, or an explicit N/A rationale in DEVELOPMENT.md for repos with genuinely no outbound metered call.
