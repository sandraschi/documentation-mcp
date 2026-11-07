# MusicCraft — Assessment

**Repo:** `D:\Dev\repos\musiccraft` · **Date:** 2026-11-05 · **Grade: reserved (no grade yet)**

## What it is

Name reservation with an initial plan — no implementation. The studio umbrella
over the fleet's scattered music work: DAW arrangement, vocal synthesis (the
virtual opera singer), stems and mix. `djcraft` stays the permanent live-decks
sibling (stage vs studio, never merged).

## Model / verbs (planned, per `docs/PRD.md`)

- **Model:** song project `{ tracks[], vocalLine?, arrangement, stems, mix }`.
- **Verbs (draft):** `project new|open|info`, `track add|list`, `stem split`,
  `vocal synth`, `mix render`, `export stems|song`, `mcp`.

## Architecture

TBD — tech triage open (likely Rust ArtCraft 3-tier in the `djcraft`/
`speechcraft` shape; Python FastMCP pilot acceptable). `.gitignore` covers both.

## Sources it consolidates

`reaper-mcp` (arrangement), `stems-mcp` (separation), `songgeneration-mcp`
(generation knowledge), `kyutai-mcp` (vocal-synth pathfinding). `djcraft` is
explicitly a sibling, not a source.

## Next 3 steps

1. Freeze scope (PRD §5: audio latency, vocal-model licensing, local-vs-cloud split).
2. Pilot verbs (`project`, `track`, `export`) + `just ci` + fixtures.
3. Vocal-synth path + first democraft recipe (`music/stems-sim`).

## Verdict

A claimed name with an honest plan and a permanent boundary against `djcraft`.
Unranked until Phase 1 lands — which is exactly what the README says.
