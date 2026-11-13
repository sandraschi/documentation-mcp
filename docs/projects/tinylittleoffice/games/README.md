# Two mini-games, no backend

Both are plain `.tlo` files. No build, no account, no dice server. The link holds
the whole game state — rolls and crumbs included — once you stop typing.

| Game | File | App | Players | Time | Needs |
|------|------|-----|---------|------|-------|
| The Night Bakery | [night-bakery.tlo](./night-bakery.tlo) | deck (gamebook) | 1, or 1 reader + room | ~10 min | nothing |
| Starfreight | [starfreight.tlo](./starfreight.tlo) | write + embedded sheet | 1 pilot | ~15 min | 1d6 (phone dice fine) |

## Play in 30 seconds

1. Open https://tinylittleoffice.com/deck/ (Bakery) or `/write/` (Starfreight).
2. Drag the `.tlo` file onto the page. It opens. (Or: `npx tinylittleoffice link deck night-bakery.tlo` → link.)
3. Play. The address bar *is* your save file — copy it to keep this exact run.

Present mode: deck `Present` button (Bakery reads great on a TV).
Print/PDF: Download menu — both games were written to survive paper.
Display Link (`?d`): read-only table copy for the room.

## 1. The Night Bakery (deck gamebook)

Slides are rooms; slide numbers are page numbers. Foyer (slide 3) branches to Oven
(slide 4), Loft (slide 5), Counter (slide 6); Counter's embedded sheet adds your
crumbs (`=SUM`) and routes to the Dawn Loaf or the Soggy Bottom. `qr: no` in the
head suppresses the closing QR slide so the room can't read ahead — stolen from the
trivia template.

Remix hooks: change the crumb math, add a slide 9 monster, swap the theme
(`chalkboard` → `midnight` for horror, `confetti` for kids). Keep slides short —
one slide shows one thing, bullets under a chart/table are not drawn (put them in
`> ` notes, like this game does).

## 2. Starfreight (write + sheet, formulas do the dealing)

A 5-leg freight run. You roll 1d6 per leg into `Roll`; `Profit` is pure kernel
formulas — no code, no macros:

```
=IF(E1>D1, C1-B1, 0-B1)      # beat Risk → Fee minus Fuel, else lose Fuel
=SUM(F1:F5)                  # Total profit, works itself out
=COUNTIF(G1:G5, "x")         # stars, where G = =IF(F1>0, "x", "")
```

Why this shape: sheet is one table, but wrapped in a *write* doc so instructions,
checklists, and footnotes travel with the playable table — and the table still
evaluates in place (kernel §5: `evaluate` takes any doc + block index). Same pattern
fits invoices, test matrices, habit trackers, any "words around a live table" game.

House rules in the file: veterans fly Risk+1, rookies reroll one leg. Perfect run
nets 170. A brave disaster nets a story.

## Design notes (what the constraints forced)

* **No RNG, no state, no code** — so: gamebook branching (player as CPU), analog dice
  (player as RNG), formulas as dealer (`IF/SUM/COUNTIF` only — single-level `IF`,
  `COUNTIF` on `"x"` markers, the two patterns proven by upstream samples).
* **Link-length budget** — both games stay far under the 2048-char meter even packed;
  they also work as plain `#doc=` links for hand-editing.
* **History leaks state** — browser history holds every pause (~15 s flush), so
  "secret" game state isn't secret. Neither game has any. (A hidden-traitor game
  would need sealed `E` payloads + out-of-band passwords — left as an exercise.)
* **Sharing = forking** — every link is a copy. Perfect for game receipts and
  remixes; don't design "shared board" games on this substrate.

## Try next

* Sealed traitor game: roles as `E` payloads, passwords read aloud, one sealed
  `locked` fence per player (` ```locked ` holds a link fragment, drawn as a card
  until its password lands in an editor).
* Calendar campaign log: `cal` spans per session + gantt `done=%`, linked from the
  game docs.
* Anim flipbook: 8-frame walk cycle over a draw sprite (`Pip the frog` pattern in
  `draw/templates.md`) as a loading-screen toy.
