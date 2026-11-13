# SportsCraft — Assessment

**Repo:** `D:\Dev\repos\sportscraft` · **Date:** 2026-11-09 · **Grade: B+** · **Origin:** fleet-owned

## What it is

Local pure-Rust biomechanics, endurance training-load, personal trainer, and spectator cup-run studio (`v0.2.0`, `3,887 LOC`, `30 tests`, 4 crates):
1. **Endurance & Biomechanics Core:** Banister impulse-response model (CTL fitness / ATL fatigue / TSB form), Riegel/Vdot race pacing predictor (800 m–100 km), IMU gait kinematics (ground contact time, vertical oscillation, leg spring stiffness, bilateral asymmetry).
2. **Personal Trainer (`v0.2.0`):** Structured workout library, adaptive coaching prescriptions based on TSB form, and training streak tracking.
3. **Spectator Mode (`v0.2.0`):** Offline historic Cup-Run Browser for exploring classic tournament brackets, match timelines, and momentum swings.

## Model / verbs

- **Model:** athlete profile (TRIMP series → CTL/ATL/TSB + workouts + streaks) + IMU gait session + spectator tournament bracket.
- **Crates (`3,887 LOC`, `30 tests`):**
  - `sportscraft-core`: Banister impulse-response math, race predictor, personal trainer coaching engine, workout log, and spectator cup-run dataset.
  - `sportscraft-kinematics`: IMU gait cycle segmentation, spring-mass stiffness, and asymmetry analysis.
  - `sportscraft-mcp`: stdio MCP server exposing athlete profile/prediction, gait analysis, trainer coaching, and cup-run inspection.
  - `sportscraft-app`: native `eframe`/`egui` studio with Banister chart, gait analyzer, Personal Trainer tab, Spectator Cup-Run Browser, and 7-locale i18n.

## Architecture

4-crate Pure-Rust ArtCraft workspace (`3,887 LOC`, `30 tests`, `clippy -D warnings` clean), `docs/`, `reports/`, `installer/`, `CHANGELOG.md`.

## Strengths

- Shipped `v0.2.0` (2026-11-07), expanding to `3,887 LOC` and `30` passing golden tests across Banister math, kinematics, personal trainer prescriptions, and spectator brackets.
- Preserves strict `source: "demo"` vs user-logged provenance labeling on all biometric data.

## Gaps / risks

- FIT / GPX / TCX file import from Garmin/Strava exports is the natural next step so users can ingest multi-year watch logs directly into the Banister model.

## Next 3 steps

1. Add GPX/TCX/CSV workout log importer into `sportscraft-core`.
2. Wire 3 `democraft` recipes (`sports/banister-golden`, `sports/gait-asymmetry`, `sports/trainer-prescription`).
3. Keep non-medical-advice disclaimer visible in Personal Trainer exports.

## Verdict

Grade B+: 3,887 LOC, 30 passing tests, honest biometric provenance, and the `v0.2.0` Personal Trainer + Spectator Cup-Run Browser additions make `sportscraft` a well-tested B+ studio.
