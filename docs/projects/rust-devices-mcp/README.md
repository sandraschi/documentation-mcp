---
title: "rust-devices-mcp - Project Overview & Conversion Blueprint"
category: project
status: active
last_updated: 2026-10-17
---

# rust-devices-mcp

**Repository:** `D:\Dev\repos\rust-devices-mcp`  
**GitHub:** `https://github.com/sandraschi/rust-devices-mcp`  
**Version:** `v0.4.0+` (Alpha, commit `aab6c17`, `58/58` active workspace tests passing + 1 opt-in live-camera RTSP test)  
**Architecture:** Pure-Rust ArtCraft 4-Crate Workspace (`devices-core` L1, `devices-store` L1 SQLite historian, `rust-devices-mcp` L2 CLI+MCP, `devices-app` L3 `eframe`/`egui` native GPU desktop dashboard)  
**Canonical Standard:** [standards/RUST_ARTCRAFT_STANDARD.md](../../standards/RUST_ARTCRAFT_STANDARD.md)  
**Internal Repo Docs:** `docs/PRD.md`, `docs/UI_PARITY.md`, `docs/ASSESSMENT_2026_10_17.md`, `installer/installer.nsi`  
**Shadowed Legacy Repo:** `D:\Dev\repos\devices-mcp` (Python/FastMCP)

---

## 1. Executive Summary

`rust-devices-mcp` is the **first pure-Rust MCP repository in the fleet** (`10,104` lines of zero-`unwrap` Rust across 26 source files) and serves as the conversion blueprint for migrating Bucket A and Bucket B MCP servers off the Python/FastMCP/Vite/Tailwind/sidecar stack onto the **ArtCraft containment harness**.

- **Binary Footprint:** `~11.5 MB` (`rust-devices-mcp.exe` CLI + MCP stdio server with full LAN/Cloud TLS, SQLite, RTSP/H.264, and USB camera capture) + `~31 MB` (`devices-app.exe` standalone GPU-accelerated `eframe`/`egui` desktop app) -> **`~16.8 MB` current-user NSIS installer** (`installer/installer.nsi`, down from ~150-450 MB in Python + Node/WebView2).
- **Cold Boot:** **50-70 ms** on Windows 11 (down from 2-4 seconds in Python).
- **Zero-Panic Guarantee:** Workspace-wide `deny` on `clippy::unwrap_used`, `clippy::expect_used`, `clippy::panic`, `clippy::unimplemented`, and `clippy::todo`.
- **Single Dispatch Door:** CLI `--json` flags (24 subcommands + `mcp`), MCP `2024-11-05` stdio `tools/call` (24 tools), and L3 `eframe`/`egui` views (14 pages) all route through `devices_core::dispatch(Command)` in-process, guarded at compile time by `dispatch_future_is_send`.
- **Zero-Config Legacy Fleet Import (`import.rs`) + "Joe Schmoe" Onboarding (`scan.rs` + `vault.rs` + `registry.rs`):** Automatically imports the sibling Python `devices-mcp` checkout (`config.yaml` with `${VAR:-default}` expansion, `.env`, `hue_bridge.cache`, `ring_token.cache`, `readonly` plug guards) AND provides a concurrent `/24` LAN scanner (`net.scan`), 1-click device adoption (`devices.json`), and Windows Credential Manager secret storage (`keyring 4`).

---

## 2. Four-Crate Topology (`10,104` Lines of Pure Rust)

| Layer | Crate | Path | Lines | Responsibilities |
|---|---|---|---:|---|
| **L1 (Core)** | `devices-core` | `crates/devices-core` | 4,913 | Vendor protocols, credential resolution (`creds.rs`), legacy fleet import (`import.rs`), live RTSP/H.264 video (`video.rs`), fleet crossconnect (`bridge.rs`), multi-provider LLM chat (`llm.rs`), concurrent LAN scanner (`scan.rs`), typed `DeviceError` (`error.rs`), 24-variant `Command` enum, and `dispatch()`. Zero UI/MCP/CLI dependencies. |
| **L1 (Store)** | `devices-store` | `crates/devices-store` | 300 | Bundled SQLite historian (`rusqlite 0.40`) at `%LOCALAPPDATA%/rust-devices-mcp/devices.db` with `PRAGMA user_version` migrations and 90-day retention (`energy_readings`, `weather_readings`, `alarm_events`). |
| **L2 (CLI+MCP)** | `rust-devices-mcp` | `crates/devices-mcp` | 1,436 | `clap` CLI (`--json` on every subcommand) + `mcp` subcommand running hand-rolled `MCP 2024-11-05` over `stdio` (24 tools; pure JSON-RPC on `stdout`, logs on `stderr`). |
| **L3 (GUI)** | `devices-app` | `crates/devices-app` | 3,455 | 14-view pure-Rust `eframe`/`egui` desktop dashboard (`Dashboard` with 3D GPU icosahedron, `Energy`, `Lighting` + `LightDetail`, `Climate`, `Cameras` with live RTSP H.264 player, `Weather`, `Alarms` + `DoorbellDetail`, `Crossconnect`, `Chat`, `Settings`, `Help`, `Raw JSON`), Windows Credential Manager vault (`vault.rs`), device registry (`registry.rs`), `egui_kittest` golden PNG snapshots, and `glyph_source_scan` tofu guard. |

---

## 3. Complete 24-Tool MCP & CLI Surface (`v0.4.0+`)

| Domain | Commands / Tools (24) | Drivers & Capabilities in `devices-core` / `devices-store` |
|---|---|---|
| **System** | `status` | Returns app version (`0.4.0`), mode (`pure-rust`), and all 24 registered command IDs. |
| **Smart Plugs** | `plug.get_stats`, `plug.toggle` | - **Tapo** (`plug_tapo.rs`): `tapo` crate (P115 -> P110 fallback, mW-to-W scaling `current_power / 1000.0`, today kWh, `readonly` toggle guard).<br>- **Kasa** (`plug_kasa.rs`): `kasa-rs` (`connect_auto` legacy XOR + KLAP).<br>- **Shelly** (`plug_shelly.rs`): `shelly-core` (Gen1 `/status` + Gen2/3 RPC).<br>- **Demo** (`plug.rs`): Deterministic `42.5 W / 0.85 kWh` oracle. |
| **Cameras & Live RTSP Video** | `camera.describe`, `camera.snapshot` (+ UI `Live` RTSP stream) | - **Snapshots (`camera.rs`):** SOI (`0xFF 0xD8`) + bounds-checked SOF0/1/2 parser across **Tapo** (`cam_tapo.rs`), **ONVIF** (`cam_onvif.rs`), **USB** (`cam_usb.rs`, `nokhwa` MediaFoundation), **Ring** (`ring.rs`), **URL** (`cam_url.rs`), and **Demo**.<br>- **Live RTSP/H.264 (`video.rs`):** Pure-Rust `retina 0.4` RTSP session + `openh264 0.9` decode + AVCC-to-Annex-B converter (no FFmpeg!), verified at 3 frames / 0.46s on Tapo cam `.164`. |
| **Philips Hue** | `hue.list_lights`, `hue.set_light`, `hue.pair` | Hand-rolled CLIP v1 REST (`hue.rs`) with Hue Bridge Pro self-signed HTTPS support, link-button pairing, and explicit `on` requirement. |
| **Netatmo** | `netatmo.stations` | Hand-rolled OAuth2 `refresh_token` + `getstationsdata` (`netatmo.rs`), proven live against Stroheckgasse station (`26.3 C`). |
| **Weather** | `weather.now` | Keyless Open-Meteo current weather + 24-hour hourly temperature curve (`weather.rs`, default Vienna `48.2082, 16.3738`). |
| **Ring** | `ring.status`, `ring.doorbells`, `ring.alarm`, `ring.auth`, `ring.auth_2fa` | Hand-rolled OAuth2 password + 2FA + refresh flow (`ring.rs`), doorbells/dings/motion history, alarm read/arm/disarm, and 640x360 doorbell snapshots. Siren excluded by design. |
| **Crossconnect** | `bridge.event`, `bridge.speak`, `bridge.webhook` | Thin HTTP client (`bridge.rs`) talking to `aiwatcher` (`:10946/api/fleet/ingest`), `speech-mcp` (`:10909/api/v1/tts`, verified live on server speakers), and generic `http(s)` webhooks. |
| **SQLite Historian** | `energy.history`, `weather.history`, `alarm.history` | Queries local `%LOCALAPPDATA%/rust-devices-mcp/devices.db` (`devices-store`) auto-populated by `dispatch()`. |
| **Local/Cloud LLM** | `llm.chat`, `llm.models` | Unified chat & model discovery (`llm.rs`) for **Ollama** (`:11434`, `qwen3.8:27b`), **LM Studio** (`:1234`), **OpenAI**, **Anthropic** (`/v1/messages`), and custom endpoints. |
| **LAN Discovery** | `net.scan` | Concurrent `/24` TCP port scanner (`scan.rs`, 256-way concurrency) with unauthenticated HTTP/HTTPS identification for Hue Bridge / Hue Bridge Pro and Shelly Gen1. |
