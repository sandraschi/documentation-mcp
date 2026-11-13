# MakerCraft — Assessment

**Repo:** `D:\Dev\repos\makercraft` · **Date:** 2026-11-09 · **Grade: B+** · **Origin:** fleet-owned

## What it is

Local-first digital-fabrication bench and hardware instrument studio in pure Rust (port `14130`, `3,570 LOC`, `37 tests`, 4 crates, 15 MCP tools): 3D printing (Klipper/Moonraker), CNC milling (GRBL with full alarm/error oracle and machine-safety envelope), USBTMC oscilloscope capture (Rigol/Siglent SCPI), and `sigrok-cli` logic analyzer protocol decoding.

## Model / verbs

- **Model:** fabrication job (G-code toolpath + bounding-box/feedrate safety check + GRBL/Klipper state) + bench instrument capture (USBTMC waveform / `sigrok` logic trace).
- **15 MCP tools / CLI verbs:**
  - Fabrication & CNC: G-code parser/validator, bounding-box & feedrate safety envelope check, GRBL status/alarm/error code oracle, Klipper/Moonraker print status, emergency stop (`confirm` gated).
  - Bench instruments: USBTMC oscilloscope SCPI query/waveform capture (`scope_*`), `sigrok-cli` logic analyzer protocol decode (`logic_*`), serial port enumeration, and hardware `doctor`.

## Architecture

4-crate Pure-Rust ArtCraft 3-tier workspace (`makercraft-hal`, `makercraft-core`, `makercraft-mcp`, `makercraft-app`), `3,570 LOC`, `37 tests`, `clippy -D warnings` clean.

## Strengths

- Massive leap from Nov-5 (`C+` with 0 tests) to `3,570 LOC` and `37` passing tests (`Grade B+`).
- Real hardware-safety engineering: G-code toolpaths are checked against machine travel/feed/spindle limits before execution, and the built-in GRBL oracle translates cryptic numeric GRBL alarm/error codes into actionable diagnostics.
- Combines fabrication (Klipper/GRBL) and bench measurement (USBTMC scope + `sigrok` logic analyzer) behind clean HAL traits with deterministic simulation fixtures when hardware is unplugged.

## Gaps / risks

- Live USBTMC and serial hardware tests require physical instruments attached to Goliath; `doctor` and HAL traits cleanly report `sim` vs `hardware` sources.

## Next 3 steps

1. Wire 3 `democraft` recipes (`maker/gcode-safety-audit`, `maker/grbl-oracle`, `maker/sigrok-decode-sim`).
2. Add Gerber / drill-file viewer tab in `makercraft-app` for PCB inspection.
3. Document the HAL trait contract in `docs/PRD.md`.

## Verdict

Grade B+: 3,570 LOC, 37 passing tests, 15 MCP tools, USBTMC + sigrok instrument integration, and G-code safety envelopes make `makercraft` the fleet's flagship hardware bench.
