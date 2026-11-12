# WriterCraft — Assessment

**Repo:** `D:\Dev\repos\writercraft` · **Date:** 2026-11-05 · **Grade: C+**

## What it is

Local-first narrative architecture, TV-Tropes indexation, corkboard scene manager,
and academic publishing studio — offline, no cloud extraction. Port `14121`.
Consolidates `tvtropes-mcp`, `arxiv-mcp`, `calibre-mcp`, `digibib5-mcp`,
bookkit/substack concepts. ScholarCraft is the academic half (same repo).

## Model / verbs

- **Model:** story node (scene/beat) + trope link + manuscript/LaTeX artifact.
- **Crates:** `writercraft-narrative`, `writercraft-core`, `writercraft-mcp`, `writercraft-app`.
- Narrative/core split mirrors djcraft's audio/core — domain engine isolated.

## Architecture

Rust ArtCraft 3-tier, MIT/Apache. `start.ps1`/`start.bat` present. No `docs/`,
no `justfile`, no test evidence at triage. Last commit 2026-11-04 (fleet i18n).

## Strengths

- Narrative + scholarship in one studio matches how books are actually written
  (corkboard → manuscript → LaTeX), and the trope engine is a genuine moat.
- Clear neighbors: bookcraft stores/converts, writercraft composes — good seam if written down.
- Offline-first matters for manuscripts (no cloud extraction of drafts).

## Gaps / risks

- Two products (fiction corkboard + academic epistemic graph + LaTeX publishing)
  in one repo — sequence fiction first, scholar second.
- Trope data licensing (TV Tropes mirror status) and arXiv/epistemic-graph
  sourcing unaddressed.
- LaTeX toolchain on Windows (headless install drift) is the doccraft-adjacent risk.
- No `docs/`, no narrative-model tests.

## Next 3 steps

1. `docs/PRD.md` with fiction-first scope and bookcraft boundary paragraph.
2. Narrative-model tests (scene graph fixture → corkboard artifact).
3. One democraft recipe: `writer/scene-pack` (fixture scenes → manuscript artifact).

## Positioning vs bookcraft (2026-11-05 decision)

Short-form and struggling authors live here: journalists on deadline,
scientists fighting an arXiv paper concept. Long-form, library management
and writing-craft knowledge (cookbooks, post workflows, literature theory,
LLM-ese perils) belong in bookcraft. Overlap at the boundary is intentional
(a manuscript becomes a book) but the audiences differ: writercraft helps you
finish the piece, bookcraft keeps and teaches everything around it.

## Verdict

Strong concept, double-product risk. C+ until scope is cut in writing and the
scene-graph tests prove the narrative crate.
