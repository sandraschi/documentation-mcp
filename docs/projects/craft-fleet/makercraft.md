# MakerCraft — Assessment

**Repo:** `D:\Dev\repos\makercraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first digital-fabrication bench + instrument studio: 3D printing (Klipper),
CNC milling (GRBL), hardware protocol debugging (Bus Pirate bridge). Port `14130`.
New bench for the `klipper-mcp`/`cnc-mcp`/hardware concepts.

## Model / verbs

- **Model:** fabrication job (model → toolpath → machine) + instrument capture.
- **Crates:** `makercraft-hal`, `makercraft-core`, `makercraft-mcp`, `makercraft-app`.
- HAL-first mirrors robotcraft (machines behind traits, correct seam).

## Architecture

Rust ArtCraft 3-tier, MIT/Apache. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-04 (fleet i18n).

## Strengths

- HAL seam again correct (printers/mills/probes behind traits; sim-first testable).
- Benchcraft-adjacent (instruments) without duplicating it — fabrication vs
  measurement is a defensible split if written down.
- Physical-making story completes the fleet (bits → atoms).

## Gaps / risks

- Hardware-present CI problem (no Klipper/GRBL on Goliath CI): sim-first is
  mandatory, mock-green is the failure mode to avoid.
- Machine-safety (heaters, spindles, motion limits) needs confirm-gates like
  robotcraft's tele-op gates — nothing at triage evidences them.
- Serial/USB device enumeration on Windows (the classic fleet paper cut) unaddressed.
- No `docs/`, no toolpath-fixture tests (model → G-code artifact is the hello world).

## Next 3 steps

1. `docs/PRD.md`: HAL traits + sim-first policy + safety/confirm gates + benchcraft boundary.
2. Toolpath fixture tests (fixture model → G-code artifact, no machine).
3. One democraft recipe: `maker/toolpath-sim` (all `sim` receipts, no hardware).

## Verdict

Right bench, right seam, same homework as robotcraft: safety gates + sim-first
proofs. C+ until a fixture model becomes G-code without touching hardware.
