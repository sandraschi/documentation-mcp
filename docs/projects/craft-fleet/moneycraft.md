# MoneyCraft — Assessment

**Repo:** `D:\Dev\repos\moneycraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Offline-first pure-Rust quantitative finance studio — Bloomberg-grade time-series
terminal and local-first algo workbench. Port `14117`. Consolidates financial
streams, backtesting, CCXT/broker feeds, plus smart-contract audit ambition.

## Model / verbs

- **Model:** symbol time-series + strategy + ledger (trades/tax).
- **Crates:** `moneycraft-core`, `moneycraft-feed`, `moneycraft-mcp`, `moneycraft-app`.
- **Docs present:** `PRD.md`, `SPEC.md`, `HELP.md` — better than most of its
  generation. Verbs: feed ingest, backtest run, ledger persist (toward DatabaseCraft blueprints).

## Architecture

Rust workspace, Tokio full, MIT. `start.ps1`/`start.bat` present. No `docs/`
folder (specs at root), no `justfile`, no test evidence at triage. Last commit
2026-11-04 (i18n + historical deep-archive 1720/1850 + panic annotations — data depth).

## Strengths

- Only scaffold-generation craft with PRD + SPEC + HELP at root.
- Historical depth (1720/1850 archives, panic annotations) is a real differentiator.
- Feed/core split is the right seam (live ingest vs offline analysis).

## Gaps / risks

- Highest-risk domain in the fleet: financial advice liability, live-money safety,
  broker credential handling. Nothing at triage proves paper-trade-only guardrails.
- Feed licensing/cost (CCXT exchange data, Bloomberg-alt claims) unaddressed.
- No backtest-correctness tests (survivorship bias, lookahead) — the one thing that
  must be tested before anything else.
- Smart-contract auditor + trading terminal in one repo risks sprawl; pick the
  terminal first.

## Next 3 steps

1. Safety doc: paper-only by default, credential redaction, no-live-trade gate.
2. 3 correctness tests on fixtures (known series → known backtest numbers, no lookahead).
3. Move PRD/SPEC into `docs/` and add `docs/TOOLS.md`; one democraft recipe on fixtures.

## Verdict

Best-documented of the new studios, but finance demands proof, not prose.
C+ until backtest fixtures go green and the paper-only guardrail is enforced in code.
