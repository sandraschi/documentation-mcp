# MoneyCraft — Assessment

**Repo:** `D:\Dev\repos\moneycraft` · **Date:** 2026-11-09 · **Grade: A-** · **Origin:** fleet-owned

## What it is

Offline-first pure-Rust quantitative finance studio, personal portfolio/holdings ledger, historical panic museum (1720–2025), and paper-trading execution workbench (`v0.7.0`, port `14117`).

## Model / verbs

- **Model:** symbol OHLCV time-series + strategy backtest + SQLite personal holdings ledger + paper broker (`PaperBroker` with `BrokerLimits` risk enforcement).
- **Crates (5 crates, `9,341 LOC`, `11 tests`):**
  - `moneycraft-core`: indicators (SMA, EMA, RSI, MACD, Bollinger), backtest engine, SQLite personal ledger (`holdings`, `transactions`, `alerts`, `watchlist`, `import_csv`, `export_csv`), historical financial panics archive, `craft-ai-core` advisor integration.
  - `moneycraft-feed`: live CoinGecko / Yahoo Finance market data ingestion with offline deterministic fallback.
  - `moneycraft-broker`: execution boundary (`Broker` trait, `PaperBroker` SQLite fill simulator, `BrokerLimits` max notional / daily loss / symbol allowlist, `dry_run` preview).
  - `moneycraft-mcp`: 17 MCP tools on stdio (`money_status`, `money_quote`, `money_candles`, `money_indicators`, `money_backtest`, `money_portfolio`, `money_ledger_add`, `money_ledger_summary`, `money_panics`, `money_paper_order`, `money_paper_positions`, `money_paper_reset`, etc.).
  - `moneycraft-app`: native `eframe`/`egui` Bloomberg-style terminal (Market Watch, Backtester, Personal Ledger, Paper Broker, Historical Panics Museum, AI Quant Advisor).

## Architecture

5-crate Pure-Rust ArtCraft 3-tier workspace (`9,341 LOC`, `11 tests`, `clippy -D warnings` clean). Includes `docs/` (10 files: `PRD.md`, `SPEC.md`, `HELP.md`, `TOOLS.md`, `PARITY.md`, `SAFETY.md`, etc.) and `dist/` packaging scripts.

## Strengths

- **Live-money safety in code, not prose:** `CoreCommand::PlaceOrder` returns an explicit refusal (`Err("Live order placement is disabled by design; use PaperOrder / PaperBroker")`), while `moneycraft-broker` enforces `BrokerLimits` (max order notional, daily loss halt, symbol allowlist) and `dry_run` validation on every paper order.
- Real SQLite persistence for both the personal holdings ledger (CSV import/export, cost basis, P&L) and paper-broker fills/positions.
- Deep historical dataset (1720 South Sea Bubble through modern macro crises) with annotated panic timelines.

## Gaps / risks

- Test count (`11` workspace tests) is solid on core/broker invariants but light relative to `9,341 LOC`; indicator golden-value vectors and survivorship-bias fixture tests should expand next.
- Live market feeds (`moneycraft-feed`) depend on public CoinGecko/Yahoo endpoints; rate-limit caching into SQLite should be default for repeatable backtests.

## Next 3 steps

1. Expand indicator + backtest golden-fixture tests from 11 to 25+ (verify exact RSI/MACD/Sharpe outputs against reference series).
2. Add SQLite OHLCV candle caching so live-fetched series become deterministic local fixtures.
3. Register 3 `democraft` recipes (`money/backtest-sma`, `money/ledger-roundtrip`, `money/paper-broker-limits`).

## Verdict

Grade A-: `moneycraft` answered every concern from the Nov-5 triage — paper-only execution is enforced in code via `moneycraft-broker`, SQLite backs both the personal ledger and paper positions, and 17 MCP tools share one dispatch bus with the desktop terminal.
