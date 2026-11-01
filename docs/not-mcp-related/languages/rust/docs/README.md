# Rust Docs: History, Design, Syntax, Toolchain

**Parent:** [Rust Hub](../README.md) | **Fleet standard:** [RUST_ARTCRAFT_STANDARD.md](../../../standards/RUST_ARTCRAFT_STANDARD.md) | **Pilot:** [rust-devices-mcp](../../../projects/rust-devices-mcp/README.md)

This is the deep-dive companion to the Rust hub. Hub gives the "why convert tout banc".
This file gives the "what is Rust, precisely".

---

## 1. History: from Graydon Hoare's side project to fleet default

- **2006-2009: personal project to Mozilla sponsorship.** Graydon Hoare starts Rust as a personal project. Mozilla Research adopts it in 2009 as the implementation language for the Servo parallel browser engine. Goal from day one: C++ control and speed with memory safety, no garbage collector.
- **2010-2014: bootstrapping.** Self-hosted compiler (rustc written in Rust), package manager Cargo (2014), crates.io registry. Early adopters tolerate weekly breaking changes.
- **1.0 (2015-05-15): stability promise.** Backward compatibility guarantee for stable code. Editions system introduced later (2015, 2018, 2021, 2024) lets the language evolve without forking the ecosystem: old crates keep compiling, new code opts into new syntax.
- **2015-2020: systems beachhead.** Firefox ships Servo components (Stylo CSS, WebRender) in Rust. Dropbox, Cloudflare, Discord, Deno (2020, TypeScript runtime in Rust + Tokio + V8) prove Rust outside browsers.
- **2021: Rust Foundation.** AWS, Google, Huawei, Microsoft, Mozilla found an independent steward. Same year: Rust enters the Linux kernel (Rust for Linux), the strongest possible endorsement for a C replacement.
- **2021-2025 Wave 1 (see Hub section 7): humans rewrite Python's own tooling in Rust.** ruff (Flake8/Black/isort replacement), uv (pip/venv/poetry replacement, 10-100x faster), pydantic-core, polars, tokenizers. Python devs already run Rust binaries daily without knowing it.
- **2025-2026: the agent-harness split.** OpenAI rewrites Codex CLI from TypeScript into pure Rust (codex-rs). Block rewrites Goose from Python into pure Rust (block/goose: goose-core + goose-cli + desktop). Zed (zed-industries/zed) proves a from-scratch Rust editor with a custom GPU UI (gpui) outruns VS Code/Electron. ArtCraft (Brandon Thomas / storytold) proves parallel agent loops can ship 7 commercial creative suites (FilmCraft, PhotoCraft, CADCraft, etc.) in pure Rust faster than human teams ship them in C++ or TypeScript - provided the repo is a strict containment harness.
- **2026-10-17: fleet regime change.** With the rust-devices-mcp pilot (0.81 MB MCP+CLI binary, 50-70 ms cold boot, zero ports, deny-unwrap clippy gates), this fleet declares Pure-Rust ArtCraft (L1 core + L2 CLI/MCP + L3 egui app) the default for Bucket A and B repos. Python stays for Bucket D (PyTorch/CUDA) and stabilizes-behind cases in Bucket C. Full matrix in RUST_ARTCRAFT_STANDARD.md section 3.

Philosophy in one line: **control + speed + safety**. C++ gives the first two but not the third. Go/Java give safety via GC but sacrifice control and determinism. Rust gives all three by moving the checks to compile time.

---

## 2. Design: the three ideas that make everything else work

### 2.1 Ownership + borrowing + lifetimes (the borrow checker)

Every value has exactly one owner. When the owner goes out of scope, the value is dropped deterministically (no GC pause, no manual free).

```rust
fn main() {
    let s1 = String::from("hello"); // s1 owns the heap buffer
    let s2 = s1;                    // move: s1 is now invalid, no double-free possible
    // println!("{}", s1);          // compile error: value borrowed after move
    println!("{}", s2);
}
```

Borrowing rules: either one mutable reference (`&mut T`) OR any number of immutable references (`&T`), never both alive at once. The compiler tracks reference lifetimes so no reference outlives its referent (no dangling pointers, no data races at compile time).

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

The `'a` is a lifetime parameter: "the return lives at most as long as the shorter input". Humans found this annotation-heavy at first. In practice, lifetime elision covers 90 percent of functions, and the compiler suggests the rest.

### 2.2 No null, no exceptions: Option and Result

```rust
enum Option<T> { None, Some(T) }
enum Result<T, E> { Ok(T), Err(E) }
```

- `Option<T>` replaces null. You cannot dereference a maybe-absent value without handling `None`. `?`, `map`, `and_then`, `unwrap_or` keep it ergonomic.
- `Result<T, E>` replaces exceptions. Every fallible call returns `Result`. Library code defines structured errors with `thiserror`; application code propagates with `anyhow` or a domain error enum and `?`. Fleet rule: library code never panics; `panic!`, `unwrap()`, `expect()`, `todo!`, `unimplemented!` are denied by clippy in every ArtCraft repo.

### 2.3 Zero-cost abstractions, traits, enums

- Traits are interfaces with default methods and generics. `Iterator`, `From`, `TryFrom`, `Display`, `Serialize`/`Deserialize` (serde) compose without virtual-call overhead when monomorphized.
- Enums with payloads (`Command::PlugToggle { vendor, device_ip, state, creds }`) replace class hierarchies and stringly-typed dispatch. `match` is exhaustive: forget a variant and compilation fails. This is the backbone of the ArtCraft Universal Command Bus.
- Iterator chains (`vec.iter().map().filter().collect()`) compile to the same loop assembly as hand-written C. "What you do not use, you do not pay for."

---

## 3. Syntax tour for Python/JS converts

| Task | Python habit | Rust equivalent |
|---|---|---|
| Mutable binding | `x = 1; x = 2` | `let mut x = 1; x = 2;` (immutable by default) |
| String building | f-strings | `format!("hello {}", name)` |
| Dict/shape | `dict` | `struct` + `serde` derive |
| Missing value | `None` | `Option<T>` |
| Error | `raise` / `try` | `Result<T, E>` + `?` |
| Async fetch | `await httpx.get(...)` | `reqwest::get(...).await` inside `#[tokio::main]` |
| Shared counter | `threading.Lock` | `Arc<Mutex<T>>`, or `tokio::sync::mpsc` channels |
| CLI | `argparse` | `clap` derive (`#[derive(Parser)]`) |
| Test | `pytest` | `#[cfg(test)] mod tests` + `cargo test` |

Minimal CLI + JSON pattern used by every L2 binary:

```rust
use clap::Parser;

#[derive(Parser)]
struct Args {
    #[arg(long, default_value = "demo")]
    vendor: String,
    #[arg(long)]
    json: bool,
}

fn main() -> anyhow::Result<()> {
    let args = Args::parse();
    let out = serde_json::json!({ "vendor": args.vendor, "ok": true });
    println!("{}", serde_json::to_string(&out)?);
    Ok(())
}
```

Async dispatch pattern (L1):

```rust
pub enum Command { Status, PlugToggle { vendor: Vendor, device_ip: String, state: bool } }

pub async fn dispatch(cmd: Command) -> serde_json::Value {
    match cmd {
        Command::Status => serde_json::json!({ "ok": true }),
        Command::PlugToggle { vendor, device_ip, state } => {
            // bounded I/O: tokio::time::timeout + reqwest with .timeout()
            serde_json::json!({ "vendor": vendor.as_str(), "ip": device_ip, "state": state })
        }
    }
}
```

Macros you meet on day one: `println!`, `format!`, `vec!`, `derive(Debug, Clone, Serialize, Deserialize, Parser)`, `#[tokio::main]`, `#[derive(thiserror::Error)]`. Declarative `macro_rules!` and proc-macros (serde, clap, thiserror) generate code at compile time with full type checking.

---

## 4. Toolchain: rustc + cargo + clippy + rustfmt

- **rustc**: the compiler. Diagnostics are the gold standard for machine-actionable errors (exact span + suggestion). Agents iterate against rustc, not against production crashes.
- **cargo**: build, test, fmt, doc, publish in one tool. `Cargo.toml` (20-line TOML manifest) + committed `Cargo.lock` (reproducible binary builds). Profiles: dev (fast compile) vs release (LTO, strip, 0.8-4 MB binaries). Workspaces (`resolver = "2"`) hold L1/L2/L3 crates in one repo.
- **clippy**: 700+ lints. Fleet gate: `cargo clippy --workspace --all-targets --all-features -- -D warnings` with `unwrap_used`, `expect_used`, `panic`, `todo`, `unimplemented` set to `deny` at workspace and crate root. Every fallible op returns `Result`; slices use `.get(i)`, math uses `checked_*`/`saturating_*`, locks use `unwrap_or_else(PoisonError::into_inner)`.
- **rustfmt**: `cargo fmt --all --check` in CI. No style debates.
- **rustup targets**: `rustup target add aarch64-apple-darwin x86_64-unknown-linux-gnu wasm32-unknown-unknown` for cross builds. One codebase compiles to Windows exe, macOS Mach-O (Metal), Linux ELF, and WASM.
- **cargo audit / deny / bloat / nextest**: vulnerability scan, license/advisory gate, binary-size audit, faster test runner. Operational note: set shared `CARGO_TARGET_DIR` (for example `D:\Dev\cargo-target`) or run `cargo clean` after release cuts; a single workspace target dir is 2-6 GB and 100 repos must not each recompile tokio.

Editions (2015/2018/2021/2024) are opt-in per crate. Old dependencies keep compiling while new code uses new syntax. This is why a 2019 crate still builds under rustc 1.90+.

---

## 5. Async, safety fence, WASM, FFI

- **Async runtime: tokio.** Standardize on `tokio` (rt-multi-thread, macros, time). Bound every I/O with `tokio::time::timeout`; set `.timeout()` on every `reqwest::Client`. Never block the executor with `std::thread::sleep` or synchronous file reads inside async fns.
- **Hostile input fence (ArtCraft Layer 1).** All external bytes are hostile: CLI flags, MCP JSON args, socket bytes, JPEG headers. Validate lengths and char boundaries before indexing; validate device IDs/IPs/URLs (non-empty, bounded length) before dialing; never log secrets; map every failure into a typed domain error.
- **unsafe boundary.** Safe Rust covers everything except raw-pointer FFI, SIMD intrinsics, and zero-copy parsing. Rule: `unsafe` only at narrow FFI seams with a `// SAFETY:` comment explaining the invariant. Audit with `cargo geiger` or `cargo audit` conventions.
- **WASM.** `cargo build --target wasm32-unknown-unknown` plus `wasm-bindgen`/`wasm-pack` or `eframe` web template compiles L1 logic and even full egui apps to the browser from the same source. Heavy logic (image resize, crypto, parsers) runs client-side with no server round-trip.
- **FFI both directions.** Rust calls C via `bindgen` (Unitree SDK, media libs). Python calls Rust via `PyO3` (how pydantic-core and polars work). Swift shells call Rust via `UniFFI` (Path B for iOS widgets, Siri intents, Apple-only entitlements). In this fleet, PyO3 was the bridge era; direct-protocol Rust modules are the destination (see Hub section 7.4).

---

## 6. Where to go next

- Hub for strategy and numbers: [Rust Hub](../README.md).
- Hands-on path: [Learning](../learning/README.md) (borrow-checker survival, 4-step PyPI-as-oracle playbook).
- Copy-paste surface: [Reference](../reference/README.md) (blessed crates, egui vs React recipe, cheat sheets).
- Books and landmark codebases: [Bibliography](../bibliography/README.md).
