---
title: "Repo Rustification & Conversion SOP (repconv)"
category: pattern
status: active
audience: all-agents
last_updated: 2026-10-18
---

# Repo Rustification & Conversion (`repconv`) -- Low-Token SOP

**Trigger:** `repconv <repo>` or `rustify <repo>`  
**Reference Macro:** `standards/rules/agentic_macros.md` -> `repconv`  
**Canonical Standard:** [`standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md`](../standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md)  
**Golden Blueprint Repo:** `D:\Dev\repos\rust-devices-mcp` (`v0.4.0+`)

---

## Why `repconv` Exists (The Token-Miser Rule)

Converting a Python/FastMCP + React/Vite/Tailwind repository to Pure-Rust ArtCraft **the naive way** (having an LLM read 60 Python/React files and write 10,000 lines of Rust from scratch) wastes **300,000+ tokens** per repo rediscovering `Cargo.toml` lints, `eframe` themes, `Ctrl+Wheel` zoom, vector Sun/Moon icons, `keyring` OS vaults, `bridge.rs`, `llm.rs`, and `MCP 2024-11-05` stdio framing.

**`repconv` cuts token usage by ~80%** by enforcing two rules:
1. **Never Read Legacy Cruft. Do run the UI oracle.** You are **FORBIDDEN** from reading `node_modules/`, `package.json`, `tailwind.config.*`, `.venv/`, `start.ps1`, or `tauri.conf.json`. You **MUST** run the [oracle loop](../standards/rust-artcraft/ORACLE_LOOP.md) against the running legacy webapp before any `egui` page is written: screenshot every page and every primary gesture (click, drag, select, open a dialog), and read that page's layout file (`sidebar.tsx`, the route file, and the one component that places its controls). A name list is not a layout. The Rust app must come out near-identical: same pages, same groups, same order, same labels, same gestures. A shell with 2 to 4 invented pages is a failed conversion.
2. **Clone the 70% Kernel from `rust-devices-mcp`, Write Only the 30% Domain Logic:** Every fleet Rust repo shares the exact same L1/L2/L3 containment harness, `bridge.rs`, `llm.rs`, `vault.rs`, `registry.rs`, `egui` dark/light shell, `justfile`, and `installer.nsi` proven in `D:\Dev\repos\rust-devices-mcp`.

---

## Gürtel und Hosenträger (Belt-and-Suspenders) Non-Negotiable Principles

Because `repconv` will be executed across 130+ fleet repositories by multiple agents, it enforces **three non-negotiable resilience invariants**:
1. **No Code Before Due Diligence (`docs/CONVERSION_DOSSIER.md` Gate):** You are **FORBIDDEN** from writing or compiling a single `.rs` file until Phase 0 completes a 7-point forensic reconnaissance of the legacy repo and commits `docs/CONVERSION_DOSSIER.md`.
2. **Continuous Self-Documentation & Checkpoint Commits (`docs/CONVERSION_LOG.md` + `HANDOVER.md`):** Every phase (`Phase 0` .. `Phase 5`) ends by appending a timestamped audit entry (commands run, test/clippy counts, findings) to `docs/CONVERSION_LOG.md`, updating `HANDOVER.md`, and creating a git checkpoint commit. If a session crashes or hits a quota/context limit mid-flight, the next agent resumes in 10 seconds with zero lost work.
3. **100% Read-Only Legacy Fence:** While building `D:\Dev\repos\rust-<name>-mcp` (Shadow Mode), the existing `D:\Dev\repos\<name>-mcp` repository and its running services/databases are **100% READ-ONLY**. Never edit, move, stop, or lock files in the legacy repo during conversion.

---

## Phase 0: Forensic Due Diligence & Pre-Build Gate (Mandatory First Commit)

**Hard Gate:** Do NOT start Phase 1 until `D:\Dev\repos\rust-<name>-mcp\docs\CONVERSION_DOSSIER.md` and `docs\CONVERSION_LOG.md` are written and committed (`git commit -m "docs(phase-0): conversion dossier and pre-flight audit"`).

### 0A. 7-Point Due-Diligence Reconnaissance (Token-Fenced)
Without reading `node_modules/` or `.venv/`, inspect the legacy repo `D:\Dev\repos\<name>-mcp` and document all 7 items in `docs/CONVERSION_DOSSIER.md`:

1. **Bucket & Hidden Binary / Privilege-Split Audit:**
   - Check root and subdirectories (`service/`, `native/`, `bin/`, `src-tauri/`, `zed-extension/`).
   - Does the repo include an install-once elevated `LocalSystem` C++/C# Windows service over a named pipe (like `fastsearch-mcp`'s `FastSearchServiceNew.exe` on `\\.\pipe\FastSearchMCP_v2`), an in-process host plugin (`blender-mcp`, `freecad-mcp`, `kicad-mcp`), or a tiny `Cargo.toml` Zed `.wasm` stub (like `calibre-mcp`)?
   - Classify strictly as: **Pure-Rust (`Bucket A/B`)**, **Privilege-Split / Host-Plugin Hybrid (`Bucket C1`)**, **Defer (`Bucket C2`)**, or **Abort -- Stays Python (`Bucket D` CUDA/PyTorch)**.
2. **Live Service, Port & Database Contention Audit:**
   - Check `fleet-start.config.ps1`, `AGENTS.md`, and running processes/ports (e.g., `calibre-mcp` HTTP proxy on `:10720`, `plex-mcp` on `:10740/:10741`).
   - Identify any shared SQLite databases (`metadata.db`), lock files, or hardware COM ports currently open on `Goliath`, and specify how the Rust shadow repo will access them non-destructively (`SQLITE_OPEN_READ_ONLY` + `busy_timeout(5000 ms)`).
3. **Legacy Git Baseline Snapshot:**
   - Record the legacy repo's current branch and commit SHA (`git -C D:\Dev\repos\<name>-mcp rev-parse --short HEAD`) to prove the legacy repo remains untouched.
4. **Complete 1:1 MCP Tool & Portmanteau Operation Mapping Table:**
   - Extract every `@mcp.tool` from `llms-full.txt` or `src/<pkg>/` (or pre-digest via local Ollama **`gemma4:12b`** at `7.47 GB` / **`gemma4:e4b`** at `8.95 GB` on `:11434` -- never use `27B`+ models on our 24 GB RTX 4090).
   - If the legacy server uses FastMCP 3.2 **portmanteau tools** (e.g., `query_books(operation="search" | "by_author" | ...)` or `plex_library(operation="sections" | ...)`), list **every `operation` variant** in a mapping table:
     `Legacy Tool & Operation -> Rust Command Variant -> CLI Subcommand -> Rust MCP Tool Name + Legacy Portmanteau Alias`
   - Explicitly list any heavy Python-only feature intentionally excluded or delegated (e.g., local LanceDB/fastembed indexing), with rationale.
5. **Credential, `.env`, Config & Data-Path Inventory (`import.rs` Spec):**
   - List every environment variable, `.env` key, `config.json` / `config.yaml` field, and local file path present in `D:\Dev\repos\<name>-mcp` (verify which ones are actually populated on `Goliath`, redacting secret values in markdown).
6. **Write-Safety & Destructive-Action Fence Design:**
   - Identify every mutating operation (deleting books/media/files, SQL `INSERT/UPDATE/DELETE`, hardware actuator toggles) and specify its compile-time/runtime guard (`readonly: bool`, read-only SQLite connection pool for query commands, explicit confirmation flag).
7. **L3 `egui` Desktop Oracle Plan (near-identical UI and UX):**
   - **Capture the original first.** With the legacy webapp running, screenshot every page at the same window size and every primary gesture (a click that changes the page, a drag, a selection, a dialog). Store them in `docs/parity/legacy/<page>.png` and `docs/parity/legacy/<page>-<gesture>.png` before Phase 1. If the webapp is not running, start it only to capture. Do not write data through it.
   - **Read the layout, not the framework.** For each route, read `sidebar.tsx`, the page file, and the component that places that page's controls. Record groups, order, labels, and which control is a drag versus a click.
   - **Every page gets a `Page` variant and a screenshot pair.** A conversion that ships fewer pages than the legacy nav is not done. The pass bar is near-identical UI and UX: same pages, same groups, same order, same labels, and the same gesture doing the same thing. Pixel-nil against Tailwind is not required. Font rasterization and CSS-only effects get one written exception each. A missing control, a reordered group, or a gesture that does something else is a fail.
   - **Mandatory Fleet Standard LLM Settings Card:** The Settings page MUST feature the fleet standard LLM card:
     - Provider selection: Ollama (`http://127.0.0.1:11434/v1`), LM Studio (`http://127.0.0.1:1234/v1`), OpenAI (`https://api.openai.com/v1`), Anthropic (`https://api.anthropic.com`), Custom.
     - Editable Base URL and default models (`gemma4:12b`, `gpt-4o-mini`, `claude-sonnet-4-20250514`).
     - API Key entry stored securely in OS Credential Manager via `keyring` (never in plain text on disk).
     - Live model elicitation button (queries `/api/tags` or `/v1/models` and populates a dynamic dropdown picker).
     - Live connection test button with interactive status pill.
   - Name the `egui_kittest` golden PNG snapshots that Phase 4 will lock, one per legacy page and one per primary gesture, taken only after the pair matches.

---

## The 10-Point "Uncrashable Binary" Engineering Contract (Enforced Across Phases 1--4)

Every converted repo MUST implement all 10 belt-and-suspenders crash/hang guards:

1. **Compile-Time Panic Ban (`Cargo.toml`):** `unwrap_used = "deny"`, `expect_used = "deny"`, `panic = "deny"`, `todo = "deny"`, `unimplemented = "deny"` across the entire workspace.
2. **UTF-8 & Slice Bounds Immunity:** Never slice strings by byte index (`&s[..n]` panics on multi-byte UTF-8 such as German umlauts `ä/ö/ü`, `°`, or book/movie titles!). Always use `.chars().take(n)` or `.char_indices()`. Never index vectors/slices with `v[i]`; always use `.get(i)`.
3. **SQLite Lock & Corruption Immunity (`rusqlite`):**
   - When querying an external database shared with another program (e.g., Calibre's `metadata.db`), open with `OpenFlags::SQLITE_OPEN_READ_ONLY | OpenFlags::SQLITE_OPEN_NO_MUTEX` and set `conn.busy_timeout(Duration::from_millis(5000))` so neither Calibre nor `rust-calibre-mcp` can ever lock or corrupt each other.
   - For owned historian databases (`<domain>-store`), enable `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL; PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000;`.
4. **Hard Timeouts & Payload Caps on Every I/O Boundary:** Wrap every HTTP (`reqwest`), TCP, UDP, Named Pipe, Serial, and subprocess call in `with_timeout_secs(secs, ...)` and enforce a strict payload cap (e.g., `32 MiB` max response/pipe read) so a hung server or malformed length prefix can never hang a worker or OOM the process.
5. **`egui` UI Thread Anti-Deadlock & Anti-Freeze Law (`app.rs`):**
   - **Zero synchronous I/O on `update()`:** Never call HTTP, SQLite, disk scan, subprocess, or `keyring` OS Credential Manager on the UI thread; dispatch everything via `self.spawn(...)` over the `mpsc` job channel.
   - **Zero `egui::Context` RwLock re-entrancy:** Never call `ctx.set_visuals()`, `ctx.set_style()`, or `ctx.set_zoom_factor()` inside `ctx.input(|i| ...)`. Read the input state into a local variable, exit `ctx.input`, and mutate `ctx` outside.
   - **Reads deadlock too, and silently:** `ctx.zoom_factor()` (or any `ctx` read) *inside* a `ctx.input(|i| ...)` closure deadlocks the same way — parking_lot RwLock, write-held-then-read-requested. Symptom is uniquely nasty: no window ever appears, process idles at ~0% CPU, **no panic, no log, exit code clean** — indistinguishable from a hung GPU init. epaint only fires its `Failed to acquire RwLock read after 10s` panic in debug builds, and only `RUST_BACKTRACE=1` reveals the `Context::input → Context::read` frames (proven live in `rust-devices-mcp`, 2026-10-17: mouse-zoom diagnostics line). Rule of thumb: if a fresh egui build shows no window within 15s and burns no CPU, suspect re-entrancy first and rerun debug with `RUST_BACKTRACE=1` before touching drivers.
   - **Zero per-frame task storms:** Gate initial/auto-load tasks behind a 3-state latch (`LoadState::Unloaded -> Loading -> Loaded`).
6. **Panic Hook & Forensic Crash Log (`main.rs`):** Install a custom `std::panic::set_hook` in both `<domain>-mcp` and `<domain>-app` that appends any unexpected third-party C/GPU panic (timestamp, thread, payload, location) to `%LOCALAPPDATA%\rust-<domain>-mcp\crash.log` and `stderr`.
7. **MCP Stdio Wire Purity & Poison-Frame Immunity (`run_mcp_stdio`):**
   - Zero bytes written to `stdout` except valid single-line JSON-RPC `2.0` frames.
   - Empty lines ignored; malformed JSON returns `-32700 Parse error` without exiting; unknown tools return `isError: true` content without panicking; `stdin` EOF exits cleanly (`Ok(())`).
8. **Dual Tool-Dispatcher Aliasing (Zero-Breakage Cutover):**
   - In `call_tool(name, args)`, support **both** the clean ArtCraft tool names (`<domain>.<action>` and `<domain>_<action>`) **AND** the legacy Python portmanteau tool names (`<legacy_tool>` with `args["operation"]`) mapped in `docs/CONVERSION_DOSSIER.md`. Existing skills, prompts, and IDE configs continue working with zero edits!
9. **Graceful Offline / Unconfigured Degradation (`Vendor::Demo` / Diagnostic Banner):**
   - If the target service/database/pipe is offline or credentials are missing, neither CLI, MCP, nor the `egui` app may crash on startup. They must surface a structured `DeviceError::Offline` / `Auth` diagnostic showing the exact path/URL checked and offer a 1-click `Demo` fallback in the UI.
10. **Headless Smoke & Visual Parity Lock:** Every repo ships `--smoke` in `<domain>-app` (boots full state, runs one headless frame, verifies zero panics, exits `0`), `egui_kittest` golden PNG snapshots in Dark + Light themes, and `glyph_source_scan` tofu protection. The Light golden MUST be eyeballed for contrast before lock: readable body text, visible card borders, visible shadows. A Light golden with white-on-white text or borderless cards fails the gate even if every other check is green (Phase 4 item 2).

---

## Phase 1: Mechanical Workspace Stamp (Zero-Invention Scaffold)

Create `D:\Dev\repos\rust-<name>-mcp` (Shadow Mode, default):

1. **Workspace `Cargo.toml` & `.gitignore`:**
   - Copy `[workspace.lints.clippy]` (`unwrap_used`, `expect_used`, `panic`, `unimplemented`, `todo` all `"deny"`) and `[workspace.dependencies]` from `D:\Dev\repos\rust-devices-mcp\Cargo.toml`.
   - Trim unused hardware crates (`tapo`, `kasa-rs`, `shelly-core`, `oxvif`, `nokhwa`, `retina`, `openh264` unless needed). Keep the blessed core stack: `serde`, `serde_json`, `clap`, `tokio`, `reqwest`, `chrono`, `uuid`, `rusqlite` (`bundled`), `keyring`, `eframe` (`0.37`), and `egui_kittest` (`0.37` in dev-dependencies).
2. **Copy the 70% Reusable Fleet Kernel from `rust-devices-mcp`:**
   - `crates/<domain>-core/src/error.rs` & `creds.rs` (`with_timeout_secs`, `classify_vendor_error`).
   - `crates/<domain>-core/src/bridge.rs` (**verbatim** -- `bridge.event`, `bridge.speak`, `bridge.webhook`).
   - `crates/<domain>-core/src/llm.rs` (**verbatim**, with `Provider::Ollama::default_model` set to `"gemma4:12b"` so RTX 4090 24 GB chat needs zero VRAM scrubbing). Includes `chat_stream` (OpenAI-compat + Anthropic SSE, `Send` callback) — wire chat pages to real tokens via generation-guarded chunk jobs, never buffered-then-faked streaming.
   - `crates/<domain>-core/src/rag.rs` (**verbatim** -- LanceDB + local MiniLM semantic index: `Embedder` trait, `StubEmbedder` for tests/demo, `FastEmbedder`, shared model cache, `RagIndex` rebuild/count/search, honest keyword fallback when unsynced). Requires `protoc` at build time (`winget install --id Google.Protobuf`); pin `lancedb` with the `remote` feature (0.40 default features do not compile upstream) and arrow to lancedb's version (58).
   - `crates/<domain>-store/src/lib.rs` (if the repo records historical readings/events/logs in SQLite).
   - `crates/<domain>-app/src/vault.rs` & `registry.rs` (**verbatim** with `SERVICE = "rust-<domain>-mcp"`).
   - `crates/<domain>-app/src/browser.rs` (**verbatim** -- shared list-browser kernel: Card/List-agnostic search/sort/first-letter-jump/pagination pipeline, theme-aware text, char-safe truncation; proven in `rust-plex-mcp`).
   - `crates/<domain>-app/src/richchat.rs` (**verbatim**, with `browser.rs` -- enriched chat kernel: personas, repo skill preprompt, example chips, streaming reveal, export-to-clipboard, theme-aware bubbles; wire the chat page onto `RichChat` instead of hand-rolling chat state).
   - `justfile`, `installer/installer.nsi`, `AGENTS.md`, and `HANDOVER.md`.
3. **Checkpoint 1:** Run `cargo check --workspace`, log in `docs/CONVERSION_LOG.md`, update `HANDOVER.md`, and commit (`feat(phase-1): mechanical workspace stamp`).

---

## Phase 2: L1 Domain Protocol Transpilation (`crates/<domain>-core`)

1. **Write Domain Modules (`crates/<domain>-core/src/<module>.rs`):**
   - Translate the wire essence documented in `docs/CONVERSION_DOSSIER.md` into zero-`unwrap` async Rust functions over `reqwest` / `rusqlite` / `tokio::net` / `tokio::process`.
   - Enforce all items of the **10-Point Uncrashable Binary Contract** (`.get()`, char-boundary slicing, `SQLITE_OPEN_READ_ONLY` + `busy_timeout` for shared DBs, `with_timeout_secs`, payload size caps, and `Demo` mode).
2. **Write `import.rs` (Zero-Config Legacy Fleet Import):**
   - Auto-discover `D:\Dev\repos\<name>-mcp` (`../<name>-mcp`), parse its `.env` (expanding `${VAR:-default}`), `config.json`, and `config.yaml`, and resolve settings in strict order: `explicit args > process env > OS vault > imported .env / config`.
   - Write unit tests verifying `.env` / config parsing and fallback resolution.
3. **Wire `Command` Enum & `dispatch(cmd: Command) -> Value` in `lib.rs`:**
   - Include all domain commands + `status` + `bridge.{event,speak,webhook}` + `llm.{chat,models}` (+ `*.history` if `<domain>-store` is present).
   - Include the mandatory compile-time guard test:
     ```rust
     #[test]
     fn dispatch_future_is_send() {
         fn assert_send<T: Send>(_: T) {}
         assert_send(dispatch(Command::Status));
     }
     ```
4. **Checkpoint 2:** Run `cargo clippy -p <domain>-core --all-targets -- -D warnings` and `cargo test -p <domain>-core`, log exact test counts in `docs/CONVERSION_LOG.md`, update `HANDOVER.md`, and commit (`feat(phase-2): L1 domain core and zero-config import`).

---

## Phase 3: L2 CLI + Dual-Aliased MCP Stdio Server (`crates/<domain>-mcp`)

1. **Install Forensic Panic Hook** at top of `main()` writing to `%LOCALAPPDATA%\rust-<domain>-mcp\crash.log` and `stderr`.
2. **Wire `clap` CLI Subcommands (`--json` on every command)** in `crates/<domain>-mcp/src/main.rs`.
3. **Wire `tools_list()` and Dual-Aliased `call_tool(name, args)` in `run_mcp_stdio()`:**
   - Accept `<domain>.<action>`, `<domain>_<action>`, **and** legacy portmanteau `<legacy_tool>(operation="...")` calls mapped in `docs/CONVERSION_DOSSIER.md`.
4. **Add Unit Tests in `crates/<domain>-mcp/src/main.rs`:**
   - `catalog_lists_<n>_tools`
   - `unknown_tool_becomes_error_content_not_panic`
   - `legacy_portmanteau_alias_routes_correctly`
   - `demo_round_trip`
   - Required write-safety parameters reject missing values instead of silently defaulting.
5. **Checkpoint 3:** Run `cargo test -p rust-<name>-mcp` and pipe a live JSON-RPC `initialize` + `tools/list` + `tools/call` test over `stdin`, record output in `docs/CONVERSION_LOG.md`, update `HANDOVER.md`, and commit (`feat(phase-3): L2 CLI and dual-aliased MCP stdio server`).

---

## Phase 4: L3 Pure-Rust `egui` Desktop Dashboard (`crates/<domain>-app`)

1. **Start from the `rust-devices-mcp` `app.rs` Shell:**
   - Includes `harsh_visuals()` (dark) + `crisp_light_visuals()` (light) + `apply_theme()`, vector Sun/Moon toggle, `Ctrl+Wheel` zoom + reset pill, `Crossconnect`, `Chat` (`gemma4:12b` default), `Settings` (`vault.rs` off UI thread + `registry.rs`), `Help`, and `Raw JSON`.
   - The shell MUST already contain the Visual Enrichment Gate (item 2 below). If it does not, backport it from the newest converted repo before writing any page. Never strip it to "simplify".
2. **Visual Enrichment & Dual-Theme Legibility Gate (mandatory, not polish):**
   Every page must pass all six checks in BOTH themes before its golden is locked. `rust-plex-mcp` (`8f11ee7`, 2026-10-18) proved that dark-only development ships an unreadable light mode, invisible card borders, and dead inspector pages — this gate exists so nobody re-pays for that:
   - **No hardcoded text colors.** All heading/title/body text goes through theme-aware helpers (`ink()` / `sub()` / `faint()` pattern: near-white/slate-400/slate-500 in dark, slate-900/700/600 in light). Zero `.color(Color32::WHITE)` or slate-grey text on theme-driven backgrounds. Accent text uses amber in dark, amber-700 (`rgb(180,83,9)`) in light — raw amber fails contrast on white.
   - **Full light `Visuals`, not a 4-field stub.** `crisp_light_visuals()` must style every widget state (`noninteractive`, `inactive`, `hovered`, `active` fills + strokes), `selection`, and `override_text_color`. A light theme that only sets `panel_fill` renders white buttons with white text.
   - **Visible cards in both themes.** Every card/poster/row `Frame` gets a ≥1.5px border (slate-500 dark / slate-400 light — 1px slate-700-on-slate-900 is invisible) AND a real `egui::Shadow` drop shadow. No shadowless, borderless white-on-white cards.
   - **Theme-aware placeholder art.** Poster/media placeholders must have light-mode fills (slate-200, not dark-navy-only) with matching text colors. Chat bubbles, badges, and popups follow the same rule: any hardcoded dark fill keeps light text ONLY if the fill stays dark in both themes.
   - **Char-boundary-safe truncation everywhere.** Titles/summaries use a `trunc()` helper over `char_indices`, never `&s[..n]` byte slices (panics on multibyte titles — proven by Japanese library names). Contract point 2 covers the rule; this gate covers its UI instances.
   - **Inspector pages read the real dispatch envelope.** Before writing any detail view, print one live `dispatch()` JSON payload and verify every field path against it (`{"item": {...}}` nesting, `duration` ms vs `duration_ms`, `Media[0].videoResolution` vs flat keys, lowercase serde names vs PascalCase Plex names). An inspector built from legacy Python dict keys shows permanent fallback text.
3. **Build every legacy page, then diff it:**
   - One `Page` variant per legacy route, in the legacy order, with the legacy labels. The devices shell supplies chrome (theme, zoom, vault, chat). It does not replace the legacy pages.
   - Route every action through `self.spawn(move || async move { dispatch(Command::...).await })` over the `mpsc` job channel.
   - Show clear offline/unconfigured diagnostic banners with a 1-click `Load Demo Data` button so the UI is usable when external servers are down. The banner sits where the legacy app shows its empty state. It does not become the page.
3. **Oracle diff, then lock:**
   - Screenshot the Rust window for every page and every primary gesture into `docs/parity/rust/`.
   - Diff each pair against `docs/parity/legacy/`. Fix `app.rs` until the UI and the gesture match. Record remaining exceptions in `docs/UI_PARITY.md`.
   - Only then keep `glyph_source_scan()` (`include_str!("app.rs")` allowing only `°`, `×`, `·`, `…`, `--`) and write `egui_kittest` goldens of those matching frames. A golden of an unmatched first draft is a fail.
4. **Checkpoint 4:** Run `cargo test -p <name>-app` and `cargo run -p <name>-app -- --smoke`, record snapshot verification in `docs/CONVERSION_LOG.md`, update `HANDOVER.md`, and commit (`feat(phase-4): L3 egui desktop app and golden snapshots`).

---

## Phase 5: 6-Gate Certification, Live Oracle Probe, Release `.exe` Packaging & GitHub Release

Run all verification and release-packaging gates sequentially in `D:\Dev\repos\rust-<name>-mcp` (never run parallel `cargo` invocations in the same workspace):

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo fmt --all --check
'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | cargo run -q -p rust-<name>-mcp -- mcp-stdio
cargo run -p <name>-app -- --smoke
cargo build --workspace --release
```

1. **Live Oracle Probe (Read-Only):** Run at least one read-only CLI command and one MCP `tools/call` against the real local database/service/API using auto-imported credentials from `../<name>-mcp`. Record the exact command, latency, and output summary in `README.md` and `docs/CONVERSION_LOG.md`.
2. **Verify Legacy Repo Untouched:** Run `git -C D:\Dev\repos\<name>-mcp status -s` to confirm the legacy repository is still 100% clean and unharmed.
3. **Final Documentation Bundle:** Write `INSTALL.md`, `CHANGELOG.md`, `docs/UI_PARITY.md`, per-crate `README.md`s, and `docs/ASSESSMENT_<DATE>.md`; finalize `docs/CONVERSION_LOG.md` and `HANDOVER.md` (mirrored to `mcp-central-docs/projects/rust-<name>-mcp/HANDOVER.md`); commit all changes (max 5 files per commit).
4. **Mandatory Release `.exe` Bundle, NSIS Installer & GitHub Release (`v0.4.0`):**
   A `repconv` run is **NOT complete** until the optimized `--release` binaries, NSIS installer, `SHA256SUMS.txt`, public GitHub repository, and GitHub Release assets are built and published:
   ```powershell
   New-Item -ItemType Directory -Force -Path "target\release\bundle" | Out-Null
   & "C:\Program Files (x86)\NSIS\makensis.exe" "installer\installer.nsi"
   Copy-Item "target\release\<name>-app.exe" "target\release\bundle\<name>-app.exe" -Force
   Copy-Item "target\release\rust-<name>-mcp.exe" "target\release\bundle\rust-<name>-mcp.exe" -Force
   $files = @("<Title>-Rust-0.4.0-setup.exe", "<name>-app.exe", "rust-<name>-mcp.exe")
   $lines = foreach ($f in $files) {
       $h = (Get-FileHash -Algorithm SHA256 "target\release\bundle\$f").Hash.ToLower()
       "$h  $f"
   }
   $lines | Set-Content -Path "target\release\bundle\SHA256SUMS.txt" -Encoding ascii

   # Create GitHub repo (if not yet created), push main + v0.4.0 tag, and upload release binaries
   gh repo create sandraschi/rust-<name>-mcp --public --source=. --remote=origin --push
   git tag v0.4.0
   git push origin v0.4.0
   gh release create v0.4.0 `
     "target\release\bundle\<Title>-Rust-0.4.0-setup.exe" `
     "target\release\bundle\<name>-app.exe" `
     "target\release\bundle\rust-<name>-mcp.exe" `
     "target\release\bundle\SHA256SUMS.txt" `
     --title "v0.4.0 — Pure-Rust ArtCraft <Title> MCP + egui 0.37 Desktop App" `
     --notes-file CHANGELOG.md
   ```

---

## 6. Multi-IDE & Weak/Local LLM Execution Strategy (Stretching \$20/mo Pro Quotas)

Why do weaker / mid-tier / contributor LLMs (such as OpenCode's `meta/muse-spark-1.3-contributor`, `deepseek-v4-flash:cloud`, `glm-4.6:cloud`, Cursor Fast mode, or local `gemma4:12b`) struggle if you hand them an entire repo conversion in a single prompt, whereas frontier models (Antigravity Gemini 4 Argon / Claude Opus/Sonnet) sail through?

1. **Copy-Paste Output Exhaustion:** Asking an LLM to read and re-emit 2,500 lines of reusable kernel files (`bridge.rs`, `llm.rs`, `error.rs`, `creds.rs`, `vault.rs`, `registry.rs`) wastes **40,000+ output tokens** (burning 30% of a \$20/mo Pro 5-hour window on pure file copying) and causes weaker models to truncate files with `// ... rest of code ...`.
2. **Horizon Collapse Past Step 12:** As documented in [`research/2026-10-14-local-llm-dev-failure.md`](../research/2026-10-14-local-llm-dev-failure.md), mid-tier and local models succeed on **single-phase, compiler-bounded tasks (`<= 10` tool calls)**, but lose the thread when asked to execute a 40-step multi-crate build in one turn.

### 6.1 The Zero-Token PowerShell Stamp (`scripts/New-RustArtcraftRepo.ps1`)
**Never spend LLM tokens copying kernel files.** Always start Phase 0/1 by running the deterministic PowerShell stamp script:

```powershell
pwsh -NoProfile -File D:\Dev\repos\mcp-central-docs\scripts\New-RustArtcraftRepo.ps1 -Domain <domain>
```

In **3 seconds and 0 LLM tokens**, this script:
- Performs the read-only git SHA, `.env` key, hidden-binary, and `@mcp.tool` regex scan of `D:\Dev\repos\<domain>-mcp`.
- Copies `bridge.rs`, `llm.rs` (auto-patched to `"gemma4:12b"`), `error.rs`, `creds.rs`, `vault.rs`, and `registry.rs` from `rust-devices-mcp`.
- Generates pre-populated `docs/CONVERSION_DOSSIER.md`, `docs/CONVERSION_LOG.md`, and `HANDOVER.md`.

### 6.2 The Quota-Miser Baton Relay (10--12 Repos per \$20/mo Pro Window)
Because `docs/CONVERSION_DOSSIER.md`, `docs/CONVERSION_LOG.md`, and `HANDOVER.md` persist state between phases, you can route each phase to the **cheapest model tier that can pass that phase's `rustc` gate**, saving frontline Pro quota (Antigravity Gemini 4 Argon / Claude Pro) strictly for the hardest 20%:

| Phase | Recommended Executor / Model Tier | Frontline Pro Quota Cost | Why Weak / Cheap Tiers Succeed Here |
|---|---|---:|---|
| **Stamp (`Phase 0/1` Init)** | `New-RustArtcraftRepo.ps1` (PowerShell) | **0 tokens** | 100% deterministic PowerShell file copy + regex extraction. |
| **Phase 0 Finalize (`CONVERSION_DOSSIER.md`)** | OpenCode Cheap/Contributor (`muse-spark-1.3` / `deepseek-v4-flash`) or Local `gemma4:12b` | **0 Pro tokens** | Structured markdown table completion from 2--3 Python files. |
| **Phase 2 (`<domain>-core` Protocol + `import.rs`)** | **Frontline Pro Quota (Antigravity Gemini 4 Argon / Claude Code)** | **~10k--15k tokens** | The only phase requiring deep protocol/lifetime synthesis under `deny(unwrap_used)`. Scoped to 2 files (`<domain>.rs` + `import.rs`). |
| **Phase 3 (`<domain>-mcp` CLI + Dual-Aliased MCP)** | OpenCode (`glm-4.6` / `kimi-k2.6`) or Cursor Fast | **0 Frontline tokens** | Mechanical 1:1 mapping from `Command` enum (already defined in Phase 2) to `clap` flags and JSON-RPC match arms. Exhaustive `match` in `rustc` catches every omission! |
| **Phase 4 (`<domain>-app` `egui` Domain Tabs)** | OpenCode / Cursor or Quick Frontline Pass | **~5k tokens** | `app.rs` chrome, theme, zoom, chat, and vault already work; the model only writes 2--3 `view_<tab>(&mut self, ui: &mut Ui)` functions. |
| **Phase 5 (6-Gate Run + `ASSESSMENT.md`)** | Terminal (`just check` / `just test`) + Cheap/Local Summarizer | **0 Frontline tokens** | Mechanical execution of the 6 verification commands and markdown table recording. |


