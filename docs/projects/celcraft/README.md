# CelCraft - fleet project entry

**Status:** Active. v1.6.0, Tier 8.1-8.5, weight-free cutout (8.10), ISNet ONNX (8.11), ToonOut on DirectML, and Dx12 over-blend plus parallax (8.6). Bokeh, snapshots, docking, scrub, and SAM (the rest of 8.12) are still required for full parity.
**Type:** Pure-Rust ArtCraft 3-tier workspace (desktop app + CLI + MCP stdio). **No ports, no webapp.**
**Repo:** `D:\Dev\repos\celcraft`
**Authoritative status:** the repo `README.md` "Status: what is real, what is a shell" table and the repo `HANDOVER.md`. This page summarises; it does not override them.

---

## What it is

A clean-room, native Rust (`forbid(unsafe_code)`) digital ink-and-paint and classical animation workstation aimed at the traditional scanned-cel and paperless frame-by-frame workflow that OpenToonz / Toonz Harlequin served. Three crates tiers: headless engine (`cel-*` L1), CLI + MCP driver (`cel-mcp` L2), and an `egui` workstation (`cel-ui` L3).

## Current state (v1.6.0)

| Area | State |
|---|---|
| Engine: raster, fill, autogap, Sauvola, peg warp, normal maps, optical flow, LPC lip-sync, `.tlv`/`.tnz`, multiplane math | Real, unit-tested, zero unsafe |
| CLI (`--json`) + MCP stdio, 42 tools | Real |
| `.celcraft` project save/open, ink strokes, undo/redo | Real |
| Animation export: PNG frames + MP4/GIF (`render-animation`) | Real |
| Desktop UI: menus dispatch, Stage renders engine frames, timeline, Pen paint, save/open | Real |
| Bundled fixtures + anime plates: `assets/fixtures/sample.tnz` + `sample.tlv` import through the engine; three fal.ai reference plates (Ghibli meadow, Neo-Tokyo alley, OVA cockpit) under `assets/reference/` ($0.60, key in OS keychain, never in repo) | Real |
| CPAL playback, waveform cache, BLAKE3 CAS, ProRes streaming, EXR write command plus a stderr-drain fix (1.5.1), working clipboard, Copy/Paste scope, palette dispatch, Ctrl+N/S/E/0 shortcuts, detailed Help | Real (Tier 7 + 1.5.1/1.5.2) |
| Weight-free figure mask, SkyTNT ISNet, and BiRefNet ToonOut from the user cache | Real (Tier 8.10, 8.11, and the ToonOut half of 8.12). DirectML on the machine that checked it. SAM is still 8.12 |
| Plate/cel over-blend and multiplane parallax on Dx12, matching the CPU pixels. Bokeh stays on the CPU | Started (Tier 8.6). RTX 4090 / Dx12 on the machine that checked it |
| `egui_kittest` snapshots, panel docking, audio scrub | Planned Tier 8.7-8.9 |

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

Build artifacts: `target\release\cel-mcp.exe`, `target\release\cel-ui.exe`, `target\celcraft-v1.5.2-setup.exe`.

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
