# Rust Toolchain Equivalents (PyPI / npm / bun → cargo)

One table for agents arriving from Python/JS. The headline: Rust has no
runtime, so half these rows *delete* tooling instead of replacing it.

| Job | Python | JS/Node | Rust | Notes |
|---|---|---|---|---|
| Package registry | PyPI | npmjs.com | **crates.io** | Plus **docs.rs**: auto-built docs for EVERY published version. Nothing like it exists in npm/PyPI — always read the docs.rs page before the README. |
| Install + resolve + build | `pip` / `uv pip` | `npm` / `bun install` | **`cargo`** (built in, no separate tool) | `Cargo.toml` = manifest, `Cargo.lock` = lockfile. Commit the lockfile for binaries/apps; gitignore it for libraries (opposite of npm habits — intentional). |
| Run a package one-off | `pipx` / `uvx` | `npx` | **No exact equivalent** (honest gap) | Closest: `cargo install <crate>` (binary lands in `~/.cargo/bin`), or `cargo install --git <url>`. For snippets: `evcxr` REPL (below). |
| Language runtime | `python3.x` | `node` / `bun` | **None** — compiled binaries | There is nothing to install on the target machine. This single fact deletes venvs, Docker slim images, and "works on my machine". |
| Version manager | `pyenv` / `uv python` | `nvm` / `fnm` | **`rustup`** | Toolchains (stable/beta/nightly), targets (`rustup target add`), components (clippy, rustfmt). Best version manager in the industry — no contest. |
| Isolated envs | `venv` / `.venv` | (bundled in node_modules) | **None needed** | Static linking + Cargo workspaces replace both venvs and monorepo hacks. |
| REPL / notebooks | `python -i` / Jupyter | `node -i` | **`evcxr`** (incl. Jupyter kernel) | Good for exploration, not a workflow pillar. |
| Lint | `ruff` | Biome / ESLint | **`clippy`** (official, 700+ lints) | Deny-gates live in `Cargo.toml` (`unwrap_used`, `expect_used`…), so agents can't lint-bypass. No config-file archaeology. |
| Typecheck | `mypy` / `pyright` | `tsc --noEmit` | **`rustc` itself** | No separate checker exists or is needed — types are proven at compile time, not audited after the fact. |
| Format wars | black / ruff-format / prettier / Biome | prettier / Biome | **`rustfmt`** | ONE format, effectively no config. Format debates are over. |
| Tests | `pytest` | vitest / jest | **`cargo test`** (built in) | Unit + integration + **doc tests** (examples in `///` comments that actually RUN — no analog anywhere else). GUI: `egui_kittest` headless PNG goldens. |
| Benchmarks | `pytest-benchmark` | `benchmark.js` | **`cargo bench` + `criterion`** (statistical, charts included) | Built-in harness covers smoke benches; criterion for serious numbers. |
| Coverage | `coverage.py` | `c8` | **`cargo-tarpaulin` / `cargo-llvm-cov`** | llvm-cov is the modern pick (exact line data, CI-friendly). |
| Security audit | `pip-audit` | `npm audit` | **`cargo-audit` + `cargo-deny`** | Audit = RustSec advisories; deny = licenses + banned crates + duplicate versions. Both belong in CI from day one. |
| Outdated deps | `pip list -o` | `npm outdated` | **`cargo-outdated` / `cargo-edit upgrade`** | Pin exact versions per repo; bump deliberately (pre-1.0 churn is real). |
| Bundle to exe | PyInstaller | `pkg` / `nexe` | **`cargo build --release`** | The compiler IS the bundler. Single file out, nothing to install. |
| Installer | NSIS scripts / electron-builder | electron-builder | **Tauri bundler or hand `makensis`** (as rust-devices-mcp does) | Current-user, no admin, Start Menu + uninstaller in ~60 lines of NSIS. |
| Task runner | `just` / `make` / npm scripts | `just` / npm scripts | **`just`** (same file works everywhere) or `cargo-xtask` (Rust-native, no extra install) | Fleet standard is `just`. |
| CI setup | `setup-python` / `setup-node` | `setup-node` / `setup-bun` | **`dtolnay/rust-toolchain` + `Swatinem/rust-cache`** | Cache action matters — clean Bevy-scale builds hit 10+ minutes without it. |
| API docs | Sphinx / mkdocs | TypeDoc | **`rustdoc` (`cargo doc`)** | Built in, and code examples are TESTED (doc tests). |
| Static musl / scratch Docker | `python:slim` images | `node:alpine` | **`FROM scratch` + musl target** | `x86_64-unknown-linux-musl` static binary, ~5 MB image. Windows services don't need this; Linux fleet boxes love it. |
| Vuln/malware DB | GitHub advisories | npm advisories | **RustSec** (`rustsec.org`) + `cargo-audit` | Smaller attack surface historically (no postinstall scripts in crates — install hooks don't exist). |

## The three honest gaps

1. **No `npx` equivalent.** One-off tool runs need `cargo install` first (slower first touch, then instant). Mitigation: a fleet `tools/` dir of prebuilt binaries, or thin `just` wrappers.
2. **No Jupyter-grade notebook culture.** `evcxr` works; the ecosystem around it is 1% of Jupyter's. Data-exploration stays Python-side (Bucket D) by design.
3. **Slower clean builds than `pip install`.** `cargo build` compiles the world the first time (aws-lc-sys C++ tax, Bevy scale). Mitigations: `Swatinem/rust-cache` in CI, workspace hygiene (never put Bevy in a leaf crate), `sccache` for teams.
