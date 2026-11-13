# TeamCraft - Assessment

**Repo:** `D:\Dev\repos\teamcraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic data; legal rules not reviewed by a professional) - **Origin:** fleet-owned

## What it is

Working time and leave for a 1-10 person Austrian team with Arbeitszeitgesetz checks. Not payroll.
Third app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.3).
Shared kernel: `craft-biz` (new `holidays` module: 13 national public holidays, Easter computed, working-day count).

## Model / verbs

- **Crates:** `teamcraft-store` (SQLite WAL: employees, time entries, week locks, leave, adjustments, KV table, AZG finding log), `teamcraft-core` (`azg.rs` pure engine, timesheet, KV check, capacity, demo), `teamcraft-mcp` (`teamcraft` binary).
- **25 MCP tools / CLI verbs:** status, employee add/list/update, clock in/out, time add/list/delete, week confirm, azg check, violations, leave request/decide/cancel/list/balance/adjust, holidays, kv import/list/check, timesheet (CSV), capacity (emits `capacity.changed`), demo seed.

## Strengths

- AZG engine covers 10 h (warning), 12 h, 60 h/week, 48 h over 17 weeks, 30 min break above 6 h (gaps count), 11 h daily rest. Findings are recorded with minutes over/short; fixed data clears them but keeps the history.
- Confirmed weeks are locked in Rust and by SQLite triggers (tested by bypassing Rust).
- Sick leave carries no reason: refused in Rust and by a CHECK constraint. No SV number, address or bank data on employees.
- Leave in half-days counted against Austrian holidays; pro rata entitlement in the start year; overdraw needs `force`.
- KV table is user-imported (no figures shipped); demo KV is labelled fictional.
- First working cross-app link: `team capacity --emit` -> file bus -> `taskcraft inbox-drain` -> shown in `taskcraft status`. Verified live with release binaries.

## Gaps / risks

- No egui window; no employee self-service.
- AZG general rules only: no KV extensions (Gleitzeit, 4-day week), no ARG Sunday/night rules, no KJBG.
- Urlaubsgesetz first-6-months accrual and 30 days after 25 years not modelled; part-timers approximated on a 5-day basis.
- Timesheet is CSV only (PDF via pdfcraft not wired).
- Rules need a review by someone who does Austrian payroll/labour law before real use.

## Next 3 steps

1. egui app: clock panel, week view with AZG flags, leave calendar, approval inbox.
2. Labour-law review of the AZG thresholds and leave rules; add Gleitzeit as an opt-in profile.
3. democraft recipes (`team/azg-findings`, `team/week-lock`, `team/capacity-to-taskcraft`).

## Verdict

Grade C+: real, tested Tier 1 with the privacy and locking invariants enforced twice; needs a GUI and a professional rules review before anyone's working hours depend on it.
