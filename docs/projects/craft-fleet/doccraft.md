# DocCraft — Assessment

**Repo:** `D:\Dev\repos\doccraft` · **Date:** 2026-11-05 · **Grade: C**

## What it is

Office-document workstation and headless automation engine.
Rebuild-PLAN Wave-1 #4 (from `libreoffice-mcp`). Office in, PDF out —
doccraft handles office input where pdfcraft handles PDF ops (boundary is explicit).

## Model / verbs

- **Model:** office document (docx/odt → pdf/txt).
- **Verbs (README):** `convert text info combine` family.
- **Surface:** `cli.py` + `mcp_server.py`, `justfile`, `AGENTS.md`. 2 test files.

## Architecture

Python FastMCP, `.venv`, `pyproject`. Scaffold committed 2026-11-04.

## Strengths

- Clean office/pdf boundary with pdfcraft — no turf war by design.
- Headless-LibreOffice verb shape is proven upstream (libreoffice-mcp); this is
  a re-skin, not an invention.

## Gaps / risks

- LibreOffice headless install drift is the known killer (version pin in `docs/` needed).
- Fixture coverage (docx/odt fixtures, page-count + byte assertions) not yet shown.
- `.bak` discipline matters here: office roundtrips litter directories without care.

## Next 3 steps

1. Pin the LibreOffice version + headless flags in `docs/` (or root doc until `docs/` exists).
2. 3 recipes: `doc/convert-roundtrip`, `doc/text-extract`, `doc/combine-split` (fixtures + measures).
3. Overlap note with writercraft's LaTeX/publishing half (who owns manuscript → PDF?).

## Verdict

Grade C: correct boundary, proven upstream verbs. Version pin + fixture recipes
are the whole promotion path.
