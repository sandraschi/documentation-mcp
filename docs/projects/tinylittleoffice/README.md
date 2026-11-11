# tinylittleoffice (aboard-io)

**Type:** Upstream reference — local-first office suite, not a fleet repo
**Upstream:** https://github.com/aboard-io/tinylittleoffice (MIT, Aboard)
**Local mirror (read-only):** `D:\Dev\repos\_upstream\tinylittleoffice`
**Status (2026-11-06):** 581 stars, 37 forks, 10 apps, 21 languages
**MCD:** this page · [TRICKS.md](./TRICKS.md) · [EXTENDING.md](./EXTENDING.md) · [games/](./games/README.md)

---

## One-line summary

A free office suite where **the document is the link**. No accounts, no server-side
documents. The whole doc lives compressed in the URL fragment (`#`), which browsers
never send anywhere. Copy the link = copy the doc. Whoever has the link has the doc.

---

## Why it matters to the fleet

1. **Reference implementation of fragment-only privacy.** No backend to breach,
   subpoena, or leak — there is nothing to leak but short-link ciphertext.
2. **Agent-native file format (TLO).** Markdown + tables + 8 block kinds, byte-stable
   round-trip (`write(parse(x)) === x`), JSON Schema, `lint`/`measure` without a browser.
3. **Copy-paste toolkit for tinylittle-somethings.** Codec, sealed docs, short links,
   plain hand-written links, `api.js` + CLI. See [TRICKS.md](./TRICKS.md).
4. **Gameable constraints.** No code execution, no fetches, no embeds — pure paper-like
   play. See [games/](./games/README.md) for two working proofs.

---

## The 10 apps

| App | Id | What a document is |
|-----|----|--------------------|
| Word Processor | `write` | Rich text, invoice template, tables evaluated in place |
| Outliner | `outline` | Nested list, tasks, statuses, due dates, edges |
| Presentation Builder | `deck` | Slides between `---`, two-column, charts, speaker notes, print formats (zine/booklet/poster/badges) |
| Spreadsheet | `sheet` | One table, formulas (`SUM IF AND OR COUNTIF …`), chart bar/line/pie/sankey, lock cells |
| Calculator | `calc` | Tape, one expression a line, `mode: graph` |
| Drawing Tool | `draw` | `Kind\|X\|Y\|W\|H\|Style\|Label` table in 8px units, or pixel-art paragraph |
| Diagram Maker | `diagram` | Lists + edges, `kind:` mind/family/org/lanes/timeline/venn/seating/net |
| Animator | `anim` | Drawing + `Shape\|Keys` table, frames/fps/loop |
| Calendar | `cal` | `- date: event` items, recurrence, `view: gantt` |
| Trip Planner | `trip` | `Place\|Lat\|Lon\|Note` table, route map |

Any app's doc embeds inside Write/Deck/Outline as a fence (```` ```sheet ```` etc.).
A sheet table inside Write or on a slide is evaluated in place.

---

## How a link works (60-second version)

```
https://tinylittleoffice.com/<app>/#/v1/<app>/<payload>
```

* `payload` = `y|z|r` + custom base64url (shortest of: deflate-with-frozen-dictionary,
  deflate, raw UTF-8). `~` for 62 (never `-`: mail clients break lines on hyphens).
  `+` every 300 chars for iMessage/Signal. Full spec: `src/kit/core/codec.ts`.
* **Sealed:** `E` + base64url(`salt16 | iv12 | AES-256-GCM(flag|bytes)`). Key =
  one HKDF-SHA256 pass over the NFKC password, salt random per password, info
  `"tinylittleoffice sealed v1"`. Passwords are app-made, 20 chars / 116 bits.
  `src/kit/share/crypt.ts`, `docs/crypto/password.md`.
* **Short link:** browser encrypts long link under a fresh 32 B key, POSTs ciphertext,
  key stays in `#key`. Service holds opaque bytes only. `docs/crypto/short-links.md`.
* **Plain link:** `<app>/#title=…&doc=<percent-encoded TLO>` — hand-writable, checked
  by nothing. `public/llms.txt` documents it for agents.

Full byte layouts + threat model: [TRICKS.md](./TRICKS.md).

---

## Run it

Upstream mirror is read-only. To play, use the live site or run your own copy:

```powershell
# live (no install)
# https://tinylittleoffice.com/write/  — pick a template, edit, copy the link

# local copy (Node 24+)
Set-Location D:\Dev\repos\_upstream\tinylittleoffice
npm install
npm run dev      # site at http://localhost:4178
npm test         # every test, Node + Chromium
npm run build    # shippable static site
```

Self-host (your Cloudflare or one Node + SQLite file): upstream `docs/self-host.md`,
`selfhost/` folder. Verify a deploy: `npm run verify-deploy -- <url> <commit>`.

Agent fast path (no clone): `npx tinylittleoffice shapes sheet`,
`npx tinylittleoffice example deck talk`, `npx tinylittleoffice try deck draft.tlo`,
`npx tinylittleoffice link deck talk.md`, plus `skill --into ~/.claude/skills`.

---

## Key files (in the mirror — read, don't edit)

| Question | File |
|----------|------|
| TLO format (what agents write) | `docs/tlo.md` + `public/llms.txt`, `/llms-full.txt`, `/llms/<app>.txt` |
| Kernel (model, ops, editor, formulas, fuzz) | `docs/kernel.md`, `src/doc/` |
| Link codec | `src/kit/core/codec.ts`, `src/kit/core/route.ts` |
| Passwords / short links | `docs/crypto/password.md`, `docs/crypto/short-links.md` |
| Threat model / network / deps | `docs/threat-model.md`, `docs/network.md`, `docs/dependencies.md` |
| App contract + registry | `src/kit/core/app.ts`, `src/kit/core/apps.ts` |
| Programmatic API + CLI | `src/api.ts`, `packages/doc/` (`tinylittleoffice` on npm) |
| Self-host / mirror / deploy | `docs/self-host.md`, `docs/mirror.md`, `selfhost/` |

`_upstream/` rule: mirrors are read-only. Report problems to the fleet repo that
depends on the mirror; refresh only via `scripts/refresh-upstream-mirrors.ps1`.

---

## What we added here

* [TRICKS.md](./TRICKS.md) — steal-this cookbook: 7 reusable patterns with byte
  layouts, minimal reimplementations, and what to copy for a tinylittle-something.
* [EXTENDING.md](./EXTENDING.md) — 11th-app recipe + 12 ranked dev-oriented expansions
  + hard constraints (what the design refuses: code exec, fetches, embeds).
* [TEST-HOSTING.md](./TEST-HOSTING.md) — test-host in 3 tiers (live site, local dev
  :4178, self-host :8000/:8001) without touching the read-only mirror.
* [games/](./games/README.md) — two playable, no-backend mini-games as plain `.tlo`
  files: a deck gamebook and a sheet trading game. Open the file, copy the link,
  play. No build, no account.
* [ideas/](./ideas/README.md) — six backlog ideas implemented as `.tlo` templates:
  kanban, RFC, runbook, API sketch, JSON playground, test plan.

---

## Change log

* **2026-11-06:** Project page + TRICKS + EXTENDING + 2 games (Night Bakery, Starfreight).
