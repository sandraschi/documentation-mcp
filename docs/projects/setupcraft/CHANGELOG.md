# Changelog

## Unreleased - 2026-11-17

- Wizard page Team records the founding batch. Each card has photo, personal data, hire date, position, and current work, source `onboarding`. The sandrasteve draft keeps Sam Hofer. An empty extra card is refused. Later hires stay in HireCraft.

## 0.1.0 - 2026-11-16

- Wizard of Crafts (`wizard`, or no command): the guide, one section at a time, then the company, the founder, and the package. `--smoke` checks the demo draft without a window.
- `template` starts a Graz skeleton the founder replaces. Capital may be above the statutory floor. Seats outside Wien are accepted.
- CLI: `demo-write`, `apply`, `dry-run`, `fingerprint`. JSON on stdout for the machine commands. `prepare` prints the guide.
- sandrasteve GmbH remains the labelled demo. A demo is not written unless `--accept-demo` is passed. The second write is a no-op.
- Package for BuchCraft, TeamCraft, BillCraft, ContractCraft, TaskCraft, AssetCraft, WikiCraft, DeskCraft, GainCraft, FormCraft, SpendCraft, HelmCraft, plus impressum, Beraterpaket, and `advice\prepare.md`.
- No installer, no write into the other apps' databases, no Lohnverrechnung. A later `lohncraft` will read the card. HireCraft still owns candidates hired after go-live.
