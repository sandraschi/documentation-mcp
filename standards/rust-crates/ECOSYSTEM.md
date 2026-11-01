# Rust Ecosystem: Maturity, Gaps & Key Sites

Honest map for agents planning rustifications: where Rust is strongest,
where it churns, and what's genuinely missing. Evidence over vibes —
every claim below names either a fleet battle (rust-devices-mcp, 2026-10-17)
or a structural fact.

## Strong (bet the repo on it)

- **Cargo itself** — best package manager in the industry (lockfiles that
  work, workspaces, features, offline builds). The toolchain story in
  TOOLCHAIN.md is 90% of why rustification pays off.
- **Async**: Tokio won (`tokio` 1.x). The old tokio/async-std split is over.
- **HTTP + serialization**: `reqwest` + `serde` are best-in-class, full stop.
- **CLI**: `clap` 4 (derive macros, shell completions free).
- **Errors**: `thiserror` + `anyhow` ended error-handling debates.
- **Crypto/TLS**: RustCrypto, `ring`/`aws-lc`, `rustls` — memory-safe TLS is
  a genuine strategic advantage (no OpenSSL CVEs).
- **SQLite**: `rusqlite` (bundled, FTS5 included).
- **Docs**: docs.rs (every version, auto-built) + doc tests (examples that
  run). Nothing in npm/PyPI compares.
- **Editions**: no Python-2/3 trauma, ever again.

## Maturing (use with pin discipline + churn budget)

- **GUI** (`egui`/`iced`/`slint`): all pre-1.0, renames happen (we adapted
  to egui 0.37's `CornerRadius`/integer-margin/`Panel` renames live).
  Accessibility lags the web badly. Mitigation: `glyph_allowlist`-style
  guards, kittest goldens, half a day per minor bump.
- **ORM three-way split**: `diesel` vs `sqlx` vs `sea-orm` — no consensus.
  Pick per repo (see DATABASE.md), don't re-litigate fleet-wide.
- **OpenAPI** (`utoipa`): good, younger than FastAPI's automatic docs.
- **Mobile** (Android/iOS): builds work, packaging is an adventure each time.
- **WASM**: solid targets (`trunk`, `wasm-pack`, leptos/dioxus), painful
  debugging.
- **Game engines** (`bevy`): powerful, pre-1.0, 10-minute clean builds.

## Real gaps (plan around them, don't pretend)

- **ML/AI is 10–100× smaller than Python.** `burn`, `candle`,
  `mistral.rs` exist; there is no transformers-equivalent with its model
  zoo, and training stays Python-side (Bucket D does this deliberately).
  For local inference prefer llama.cpp bindings / Ollama (Go) over
  heroic Rust ports.
- **Niche IoT vendor crates are missing.** We hand-rolled Hue (CLIP),
  Ring (OAuth2+2FA), Netatmo, and ONVIF fallbacks in rust-devices-mcp
  because nothing maintained exists; Tapo/Kasa live on single-maintainer
  crates (`tapo`, `kasa-rs`). Budget hand-roll time for every new vendor.
- **No commercial GUI designers.** No Figma-to-egui pipeline; UI is
  hand-coded against screenshot oracles (`docs/UI_PARITY.md` flow).
- **Single-maintainer risk** across the long tail. Mitigations: prefer
  multi-maintainer orgs (tokio team, serde), pin exact versions, vendor
  audit before adopting, and keep hand-roll fallbacks feasible (small
  REST APIs are ~100 lines with `reqwest`).
- **Apple-platform Rust**: works via `wgpu`/Metal, Swift interop is a thin
  `UniFFI` veneer — fine, but every macOS release needs a verification
  pass nobody schedules. Schedule it.
- **Enterprise SSO/SAML** libraries are thin; plan custom OIDC work for
  any repo that needs corporate login.

## Key sites

**Official**: [rust-lang.org](https://www.rust-lang.org) ·
[doc.rust-lang.org](https://doc.rust-lang.org) (Book, std, rust-by-example) ·
[crates.io](https://crates.io) · [docs.rs](https://docs.rs) ·
[play.rust-lang.org](https://play.rust-lang.org) ·
[users.rust-lang.org](https://users.rust-lang.org) (forum) ·
[blog.rust-lang.org](https://blog.rust-lang.org) ·
[rustsec.org](https://rustsec.org) (advisories)

**Pulse (community, essential)**: [this-week-in-rust.org](https://this-week-in-rust.org)
(the newsletter — subscribe) · [r/rust](https://www.reddit.com/r/rust/) ·
[awesome-rust](https://github.com/rust-unofficial/awesome-rust) ·
**[lib.rs](https://lib.rs)** (curated index with quality signals — better
discovery than crates.io search) · the **AreWe\* family** for maturity
checks before adopting: [areweguiyet.com](https://areweguiyet.com),
[arewewebyet.org](https://arewewebyet.org),
[arewelearningyet.com](https://www.arewelearningyet.com),
[arewegameyet.rs](https://arewegameyet.rs)

**Learning**: rustlings · Exercism Rust track · *Zero To Production*
(backend APIs) · *Command Line Applications in Rust* · *Rust for
Rustaceans* · [learn-wgpu](https://sotrh.github.io/learn-wgpu/) (GPU) ·
egui demo app (run the `egui` example — fastest way to learn the widgets).
