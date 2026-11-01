# Adobe Offensive - Fleet Project Hub

Status: active cold-watch + build-harness. Last updated: 2026-10-08.

## What this is

Brandon Thomas / storytold / ArtCraft pivoted 2026-10-04 from a controllable-AI IDE
to 7 open source Adobe clones in pure Rust + WASM, built AI-only with Claude Opus 5.5
since Feb 2026. Ars Technica covered it 2026-10-07 (Kyle Orland):
"Software is over: Bold AI developer takes aim at Adobe with open source clones".

This section is the fleet's working file for Opus and all agents. It answers:
what happened, what we can legally copy, what we already own, what other Windows
apps are now reversible the same way, why pywinauto-mcp is the superpower, and
what plans to execute.

## Docs in this section

| File | What |
|---|---|
| `01-artcraft-ars-analysis.md` | Timeline, 7 apps, tech, funding, claims, legal, why bug-counting is myopic |
| `02-what-to-copy.md` | Copyable patterns, clean-room rules, MIT vs Fair Source boundary |
| `03-fleet-inventory.md` | Fleet 7:7 map vs Adobe, gaps, crossconnect plan |
| `04-winapp-targets.md` | Other reversible Windows targets beyond Adobe, ranked |
| `05-pywinauto-superpower.md` | Why pywinauto-mcp + browser-mcp + autohotkey-mcp = reversal engine |
| `06-plans-roadmap.md` | Phased plans for Opus: watch, harness, single-panel demo, mesh |
| `07`-`11` | Strategy/timing, videostudio, robotstudio, InterPositive, contributor funnel |
| `12-artcraft-ux-teardown.md` | Webapp sidebar IA (Create vs Studio), tokens, stack, apps site, per-app page template |
| `13-business-model.md` | Free apps vs metered AI, credit economics, relicense, Canva-Affinity twin |
| `14-legal-deep-dive.md` | US/EU doctrine table, 2026 SCOTUS status, trade dress, patents, CUA clean-room honesty |
| `15-trajectories.md` | Scenarios A-G (destroyed, Adobe, AI corp, founder hire, pipeline sale, king, fizzle), comps, signals |
| `16-portfolio-expansion.md` | Office batch (2026-10-07), fit matrix, shared-engine thesis, -craft name collisions, cadcraft + qcad-mcp + freecad-mcp pipeline |
| `21-wordcraft-authoring.md` | WordCraft authoring pipeline |
| `22-soundcraft-status.md` | SoundCraft 0.8.0 status: built-ins work, VST3 effects work, VST3 instruments silent (BUG-082 / upstream PR #347), Reaper control, re-test checklist |
| `HANDOVER.md` | Session log for whoever picks this up next |

> ERRATUM 2026-10-11: core artcraft was relicensed from WIP Fair Source to
> MIT OR Apache-2.0 on 2026-10-10 (PR #2043). Every "Fair Source" statement in
> 01, 02, 06 and rule 1 below is historical. See 13 section 2.

## Key links

- Core IDE repo: https://github.com/storytold/artcraft (Fair Source, NOT MIT)
- Apps hub: https://getartcraft.com/apps (claims MIT/Apache per Ars - verify per repo)
- Ars: https://arstechnica.com/ai/2026/10/software-is-over-bold-ai-developer-takes-aim-at-adobe-with-open-source-clones/
- Reddit announce: https://www.reddit.com/r/SaaS/comments/1wwnhbt/ive_created_open_source_100_rust_cleanroom/
- HN threads: 49934228, 49958850, 49959605, 49960138

## Rules for this project

1. (Superseded 2026-10-10: core is now MIT OR Apache-2.0.) Reuse is legal with
   attribution; brand assets stay reserved by NOTICE. Still prefer bridging over cloning.
2. New Craft apps are claimed MIT - verify LICENSE file per repo before any reuse.
3. Never copy Adobe trade dress pixel-for-pixel. Functional parity is legal, lookalike UI is Tetris-case risk.
4. ASCII-only prose in all docs here. No em dashes, no smart quotes, no emoji.
5. Max 5 files per commit. 3+ edits need .bak first.
