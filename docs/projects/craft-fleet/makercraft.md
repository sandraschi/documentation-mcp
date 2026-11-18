# MakerCraft — Assessment

**Repo:** `D:\Dev\repos\makercraft` · **Date:** 2026-11-13 · **Grade: B+** · **Origin:** fleet-owned

Correction 13 November 2026. `instrument.capture` writes a labelled demo file for seven bench sources. The catalog is 17 tools. The meter, function generator, spectrum analyzer, and JTAG adapter are files only. Scope, logic, and Bus Pirate keep their existing live commands. The grade above is the 9 November assessment.

Recount 13 November 2026, same method as the old 3,570: physical lines in the nine `.rs` files, comments and blanks included. That count is 3,796. tokei, which skips comments and blanks, reports 3,399 Rust code lines. `cargo test --workspace --offline` passed 38 tests: 15 in `makercraft-core`, 16 in `makercraft-hal`, 7 in `makercraft-mcp`. Doc-tests: 0.

## What it is

Local-first digital-fabrication bench and hardware instrument studio in pure Rust (3,796 physical lines in nine `.rs` files, 38 passing tests, 4 crates, 17 MCP tools over stdio): 3D printing (Klipper/Moonraker), CNC milling (GRBL with full alarm/error oracle and machine-safety envelope), USBTMC oscilloscope capture (Rigol/Siglent SCPI), and `sigrok-cli` logic analyzer protocol decoding. The window paints `14130` as a label.

## Model / verbs

- **Model:** fabrication job (G-code toolpath + bounding-box/feedrate safety check + GRBL/Klipper state) + bench instrument capture (USBTMC waveform / `sigrok` logic trace).
- **17 MCP tools / CLI verbs on `makercraft-mcp`:**
  - Fabrication & CNC: G-code parser/validator, bounding-box & feedrate safety envelope check, GRBL status/alarm/error code oracle, Klipper/Moonraker print status, emergency stop (`confirm` gated).
  - Bench instruments: USBTMC oscilloscope SCPI query/waveform capture (`scope_*`), `sigrok-cli` logic analyzer protocol decode (`logic_*`), serial port enumeration, and hardware `doctor`.
  - Capture: `instrument.sources` and `instrument.capture`. The capture file is labelled demo.

## Architecture

4-crate Pure-Rust ArtCraft 3-tier workspace (`makercraft-hal`, `makercraft-core`, `makercraft-mcp`, `makercraft-app`). Recounted 13 November 2026: 3,796 physical Rust lines, 3,399 tokei code lines, 38 passing tests.

## Strengths

- Massive leap from Nov-5 (`C+` with 0 tests) to `3,570 LOC` and `37` passing tests (`Grade B+`).
- Real hardware-safety engineering: G-code toolpaths are checked against machine travel/feed/spindle limits before execution, and the built-in GRBL oracle translates cryptic numeric GRBL alarm/error codes into actionable diagnostics.
- Combines fabrication (Klipper/GRBL) and bench measurement (USBTMC scope + `sigrok` logic analyzer) behind clean HAL traits with deterministic simulation fixtures when hardware is unplugged.

## Gaps / risks

- Live USBTMC and serial hardware tests require physical instruments attached to Goliath; `doctor` and HAL traits cleanly report `sim` vs `hardware` sources.

## Next 3 steps

1. Put a live reading into the capture file for the multimeter, function generator, spectrum analyzer, or JTAG adapter. The file stays a demo until that reading exists. Do not drive an output or flash a chip.
2. Wire 3 `democraft` recipes (`maker/gcode-safety-audit`, `maker/grbl-oracle`, `maker/sigrok-decode-sim`).
3. Add Gerber / drill-file viewer tab in `makercraft-app` for PCB inspection.

## Verdict

Grade B+ stands from 9 November. The 13 November recount is 3,796 physical Rust lines and 38 passing tests. USBTMC and sigrok integration and the G-code safety envelopes are unchanged. The catalog is 17 tools. The four capture-only instruments are still files.
