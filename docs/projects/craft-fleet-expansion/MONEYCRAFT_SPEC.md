# MoneyCraft Specification & Architecture Plan
**Sovereign Financial Intelligence, Algorithmic Trading Studio & Portfolio Defense**

**Version**: 0.7.0  
**Date**: 2026-11-04  
**Author**: sandraschi fleet architecture / DeepMind AGY  
**Domain**: Quantitative Finance, Fleet-Standard i18n Localization (7 Languages), Historical Deep-Archive (1720–2026), 19 Major Financial Panics Catalog & Chart Annotations, Personal Wealth & Inflation Defense, Global Indices Desk, Historic London Sovereign Papers (East India Co, Consols, South Sea Bubble), Multi-Asset Comparisons, Crypto Derivatives & Futures Sandbox, Forex Desk, Time-Series Analysis, Agentic AI Workflows, Anti-Scam Verification  
**Standard Port**: 14117 (Assigned via fleet registry `WEBAPP_PORTS.md`)  

---

## 1. Executive Summary: Dismantling the Cloud Investor Cartel

### The Retail Investor Landscape: Predatory, Expensive, and Opaque
1. **The Terminal Trap (Bloomberg, Refinitiv, FactSet)**:
   - \$24,000 to \$32,000/year per terminal. Completely inaccessible to independent quants, family offices, and normal professionals.
2. **Cloud Day-Trading & "Fintech" Platforms (TradingView, SeekingAlpha, Benzinga)**:
   - Aggressive paywalls for basic technical indicators, rate-limited alerts, and dark-pattern upsells.
   - User browsing and watchlist data is monetized and front-run by institutional order flow.
3. **The Crypto & "Guru" Scam Minefield**:
   - Predatory Discord pump-and-dump signals, honeypot smart contracts, opaque algorithmic trading bots with hidden liquidation risks, and fake exchange APYs.

### The MoneyCraft Thesis: Sovereign, Zero-Tax Financial Intelligence
MoneyCraft is an offline-first, pure-Rust quantitative finance studio and autonomous trading workbench. It combines **institutional-grade algorithmic execution**, **G10 Forex trading**, **real-time breaking news analysis**, **cryptographic scam detection**, and **local private portfolio accounting** with zero monthly SaaS fees and zero privacy leakage.

```
                      ┌───────────────────────────────────────────┐
                      │             MoneyCraft Studio             │
                      │       (Native egui Candlestick, Area,     │
                      │       Forex Desk & Breaking News Wire)    │
                      └─────────────────────┬─────────────────────┘
                                            │
        ┌───────────────────────────────────┼───────────────────────────────────┐
        ▼                                   ▼                                   ▼
┌──────────────────┐               ┌──────────────────┐                ┌──────────────────┐
│   Sovereign FX   │               │   Agentic AI     │                │   Anti-Scam      │
│   & Multi-Asset  │               │   Quant Engine   │                │   & Smart-       │
│ • EUR, USD, JPY  │               │ • BQuant Code Gen│                │   Contract       │
│ • GBP, CNY/RMB   │               │ • PORT Stress-Tst│                │   Auditor        │
│ • BTC, ETH, SOL  │               │ • Sentiment Alpha│                │ • Honeypots      │
│ • NVDA, SPY, Gold│               │ • Smart Order Rte│                │ • Drainer Traps  │
└────────┬─────────┘               └────────┬─────────┘                └────────┬─────────┘
        └───────────────────────────────────┼───────────────────────────────────┘
                                            │
                                            ▼
                           ┌──────────────────────────────────┐
                           │      Sovereign Financial DB      │
                           │      (DatabaseCraft Powered)     │
                           │ • Offline Tax & Cost Basis       │
                           │ • Immutable Trade Ledger         │
                           │ • Zero Data Scraping/Leakage     │
                           └──────────────────────────────────┘
```

---

## 2. Core Pillars of MoneyCraft

### Pillar 1: High-Density Bloomberg Time-Series & Forex Desk
- **60-Bar Stochastic Market Simulation**: High-density tick stream with realistic geometric Brownian drift and micro-wicks.
- **Visual Styles**: Dynamic toggle between Candlestick (Jade/Crimson), Mountain Area (alpha gradient fill), and Heikin-Ashi.
- **Overlay Suite**: SMA 20 (Cyan), EMA 50 (Gold), Bollinger Bands (Purple 2σ ribbon), Volume profile, and RSI 14 oscillator with 70/30 threshold lines.
- **G10 Forex Desk**: Pip-scaled pricing for EUR/USD, USD/JPY, GBP/USD, USD/CNY, and EUR/GBP.
- **Interactive Crosshair HUD**: Moving cursor projects crosshairs and floating coordinate cards.

### Pillar 2: Breaking News Wire & NLP Sentiment Polarity
- Continuous marquee news banner with categorized items: `[MACRO]`, `[FOREX]`, `[CENTRAL_BANK]`, `[CRYPTO]`, and `[EQUITY]`.
- Scored sentiment badges (`🟢 BULLISH`, `🔴 BEARISH`, `🟡 NEUTRAL`) indicating market catalyst velocity.

### Pillar 3: Grounded Agentic AI Quant Workflows
1. **BQuant Strategy Synthesis**: Generates vectorized alpha code with projected Sharpe ratio and maximum drawdown.
2. **PORT Macro Stress-Testing**: Simulates central bank rate scenarios and computes portfolio Value-at-Risk ($\text{VaR}_{99}$) and hedging requirements.
3. **NLP Sentiment Alpha**: Analyzes transcripts and breaking headlines for semantic drift.
4. **Smart Order Routing (SOR)**: Slices blocks across dark pools and ECNs using adaptive VWAP.

### Pillar 4: Anti-Scam & Structural Due Diligence Engine
- **Smart Contract Honeypot Analyzer**: Simulates on-chain buy/sell transactions in a local sandbox EVM before executing; flags non-standard transfer taxes (>5%), blacklisting logic, or minting backdoors.
- **Wash-Trading & Liquidity Depth Detector**: Analyzes bid/ask spread thickness and tick frequency to verify real market liquidity vs. artificial spoofing bots.

### Pillar 5: Sovereign Portfolio & Tax Ledger (DatabaseCraft Integration)
- Automatically computes FIFO, LIFO, and Specific Identification cost basis for capital gains tax calculations.
- Exports fully audit-ready tax manifests directly with zero external telemetry.

### Pillar 6: Personal Wealth, Savings & Inflation Erosion Simulator
- **The "Bank App Illusion"**: Solves the beginner psychological trap where nominal balances (Girokonto, 3% Festgeld, Bausparer) appear to grow while high inflation (3.8%+) silently strips away real purchasing power.
- **Dynamic Compounding & Real-Discount Engine**: Simulates monthly net cashflow (+2,000 € net income, 1,400 € living expenses), 0% Girokonto accumulation, 3-year locked Festgeld, and Bausparvertrag deposits.
- **Rule of 72 Halving Clock**: Calculates the exact half-life of fiat capital under active inflation ($72 / i$).
- **Nominal vs Real Purchasing Power Grid**: Contrasts nominal app balance against actual inflation-discounted value, displaying cumulative silent losses and preserved purchasing percentage.
- **Actionable Beginner Defense Playbook**: Prescribes the Notfallgroschen emergency buffer, Tagesgeld/DBX0AN Geldmarkt-ETF, All-World ETF (MSCI World / FTSE All-World), and Physical Gold.

### Pillar 7: Global Indices, Multi-Asset Comparisons & Date Ranges
- **Global Market Coverage**: Dow Jones (`DJIA`), S&P 500 (`SPX`), Nasdaq (`NDX`), DAX 40 (`DAX`), Nikkei 225 (`N225`), KOSPI (`KOSPI`), FTSE 100 (`FTSE`), and Hang Seng (`HSI`).
- **Normalized 0.0% Baseline Graph**: Normalizes multiple disparate assets to 0.0% at start of period to visualize relative percentage outperformance.
- **Date Presets**: Fast switching between `1D`, `1W`, `1M`, `3M`, `YTD`, and `1Y`.

### Pillar 8: Crypto Derivatives Desk & Fantasy Paper Trading Arena
- **Cross-DEX Funding Rate Arbitrage**: Compares Hyperliquid vs Binance/Bybit/OKX APR spreads for delta-neutral yield harvesting.
- **Liquidation Heatmaps**: Visualizes open interest cascades, short squeeze clusters, and long flushes.
- **Risk-Free Futures Sandbox**: Supports 1x to 50x leverage trading with margin call alerts and floating PnL tracking.

### Pillar 9: Fleet-Standard i18n Localization Architecture
- **Storytold Craft Alignment**: Directly mirrors the i18n engine of *GameCraft*, *QGISCraft*, and *DesignCraft*.
- **Static Compile-Time Localization**: Zero disk I/O, zero gettext, typed enum dictionary mapping (`t(key, locale)`).
- **Supported Languages**: English (`EN`), Deutsch (`DE`), Français (`FR`), Español (`ES`), Japanese (`JA`), Korean (`KO`), Chinese (`ZH`).
- **Dynamic Top-Bar Locale Switcher**: Instant live repainting without restarting the binary.

### Pillar 10: Historical Deep-Archive & Financial Panics Engine (1720–2026)
- **Deep Historical Date Presets**: `5Y`, `MAX (1990)` (35+ years), `HISTORIC (1850)` (London Victorian era / Industrial Revolution), `ALL-TIME (1720)` (Exchange Alley & South Sea Bubble).
- **London Sovereign Papers**: Continuous records for **The Honourable East India Company (EIC)** (1600–1874), **Bank of England 3% Consols** (from 1751), and **South Sea Company** (1711–1720).
- **19 Cataloged Financial Panics with Chart Annotations**: Vertical timeline flags, hover tooltip dossier, drop percentages, catalysts, and quant risk lessons from 1720 South Sea Bubble to the 2022 Inflation/SVB shock.

### Pillar 9: Multi-Source Market Data Engine & Exchange Payola Matrix
- **Switchable Feed Architecture**: Instant toggle between 9 data providers:
  1. `synthetic`: Air-gapped stochastic Brownian drift (0ms, $0, 100% offline).
  2. `binance`: Official live public REST Kline stream (⚡ <150ms real-time, $0, zero-auth).
  3. `hyperliquid`: Direct L1 decentralized node feed for perps, mark prices & funding rates (⚡ <120ms, $0, zero-auth).
  4. `yahoo`: Real global equity indices (`^DJI`, `^GSPC`, `^KS11`, `^GDAXI`, forex, gold) using the 15-minute public regulatory exemption (⏱️ 15-min delay, $0).
  5. `ecb`: Official European Central Bank Euro foreign exchange daily benchmark fixings (📅 14:15 CET, $0).
  6. `twelve_data`: Commercial market data aggregator with free tier API key support.
  7. `interactive_brokers`: Direct local TWS / Gateway socket (port 7496) passing through raw exchange fees ($1.50/mo vs $24k Bloomberg).
  8. `polygon_io`: Consolidated SIP Tape A/B/C developer subscription ($29-$199/mo).
  9. `bloomberg_bpipe`: Institutional Wall Street leased-line cartel feed ($2,000-$2,700/mo).
- **Latency & Payola Transparency**: Every quote displays its exact latency delay, cost tier, and exchange redistribution breakdown.
