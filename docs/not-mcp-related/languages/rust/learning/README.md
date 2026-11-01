# Rust Learning: From "Too Complicated" to Tout Banc

**Parent:** [Rust Hub](../README.md) | **Deep dive:** [Docs](../docs/README.md) | **Cheats:** [Reference](../reference/README.md)

This page is the training path for humans and agents converting from Python/TypeScript to Rust in this fleet.

---

## 1. Why devs thought Rust was too complicated (and what actually happened)

Every complaint below was legitimate for a human typing at 60 wpm in 2018. Every one inverts when an agent writes code at 100+ tokens/sec inside a strict harness.

1. **"The borrow checker fights me."** Beginners hit move-after-use, mutable/immutable conflicts, and lifetime errors on day one. Python never says no; Rust says no 50 times before breakfast. Truth: the compiler is catching the use-after-free, double-free, and data race that would have been a 3 AM production page in C++ or a silent dict-mutation bug in Python. ArtCraft rule: do not fight it with `.clone()` spam or `Rc<RefCell<>>` everywhere; restructure to move ownership or message-passing (`mpsc`) instead.
2. **"Lifetimes are line noise."** `'a` annotations look intimidating. Truth: elision covers almost all functions; you write explicit lifetimes only at API boundaries (returning a borrow). The compiler suggests the annotation. Agents learn this in one session.
3. **"Error handling is verbose."** `Result<T, E>` everywhere, `match` on every call, no `try/except` blanket. Truth: verbosity is the feature. You cannot forget a failure mode; the compiler lists the unhandled variants. `?` plus `thiserror`/`anyhow` makes propagation one character. Fleet data: "if it compiles, it works" is statistical reality, not a meme.
4. **"Async is split-brained."** tokio vs async-std vs smol, `Send` bounds, executor pinning. Truth: standardize on tokio (fleet blessed stack) and the debate ends. Bound all I/O with timeouts; keep blocking work on `spawn_blocking`.
5. **"Compile times are slow, target/ eats my SSD."** True: a workspace with tokio + reqwest + eframe generates a 2-6 GB `target/` dir, and clean rebuilds take minutes. Mitigations used fleet-wide: shared `CARGO_TARGET_DIR` (for example `D:\Dev\cargo-target`), `sccache`, `cargo nextest`, and `cargo clean` after release cuts. Never kill a peer agent's Cargo file lock; wait or read statically.
6. **"No library for my device/API."** PyPI has a `pysomething` for everything; crates.io has abandoned 0.0.1 stubs from 2019. Truth: this is the PyPI-as-oracle opportunity, not a blocker. The Python package is 85 percent ceremony around 15 percent wire essence (URLs, headers, OAuth quirks, packet layouts). Read it as a spec, port the 15 percent into a 150-300 line zero-unwrap Rust module on reqwest/serde/tokio in one pass. Proven in rust-devices-mcp for Ring, Netatmo, Hue. Full playbook below.

---

## 2. Learning path (Python/TS dev, 5 stages)

- **Stage 0 - install and verify (30 min).** `rustup` stable, `cargo --version`, `cargo new hello`, `cargo run`, `cargo test`, `cargo clippy`, `cargo fmt`. Read the rustc error for a deliberate move-after-use bug; notice it points at both the move and the use.
- **Stage 1 - ownership gym (1 day).** The Book chapters 4, 5, 6, 8, 9, 10 (ownership, structs, enums, collections, errors, generics/traits/lifetimes). Exercises: fix 10 borrow-checker rejections without adding `.clone()`; convert a Python dict-munging function into a serde struct round-trip test.
- **Stage 2 - Result discipline (1 day).** Replace every `unwrap`/`expect`/`panic` with `Result` + `?` + `thiserror` error enum. Gate: `cargo clippy -- -D clippy::unwrap_used -D clippy::expect_used` passes. Write a hostile-input test (empty string, oversized slice index, poisoned mutex) proving graceful `Err`.
- **Stage 3 - async + HTTP (2 days).** tokio mini-redis style tasks, `mpsc` channels, `reqwest` client with `.timeout()`, `tokio::time::timeout` wrapper. Exercise: port a 50-line Python `requests` script into a Rust module with a `Vendor::Demo` deterministic path and golden JSON fixtures from the Python tests.
- **Stage 4 - ArtCraft slice (2 days).** Build the smallest L1/L2/L3: `Command` enum + `dispatch()` in L1, `clap` CLI with `--json` + hand-rolled MCP stdio loop in L2 (stdout is pure JSON-RPC, logs to stderr only), one `egui` window with a button calling `dispatch` in-process in L3. Gates: `just check`, `just test`, byte-exact `initialize -> tools/list -> tools/call` probe, `Cargo.lock` committed.

Primary sources: The Book, Rust by Example, rustlings exercises. Links in [Bibliography](../bibliography/README.md).

---

## 3. Borrow-checker survival guide (copy-paste rules)

- Default to move, not share. Pass ownership into functions that consume; return ownership out.
- Need shared read? `&T` or `Arc<T>`. Need shared mutation across threads? `Arc<Mutex<T>>` with `lock().unwrap_or_else(PoisonError::into_inner)` (never bare `unwrap`), or better: channels (`tokio::sync::mpsc`) so threads never share memory at all.
- Never index slices with `buf[i]` on external data; use `buf.get(i)` and map `None` to a typed error. Never slice strings by byte index; use char boundaries or `.chars()`.
- Use `checked_add`/`checked_mul`/`saturating_*` for offsets, lengths, power math.
- When the compiler suggests a lifetime or a `.clone()`, pause: the suggestion compiles but may hide a design smell. Prefer restructuring (narrower borrow scope, split struct, message pass) over cloning in hot paths.
- `match` exhaustively on every `Command` and every `Result`. Let the compiler list what you forgot.

---

## 4. The 4-step PyPI-as-oracle conversion playbook (fleet canonical)

Used for every Bucket A/B conversion where no mature Rust crate exists. Source: RUST_ARTCRAFT_STANDARD.md section 7.4.

1. **Recon the wire spec (read, never vendor).** Find the upstream `pysomething` source (site-packages or GitHub). Extract the 15 percent essence: base URLs, auth/refresh flows, custom headers, request/response JSON shapes, timeouts, error codes. Ignore the 85 percent ceremony (setup.py, wrapper classes, compat shims).
2. **Extract golden vectors.** Copy representative JSON/binary fixtures from the Python `tests/` dir (or capture live responses). These become deterministic Rust unit-test inputs. No live hardware needed for CI.
3. **Synthesize the L1 module under deny(unwrap_used).** Write `crates/<domain>-core/src/<vendor>.rs` on the blessed stack only (reqwest, serde, serde_json, tokio, uuid, chrono, aes/sha2 where needed). Map all failures into `<Domain>Error` (Timeout, Auth, Protocol, Offline, InvalidInput, Unsupported). Expose `Vendor::Demo` returning realistic constants tagged `"vendor": "demo"`.
4. **Verify parity and mint crates.** `just check` (clippy deny), `just test` against golden fixtures plus live hardware, byte-exact MCP stdio probe. When the module matures, factor it out as a standalone `<vendor>-rs` crate so the fleet becomes a factory for the crates crates.io was missing.

Trap to avoid: do not pull an unmaintained 0.0.x wrapper crate when the protocol is plain HTTP/REST, OAuth2, WebSocket, JSON-RPC, SCPI, or framed TCP/UDP/serial. Direct protocol always wins. Second trap: verify non-core crate signatures (nokhwa, cpal, btleplug, serialport) against the installed registry source immediately; LLM training cutoffs hallucinate renamed methods.

---

## 5. Capstone: your first tout-banc slice

Pick one tiny Bucket A repo (REST + JSON + SQLite, or CLI wrapper). Deliver Tier 1: workspace + deny gates + Command enum + Demo oracle + CLI --json + MCP stdio + L3 parity test + CHANGELOG line + release binary under 2 MB. If you can demo `initialize -> tools/list -> tools/call` byte-exact and toggle the same Command from both CLI and an egui button, you are ready to convert real repos.
