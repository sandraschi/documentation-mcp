---
title: "Agentic Install Standard"
category: standard
status: draft
audience: mcp-dev
last_updated: 2026-10-30
related:
  - standards/ONE_CLICK_INSTALL_UX_STANDARD.md
  - standards/AGENT_INSTALL_REFERENCE.md
  - standards/PACKAGING_STANDARDS.md
  - standards/NAKED_PC_INSTALL_STANDARD.md
  - standards/ONBOARDING_STANDARD.md
# status: draft -- written 2026-10-30 from the rust-saschirob-mcp pilot,
# pivoted same-day: the classical install doc is dead, minimal core only.
# Moves to active once a second repo adopts the core and section 6 passes.
---

# Agentic Install Standard (`install <repo>`)

**One-line rule:** repos ship machine-readable facts, one tested single-step path,
and a proof step. The agent does the rest from evidence. Hand-written multi-option
install procedures are dead inventory — do not write new ones, do not maintain old ones.

## 1. The new approach (paradigm shift, obvious in hindsight)

The classical install doc — clone the repo, run this Python stuff (`uv sync`,
`pip install`, env vars, port forwards, tribal flags), hope for the best, paste the
traceback back when it breaks — is dead. It died the day a SOTA agent read a
stale-since-2025 repo with hand-install-only instructions and just installed it anyway
from the tree.

What that changes: the install doc was written for a reader who cannot read code. On
the agentic path, that reader no longer exists. What remains:

- **The agent** (hands: shell + filesystem + network) derives everything from repo
  evidence — manifests, entry points, lockfiles, health checks, existing scripts. It
  needs facts and a way to verify, not procedures.
- **The human without an agent, and Desktop chat without hands,** still need exactly
  one path that works with zero understanding. That path is maintained. It is the only
  prose procedure the repo owes.
- **Distribution** — versioned, hashed, attributable artifacts (mcpb, NSIS, release
  notes). "An agent built it from source once" is not a release.

Consequence for maintainers: stop curating install essays. Every hour spent maintaining
three install methods per repo is an hour not spent on machine-readable installability
(correct manifests, pinned deps, working entry points, health endpoints) — the surface
agents actually consume.

## 2. What the repo owes (minimal core)

1. **Facts, machine-readable.** Correct package manifests with real entry points,
   lockfiles, a health/status signal, and (for servers) the exact launch command and
   args. If the agent cannot derive the install from the tree, fix the tree, not the docs.
2. **Exactly one tested single-step path.** The zero-understanding route (double-click
   `.mcpb`, run `install.ps1`, one `start.bat`) — tested, working, maintained. Serves
   Steve, Desktop-no-hands, and the demo.
3. **A proof step.** One command with expected output (health endpoint, `tools/list`
   probe, smoke gate). The agent reports success only when the proof passes.
4. **A trigger line.** README quickstart, quoted, ~8 lines max: `` `install <repo>` ``
   plus the repo path of the agent doc plus the proof expectation. A pointer, never the
   procedure.

## 3. What the repo does NOT owe anymore

- Multi-option install procedures (Options A–D style walkthroughs written for agents).
  One path; the agent derives the rest.
- Pasted command outputs, pinned hashes, or per-client config essays in prose. Facts
  live in manifests and scripts; the agent adapts them.
- Troubleshooting novels. Keep symptom → one-line fix; the agent investigates from logs.

Existing docs in this style are not deleted on sight — but they are not maintained
either. Touch one only to replace it with the section 2 core.

## 4. Routing rules (these survive)

- **Capability-check-first.** The agent plan (`docs/AI_SETUP.md`, kept in the ONE_CLICK
  section 6 shape) opens by classifying the installer: no hands → the single-step path,
  executed by the human; hands → derive from evidence using the repo's facts.
- **Desktop-no-hands.** Claude Desktop chat without a filesystem MCP cannot download,
  build, or register anything. Say so in the plan; route to the single-step path. Never
  let a handless agent believe it installed something.

## 5. Plans rot; agents read anyway

A SOTA agent with hands installs even a stale, hand-install-only repo by reading the
tree — that is the magic, not a violation. Write the remaining plan content to age
gracefully (paths over pasted outputs, invariants over transients) and forbid only the
dangerous moves (elevation, exfiltration beyond `127.0.0.1`, source edits as fixes).
Never forbid the fallback to repo evidence.

## 6. Acceptance (moves this standard to active)

1. Second repo (different class than the pilot) adopts the section 2 core —
   candidate: `gamecraft` (Rust workspace + Godot depot, no install docs at all;
   the perfect test of "agent reads the tree").
2. A fresh agentic session given only the trigger line installs by following the agent
   doc plus repo evidence — and a handless session routes to single-step instead of
   pretending.
3. Assfix checklist gains: agent doc present, proof step present, no second full
   procedure hiding in README.

## 7. Class table (same contract, different facts)

The section 2 core does not change per class. What changes is what the facts,
the one path, and the proof concretely are:

| Repo class | Facts live in | One tested path | Proof |
|---|---|---|---|
| Python MCP hand, `start.bat` track | `pyproject.toml`, `uv.lock`, `start.ps1` flags | `start.bat` | health endpoint / smoke |
| Rust workspace + start scripts (`gamecraft`, `lookcraft`, `rust-devices-mcp`, `rust-yahboom-mcp`, ...) | workspace `Cargo.toml`, `justfile` recipes | `start.bat` (= `cargo run`) or `cargo build --release` | `just test` / `tools/list` probe / class smoke |
| Rust CLI-first, no start scripts (`rust-saschirob-mcp`) | `Cargo.toml`, `mcpb/manifest.json`, `installer/installer.nsi` | `.mcpb` double-click / `install.ps1` | `tools/list` probe |
| Game/art depot (`gamecraft`) | above, plus Godot version + `depot/` manifest | `start.bat` (viewer) | `smoke-godot` / `depot-godot` / `verify-depot` — needs the Godot binary |

Rust-class gotchas worth one line in the agent doc, not an essay: the toolchain comes
from rustup (`winget install Rustlang.Rustup`), `~\.cargo\bin` is routinely missing from
inherited PATH (fleet `justfile`s prefix it on every recipe — agents must do the same
in every shell), and external verifiers (Godot binary) are detected-not-bundled: proof
degrades to build + unit gates when absent, and says so.

## 7. Changelog

| Date | Change |
|---|---|
| 2026-10-30 | Draft from rust-saschirob-mcp pilot (trigger-as-pointer, capability-first, proof mandatory). |
| 2026-10-30 | Correction: plans rot, strong agents read anyway. |
| 2026-10-30 | **Pivot: the classical clone-and-hope install doc is dead.** Slimmed to minimal core (facts + one path + proof); multi-option procedures declared dead inventory. |
| 2026-10-30 | Class table: same contract for Python/Rust/game-depot classes; Rust PATH + Godot-detected-not-bundled gotchas; `gamecraft` named as acceptance pilot #2. |
