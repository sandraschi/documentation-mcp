---
title: "Fleet 4-Bucket Triage & Mass PyPI-to-Rust Transpilation Doctrine"
category: standard
status: active
audience: all-agents
last_updated: 2026-10-17
---

# Fleet 4-Bucket Triage & Mass `PyPI -> Rust` Transpilation Doctrine

**Parent Hub:** [RUST_ARTCRAFT_STANDARD.md](../RUST_ARTCRAFT_STANDARD.md)  
**Pilot Reference Implementation:** [`rust-devices-mcp`](../../projects/rust-devices-mcp/README.md) (`D:\Dev\repos\rust-devices-mcp`)

---

## 1. Fleet Rustification Strategy: The 4-Bucket Triage Matrix

Should we convert most of the 187 `*-mcp` repositories to the pure-Rust ArtCraft pattern?

**Yes for ~70% of the fleet (Buckets A & B), Hybrid for ~15% (Bucket C), and No for ~15% (Bucket D).**

| Bucket | Fleet Share | Target Profile | Representative Fleet Repos | Architecture Verdict |
|---|---|---|---|---|
| **Bucket A: REST, Cloud APIs, SQLite, System, CLI & File Ops** | **~55% (~100 repos)** | Speaks HTTP/JSON, SQLite, OS APIs, or wraps a CLI binary | `arr-mcp`, `plex-mcp`, `jellyfin-mcp`, `immich-mcp`, `calibre-mcp`, `kavita-mcp`, `komga-mcp`, `github-mcp`, `forgejo-mcp`, `discord-mcp`, `bluesky-mcp`, `mastodon-mcp`, `notion-mcp`, `stripe-mcp`, `tailscale-mcp`, `docker-mcp`, `podman-mcp`, `kubernetes-mcp`, `filesystem-mcp`, `fastsearch-mcp`, `disk-usage-mcp`, `windows-operations-mcp`, `sysinternals-mcp`, `rss-mcp`, `bookmarks-mcp` | **100% Pure Rust (Highest ROI).** Only needs `reqwest`, `rusqlite`, `tokio::process`, or `windows-sys`. Zero obscure crates needed. |
| **Bucket B: Clean Hardware, Bench Instruments & Local IoT** | **~15% (~30 repos)** | Speaks SCPI (TCP/Serial/USB-TMC), JTAG/SWD, Modbus, OSC, WebSocket, RTSP, or LAN REST | `rust-devices-mcp`, `oscilloscope-mcp`, `multimeter-mcp`, `power-supply-mcp`, `function-generator-mcp`, `spectrum-analyzer-mcp`, `bus-pirate-mcp`, `jtag-swd-mcp`, `obs-mcp`, `reaper-mcp`, `vcv-rack-mcp`, `resolume-mcp`, `osc-mcp` | **100% Pure Rust.** Direct SCPI over `tokio::net::TcpStream` (`:5025`) or `tokio-serial` replaces bloated NI-VISA/`pyvisa`. `probe-rs` is SOTA for JTAG/SWD. |
| **Bucket C: Host-App Embedded Scripting & Reverse-Engineered Cloud Crypto** | **~15% (~25 repos)** | Runs Python *inside* a host binary (`bpy`, `pcbnew`, FreeCAD) OR relies on fast-moving community reverse-engineered crypto (`python-miio`, `alexapy`) | `blender-mcp`, `freecad-mcp`, `kicad-mcp`, `gimp-mcp`, `inkscape-mcp`, `davinci-resolve-mcp`, `libreoffice-mcp`, `dreame-mcp`, `alexa-mcp`, `nest-protect-mcp` | **Split Verdict:**<br>- **Host-App Bridges:** Rustify the MCP server + `egui` app (`L1/L2/L3`) talking over a local TCP/pipe socket to a thin 100-line Python listener inside Blender/FreeCAD.<br>- **Undocumented Cloud Crypto (`dreame`, `alexa`):** Keep Python until protocol stabilizes; do not hand-maintain monthly Xiaomi/Amazon auth reverse-engineering in Rust. |
| **Bucket D: Heavy PyTorch / CUDA / Training / Multimodal ML** | **~15% (~30 repos)** | Loads `.safetensors`/CUDA kernels via PyTorch, Triton, Diffusers, Unsloth, or IsaacLab | `unsloth-mcp`, `triton-mcp`, `vla-mcp`, `avatar-pipeline-mcp`, `splatmaker-mcp`, `songgeneration-mcp`, `kyutai-mcp`, `uitars-mcp`, `isaac-mcp`, `mujoco-mcp`, `speech-mcp` | **Stay Python (or Rust Front-Door + Python GPU Worker).** Rewriting PyTorch/CUDA ecosystems in pure Rust is a negative-ROI trap unless inference is pure ONNX (`ort`) or local HTTP to Ollama/vLLM. |

---

## 2. Storming the Python Bastille: The Mass `PyPI -> Rust` Transpilation Doctrine

For 15 years, Python held a monopoly over the long-tail integration ecosystem (`pysomething` packages on PyPI for smart home devices, bench electronics, media servers, cloud APIs, and file formats) for **one reason only: human authoring friction**. When a weekend reverse-engineer figured out a Ring doorbell handshake, a Netatmo OAuth flow, a Xiaomi MiIO packet, or a Rigol SCPI quirk, they wrote `requests.post(...)` and `json.loads(...)` in Python because writing a zero-panic async Rust crate with custom error types and serde structs by hand took 10x longer.

**Agentic coding inside an ArtCraft containment harness completely inverts that economic equation.**

### 2.1 Why the "PyPI Moat" Just Evaporated

When you inspect almost any long-tail `pysomething` package on PyPI or GitHub, its contents split 15/85:
1. **The Protocol Essence (~15% of the repo):** The hard-won domain truth -- exact endpoint URLs, undocumented headers (`hardware_id`, `2fa-support: true`), OAuth grant quirks, AES/XOR framing, or register offsets.
2. **The Python Ceremony (~85% of the repo):** `setup.py` / `pyproject.toml`, `requests` vs. `aiohttp` wrapper classes, dynamic `dict` munging, untyped exception hierarchies, and Python 3.x compatibility shims that rot every two minor releases.

To a human developer, rewriting that 15% essence in Rust was tedious.
**To an LLM agent inside an ArtCraft harness, an existing Python library is no longer a runtime dependency to `pip install` -- it is a free, plain-text, machine-readable wire specification to compile directly into native Rust.**

- In [`rust-devices-mcp`](../../projects/rust-devices-mcp/README.md), it took human maintainers *years* of `mitmproxy` and Wireshark captures to discover the protocol inside `python-ring-doorbell`, `pyatmo`, and `aiohue`.
- It took OpenCode **minutes** to read those Python files as specifications and emit [`ring.rs`](file:///d:/Dev/repos/rust-devices-mcp/crates/devices-core/src/ring.rs), [`netatmo.rs`](file:///d:/Dev/repos/rust-devices-mcp/crates/devices-core/src/netatmo.rs), and [`hue.rs`](file:///d:/Dev/repos/rust-devices-mcp/crates/devices-core/src/hue.rs) -- zero-unwrap, memory-safe, native Rust modules compiling into a single standalone binary.

### 2.2 Why Agents Write *Safer* Rust Than Python

Counterintuitively, LLMs are far more reliable writing strict Rust than writing dynamic Python:

| Dimension | LLM Writing Python (`pysomething`) | LLM Writing Strict Rust (ArtCraft Harness) |
|---|---|---|
| **Verification Loop** | **Open loop.** Code parses even when attribute names, dict keys, or `None` branches are hallucinated. Bugs hide until production runtime. | **Closed loop.** `rustc` + `clippy -D warnings` + `deny(unwrap_used)` act as an adversarial theorem prover. The agent loops until every branch and error path is proven sound at compile time. |
| **Dependency Solver** | `pysomething` pins `aiohttp<4`, `pydantic<2`, `cryptography==39.*`, causing version-solver deadlocks across venvs. | Compiles to a self-contained static `.exe` against `reqwest` + `serde`. Zero runtime dependency solver on the target machine. |
| **Architectural Drift** | An agent can silently mutate a shared dict, leak state across async tasks, or `print()` debug text onto `stdout`. | Ownership, borrow checking, crate boundary visibility, and exhaustive `match` on `Command` turn architectural drift into immediate compile errors. |

**Core Axiom:** *Python optimizes for human typing speed; Rust optimizes for automated verification speed.* When agents generate code at 100+ tokens/sec, human typing speed is worth zero, and compile-time verification speed is worth everything.

### 2.3 The Three Waves of the Great `PySomething` Rustification

1. **Wave 1 (2021-2025) -- The Infrastructure Layer (Complete):**
   - Humans rewrote Python's own core tooling in Rust: `ruff` (replacing Flake8/Black/isort), `uv` (replacing pip/venv/poetry), `pydantic-core`, `polars`, `tokenizers`.
2. **Wave 2 (2026-2027) -- The Glue, CLI, Daemon & MCP Layer (Active Now in Our Fleet):**
   - Retiring 150 MB bundled Python interpreters that exist only to talk to REST APIs, SQLite databases, LAN IoT devices, or serial ports.
   - Every MCP server, CLI tool, and local daemon absorbs its `pysomething` dependency directly into a 150-300 line `<domain>-core` Rust module (or spins it out as a standalone `*-rs` crate).
3. **Wave 3 (2027+) -- Automated Clean-Room Transpilation of Long-Tail PyPI:**
   - Entire categories of PyPI (protocol parsers, hardware drivers, file-format readers, cloud SDKs) batch-ported to `crates.io` by agent loops using the upstream Python `pytest` fixtures as the ground-truth verification oracle.

### 2.4 The Mechanical 4-Step "PyPI-as-Oracle" Conversion Playbook

Whenever an agent in this fleet converts a Python MCP repo (or any tool wrapping a `pysomething` package where no mature Rust crate exists), follow this exact 4-step playbook:

1. **Recon the Python Wire Spec (Read, Never Vendor):**
   - Locate the upstream `pysomething` source (in `.venv/Lib/site-packages/` or GitHub).
   - Extract the 15% wire essence: base URLs, auth/refresh flows, custom headers, request/response JSON shapes, timeouts, and error codes.
2. **Extract Golden Test Vectors (The Oracle):**
   - Copy or transcribe representative JSON/binary fixtures from the Python library's `tests/` directory (or capture live responses) to serve as deterministic unit-test inputs in Rust.
3. **Synthesize the L1 Rust Module Under `deny(unwrap_used)`:**
   - Write `crates/<domain>-core/src/<vendor>.rs` using only the blessed stack (`reqwest`, `serde`, `serde_json`, `tokio`, `uuid`, `chrono`).
   - Map all network, timeout, auth, and parse failures into `<Domain>Error` (`Timeout`, `Auth`, `Protocol`, `Offline`, `InvalidInput`, `Unsupported`).
   - Expose a `Vendor::Demo` / `Source::Demo` deterministic path for zero-hardware CI verification.
4. **Verify Parity & Mint Reusable Crates:**
   - Run `just check` (`clippy -D warnings`) and `just test` against the golden fixtures and live hardware.
   - When a hand-rolled L1 protocol module (`ring.rs`, `netatmo.rs`, `hue.rs`, SCPI, etc.) reaches full maturity, it can be factored out into its own standalone `<vendor>-rs` crate -- turning our 220-repo MCP fleet into a factory for the modern async Rust crates that `crates.io` was missing.

---

## 3. Top 35 Wave-1 Conversion Candidates (With Exact Reasons & Target Crates)

Based on a direct census of the 220 `*-mcp` directories in `D:\Dev\repos`, these **35 repositories across 5 sub-domains** offer the highest immediate ROI for `repconv` conversion.

### 3.0 Wave-0 First-Pilot Shortlist: Which Repo Should We Test `repconv` on First?
To validate the end-to-end `repconv` workflow (cloning the 70% kernel from `rust-devices-mcp`, running `gemma4:12b` wire-spec extraction, writing the 30% domain logic, and passing all 6 ArtCraft gates in a single low-token session), start with these daily-driver Wave-0 pilots:

| Pilot Rank | Repo | Why It Is the Ideal First `repconv` Test | Expected Effort & Payoff |
|---|---|---|---|
| **#1 Recommended First Pilot (Daily-Driver Local SQLite Library)** | **`calibre-mcp`** | Zero elevated services, zero external hardware dependencies. Calibre's `metadata.db` is a standard local SQLite database (`books`, `authors`, `tags`, `series`, `comments`, `data`). In Python, `calibre-mcp` needed an HTTP daemon + stdio proxy on `:10720` just to avoid startup/lock pain. In Rust (`rust-calibre-mcp`), bundled `rusqlite` queries 50,000 books in `< 2 ms`, `import.rs` auto-discovers the library path from `../calibre-mcp`, and `egui` renders a crisp cover-art grid + `gemma4:12b` book assistant. | **~20--25 min (`< 25k` tokens).** Retires the `:10720` Python proxy daemon and proves `rusqlite` + `egui` card/table UI on a daily driver. |
| **#2 Twin Daily-Driver Pilot (Pure HTTP REST Media Server)** | **`plex-mcp`** *(and sibling `arr-mcp`)* | Structurally almost identical to `calibre-mcp` in the UI (Media Grid, Search, Detail Inspector, Playlists), while testing pure HTTP REST (`reqwest` against Plex `:32400` with `X-Plex-Token` + `Accept: application/json`). Replaces a massive Python `PlexAPI` + FastAPI + **Next.js 15.2** stack (`:10740/:10741`) and its image-proxy routes with a single 8 MB native `.exe`. | **~20--25 min.** Reuses 85% of the `rust-calibre-mcp` media browser UI layout while proving `import.rs` (`.env` `PLEX_URL`/`PLEX_TOKEN`) + `reqwest`. |
| **#3 Best Bucket B Hardware Instrument Pilot** | **`multimeter-mcp`** *(or `oscilloscope-mcp`)* | Replaces a 500 MB Python `pyvisa` stack with 120 lines of raw async SCPI over `tokio::net::TcpStream` (`:5025`) / `tokio-serial`, plus a live 60 FPS `egui` GPU waveform/readout panel and `rusqlite` measurement historian. | **~25--30 min.** Proves Bucket B bench-electronics superiority (`egui` GPU plotting + `<domain>-store`). |

> **How `fastsearch-mcp`'s Privilege-Split Architecture Works Under `repconv`:** `fastsearch-mcp` uses a deliberate two-tier privilege split ([`fastsearch-mcp/AGENTS.md`](../../../fastsearch-mcp/AGENTS.md)):
> 1. **Elevated `LocalSystem` C++ Service (`FastSearchServiceNew.exe`):** Installed *once* with elevation so it holds the raw NTFS `$MFT` volume handle (`\\.\C:`) and exposes named pipe `\\.\pipe\FastSearchMCP_v2` (`\\.\pipe\FastSearchMCP`).
> 2. **Unprivileged Userland Pipe Client ([`pipe_client.py`](../../../fastsearch-mcp/src/fastsearch_mcp/pipe_client.py)):** Lives 100% in normal userland (zero UAC/elevation during normal use) and speaks a trivial 4-byte little-endian length-prefixed JSON protocol (`u32::to_le_bytes(len)` + UTF-8 JSON) over the named pipe.
>
> **Conversion Rule for `fastsearch-mcp`:** **Never rewrite the working C++ `LocalSystem` service.** Keep `FastSearchServiceNew.exe` as the install-once elevated service, and convert **only the userland half** (replacing Python `pywin32` + FastAPI `:10845` + React `:10844` with a 40-line `tokio::net::windows::named_pipe` L1 client in `rust-fastsearch-mcp` + an instant `egui` search table in userland).

### 3.1 Group 1: Smart Home & IoT Siblings (Zero-Friction -- Drivers Already Written in `rust-devices-mcp`!)
| Repo | Why It Is a Prime Candidate | Rust Crates / Reusable Modules |
|---|---|---|
| `tapo-mcp`, `ring-mcp`, `netatmo-weather-mcp` | **100% of their protocol code is already written, tested, and proven live in `rust-devices-mcp` (`plug_tapo.rs`, `cam_tapo.rs`, `ring.rs`, `netatmo.rs`)!** Can be either absorbed/retired into `rust-devices-mcp` or spun out as thin workspace aliases. | Direct reuse of `devices-core` modules |
| `home-assistant-mcp` | Pure REST (`POST /api/services/<domain>/<service>`) + WebSocket event stream (`/api/websocket`). Eliminates Python interpreter overhead for 24/7 home automation. | `reqwest`, `tokio-tungstenite`, `serde_json` |
| `nuki-mcp`, `smoke-detector-mcp`, `nest-protect-mcp` | Local Bridge HTTP REST + token auth + webhook event ingestion into `devices-store` (`alarm_events`). | `reqwest`, `rusqlite` (`devices-store`) |

### 3.2 Group 2: Bench Electronics, Embedded & Hardware Instruments (Massive Latency & Driver Win)
| Repo | Why It Is a Prime Candidate | Rust Crates / Reusable Modules |
|---|---|---|
| `oscilloscope-mcp`, `multimeter-mcp`, `power-supply-mcp`, `function-generator-mcp`, `spectrum-analyzer-mcp` | Python versions drag in 500 MB NI-VISA / `pyvisa` / `pyvisa-py` stacks just to send ASCII SCPI strings (`*IDN?`, `:MEAS:VOLT:DC?`) over TCP `:5025` or USB-Serial. Furthermore, `egui` renders **120 FPS live oscilloscope/spectrum waveforms** natively on the GPU! | `tokio::net::TcpStream` (`:5025` raw SCPI), `tokio-serial`, `egui` GPU canvas / `egui_plot` |
| `logic-analyzer-mcp`, `bus-pirate-mcp`, `jtag-swd-mcp` | Rust is the undisputed SOTA language for embedded debugging (`probe-rs` is written in Rust!). Eliminates fragile Python libusb/OpenOCD wrappers. | `probe-rs`, `tokio-serial`, `rusqlite` |
| `sdr-mcp`, `openbci-mcp`, `lidar-mcp` | High-throughput binary byte streams (IQ samples, EEG channels, point clouds) where Python's GIL and GC cause dropped packets; Rust + `egui` renders live waterfalls/plots at 60+ FPS with zero copy. | `tokio::net::UdpSocket`, `tokio-serial`, `egui` `TextureHandle::set` |

### 3.3 Group 3: Local OS, Filesystem, Search & Infrastructure Daemons (10--100x Speedup)
| Repo | Why It Is a Prime Candidate | Rust Crates / Reusable Modules |
|---|---|---|
| `filesystem-mcp`, `disk-usage-mcp` *(and `fastsearch-mcp` pipe client)* | File tree traversal, directory scanning, and regex search in Rust (`ignore`, `grep-searcher`, `walkdir`, `rayon`) are **20--100x faster** than Python and boot in `50 ms`. *(For `fastsearch-mcp`, keep the existing C++ `FastSearchServiceNew.exe` elevated `$MFT` service and replace only the Python `\\.\pipe\FastSearchMCP` client + React UI with Rust).* | `ignore`, `grep-searcher`, `walkdir`, `notify`, `tokio::net::windows::named_pipe` |
| `windows-operations-mcp`, `sysinternals-mcp`, `system-admin-mcp`, `monitoring-mcp` | Direct Win32/WMI/ETW/Service Control Manager calls (`windows-sys`, `sysinfo`) without spawning slow PowerShell child processes for every metric. | `windows-sys`, `sysinfo`, `rusqlite` |
| `secrets-mcp`, `multi-backup-mcp`, `winrar-mcp`, `pdf-mcp` | Native OS Credential Manager (`keyring 4`, already proven in `vault.rs`), fast streaming SHA-256/zstd archive verification, and pure-Rust PDF parsing (`lopdf`/`pdf-extract`). | `keyring`, `sha2`, `zip`/`tar`, `lopdf` |
| `docker-mcp`, `podman-mcp`, `kubernetes-mcp`, `tailscale-mcp` | Speaks HTTP-over-named-pipe/Unix-socket to Docker/Podman API (`bollard` or `reqwest`) or wraps `tailscale.exe --json` with typed structs. | `reqwest`, `bollard`, `tokio::process` |

### 3.4 Group 4: Self-Hosted Media, Arr Stack, Libraries & Knowledge Bases (Pure REST + SQLite)
| Repo | Why It Is a Prime Candidate | Rust Crates / Reusable Modules |
|---|---|---|
| `arr-mcp`, `plex-mcp`, `jellyfin-mcp`, `iptv-org-mcp` | 100% clean HTTP REST + API key header + JSON responses + m3u8 playlist parsing. Zero Python-specific dependencies. | `reqwest`, `serde_json`, `rusqlite` |
| `calibre-mcp`, `kavita-mcp`, `komga-mcp`, `immich-mcp` | Calibre's `metadata.db` is a standard SQLite database! `rusqlite` (`bundled` with FTS5) queries 50,000 books in `< 2 ms`, and `egui` renders cover-art grids natively via `image`. | `rusqlite` (`bundled`), `reqwest`, `image`, `zip` (EPUB/CBZ) |
| `rss-mcp`, `bookmarks-mcp`, `obsidian-mcp`, `quicknotes-mcp`, `advanced-memory-mcp` | Local Markdown + SQLite FTS5 + Atom/RSS XML feeds (`quick-xml` / `feed-rs`). Replaces slow Python startup with instant local knowledge tools. | `rusqlite`, `ignore`, `reqwest`, `quick-xml` |

### 3.5 Group 5: Creator, Real-Time Audio/Video & OSC Control Bridges (Jitter-Free Real-Time)
| Repo | Why It Is a Prime Candidate | Rust Crates / Reusable Modules |
|---|---|---|
| `obs-mcp`, `osc-mcp`, `reaper-mcp`, `vcv-rack-mcp`, `resolume-mcp`, `virtualdj-mcp`, `mixx-dj-mcp` | Speaks OBS WebSocket v5 (`tokio-tungstenite` + SHA256 auth challenge) or UDP Open Sound Control (`rosc`). Native `egui` control surfaces give DJs and streamers a zero-latency, 15 MB RAM companion panel instead of a 400 MB WebView2 window while GPU/audio workloads are running. | `rosc`, `tokio-tungstenite`, `tokio::net::UdpSocket`, `eframe` |

---

## 4. Which Repos Resist Conversion? (And How to Handle Them)

Not every repository in the 220-repo fleet should be blindly transpiled to pure Rust. Repositories that resist conversion fall into **four distinct categories**, each with a clear architectural rule:

| Resistance Category | Fleet Examples | Why They Resist Pure Rust | Mandatory Fleet Strategy |
|---|---|---|---|
| **1. Heavy PyTorch / CUDA / Triton / `.safetensors` Model Hosts (Bucket D -- ~30 repos)** | `unsloth-mcp`, `triton-mcp`, `vla-mcp`, `avatar-pipeline-mcp`, `splatmaker-mcp`, `songgeneration-mcp`, `kyutai-mcp`, `uitars-mcp`, `isaac-mcp`, `mujoco-mcp`, `speech-mcp`, `invokeai-mcp`, `comfyops-mcp` | They execute custom CUDA C++ kernels via `torch`, `triton`, `diffusers`, `xformers`, or NVIDIA IsaacLab/PhysX Python bindings. Rewriting PyTorch training/diffusion pipelines in Rust (`candle`/`burn`) loses 90% of upstream model ecosystem compatibility. | **DO NOT CONVERT THE GPU WORKER.** Keep the Python CUDA worker, OR (optional) put a thin Rust `L2/L3` front-door + `egui` UI in front of the Python inference HTTP port (exactly as `bridge.rs` calls `speech-mcp` on `:10909`). |
| **2. In-Process Host-Application Python Scripting (Bucket C1 -- ~12 repos)** | `blender-mcp` (`import bpy`), `freecad-mcp` (`import FreeCAD`), `kicad-mcp` (`import pcbnew`), `gimp-mcp`, `inkscape-mcp`, `davinci-resolve-mcp`, `libreoffice-mcp` | Blender, FreeCAD, KiCad, and DaVinci Resolve embed a CPython interpreter *inside* the host C++ application process. The inner plugin script *must* be Python because the host API is a CPython C-API module. | **HYBRID SPLIT (High ROI!):** Convert the outer MCP server, CLI, and `egui` desktop app (`L1/L2/L3`) to **Pure Rust**, and have `L1` talk over a localhost TCP/named-pipe socket to a tiny, zero-dependency 80-line Python listener running inside Blender/FreeCAD/KiCad! |
| **3. Volatile Anti-Bot / Reverse-Engineered Cloud Auth (Bucket C2 -- ~6 repos)** | `dreame-mcp` (`python-miio` custom cloud crypto), `alexa-mcp` (`alexapy` Amazon web-view anti-bot cookie/CAPTCHA dance), `bilibili-mcp`, `readly-mcp` | Vendors like Amazon and Xiaomi rotate undocumented login/CAPTCHA/signing schemes every few months; the community patches land in Python libraries first. | **DEFER UNTIL STABLE.** Only port via `PyPI-as-Oracle` when the auth protocol is stable (like Ring, Hue, and Netatmo proved to be in `rust-devices-mcp`). |
| **4. Heavy Browser DOM / Office COM / Win32 GUI Tree Walkers (~6 repos)** | `browser-mcp`, `playwright-mcp`, `pywinauto-mcp`, `onenote-mcp`, `ms-graph-mcp` | Tightly coupled to Playwright's Python selector engine or Windows UIAutomation / COM dynamic dispatch (`pywinauto` / `win32com`). | **EVALUATE CASE-BY-CASE:** Keep `pywinauto-mcp` in Python (or migrate to Rust `uiautomation` crate only after side-by-side benchmark); browser CDP repos can stay on Playwright MCP. |

