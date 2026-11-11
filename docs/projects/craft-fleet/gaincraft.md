# GainCraft - Assessment

**Repo:** `D:\Dev\repos\gaincraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic data only) - **Origin:** fleet-owned

## What it is

Customer health for small B2B: aggregate usage per account and day, contract data, support signals, an explainable 0-100 score and calls to action.
Seventh app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.7). Docs in repo: README, HELP.md, docs/PRD.md, docs/TOOLS.md (generated, test-checked).

## Model / verbs

- **Crates:** `gaincraft-store` (accounts, telemetry_daily, signals, triage, ctas, snapshots), `gaincraft-core` (`health.rs`, CTA rules, CSV import, bus inbox, deadlines, demo), `gaincraft-mcp` (`gaincraft` binary).
- **16 MCP tools / CLI verbs:** status, account add/list/show/update, telemetry_import, signal_add, health, health_all, triage_set, cta list/resolve, deadlines, weights, inbox_drain, demo_seed.
- **Score:** `100 x (0.45 adoption + 0.35 recency + 0.20 sentiment) x modifier`; adoption = 30-day average active / seats, recency halves every 14 idle days, sentiment = decayed signals (30-day half-life, 180-day window), modifier 0.8-1.2 advisory with reason and expiry.

## Strengths

- No per-person data by construction: the telemetry table has no person column (test-checked) and the import refuses user/e-mail/name/login/IP headers (ArbVG section 96a, DSGVO).
- Score is deterministic and explained component by component; an LLM may only nudge it within 0.8-1.2 with a written reason (Rust check + SQL CHECK).
- Import is all-or-nothing and idempotent per day; CTAs open once per account/kind/reference and need a note to close.
- Live chains verified with real binaries: deskcraft `signals --emit` -> gaincraft sentiment; contractcraft seal + `move executed` -> gaincraft ARR 5.400,00, C-2026-003, notice 31.08.2027.
- The live run caught a double-count (re-emitted ticket halved the sentiment, score 30 -> 22); fixed in the store with a regression test.

## Gaps / risks

- No egui window; CSV only, no product-database connector.
- Default weights and half-lives are reasoned, not fitted to churn data.
- Threshold CTAs (adoption_drop, seats_unused) will misfire for seasonal customers.
- contractcraft does not yet send amendments or terminations, so ARR and dates can go stale.

## Next 3 steps

1. formcraft survey responses as signals (negative and positive).
2. `contract.terminated` / `contract.amended` from contractcraft.
3. egui app: account list with trend sparkline, CTA board; optional backtest to tune weights against past churn.

## Verdict

Grade C+: a privacy-first, explainable Tier 1 that closes the contractcraft and deskcraft links; needs a GUI and real usage data before daily use.
