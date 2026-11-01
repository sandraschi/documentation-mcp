---
title: "Fleet Rustification & Repo Conversion Standard (Shadow-to-Cutover & Automation)"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-18
---

# Fleet Rustification & Repo Conversion Standard

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)  
**Operational SOP / Macro:** [`repconv` (`patterns/REPCONV_SOP.md`)](../../patterns/REPCONV_SOP.md)  
**Reference Blueprint:** [`rust-devices-mcp`](../../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp`, `v0.4.0+`)

---

## 1. Purpose & Scope

This standard governs how existing Python/FastMCP + React/Vite/Tailwind repositories in the 220-repo `*-mcp` fleet are converted to the **Pure-Rust ArtCraft 4-Crate Architecture** (`<domain>-core`, `<domain>-store`, `rust-<domain>-mcp`, `<domain>-app`) with:
1. **Zero loss of existing user configuration or credentials** (via `import.rs` + OS Credential Manager `vault.rs`).
2. **Minimum LLM token expenditure** (via the `repconv` 80%-boilerplate stamp + surgical wire-spec extraction).
3. **Deterministic quality gates** (`clippy -D warnings` with `deny(unwrap_used)`, `cargo test`, `egui_kittest` golden PNGs, `glyph_source_scan`, and live hardware/API probes).

---

## 2. Two Conversion Modes: Shadow Repo vs. In-Place Cutover

| Mode | Naming & Layout | When to Use | Cutover Lifecycle |
|---|---|---|---|
| **Mode A: Shadow-Then-Swap (Recommended for Live Daily-Driver Repos)** | Build in `D:\Dev\repos\rust-<domain>-mcp` while `D:\Dev\repos\<domain>-mcp` stays running in production. | Any repo currently wired into Claude Desktop / Cursor / NSSM / LAN automation (`devices-mcp`, `arr-mcp`, `plex-mcp`, `calibre-mcp`, `immich-mcp`, `obs-mcp`). | 1. Build `rust-<domain>-mcp` to `v0.4+` parity.<br>2. `import.rs` reads config/`.env`/caches directly from `../<domain>-mcp`.<br>3. Switch MCP client config to `rust-<domain>-mcp.exe mcp`.<br>4. Archive Python repo to `D:\Dev\repos\_archives\<domain>-mcp-python`. |
| **Mode B: In-Place Branch Conversion (For Standalone / Stateless / Dormant Repos)** | Branch `feat/rust-artcraft` inside `D:\Dev\repos\<domain>-mcp`, move legacy Python to `_legacy_py/` during port, then remove `_legacy_py/` at merge. | Stateless REST wrappers, CLI utilities, or bench instrument repos not running 24/7 as NSSM services (`multimeter-mcp`, `rss-mcp`, `fastsearch-mcp`, `xkcd-mcp`). | Merge `feat/rust-artcraft` to `main` once all 6 ArtCraft gates pass and tool names match 1:1. |

---

## 3. The Canonical 4-Crate Target Topology (Proven in `rust-devices-mcp` `v0.4.0+`)

Every converted repo adopts the 4-crate workspace proven in `rust-devices-mcp` (crates without time-series/historical state may omit `<domain>-store`, keeping 3 crates):

```text
rust-<domain>-mcp/
├── Cargo.toml                  # Virtual workspace + clippy deny(unwrap_used, expect_used, panic, todo, unimplemented)
├── Cargo.lock                  # Committed lockfile
├── justfile                    # PowerShell recipes: check / test / fmt-check / run-mcp / run-cli / build-release
├── AGENTS.md                   # ArtCraft containment rules + fleet context block
├── HANDOVER.md                 # Live session continuity state (updated at every Phase 0..5 checkpoint)
├── CHANGELOG.md                # Tiered milestone log
├── README.md                   # Measured binary/boot table, CLI + MCP tool tables, live verification table
├── docs/
│   ├── CONVERSION_DOSSIER.md   # Mandatory Phase 0 7-point forensic reconnaissance & 1:1 tool mapping (BEFORE any .rs code)
│   ├── CONVERSION_LOG.md       # Append-only timestamped Phase 0..5 execution, compiler & test audit trail
│   ├── PRD.md                  # Functional requirements F1..Fn with live/code-complete status
│   ├── UI_PARITY.md            # 6-step visual parity workflow
│   └── ASSESSMENT_<DATE>.md    # Post-conversion audit report
├── installer/
│   └── installer.nsi           # Hand-written current-user NSIS installer (Start Menu + Uninstaller, no UAC)
└── crates/
    ├── <domain>-core/          # L1: Domain drivers + Command::dispatch + shared fleet modules:
    │   └── src/
    │       ├── lib.rs          # Command enum, dispatch(), dispatch_future_is_send test
    │       ├── error.rs        # Typed <Domain>Error (InvalidInput, Offline, Timeout, Auth, Protocol, Unsupported)
    │       ├── creds.rs        # 4-level credential resolution + with_timeout_secs + classify_vendor_error
    │       ├── import.rs       # Zero-config reader for sibling Python <domain>-mcp (.env + config.json + config.yaml)
    │       ├── bridge.rs       # Reusable fleet crossconnect client (aiwatcher :10946, speech-mcp :10909, webhook)
    │       ├── llm.rs          # Reusable LLM chat client (gemma4:12b default on Ollama :11434, LM Studio, OpenAI, Anthropic)
    │       └── <driver>.rs     # The 2-6 domain-specific protocol modules (the ONLY code written from scratch!)
    ├── <domain>-store/         # L1 (Optional): Bundled rusqlite historian (%LOCALAPPDATA%/rust-<domain>-mcp/<domain>.db)
    ├── <domain>-mcp/           # L2: clap CLI (--json) + dual-aliased `mcp` stdio server (ArtCraft names + legacy portmanteau aliases)
    └── <domain>-app/           # L3: Pure-Rust eframe 0.37 / egui GPU desktop app:
        ├── src/
        │   ├── main.rs         # eframe native launcher + crash.log panic hook + `--smoke` headless CI flag
        │   ├── vault.rs        # Reusable Windows Credential Manager secret store (`keyring 4`)
        │   ├── registry.rs     # Reusable user-adopted target/endpoint registry (`devices.json`)
        │   └── app.rs          # Shared chrome (Topbar, Ctrl+Wheel zoom, Sun/Moon theme, Chat, Crossconnect,
        │                       # Settings, Help, Raw JSON) + domain pages + egui_kittest & glyph_source_scan tests
        └── tests/snapshots/    # Blessed egui_kittest PNG golden snapshots
```

---

## 4. The 70% Reusable Fleet Kernel (Why Conversions Do Not Start From Zero)

A critical lesson from `rust-devices-mcp` (`v0.1` -> `v0.4.0+`) is that **nearly 70% of a full-featured SOTA fleet repo is domain-agnostic infrastructure** that can be copied verbatim (with mechanical crate-name substitution) into every new Rust repo:

| Reusable Module (from `rust-devices-mcp`) | Lines | Reusability Across the Fleet |
|---|---:|---|
| `crates/devices-core/src/bridge.rs` | 221 | **100% verbatim.** Gives every Rust repo `bridge.event` (`aiwatcher`), `bridge.speak` (`speech-mcp`), and `bridge.webhook`. |
| `crates/devices-core/src/llm.rs` | 374 | **100% verbatim.** Gives every Rust repo `llm.chat` and `llm.models` (Ollama, LM Studio, OpenAI, Anthropic) with zero changes. |
| `crates/devices-core/src/error.rs` + `creds.rs` | 289 | **95% verbatim.** Timeout wrapper (`with_timeout_secs`), vendor error classifier, and device/target ID validator. |
| `crates/devices-app/src/vault.rs` + `registry.rs` | 151 | **95% verbatim.** OS Credential Manager integration (`keyring 4`) off the UI thread + JSON target registry. |
| `crates/devices-app/src/app.rs` (Shell & Chrome) | ~1,400 | **90% verbatim.** `harsh_visuals()`, `crisp_light_visuals()`, `apply_theme()`, vector Sun/Moon button, `Ctrl+Wheel` zoom + reset pill, 3D GPU icosahedron, `card_frame()`, `hero_kpi()`, `on_pill()`, `spark_chart()`, `Chat` page, `Crossconnect` page, `Settings` page, `Help` page, `Raw JSON` page, and `glyph_source_scan` test. |
| `crates/devices-mcp/src/main.rs` (`run_mcp_stdio`) | ~120 | **100% verbatim.** Infallible `MCP 2024-11-05` line-delimited JSON-RPC framing over `stdin`/`stdout`. |
| `installer/installer.nsi` + `justfile` | ~140 | **95% verbatim.** Parameterized only by binary/app name. |

**Consequence:** When converting `plex-mcp`, `arr-mcp`, `calibre-mcp`, or `oscilloscope-mcp`, the agent **never** wastes tokens re-inventing themes, zoom, OS vaults, LLM chat, speech crossconnect, MCP stdio loops, or NSIS scripts. The agent writes:
1. The domain protocol files in `crates/<domain>-core/src/`.
2. The domain `Command` variants in `lib.rs` and CLI/MCP entries in `main.rs`.
3. Every legacy page in `crates/<domain>-app/src/app.rs`, matched to screenshots of the running legacy webapp ([oracle loop](ORACLE_LOOP.md)). A 2 to 4 page shell is a failed conversion.

---

## 5. Novel Automation & Low-Token Conversion Pipelines

To convert 130+ Bucket A and Bucket B repositories without burning tens of millions of frontier LLM tokens, use these four complementary automation mechanisms:

### 5.1 Mechanism 1: The `repconv` Macro & Mechanical Boilerplate Stamp
Defined in [`patterns/REPCONV_SOP.md`](../../patterns/REPCONV_SOP.md), the `repconv <repo>` macro separates **mechanical scaffolding (0 LLM tokens)** from **protocol transpilation (focused LLM tokens)**:
- **Step 1 (Scripted Stamp):** Copies the workspace skeleton, lint gates, `bridge.rs`, `llm.rs`, `vault.rs`, `registry.rs`, `egui` shell, and `justfile` from `rust-devices-mcp` and renames `devices` -> `<domain>`.
- **Step 2 (Wire-Spec Extraction):** Reads the Python repo's tool signatures and protocol files, plus `sidebar.tsx`, each route, and that page's layout component. Never reads `node_modules/`, `.venv/`, or boilerplate tests. Screenshots of the running legacy UI are mandatory (`docs/parity/legacy/`).

### 5.2 Mechanism 2: Local Ollama (`gemma4:12b` / `gemma4:e4b`) Pre-Digestion ("Spec Distiller")
Before invoking a frontier agent session (OpenCode / Claude / Antigravity) on a large legacy Python repo:
- Run a zero-cost local Ollama pass using a **lightweight Gemma 4 model** (`rust-devices-mcp chat --provider ollama --model gemma4:12b` or `gemma4:e4b`) over the legacy Python `src/` files to emit `docs/WIRE_SPEC_DIGEST.md` containing:
  1. Every `@mcp.tool` name, parameter list, and return shape.
  2. Every external HTTP URL, header, auth scheme, SQLite table, or serial command string.
  3. Every environment variable read via `os.environ` / `pydantic_settings`.
- The frontier agent reads the **150-line `WIRE_SPEC_DIGEST.md`** instead of 8,000 lines of Python boilerplate -- reducing prompt input tokens by **85--90%**.

#### Why `gemma4:12b` / `gemma4:e4b` Beats `27B` Models on our Single RTX 4090 (24 GB VRAM Rule)
Never default to a `27B`--`35B` model (`qwen3.8:27b`, `gemma4:26b`, `qwen2.5:32b`) for `repconv` spec distillation or embedded `egui` app chat (`llm.rs`):

| Local Ollama Model on `Goliath` (`:11434`) | Weights (`Q4_K_M`) | + 32k KV Cache | + Win11 DWM / `wgpu` / Apps (`~3.5 GB`) | RTX 4090 (24 GB) Verdict |
|---|---:|---:|---:|---|
| **`gemma4:12b` / `gemma4:12b-fixed` (Recommended Default)** | **7.47 GB** | ~1.8 GB | ~12.8 GB total (**11.2 GB free!**) | **Zero VRAM scrubbing needed.** 110+ tok/s, instant load, coexists with `speech-mcp` and `egui` `wgpu` apps. |
| **`gemma4:e4b` (Fast Ultra-Light Alternative)** | **8.95 GB** | ~1.5 GB | ~14.0 GB total (**10.0 GB free!**) | **Zero VRAM scrubbing needed.** Ideal for rapid tool-signature extraction and low-latency house chat. |
| **`gemma4:e2b` (Sub-7 GB Featherweight)** | **6.67 GB** | ~1.2 GB | ~11.4 GB total (**12.6 GB free!**) | **Zero VRAM scrubbing needed.** Runs even while heavy 3D/video workloads are active on the 4090. |
| `qwen3.8:27b` / `gemma4:26b` *(Too Heavy for Unscrubbed 4090)* | 16.52--16.75 GB | ~4.2 GB | **24.2+ GB (Spills over 24 GB!)** | **Requires aggressive VRAM scrubbing** (killing background GPU processes) or spills into PCIe RAM at 8 tok/s. Overkill for wire-spec extraction. |

### 5.3 Mechanism 3: Issue / PR Tiered Factory Automation (`Tier 1` -> `Tier 4` PRs)
Instead of "one giant prompt to convert everything", automate repo conversions through four deterministic GitHub issues/PRs per repo (orchestrated by `robofang` or `git-github-mcp`):
- **PR #1 (`tier-1-scaffold`):** Mechanical stamp + `Command` enum + `Vendor::Demo` deterministic oracles + `just check` / `just test` green.
- **PR #2 (`tier-2-drivers`):** L1 domain protocol modules (`<domain>-core`) + `import.rs` reading the sibling Python `.env`/`config.yaml` + unit tests with golden JSON fixtures from the Python repo.
- **PR #3 (`tier-3-egui-ui`):** Domain views wired in `crates/<domain>-app/src/app.rs` + `egui_kittest` golden PNG snapshots + `glyph_source_scan` green.
- **PR #4 (`tier-4-live-cutover`):** Live LAN/API verification table in `README.md`, `installer/installer.nsi` package build, and `docs/ASSESSMENT_<DATE>.md`.

### 5.4 Mechanism 4: Parallel Git Worktree Agent Swarms
Because each `rust-<domain>-mcp` repo is an isolated directory (and shares a single `CARGO_TARGET_DIR=D:\Dev\cargo-target` so `tokio`, `reqwest`, `eframe`, and `rusqlite` compile **once** across the entire machine!), multiple OpenCode / Antigravity agents can convert 3--5 repos concurrently in separate directories with zero port conflicts (`WEBAPP_PORTS.md` is never touched) and zero compiled-dependency duplication.

---

## 6. Cutover & Legacy Python Retirement Checklist

A converted `rust-<domain>-mcp` repo officially replaces its legacy Python `<domain>-mcp` predecessor when all 7 cutover criteria are met:

- [ ] **1. Tool Surface Parity:** Every active MCP tool from the Python server is present in `rust-<domain>-mcp` `tools/list` (plus the standard fleet `bridge.*` and `llm.*` tools).
- [ ] **2. Zero-Config Import Verified:** `import.rs` automatically loads credentials and endpoints from the existing Python repo's `.env` / `config.yaml` / cache files without manual re-entry.
- [ ] **3. All 6 ArtCraft Gates Green:** `cargo clippy -- -D warnings`, `cargo test --workspace`, `cargo fmt --check`, MCP stdio JSON-RPC probe, `egui_kittest` snapshots, and `glyph_source_scan` all pass.
- [ ] **4. Live Hardware / API Oracle Proven:** At least one real end-to-end read query against the live target service/device is recorded in `README.md` §"Live verification".
- [ ] **5. Desktop App & Installer Built:** `devices-app` (or `<domain>-app`) launches cleanly, passes `--smoke`, and builds a `< 25 MB` current-user NSIS installer.
- [ ] **6. MCP Host Re-Pointed:** Claude Desktop / Cursor / OpenCode / Zed MCP config updated to invoke `rust-<domain>-mcp.exe mcp`.
- [ ] **7. Legacy Repo Archived & Port Reclaimed:** Stop any NSSM/sidecar service for the Python repo, release its port pair in `operations/WEBAPP_PORTS.md`, and move `D:\Dev\repos\<domain>-mcp` to `D:\Dev\repos\_archives\<domain>-mcp-python` (keeping `.env` migrated to the OS Credential Manager vault or user config dir).
