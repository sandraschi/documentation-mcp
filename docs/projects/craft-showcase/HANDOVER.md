---
updated: 2026-11-15T11:02:00+01:00
agent: antigravity
status: completed
tags: [craft-showcase, wasm, diy-fleet, tailscale-funnel, sync]
---

# Handover — Craft Showcase

## What Was Done
- Built and verified in-browser WebAssembly studio compiling `egui / eframe 0.37` via `trunk` to `wasm32-unknown-unknown` (`crates/craft-showcase-wasm` → `web/wasm/`).
- Split the showcases cleanly into two pages on port `11270` with a shared header switcher:
  - `web/index.html`: **Sovereign Back-Office Suite** (12 B2B apps, ROI calculator, domino cascade, WASM studio).
  - `web/diy.html`: **DIY Craft Fleet** (33 non-backoffice `*craft*` apps across 5 categories with filter pills + live search).
- Added `scripts/sync-diy-catalog.ps1` and `.\start.ps1 -Sync` to scan `D:\Dev\repos\*craft*`, read `Cargo.toml` versions, `README.md` summaries, and `git remote get-url origin`, and write `web/data/diy-apps.json`.
- Added `GitHub ↗` repo links to every card in both `web/index.html` and `web/diy.html`.
- Exposed port `11270` publicly via Tailscale Funnel on `https://goliath.<tailnet>.ts.net:8443/`.

## Last Concrete Action
- Verified `.\start.ps1 -Sync` (`33` DIY craft apps) and `.\start.ps1 -Smoke` (`smoke: ok (craft-showcase web, diy & wasm)`, exit 0).
- Verified `200 OK` over Tailscale Funnel for `/`, `/diy.html`, `/wasm/`, and `/data/diy-apps.json`.

## Next Step
- Commit & push `craft-showcase` changes (`web/diy.html`, `web/data/diy-apps.json`, `scripts/sync-diy-catalog.ps1`, `start.ps1`, `web/index.html`) to `sandraschi/craft-showcase`.
- Record the 4-act video trailer in `web/index.html` when ready.
