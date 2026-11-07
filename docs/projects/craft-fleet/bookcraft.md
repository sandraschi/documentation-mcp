# BookCraft — Assessment

**Repo:** `D:\Dev\repos\bookcraft` · **Date:** 2026-11-05 · **Grade: A**

## What it is

Full-power Calibre library manager in pure Rust: search, inspect, edit, add,
remove, convert, ingest. v0.3.0 — L1 core + L2 CLI/MCP (15 tools) + L3 shelf,
34 tests, `--smoke` green. The rebuild-PLAN cutover call is made: **BookCraft is
the craft; `rust-calibre-mcp` stays the read-only dashboard (no archive).**

## Model / verbs

- **Model:** Calibre library (`metadata.db` + formats + full-text index).
- **17 verbs:** `status list search info grep stats convert ingest schema backup
  update add-book remove-book add-format remove-format tools mcp` — every verb accepts
  `--json`; MCP exposes 15 tools (`book_*`, dotted aliases accepted).
- Ingest = saved HTML → Markdown artifact; live Readly browser path stays in `readly-mcp`.

## Architecture

Rust 3-tier (core/mcp/app), clippy five-denies, `just ci` (fmt + clippy + test),
`AGENTS.md` containment rules, `HANDOVER.md`, `INSTALL.md`, `CHANGELOG.md`,
`docs/` (PRD, TOOLS, UI_PARITY, PARITY). One `dispatch` bus: CLI and MCP cannot
disagree; L3 app calls `dispatch` in-process (proven by
`app_dispatch_matches_core_dispatch`). `--root` confinement; stdio invariant
(stdout = JSON-RPC only, logs → stderr).

## Strengths

- The fleet's honesty exemplar: backup-before-write (timestamped, reused <120 s),
  trash-not-delete (`remove-book` recoverable, `--permanent` explicit), converter
  `down`-reporting, `LIKE`-escape + format validation, no silent downgrades.
- PARITY docs state what is deliberately out of scope — the pattern every craft
  should copy.
- Democraft-registered (`book` tile) with 5 green recipes at last report.

## Gaps / risks

- Phase B pending: catalog rename/merge, analytics, export (per PLAN progress note).
- Calibre-version drift (schema triggers) needs a version matrix in `docs/`.
- `ebook-convert` dependency honesty is correct but UX-thin — installer guidance matters.

## Next 3 steps

1. Phase B: rename/merge + analytics + export, each with `docs/` + tests.
2. Calibre-version matrix (tested versions, trigger-behavior notes).
3. Keep the 5 democraft recipes green; add the convert-roundtrip timing baseline.

## Positioning vs writercraft (2026-11-05 decision)

Long-form, library, and writing-craft knowledge live here: the calibre-mcp
consolidation, book repos, writing workflows and cookbooks (blog writing, HN /
Discord / Reddit posts), literature theory and practice across the centuries,
the perils of LLM-ese style. Renaming to something broader rejected —
`etextcraft` considered and discarded as fugly; Calibre itself already holds
books, comics, manga, magazines and papers, and the bookcraft name carries
that width. (Open: user mentioned "hyperwar" book repos — confirm which repos
these are.) Short-form and struggling authors (journalists, scientists
fighting an arXiv paper) belong in writercraft.

## Verdict

Grade A: the craft the others are measured against. Strictest write-safety,
best parity docs, proven recipes. Remaining work is growth (Phase B), not repair.
