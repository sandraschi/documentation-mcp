# Craft Showcase — Assessment

**Repo:** `D:\Dev\repos\craft-showcase` · **Date:** 2026-11-10 · **Grade:** A · **Origin:** fleet-owned

## What it is

Interactive in-browser WebAssembly studio, client presentation portal, dynamic ROI calculator, and video pitch storyboard for the Sovereign Back-Office Suite. Allows prospective enterprise clients and executives to test the full suite directly inside any modern browser without downloading binaries or configuring cloud backends.

## Architecture & Verbs

- **Crates:**
  - `crates/craft-showcase-wasm`: Pure-Rust `eframe 0.37` WebAssembly workstation compiled to `wasm32-unknown-unknown` via `trunk` (WebGL2 / WebGPU canvas runner).
- **Web Portal:**
  - `web/index.html`: Modern dark-mode client showcase with interactive seat slider ROI calculator (€314k/yr savings at 50 seats), domino cascade visualizer, Austrian statutory law mapping, and 2.5-minute video presentation script.
  - `web/wasm/`: Self-contained compiled WebAssembly distribution (`.wasm` + `.js` glue).
  - `web/downloads/`: One-click downloads for A4 PDF brochure and EPUB digital editions.

## Strengths

- Pure Rust WebAssembly compiled with zero panics under strict `#![deny(clippy::unwrap_used, clippy::expect_used, clippy::panic)]`.
- Solves client demo friction: prospective clients can explore `HelmCraft`, `BillCraft`, `SpendCraft`, `HireCraft`, and `TaskCraft` immediately in their browser at 60 FPS.
- Transparent economic calculator with interactive seat scaling.
- Complete 4-act director's screenplay ready for video production.

## Next 3 Steps

1. Record live screen footage for the 4 acts outlined in the video storyboard.
2. Publish static bundle to GitHub Pages or custom domain (`craft.s.at`).
3. Add full screen capture clips to the video preview card on the landing page.

## Verdict

Grade A: Essential client-facing weapon that bridges local-first sovereign Rust desktop software with zero-friction web demonstration and compelling financial ROI presentation.
