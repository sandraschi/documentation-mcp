---
title: "Documentation sites, explained plainly: what we have, what is broken, and whether the article is worth copying"
category: guide
status: active
audience: end-users, mcp-dev
last_updated: 2026-10-31
last_verified: 2026-10-31
review_every_days: 90
sources:
  - https://tangled.org/blog/docs/
  - https://pandoc.org/MANUAL.html
  - https://www.mkdocs.org/
  - https://docusaurus.io/
# status: active -- every number below was measured on this machine on 2026-10-31 and
# the commands used are at the bottom, so anyone can re-run them. The recommendation
# half is judgement, and it is labelled as such.
---

# Documentation sites, explained plainly

## The short version

Someone at a software project called Tangled wrote a blog post saying you do not need a paid
documentation service. You can point a free tool called pandoc at a pile of plain text files and get
a small website out, with no JavaScript and no monthly bill.

That is true, for them. I checked whether it is true for us. Almost none of their setup applies to
this fleet, and copying it would lose things we actually use.

But the check turned up something more useful than the article did:

> Four of our five documentation sites have menus where most of the links point at pages that no
> longer exist. None of the five is ever built by anything.

That is worth fixing regardless of which tool we use.

## Six words that make this confusing

| Word | What it means here |
|---|---|
| Markdown | A plain text file with simple markings for bold, lists and links. File name ends in `.md`. |
| Documentation site | A folder of Markdown files turned into a browsable website. |
| Static site generator | The program that does the turning. It reads the files and writes HTML pages. |
| nav (menu) | A list, written by hand in a settings file, saying which page sits under which heading. |
| MkDocs | A static site generator for documentation. "Material" is its most popular theme. |
| Docusaurus | A different generator, built with React. Heavier, aimed at bigger sites. |

The key detail is the word **nav**. The menu is written by hand, separately from the pages. When
someone moves or renames a page, the menu keeps pointing at the old path. Nothing breaks loudly, so
nobody notices. The article's whole argument is about avoiding that.

## What the article says

1. Roll your own using pandoc instead of paying for Mintlify or shipping a React app.
2. Feed pandoc one big Markdown file. Its `chunkedhtml` output cuts that file into one web page per
   heading, and builds the menu out of the headings themselves.
3. Because the menu is derived from the pages, it cannot point at a page that does not exist.
4. For search, use your browser's Find, plus a second copy of the same documentation rendered as one
   long page. The mobile menu needs no JavaScript because of a built-in browser feature called
   `popover`.

Point 3 is the useful idea. Points 1, 2 and 4 are one person's taste, and they say so themselves.

## What we actually have

Measured on 2026-10-31 across `D:\Dev\repos`. "Menu resolves" means: take every page path written in
the settings file, check whether that file exists on disk.

| Repository | Tool | Markdown pages | Menu resolves |
|---|---|---|---|
| `rtorrent-mcp` | MkDocs Material | 43 | **0 of 19** |
| `handbrake-mcp` | MkDocs Material | 82 | 2 of 17 |
| `mcp-studio` | MkDocs Material | 103 | 4 of 17 |
| `virtualization-mcp` | MkDocs Material | 151 | 7 of 14 |
| `blender-mcp/docs/docsviewer` | MkDocs Material | 6 | 39 of 46 |
| `multi-gpu-cluster-recipes/website` | Docusaurus | **0** | no pages at all |

Three further facts:

- **Nothing builds them.** No GitHub workflow in any of those repositories mentions MkDocs or
  Docusaurus, and no built `site/` output folder exists in any of them.
- **`rtorrent-mcp` is the worst case.** Its `docs/` folder holds flat files named `TOOLS.md`,
  `ARCHITECTURE.md`, `ONBOARDING.md`. Its menu points at `about/changelog.md`,
  `developer-guide/api-reference.md` and seventeen other paths that do not exist. The pages were
  reorganised and the settings file was never updated.
- **The Docusaurus site is empty.** `multi-gpu-cluster-recipes/website` contains six files and zero
  documentation pages, and it still holds port 11136 in that repository's `fleet-start.config.ps1`.

What MkDocs does with a menu entry that points at a missing file: it prints a warning, builds the
site anyway, and leaves a dead link in the menu. Add `--strict` and the build refuses. So "broken"
here means "silently ships dead links", not "crashes".

## Two things I got wrong first

Worth recording, because both are easy to repeat:

- Five repositories (`on-hyperart`, `on-ai-takeover`, `on-metacraft`, `on-hyperwar`, `on-hypermind`)
  contain a `book.toml`. That is the standard file name for **mdBook**, and I initially counted them
  as mdBook sites. They are not. They use `bookkit`, our own book tool, which happens to reuse the
  file name. Different pipeline, not a documentation site.
- `annoyinator` and `myai` contain `_sidebar.md` files, which is the Docsify convention. No Docsify
  is installed anywhere in the fleet. Those are leftovers from an abandoned tool.

## Why we cannot simply copy the article

The article's premise is "a collection of pages containing just text". Four of our five sites are not
that:

- **`mkdocstrings`** generates reference pages by reading the Python source and its docstrings. Pandoc
  does not read Python, so those pages would simply not exist.
- **`git-committers`** and **`git-revision-date-localized`** put the author and last-changed date on
  every page.
- **`handbrake-mcp`** runs a custom Python macro (`docs/hooks.py`) at build time.

That is a real feature set. Swapping it for pandoc would not be a simplification, it would be a
downgrade to a working-but-poorer site. The honest options are: fix the settings files, or delete
the documentation sites and keep the Markdown as files.

## Can mcp-central-docs profit from it? Yes, but not by building a website

First, the size of the thing you asked about, measured as Git sees it:

| Folder | Markdown files | What it is |
|---|---|---|
| `not-mcp-related/` | 3,885 | Notes, vendored articles, third-party material. Largely not ours. |
| `projects/` | 1,478 | Per-repository mirrors of each repo's own docs. |
| `integrations/` | 270 | Third-party service guides. |
| `standards/` | 174 | The rules. |
| `operations/` | 163 | Fleet state, ports, session logs. |
| `patterns/` | 113 | Step-by-step procedures. |
| all of `mcp-central-docs` | **3,506** | 28 MB. 8,426 if you also count ignored and hidden junk. |

A website would not help here, and the article's own method would actively fail: their trick is to
concatenate everything into one file, which at 28 MB produces a document nobody can open.

The profit is in the article's *reasoning*, not its tool:

**Their complaint:** a hand-written menu goes stale, because nothing forces it to match reality.

**Our version of that complaint, which is measurably true right now:**

- `standards/AGENT_READING_ORDER.md` is hand-kept. Its Primary Read List names 13 of the 174 files
  in `standards/`, and the page as a whole references 47 distinct filenames, so 127 of the 174 are
  never mentioned anywhere on it. That page is the front door to 174 documents.
- The generated "Fleet context" block in `AGENTS.md` states "There are **124** files under
  `standards/`". The real number is **174**. Even a generated artefact went stale, because it was
  generated once, committed, and never re-run.

**So the thing worth taking is:** make the index a build output, with a dated snapshot and a
freshness check, instead of a paragraph somebody edits by hand. We already do exactly this for the
guides folder - `scripts/guide_freshness.py` re-checks every guide against its sources and reports
which ones have expired. The same pattern applied to `standards/` would produce a table of path,
title, status and last-updated date, regenerated on demand, impossible to drift.

One script. No website, no JavaScript, no pandoc.

## What this does not fix

Being honest about the boundary:

- It does not make 3,506 files easier to read. Curation is a separate job.
- Much of that number is not documentation at all. `not-mcp-related/` (3,885 including ignored junk)
  and `projects/` (1,478 mirror copies) are the bulk. Deciding what is publishable is a human
  decision, not a tooling one.
- Our freshness checker (`scripts/audit-doc-freshness.ps1`) only scans `docs/`, which is 53 files out
  of 3,506. The audit tooling covers roughly one and a half percent of the corpus.

## If we ever do publish a site

Two ideas from the article are worth stealing, and both are free:

1. The mobile menu with `<button popovertarget>` and a `popover` div. No JavaScript, and clicking
   outside closes it.
2. Render the same source twice: once as separate pages, once as a single long page. The long page
   makes the browser's Find work across the whole documentation, which is what people actually use.

And one thing not to copy: the single concatenated file, for the size reason above.

## What to do next, cheapest first

1. **`rtorrent-mcp`** - the menu is 100 percent dead. Rebuild it from the real files, or delete
   `mkdocs.yml`. Deleting costs nothing because nothing builds it.
2. **`multi-gpu-cluster-recipes/website`** - an empty Docusaurus folder holding port 11136. Either
   put pages in it or reclaim the port.
3. **`handbrake-mcp`, `mcp-studio`, `virtualization-mcp`** - decide whether the generated API
   reference is wanted. If yes, the settings files need rebuilding from the actual tree. If no, the
   article's approach becomes genuinely reasonable.
4. **`mcp-central-docs`** - pilot run on 2026-10-31: `scripts/standards_index.py` generates the
   index for `standards/` from the files themselves. Measured: 174 files, 163 with frontmatter, 11
   without, 47 referenced by the hand-kept reading order, 10 not updated in over 180 days. Report at
   `reports/standards-index-pilot.md` (gitignored). Next decision is not technical: adopt the
   generated index or keep the hand list, and whether to date the 11 undocumented files.

## How the numbers were taken

```powershell
# find every documentation-site config in the fleet
fd -t f -i '^mkdocs\.ya?ml$' D:\Dev\repos -E node_modules -E .venv -E _upstream -E _archives -E external
fd -t f -i '^docusaurus\.config\.[jt]sx?$' D:\Dev\repos

# count markdown as Git sees it
fd -e md -t f . D:\Dev\repos\mcp-central-docs | Measure-Object

# does each menu entry point at a real file?
# extract "<name>: path.md" lines from mkdocs.yml, test each against the docs folder
```

The menu check compared each path in the `nav:` block against the repository's docs folder. Paths
starting `../` were counted as unresolved, because MkDocs does not read outside its documentation
folder.

## What this page does not claim

- It is not a benchmark of MkDocs, Docusaurus or pandoc. Only our configuration of them was tested.
- It does not say the article is wrong. For a project with plain text pages and no API reference,
  its approach is reasonable and cheap.
- It does not say the broken menus matter to users. Nothing publishes these sites today, so no
  reader has been harmed. The cost is that the documentation work already done goes unread.
