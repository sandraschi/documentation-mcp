# 21 - WordCraft authoring round-trip (book repos)

Date: 2026-10-15. Status: proof in temp/, not committed to book repos.
Follows 20 (DesignCraft x books, FigCraft x web). Upstream read-only: `D:\Dev\repos\_upstream\wordcraft`.

## Installed

`C:\Program Files\WordCraft\wordcraft.exe` + `wordcraft-cli.exe` (75MB CLI).

```text
convert <in> <out> [--markup] [--format wordml2003|flatopc]  # docx, doc[read], pdf, odt, rtf, html, md, tex, txt, json, png, xml
info / text / inspect / render [--page N] [--scale S]
run [--file F | --template T] --cmd 'id={json}' [--save OUT] [--print] [--author NAME]
commands [--json] / parity / zotero <cmd> (Zotero must be running)
mcp [--connect HOST:PORT | --author NAME] [--automation-read-root DIR] [--automation-write-root DIR]
```

## Proof (on-metacraft 00-preface.md, preface is front_matter so closest to real)

- `info chapters/00-preface.md` -> 2pp, 17 paras, 0 comments, clean, 191ms layout.
- `convert 00-preface.md -> temp/00-preface.docx` (8.7KB) OK.
- `convert 00-preface.docx -> temp/00-preface-rt.md` (2926B) OK.
- `git diff --no-index`: 11 insertions, 42 deletions. Content preserved, hard-wrap collapsed (multi-line paras joined to one line, `**Status**...**Revision**` joined). Expected md->docx->md reflow, not text loss. No docx edit in loop yet - next step is a real tracked-change pass to prove `--author` + `--markup`.

## Role in chain

bookkit = source of truth (`lore`, `build`, `validate`). WordCraft = edit/cite round-trip (reviewers who live in Word, Zotero citations, Print Markup). DesignCraft (20) = final threaded print layout + PDF/X-4 + EPUB. Never round-trip stubs as final; preface pilot only.

## MCP registration (when wanted)

```json
{ "mcpServers": { "wordcraft": { "command": "C:\\Program Files\\WordCraft\\wordcraft-cli.exe", "args": ["mcp"] } } }
```
Confine with `--automation-read-root D:\Dev\repos\on-metacraft --automation-write-root D:\Dev\repos\temp` for agent passes.

Next: tracked-change docx pass on preface with `--author`, then `convert --markup` back and diff.

## Tracked-change proof 2026-10-15 (done)

- `run --file temp/00-preface-review.docx --author "Muse Spark" --cmd review.trackChanges=true --cmd review.newComment="pilot..." --save` OK.
- `info` -> comments 1, trackChanges true, lastModifiedBy Muse Spark, revision 2, 470 words, 2pp.
- `convert --markup -> temp/00-preface-review-markup.md` OK, Comments section carries `1. **Muse Spark** on "Preface": pilot...`.
- Artifacts stay in `temp/` (`00-preface-review.docx`, `00-preface-review-markup.md`). Book repo untouched.
