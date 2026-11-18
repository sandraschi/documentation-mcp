# SetupCraft

**Repo:** `d:\Dev\repos\setupcraft`
**Version:** 0.1.0 (2026-11-16)
**Status:** Wizard of Crafts writes one founder card. `demo-write` writes the sandrasteve founding batch (two people). No craft database is updated yet. No Lohnverrechnung.

Any small Austrian GmbH or FlexKapG. sandrasteve GmbH is only the labelled demo.

```powershell
cargo run --manifest-path D:\Dev\repos\setupcraft\Cargo.toml -- wizard
```

The window walks the Gruendung guide, then the company, then one founder card: photo, personal data, hire date, position, current work, and monthly gross. It then writes the package. `wizard --smoke` checks that draft without opening a window. The wizard drops every person after the founder.

`demo-write --accept-demo` writes the labelled demo in full: Alex Berger and Sam Hofer, both `source: onboarding`, plus the advisors and the photo names.

People hired after go-live are added in HireCraft. That app keeps the candidate pane. The Mitarbeiterkarte file is `teamcraft\employees.json`. TeamCraft does not show that page yet. Lohnverrechnung is a later `lohncraft`, which will read a complete card and a locked month.

CLI: `prepare`, `template`, `acknowledge`, `apply`, `demo-write --accept-demo`, `dry-run`, `fingerprint`.

Shared types live in `craft-biz::company`. The guide lives in `craft-biz::advice`. Spec: `docs/PRD.md`.
