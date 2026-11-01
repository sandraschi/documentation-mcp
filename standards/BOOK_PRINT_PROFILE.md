---
title: "Book Print Profile (DesignCraft)"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-10-20
---
# Book Print Profile (DesignCraft)

Canonical print settings for the `on-*` book series. The source of truth is
`on-hyperart/tools/build_layout.py`; this file records what "same settings"
means so the other books can match it without guessing.

## Page

| Setting | Value |
|---|---|
| Trim | A4, 595.276 x 841.89 pt |
| Facing pages | yes |
| Bleed | 9 pt (~3.17 mm) |
| Margins | top 84, bottom 92, inside 92, outside 78 pt |
| Text column | 425.28 pt |
| Body start | page 5 (front matter is 4 pages) |
| Chapter openers | recto, blank verso inserted as needed |

## Type

Georgia throughout.

| Style | Size / leading | Notes |
|---|---|---|
| Body | 12.5 / 19.5 | left-justified, first-line indent 12, hyphenate |
| Body First | inherits Body | indent 0 |
| Chapter Title | 26 / 30 | bold, space after 26 |
| Section | 12.5 / 16 | bold, space before 16, after 6 |
| Quote | 10 / 14.5 | italic, left indent 18 |
| Note | 7.3 / 9.4 | footnotes |
| TOC Title | 18 / 22 | bold, space after 18 |
| TOC Entry | 10 / 14 | space before/after 3 |
| Head Verso/Recto | 7.5 / 9 | tracking 80; verso left, recto right |
| Folio Verso/Recto | 8.5 / 10 | verso left, recto right |
| Plate Caption | 8.5 / 12 | italic |

## Structure

1. Title page: title 34/40 bold, subtitle 14/20 italic, author 13/18,
   imprint 9/13.
2. Colophon verso: title, author, draft status, production note, credits.
3. Contents on page 3 (recto); page 4 is the structural verso.
4. Body from page 5. Each chapter starts on a recto; insert one blank verso
   when the previous chapter ends on a recto.
5. Running heads: book title verso, chapter title recto. Folios bottom outer.
6. TOC generated after all chapters so folios are final.

## Tables

DesignCraft equalises DOCX table columns regardless of `tblGrid`/`tcW`.
Set widths after import:

- Find the body story by matching the chapter title against
  `document.inspect` story previews (the `file.place` story id is not reliable).
- `table.select {story, table, cols: [c,c], what: "column"}` then
  `table.setColumnWidth {width}`.
- Table indices are 1-based.
- Widths come from header proportions, scaled to the 425.28 pt column.

## Build pipeline

1. Markdown -> DOCX with pandoc, named styles mapped to the table above.
2. DesignCraft script: `file.new`, styles, front matter, chapter placement
   (recto, autoflow), plate images, table pass.
3. Final stage: running heads, folios, `toc.generate`, export PDF.
4. Verify: page count, blank pages, TOC folios, table header `x0` positions.

## Current state (updated 2026-10-29)

- `on-hyperart` is the reference implementation: 90 pages, one structural blank.
- `on-metacraft`: 120 pages (scaled up from 52 pages following late-October chapters).
- `on-hyperwar` (92) and `on-ai-takeover` (84) fully built. All four use the
  shared `bookkit/designcraft_pdf.py` module via `just print`
  (`bk pdf --engine designcraft`).
- `bk pdf` without `--engine` remains the A5 headless-Edge draft.
- `on-consciousness` does not exist yet.
- Portal for future books: add `just print` and keep `book.toml` chapter order;
  no per-repo layout script needed.
