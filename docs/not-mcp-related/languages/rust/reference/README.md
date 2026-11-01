# Rust Reference: Blessed Crates, egui React Replacement, Cheat Sheets

**Parent:** [Rust Hub](../README.md) | **Standard:** [RUST_ARTCRAFT_STANDARD.md](../../../standards/RUST_ARTCRAFT_STANDARD.md)

Copy-paste surface for daily Rust work in this fleet. Prose and rationale live in the Hub and Docs.

---

## 1. Blessed crate stack (SOTA 2026, fleet-wide)

Use this matrix unless you have a written reason not to. It prevents dependency sprawl across 100+ Rust repos.

| Need | Crate (version) | Notes |
|---|---|---|
| Serialization | `serde` 1.0 + derive, `serde_json` 1.0 | Mandatory in L1/L2/L3. Structs derive Serialize/Deserialize; MCP and CLI share the same types. |
| CLI | `clap` 4 + derive | L2 only. Every command supports `--json` for agent scripting. |
| Async runtime | `tokio` 1 (rt-multi-thread, macros, time) | `OnceLock<Runtime>` in sync entrypoints; bound all I/O with `tokio::time::timeout`. |
| HTTP / REST / OAuth2 | `reqwest` 0.12 + json | Always `.timeout()` on Client::builder. Direct-protocol rule: prefer hand-rolled reqwest module over abandoned 0.0.x wrappers. |
| SQL / embedded RAG | `rusqlite` + bundled | Zero external SQLite DLL on Windows. |
| Time / IDs | `chrono` 0.4, `uuid` 1 (v4, v5) | Standard across L1. UUIDv5 used for hardware_id style fingerprints (Ring pattern). |
| Serial / SCPI / UART | `tokio-serial` or `serialport` | Bucket B bench instruments (:5025 SCPI, Modbus, USB-TMC). |
| Windows natives | `windows-sys` | Lightweight bindings for windows-operations/sysinternals class repos. |
| Errors | `thiserror` (libs), `anyhow` (apps) | Fleet gate bans unwrap/expect/panic; errors are typed and propagated with `?`. |
| Crypto/hash | `sha2`, `hmac`, `aes`, `base64`, `hex` | Xiaomi MiIO-style framing, OAuth signing, checksum validation. |
| Desktop GUI L3 | `eframe` + `egui` (+ `egui_extras`, `egui_plot`) | Primary ArtCraft L3. Immediate-mode, GPU via wgpu/glow, 60-144 FPS, zero node_modules. |
| GPU abstraction | `wgpu` | Backs eframe/egui on DX12/Vulkan/Metal. Write raw wgpu only for custom renderers; most apps stay at egui level. |
| Alternative GUIs | `iced`, `gpui` (Zed), `tauri` v2 fallback | iced for Elm-style retained UI; gpui for Zed-class text editors; tauri only for legacy transition shells. |
| WASM | `wasm-bindgen`, `wasm-pack`, `eframe` web | Compile L1 logic or full egui app to wasm32-unknown-unknown. |
| Media/USB edge | `nokhwa`, `cpal`, `hidapi`, `btleplug` | Verify signatures against installed registry source first (cutoff hallucination trap). |
| Plugins (user hooks) | `extism`, `mlua`, `rquickjs` | Keep core zero-panic Rust; run 20-line user scripts in a sandboxed micro-VM. Replaces TS plugin excuse for staying on Node. |

---

## 2. egui + wgpu as the React replacement (the 15-layer funeral)

Legacy cost to put one button on screen (Python driver + FastMCP + Pydantic + FastAPI + Uvicorn + ports + CORS + TS fetch + Zustand + useEffect + tsx + Tailwind + Vite + node_modules + Biome + Tauri IPC + WebView2): 15 layers, 3 languages, 250-500 MB RAM, 450 MB disk per repo.

ArtCraft L3 cost: 1 language, 1 toolchain, 5 lines.

```rust
// crates/<domain>-app: one button, zero HTTP, zero JS/CSS
if ui.button("Toggle Plug").clicked() {
    self.last_result = Some(run(Command::PlugToggle {
        vendor: self.vendor,
        device_ip: self.ip.clone(),
        state: !self.is_on,
        creds: self.creds.clone(),
    }));
}
```

Why it wins:

- **Footprint:** 15-30 MB RAM (native wgpu surface) vs 250-500 MB (Python + Uvicorn + Chromium). 2-4 MB exe vs 450 MB venv + node_modules + dist.
- **Latency:** sub-millisecond in-process `dispatch()` vs fetch -> CORS -> FastAPI -> Python. 60-144 FPS immediate-mode vs DOM layout + IPC + localhost serialization.
- **Agent velocity:** add 1 Command variant in L1 + 5 lines of `ui.horizontal(...)` in L3, compiler verifies end to end. Legacy required edits across 6 files in 3 languages with CORS/type/hook failure modes.
- **Testing:** `egui_kittest` or headless rasterizer renders frames inside `cargo test` in milliseconds. Legacy required Uvicorn + Vite + headless Playwright.
- **Portability:** same codebase compiles to Windows exe, macOS Metal, Linux Vulkan, and WASM for browser. No WebView2 quirks, no port registry, no sidecar zombies.

GPU punchline ("who does UI on the GPU?!"): Electron/WebView critics mocked Zed's gpui and egui for writing shaders to draw text boxes - while running a 15-million-line Chromium compositor (Skia + Blink + Dawn) that rasterizes HTML/CSS into GPU triangles anyway after DOM, CSS cascade, and JS GC. egui/gpui cut out the middleman: compute layout in flat Rust arrays, upload one vertex buffer, draw in under 0.5 ms via wgpu/Metal/DX12/Vulkan. UI becomes a pure function `fn update(&mut self, ctx: &egui::Context)` of current structs every frame: no shadow DOM, no stale closure, no CSS war. That is why agent loops could build FilmCraft/PhotoCraft/CADCraft without drowning in frontend state bugs.

When to pick what:

- **Default L3:** `eframe` + `egui` + `egui_extras` (tables/images) + `egui_plot` (telemetry/waveforms).
- **Pro text editor / 120 Hz lists:** `gpui` (Zed pattern, steepest curve, fastest text).
- **Elm-style retained widgets:** `iced`.
- **Legacy bridge only:** `tauri` v2 while retiring a React app; never for greenfield.

---

## 3. MCP + CLI + GUI parity (the triple-face contract)

Every capability is one `Command` variant with a canonical string ID. CLI subcommands, MCP `tools/call`, and egui buttons all construct the variant and call the same `dispatch()`.

- L2 stdio invariant: in `mcp` mode, **stdout is 100 percent line-delimited JSON-RPC (MCP 2024-11-05)**. All diagnostics go to stderr via `eprintln!`. One stray `println!` breaks the handshake.
- Tool naming: internal bus uses dots (`plug.get_stats`) but strict hosts validate `^[a-zA-Z0-9_-]{1,64}$`. Expose underscores (`plug_get_stats`) in `tools/list`, or accept both spellings in `call_tool` match arms.
- No binary blobs over MCP: validate bytes (for example JPEG SOI `0xFF 0xD8` + SOF dimensions), optionally write to `out_path`, return metadata JSON (`bytes`, `width`, `height`, `path`). Never dump megabytes of base64 into LLM context.
- Demo oracle: every controller supports `Vendor::Demo` returning deterministic constants tagged `"vendor": "demo"` so CI, stdio probes, and onboarding previews run with no hardware.
- Credential fence: explicit flag/arg wins, vendor env var fallback (`TAPO_EMAIL`, `HUE_USERNAME`, ...), missing creds produce typed `Auth` error naming the flag/var - never logging secrets.

---

## 4. Cheat sheets

**Cargo daily:**

```powershell
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace
cargo fmt --all --check
cargo run -p rust-<domain>-mcp -- <subcommand> --json
cargo run -p rust-<domain>-mcp -- mcp
cargo build --release --workspace
```

**justfile pattern (Windows-safe):**

```just
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
check:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo clippy --workspace --all-targets --all-features -- -D warnings
test:
    $env:Path = "$env:USERPROFILE\\.cargo\\bin;$env:Path"; cargo test --workspace
```

**Serde struct:**

```rust
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, Serialize, Deserialize)]
struct Config { ip: String, port: u16 }
```

**Bounded fetch:**

```rust
let client = reqwest::Client::builder().timeout(std::time::Duration::from_secs(8)).build()?;
let res = tokio::time::timeout(
    std::time::Duration::from_secs(10),
    client.get(url).send(),
).await.map_err(|_| DomainError::Timeout)??;
```

**Safe slice + checked math:**

```rust
let b = buf.get(i).ok_or(DomainError::Protocol("short frame"))?;
let end = start.checked_add(len).ok_or(DomainError::InvalidInput("overflow"))?;
```

**Workspace deny gates (root Cargo.toml + every lib.rs/main.rs):**

```toml
[workspace.lints.clippy]
unwrap_used = "deny"
expect_used = "deny"
panic = "deny"
unimplemented = "deny"
todo = "deny"
```
