---
title: "Upstream craft doctrine (the Basilica rule)"
category: standard
status: active
audience: all
last_updated: 2026-10-14
---

# Upstream craft doctrine

storytold/ArtCraft is the mothership: the canonical reference for pure-Rust,
CLI-first, MCP-serving desktop apps. The local checkouts in
`D:\Dev\repos\_upstream\` are the parish church - same texts, read-only
default, pilgrimage as needed. This file states how to treat them.

## What lives in `_upstream` (verified 2026-10-14)

All 12 crafts (word/deck/design/effect/film/grid/light/pdf/photo/sound/vector/
cadcraft) + `craft-launcher` + Strata + buzz/ResoniteLink/VoiceStudio/
gods-eye-view. `figcraft` cloned 2026-10-14 @ `bcedfeb` (repo went up 2026-10-09).

## Remote wiring is MIXED - check per dir

- `origin=storytold`, no other remote: pure clone (pull-only). Example: figcraft.
- `origin=sandraschi` + `upstream=storytold`: fork (pushable; PRs go upstream).
  Example: craft-launcher, wordcraft.
- Rule: `git remote -v` before assuming. Default read-only either way; never
  modify without a reason. (Fleet root AGENTS.md still says "never modify" as
  an absolute - that line predates the forks and is stale as written.)

## Licensing: paste 99.9%

Every craft root carries `LICENSE-MIT` + `LICENSE-APACHE` (checked: figcraft,
wordcraft, craft-launcher). MIT OR Apache-2.0 grants copy, modify, sublicense.
Two obligations, both mechanical:

1. **Keep the attribution.** Copyright + permission notices travel with every
   paste; preserve NOTICE/ATTRIBUTION.md where present. Stripping notices is
   the one way to turn licensed use into infringement.
2. **Pin the source commit.** One line per paste: file, upstream commit, date,
   why. Upstream ships near-daily; unpinned pastes become mystery code within
   weeks ("from figcraft @ `bcedfeb`, 2026-10-14" is the whole format).

Excluded: `docs/brand/` and contributor art (names, logos, marks). Code,
patterns, procedures, docs prose: fair game with 1+2 done. No clean-room
needed on our side - the license is a grant, use it as one.

## Vendoring guidance (megaton cadence)

- **Small pieces** (CLI arg shapes, MCP envelope handling, error codes,
  agent-convention tables): vendor with provenance lines. You own their
  bugfixes from the paste date forward.
- **Big pieces** (renderers, format codecs, collab protocol): do NOT vendor.
  Point at the checkout (`_upstream\<craft>\docs\...`) and `git pull` before
  porting. `figcraft/docs/mcp.md` alone is 126KB; owning a copy means owning
  its daily diff.
- Re-pull before any port. Never port from a month-old checkout without
  checking what moved - the parity docs (`target-app-parity.md` etc.) are
  dated change rows; read the tail first.

## Verified findings (so nobody re-pays the lookup)

- **craft-launcher has NO MCP server.** All 152 files grepped: the only MCP
  hits are marketing strings in `crates/core/src/details.rs`. No rmcp dep, no
  server code. The launcher installs/updates/opens apps; each app ships its
  own MCP (`crates/mcp` + `docs/mcp.md` + e2e `agent_tasks.rs`).
- **FigCraft reference layout** (the shape to copy): `apps/` + `crates/`
  (incl. `mcp`, `engine`, `format`, `ui-egui`) + `docs/` (cli.md,
  control-protocol.md, mcp.md, server.md, plugins.md) + `xtask` CI.
  MCP protocol `2025-06-18`, headless or `--attach`, same command ids across
  menus/CLI/control-channel/MCP.
- **Strata is here, not absent** (`_upstream\Strata`: engine + venv + 11235
  config built; weights missing; opencode MCP entry points at a stale path).
  Full story: `research/2026-10-14-local-llm-dev-failure.md` sections 2, 4f, 5.6.
