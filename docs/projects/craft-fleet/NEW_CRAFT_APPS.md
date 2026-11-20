# New craft apps

**Date:** 2026-11-16
**Status:** Proposal. Four demos are local folders, not committed and not pushed: `horsecraft`, `bridgeclubcraft`, `philosophercraft`, `crochetcraft`. On 2026-11-16, `cargo test --workspace` and `cargo clippy --workspace --all-targets -- -D warnings` passed for each. `--smoke` passed for each. Horse hay for 520 kg is 8840 g. Four spades, not vulnerable, ten tricks, scores 420. The demo scarf is 36 stitches, 264 rows, 760 m.
**Owner:** Sandra S. + fleet agents

This file is the list of craft apps proposed on 2026-11-16. It is a proposal, not a status matrix. The hub matrix in `README.md` stays the list of apps that already exist.

Sizes below are Rust code after `cargo test` and clippy `-D warnings`. Seed texts, photos, and pattern libraries are extra. They are not in the line counts.

Measured siblings the same day (tokei, Rust code, `target` excluded):

| App | Rust code lines | What that size buys |
|---|---|---|
| formcraft | 2,121 | Thin back-office tool |
| sportscraft | 3,559 | Spectator tables plus a trainer |
| kittycraft | 4,639 | Cat advisor |
| puppycraft | 8,172 | Dog advisor |
| travelcraft | 10,553 | Offline guide |
| celcraft | 12,029 | Animation studio |

One agent-hour, on a sibling of an existing app, lands about 1,500 to 2,500 gated lines. A rules engine lands about 800 to 1,200. The hour is cargo, clippy, and the command bus. Typing is not the limit. A one-hour demo is one job, one preset, JSON on stdout, an MCP tool list, and `--smoke`. The full cuts below are later sessions.

Shared shape for every app in this list:

- L1 `{name}-core`: the domain and `dispatch`. No UI.
- L2 `{name}` binary: CLI subcommands plus a `mcp` subcommand. Stdout is JSON. MCP is JSON-RPC 2024-11-05 on stdio. Logs go to stderr.
- L3 `{name}-app`: egui window. `--smoke` exits 0 without a window.
- `#![forbid(unsafe_code)]`. Clippy denies `unwrap`, `expect`, `panic`, `todo`, `unimplemented`.
- No network port. No account system. Demo data is labeled demo.

## Already taken

Do not rebuild these. The proposals below sit beside them.

- Animal advisors: `kittycraft`, `puppycraft`. Horses are the open one.
- Sport: `sportscraft` is football tables and a personal trainer.
- Machine paths: `patterncraft` is plotter and CNC, not textile charts.
- Writing: `writercraft` is novels, screenplays, and papers.
- Employment time: `teamcraft` is AZG, leave, and wage floors. A Verein is not an employer.
- Ledger, invoices, stock, tasks, contracts, tickets, forms, wiki: the `craft-biz` suite.
- Animation, music, DJ, splat, GIS, home control, books, mail: the DIY catalog in `craft-showcase`.

## The four demos

These four demos are built. Each section is the demo that landed, then the later full cut.

### HorseCraft

- **Repo:** `D:\Dev\repos\horsecraft`
- **Kind:** hobby advisor, next to KittyCraft and PuppyCraft
- **Demo:** 8 breeds, hay at 17 g per kg of body weight per day, two care reminders, one diary line for a demo horse named Mira. Farrier and dentist intervals are reminders. Deworming is a fecal test, not a calendar.
- **Full cut:** about 8,000 lines, 4 to 5 agent-hours. Stable diary, photo log, Austrian keeping notes, farrier and vet history. A studbook and conformation scoring is a second version, nearer 16,000 lines.
- **Leave out:** veterinary diagnosis, drug doses, and a claim that the hay figure fits every horse.

### BridgeClubCraft

- **Repo:** `D:\Dev\repos\bridgeclubcraft`
- **Kind:** entertainment. SportsCraft stays football.
- **Demo:** seeded 52-card deal into North, East, South, West. Undoubled Chicago score. Chicago deals use this schedule: deal 1 neither side vulnerable, deals 2 and 3 the dealer's side vulnerable, deal 4 both sides vulnerable. Dealer rotates North, East, South, West. Part-score bonus 50. Game bonus 300 or 500. Small slam 500 or 750. Grand slam 1,000 or 1,500. Down 50 or 100 a trick. No doubles.
- **Full cut:** about 10,000 lines, 8 to 12 agent-hours. Members, partnerships, travelers, session results. A teaching table that checks a played card and walks SAYC is about 16,000. A bidder is a separate engine, about 20,000 lines on top, and it is not part of this proposal's first build.
- **Leave out:** doubles, redoubles, rubber bridge, and any claim of tournament clock timing.

### PhilosopherCraft

- **Repo:** `D:\Dev\repos\philosophercraft`
- **Kind:** advisor and study desk. WriterCraft stays the manuscript tool.
- **Demo:** 12 thinkers with one question and one claim each. A phrase checklist flags ad hominem, appeal to popularity, false dichotomy, slippery slope, and appeal to authority. The checklist matches phrases. It does not prove anything.
- **Full cut:** about 7,000 lines, 3 to 4 agent-hours. Argument cards, local notes, a reading list kept as markdown. A propositional proof checker is about 5,000 more. A debate mode is a thin chat over a corpus, about 2,000 lines of app code, and the quality is the reading list.
- **Leave out:** a finished history of philosophy, and any wording that calls the phrase list a fallacy detector with authority.

### CrochetCraft

- **Repo:** `D:\Dev\repos\crochetcraft`
- **Kind:** arty hobby. PatternCraft stays machine paths.
- **Demo:** integer gauge. Stitch count is `(span_mm * stitches_per_10cm + 50) / 100`, half-up. One scarf in US terms: 18 st and 22 rows per 10 cm, 200 mm wide, 1,200 mm long, 8 m of yarn per 100 sc. UK names for sc, hdc, dc, tr, dtr, ch, and sl st. A row counter.
- **Full cut:** about 7,000 lines for the project desk (gauge, stash, counter, written pattern, photos), 3 to 5 agent-hours. A symbol chart editor is about 16,000 and is the version that matches a charting program.
- **Leave out:** stitch-symbol fonts, PDF chart export, and a claim that 8 m per 100 sc fits every yarn.

## Business

### VereinCraft

- **Repo:** `vereincraft`
- **Kind:** business, Austrian association
- **Beside:** TeamCraft, which is employment law. This one is members.
- **Demo:** member list, a due in cents, one set of minutes, a vote tally.
- **Full cut:** about 10,000 lines, 6 to 8 agent-hours. Dues ledger, minutes, elections, a bus event toward BuchCraft for fees received.
- **Leave out:** ZVR filing, payroll, and a legal opinion on statutes.

### ShiftCraft

- **Repo:** `shiftcraft`
- **Kind:** business, duty rota
- **Beside:** TeamCraft stores the time record after the shift. This one builds the rota.
- **Demo:** one week, rest gap checked against a stated minimum, one posted record.
- **Full cut:** about 10,000 lines, 6 to 8 agent-hours. Rotas, rest gaps, export of time records to TeamCraft.
- **Leave out:** wages, AZG legal advice, and a hospital on-call model.

### GastroCraft

- **Repo:** `gastrocraft`
- **Kind:** business, small kitchen
- **Beside:** StockCraft and BuchCraft. This one costs a plate.
- **Demo:** one recipe, cost in cents from ingredient lines, the EU-14 allergen list as tags.
- **Full cut:** about 12,000 lines, 8 to 12 agent-hours. Recipe cost, allergen tags, a temperature log, links to stock and the ledger.
- **Leave out:** a Registrierkasse, HACCP certification, and nutrition claims.

## Hobby

### BeeCraft

- **Repo:** `beecraft`
- **Kind:** hobby
- **Demo:** one hive, a Varroa treatment window as a date span the user enters, a honey harvest in grams.
- **Full cut:** about 6,000 lines, 2 to 3 agent-hours. Hive diary, treatment windows, harvests.
- **Leave out:** a diagnosis of colony disease, and mite-treatment doses.

### GardenCraft

- **Repo:** `gardencraft`
- **Kind:** hobby
- **Demo:** a frost date the user types, one bed, a rotation note (same crop family not planted twice in a row).
- **Full cut:** about 8,000 lines, 3 to 4 agent-hours. Frost calendar, rotation, seed stock.
- **Leave out:** a live weather feed and pesticide advice.

### CellarCraft

- **Repo:** `cellarcraft`
- **Kind:** hobby, and a small Heuriger
- **Demo:** bottles with a drink-from year and a drink-until year, a count of what is ready in a given year.
- **Full cut:** about 6,000 lines, 2 to 3 agent-hours.
- **Leave out:** a point score presented as taste, and sales tax. Fees belong in BuchCraft.

## Advisor

### RepairCraft

- **Repo:** `repaircraft`
- **Kind:** advisor
- **Demo:** one appliance, a fault tree of about ten nodes, a parts list with no prices yet.
- **Full cut:** about 9,000 lines, 4 to 6 agent-hours. Fault trees, parts, a local manual shelf.
- **Leave out:** mains-voltage procedures and a claim of licensed repair.

### SkyCraft

- **Repo:** `skycraft`
- **Kind:** advisor, night sky
- **Demo:** a fixed observer latitude, planets and a few bright stars for one civil date, an observation log line. Positions can be a labeled low-precision demo for that date.
- **Full cut:** about 8,000 lines, 3 to 4 agent-hours. Tonight's sky for a saved place, plus the log.
- **Leave out:** telescope control and a name that collides with the video game.

HorseCraft and PhilosopherCraft are the other two advisors. They are in the demo section above.

## Entertainment

### QuizCraft

- **Repo:** `quizcraft`
- **Kind:** entertainment
- **Demo:** two teams, one question pack of ten, a timed score.
- **Full cut:** about 6,000 lines, 2 to 3 agent-hours. Host console, teams, packs the user edits.
- **Leave out:** a buzzer device driver in the demo. The full cut can add a keyboard buzzer.

BridgeClubCraft is the other entertainment app. It is in the demo section above.

## Arty

### WeaveCraft

- **Repo:** `weavecraft`
- **Kind:** arty. The drawdown is the product.
- **Demo:** one threading, one treadling, one tie-up, the drawdown grid as text.
- **Full cut:** about 12,000 lines, 6 to 8 agent-hours. Draft editor and cloth view.
- **Leave out:** a loom machine connection. PatternCraft remains the CNC path tool.

### CeramicCraft

- **Repo:** `ceramiccraft`
- **Kind:** arty, glaze math
- **Demo:** one glaze as oxide fractions that sum to 1.000 within a stated tolerance, a cone number, one test-tile note.
- **Full cut:** about 10,000 lines, 5 to 7 agent-hours. Unity formula, cone, test tiles.
- **Leave out:** kiln firing schedules presented as safe for a specific kiln, and any hazardous-material procedure.

### StageCraft

- **Repo:** `stagecraft`
- **Kind:** arty, performance
- **Demo:** a cue list of ten cues, a lighting plot with channels, a run-of-show order.
- **Full cut:** about 9,000 lines, 4 to 6 agent-hours.
- **Leave out:** a lighting console protocol in the demo. The full cut can add one documented protocol.

CrochetCraft is the other arty app. It is in the demo section above.

## Order after the four demos

1. QuizCraft. Smallest remaining app, and it is easy to show.
2. BeeCraft and CellarCraft. Logs with one calculation each.
3. WeaveCraft. The drawdown is original math and it does not need a corpus.
4. VereinCraft. Real Austrian gap beside TeamCraft.
5. ShiftCraft, GardenCraft, SkyCraft, RepairCraft.
6. GastroCraft, CeramicCraft, StageCraft.
7. Full cuts of the four demos, in this order: HorseCraft, CrochetCraft project desk, PhilosopherCraft reading desk, BridgeClubCraft club desk.

## Hours

| App | Demo session | Full cut in the sizes above |
|---|---|---|
| HorseCraft | 1 | 4 to 5 hours |
| BridgeClubCraft | 1 | 8 to 12 hours |
| PhilosopherCraft | 1 | 3 to 4 hours |
| CrochetCraft | 1 | 3 to 5 hours |
| QuizCraft | 1 | 2 to 3 hours |
| BeeCraft | 1 | 2 to 3 hours |
| CellarCraft | 1 | 2 to 3 hours |
| GardenCraft | 1 | 3 to 4 hours |
| SkyCraft | 1 | 3 to 4 hours |
| RepairCraft | 1 | 4 to 6 hours |
| StageCraft | 1 | 4 to 6 hours |
| CeramicCraft | 1 | 5 to 7 hours |
| VereinCraft | 1 | 6 to 8 hours |
| ShiftCraft | 1 | 6 to 8 hours |
| WeaveCraft | 1 to 2 | 6 to 8 hours |
| GastroCraft | 1 | 8 to 12 hours |

The four demos in sequence are about four agent-hours. The four full cuts are about 20 to 25 agent-hours. The whole list of full cuts is about 70 to 90 agent-hours.

## Not on this list

Medical diagnosis, a law practice tool, and payroll stay off the list. BuchCraft already owns the ledger. TeamCraft already owns employment time. A second bookkeeping app would split the suite.
