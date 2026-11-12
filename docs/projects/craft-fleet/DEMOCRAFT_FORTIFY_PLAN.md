# Democraft Fortification Plan — the transverse layer without a new repo

**Date:** 2026-11-05 · **Status:** plan, not started · **Owner question:** when
does this outgrow democraft and earn the name `metacraft` (§6 gate).

## 0. What democraft already is (measured 2026-11-05, not assumed)

- **Registry** (`crafts.py`): exe path, verb surface, HERO, family — Storytold
  apps (cad/deck/design/effect/grid/material/solid/vector/pdf/…) and fleet
  crafts in one table.
- **Recipes** (`recipes.py`, ~60+): per-craft demo functions emitting `run.json`
  + markdown report. Storytold side (house-plan, pitch-deck, title-card,
  macro-replay, …) and fleet side already live: `virt_*`, `rev_*`, `doc_*`,
  `file_*`, `git_*`, `container_*`, `book_*` (incl. `readly_ingest_sim`),
  `money_ledger_reconcile`, `database_*`, `splat_*`.
- **Compat probing** (`compat.py`): `probe_version`, `verbs_of`, `recorded`
  state, `check(cli_path)` — version/verb drift detection already exists.
- **Flows** (`flows.py`): `validate_flow` — runbook validation exists.
- **Server ops**: `run_demo`, `ai_flow`, `craft_commands`, gallery webapp.

Verdict: democraft is already halfway to supervisor on the **verify /
demonstrate** axis. Missing entirely on the **plan / chain / optimize** axis,
and it has demos where it needs spikes (§2).

## 1. Gap analysis (what "fortify" means)

| # | Gap | Why it matters |
|---|---|---|
| 1 | No cross-craft chaining | Real workflows transverse crafts (travel→qgis, writer→book, music→dj, script→short). Nothing executes A→B today. |
| 2 | No planning verb | `run_demo` runs one demo; nothing turns a goal into a multi-craft runbook. |
| 3 | Demos, not spikes | Demos show success paths. Nothing probes the one unknown that kills (no-lookahead, FK/IK correctness, DOWN behavior). |
| 4 | No compare/optimize | Same task two ways, measured pick — the optimizer half of "supervisor, planner, optimizer". |
| 5 | Compat drift is advisory | `compat.py` records; nothing fails CI fleet-wide when verbs drift. |
| 6 | No fleet scoreboard | Gallery shows crafts; nothing shows per-craft recipe health red/green in one view. |

## 2. Spike doctrine

A **spike** is a narrow, sharp, time-boxed probe that resolves exactly one
unknown with a verdict — the agile spike solution, revived for agent
planning. A demo says "look what it can do"; a spike says "here is the one
thing that could kill us, and here is the measured answer."

Spike format (mandatory): fixture in → artifact + measurements out → verdict
`PASS` / `FAIL` / `DOWN` (dependency absent, with receipt — never a fake
green). Time-boxed. One unknown each. Headless, no network/mic/hardware
unless the unknown IS the hardware.

Two flavors, two homes. **Probe-spikes** live in democraft (the verify axis):
measured, headless, fixture-driven, verdict PASS/FAIL/DOWN — including the
robustness flavor (spike-load bursts, corrupt fixtures, absent engines).
**Dev-spikes** live in AppCraft's generation pipeline: time-boxed
investigations that resolve a build-blocker BEFORE code is generated — legal
unknowns, hardware unknowns, licensing unknowns, data-source unknowns. The
Bohr legal-compliance spike (§8) is the reference dev-spike. Both share the
shape (one unknown, time-boxed, artifact verdict); they differ in home and in
what "verdict" may claim — a dev-spike on legal questions lists gaps but
never issues clearance (see §8).

Spike catalog v1 (each maps to one C+→B sharp edge or one transverse seam):

- `spike/money-nolookahead` — known series → backtest numbers must match; any
  lookahead fails the spike, not the suite.
- `spike/robot-fk-sim` — fixture URDF → end-effector within tolerance.
- `spike/mod-primitive-volume` — cube/sphere/cylinder → exact volumes; one
  boolean union.
- `spike/travel-qgis-handoff` (transverse) — travelcraft place output must
  ingest as a qgiscraft layer unchanged. The seam, tested.
- `spike/writer-book-handoff` (transverse) — corkboard export must open as a
  bookcraft ingest. The boundary, tested.
- `spike/music-dj-handoff` (transverse) — rendered stems must load in djcraft
  decks. Studio→stage, tested.
- `spike/shorts-script-sim` — fixture script → timed scene list, no render.
- `spike/speech-fixture-wav` — fixture WAV → transcript artifact, no mic.
- `spike/down-receipts` (robustness) — every engine-gated recipe (capa,
  frida, daemons, GPU train) with the engine absent must emit `DOWN`, exit 0.
- `spike/corrupt-fixture` (robustness) — truncated DB / malformed spec →
  clean error, never a traceback-as-output.

## 3. New verbs (transverse, stigmergic)

All verbs pass artifacts, never conversational state. `run.json` + report is
the protocol; democraft never holds hidden memory between steps.

- **`plan` (dry-run first)** — goal in → runbook out: ordered craft verbs,
  fixture I/O contract between steps, unknowns flagged as spikes. Never
  executes; the runbook is itself an artifact for review.
- **`chain`** — runbook in → chained execution across crafts, each step's
  artifact becoming the next step's fixture. Failures stop the chain with
  the failing artifact attached (stigmergy: the next agent reads the
  artifact, not a chat log).
- **`compare`** — same task, N craft paths, measured pick by stated metric
  (ms, bytes, rows). The optimizer, deterministic edition.
- **`sweep`** — fleet-wide recipe run with per-craft receipts; the bench.
- **`spike`** — run one catalog spike, return the verdict.

## 4. Stigmergic contract (the anti-meta-mcp)

meta-mcp failed as an obscure supervisor nobody invoked. The defense is
structural, not motivational:

1. **No hidden state.** Every verb reads/writes files (`run.json`, reports,
   fixtures). A supervisor that can be `Ctrl+C`'d mid-run and resumed from
   disk needs no babysitting and earns no obscurity.
2. **Grow where users are.** `plan`/`chain`/`compare` live in democraft
   (gallery traffic exists) — not in a new repo with zero users.
3. **Compat as gate, not advice.** `compat.py` baselines (`recorded`) become
   CI-failing: unrecorded verb drift breaks the build with the diff attached.
4. **Scoreboard, not dashboard-chrome.** One gallery view: per-craft recipe
   health red/green with last-verdict timestamps. Boring, load-bearing.

## 5. Phases

- **0 (recon, done):** inventory above. No code written.
- **1 — spikes first (1 session):** implement the 10 catalog spikes as recipe
  functions. Spikes before chains: you cannot chain crafts whose unknowns
  are unresolved. Gate: all 10 verdict `PASS` or honest `DOWN`.
- **2 — `plan` verb (1 session):** goal→runbook over the existing registry,
  dry-run only, 3 hand-written transverse runbooks as golden tests
  (travel→qgis, writer→book, music→dj).
- **3 — `chain` verb (1–2 sessions):** execute runbooks stigmergically;
  failure attaches the artifact. Gate: the 3 golden runbooks green end to end.
- **4 — `compare` + `sweep` (1 session):** deterministic optimizer + nightly
  sweep wiring (fleet-ci or scheduled task; receipts, never pages).
- **5 — compat-as-gate + scoreboard (1 session):** recorded baselines fail CI
  on drift; gallery health view. Then re-grade: transverse layer done.

## 6. Metacraft decision gate (when the name is earned)

`metacraft` is ontologically strong — which is why it stays parked until ALL
of these are true:

1. Autonomous replanning: `chain` fails mid-runbook and the layer itself
   produces the recovery runbook (not a human, not a fresh prompt).
2. Real optimizer: `compare` with a search budget (not N=2 hand-picked).
3. Cross-craft transactions: multi-step mutations with rollback semantics
   (bookcraft's backup-before-write, generalized).

Until then: no repo, no supervisor service. If the name needs squatting
protection meanwhile, reserve it empty with one honest README line — cheap,
reversible, and not a meta-mcp resurrection.

## 7. What NOT to do (meta-mcp scar tissue)

- No chatty orchestrator service holding session state.
- No autonomous fleet-wide mutation without confirm-gates (gitcraft rule applies).
- No second gallery, no second registry — extend `crafts.py`/`recipes.py`.
- No LLM-judged pass/fail in CI. Verdicts are measured (ms, bytes, rows,
  exit codes) or they are theater.

## 8. Reference dev-spike: legal compliance (Bohr case, 2026-11-05)

The first dev-spike AppCraft's pipeline ever ran. Shape for all future
legal-unknown spikes.

- **Input:** the app repo + a data-flow description (what personal data, whose,
  where stored, where transmitted, who operates the machine it runs on).
- **Method:** inventory → matrix. Rows: GDPR Art. 5 principles, Art. 6 basis,
  Art. 9 health-data conditions, Austrian DSG, medical confidentiality
  (ÄrzteG Verschwiegenheitspflicht), processor contracts
  (Auftragsverarbeiter), TOMs, residency/transfers (Schrems II), retention +
  deletion, patient rights (Auskunft/loss), access logging. Each cell:
  evidenced / gap / unknown-needs-owner.
- **Verdict vocabulary:** `GAPS LISTED` (with owner per gap) or
  `BLOCKED` (cannot assess — needs X). Mechanical sub-checks may PASS
  ("binary makes no network calls", evidenced). The overall stamp is NEVER
  `COMPLIANT` from an agent — clearance is a human counsel's signature.
  An LLM issuing legal clearance is malpractice-adjacent theater, and this
  plan forbids it the same way it forbids fake greens.
- **Why our stack helps:** local-first is the mitigator-in-chief — patient
  data that never leaves the ordination PC has no transfer problem, no
  processor chain, and a one-line residency story. The spike's job is to
  verify that story per app (no telemetry, no cloud fallback without consent
  and contract), not to assume it.
