# SportsCraft — Assessment

**Repo:** `D:\Dev\repos\sportscraft` · **Date:** 2026-11-05 · **Grade: B+**

## What it is

Local pure-Rust biomechanics + training-load studio: Banister fitness/fatigue/form
(CTL/ATL/TSB), race pacing prediction (800 m–100 km), IMU gait kinematics.
No account, no cloud, no port.

## Model / verbs

- **Model:** athlete (TRIMP series → CTL/ATL/TSB) + gait session (IMU fixture).
- **MCP (stdio, 4 tools):** `status`, `athlete.profile`, `athlete.predict`, `gait.analyze`.
- Demo honesty: gait output says `source: "demo"` — no sensor/importer attached yet.

## Architecture

Rust workspace (core/kinematics/mcp/app), clippy denies, `justfile`, `AGENTS.md`,
`CHANGELOG.md`, `docs/` (2) + `reports/` + `installer/` (NSIS posture),
`LICENSE-APACHE/MIT`. eframe/egui studio (Banister panel, gait panel, pacing
simulator, theme + locale EN/DE/FR/ES/JA/KO/ZH). Assfix-touched 2026-11-05
(timestamp-at-landing fix).

## Strengths

- `source: "demo"` labeling is the fleet honesty pattern applied to biometrics.
- Banister math + pacing window (+5…+18 TSB) + gait stiffness/asymmetry = real
  sports-science depth, not dashboard chrome.
- Installer/ + reports/ show ship thinking beyond the binary.

## Gaps / risks

- No importer: TRIMP/gait data entry path is the missing half (manual? file? Strava-alt?).
- wearables/IMU mapping unvalidated (no sensor comparison study, even informal).
- Medical-adjacent overreach risk: pacing guidance needs a not-medical-advice line.
- Test evidence thin at triage; Banister fixtures (known TRIMP → known CTL/ATL) are
  the obvious golden tests.

## Next 3 steps

1. Golden Banister fixtures (3 series → exact CTL/ATL/TSB assertions).
2. Importer decision (CSV first) + `source` labeling extended to every input.
3. One democraft recipe: `sports/banister-sim` (fixture TRIMP → prediction report).

## Verdict

B+: honest demo labeling, real models, ship posture. Importers + golden fixtures
are the A- path.
