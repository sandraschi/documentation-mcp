# Craft Fleet — Documentation Hub

**Last updated:** 2026-11-05
**Owner:** Sandra S. + fleet agents
**Scope:** 26 craft repos under `D:\Dev\repos\*craft` — the local-first studio layer (23 assessed + `musiccraft` reserved + `smallvideocraft` planned 2026-11-05; `robotcraft` consolidation credited incl. `rust-saschirob-mcp`).
**Sources:** live `D:\Dev\repos` listing 2026-11-05, `projects/craft-fleet-rebuild/PLAN.md`
(10-pilot plan), `projects/craft-fleet-expansion/MASTER_CRAFT_EXPANSION_PLAN.md`
(15-suite matrix, ports 14112–14131).

This hub is the **section index**. Each spoke is one assessment file in this
directory (`<name>.md`). Spokes are point-in-time triage notes, not marketing —
read the spoke, then the repo's own `README.md` / `HANDOVER.md` / `docs/`.

## How to read this hub

- **New here?** Read this file, then the spoke for the craft you care about.
- **Picking a pilot?** Start with grades A / B (proven verbs), not grade C scaffolds.
- **Adding a craft?** Copy the spoke template (§ Template) and follow the
  rebuild PLAN's fit test: single model, headless verbs, files in/out, 3 obvious recipes.
- **Rule reminders:** max 10 files per commit; 3+ file edits need timestamped `.bak`
  first; never invent a date — hub date above was read from the environment clock.

## Architecture tiers (normative)

| Tier | Stack | Applies to |
|---|---|---|
| Pure-Rust ArtCraft 3-tier (L1 `-core`, L2 `-mcp`/CLI, L3 `-app`) | Rust, `deny(clippy::unwrap_used)`, no ports, stdio MCP | bookcraft, databasecraft, qgiscraft, sportscraft, gamecraft, travel/money/dj/mod/writer/coder/robot/app/speech/maker |
| Python FastMCP craft workstation | Python, `cli.py` + `mcp_server.py`, stdio | containercraft, gitcraft, filecraft, doccraft, revecraft, virtucraft, splatcraft |
| Upstream reference | Storytold ArtCraft monorepo | artcraft (not fleet-owned) |

Fit test (from rebuild PLAN §1.2): single model? headless verbs? files in/out?
3 recipes obvious? Server-shaped repos (Plex, Immich, email, discord, observers,
voice bus, CUDA) stay bridges — they are **not** crafts.

## Status matrix

| Spoke | Repo | Lang | Crates / modules | Docs in repo | Tests | Last commit | Grade |
|---|---|---|---|---|---|---|---|
| [artcraft](artcraft.md) | `D:\Dev\repos\artcraft` | Rust (upstream Storytold) | 14+ crates, native egui app | `docs/` (3+) | upstream CI + Sonar | 2026-10-23 | A (reference, not owned) |
| [gamecraft](gamecraft.md) | `D:\Dev\repos\gamecraft` | Rust workspace v0.13.0 | 10 crates + cli + desktop | `docs/` (14) | `tests/` (3 files) | 2026-11-04 | A- |
| [bookcraft](bookcraft.md) | `D:\Dev\repos\bookcraft` | Rust ArtCraft 3-tier v0.3.0 | core/mcp/app | `docs/` (4: PRD, TOOLS, UI_PARITY, PARITY) | 34 tests | 2026-11 (HANDOVER) | A |
| [qgiscraft](qgiscraft.md) | `D:\Dev\repos\qgiscraft` | Rust, clippy-deny | 5 crates + xtask | `docs/` (**25 files**) | — | 2026-11-04 | A- |
| [databasecraft](databasecraft.md) | `D:\Dev\repos\databasecraft` | Rust, clippy-deny-all | core/store/mcp/app | `docs/` (4) | — | 2026-11-04 | B+ |
| [sportscraft](sportscraft.md) | `D:\Dev\repos\sportscraft` | Rust, clippy-deny | core/kinematics/mcp/app | `docs/` (2) + `reports/` + `installer/` | — | 2026-11-05 (assfix) | B+ |
| [splatcraft](splatcraft.md) | `D:\Dev\repos\splatcraft` | Python FastMCP | 9 modules (cloud/train/engines/recipes/…) | — | 10 test files | 2026-11-04 | B- |
| [speechcraft](speechcraft.md) | `D:\Dev\repos\speechcraft` | Rust ArtCraft (:14132) | dsp/core/mcp/app | — | — | 2026-11-05 | C+ |
| [travelcraft](travelcraft.md) | `D:\Dev\repos\travelcraft` | Rust ArtCraft | baedeker/core/mcp/app | — | — | 2026-11-04 | C+ |
| [moneycraft](moneycraft.md) | `D:\Dev\repos\moneycraft` | Rust ArtCraft (:14117) | core/feed/mcp/app + PRD/SPEC/HELP | — | — | 2026-11-04 | C+ |
| [djcraft](djcraft.md) | `D:\Dev\repos\djcraft` | Rust ArtCraft | audio/core/mcp/app | — | — | 2026-11-04 | C+ |
| [modcraft](modcraft.md) | `D:\Dev\repos\modcraft` | Rust ArtCraft (:14120) | geometry/core/mcp/app | — | — | 2026-11-04 | C+ |
| [writercraft](writercraft.md) | `D:\Dev\repos\writercraft` | Rust ArtCraft (:14121) | narrative/core/mcp/app | — | — | 2026-11-04 | C+ |
| [codercraft](codercraft.md) | `D:\Dev\repos\codercraft` | Rust ArtCraft (:14128) | core/agent/mcp/app + PRD/SPEC | — | — | 2026-11-04 | C+ |
| [robotcraft](robotcraft.md) | `D:\Dev\repos\robotcraft` | Rust ArtCraft (:14116) | core/hal/mcp/app + `web/` | — | — | 2026-11-04 | C+ |
| [appcraft](appcraft.md) | `D:\Dev\repos\appcraft` | Rust ArtCraft (:14115) | core/templates/mcp/app | — | — | 2026-11-04 | C+ |
| [makercraft](makercraft.md) | `D:\Dev\repos\makercraft` | Rust ArtCraft (:14130) | hal/core/mcp/app | — | — | 2026-11-04 | C+ |
| [containercraft](containercraft.md) | `D:\Dev\repos\containercraft` | Python FastMCP | `cli.py` + `mcp_server.py` | — | 2 test files | 2026-11-05 | C |
| [gitcraft](gitcraft.md) | `D:\Dev\repos\gitcraft` | Python FastMCP | `cli.py` + `mcp_server.py` | — | 2 test files | 2026-11-04 | C |
| [filecraft](filecraft.md) | `D:\Dev\repos\filecraft` | Python FastMCP | `cli.py` + `mcp_server.py` | — | 2 test files | 2026-11-04 | C |
| [doccraft](doccraft.md) | `D:\Dev\repos\doccraft` | Python FastMCP | `cli.py` + `mcp_server.py` | — | 2 test files | 2026-11-04 | C |
| [revecraft](revecraft.md) | `D:\Dev\repos\revecraft` | Python FastMCP | `cli.py` + `mcp_server.py` | — | 2 test files | 2026-11-04 | C |
| [virtucraft](virtucraft.md) | `D:\Dev\repos\virtucraft` | Python FastMCP | `cli/hypervisor/models/sandbox/mcp_server` | — | 2 test files | 2026-11-04 | C |
| [musiccraft](musiccraft.md) | `D:\Dev\repos\musiccraft` | Reserved (no code yet) | README + `docs/PRD.md` only | — | — | 2026-11-05 | Reserved |
| [smallvideocraft](smallvideocraft.md) | `D:\Dev\repos\smallvideocraft` | Planned, flagship runs as `ittybittyvideos` | README + `docs/PRD.md` only | — | — | 2026-11-05 | Planned |

Grades: **A** = proven + documented + tested · **B** = working with gaps ·
**C** = day-1 scaffold, verbs declared but depth unverified. Plus/minus = docs/tests momentum.

Related (out of scope for spokes, present in tree): `lookcraft`, `on-metacraft`
exist in `D:\Dev\repos` but were not in the requested 23 — no spoke yet.

## What the matrix says

1. **Two generations.** The A/B tier (game/book/db/qgis/sports/splat) grew over
   weeks with docs, tests, assfix passes. The C/C+ tier (11 Rust Antigravity
   scaffolds + 6 Python workstations) all landed 2026-11-04/05 in one wave —
   uniform 4-crate shape, fleet i18n (EN/DE/FR/ES/JA/KO/ZH), `KIBITZ.md`, but no
   `docs/` and no test evidence yet.
2. **Best patterns to copy:** bookcraft (6-gate ArtCraft bar, backup-before-write,
   `docs/PARITY.md` honesty) and qgiscraft (WRAPPEE/ECOSYSTEM docs, `--smoke` BMP
   preview, keyless-first). Worst pattern to copy: shipping 11 repos with zero
   `docs/` between them.
3. **Naming collisions to resolve:** `databasecraft/` dir vs `dbcraft` binary name;
   `revecraft` vs rebuild-PLAN spelling; `virtucraft` vs `VirtuCraft` capitalisation.
   Decide per spoke; do not keep two names long-term.
4. **Democraft wiring is the gate.** Per rebuild PLAN §7, a craft without
   3 green democraft recipes (`run.json` + report) is not a craft yet. Only
   bookcraft and gamecraft can point at recipes today.

## Spoke template (for new assessments)

```markdown
# <Name>Craft — Assessment
**Repo:** `D:\Dev\repos\<name>` · **Date:** 2026-11-05 · **Grade:** X
## What it is / Model / Verbs / Sources it consolidates
## Architecture (tier, crates/modules, ports)
## Strengths / Gaps / Risks
## Next 3 steps (smallest verifiable)
## Verdict (one paragraph)
```

## Public release (2026-11-05)

All 22 fleet crafts are public on GitHub under `sandraschi/`, each marked
`[ALPHA]` in its description with topics `alpha`, `artcraft-pattern`,
`mcp-server`, `rust`/`python`. Wording (corrected 2026-11-05): each description
says the repo *implements the Storytold craft-app harness* and points at
`storytold/artcraft` — ArtCraft itself ("the IDE for artists") was the starting
point, and the 16-app Storytold stable's modus operandi + harness is what we
follow. Every craft README carries a `Lineage` section saying exactly that, with
the link. (`artcraft` itself is Storytold upstream — untouched, no sandraschi fork.)

- **Already public before this:** travelcraft, databasecraft.
- **Flipped private → public (11):** qgiscraft, robotcraft, gamecraft,
  containercraft, gitcraft, filecraft, doccraft, revecraft, virtucraft,
  speechcraft, splatcraft. Hygiene pre-scan: zero secrets/bad files committed
  anywhere. qgiscraft's pending i18n commit and gamecraft's agent-branch commit
  were pushed first so public matches local.
- **Created + pushed (9):** moneycraft, djcraft, modcraft, writercraft,
  codercraft, appcraft, sportscraft, makercraft (existing history),
  bookcraft (genesis import, 28 curated files — contaminated worktree dirs
  `_archives/`, `4g-usb-phone-mcp/`, `FreeCAD/`, `.trash/` deliberately excluded).
- **Known gaps on public repos (not hidden, to be closed by the C+→B plan):**
  dj/mod/writer/app carry uncommitted launcher + `.gitignore` (KIBITZ) tweaks;
  makercraft carries uncommitted source work (its public state trails local);
  splatcraft carries two `.bak` launcher backups (untracked, ignored).
  C/C+ grades and the retrofit plan are public in this hub — the alpha label is honest.
