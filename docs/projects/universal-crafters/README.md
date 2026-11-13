# Universal Crafters — Documentation Hub

**Last updated:** 2026-11-07
**Owner:** Sandra S. + fleet agents
**Scope:** the gold-rush category: tools that **clone + improve** existing software
(websites, apps, games) and the missing twin: tools that clone **physical things**
— small bodies (matrioska dolls, anime figurines, toy robots, Meissen porcelain)
via photo-to-3D to makerspace print, and big bodies (houses → AutoCAD/BIM/Revit,
visible-gear machines, 16th-century automata) via multi-photo + floorplan pipelines.
**Status:** new section, v0.3 (2026-11-07: +BUILDINGS_MACHINES spoke, +Gap 6
Einfamilienhaus, +fal rent check §6). Opus entry: read this file, then
COMPARISON.md → PHYSICAL_LOOP.md → BUILDINGS_MACHINES.md → ECONOMICS_BYOK.md §6 → FLEET_GAPS.md Gap 6.

This hub is the **section index**. Each spoke is one deep note in this directory.
Spokes are point-in-time research, not marketing — read the spoke, then the
upstream README / pricing page / local `_upstream/` checkout.

**Do not duplicate this matrix elsewhere** — `projects/craft-fleet/README.md`
remains the fleet-craft index (our own builds); `research/2026-11-01-*craft*`
remain the one-off teardowns. This section is the *category* view.

## Why this section exists

Maker tools (generate a bookkeeping app from zero) have existed for years:
Vercel v0, Lovable, Bolt.new, Replit Agent, Durable. The **reversing part is new**:
point at an existing bookkeeping website, clone it, then improve it. That is the
gold rush of late 2026.

Three archetypes collided in one week of fleet research:

1. **REA (`morluto/rea`, rea.tools)** — 439k stars, 6,640 commits. The oracle.
   Inspects anything (native, .NET, APK, Electron, web, firmware, packets) via
   ~350 MCP tools, returns pseudocode + evidence. Does NOT build. Node.js.
2. **Craft Anything (`storytold/craft-anything`)** — 19.3k stars, 468 commits.
   The cloner. Study → Build → Check → Ready. Pure Rust, 320 tools, Clean-room /
   Deep modes, drives YOUR `claude` CLI (BYOK), checks at 3 viewports, ships
   Win/Mac/Linux/FreeBSD + WASM viewer. Early alpha.
3. **fal.ai** — NOT a crafter. The arms dealer. 1,000+ generative media models
   behind one API: image/video/audio/3D. `fal-ai/trellis-2` image-to-3D at
   $0.25–0.35/pop returns GLB. Craft Anything calls it opt-in for pictures and
   3D models with YOUR fal key.

None of them closes the **physical loop**: photo of a matrioska → 3D asset →
printable makerspace file on a micro-USB stick. See `PHYSICAL_LOOP.md`.

## How to read this hub

- **New here?** Read this file, then `COMPARISON.md` (the matrix).
- **Want the matrioska workflow?** Read `PHYSICAL_LOOP.md` (photo → Trellis v2 →
  splat/CAD → STL/3MF → Orca/Bambu → makerspace).
- **Want to self-host?** Read `FOSS_CATALOG.md` (what to clone locally today).
- **Want the money math?** Read `ECONOMICS_BYOK.md` (heavy AI use, local BYOK,
  why the fleet bets on Claude-subscription + local engine + pay-per-asset fal).

## Spoke index

| Spoke | Question it answers |
|---|---|
| [COMPARISON.md](COMPARISON.md) | craft-anything vs REA vs fal.ai vs v0/Lovable/Bolt/screenshot-to-code — who clones, who makes, who charges |
| [PHYSICAL_LOOP.md](PHYSICAL_LOOP.md) | Why no cloner does bodies yet, and the matrioska → Trellis v2 → splat/CAD → makerspace pipeline that works today by hand |
| [BUILDINGS_MACHINES.md](BUILDINGS_MACHINES.md) | Second bodies class: house (+rooms +floorplans) → AutoCAD → BIM/IFC → Revit, visible-gear machines, 16th-c. automata |
| [FOSS_CATALOG.md](FOSS_CATALOG.md) | Every FOSS repo worth cloning for each stage, with license + run cost |
| [ECONOMICS_BYOK.md](ECONOMICS_BYOK.md) | Heavy-model strategy: BYOK Claude + local engine + fal-per-asset vs cloud-seat builders |
| [FLEET_GAPS.md](FLEET_GAPS.md) | What the fleet should build next (splatcraft/modcraft/makercraft wiring) |

## One-paragraph verdict

REA won inspection. Craft Anything won the rebuild loop. fal.ai won the
asset till — props, styles, scenes, worlds catalog far ahead of everyone, but
no physical-make support yet (no slice, no tolerance, no maker routing). Expect
that gap to close commercially first: fal + a few US/PRC physical-maker corps
(print/mill/fulfilment) as paid endpoints next. That is convenient and, at
fal margins, brutally expensive rent-seeking — see ECONOMICS_BYOK.md §6. The
fleet bet stays: local lift + repair + CAD/BIM in our crafts, fal only for the
one glamour pass. That is the bet this section documents.

## Sources (grounded 2026-11-07)

- `_upstream/craft-anything/README.md` (local) + live GitHub (19.3k stars,
  3.6k forks, 320 tools, Claude Code-first, fal.ai opt-in).
- `_upstream/rea/README.md` (local) + live GitHub (439k stars, 108.8k forks) +
  `https://rea.tools/` (Calculator/Dino/Notion/DX-Ball showcases).
- `https://fal.ai/pricing` + `https://fal.ai/models/fal-ai/trellis-2`
  ($0.25/512p, $0.30/1024p, $0.35/1536p → GLB).
- `research/2026-11-01-craft-anything-and-rea-deep-dive.md` (fleet teardown).
- `projects/craft-fleet/README.md` (fleet-owned crafts: splatcraft B-,
  makercraft/modcraft C+, solidcraft via Tangency Labs).
