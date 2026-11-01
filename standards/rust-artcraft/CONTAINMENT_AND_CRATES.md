---
title: "ArtCraft Five-Layer Containment Harness, Traps & Blessed Crates"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-17
---

# ArtCraft Five-Layer Containment Harness, Traps & Blessed Crates

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)  
**Pilot Reference Implementation:** [`rust-devices-mcp`](../../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp`)

---

## 1. The ArtCraft Five-Layer Containment Harness

Borrowed with credit from Brandon Thomas's **ArtCraft** suite (`storytold`), the core philosophy is:
> **Never let an LLM invent its own architecture, and never treat an agent as an unguarded author -- treat it as a bounded compiler operating inside a deterministic test harness.**

Every pure-Rust MCP repository in this fleet enforces five non-negotiable containment layers:

### Layer 1: Load-Bearing Lint Walls (Zero-Panic Policy)
Every workspace root `Cargo.toml` AND every crate root (`lib.rs` / `main.rs`) MUST declare:

```toml
[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
unimplemented = "deny"
todo = "deny"
```

- Every fallible operation returns `Result<T, DomainError>` and propagates with `?` or explicit `match` / `unwrap_or` / `ok_or_else`.
- **Hostile Input Fence:** All external inputs (CLI flags, MCP JSON arguments, raw socket/HTTP bytes, JPEG headers) are treated as hostile:
  - Never index slices directly (`buf[i]` can panic); use `buf.get(i)` returning a typed error on `None`.
  - Use `checked_add` / `checked_mul` / `saturating_*` for byte offsets, lengths, and power/rate math.
  - Never slice strings by byte index; slice only on char boundaries or via `.chars()`.
  - Validate device identifiers / IPs / URLs as non-empty and bounded (`<= 253` chars) before touching any socket.
  - Lock poisoning must never cascade (`lock().unwrap_or_else(PoisonError::into_inner)`).

### Layer 2: Strict Three-Tier Workspace Seam (`L1` / `L2` / `L3`)
Every repo is a Cargo virtual workspace (`resolver = "2"`) with three crates under `crates/`:

```text
rust-<domain>-mcp/
├── Cargo.toml                  # Virtual workspace + clippy deny gates + shared deps
├── Cargo.lock                  # ALWAYS committed (binary workspace reproducibility)
├── justfile                    # check / test / fmt-check / run-mcp / run-cli / build-release
├── AGENTS.md                   # ArtCraft containment rules + fleet context block
├── docs/                       # PRD.md + UI_PARITY.md + parity screenshots
├── installer/                  # Hand-written current-user installer.nsi
└── crates/
    ├── <domain>-core/          # L1: Protocols, credential resolution, fleet import, error taxonomy, Command::dispatch
    ├── <domain>-mcp/           # L2: CLI-first binary (clap + --json) + `mcp` stdio subcommand
    └── <domain>-app/           # L3: Pure-Rust eframe/egui desktop dashboard calling L1 directly in-process
```

1. **L1 (`<domain>-core`)**:
   - Owns all hardware/API protocols, state machines, credential resolution, legacy fleet import (`import.rs`), typed errors, and the universal command bus (`pub enum Command` + `pub async fn dispatch(cmd: Command) -> serde_json::Value`).
   - **Forbidden dependencies in L1:** Zero UI crates (`egui`, `eframe`, `tauri`), zero CLI crates (`clap`), zero MCP transport framing. Protocol and async runtime crates (`serde`, `serde_json`, `tokio`, `reqwest`, etc.) live here.
   - `dispatch(cmd)` **never panics**: `Result<T, DomainError>` is encoded at the boundary into either the serialized `Value` or `{"error": e.to_string()}` so L2 and L3 never branch on transport error types.
2. **L2 (`<domain>-mcp`)**:
   - **CLI-First + MCP Stdio in One Binary:** Humans and scripts run `rust-<domain>-mcp <subcommand> [--json]`; MCP clients run `rust-<domain>-mcp mcp`.
   - Both CLI subcommands and MCP `tools/call` construct a `Command` variant and pass it to `devices_core::dispatch(cmd)`. **The CLI and MCP surfaces can never disagree because they execute the exact same code path.**
   - **The Stdio Invariant:** In `mcp` mode, **`stdout` is 100% pure line-delimited JSON-RPC (`MCP 2024-11-05`)**. Every diagnostic or startup log MUST go to `stderr` via `eprintln!`. A single rogue `println!` in L1 or L2 breaks the MCP client handshake.
   - **No Binary Blobs Over MCP:** Tools like `camera.snapshot` validate raw bytes (e.g., JPEG `0xFF 0xD8` SOI magic + SOF0/1/2 dimensions), optionally write the file to disk (`out_path`), and return structured metadata JSON (`bytes`, `width`, `height`, `path`). Never dump megabytes of base64 into the LLM context window.
3. **L3 (`<domain>-app`)**:
   - Pure-Rust `eframe` / `egui` native GPU desktop application calling `devices_core::dispatch(Command::...)` **directly in-process** over a background `tokio` runtime + `mpsc` job channel (note: Tauri v2 was prototyped in `v0.1` and dropped in `v0.2.0` so that the entire desktop UI is 100% pure Rust with zero WebView2/HTML/JS/CSS).
   - **Forbidden in L3:** Never spawn `rust-<domain>-mcp.exe` as a child process, never open a localhost HTTP sidecar port for the desktop UI, and never route GUI actions through JSON-RPC.
   - Ships a unit test proving `run(Command::...) == dispatch(Command::...)` (executable GUI/MCP parity), `--smoke` headless CI launch mode, and `egui_kittest` golden widget PNG snapshots.

### Layer 3: The Universal Command Bus, Legacy Fleet Import & Actuator Safety Fence
- Every capability is a variant on `Command` with a canonical constant string ID (`CMD_STATUS`, `CMD_PLUG_STATS`, `CMD_WEATHER_NOW`, etc.).
- **Zero-Config Legacy Fleet Import (`import.rs`) & Credential Precedence (`creds.rs`):**
  - When a `rust-<domain>-mcp` repo shadows a legacy Python `<domain>-mcp` repo, L1 provides an `import.rs` module that automatically discovers the sibling Python checkout (`DEVICES_MCP_DIR`, `../<domain>-mcp`, or `D:\Dev\repos\<domain>-mcp`) and parses its `config.yaml`, `.env`, and token caches (`hue_bridge.cache`, `ring_token.cache`) at startup.
  - **Strict 4-Level Precedence:** `1. Explicit CLI/MCP args` > `2. Process environment` > `3. Imported .env` > `4. Imported config.yaml`.
  - **Never Persist Imported Secrets:** L3 (`ui.json` in `%LOCALAPPDATA%`) only persists non-secret form fields (last selected IP, latitude/longitude, city, theme, zoom). Passwords and tokens are re-hydrated from `import.rs` / env vars at every launch so secret material is never duplicated to disk.
- **Deterministic `Demo` + Keyless First-Paint Oracles:** Every hardware/API controller supports an explicit `Vendor::Demo` / `CamSource::Demo` mode returning deterministic, realistic values (e.g., `42.5 W`, `0.85 kWh`, or a minimal valid 16-byte 4x2 JPEG frame), plus keyless live endpoints where available (such as `weather.now` via Open-Meteo for Vienna so the desktop dashboard has real live telemetry on first paint even before LAN credentials are configured).
- **Physical, Acoustic & Critical-Infrastructure Actuator Safety:**
  - High-risk physical or acoustic actuators that lack interactive confirmation over MCP (such as the Ring alarm siren) are **deliberately excluded** from the command bus.
  - **`readonly` Plug Guard:** Critical infrastructure plugs marked `readonly: true` in `config.yaml` (such as `192.168.0.38` Server on the Vienna LAN) are enforced in both L3 (Toggle Off button disabled with `(readonly)` badge) and L1/L2 (refusing to power-cycle the host running the agent).
  - State-mutating commands with no safe default (such as `hue.set_light` `on: bool`) require explicit parameters rather than silently defaulting to `false`.

### Layer 4: Automated Gap Scorecard, Live-Hardware Verification & Bug Bounties
Instead of shipping fake `"planned": true` stubs, pure-Rust repos progress through four explicit scorecard tiers and verify against live hardware:
- **Tier 1 (`v0.1`):** Workspace structure, clippy deny gates, `Command` enum, `Demo` deterministic oracles, CLI `--json` + MCP `stdio` server, L3 in-process parity test, release binaries `< 2 MB`.
- **Tier 2 (`v0.2`):** Live LAN/Cloud read + actuator drivers (Tapo/Kasa/Shelly plugs, Hue CLIP v1, Netatmo OAuth2, Ring OAuth2/2FA/doorbells/alarms, Open-Meteo `weather.now`) + zero-config `import.rs` from the legacy Python repo.
- **Tier 3 (`v0.3`):** Media/stream frame capture (Tapo camera, ONVIF, USB MediaFoundation, Ring snapshot polling, HTTP URL) with pure-Rust header validation.
- **Tier 4 (`v1.0`):** Full pure-Rust `eframe`/`egui` multi-view dashboard (`devices-app`), `egui_kittest` golden PNG regression suite, hand-written current-user NSIS installer (`installer/installer.nsi`, no admin UAC required), and cold-boot / binary-size benchmark table in `README.md`.
- **Proof That Live-Hardware Verification Catches Real Protocol Bugs (`v0.2.0` Vienna LAN Bounties):**
  Running `rust-devices-mcp` against Sandra's live Vienna home hardware immediately caught and fixed **three real-world protocol bugs** (each now locked with a unit regression test):
  1. **Tapo P115 Milliwatt Scaling (`plug_tapo.rs`):** The `tapo` crate's `get_energy_usage().current_power` returns **milliwatts**, not watts -- causing the `.38` Server plug to report `290,000 W` (`290 kW`) instead of `290 W`. Fixed (`milliwatts as f64 / 1000.0`).
  2. **JPEG `APP0` Segment Offset Off-by-2 (`camera.rs`):** In `jpeg_dimensions()`, advancing past variable-length JPEG segments (`APP0` / `COM` headers emitted by real cameras and `placehold.co`) jumped by `i + 2 + seg_len` instead of `i + seg_len` (because in JPEG, `seg_len` includes its own 2-byte length field), landing mid-payload and failing SOF dimension extraction on real camera frames.
  3. **Ring OAuth Refresh `406 Not Acceptable` (`ring.rs`):** Ring's `https://oauth.ring.com/oauth/token` rejected refresh requests that included `client_id`/`scope` in the body or lacked an explicit `User-Agent: android:com.ringapp` header.

### Layer 5: Rigid Definition of Done (Merge Gate)
No commit or tier closes unless all 6 gates pass:
1. `cargo clippy --workspace --all-targets --all-features -- -D warnings` (zero warnings, zero unwraps/panics).
2. `cargo test --workspace` (all unit + dispatch + round-trip serialization + `egui_kittest` snapshot + `glyph_allowlist` tests green; every bug fix ships with a regression test).
3. `cargo fmt --all --check` clean.
4. Byte-exact MCP stdio probe verified (`initialize` -> `tools/list` -> `tools/call`).
5. `Cargo.lock` committed; no `*.bak`, `*.cache`, `*.exe`, or `target/` artifacts in `git status`.
6. `CHANGELOG.md` checkpoint line updated.

---

## 2. Five Mandatory Guardrails & Traps for Fleet Rollout

The pilot (`rust-devices-mcp` v0.1 -> v0.2) surfaced five concrete traps that every agent MUST follow when building or porting a Rust MCP repo:

### Trap 1 & The "PySomething-to-Rust-in-a-Jiffy" Doctrine
In Python, almost every smart device or web service has a mature PyPI library (`python-ring-doorbell`, `pyatmo`, `phue`, `python-miio`, `alexapy`). On `crates.io`, many hardware/API wrapper crates are either nonexistent or abandoned `0.0.1` hobby projects from 2019.
- **Why "No Rust Crate Exists" Is NEVER a Blocker:**
  - Almost every `pysomething` library on PyPI is just 80% Python boilerplate, class hierarchies, and async/sync wrappers around **200 lines of actual wire protocol** (HTTP endpoints, OAuth headers, AES/XOR framing, or serial byte sequences).
  - An agent in OpenCode/Claude/Antigravity can read the upstream Python package (`site-packages` or GitHub) as an executable wire specification and **transpile the actual protocol into a rock-solid, zero-unwrap 150-300 line Rust module (or a brand-new standalone `*-rs` crate) in 10 minutes**.
- **HARD RULE (The Direct-Protocol & Jiffy-Port Rule):**
  1. Never let "there is no crate on crates.io" block a Rustification.
  2. Never pull an unmaintained `0.0.x` wrapper crate when the protocol is HTTP/REST, OAuth2, WebSocket, JSON-RPC, SCPI, or binary framing over TCP/UDP/Serial.
  3. Read the Python `pysomething` source to extract the exact URLs, headers, packet layouts, and state transitions, then write the Rust module directly in `<domain>-core` (or publish it as our own `<protocol>-rs` crate) on top of the blessed stack (`reqwest`, `serde`, `serde_json`, `tokio`, `aes`, `sha2`, `uuid`).

### Trap 2: LLM Training-Cutoff Hallucinations on Rapidly Churning Crates
During the `rust-devices-mcp` v0.2 expansion, `nokhwa 0.10.11` (USB webcam capture) failed compilation on first pass because the agent wrote `nokhwa 0.9` / early `0.10` signatures (`RequestedFormat::with_decoder`, `usize` index instead of `CameraIndex::Index`, `frame.source_buffer()` instead of `frame.buffer()`).
- **HARD RULE:** When integrating a hardware/media crate outside the core `tokio`/`reqwest`/`serde` stack (`nokhwa`, `cpal`, `btleplug`, `serialport`, `hidapi`), **inspect the actual installed crate signature in Cargo's registry cache or run `cargo doc --open` / `cargo check` immediately after adding the dependency** before writing 500 lines against hallucinated method names.

### Trap 3: The `rmcp` SDK vs. Hand-Rolled Stdio Framing
The official Rust MCP SDK (`rmcp`) is evolving rapidly and pulls a heavy proc-macro and async transport tree.
- **HARD RULE:** Until `rmcp` stabilizes and is audited fleet-wide against the stderr-only invariant, pure-Rust fleet repos use the **proven ~75-line hand-rolled MCP `2024-11-05` stdio loop** (`run_mcp_stdio()` in `crates/<domain>-mcp/src/main.rs`).
- Keep `tools_list()` and `call_tool(name, args)` as **pure functions** returning `serde_json::Value` so they can be unit-tested in milliseconds without spawning processes or opening pipes, and can be mechanically swapped to `rmcp` `#[tool_router]` macros later if desired.

### Trap 4: Tool Naming Compatibility (`.` vs `_`)
ArtCraft's internal command bus uses dotted identifiers (`plug.get_stats`, `camera.snapshot`). However, several strict MCP hosts and OpenAI-compatible tool routers validate tool names against `^[a-zA-Z0-9_-]{1,64}$` and reject `.` in tool names.
- **RECOMMENDED PATTERN:** Either expose underscore names (`plug_get_stats`, `camera_snapshot`) in `tools/list`, OR accept **both** `plug_get_stats` and `plug.get_stats` in `call_tool()` match arms (`"plug_get_stats" | "plug.get_stats" => ...`) so CLI scripts, ArtCraft scorecards, and strict MCP clients all work seamlessly.

### Trap 5: Cargo `target/` Disk Space Multiplication
A single Rust workspace with `tokio` + `reqwest` + `eframe` generates a **2 GB to 6 GB `target/` directory**. Across 100+ Rustified repos, isolated `target/` folders will consume **300-600 GB** of SSD space and recompile `tokio`/`reqwest` 100 times.
- **OPERATIONAL RULE:**
  - Set a shared user-level cache (`CARGO_TARGET_DIR=D:\Dev\cargo-target` or `sccache`) when working across multiple Rust repos, OR run `cargo clean` after cutting release binaries into the repo's distribution staging directory.
  - **Concurrent Agent Lock Contention:** When two agents (e.g., OpenCode and Antigravity) run `cargo check` simultaneously in the same workspace, Cargo prints `Blocking waiting for file lock on build directory`. Never kill a peer agent's build lock; wait for completion or inspect source files statically while another agent is compiling.

---

## 3. Blessed Rust Crate Stack (SOTA 2026)

To prevent dependency sprawl, use this standardized crate matrix across all pure-Rust fleet repos:

| Need | Blessed Crate | Notes |
|---|---|---|
| Serialization | `serde` (`1.0`, `derive`), `serde_json` (`1.0`), `serde_yaml` (`0.9`) | Mandatory in L1/L2/L3 |
| CLI Parsing | `clap` (`4`, `derive`) | L2 only; every command MUST support `--json` |
| Async Runtime | `tokio` (`1`, `rt-multi-thread`, `macros`, `time`) | Use `OnceLock<Runtime>` in sync L2/L3 entrypoints; bound all I/O with `tokio::time::timeout` |
| HTTP / REST / OAuth2 | `reqwest` (`0.12`, `json`) | Prefer `rustls-tls` or default TLS; always set `.timeout()` on `Client::builder()` |
| Embedded SQL / RAG | `rusqlite` (`bundled`) | Zero external SQLite DLL needed on Windows |
| Date / Time / IDs | `chrono` (`0.4`), `uuid` (`1`, `v4`, `v5`) | Standard across L1 |
| Serial / SCPI / UART | `tokio-serial` or `serialport` | For Bucket B bench instruments (`multimeter`, `oscilloscope`, `bus-pirate`) |
| Windows Native APIs | `windows-sys` | Lightweight zero-overhead bindings for `windows-operations-mcp` / `sysinternals-mcp` |
| Native Desktop / Web GUI (L3) | `eframe` (`0.37`) + `egui` (`egui_kittest`, `egui_plot`) | **Primary L3 UI stack (ArtCraft standard):** Pure-Rust immediate-mode GPU GUI (`wgpu`/`glow`), zero `node_modules`, zero WebView2, compiles to native `.exe` AND WebAssembly (`wasm32`) from one codebase. |

---

## 4. Windows PowerShell & Justfile Invariants for Rust Repos

Because `$env:USERPROFILE\.cargo\bin` is not always present on the inherited `PATH` of NSSM services, IDE subshells, or clean Windows runners, every pure-Rust `justfile` MUST follow the `rust-devices-mcp` pattern:

```just
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]

default:
    @just --list

check:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo clippy --workspace --all-targets --all-features -- -D warnings

test:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo test --workspace

fmt-check:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo fmt --all --check

run-mcp:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; $env:RUST_LOG = "debug"; cargo run -p rust-devices-mcp -- mcp

build-release:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo build --release --workspace
```
