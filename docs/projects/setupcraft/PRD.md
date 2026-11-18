# SetupCraft PRD

Status 16 November 2026. The preparation guide, the package writer, and the Wizard of Crafts are in code. The wizard records one founder. Writing into each craft database is not built.

## Read, then type your own company

The founder reads `setupcraft prepare`. That text is the same for every small company. It covers:

- GmbH: at least 35,000 euro subscribed, at least half and at least 17,500 euro paid in. More is allowed.
- Gruendungsprivilegierung: at least 10,000 euro raised and below 35,000, at least half and at least 5,000 paid in, for ten years from the founding date.
- FlexKapG: at least 10,000 euro subscribed and at least 5,000 paid in, as a permanent minimum.
- There is no Austrian UG.
- Notar, Firmenbuch, bank confirmation, the GSVG/ASVG question for a shareholder-director, employees versus advisors, and the filings this program does not send.

`setupcraft template` writes a live skeleton (Graz, placeholder UID, acknowledgement false). `setupcraft acknowledge` records that the guide was read. `apply` still refuses the skeleton until the UID and the other fields are the founder's own. sandrasteve GmbH stays a demo and still needs `--accept-demo`.

Any Austrian seat is accepted. A Wien seat keeps PLZ 1010-1230. The court is whatever the founder types, because it follows the seat.

## What it is

One dossier for one small Austrian GmbH or FlexKapG on one PC. `%LOCALAPPDATA%\craft-biz\company\dossier.json` is the intended live path. v0.1.0 writes whatever directory the CLI is given.

`craft-biz::company` validates the dossier, builds a fingerprint, and renders one file per craft. SetupCraft's CLI is the writer. A demo dossier (`vendor: demo`) is refused unless the caller passes `--accept-demo`.

Fingerprint shape:

```text
fn=123456a|uid=ATU13585627|employees=2|iban_tail=3201|cards_complete=2|vendor=demo
```

`employees` counts Arbeitnehmer and a Geschaeftsfuehrer who draws an ASVG wage. Shareholders without a wage, and advisors, are not in that count.

## What v0.1.0 writes

- `dossier.json` and `fingerprint.txt`
- `buchcraft\opening.json`: debit 2800 Bank, credit 9000 Kapital, for the paid-in amount. Unpaid capital is a number on the file and is not posted. The EKR seed has no Ausstehende Einlagen account. A George CSV path suppresses the lines.
- `teamcraft\employees.json`: Mitarbeiterkarte per team member. Complete when photo, SVNR, address, hire date, position, and current-work text are present. Founding cards must be complete. A `source: hirecraft` card may list gaps. Monthly gross is stored. No tax is calculated.
- `billcraft\seller.json`: Firma, FN, court, UID, address, IBAN, logo.
- `contractcraft\drafts.json`: one employment draft per team member, one mandate per advisor. A missing Auftragsverarbeitungsvertrag is `missing_avv: true`.
- `taskcraft\tasks.json`: SV-Anmeldung, first UVA (day 15, two months after founding), send the Beraterpaket. Nothing is submitted.
- `assetcraft\machine.json`: this PC.
- `wikicraft\handbook.md`, `impressum.txt`, `advisors.json`
- `deskcraft\profile.json` with SMTP off
- `gaincraft\vendor.json` with no customers
- `formcraft\contact.json` with `serve: false`
- `spendcraft\policy.json`
- `helmcraft\cockpit.json`: paid-in capital, headcount, complete cards, open tasks
- `beraterpaket\index.txt`

Wien uses PLZ 1010-1230. Any other Austrian seat uses a 4-digit PLZ and the court the founder enters. UID and IBAN use the checksums in `craft-biz`. SVNR uses the 10-digit check and must match the birth date. Firmenbuchnummer is a shape check (digits plus one letter), not a court lookup. Legal form is `GmbH` or `FlexKapG`.

Capital is a floor, not a fixed sum. Full GmbH: subscribed at least 3,500,000 cents, paid at least half and at least 1,750,000 cents. Privileged GmbH: subscribed at least 1,000,000 and below 3,500,000 cents, paid at least half and at least 500,000 cents, privilege end date ten years after founding. FlexKapG: subscribed at least 1,000,000 cents, paid at least 500,000 cents. The sandrasteve demo uses the privileged minimum.

## People

Four kinds. An advisor never becomes an employee.

- Gesellschafter, with a share count
- Geschaeftsfuehrer, with or without an ASVG wage. Without a wage there is no TeamCraft card and no later payroll
- Arbeitnehmer, the Mitarbeiterkarte
- Externe: bookkeeping, advisor, notary, lawyer, bank, insurance

Founding people have `source: onboarding`. Later hires have `source: hirecraft` and a candidate id. HireCraft still shows candidates, not employee cards. TeamCraft does not yet read `employees.json`.

## Where people are entered

- The dossier and `demo-write` hold the founding batch. sandrasteve has two complete cards: Alex Berger (Geschaeftsfuehrung) and Sam Hofer (Entwickler). Each card has personal data, a photo file name, hire date, position, department, and a current-work description. Monthly gross is stored. No tax is calculated.
- The wizard collects that same card for the founder only, then `people.truncate(1)`. Adding the rest of the current staff in the window is the next wizard step.
- A Geschaeftsfuehrer without an ASVG wage is not a TeamCraft card (`is_team_member`).
- After go-live, a new person starts in HireCraft. The hire event still lacks start date, position, and work text, and TeamCraft still drops the wage. When that path is built, TeamCraft opens an incomplete card until photo, SVNR, and address are filled.
- The detail page for every card is a TeamCraft view that reads `employees.json`. It is not built. SetupCraft does not become the HR file after onboarding.
- Lohnverrechnung is a later `lohncraft`. It reads a complete card and a locked TeamCraft month. ELDA and FinanzOnline stay with the Buchhaltungsfirma.

## Not built

- Wizard steps for the rest of the founding batch (the window keeps the founder only)
- Installer and pinned craft binaries
- `company.apply` inside BuchCraft, TeamCraft, BillCraft, and the other databases
- Face boxes stored as image crops. The dossier names the portrait file. The CEO still assigns the file. There is no face recognition
- A second PC
- Lohnverrechnung. A later `lohncraft` reads a complete card and a locked TeamCraft month. ELDA and FinanzOnline stay with the Buchhaltungsfirma
- Filing with the Firmenbuch

## Acceptance already covered

- sandrasteve validates, the opening entry balances, advisors are absent from the employee file, a photo-less founding card is rejected, a UID change moves the fingerprint, a second write changes nothing, a silent demo write fails.
- Tests: `cargo test -p craft-biz --lib company` and `cargo test --manifest-path D:\Dev\repos\setupcraft\Cargo.toml`.
