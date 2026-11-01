# Rust for the Tout-Banc Conversion: Fleet Hub 2026

**Version:** rustc 1.85+ (2024 edition), fleet gate per RUST_ARTCRAFT_STANDARD.md
**Context:** memory safety without GC, fearless concurrency, single-toolchain builds
**Role in fleet:** default for all new and converted Bucket A + B repos (REST, SQLite, CLI, LAN IoT, bench)
**Build:** `cargo` + `clippy -D warnings` + `rustfmt` (one language, one lockfile, zero ports)
**GUI:** `eframe` + `egui` over `wgpu` (React/Vite/Tailwind/WebView2 retired in L3)

> [!IMPORTANT]
> "Butter bei die Fische": this document is the Single Source of Truth for Rust in this fleet. It links global knowledge (history, syntax, crates) with local operational standards (ArtCraft L1/L2/L3, deny-unwrap gates, Demo oracles). Normative build rules live in standards/RUST_ARTCRAFT_STANDARD.md. This hub explains why they exist and how to work inside them.

---

## Table of Contents

1. [Executive summary: why tout banc](#1-executive-summary-why-tout-banc)
2. [History in 10 dates](#2-history-in-10-dates)
3. [Syntax and usage: the 30-minute mental model](#3-syntax-and-usage-the-30-minute-mental-model)
4. [Libraries and crates: what you actually build on](#4-libraries-and-crates-what-you-actually-build-on)
5. [egui + wgpu as the React replacement](#5-egui--wgpu-as-the-react-replacement)
6. [Why LLMs love Rust (and why that matters more than dev taste)](#6-why-llms-love-rust-and-why-that-matters-more-than-dev-taste)
7. [Why devs thought Rust was too complicated (and the honest residue)](#7-why-devs-thought-rust-was-too-complicated-and-the-honest-residue)
8. [Proof: tools already converted, apps born in Rust](#8-proof-tools-already-converted-apps-born-in-rust)
9. [Fleet conversion: buckets, tiers, playbook](#9-fleet-conversion-buckets-tiers-playbook)
10. [Where to go next](#10-where-to-go-next)

---

## 1. Executive summary: why tout banc

Across 187 `*-mcp` repos the legacy Python + FastMCP + FastAPI + Vite/Tailwind + Tauri pattern cost roughly 450 MB disk per repo (venv + node_modules + dist), 250-500 MB RAM per open app (interpreter + Uvicorn + Chromium), 2-4 second cold boots, port-pair claiming, CORS, sidecar zombies, and duplicate Pydantic/TS/React types for every command. Agents spent 70 percent of tokens on plumbing ceremony, and dynamic typing let hallucinated attributes pass until production.

Pure-Rust ArtCraft (pilot: rust-devices-mcp, 2026-10-17) measured: **0.81 MB** MCP+CLI binary, **50-70 ms** cold boot, **15-30 MB** native GUI, **zero ports** (stdio + in-process calls), **1 toolchain** (cargo + clippy + rustfmt). One `Command` enum variant serves CLI `--json`, MCP `tools/call`, and the egui button through the same `dispatch()` function, so the three surfaces can never disagree.

Policy: Buckets A (REST/Cloud/SQLite/System/CLI, about 55 percent) and B (clean LAN hardware, SCPI, serial, about 15 percent) convert to pure Rust. Bucket C (host-app embedded Python like Blender/FreeCAD, fast-moving reverse-engineered cloud crypto) splits: Rust server plus thin in-host listener, or stay Python until the protocol stabilizes. Bucket D (PyTorch/CUDA training, multimodal ML) stays Python, optionally behind a Rust front door. Full matrix in RUST_ARTCRAFT_STANDARD.md section 3.

---

## 2. History in 10 dates

- **2006:** Graydon Hoare starts Rust as a personal project. Goal: C++ speed and control without memory unsafety, no garbage collector.
- **2009:** Mozilla Research sponsors Rust for the Servo parallel browser engine.
- **2014:** Cargo + crates.io ship. One build tool, one registry, from early on.
- **2015-05-15:** 1.0 stable with a backward-compat promise. Editions (2015/2018/2021/2024) later allow language evolution without forking old crates.
- **2017-2019:** Firefox ships Rust components (Stylo, WebRender). Deno bets on Rust + Tokio + V8.
- **2021:** Rust Foundation (AWS, Google, Huawei, Microsoft, Mozilla). Rust enters the Linux kernel. The "toy language" debate ends.
- **2021-2025 Wave 1:** Humans rewrite Python's own core in Rust: ruff (lint/format), uv (install/resolve, 10-100x faster than pip), pydantic-core, polars, tokenizers. Every Python dev in this fleet already runs Rust daily.
- **2024-2025:** Zed (Rust + custom gpui over Metal) proves a from-scratch editor beats Electron. ArtCraft (Brandon Thomas / storytold: FilmCraft, PhotoCraft, CADCraft and siblings) proves agent loops inside a strict harness ship commercial creative suites in pure Rust faster than human teams ship them in C++ or TypeScript.
- **2025-2026 Wave 2:** Flagship harnesses convert. OpenAI rewrites Codex CLI from TypeScript into Rust (codex-rs). Block rewrites Goose from Python into Rust (goose-core + goose-cli + desktop) after Python packaging and async concurrency break down at scale.
- **2026-10-17:** Fleet regime change. rust-devices-mcp pilot validates the ArtCraft 3-tier pattern (L1 core + L2 CLI/MCP + L3 in-process app, deny-unwrap clippy, Demo oracles, 6-gate done-definition). RUST_ARTCRAFT_STANDARD.md supersedes Python/FastMCP/Starlette/port-claiming rules for every repo with a root Cargo.toml.

Design lineage: C++ gives control plus speed but not safety. Java/Go give safety via GC but not control or determinism. Rust gives all three by checking ownership, borrowing, lifetimes, and exhaustive matching at compile time. Abstractions (traits, generics, iterator chains) are zero-cost: what you do not use, you do not pay for.

Details: [docs/](docs/README.md) sections 1-2.

---

## 3. Syntax and usage: the 30-minute mental model

Three ideas explain 90 percent of Rust:

**Ownership.** Every value has one owner; dropping the owner frees the value deterministically. Moves (`let s2 = s1`) invalidate the old binding at compile time. No double-free, no GC pause.

**Borrowing + lifetimes.** Either one `&mut T` or any number of `&T`, never both live at once. The compiler rejects dangling references before the binary exists. Elision covers most functions; explicit `'a` appears only where a return borrows from inputs.

**No null, no exceptions.** `Option<T>` replaces null; `Result<T, E>` replaces exceptions. Library code defines structured errors with `thiserror`, apps propagate with `?`, fleet clippy denies `unwrap`/`expect`/`panic`/`todo`. You cannot forget a failure mode; the compiler lists it.

Everyday mapping for converts:

- `let` / `let mut` (immutable by default), `format!` instead of f-strings, `struct` + `serde` derive instead of dicts, `match` instead of isinstance chains, `#[derive(Parser)]` (clap) for CLIs, `#[tokio::main]` + `reqwest` with `.timeout()` for async fetch, `Arc<Mutex<T>>` or `mpsc` channels for sharing.
- The fleet triple-face: one `Command::PlugToggle { vendor, device_ip, state }` variant, one `dispatch()` function, three callers (CLI flag parser, MCP stdio handler, egui button). Types are shared, not duplicated across Python/TS/CSS.

Full tour with snippets: [docs/](docs/README.md) section 3. Hands-on path: [learning/](learning/README.md).

---

## 4. Libraries and crates: what you actually build on

crates.io holds 150k+ crates, but this fleet standardizes on a blessed dozen so 100 repos do not diverge. Rule: if the protocol is HTTP/REST, OAuth2, WebSocket, JSON-RPC, SCPI, or framed TCP/serial, hand-roll a 150-300 line module on the blessed stack rather than pulling an abandoned 0.0.x wrapper.

- **Foundation:** serde + serde_json (all types), tokio (async runtime, timeouts), reqwest (HTTP/OAuth, always with `.timeout()`), chrono + uuid (time, IDs, hardware fingerprints), thiserror + anyhow (typed errors).
- **L2 CLI:** clap 4 derive. Every command supports `--json` so agents script the binary without parsing human text.
- **Storage:** rusqlite bundled (zero external DLL on Windows) for embedded SQL/RAG.
- **Hardware edge:** tokio-serial/serialport (SCPI :5025, Modbus), windows-sys (native APIs), aes/sha2/hmac/base64 (MiIO-style framing, signing). Media/USB crates (nokhwa, cpal, hidapi, btleplug) require checking installed-registry signatures first; training cutoffs hallucinate renamed methods.
- **L3 GUI:** eframe + egui + egui_extras (tables/images) + egui_plot (telemetry). wgpu underneath on DX12/Vulkan/Metal. Alternatives: iced (Elm-style), gpui (Zed-class text), tauri v2 only as legacy bridge. User plugins via extism/mlua/rquickjs sandboxes so core stays zero-panic.
- **Cross targets:** same source compiles to Windows exe, macOS Metal Mach-O, Linux ELF, and wasm32 WASM (browser or plugin) via rustup targets.

Table with versions plus cheat sheets: [reference/](reference/README.md) sections 1 and 4.

---

## 5. egui + wgpu as the React replacement

(Note: "egpu" in the request is read as wgpu, the GPU abstraction under eframe/egui. There is no egpu crate in this stack; eframe/egui sit on wgpu/glow.)

Legacy price for one button: 15 layers across 3 languages (driver, FastMCP wrapper, Pydantic schema, FastAPI route, Uvicorn, ports, CORS, TS fetch, Zustand, useEffect, tsx, Tailwind, Vite/node_modules, Biome/tsc, Tauri IPC + WebView2). ArtCraft price:

```rust
if ui.button("Toggle Plug").clicked() {
    self.last_result = Some(run(Command::PlugToggle {
        vendor: self.vendor, device_ip: self.ip.clone(),
        state: !self.is_on, creds: self.creds.clone(),
    }));
}
```

Scoreboard (measured on Goliath): disk 450 MB vs 2-4 MB exe; RAM 250-500 MB vs 15-30 MB; latency localhost-HTTP vs sub-ms in-process; authoring 6 files in 3 languages vs 1 variant + 5 UI lines compiler-checked end to end; UI tests Playwright + servers vs `egui_kittest` inside `cargo test` in milliseconds; platforms WebView2 quirks vs native Windows/Linux/macOS-Metal plus optional WASM from the same code.

Conceptual core: immediate-mode GPU UI treats the app like a 120 FPS game frame. Layout in flat Rust arrays, upload one vertex buffer, draw in under 0.5 ms. The UI is a pure function `fn update(&mut self, ctx: &egui::Context)` of current structs every frame, so there is no shadow DOM to go stale, no CSS cascade, no callback spaghetti. Critics who asked "who does UI on the GPU?!" were running Chromium, which rasterizes HTML/CSS into GPU triangles anyway after 15 million lines of Skia/Blink/Dawn plus DOM, CSS, and JS GC. egui/gpui delete the middleman, which is why agent loops survived building 7 creative suites without drowning in frontend state bugs.

Default L3 is eframe/egui. Pick gpui only for Zed-class text editors, iced for Elm-style retained widgets, tauri only while retiring a legacy React app. Full comparison: [reference/](reference/README.md) section 2 and RUST_ARTCRAFT_STANDARD.md section 8.

---

## 6. Why LLMs love Rust (and why that matters more than dev taste)

Core axiom from the fleet standard: **Python optimizes human typing speed; Rust optimizes automated verification speed.** When agents emit 100+ tokens/sec, typing speed is worth zero and compile-time proof is worth everything.

- **Closed loop vs open loop.** Python parses even when attribute names, dict keys, or None branches are hallucinated; bugs hide until production. `rustc` + `clippy -D warnings` + `deny(unwrap_used)` act as an adversarial prover: the agent loops until every branch and error path is sound before anything runs.
- **No runtime dependency solver on target.** Python agents fight `aiohttp<4` vs `pydantic<2` venv deadlocks per machine. Rust compiles to a static exe against reqwest + serde; nothing to resolve where it runs.
- **Architecture drift becomes compile errors.** Agents cannot silently mutate shared dicts, leak state across tasks, or `print()` debug text onto MCP stdout: ownership, crate boundaries, exhaustive `Command` matching, and the stderr-only stdio invariant turn drift into immediate failures with line numbers and fixes.
- **Python libraries become free specs.** The 15 percent wire essence inside any `pysomething` package (URLs, headers, OAuth quirks, framing) is plain-text machine-readable spec. Agents transpiled python-ring-doorbell, pyatmo, and phue into zero-unwrap Ring/Netatmo/Hue Rust modules in single passes, verified against golden JSON fixtures from the Python tests. What took humans years of mitmproxy captures takes agents minutes of reading.

Net: in 2026 every human contributor has an agent writing the PR, and agents already know Rust. `rustc` + `clippy` become an incorruptible reviewer letting 500-contributor repos merge at speed without rotting into runtime exceptions. Long version: RUST_ARTCRAFT_STANDARD.md sections 7 and 10.

---

## 7. Why devs thought Rust was too complicated (and the honest residue)

Fair history, straight:

1. **Borrow checker hostility.** Day-one move/borrow/lifetime rejections with no Python equivalent. Newcomers papered over them with `.clone()` spam or `Rc<RefCell<>>`, then blamed the language for the slowdown.
2. **Lifetime noise.** `'a` annotations look scary; the reason they exist (no dangling refs) is invisible until you have debugged a use-after-free in C++.
3. **Verbose errors.** `Result` everywhere felt bureaucratic next to `try/except`. The payoff (unforgettable failure modes, "if it compiles it works") only lands after the first production incident it prevents.
4. **Async fragmentation.** tokio vs async-std vs smol plus `Send` bounds, while Python had one asyncio and JS had one event loop.
5. **Slow builds, giant target/.** 2-6 GB per workspace, minute clean rebuilds, Cargo lock fights between parallel agents.
6. **Missing long-tail crates.** PyPI had a library for every $20 plug; crates.io had 2019 stubs. Hand-rolling felt like going backwards.

What remains true after the harness: 5 and parts of 4 are real operational costs, handled by shared `CARGO_TARGET_DIR`/`sccache`/`nextest`/`cargo clean` discipline and a tokio-only rule. Items 1-3 and 6 invert under agents: the compiler is the fastest reviewer you have, and the missing crate is a 10-minute port, not a blocker. Survival rules and the 4-step PyPI-as-oracle playbook: [learning/](learning/README.md) sections 3-4.

---

## 8. Proof: tools already converted, apps born in Rust

**Wave 1 - Python's own toolchain, rewritten by humans:**

- **ruff** (astral-sh/ruff): Flake8 + Black + isort in one Rust binary. The fleet linter.
- **uv** (astral-sh/uv): pip + venv + poetry in one Rust binary, 10-100x faster. The fleet installer.
- **pydantic-core, polars, tokenizers**: validation, DataFrames, tokenization cores in Rust via PyO3. Python kept the API; Rust took the hot path.

**Wave 2 - harnesses converting now:**

- **Block Goose (block/goose):** agent harness rewritten from Python into pure Rust (goose-core + goose-cli + desktop) after packaging and async tool concurrency broke down at scale. The closest public analog to this fleet's own tout-banc bet.
- **OpenAI Codex CLI (codex-rs):** rewritten from TypeScript/Node into pure Rust for zero-dep distribution, native sandboxing, reliable TUI streaming.
- **This fleet (rust-devices-mcp):** Tapo/Kasa/Shelly/Hue/Netatmo/Ring ported from `pysomething` packages into zero-panic L1 modules; 0.81 MB; 50-70 ms boot; byte-exact MCP stdio probe.

**Born in Rust (never converted, built the pattern):**

- **Zed (zed-industries/zed):** editor + agent harness from scratch in Rust on custom **gpui** (GPU text over Metal/Vulkan, 120 Hz). Built by Atom/Electron veterans who deliberately abandoned Electron. Reference pick when egui is not enough for text.
- **ArtCraft suite (storytold / Brandon Thomas): FilmCraft, PhotoCraft, CADCraft (+ siblings, 7 apps):** commercial creative suites built by parallel agent loops in pure Rust on **eframe/egui over wgpu** plus the Universal Command Bus, Demo oracles, and tiered scorecards. Methodology provenance for the entire fleet standard. Proof that agents plus a strict harness outship human C++/TS teams on real GUI products.
- **Supporting cast agents already run on Rust:** ripgrep (ignore + grep-searcher), tree-sitter, tokenizers, git libs (gix/git2), rusqlite. A pure-Rust harness calls them in-process with zero serialization; a TS/Python harness marshals megabytes across FFI per query.

Sources and links: [bibliography/](bibliography/README.md) section 3.

---

## 9. Fleet conversion: buckets, tiers, playbook

**Triage first (RUST_ARTCRAFT_STANDARD.md section 3).** Bucket A: 100 percent pure Rust (highest ROI, only reqwest/rusqlite/process/windows-sys needed). Bucket B: 100 percent pure Rust (direct SCPI/serial replaces NI-VISA/pyvisa; probe-rs for JTAG/SWD). Bucket C: split (Rust server + 100-line in-host Python listener over TCP/pipe; keep Python for undocumented rotating cloud crypto). Bucket D: stay Python (or Rust front door + Python GPU worker; never rewrite PyTorch/CUDA for its own sake).

**Shape (section 2).** Every converted repo is a Cargo virtual workspace: `crates/<domain>-core` (L1: protocols, creds, error taxonomy, `Command::dispatch`, zero UI/CLI/MCP-transport deps), `crates/<domain>-mcp` (L2: clap CLI with `--json` + `mcp` stdio subcommand sharing `dispatch`, stdout pure JSON-RPC, stderr-only logs), `crates/<domain>-app` (L3: eframe/egui calling `dispatch` in-process, parity test proving GUI equals MCP). Workspace + crate roots deny unwrap/expect/panic/todo. Hostile-input fence on all external bytes. `Cargo.lock` committed. `CHANGELOG.md` per gate.

**Rollout (section 2, Layer 4).** Tier 1 (v0.1): structure, gates, Command bus, Demo oracles, CLI+MCP, parity test, sub-2 MB binary. Tier 2 (v0.2): live LAN/cloud reads + actuators with bounded timeouts. Tier 3 (v0.3): media frames with header validation, metadata over MCP (never base64 blobs). Tier 4 (v1.0): full native window + signed installer + benchmark table.

**Done means (Layer 5):** clippy zero-warning, full `cargo test` green with regression tests, fmt clean, byte-exact `initialize -> tools/list -> tools/call` probe, no bak/cache/exe/target in git status, changelog line.

**Convert one repo (section 7.4):** recon the `pysomething` wire spec, extract golden fixtures as oracle, synthesize the L1 module under deny-unwrap with a Demo path, verify parity and factor mature modules out as standalone `*-rs` crates. Never let "no crate exists" block; never vendor a dead 0.0.x wrapper for a plain HTTP/serial protocol.

---

## 10. Where to go next

- **Build rules (normative):** [standards/RUST_ARTCRAFT_STANDARD.md](../../standards/RUST_ARTCRAFT_STANDARD.md) - invalidation table, 5-layer harness, blessed stack, justfile invariants, Apple/Swift and OpenCode analyses.
- **Deep dive:** [docs/](docs/README.md) - history, ownership/lifetimes/Result, syntax tour, toolchain, async/fence/WASM/FFI.
- **Hands-on:** [learning/](learning/README.md) - borrow-checker survival, 5-stage path, PyPI-as-oracle playbook, capstone slice.
- **Copy-paste:** [reference/](reference/README.md) - blessed crates, egui-vs-React recipe, triple-face parity, cheat sheets.
- **Read/watch:** [bibliography/](bibliography/README.md) - Book, papers, ruff/uv/Goose/Codex/Zed/ArtCraft/rust-devices-mcp links.
- **Pilot to crib from:** [projects/rust-devices-mcp](../../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp`).

---

**Maintainer:** Sandra S.
**Last updated:** 2026-10-17 (tout-banc rewrite; supersedes 2026-02-13 robotics/PyO3 edition)
**Status:** SOTA 2026 compliant. ASCII-only by fleet hygiene rule.
