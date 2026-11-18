---
updated: 2026-11-16T18:55:00+01:00
agent: cursor
status: package-writer
tags: [setupcraft, craft-biz, sandrasteve, dossier]
---

# Handover - SetupCraft

## What is real

- `d:\Dev\repos\craft-biz\crates\craft-biz\src\company.rs` validates a Wien GmbH dossier, fingerprints it, and renders the onboarding package. Nine unit tests.
- The window is the Wizard of Crafts (`wizard`). `prepare` still prints the same guide.
- `d:\Dev\repos\craft-biz\crates\craft-biz\src\advice.rs` is the Gruendung guide. `prepare` prints it. A live company is written only after `acknowledge`. `template` is a Graz skeleton with a placeholder UID.
- Capital is a statutory floor, not a fixed sum. GmbH, gruendungsprivilegierte GmbH (ten years), and FlexKapG. Any Austrian seat. Wien keeps PLZ 1010-1230.
- The wizard writes one founder card (photo, personal data, hire date, position, current work, gross) and drops everyone after that person.
- `demo-write --accept-demo` keeps the founding batch: Alex Berger and Sam Hofer, both source `onboarding`, plus advisors. Cards are complete in that file.
- Clippy `-D warnings` is clean on `craft-biz` lib after the collapsible-if fix, and on setupcraft.

## What was deliberately not done

- The wizard does not yet collect the rest of the founding batch.
- No installer, no NSIS.
- No craft database is updated. BuchCraft, TeamCraft, and BillCraft do not import the package yet. TeamCraft has no Mitarbeiterkarte page.
- HireCraft's `candidate.hired` payload is unchanged. It still omits position, start date, and work text, and TeamCraft still drops the wage. HireCraft has candidate panes, not employee cards.
- No Lohnverrechnung, no ELDA, no FinanzOnline, no Firmenbuch lookup. Payroll waits on a later `lohncraft`.
- The repo is not committed and not pushed.
- `mcp-central-docs\projects\craft-fleet-expansion\BACKOFFICE_CRAFT_SUITE.md` was not edited. Its 12 November note that TeamCraft and AssetCraft ignore `candidate.hired` is stale: both drain that event. This package does not go through that bus.

## Next step

1. A wizard step that adds every current employee, with the same card fields as the founder, source `onboarding`.
2. A TeamCraft detail page that reads `teamcraft\employees.json` (photo, personal data, hire date, position, current work).
3. `company.apply` in BuchCraft for the opening lines (Storno if a second apply would post them again) and in BillCraft for the seller block.
4. A richer `candidate.hired` for people hired after go-live. `lohncraft` stays after the cards are on screen.

## Prove

```powershell
cargo test -p craft-biz --lib company --manifest-path D:\Dev\repos\craft-biz\Cargo.toml
cargo test --manifest-path D:\Dev\repos\setupcraft\Cargo.toml
cargo run --manifest-path D:\Dev\repos\setupcraft\Cargo.toml -- demo-write --out $env:TEMP\sandrasteve --accept-demo
```
