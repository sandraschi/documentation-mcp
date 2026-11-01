---
title: "Pure-Rust ArtCraft MCP Architecture & Fleet Rustification Standard (Primary Hub)"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-18
---

# Pure-Rust ArtCraft MCP Architecture & Fleet Rustification Standard

**Status:** Canonical Fleet Architecture Standard (established 2026-10-17 -- Red-Letter Regime Change)  
**Pilot Reference Implementation:** [`rust-devices-mcp`](../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp`, `v0.4.0+` Alpha, 4 crates, 24 tools, 58/58 tests)  
**Operational Conversion Macro / SOP:** [`repconv <repo>` (`patterns/REPCONV_SOP.md`)](../patterns/REPCONV_SOP.md)  
**Methodology Provenance:** Adapted from the **ArtCraft** containment harness (Brandon Thomas / `storytold` on GitHub). Public banner bearer of this Rust wave: Thomas and the 13 Crafting Apps (CADCraft, DeckCraft, DesignCraft, EffectCraft, FigCraft, FilmCraft, GridCraft, LightCraft, PdfCraft, PhotoCraft, SoundCraft, VectorCraft, WordCraft), each a pure-Rust native app with a CLI and an MCP server. Fleet r11n borrows the harness and wraps those engines. It does not reimplement them. Inventory: [`CRAFT_APPS_MCP_UTILIZATION.md`](./rust-artcraft/CRAFT_APPS_MCP_UTILIZATION.md). Desired and not yet built: the shared release factory and agent learnings, [`RELEASE_FACTORY.md`](./rust-artcraft/RELEASE_FACTORY.md). Parity method: [`ORACLE_LOOP.md`](./rust-artcraft/ORACLE_LOOP.md).  
**Navigation Hub:** [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md) | [STANDARDS_BAR.md](./STANDARDS_BAR.md) | [AGENT_READING_ORDER.md](./AGENT_READING_ORDER.md) | [Rust Language Hub](../languages/rust/README.md)

> [!IMPORTANT]
> **2026-10-17 Regime Change:** Effective 2026-10-17, the legacy Python/FastMCP + Starlette sidecar + multi-port React/Vite/Tailwind webapp standards are **SUPERSEDED** for all new and converted Pure-Rust ArtCraft MCP repositories. An agent working in a Pure-Rust repo (`Cargo.toml` at root) MUST follow this hub and its modular sub-standards below, and MUST NOT enforce Python/FastMCP/Starlette/port-claiming gates on it.

---

## Modular Sub-Standards (Table of Contents)

To keep context windows lean and high-signal, the Pure-Rust ArtCraft standard is organized into this **Primary Hub** plus focused sub-documents under [`standards/rust-artcraft/`](./rust-artcraft/) and [`patterns/REPCONV_SOP.md`](../patterns/REPCONV_SOP.md):

| Sub-Standard | Scope & Key Topics | When to Read |
|---|---|---|
| **1. [CONTAINMENT_AND_CRATES.md](./rust-artcraft/CONTAINMENT_AND_CRATES.md)** | - **The 5-Layer ArtCraft Containment Harness:**<br>  - Layer 1: `deny(unwrap_used, expect_used, panic, todo, unimplemented)` + Hostile Input Fence<br>  - Layer 2: `L1 (<domain>-core + <domain>-store)` / `L2 (<domain>-mcp)` / `L3 (<domain>-app)` workspace seam<br>  - Layer 3: Universal `Command::dispatch` Bus (`dispatch_future_is_send`), Zero-Config Legacy Fleet Import (`import.rs`), `readonly` Actuator Safety Fence<br>  - Layer 4: Tiered Scorecard & Live Vienna LAN Bug Bounties (Tapo milliwatts, JPEG `APP0` offset, Ring OAuth 406, `egui` RwLock deadlock, `Send` stream poisoning)<br>  - Layer 5: 6-Gate Definition of Done<br>- **5 Mandatory Guardrails / Traps** + **Blessed Crate Stack** + **PowerShell `justfile` Contract** | **Mandatory before writing or reviewing any Rust code in a fleet repo.** |
| **2. [FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md](./rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md)** | - **The 4-Bucket Fleet Triage Matrix** (~70% Pure Rust in Buckets A/B, ~15% Hybrid in Bucket C, ~15% Stay Python for CUDA/PyTorch in Bucket D)<br>- **Storming the Python Bastille (`PyPI -> Rust` Transpilation Doctrine)** & **4-Step `PyPI-as-Oracle` Playbook**<br>- **Top 35 Wave-1 Conversion Candidates (With Exact Reasons & Crates)**<br>- **Repos That Resist Conversion & Countermeasures** | **Mandatory when selecting repos to convert or porting a Python `pysomething` driver to Rust.** |
| **3. [EGUI_DESKTOP_UI_AND_PARITY.md](./rust-artcraft/EGUI_DESKTOP_UI_AND_PARITY.md)** | - **Retiring the 15-Layer Web/Backend Cruft Tower** (`FastMCP` + `FastAPI` + `Vite` + `Tailwind` + `React` + `WebView2`)<br>- **The Vindication of GPU-Rendered UIs (`egui`, `gpui`, `wgpu`)**<br>- **The 6-Step Mechanical UI Parity Loop (`UI_PARITY.md`)**, `egui_kittest` Golden PNG Snapshots & the `glyph_source_scan` Tofu (`□`) Guard<br>- **Pure-Rust Desktop Feature Parity & Polish Patterns (`egui 0.37`):** `Ctrl+Wheel` zoom, Light/Dark vector Sun/Moon topbar button, zero-dep GPU Energy & Weather charts, and hairline panel/card borders | **Mandatory when building or polishing `crates/<domain>-app` (`L3` `eframe`/`egui` desktop UI).** |
| **4. [ECOSYSTEM_IMPACT_SWIFT_AND_AGENTS.md](./rust-artcraft/ECOSYSTEM_IMPACT_SWIFT_AND_AGENTS.md)** | - **Apple Ecosystem & Swift (`macOS`/`iOS`/`visionOS`):** Metal via `wgpu`/`egui`/`gpui`, relegating Swift to a 0--5% `UniFFI` veneer<br>- **Large Multi-Contributor Agent Harnesses (`OpenCode`, `Codex CLI`, `Goose`, `Zed`):** How `rustc` + `Command::dispatch` turn a 500-contributor repo into a self-policing compiler | **Reference for cross-platform macOS/iOS strategy and multi-agent harness architecture.** |
| **5. [FLEET_CONVERSION_STANDARD.md](./rust-artcraft/FLEET_CONVERSION_STANDARD.md)** & **[REPCONV_SOP.md](../patterns/REPCONV_SOP.md)** | - **Shadow-Then-Swap vs. In-Place Conversion Modes**<br>- **The 70% Reusable Fleet Kernel** (`bridge.rs`, `llm.rs`, `vault.rs`, `registry.rs`, `devices-store`, `egui` shell)<br>- **Low-Token Automation Pipelines:** Mechanical boilerplate stamp, local Ollama `qwen3.8:27b` wire-spec distiller, 4-PR tiered factory, and parallel worktree swarms<br>- **The `repconv <repo>` Macro & 7-Point Cutover Retirement Checklist** | **Mandatory before running `repconv <repo>` or converting any legacy Python MCP repository.** |
| **6. [RELEASE_FACTORY.md](./rust-artcraft/RELEASE_FACTORY.md)** | - **Desired, not built (2026-10-18).**<br>- One shared release recipe and one shared agent-learnings log for every `rust-*-mcp`.<br>- Observed from public Craft `docs/releasing.md`. The canonical `craftrules` playbook stays private.<br>- Local cut on Goliath. No billable GitHub Actions on private repos. | **Read before cutting a Rust fleet release, or when asking for the ArtCraft release factory.** |
| **7. [ORACLE_LOOP.md](./rust-artcraft/ORACLE_LOOP.md)** | - **Original app is the oracle.** Click and drag, write the file out, diff the clone.<br>- **Same loop for UI.** Click and drag, screenshot the original, screenshot the clone, diff the frames.<br>- Start at one object. Grow to thousands, then millions. Floor only rises. A lone golden of our window is not the loop. | **Mandatory when claiming parity with a legacy app, a Craft engine, a file format, or a screen.** |

---

| **8. [CRAFT_COMMAND_BUS.md](./rust-artcraft/CRAFT_COMMAND_BUS.md)** | - **The two planes:** headless `run` (in-process engine) vs live `mcp --attach` / `--bridge` / `--connect` to `<app> --control PORT`.<br>- **The command registry** (`commands --json`, `describe`, JSON params) is the whole API.<br>- **Per-app flag table**, verified usage examples (Photo, Deck, Grid, Sound, Fig), client-config shapes, and traps (opt-in control, fails fast, syntax drift). | **Read before wiring a Craft app to an agent or claiming a live hands-in demo.** |

## 0. What Is Invalidated vs. What Replaces It: The Great Cruft Extinction (2026-10-17)

Most of the fleet's 2025--mid-2026 standards were written to paper over failure modes of the **two-language, 15-layer Python + JS/TS stack** (`Python` + `uv` + `FastMCP` + `FastAPI` + `Starlette` + `Uvicorn` + `Pydantic` + `Prefab UI` + `Node/Bun` + `React` + `Vite` + `Tailwind` + `Zustand` + `Biome` + `Tauri/WebView2`).

In a Pure-Rust ArtCraft repo, **that entire 15-layer tower is retired and replaced by a single language (`rustc` + `cargo`)**:

| Legacy Standard / Tooling Layer (Python + JS Era) | Status for Rust Repos | Replacement in Pure-Rust ArtCraft Architecture |
|---|---|---|
| **FastMCP 3.4+ / 4.x (`SOTA_REQUIREMENTS.md`, `fastmcp/*`)** | **INVALIDATED** | Replaced by L2 `rust-<domain>-mcp`: CLI-first `clap` binary (`--json`) + hand-rolled MCP `2024-11-05` stdio loop (`run_mcp_stdio`) over L1 `Command::dispatch`. |
| **FastAPI / Starlette / Uvicorn / Pydantic (`STARLETTE_NO_PYDANTIC_STANDARD.md`)** | **INVALIDATED** | **No HTTP backend sidecar, no Uvicorn server, no CORS middleware.** L3 (`<domain>-app`) invokes L1 (`<domain>-core::dispatch`) **directly in-process** in Rust memory. |
| **React / Vite / Tailwind / Zustand / Bun / Biome (`WEBAPP_SOTA_STANDARDS.md`, `BUN_STANDARDS.md`, `BIOME_STANDARDS.md`, `REACT_HARDENING.md`)** | **INVALIDATED** | Replaced by **Pure-Rust Immediate-Mode Native GUI (`egui` / `eframe`)** in L3 `<domain>-app`. Zero `node_modules/`, zero DOM/CSS, zero `package.json`, zero React `useEffect` race conditions, 60-144 FPS native GPU rendering, and browserless `egui_kittest` PNG snapshots. |
| **Tauri + WebView2 Wrapper (`TAURI_PRODUCTION_PITFALLS.md`)** | **SUPERSEDED** | `egui` / `eframe` renders directly via `wgpu`/`glow` without a 200 MB Chromium/WebView2 process or IPC serialization bridge, packaged via a current-user NSIS script (`installer/installer.nsi`). |
| **Port Claiming & Registry (`WEBAPP_PORTS.md`, `claim_ports.py`)** | **INVALIDATED** | **Zero ports claimed.** MCP runs over `stdio`; the `egui` desktop app calls L1 directly in-process with zero network sockets. |
| **Naked-PC `uv` + Node Bootstrap (`NAKED_PC_INSTALL_STANDARD.md`)** | **SUPERSEDED** | Two compiled `.exe` files run natively on any Windows/Linux/macOS box with **zero runtime dependencies** (no Python, no `uv`, no `.venv`, no Node/Bun). |
| **Ruff / `ty` / `uv.lock` / `bun.lock` (`RUFF_STANDARDS.md`, `UV_STANDARDS.md`)** | **INVALIDATED** | Replaced by `cargo clippy --workspace --all-targets --all-features -- -D warnings` (with `unwrap_used`/`expect_used`/`panic`/`todo`/`unimplemented` all `deny`), `cargo fmt --all --check`, and committed `Cargo.lock`. |
| **Portmanteau 1-Tool Consolidation (`TOOL_DESIGN_STANDARDS.md` §1)** | **REPLACED** | Replaced by the **ArtCraft Universal Command Bus**: 1:1 typed `Command` variants (`plug.get_stats`, `plug.toggle`, `hue.set_light`, `weather.now`, `bridge.speak`, `llm.chat`) shared identically between CLI subcommands, MCP `tools/list`, and L3 `egui` UI buttons. |
| **"No Stubs / Everything in One Pass" (`NEW_REPO_BUILD_COMPLETE.md`)** | **REPLACED** | Replaced by the **ArtCraft Tiered Scorecard (Tiers 1--4)** + explicit `Vendor::Demo` / `CamSource::Demo` deterministic oracles (`"vendor": "demo"` in JSON output) + keyless live endpoints (`weather.now`) for first-paint telemetry. |
| **19-Category Python/React `assfix` (`patterns/repo-assess-and-fix.md`)** | **SUPERSEDED** | Replaced by the **ArtCraft 6-Gate Definition of Done** ([CONTAINMENT_AND_CRATES.md §1 Layer 5](./rust-artcraft/CONTAINMENT_AND_CRATES.md)) and the **`repconv <repo>`** conversion macro ([`patterns/REPCONV_SOP.md`](../patterns/REPCONV_SOP.md)). Never fail a Rust repo for lacking `pyproject.toml`, `webapp/`, `package.json`, `fastmcp`, `prefab-ui`, or `/api/capabilities`. |

---

## 1. Measured Comparison (`devices-mcp` vs `rust-devices-mcp` `v0.4.0+`, 2026-10-17)

| Metric | Legacy Stack (`Python` + `FastMCP` + `FastAPI` + `Vite/Tailwind`) | Pure-Rust ArtCraft (`rustc` + `devices-core` + `egui`) |
|---|---|---|
| **Languages & Package Managers** | 3 languages (Python, TS, CSS) + `uv` + `bun` + `ruff` + `biome` | **1 language (`Rust`) + `cargo` + `clippy` + `rustfmt`** |
| **MCP + CLI Server Binary (`L2`)** | ~150 MB bundled interpreter (typical) | **0.81 MB (core) / ~11.5 MB (full 24-tool LAN+Cloud TLS+RTSP H.264+SQLite+USB cam)** |
| **Desktop App Binary (`L3`)** | Python sidecar + WebView2 (~250-500 MB RAM) + React bundle | **~31 MB standalone 14-view `eframe`/`egui` GPU `.exe` (15-30 MB RAM, zero WebView2)** |
| **Full Installer Bundle** | Multi-step `uv` + Node + WebView2 bootstrap (120 MB+) | **~16.8 MB single-file current-user NSIS installer (`installer.nsi`)** |
| **Cold CLI / Stdio Boot** | 2,000 - 4,000 ms (interpreter + imports) | **50 - 70 ms** (measured on Goliath) |
| **Desktop-to-Engine Transport** | React `fetch()` -> CORS -> FastAPI/Starlette -> Python | **Zero-hop in-process Rust function call (`devices_core::dispatch`)** |
| **Visual Regression Testing** | Requires Uvicorn + Vite + headless Chromium (`playwright`) | **Browserless `egui_kittest` golden PNG snapshots in `cargo test` + `glyph_source_scan` tofu guard** |

---

## 2. Quick-Reference: The 6-Gate Merge Bar for Pure-Rust Repos

Every commit or tier closure in a Pure-Rust ArtCraft repo MUST pass all 6 gates (full details in [CONTAINMENT_AND_CRATES.md](./rust-artcraft/CONTAINMENT_AND_CRATES.md)):

1. `cargo clippy --workspace --all-targets --all-features -- -D warnings` (zero warnings; `unwrap_used`, `expect_used`, `panic`, `todo`, `unimplemented` all `deny`).
2. `cargo test --workspace` (all unit + dispatch + round-trip serialization + `egui_kittest` snapshot + `glyph_allowlist` tests green; every bug fix ships with a regression test).
3. `cargo fmt --all --check` clean.
4. Byte-exact MCP stdio probe verified (`initialize` -> `tools/list` -> `tools/call`; `stdout` 100% pure JSON-RPC, logs only on `stderr`).
5. `Cargo.lock` committed; no `*.bak`, `*.cache`, `*.exe`, or `target/` artifacts in `git status`.
6. `CHANGELOG.md` checkpoint line updated.
