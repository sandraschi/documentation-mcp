# DatabaseCraft — Assessment

**Repo:** `D:\Dev\repos\databasecraft` · **Date:** 2026-11-05 · **Grade: B+**

## What it is

Pure-Rust relational database, schema engine, and dynamic data-merge platform
for the Storytold ArtCraft ecosystem. The structural backbone: 10 domain
blueprints that AppCraft compiles into apps. Rebuild-PLAN pilot #2
(`dbcraft`): finish this repo, consolidate `database-operations-mcp`.

## Model / verbs

- **Model:** connection + schema + dump (DB as document).
- **Verbs (PLAN + CLI):** `status`, `query`, `schema-inspect`, `record-insert`,
  `export-merge`, `seed-demo`, `embed`, `semantic-search`, `commands`, `describe`, `mcp`.
- Decision recorded in PLAN: dir stays `databasecraft/`, binary ships as
  `dbcraft-cli.exe` — do not keep both names long-term.

## Architecture

Rust workspace (core/store/mcp/app), workspace-level clippy
`unwrap/expect/panic/unimplemented/todo` **all denied**, `justfile`, `docs/` (4),
`AGENTS.md`, `CHANGELOG.md`. Registered control-port reporting in `status`.
`databasecraft-cli` + `mcp` (Plane 1 headless / Plane 2 `--attach`) already exist.

## Strengths

- Strictest lint gate in the fleet (five denies) plus committed `Cargo.lock`.
- Real CLI surface today (query/schema/backup/seed/embed/search), not a verb list.
- Backbone role is load-bearing and correct: blueprints → AppCraft, persistence
  for robot/money/cad/dj/art crafts.

## Gaps / risks

- Credential handling: URLs with passwords must never hit logs/`run.json` — needs
  a redaction proof, not just intent.
- `databasecraft` vs `dbcraft` naming still dual — finish the alias decision.
- Postgres/MySQL paths need dockerized CI or explicit sqlite-only labeling.
- Democraft recipes named in PLAN (`queryardstick`, `backup-restore-roundtrip`,
  `schema-diff`) need to exist and stay green.

## Next 3 steps

1. Redaction test: password-bearing URL through every verb → assert redacted artifacts.
2. Settle the binary name (`dbcraft-cli.exe`) and document the alias once.
3. Land the 3 PLAN recipes and pin baselines (`data/craft_compat.json` discipline).

## Trifecta meta-blueprint (2026-11-05 decision — Stich generalises)

The beekeeper case generalises to an artisanal trifecta — SHOP (physical:
cash register, shelves kept stocked), WEBSHOP (orders, products,
storefront), PRODUCTION (facility: machine supervision + safety, raw
material restocking, + trade sensors). A baker is the same trifecta with a
different backroom. Legs compose; backrooms vary. ("Meta" here means
composition pattern, not supervisor — the parked metacraft is a different
conversation.)

- Each leg is a blueprint MODULE, not a new blueprint per trade. New trades
  add one production-backroom module; shop + webshop legs are shared. This
  is what keeps beekeeper #2 (baker) cheap after beekeeper #1.
- `small_business` audit (measured): customers / products / invoices /
  invoice_items / payments only — no POS shifts, no shelf levels, no
  webshop orders, no production tables. That delta IS the build list.
- Production leg is sold ONLY to artisanal/family outfits (scope rule —
  full facility supervision doesn't pay outside small producers).
- Pricing rule, no amounts set: legs required decide the price — 1/2/3-leg
  tiers, never per-feature counting.
- Trade sensors ingest into the production leg as telemetry tables +
  thresholds (hive temp, door cam stills, varroa treatment log + reminders
  — the mite work is a domain workflow, not just a reading). Hardware
  source, decided 2026-11-05: `devices-mcp` (PUBLIC, v2.4.0 beta — Tapo/USB
  cams for the door cam, plugs for machine power, Netatmo-class telemetry;
  LAN-configured, no cloud). Honest gap: in-hive interior probes are not
  covered yet — likely Shelly-class additions to devices-mcp, not a new
  craft.
- Amazon variant (Schraubinger & Neffe, screws and bolts, 2026-11-05):
  legs can be RENTED, not just built. Amazon is the shop AND the webshop
  (listings, cart, payment, traffic); the merchant keeps warehouse +
  dispatch (stock by bin, pick/pack/ship, returns). No production leg
  (traded goods) — the trifecta degrades gracefully to the legs that exist.
  New databasecraft work item: warehouse module (inventory locations, pick
  lists, shipments, returns, Amazon settlement import) — `small_business`
  has none of it. Pricing rule extends naturally: we charge for the legs
  we run (warehouse/dispatch system + Amazon account handling), not for
  Amazon's. Open: FBA vs merchant-fulfilled (customer states own warehouse,
  so FBM-first assumption; confirm), Amazon SP-API credentials (their
  account, token-gated like all cloud integrations), invoicing flow.

## Verdict

The load-bearing craft: strictest gates, real verbs, clear downstream consumers.
B+ — one redaction proof and three green recipes from A-.
