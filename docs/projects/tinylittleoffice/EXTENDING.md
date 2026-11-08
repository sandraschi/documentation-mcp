# Extending TinyLittleOffice — 11th-app recipe + dev backlog

Paths are in the read-only mirror `D:\Dev\repos\_upstream\tinylittleoffice`.
Contract: `src/kit/core/app.ts` (`AppDef`). Registry: `src/kit/core/apps.ts`.
Format: `docs/tlo.md`. Kernel: `docs/kernel.md`.

---

## Recipe: add an 11th app in ~10 steps

Copy `src/apps/sheet/` (smallest full citizen: `def.ts editor.ts view.ts model.ts
commands.ts templates.md templates.ts tests/ style.css`), rename to `src/apps/<id>/`.

1. **`def.ts` — the definition (no DOM).** `defineApp({ id, name, noun, group, icon,
   blurb, blank(), templates(), editor(), title(), retitle(), view(), exports?,
   handoffs?, commands?, text?, steps?, motion?, long? })`. See sheet's 75-line
   `def.ts` — that shape is the whole pattern. `title/retitle` = one `head` op.
   `view(doc, opts)` returns `Page[] { w, h, svg, alt }` and must honor
   `small/thumb/still/card/upTo/frame/open` (print, PDF, PNG, thumbnail, embed,
   slideshow depend on it).
2. **`model.ts` — read your domain from the kernel.** `parse(doc)` → work on
   `Doc { head, blocks }`. Tables via `tableAt/evaluate`, lists via outline helpers.
   Never invent a 9th block kind — map to the 8 (`h p li quote hr table fence edge`).
   Settings go in the head (`currency:`, `chart:`, `zone:` pattern).
3. **`editor.ts` — thin Lit wrapper around `<to-text>`.** Owns a span of blocks,
   emits `Op[]` (`head/splice/move/text/cells/rows/cols/col`), applies with `apply()`.
   Focus goes *in* your editor via `focusFirst()`. Undo/redo/history stay in the
   kernel — don't reimplement.
4. **`view.ts` — draw with the sheet/draw kit**, not raw SVG strings where avoidable
   (`kit/draw/*`, `raster.ts` for PNG). Long docs: set `long: true` so slides cut with
   "See more" instead of shrinking past reading. Moving docs: implement
   `motion()` + `view(doc, { still, frame })`.
5. **`templates.md + templates.ts`** — blank + everyday + advanced, each real data,
   each canonical (`write(parse(x)) === x`, held by `test/doc/corpus.test.ts`).
   These also become `packages/doc/examples/<app>.json` (via `scripts/make-skill.ts`)
   and the agent skill references.
6. **`commands.ts`** — bar, menus, context bars, keys, drawer search. Same module the
   editor imports, so home page carries none of it (lazy `commands()`).
7. **`lint.ts` (checker uses the renderer).** Return `Finding[] { app, at, block,
   kind, words, fix }` + `Measure`. Wire into `src/lint.ts` so
   `tinyoffice lint/measure/try` cover you. Fenced inner docs lint too.
8. **Register + convert.** Add to `ALL` in `src/kit/core/apps.ts` (order = home-page
   order). Add `handoffs` both ways (`Download > Open in`, `convert.ts` pure fns) and
   `takes()` if another app's docs convert into yours.
9. **i18n + budgets.** Names/blurbs through `t()` (21 languages in `src/i18n/`).
   Check `budgets.json` — registry + `/api.js` have size gates; keep defs light,
   lazy-import templates/editors.
10. **Tests.** Corpus byte-stability over every template; grammar properties
    (`test/doc/properties.test.ts`); paste properties if you accept paste; a walk
    (`test/browser/walks.test.ts`) if you add chrome interactions. Then
    `npm test`, `npm run build`, `npm run verify-deploy` thinking.

Done means: template opens, edits project into the link within ~15 s of pause,
Display Link reads, embed draws, PDF/PNG/MD/TLO/JSON + your formats download,
another app's doc embeds yours as a fence, lint names real problems.

## Hard constraints (the design says no — don't fight it)

* No new block kinds, no pictures/embeds from the web, no fetched content except
  behind an explicit switch (Trip map tiles pattern). `![alt](url)` stays link text.
* Never render user HTML/CSS/JS. (The sections app was removed for exactly this.)
* No backend per doc. Compute must be client-side + deterministic (formula engine,
  layout code). Secrets don't go in links unless sealed — and sealed still leaks
  length + app id.
* URL economy: stay under the 2048 meter; short links cap at 16 KB ciphertext;
  inflate cap 4 MB. If your domain is naturally big (logs, images), it doesn't fit —
  pick a summary-shaped app instead.
* Don't touch the frozen dictionary; don't add hosts outside `kit/core/network.ts`
  (CSP + `test/csp.test.ts` + `test/network.test.ts` will fail you, correctly).

## Dev-oriented backlog (ranked, all fit the constraints)

1. **Kanban** — Outline columns as lanes (`kind: board`), cards = items with
   `status:`/`due:`/`{done=%}` already in the kernel. Pure reorder ops. Fits perfectly.
2. **RFC / decision log** — Write template + `Status | Option | Cost | Risk` table,
   `IF/COUNTIF` scoring, Display Link as the readable spec. Zero new code.
3. **Runbook / incident** — Cal (timeline/gantt) + checklists + fenced sheet for
   numbers. `view: gantt` exists; add `sev:` head + lint ("every step has an owner").
4. **API sketch** — Table `Method | Path | Body | 200` + `lint` (route shape,
   `:` params, example bodies parse as JSON). Export OpenAPI-ish JSON via `exports`.
5. **JSON playground** — Fence lang `json`, pretty/canonicalize via kernel JSON
   (`toJson/fromJson`), lint names schema faults with paths. No execution needed.
6. **Regex / cron explainer** — Calc-tape-shaped: one pattern a line, lint explains
   tokens, measure shows catastrophic-backtracking risk heuristically. Pure text.
7. **JWT decoder (sealed demo)** — Paste parts, decode base64url client-side, show
   header/claims, warn on `alg: none`/expiry. Never seal the token itself in a demo
   link — keep it in-memory only, say so.
8. **Log viewer** — Paste lines → table (`Time | Level:option | Msg`), `COUNTIF` by
   level, `lock:` the parsed columns. Cap: big logs don't fit links — "last 200 lines"
   template + trim lint.
9. **Invoice++ / quote** — Write's invoice head fields + money table + `chart: bar`
   already exist; add `due:`/`paid:` lint and `xlsx/csv` exports. Smallest real money.
10. **Test plan** — Outline suites + sheet matrix (`Case | Steps | Expect | Result:option`),
    `COUNTIF(Result,"pass")/total` as pass rate, `lock:` expectations. Prints as booklet.
11. **Flashcards** — Deck where each slide = `Front | Back` + Anim for the flip;
    `steps()` reveals back second. Teacher-notes pattern from lesson template.
12. **Changelog / release notes** — Cal spans per version + Write summary; `measure`
    counts breaking changes (`!` conventional commits); export MD/JSON.

Each of 1–5 is a weekend; 6–12 are templates + lint before any editor work. Start
every one as `.tlo` files + `shapes/example` entries — only build an editor when the
docs prove the shape.
