---
title: "Typography and Print Glossary"
category: reference
status: active
audience: fleet
last_updated: 2026-10-20
---
# Typography and Print Glossary

Plain-language reference for the terms that show up in book and print
pipelines. Aimed at agents and developers who can read a PDF but have never
stood at a press.

## Pages and spreads

- **Recto** — a right-hand page (odd page number in a Western book). Chapter
  openers usually start on a recto.
- **Verso** — a left-hand page (even page number).
- **Spread** — the pair of facing pages a reader sees at once: verso on the
  left, recto on the right. "Facing pages" in layout software means pages are
  arranged in spreads, not singly.
- **Folio** — the printed page number. Also used for the page number's position
  and style (top outer corner, bottom centre, etc.).
- **Running head** — the line at the top of each page naming the book, chapter,
  or section. Usually book title on verso, chapter title on recto.
- **Front matter** — everything before the body: half-title, title page,
  copyright/colophon, dedication, contents, preface. Often numbered in roman
  numerals.
- **Body** — the main text, usually starting at page 1 in arabic numerals.
- **End matter / back matter** — after the body: appendices, notes, glossary,
  bibliography, index, colophon.
- **Colophon** — the note about how the book was made: typefaces, production
  tools, credits, edition data.

## Page geometry

- **Trim size** — the final page size after the printer cuts the sheet (A4,
  US Letter, 6x9 in).
- **Bleed** — artwork that runs past the trim edge so a small cutting error
  does not leave a white sliver. 3 mm is a common book bleed.
- **Slug** — an extra area outside the trim/bleed for printer marks and notes;
  not part of the finished page.
- **Gutter** — the inner margin at the spine; the space the binding eats.
- **Inside margin** — the margin at the spine (gutter side).
- **Outside margin** — the margin at the fore-edge (the opening side).
- **Fore-edge** — the outer edge of the book, opposite the spine.
- **Head / foot** — top / bottom of the page.
- **Baseline grid** — an invisible grid of text baselines; elements snap to it
  so facing pages line up.
- **Signature** — a folded sheet of pages in a bound book (usually 8, 16, or 32
  pages). Books are printed in signatures, then folded and trimmed.
- **Imposition** — arranging pages on the press sheet so they end up in the
  right order after folding and cutting. "Printer's spread" is the imposed
  pair, which is not the same as the reader's spread.

## Type

- **Leading** (rhymes with "sledding") — the vertical distance between
  baselines, i.e. line spacing. 12.5/19.5 means 12.5 pt type on 19.5 pt
  leading.
- **Kerning** — adjusting space between a specific pair of letters.
- **Tracking** — adjusting space across a range of letters (letter-spacing).
- **Widow** — a short last line of a paragraph stranded at the top of a page.
- **Orphan** — a short first line stranded at the bottom of a page.
- **Drop cap** (versal, initial) — an oversized first letter of a chapter or
  paragraph, usually spanning 2-3 lines, with the text wrapping around it. In
  InDesign terms: `dropCapLines` + `dropCapCharacters`.
- **Raised cap** — a large initial that sits on the first baseline instead of
  dropping into the paragraph.
- **Small caps** — uppercase letterforms at roughly x-height size, used for
  acronyms and emphasis without shouting.
- **Ligature** — two or more letters drawn as one glyph (fi, fl, ffi).
- **x-height** — the height of lowercase letters without ascenders/descenders.
- **Measure** — the width of a line of text, usually in characters or picas.
- **Ragged right** — left-aligned, uneven right edge. The opposite of
  justified.
- **Justified** — text aligned on both edges, with word spacing adjusted.
- **Hyphenation** — breaking words at line ends; needed for good justification.
- **Widow/orphan control** — settings that prevent stranded lines.

## Tables and figures

- **Table grid** — the column-width definition in a DOCX (`tblGrid`/`gridCol`)
  or an InDesign table.
- **Cell inset** — padding inside a table cell.
- **First baseline** — where the first line of text sits inside a cell; can be
  measured from the cell top, cap height, x-height, or leading.
- **Span / merge** — a cell covering multiple rows or columns.
- **Plate** — a full-page image, often on its own page and sometimes with a
  caption on the facing page.
- **Caption** — the text identifying a figure or plate.
- **Figure** — a diagram, chart, or illustration embedded in the text flow.

## Colour and output

- **CMYK** — cyan, magenta, yellow, black; the ink model for print.
- **RGB** — red, green, blue; the light model for screens.
- **Rich black** — a black built from multiple inks (e.g. 60/40/40/100) for
  dense areas; plain 100K is "flat black".
- **Overprint** — printing one ink over another instead of knocking it out.
- **PDF/X** — a family of PDF standards for print exchange (PDF/X-1a, X-4).
  X-4 allows live transparency and colour management, and carries XMP metadata.
- **XMP** — metadata embedded in a PDF (creation date, version id, colour
  profile).
- **Imposition proof** — a proof showing pages in printer's-spread order.

## Pipeline terms

- **Preflight** — automated checks before output: missing fonts, low-resolution
  images, RGB in a CMYK job, bleed too small.
- **Package** — collect the document plus linked images and fonts so another
  machine can open it.
- **Link** — a reference to an external image/font rather than an embedded copy.
- **Flatten** — merge transparency/effects into a single image layer (older
  PDF/X-1a workflows).
- **Reproducible build** — same inputs produce the same PDF; avoids manual
  nudging in the GUI.
