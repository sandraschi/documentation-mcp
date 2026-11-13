# CelCraft - fleet project entry

**Status:** Active. v1.5.0, Tier 7 complete. Tier 8 (GPU Render Parity & Hardening) is planned and required for full parity.
**Type:** Pure-Rust ArtCraft 3-tier workspace (desktop app + CLI + MCP stdio). **No ports, no webapp.**
**Repo:** `D:\Dev\repos\celcraft`
**Authoritative status:** the repo `README.md` "Status: what is real, what is a shell" table and the repo `HANDOVER.md`. This page summarises; it does not override them.

---

## What it is

A clean-room, native Rust (`forbid(unsafe_code)`) digital ink-and-paint and classical animation workstation aimed at the traditional scanned-cel and paperless frame-by-frame workflow that OpenToonz / Toonz Harlequin served. Three crates tiers: headless engine (`cel-*` L1), CLI + MCP driver (`cel-mcp` L2), and an `egui` workstation (`cel-ui` L3).

## Current state (v1.5.0)

| Area | State |
|---|---|
| Engine: raster, fill, autogap, Sauvola, peg warp, normal maps, optical flow, LPC lip-sync, `.tlv`/`.tnz`, multiplane math | Real, unit-tested, zero unsafe |
| CLI (`--json`) + MCP stdio, 37 tools | Real |
| `.celcraft` project save/open, ink strokes, undo/redo | Real |
| Animation export: PNG frames + MP4/GIF (`render-animation`) | Real |
| Desktop UI: menus dispatch, Stage renders engine frames, timeline, Pen paint, save/open | Real |
| Audio & master delivery: CPAL playback, WAV waveform, WAV lip-sync, OpenEXR write, ProRes 4444 stream, BLAKE3 CAS | Real (Tier 7) |
| wgpu compute DAG, `egui_kittest` snapshots, panel docking, native file dialog, layers/paint channel | Planned Tier 8 |

Known gaps are documented in the repo README and PRD section 6.

## Run

```powershell
cd D:\Dev\repos\celcraft
just gates                                  # tests (serialized) + clippy + fmt
just demo                                   # 48 PNG frames + animation.mp4/gif
cargo run --release -p cel-ui               # workstation
cargo run -p cel-mcp -- status --json
cargo run -p cel-mcp -- mcp                 # MCP stdio server
```

Build artifacts: `target\release\cel-mcp.exe`, `target\release\cel-ui.exe`, `target\celcraft-v1.5.0-setup.exe`.

## Mirrored docs

- [PRD.md](./PRD.md) - requirements + section 6 implementation-status matrix (shipped vs planned)
- [TIERED_PLAN.md](./TIERED_PLAN.md) - Tiers 1-8 with verification gates
- [ARCHITECTURE.md](./ARCHITECTURE.md) - memory layout, bitfield, autogap, render DAG, crate responsibilities
- [HANDOVER.md](./HANDOVER.md) - current state, what is not real, next step
- [CHANGELOG.md](./CHANGELOG.md) - release history

## Fleet notes

- No network ports are allocated for this repo (in-process engine; stdio MCP).
- The test suite shares process-global state and must run with `--test-threads=1` (the justfile does this).
- MCP server advertises its version from `CARGO_PKG_VERSION`; keep it in step with the workspace version.
