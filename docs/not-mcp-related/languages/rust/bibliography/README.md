# Rust Bibliography: Books, Docs, Landmark Codebases

**Parent:** [Rust Hub](../README.md)

Curated entry points. For Calibre-held books use `calibre-mcp` semantic search; entries below note what to search for.

---

## 1. Start here (official, free)

- The Rust Programming Language (The Book) - https://doc.rust-lang.org/book/ - ownership, structs, enums, lifetimes, testing. Read chapters 4, 6, 9, 10 first if converting from Python.
- Rust by Example - https://doc.rust-lang.org/rust-by-example/ - runnable snippets per concept.
- std docs - https://doc.rust-lang.org/std/ - authoritative API for Option, Result, Iterator, Arc/Mutex, channels.
- Cargo Book - https://doc.rust-lang.org/cargo/ - workspaces, profiles, targets, lockfiles.
- Clippy lints - https://rust-lang.github.io/rust-clippy/ - what each deny gate actually checks.
- rustup - https://rust-lang.github.io/rustup/ - toolchains, targets (aarch64-apple-darwin, wasm32-unknown-unknown).
- Tokio tutorial - https://tokio.rs/ - async, tasks, channels, timeouts.
- Serde - https://serde.rs/ - derive patterns for JSON/TOML/YAML/msgpack.
- reqwest - https://docs.rs/reqwest/ - client builder, timeouts, TLS backends.
- Clap derive - https://docs.rs/clap/ - Parser/Args/Subcommand patterns.
- egui + eframe - https://www.egui.rs/ , https://docs.rs/egui/ , https://docs.rs/eframe/ - immediate-mode widgets, tables (egui_extras), plots (egui_plot), kittest headless tests.
- wgpu - https://wgpu.rs/ , https://docs.rs/wgpu/ - Metal/DX12/Vulkan abstraction backing eframe; learn only if writing custom renderers.
- UniFFI (Mozilla) - https://mozilla.github.io/uniffi-rs/ - Rust core + thin Swift/Kotlin shell for Apple/Android-only surfaces.

## 2. Books (search Calibre for these titles)

- The Rust Programming Language (Klabnik/Nichols) - print companion to The Book.
- Programming Rust (Blandy/Orendorff/Tindall, O'Reilly) - systems depth, ownership internals, concurrency.
- Rust for Rustaceans (Blandy) - idiomatic patterns for experienced devs.
- Zero to Production in Rust (Longuinan) - backend service patterns that map cleanly onto L1 dispatch + L2 CLI design.
- Hands-On Concurrency with Rust - channels, actors, async runtimes beyond the tokio tutorial.

## 3. Landmark Rust codebases (proof, not hype)

Wave 1 - Python's own tooling rewritten in Rust by humans:

- astral-sh/ruff - Python linter/formatter (replaces Flake8/Black/isort). Proof that Rust can absorb Python ceremony and return 10-100x speedups.
- astral-sh/uv - Python installer/resolver (replaces pip/venv/poetry). Same team, same lesson.
- pydantic/pydantic-core - validation core in Rust via PyO3.
- pola-rs/polars - DataFrames in Rust.
- huggingface/tokenizers - tokenizers in Rust.

Wave 2 - agent harnesses and CLIs converting now:

- block/goose (block/goose) - Goose agent rewritten from Python into pure Rust (goose-core + goose-cli + desktop). Cited in fleet standard section 10.3 as the packaging/concurrency breaking point for Python harnesses.
- openai/codex (codex-rs) - Codex CLI rewritten from TypeScript/Node into pure Rust for zero-dep distribution and OS sandboxing.
- zed-industries/zed - editor + agent harness from scratch in Rust on custom gpui (Metal/Vulkan GPU UI). Runs circles around Electron editors; reference for gpui vs egui choice.
- sst/opencode - high-velocity TS/Bun + Go harness used in fleet standard as the counter-example: what rots under 500 contributors without a compiler gatekeeper, and how a Rust L1/L2/L3 re-architecture would fix it.

Rust-from-start creative suites (ArtCraft):

- storytold ArtCraft suite (Brandon Thomas) - FilmCraft, PhotoCraft, CADCraft and siblings. Methodology provenance for RUST_ARTCRAFT_STANDARD.md: strict containment harness + Universal Command Bus + Demo oracles + tiered scorecards letting parallel agent loops outship human C++/TS teams. L3 pattern source for eframe/egui over Command::dispatch.

Fleet pilot:

- rust-devices-mcp (D:\Dev\repos\rust-devices-mcp) - Tapo/Kasa/Shelly/Hue/Netatmo/Ring L1 modules ported from python-ring-doorbell/pyatmo/phue via the PyPI-as-oracle playbook; 0.81 MB binary; 50-70 ms boot; hand-rolled MCP 2024-11-05 stdio loop; Demo oracles; dual dot/underscore tool names.

## 4. Papers and background for the GPU-UI claim

- Zed gpui announcement posts and awesome-gpui list - why custom Metal/Vulkan text rendering beats Electron compositing at 120 Hz.
- eframe/egui architecture notes (emilk) - immediate-mode tradeoffs: per-frame layout cost vs zero retained-state sync bugs.
- Rust for Linux (rust-for-linux.com) - why the kernel accepted a second language: ownership as a compile-time borrow checker for C's biggest bug classes.
