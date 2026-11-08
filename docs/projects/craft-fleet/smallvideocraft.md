# SmallVideoCraft — Assessment

**Repo:** `D:\Dev\repos\smallvideocraft` · **Date:** 2026-11-05 · **Grade: planned (nucleus runs elsewhere)**

## What it is

Name reservation with a plan — the short-video umbrella. "Small" is the
scope and the Storytold boundary in one word: shorts, explainers, demo clips,
propaganda cuts. Timelines and NLE belong to Storytold filmcraft/effectcraft.

## Model / verbs (planned, per `docs/PRD.md`)

- **Model:** short project `{ script, scenes[], narration, aspect, footage[],
  captions, render }`.
- **Verbs (draft):** `script new`, `footage gather`, `narrate`, `render`,
  `caption`, `publish`, `mcp`.

## Architecture

Umbrella only. The flagship runs under its own brand:
[ittybittyvideos](https://github.com/sandraschi/ittybittyvideos) (script in →
shorts out, installer + dashboard + MCP) keeps name, installer, and issues.
Phase 1 maps its verbs onto the PRD before any native build.

## Sources it consolidates

`ittybittyvideos` (flagship, keeps brand), `streamfog-mcp` (live AR input →
clips), `rust-photoprism-mcp` stills input (tentative). Built-in demand:
democraft gallery + gamecraft web clips.

## Next 3 steps

1. Scope freeze + flagship alignment (PRD Phase 1).
2. `footage gather` + `publish` as first native verbs.
3. First democraft recipe (`shorts/script-to-short` on fixtures).

## Verdict

A claimed umbrella with a running flagship and an honest non-goal vs
filmcraft. Unranked until Phase 1 — which the README says.
