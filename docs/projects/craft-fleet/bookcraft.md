# BookCraft — Assessment

**Repo:** `D:\Dev\repos\bookcraft` · **Date:** 2026-11-09 · **Grade: A** · **Origin:** fleet-owned

## What it is

Full-power Calibre library manager and e-book reader/extractor in pure Rust (`v0.5.0`): search, inspect, edit, add, remove, convert, ingest, catalog rename/merge, text extraction, cover art shelf, and in-shelf reading. L1 core + L2 CLI/MCP (30 tools) + L3 native `eframe`/`egui` shelf (`7,170 LOC`, `46 tests`, `--smoke` green). **BookCraft is the craft; `rust-calibre-mcp` stays the read-only dashboard.**

## Model / verbs

- **Model:** Calibre library (`metadata.db` + book formats + full-text index + cover thumbnails + reading marks/annotations).
- **30 MCP tools / CLI verbs (`v0.5.0`):**
  - Core library & search: `status`, `list`, `search`, `info`, `grep`, `stats`, `schema`, `backup`, `doctor`, `tools`
  - Mutation & safety: `update`, `bulk-update`, `add-book`, `remove-book`, `add-format`, `remove-format`, `convert`, `ingest`
  - Phase B catalog & extraction (`v0.4.0`–`v0.5.0`): `authors`, `tags`, `series`, `publishers`, `rename-tag`, `merge-tags`, `rename-author`, `extract-text`, `cover`, `cover-rgba`, `marks-list`, `marks-set`, `export-catalog`
  - Every verb accepts `--json`; CLI, MCP, and L3 GUI share one `dispatch` bus.

## Architecture

Rust 3-tier workspace (`bookcraft-core`, `bookcraft-mcp`, `bookcraft-app`), `7,170 LOC`, `46 tests`, clippy five-denies, `just ci` (fmt + clippy + test), `AGENTS.md`, `HANDOVER.md`, `INSTALL.md`, `CHANGELOG.md`, `docs/` (`PRD.md`, `TOOLS.md`, `UI_PARITY.md`, `PARITY.md`). L3 desktop app now includes the visual Cover Art Shelf (`cover_rgba` decoding), in-shelf text reader, and bulk selection marks.

## Strengths

- The fleet's honesty and write-safety exemplar: automatic timestamped `metadata.db` backup before every write (reused within 120 s), recoverable trash-by-default on `remove-book` (`--permanent` explicit), and strict `--root` path confinement.
- Phase B (`v0.4.0`/`v0.5.0`) closed all major gaps from the Nov-5 assessment: tag/author rename & merge, full-text extraction (`extract-text`), cover decoding (`cover_rgba`), reading marks, and bulk metadata updates are live and tested (`46 tests`).
- Complete parity documentation (`docs/PARITY.md`, `docs/UI_PARITY.md`, `docs/TOOLS.md`).

## Gaps / risks

- Calibre schema trigger differences across older Calibre 5.x vs 7.x libraries still merit a short compatibility matrix in `docs/`.
- EPUB/PDF reflow formatting in the in-shelf reader is plain-text/chapter-structured first; complex CSS layout remains delegated to external viewers when needed.

## Next 3 steps

1. Add Calibre 5.x–7.x schema/trigger compatibility notes to `docs/PARITY.md`.
2. Add performance benchmarks for large libraries (10k+ books cover thumbnail caching) in `benchcraft`.
3. Keep all `democraft` book recipes green against `v0.5.0`.

## Verdict

Grade A: the craft the rest of the fleet is measured against. With `v0.5.0` shipping 30 MCP tools, 46 tests, catalog tag/author management, cover-art grid, and in-shelf reading, Phase B is complete.
