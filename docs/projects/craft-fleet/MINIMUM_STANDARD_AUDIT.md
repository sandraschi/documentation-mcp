# Minimum-standard audit — all craft apps (2026-11-05)

**Question:** are all craft apps at minimum standard — README stack, helpful
help, clear today-vs-next-week, PRD, CHANGELOG, KIBITZ, docs, tests, mini CLI?
**Answer: no. Zero of 25 meet the full standard.** The gap is documentation
and gates, not engines — and part of the bad news is my own triage error
(corrected §4).

## 1. The standard (9 items)

| # | Item | Bar |
|---|---|---|
| R | README | states what exists |
| CLI | mini CLI | `--help`/`--version` work (spot-run, rest wired-by-inspection) |
| T | tests | test fns exist in-repo (content-verified, NOT name-globbed) |
| P | PRD | root or `docs/PRD.md` |
| C | CHANGELOG | exists |
| H | help | `HELP.md` (uniform agent surface; CLI `--help` alone is not enough) |
| S | status block | README says DOES-TODAY / NEXT-WEEK / NON-GOALS explicitly |
| K | KIBITZ | review notes carried (SHOULD — history, not gate) |
| J | justfile | one-command CI entry |

## 2. Matrix (measured, content-verified)

`T(n)` = test fns counted in source (excl. .venv/target/outbox). S = status
signals found (bar is an explicit block, so counts >0 still usually mean MISSING).

| Repo | R | H | P | C | K | D | T | J | CLI | S |
|---|---|---|---|---|---|---|---|---|---|---|
| travelcraft | Y | - | - | - | Y | - | Y(11) | - | Y | - |
| moneycraft | Y | Y | Y | - | Y | - | Y(2) | - | Y | - |
| djcraft | Y | - | - | - | Y | - | Y(3) | - | Y | - |
| modcraft | Y | - | - | - | Y | - | Y(2) | - | Y | - |
| writercraft | Y | - | - | - | Y | - | Y(1) | - | Y | - |
| qgiscraft | Y | Y | - | Y | - | Y(25) | Y(133) | Y | Y | - |
| codercraft | Y | Y | Y | - | Y | - | Y(7) | - | Y | - |
| databasecraft | Y | - | Y | Y | Y | Y | Y(17) | Y | Y | - |
| robotcraft | Y | - | - | - | Y | - | Y(2) | - | Y | - |
| appcraft | Y | - | - | - | Y | - | Y(3) | - | Y | - |
| gamecraft | Y | - | - | Y | Y | Y | Y(225) | Y | Y | - |
| bookcraft | Y | - | Y | Y | - | Y | Y(34) | Y | Y | - |
| sportscraft | Y | - | - | Y | Y | Y | Y(16) | Y | Y | - |
| containercraft | Y | - | - | - | - | - | Y(6) | Y | Y | - |
| gitcraft | Y | - | - | - | - | - | Y(7) | Y | Y | - |
| filecraft | Y | - | - | - | - | - | Y(8) | Y | Y | - |
| doccraft | Y | - | - | - | - | - | Y(5) | Y | Y | - |
| revecraft | Y | - | - | - | - | - | Y(7) | Y | Y | - |
| virtucraft | Y | - | - | - | - | - | Y(5) | Y | Y | - |
| speechcraft | Y | - | - | - | - | - | Y(20) | - | Y | - |
| splatcraft | Y | - | - | - | - | - | Y(16) | Y | Y | - |
| makercraft | Y | - | - | - | Y | - | Y(9) | - | Y | - |
| musiccraft | Y | - | Y | - | - | Y | - | - | - | plan-only |
| smallvideocraft | Y | - | Y | - | - | Y | - | - | - | plan-only |
| artcraft | upstream, out of scope |

Strict-9 pass rate: **0/25**. Engine-healthy (R+CLI+T): **23/25**
(reservations excluded). Docs-healthy (P+C+H+D): **0/25**.

## 3. Fix batches (concrete, no new repos)

- **S-block (status: today / next-week / non-goals): 22 READMEs — DONE
  2026-11-05.** Landed one uniform `Status` block per README (does-today
  with verified numbers, next-week from the repo's own plan, explicit
  non-goals), one commit per repo, all pushed. Reservations
  (music/smallvideo) carry plan-status instead; artcraft upstream
  untouched. S column above reflects the pre-block state.
- **HELP.md: 22 repos** (only money/qgis/coder have one). Uniform agent
  help surface; canonical skeleton once, fill per repo.
- **LICENSE + CONTRIBUTING + issue/PR templates: 24 repos — DONE
  2026-11-05.** Dual MIT/Apache-2.0 (matches every workspace manifest's
  `license = "MIT OR Apache-2.0"`; files copied byte-identical from
  sportscraft, the one repo that had them) + uniform CONTRIBUTING
  (contributor/issue/PR rules) + bug/feature templates + PR template.
  One commit per repo, all 24 pushed.
- **PRD: 20 repos.** C+→B Phase 1 covers 10; +10 more (qgis, game, sports,
  6 python, splat). qgis/game/sports are the embarrassing three — proven
  code, no PRD.
- **CHANGELOG: 20 repos.**
- **justfile: 10 repos** — exactly the C+ batch (C+→B Phase 2 owns it).
- **KIBITZ: 12 missing — SHOULD, lowest priority.** Reservations exempt.
- **Tests: extend thin ones** (writer 1, money/mod/robot 2, dj/app 3 fns)
  + wire `just ci` + actually RUN all suites (see §5).

## 4. Correction to prior claims (my error, owned)

Spokes for the Antigravity batch said "no test evidence at triage" and the
C+→B plan presumed greenfield tests. Both wrong — my file-glob (`tests/`
dirs + `*test*.rs` names + truncated listings) missed inline test fns.
travelcraft has 11, speechcraft 20, makercraft 9. The C+ grade STANDS
(scaffold + thin starter tests + no docs + no recipes is still C+), but
the justification changes, and C+→B Phase 3 becomes "extend to 3+ with
headless-fixture discipline", not "write first tests". Spokes get
corrected at the planned Phase 5 re-grade; this audit supersedes them
meanwhile. qgiscraft (133 fns) and gamecraft (225) were also understated.

## 5. Verification ledger (honest)

- RUN: `--help` spot 2/2 PASS (`bookcraft-cli 0.3.0`; containercraft 8-verb
  argparse). Existence sweep above: 25/25 repos, Test-Path + content grep.
- NOT RUN: full test suites, 0/25. The single most important unrun gate in
  the fleet — C+→B Phase 2 owns it. Any claim of "tests pass" before then
  is unverified.
- CLI column above = files present + clap/argparse wired by inspection,
  except the 2 spot-runs. Reservations (music/smallvideo) correctly show
  CLI:- — no code claimed.
