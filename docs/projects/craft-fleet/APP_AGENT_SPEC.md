# AppCraft Building Robot — Resident Agent Loop (spec draft 0, 2026-11-05)

**Status:** draft for review, no code. This is the component that turns
AppCraft from a workbench (tools without a carpenter) into the building
robot the name promises.

## 0. Lineage (why not dark-app-factory again)

Dark-app-factory got one thing right and one thing wrong. Right: a resident
loop that ingests a request, researches, builds, tests, and supervises —
without it, every build needs a human holding the tools (which is how Bohr's
app got built: an external agent did the loop by hand). Wrong: hierarchy.
Foreman/worker agents with conversational state are uninspectable, unpausable,
and die with their process. AppCraft already owns the correction: the
stigmergic ledger (emit → claim → complete as data, not chat). The robot
specified here is a dark-app-factory foreman rewritten as a stigmergic
worker: same loop, no boss, all state in artifacts.

## 1. Goal

A goal sentence in → a verified, generated app out, with zero human keystrokes
between gates. Example acceptance goal: *"dental practice app for Bohr:
patients, appointments, treatment plans, LAN portal, local-only"* must
reproduce today's `bohr-ordination` to functional equivalence (same tables,
same verbs, same smoke results — byte-identity not required, behavior is).

## 2. Non-goals (explicit)

- No autonomous publishing. Nothing leaves the machine (no `git push`, no
  deploy, no store submission) without an explicit human yes per artifact.
- No cloud-by-default inference. Local first (Ollama via the
  `craft-ai-core` pattern, same as codercraft-agent); cloud keys only when
  the owner configures them, and never for patient data without counsel.
- No legal clearance, ever. The loop *runs* the legal dev-spike (§8 of the
  democraft fortification plan) and *lists* gaps; clearance stays human.
- No replacement for democraft recipes. Recipes verify; the robot builds.
  `app/scaffold-smoke` stays the independent check, not the robot's self-grade.

## 3. Architecture: one new crate, zero new servers

New crate `appcraft-agent` beside core/templates/mcp/app. It drives the
*existing* dispatch bus — no parallel tool surface, no private APIs:

```
goal (text) → INTAKE (spec artifact) → SPIKE (unknowns w/ verdicts)
→ PLAN (ordered dispatch calls) → EMIT (InitApp + out_dir)
→ BUILD (CompileArtifact, real cargo) → TEST (golden + smoke recipe)
→ VERIFY (run.json + report) → human gates between each arrow that mutates
```

Each phase reads and writes files only (`goal.md`, `spec.md`,
`spikes/*.md`, `runbook.json`, `run.json`, `report.md`). Kill the process
mid-run and resume from the artifacts — the stigmergic contract from the
democraft plan applies verbatim. Multi-actor by construction: the robot
claims ledger tasks; a human or a second agent sees the same board and can
take, block, or annotate any of them.

## 4. The brain: local-first inference with a budget

- Default: local Ollama model via the codercraft `craft-ai-core` client
  shape (already proven in-fleet; copy the pattern, not the code blindly).
- Fallback: user-supplied cloud key (Claude / Google / OpenAI) for steps
  the local model fails twice — recorded in the run log which brain did
  which step, so cost and data-exposure are auditable per run.
- Budget caps, non-negotiable: max iterations per phase (default 5),
  max cloud spend per goal (default: zero — cloud is opt-IN), max wall
  time (default 30 min). Caps live in config, not in prompts.
- No patient/customer seed data to cloud models, ever — enforced by
  redacting the data layer from cloud-bound prompts (schemas and row
  *counts* may travel; cell values may not).

## 5. Human gates (the robot stops, the human decides)

- After INTAKE if the goal is ambiguous (the robot asks; it does not guess
  the business).
- After SPIKE if any unknown verdict is `BLOCKED` (missing data, license,
  hardware, or legal input).
- Before EMIT if the blueprint is new or modified (schema changes are
  migrations, not drafts).
- Legal dev-spike is MANDATORY before any app whose tables hold personal
  data — the loop refuses to proceed past PLAN without a GAPS-LISTED
  artifact, and refuses to ever write COMPLIANT itself.
- Publish/deploy is always a human action. The robot prepares; it never ships.

## 6. Interfaces (one bus, three drivers — now four)

- **CLI:** `appcraft agent --goal "..." [--blueprint X] [--dry-run]`
  (dry-run prints the runbook and stops — the default first run for any
  new goal shape).
- **MCP:** `agent_run` tool (same parameters; returns run_id immediately,
  progress via the run's `run.json` — polling, not streaming).
- **GUI:** a "Build from goal" panel showing the phase board (each phase:
  pending/running/blocked/done + its artifact link). Same dispatch calls
  the CLI makes; the GUI never gets a private path.
- **Outer agents** (opencode sessions, fleet-agent, democraft `plan`) keep
  working exactly as today — the resident loop is a fourth driver, not a
  replacement. Bohr's app was built driver #4-absent; the acceptance test
  is rebuilding it driver #4-present with no human keystrokes but gates.

## 7. Relationship to neighbors (no turf wars)

- **democraft `plan`/`chain`:** transverse (multi-craft runbooks). The robot
  is single-app (one blueprint, one emission). A democraft plan may *call*
  the robot as one step; the robot never calls democraft.
- **dark-app-factory intake:** the questionnaire/spec flow is the missing
  INTAKE — mine it (day-plan Phase 4) as the robot's first phase, stigmergic
  spec artifact out, foreman nowhere.
- **democraft recipes:** stay the independent verification layer. The robot
  passes `app/scaffold-smoke`; it does not grade itself.

## 8. Open questions (for the humans, not the robot)

1. Default iteration/token budgets — 5 steps and zero-cloud are guesses.
2. Where run artifacts live (`madeapps/<app>/runs/<ts>/` vs a central runs dir).
3. Whether the GUI panel ships in v1 or the robot is CLI/MCP-only first
   (recommendation: CLI/MCP first — GUI panel after the first three
   successful builds, so the panel displays a proven history).
4. Voice ingress (`fleet-agent` intents as goals) — explicitly later.

## 9. Acceptance (definition of done, no adjectives)

1. Goal sentence for `bohr-ordination` → robot run with zero human keystrokes
   except gate answers → output builds (`cargo check` clean), db schema
   identical (6 tables + indexes), demo recipe green.
2. Legal dev-spike artifact produced and listed as a gate (not as clearance).
3. Every LLM call logged with model, tokens, cost (zero for local).
4. Kill mid-run twice; resume from artifacts both times with no lost work.
5. `just ci` green on `appcraft-agent` itself; golden tests unaffected.
