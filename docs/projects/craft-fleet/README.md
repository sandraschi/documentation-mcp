# Craft Fleet — Documentation Hub

**Last updated:** 2026-11-10
**Owner:** Sandra S. + fleet agents
**Scope:** 29 active Pure-Rust craft/infrastructure repos under `D:\Dev\repos\*craft*` — the local-first studio layer (23 Pure-Rust craft studios incl. `wincraft`, `splatcraft`, `vmcraft`, `giscraft`, plus 12-app Sovereign Back-Office suite; 4 shared Rust infrastructure repos `craft-ai`, `democraft`, `benchcraft`, `lookcraft`; `artcraft` upstream reference; `musiccraft` + `smallvideocraft` PRD specs). All 6 Nov-4 Python craft scaffolds (`revecraft`, `filecraft`, `doccraft`, `gitcraft`, `containercraft`, `virtucraft`) are retired/superseded.
**Sources:** live `D:\Dev\repos` audit 2026-11-09, `projects/craft-fleet-rebuild/PLAN.md`, `projects/craft-fleet-expansion/MASTER_CRAFT_EXPANSION_PLAN.md`.

This hub is the **section index**. Each spoke is one assessment file in this
directory (`<name>.md`). Spokes are point-in-time triage notes, not marketing —
read the spoke, then the repo's own `README.md` / `HANDOVER.md` / `docs/`.
**Do not duplicate this matrix elsewhere** — `projects/FLEET_INDEX.md` is stale
(see its banner) and `operations/fleet-status.md` carries only PR/issue/dirty
deltas plus a one-section craft delta pointer (no second matrix).

## Architecture tiers (normative)

| Tier | Stack | Applies to |
|---|---|---|
| Pure-Rust ArtCraft 3-tier (L1 `-core`, L2 `-mcp`/CLI, L3 `-app`) | Rust, `deny(clippy::unwrap_used)`, stdio MCP (+ optional web track) | gamecraft, bookcraft, giscraft, splatcraft, moneycraft, wincraft, vmcraft, databasecraft, sportscraft, makercraft, travelcraft, studiocraft, codercraft, speechcraft, robotcraft, appcraft, djcraft, modcraft, writercraft |
| Shared Rust infrastructure | Rust library / harness workspaces | craft-ai (`craft-ai-core`), democraft, benchcraft, lookcraft |
| Upstream reference | Storytold ArtCraft monorepo | artcraft (not fleet-owned) |

Fit test (from rebuild PLAN §1.2): single model? headless verbs? files in/out?
3 recipes obvious? Server-shaped or multi-engine Python/JVM orchestrators
(`reversing-mcp`, Plex, Immich, email, discord, observers) stay bridges — they
are **not** rewritten as Rust crafts.

## Active Craft Status Matrix (measured 2026-11-09)

| Spoke | Repo | Origin | Lang | Crates / modules | Rust LOC | Tests | Last commit | Grade |
|---|---|---|---|---|---|---|---|---|
| [artcraft](artcraft.md) | `D:\Dev\repos\_upstream\artcraft` | storytold-ref | Rust (upstream Storytold) | 15 crates, native egui app | 62,158 | 510 | 2026-10-23 | A (reference) |
| [gamecraft](gamecraft.md) | `D:\Dev\repos\gamecraft` | fleet-owned | Rust workspace v0.14.0 | 12 crates (core/commands/godot/mcp/forge/sim/gltf/bevy/replay/trellis + cli + desktop) | 37,735 | 258 | 2026-11-09 | A |
| [bookcraft](bookcraft.md) | `D:\Dev\repos\bookcraft` | fleet-owned | Rust ArtCraft 3-tier v0.5.0 | 3 crates (core/mcp/app), 30 MCP tools | 7,170 | 46 | 2026-11-09 | A |
| [giscraft](qgiscraft.md) | `D:\Dev\repos\giscraft` | fleet-owned | Rust v0.2.1 (renamed from `qgiscraft`) | 5 crates (core/store/mcp/app/web) + xtask | 13,460 | 142 | 2026-11-08 | A- |
| [splatcraft](splatcraft.md) | `D:\Dev\repos\splatcraft` | fleet-owned | Rust workspace v0.1.0 (rewritten from Python) | 9 crates (core/io/ply/cloud/mcp/gui/cli/train/craft-secrets) | 8,530 | 116 | 2026-11-08 | A- |
| [moneycraft](moneycraft.md) | `D:\Dev\repos\moneycraft` | fleet-owned | Rust workspace v0.7.0 (:14117) | 5 crates (core/feed/broker/mcp/app), 17 MCP tools | 9,341 | 11 | 2026-11-09 | A- |
| [wincraft](wincraft.md) | `D:\Dev\repos\wincraft` | fleet-owned | Rust ArtCraft 3-tier v0.1.0 | 3 crates (core/mcp/app), 26 MCP tools, native Win32 Restart Manager + RAM Weeder + FileOps + NSSM + Cards/List/JSON/Export | 3,150+ | 12 | 2026-11-09 | A- |
| [databasecraft](databasecraft.md) | `D:\Dev\repos\databasecraft` | fleet-owned | Rust ArtCraft 3-tier | 4 crates (core/store/mcp/app) | 4,768 | 29 | 2026-11-06 | B+ |
| [sportscraft](sportscraft.md) | `D:\Dev\repos\sportscraft` | fleet-owned | Rust ArtCraft v0.2.0 | 4 crates (core/kinematics/mcp/app) | 3,887 | 30 | 2026-11-07 | B+ |
| [makercraft](makercraft.md) | `D:\Dev\repos\makercraft` | fleet-owned | Rust ArtCraft (:14130) | 4 crates (hal/core/mcp/app), 15 MCP tools | 3,570 | 37 | 2026-11-07 | B+ |
| [vmcraft](vmcraft.md) | `D:\Dev\repos\vmcraft` | fleet-owned | Rust ArtCraft v0.2.0 (supersedes `virtucraft`) | 3 crates (core/mcp/app), 19 MCP tools | 2,821 | 25 | 2026-11-08 | B+ |
| [travelcraft](travelcraft.md) | `D:\Dev\repos\travelcraft` | fleet-owned | Rust ArtCraft v0.2.0 | 4 crates (baedeker/core/mcp/app), 13 MCP tools | 6,771 | 27 | 2026-11-08 | B+ |
| [studiocraft](studiocraft.md) | `D:\Dev\repos\studiocraft` | fleet-owned | Rust ArtCraft v0.2.0 | 3 crates (core/mcp/app), 12 MCP tools, 6 skills | 2,812 | 12 | 2026-11-07 | B |
| [codercraft](codercraft.md) | `D:\Dev\repos\codercraft` | fleet-owned | Rust ArtCraft (:14128) | 4 crates (core/agent/mcp/app) + `craft-ai-core` | 2,616 | 14 | 2026-11-09 | B |
| [speechcraft](speechcraft.md) | `D:\Dev\repos\speechcraft` | fleet-owned | Rust ArtCraft (:14132) | 4 crates (dsp/core/mcp/app) | 1,929 | 20 | 2026-11-09 | B- |
| [robotcraft](robotcraft.md) | `D:\Dev\repos\robotcraft` | fleet-owned | Rust ArtCraft (:14116) | 4 crates (core/hal/mcp/app) + `web/` | 1,680 | 5 | 2026-11-07 | C+ |
| [appcraft](appcraft.md) | `D:\Dev\repos\appcraft` | fleet-owned | Rust ArtCraft (:14115) | 4 crates (core/templates/mcp/app) | 1,247 | 4 | 2026-11-07 | C+ |
| [djcraft](djcraft.md) | `D:\Dev\repos\djcraft` | fleet-owned | Rust ArtCraft | 4 crates (audio/core/mcp/app) | 883 | 3 | 2026-11-07 | C |
| [modcraft](modcraft.md) | `D:\Dev\repos\modcraft` | fleet-owned | Rust ArtCraft (:14120) | 4 crates (geometry/core/mcp/app) | 651 | 2 | 2026-11-07 | C |
| [writercraft](writercraft.md) | `D:\Dev\repos\writercraft` | fleet-owned | Rust ArtCraft (:14121) | 4 crates (narrative/core/mcp/app) | 645 | 1 | 2026-11-07 | C |
| [rsicraft](rsicraft.md) | `D:\Dev\repos\rsicraft` | fleet-owned | Rust ArtCraft 3-tier v0.1.0 | 3 crates (core/mcp/app), GPU RSI optimizer + egui studio | 3,850+ | 16 | 2026-11-09 | A- |
| [buchcraft](buchcraft.md) | `D:\Dev\repos\buchcraft` | fleet-owned | Rust ArtCraft v0.2.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Austrian double-entry bookkeeping | 4,200+ | 28 | 2026-11-09 | A- |
| [taskcraft](taskcraft.md) | `D:\Dev\repos\taskcraft` | fleet-owned | Rust ArtCraft v0.1.2 (craft-biz suite) | 4 crates (store/core/mcp/app), Jira/Linear issue tracker & native Kanban board | 3,350+ | 18 | 2026-11-10 | A- |
| [teamcraft](teamcraft.md) | `D:\Dev\repos\teamcraft` | fleet-owned | Rust ArtCraft v0.1.1 (craft-biz suite) | 4 crates (store/core/mcp/app), Austrian AZG time & leave tracking & native timesheet workstation | 3,250+ | 23 | 2026-11-10 | A- |
| [assetcraft](assetcraft.md) | `D:\Dev\repos\assetcraft` | fleet-owned | Rust ArtCraft v0.1.1 (craft-biz suite) | 4 crates (store/core/mcp/app), Fixed assets with Austrian AfA/GWG & native inventory workstation | 3,200+ | 22 | 2026-11-10 | A- |
| [contractcraft](contractcraft.md) | `D:\Dev\repos\contractcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Contract lifecycle & Kündigungsfristen & native pipeline | 3,300+ | 23 | 2026-11-10 | A- |
| [gaincraft](gaincraft.md) | `D:\Dev\repos\gaincraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Account health & CTAs (Gainsight-equiv) & native Customer 360 | 3,100+ | 22 | 2026-11-10 | A- |
| [deskcraft](deskcraft.md) | `D:\Dev\repos\deskcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Support tickets from .eml/Maildir (Zendesk-equiv) & native inbox | 3,100+ | 20 | 2026-11-10 | A- |
| [formcraft](formcraft.md) | `D:\Dev\repos\formcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Surveys, NPS scorecards, detractor routing (:11258/:11259) | 2,750+ | 3 | 2026-11-10 | A- |
| [wikicraft](wikicraft.md) | `D:\Dev\repos\wikicraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Markdown wiki, FTS5 search, ADR state machine (:11260/:11261) | 3,100+ | 4 | 2026-11-10 | A- |
| [billcraft](billcraft.md) | `D:\Dev\repos\billcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Austrian ebInterface 6.1 & SEPA pain.008 direct debit & native GUI | 3,250+ | 1 | 2026-11-10 | A- |
| [spendcraft](spendcraft.md) | `D:\Dev\repos\spendcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), Austrian §26 EStG travel allowances & SEPA pain.001 credit transfer & native GUI | 3,150+ | 1 | 2026-11-10 | A- |
| [hirecraft](hirecraft.md) | `D:\Dev\repos\hirecraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), ATS recruiting pipeline, blind scorecards & onboarding cascade & native GUI | 3,100+ | 1 | 2026-11-10 | A- |
| [helmcraft](helmcraft.md) | `D:\Dev\repos\helmcraft` | fleet-owned | Rust ArtCraft v0.1.0 (craft-biz suite) | 4 crates (store/core/mcp/app), CEO/CFO executive cockpit & live cross-fleet telemetry radar & native GUI | 3,300+ | 1 | 2026-11-10 | A- |
| [craft-biz](craft-biz.md) | `D:\Dev\repos\craft-biz` | fleet-owned | Rust shared kernel & UI kit | 2 crates (craft-biz, craft-biz-ui), Money, ÖNORM, ATU, EKR, Bus | 3,100+ | 46 | 2026-11-09 | A- |
| [musiccraft](musiccraft.md) | `D:\Dev\repos\musiccraft` | fleet-owned | Reserved (no code yet) | README + `docs/PRD.md` only | 0 | 0 | 2026-11-06 | Reserved |
| [smallvideocraft](smallvideocraft.md) | `D:\Dev\repos\smallvideocraft` | fleet-owned | Planned (`ittybittyvideos` flagship) | README + `docs/PRD.md` only | 0 | 0 | 2026-11-06 | Planned |

## Retired / Superseded Python Scaffolds (2026-11-09)

The six Nov-4 Python FastMCP craft scaffolds were audited and retired from active craft status on 2026-11-09:

| Spoke | Former Python Scaffold | Replaced / Superseded By | Reason |
|---|---|---|---|
| [revecraft](revecraft.md) | `sandraschi/revecraft` (933 LOC) | **`D:\Dev\repos\reversing-mcp` (`v2.3.0`)** | `revecraft` was a copy-paste subset of `reversing-mcp` (27 tools across 10 domains: Ghidra/ReVa, REA, IDA, Frida, ClickerLab CUA-to-disassembly, Directmedia `.DKI`). `reversing-mcp` is an engine orchestrator and remains the canonical reversing system. |
| [filecraft](filecraft.md) | `sandraschi/filecraft` (498 LOC) | **[wincraft](wincraft.md) (`D:\Dev\repos\wincraft`)** | Naive Python `os.walk` loops replaced by Pure-Rust `wincraft` (`win_fs_du`, 3-stage streaming `win_fs_dups`, `win_lock_inspect` Restart Manager FFI, `.bak` write/undo). |
| [virtucraft](virtucraft.md) | `sandraschi/virtucraft` | **[vmcraft](vmcraft.md) (`D:\Dev\repos\vmcraft`)** | Replaced by Pure-Rust 3-crate `vmcraft` (`v0.2.0`, 19 MCP tools, 25 tests, live-verified on Goliath). |
| [doccraft](doccraft.md) | `sandraschi/doccraft` (418 LOC) | **[bookcraft](bookcraft.md) (`v0.5.0`) + `office-mcp`** | Thin `soffice --headless` + 25-line `pypdf` wrapper; superseded by `bookcraft` (30 tools) and `office-mcp`. |
| [gitcraft](gitcraft.md) | `sandraschi/gitcraft` (451 LOC) | **`git-github-mcp` + [codercraft](codercraft.md)** | 6 thin `subprocess.run(["git"/"gh"])` wrappers; superseded by `git-github-mcp`. |
| [containercraft](containercraft.md) | `sandraschi/containercraft` (256 LOC) | **`docker-mcp` + [vmcraft](vmcraft.md)** | 6 thin `subprocess.run(["docker"])` wrappers; superseded by `docker-mcp`. |

## Proposed apps (2026-11-16)

The proposal list, the demo cuts, and the full-cut estimates are in [NEW_CRAFT_APPS.md](NEW_CRAFT_APPS.md). Four local demos started the same day: `horsecraft`, `bridgeclubcraft`, `philosophercraft`, `crochetcraft`.

## Spoke template (for new assessments)

```markdown
# <Name>Craft — Assessment
**Repo:** `D:\Dev\repos\<name>` · **Date:** 2026-11-09 · **Grade:** X · **Origin:** fleet-owned | storytold-ref | community
## What it is / Model / Verbs / Sources it consolidates
## Architecture (tier, crates/modules, ports)
## Strengths / Gaps / Risks
## Next 3 steps (smallest verifiable)
## Verdict (one paragraph)
```
