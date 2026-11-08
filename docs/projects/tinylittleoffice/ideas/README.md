# Ideas, implemented as templates (no code)

Six of the twelve [EXTENDING.md](../EXTENDING.md) backlog items, built as plain
`.tlo` files. No new app code — each proves its shape fits the kernel before anyone
builds an editor for it. Open by dragging onto the site (Tier 0,
[TEST-HOSTING.md](../TEST-HOSTING.md)).

| File | Backlog # | App | What proves what |
|------|-----------|-----|------------------|
| [kanban.tlo](./kanban.tlo) | 1 | outline | Lanes as nested items, `statuses:` head + `{status=}` + `{due=}`, edges between lanes |
| [rfc.tlo](./rfc.tlo) | 2 | write + sheet | Words around a live scoring table; arithmetic re-scores when numbers change |
| [runbook.tlo](./runbook.tlo) | 3 | write + cal | Checklists + embedded timeline; calendar fence keeps its own head (`zone:`, colors) |
| [api-sketch.tlo](./api-sketch.tlo) | 4 | write + sheet | Contract as rows; open questions as tasks; lint-shaped rules listed, not enforced yet |
| [json-playground.tlo](./json-playground.tlo) | 5 | write + json fence | `json` fence is text-kept-as-written: paste `toJson` output, predict `fromJson` |
| [testplan.tlo](./testplan.tlo) | 10 | write + sheet | `Expect` locked, `Result` typed, `=IF(D1=C1,"x","")` per row + `=COUNTIF` total |

Patterns reused (all single-level `IF`, all `COUNTIF` on `"x"` markers — the two
formula shapes upstream samples prove): Starfreight in [games/](../games/README.md)
is the same engine with dice.

Next to build (still templates first): regex/cron explainer (calc tape + lint
vocabulary), JWT decoder (in-memory only, never seal a demo token into a link),
log viewer (last-200-lines + `lock:` parsed columns), invoice++ (`due:`/`paid:` +
`xlsx` export), flashcards (deck `steps()` reveal), changelog (cal spans + MD export).
