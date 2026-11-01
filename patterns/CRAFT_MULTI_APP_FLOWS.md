---
title: "Craft multi-app flows: the twelve readymade chains and the flow runner"
category: pattern
status: review
audience: mcp-dev, all-agents
last_updated: 2026-10-20
---

# Craft multi-app flows

A **flow** is a named, ordered list of demo steps across Craft apps. The runner
executes them sequentially, copies each step's artifacts into a per-run bundle,
and records what happened. Flows are data (JSON), not code, so the webapp can
create, edit and delete them.

The point is not the individual demo. It is the chain: grade in PhotoCraft, lay
out in DesignCraft, assemble in PdfCraft, with each app on its own control port
and the whole run kept as one bundle.

## The twelve flows

Ports are the registered control channels (14100-14112); a step runs headless by
default and can be watched live when its app is attached.

| # | Flow | Steps (app:demo) | Ports | Status |
|---|---|---|---|---|
| 1 | Cover factory | photo:plate-grade -> design:print-spread -> pdf:portfolio | 14109 -> 14102 -> 14108 | ready |
| 2 | Photo book | photo:batch-treatment -> design:print-spread -> pdf:portfolio | 14109 -> 14102 -> 14108 | ready |
| 3 | Data deck | grid:homepage-grid -> deck:pitch-deck -> pdf:portfolio | 14106 -> 14101 -> 14108 | ready |
| 4 | CAD board | cad:house-plan -> design:print-spread -> pdf:portfolio | 14100 -> 14102 -> 14108 | ready |
| 5 | Poster lab | vector:pelican-vector -> photo:plate-grade -> design:print-spread | 14111 -> 14109 -> 14102 | ready |
| 6 | Data report | grid:homepage-grid -> word:demo-report -> pdf:portfolio | 14106 -> 14112 -> 14108 | ready |
| 7 | Brand kit | vector:pelican-vector -> design:print-spread -> deck:transition-reel | 14111 -> 14102 -> 14101 | exploratory |
| 8 | Storyboard | fig:landing-page -> design:print-spread -> film:storyboard | 14104 -> 14102 -> 14105 | ready |
| 9 | Lyric sheet | word:demo-report -> design:print-spread -> pdf:portfolio | 14112 -> 14102 -> 14108 | ready |
| 10 | Audiobook art | photo:plate-grade -> vector:pelican-vector -> pdf:portfolio | 14109 -> 14111 -> 14108 | ready |
| 11 | Title sequence | design:print-spread -> effect:title-card -> film:timeline-cut | 14102 -> 14103 -> 14105 | exploratory (cut builds its own footage) |
| 12 | Score-driven cut | sound:ident-jingle -> film:timeline-cut | 14110 -> 14105 | exploratory (own footage; SoundCraft VST3i, BUG-082) |

The seed catalog lives in `src/democraft_mcp/flows.py` (`SEED_FLOWS`); the webapp
shows it at `/flows` and hints at more as the suite grows.

## Flow schema

```json
{
  "id": "cover-factory",
  "name": "Cover factory",
  "description": "Grade a plate, lay it into a print spread, export a portfolio PDF.",
  "status": "ready",
  "blocked_reason": "",
  "steps": [
    { "app": "photo", "demo": "plate-grade", "note": "non-destructive grade" },
    { "app": "design", "demo": "print-spread", "note": "facing pages" },
    { "app": "pdf", "demo": "portfolio", "note": "assemble" }
  ]
}
```

- `id`: 2-49 chars, lowercase letters, digits, hyphens. Immutable on edit.
- `status`: `ready` | `exploratory` | `blocked`. Blocked flows refuse to run.
- Steps must name an installed app key and one of its real demo ids; the store
  validates both at write time.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/flows` | list (seeded + user flows) |
| POST | `/api/flows` | create |
| GET | `/api/flows/{id}` | one flow |
| PUT | `/api/flows/{id}` | update (id is taken from the path) |
| DELETE | `/api/flows/{id}` | delete |
| POST | `/api/flows/{id}/run` | start a sequential run |
| GET | `/api/flows/runs/{run_id}` | poll status, steps, artifacts |
| GET | `/api/flow-artifacts/{path}` | serve a bundled artifact |

## Runner semantics

1. Steps run **sequentially**; a failed step stops the flow and the run is
   marked `failed`.
2. Each step calls the existing `run_demo` (no new execution path).
3. Artifacts are copied into `outbox/_flows/<run_id>/<NN>-<app>-<demo>/`, so the
   flow has one bundle even though the demos write into their own directories.
4. `run_id` is `YYYYMMDD-HHMMSS-<6 hex>`; status is in memory, artifacts are on
   disk.
5. A blocked flow is refused with the recorded reason; nothing starts.

## Live variant

Every step can be watched instead of batch-run: start the apps on their
registered ports and attach the MCP servers (`--attach` Fig, `--bridge` Photo,
`--connect` Design/Grid/Sound). See
[`standards/rust-artcraft/CRAFT_COMMAND_BUS.md`](../standards/rust-artcraft/CRAFT_COMMAND_BUS.md).

```powershell
# batch chain (no windows)
# the runner does the equivalent of:
photocraft-cli run plate.jpg --cmd image.adjustments.blackWhite --params '{"reds":45}' --out plate.pcraft
designcraft-cli run --cmd 'file.place={"path":"plate.png"}' --export spread.pdf
pdfcraft-cli run --cmd 'pdf.merge={"inputs":["spread.pdf"],"output":"deliverable.pdf"}'

# live chain (windows visible)
figcraft --control 14104
designcraft --control 14102
deckcraft --control 14101
# then attach one MCP server per port in the client
```

Command ids above are illustrative; the v1 runner executes **demos**, not
arbitrary command lines. Command-level steps and true artifact piping are the
next iteration, and they are why the flow schema keeps `topic` and `note`.

## v1 limits (stated, not hidden)

- **Steps are demos, not commands.** A step cannot yet say "take the previous
  step's PNG and place it"; the handoff is by convention and the bundle keeps
  both artifacts.
- **No conditional branches, no parallel steps, no retries.** Sequential only.
- **Runs are in memory.** Restarting the backend loses run status; bundles stay
  in `outbox/_flows/`.
- **FilmCraft has a timeline and a `timeline-cut` demo.** It imports demo
  footage, builds a 24 fps sequence, applies a 12-frame cross dissolve and
  exports H.264. The two film chains remain exploratory because the cut builds
  its own footage instead of ingesting the previous step's artifact, and because
  SoundCraft VST3 instruments are silent (BUG-082).

## Adding a flow

- **UI:** `/flows` -> New flow -> name/id/status -> add steps (app, demo, note,
  up/down/remove) -> Save. Edit and Delete are on the same page.
- **API:** POST the JSON above; validation rejects unknown apps, unknown demos,
  duplicate ids and empty step lists.

## Community apps are not flows

The flow table above covers the `storytold/*` suite. A **community app** is made outside
ArtCraft and admitted to the catalog as `AppKind::Community`. It is not a flow step, it does
not appear above, and adding one is not an agent task.

Admission rules, from `craft-launcher/AGENTS.md` (read 2026-10-29):

- Downloads come from `github.com/storytold/<app>/releases`, or from an approved community
  app's **own** repo. Today only one: `tangency-labs/solidcraft/releases` (SolidCraft,
  approved by the project owner on 2026-10-28, AGENTS.md lines 61-64).
- The repo is pinned in the catalog (`CraftApp::repo`). A release feed may move an app within
  `storytold/`; it may never move it to another owner.
- Every download is checked against the release's `SHA256SUMS.txt`, community apps included.
  macOS additionally requires a Developer ID signature, so an unsigned app is not installed
  there and is only opened if already present (SolidCraft, `installs_on_mac = false`).
- **"Agents never land or approve a third-party app"** (line 78). An agent reviewing such a PR
  reports who owns the repo, its age and history, and whether builds are signed - then stops:
  no merge, no approval, no commits pushed to the PR.

State as measured on 2026-10-29:

| App | Repo | Status |
|---|---|---|
| SolidCraft | `tangency-labs/solidcraft` | approved 2026-10-28, in catalog, shipped |
| NoteCraft | `AlienTechSoftware/notecraft` | launcher PR #979 open, explicitly blocked on owner approval |
| AniCraft | `storytold/AniCraft` | empty repo, no commits, no default branch; not in catalog |

**The launcher is distribution, not a runtime dependency.** A craft app runs from its own
installer or portable archive with the launcher closed or absent; integration adds install
detection and update, nothing else. So "not merged" never means "not usable" - it means the
user updates it by hand.

See also
[`research/2026-10-29-fusion-360-and-solidcraft-parity.md`](../research/2026-10-29-fusion-360-and-solidcraft-parity.md)
for what SolidCraft is and how it compares to `freecad-mcp`.

## Related

- [`standards/rust-artcraft/CRAFT_COMMAND_BUS.md`](../standards/rust-artcraft/CRAFT_COMMAND_BUS.md) - headless/live planes, attach flags, ports, config shapes.
- [`projects/adobe-offensive/22-soundcraft-status.md`](../projects/adobe-offensive/22-soundcraft-status.md) - why two flows are blocked.
- `democraft-mcp/docs/PLAN.md` - Phase 3 (flow runner) sits on the job engine.
- [`research/2026-10-29-fusion-360-and-solidcraft-parity.md`](../research/2026-10-29-fusion-360-and-solidcraft-parity.md) - **SolidCraft** is the launcher's first community app (`tangency-labs/solidcraft`, not `storytold`), so it is not in the flow table above. That doc covers what it clones (Fusion, not SolidWorks), its MCP surface, and why it is a peer to `freecad-mcp` rather than a replacement.


