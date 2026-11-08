# C+ → B Retrofit Plan: pulling the ten scaffold-generation crafts up to grade

**Date:** 2026-11-05 · **Scope:** the ten C+ spokes in this hub —
travelcraft, moneycraft, djcraft, modcraft, writercraft, codercraft,
robotcraft, appcraft, speechcraft, makercraft.
**Goal:** every one of them earns a B (working, documented, tested, one green
recipe) without rewriting what Antigravity already stamped out.
**Non-goal:** A-grade (full recipe suites, parity docs, installer polish) — that
comes later, per craft, on its own schedule.

## Why C+ and what B means

The October surprise (16 Storytold CLIs + ArtCraft harness + standards wave) produced
11 uniform Rust workspaces in ~48 hours: 4 crates, fleet i18n, `KIBITZ.md`,
`start.ps1`/`start.bat` — but no `docs/`, no tests, no `justfile`, no recipes.
The ideas are sound (moneycraft's 1720/1850 deep-archive + panic annotations is
the standout), the debt is all scaffolding. B means:

- [ ] `docs/PRD.md` — model, verbs, scope cut, neighbor boundaries
- [ ] `docs/TOOLS.md` — verb/tool surface inventory
- [ ] `just ci` green — `cargo fmt --check` + `clippy -D warnings` + `cargo test`
      (workspace denies: `unwrap_used`, `expect_used`, at minimum)
- [ ] ≥3 headless fixture tests (no hardware, no network, no mic in CI)
- [ ] 1 green democraft recipe (`run.json` + report artifact, `sim`/`down` receipts where live)
- [ ] Domain safety paragraph enforced in code or tests (the per-craft sharp edge)

That is the whole bar. Nothing in it requires inventing new architecture.

## Per-craft sharp edges (the safety paragraph each owes)

| Craft | Sharp edge | Proof required |
|---|---|---|
| moneycraft | live-money / financial advice | paper-only default + credential redaction test |
| robotcraft | physical actuators | confirm-gates + sim-only CI test |
| makercraft | heaters / spindles / motion | confirm-gates + sim-first toolpath test |
| speechcraft | mic capture / voice-bus drift | bus contract pin + fixture-WAV test (no mic in CI) |
| djcraft | real-time DSP claims | headless mix on fixtures with measured ms |
| modcraft | kernel build-vs-wrap | decision doc + primitive-volume tests |
| writercraft | trope-data licensing | source/licence note + scene-graph fixture test |
| codercraft | scope (IDE+server+UX) | scope-cut PRD + deterministic edit-roundtrip test |
| travelcraft | guide-data licensing + qgiscraft overlap | boundary paragraph + pack-fixture test |
| appcraft | generated-code trust | output contract + golden-tree diff test |

## Phases

### Phase 0 — Fleet template (one session, benefits all ten)

1. Write the canonical `docs/PRD.md` + `docs/TOOLS.md` skeletons once (copy from
   bookcraft's — it is the exemplar) into a hub template.
2. Write the canonical `justfile` (`fmt-check`, `check`, `test`, `ci`) once.
3. Decide the workspace-lint floor once: `unwrap_used` + `expect_used` deny at
   workspace level (bookcraft's five-denies is the stretch goal, not the floor).
4. Record the `databasecraft` vs `dbcraft`-style naming answers already made so no
   craft re-litigates them.

### Phase 1 — Docs wave (10 crafts × ~30 min, mechanical)

Per craft: `docs/PRD.md` (model, verbs, scope cut, two boundary paragraphs:
which neighbor owns what) + `docs/TOOLS.md` (verb inventory). Source material is
the spoke assessment + the repo README — no new thinking, just write-down.
Boundary pairs that must appear: travel↔qgis, writer↔bookcraft↔doccraft,
mod↔SolidCraft, dj↔Effect/SoundCraft apps, robot↔benchcraft, app↔dark-app-factory,
speech↔voice-bus, money↔DatabaseCraft ledgers, coder↔opencode (difference in writing).

### Phase 2 — Gates wave (10 crafts × ~1 h, mostly mechanical)

Per craft: add `justfile`, workspace lint denies, `cargo fmt`, fix what clippy
finds (scaffold code is usually clean — the risk is `unwrap` in generated code).
`just ci` must run end-to-end. Do NOT fix architecture; fix lints.

### Phase 3 — Tests wave (10 crafts × ~2 h, the real work)

≥3 headless fixture tests per craft, no hardware/network/mic:

- travel: guide-pack fixture → artifact · money: known series → known backtest numbers
  (no-lookahead assertion) · dj: fixture mix → artifact + ms · mod: primitive volumes +
  boolean union · writer: scene graph → corkboard artifact · coder: fixture edit →
  byte-identical artifact · robot: FK/IK on fixture URDF · app: blueprint → golden tree
  diff · speech: fixture WAV → transcript artifact · maker: fixture model → G-code.

### Phase 4 — Recipes wave (10 crafts × ~1 h, wiring)

One democraft recipe each (fixture-only default; live paths token-gated, `sim`/`down`
receipts, never in default `just ci`): `travel/guide-pack`, `money/backtest-sim`,
`dj/transition-sim`, `mod/primitive-bom`, `writer/scene-pack`, `coder/edit-roundtrip`,
`robot/fk-sim`, `app/scaffold-smoke`, `speech/transcribe-sim`, `maker/toolpath-sim`.
Register in `crafts.py` + `recipes.py`; gallery tile optional (B does not require it).

### Phase 5 — Re-grade (one session)

Re-run each spoke's checks, update grades B (or B+/A- where earned), record remaining
gaps honestly. Crafts that miss get a dated note, not a silent pass.

## Ordering

Phase 0 → then per craft in dependency order: moneycraft first (sharpest domain risk,
best existing specs — fastest win), then robot/maker/speech (safety gates),
then the rest in any order, appcraft last (its golden test depends on the
DatabaseCraft output contract, which is Phase-0-adjacent work).

Effort: ~5 h per craft end-to-end, but Phases 1–2 are mechanical enough to batch
(respect the 10-files-per-commit rule; never batch across repos in one commit).

## Verification (no fake greens)

- `just ci` output pasted or linked per craft — a gate that reports success having
  examined nothing is a failure, not a pass.
- Every recipe writes `run.json` + report with measured numbers (ms, bytes, rows).
- Missing hardware/network/token = `sim`/`down` receipt, never a skipped assertion
  dressed as green.
- Re-grade updates the spoke file in this hub with the date and the evidence.
