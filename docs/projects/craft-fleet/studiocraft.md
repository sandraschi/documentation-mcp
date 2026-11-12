# StudioCraft — Assessment
**Repo:** `D:\Dev\repos\studiocraft` · **Date:** 2026-11-06 · **Grade:** C+ · **Origin:** fleet-owned

## What it is / Model / Verbs / Sources it consolidates
Shared `.studiocraft` project host for the Photo <-> Vector safe round-trip
(#1233 idea, no launcher fork). Model: `manifest.json (contract studiocraft/v1)` +
`painting/ + vectors/ + companions/ + composite.png (preview)`.
Verbs (12 MCP tools + CLI, one dispatch): status, caps, init, open, list,
handoff_check, companion_attach, composite_bump, skills_list, skill_show,
llm_chat, llm_models. Consolidates: storytold-ref engines (photo/vector/light/design
as probes/caps, never reimplemented) + our own future crafts behind same adapter shape.

## Architecture (tier, crates/modules, ports)
Pure-Rust ArtCraft 3-tier, zero ports, stdio MCP 2024-11-05:
`studiocraft-core` (project, adapters, handoff, skills, workflows, llm),
`studiocraft-mcp` (`studiocraft-cli` + hand-rolled stdio loop),
`studiocraft-app` (7-view egui: Projects/Handoff/Adapters/Chat/Skills/Help/Logs,
harsh dark visuals, Ctrl+Wheel zoom, glyph allowlist, `--smoke`, no child spawn).

## Strengths / Gaps / Risks
Strengths: 6 gates green (clippy/test/fmt/stdio/lock/changelog), 10+ tests,
8 docs (PRD/TOOLS/PARITY/UI_PARITY/CONTRACT/WORKFLOWS/SKILLS/CHAT), 6 skills,
Fleet LLM card (ollama/lmstudio/openai/anthropic/custom, memory-only keys),
block-never-flatten gate, provenance tags.
Gaps: no live Photo/Vector driving yet (probes report down honestly),
no composite PNG writer (manifest-level), no 12-app canvas, no democraft recipes yet,
no keyring vault (env/memory only).
Risks: scope creep to 12-app editable; chat latency on local 27B; revision misuse
(bump before verify).

## Next 3 steps (smallest verifiable)
1. Wire 3 democraft recipes (init+open, photo->vector clean, vector->photo blocked-on-unsaved) with `run.json`.
2. Add composite PNG writer (max 4MP rev-cache) + `workflows::composite_refresh` test.
3. Attach first companion end-to-end (design linked preview) and prove open/attach/open.

## Verdict (one paragraph)
First C+ to add docs + green gates + skills in the runt wave. Real studio shell,
honest runt core: safe 2-app loop proven headless, companions preview-only by design.
Promote to B when 3 democraft recipes go green and composite refresh lands.
