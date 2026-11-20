# SetupCraft

**Repo:** `d:\Dev\repos\setupcraft`
**Version:** 0.1.0 (2026-11-16)
**Status:** Wizard of Crafts writes the founder and the current staff. `demo-write` and the wizard demo both keep Alex Berger and Sam Hofer. No craft database is updated yet. No Lohnverrechnung.

Any small Austrian GmbH or FlexKapG. sandrasteve GmbH is only the labelled demo.

```powershell
cargo run --manifest-path D:\Dev\repos\setupcraft\Cargo.toml -- wizard
```

The window walks the Gruendung guide, then the company, then the founder card, then each current employee: photo, personal data, hire date, position, and current work. It then writes the package. `wizard --smoke` checks the sandrasteve draft (two complete cards) without opening a window.

`demo-write --accept-demo` writes the same two people from the labelled demo, plus the advisors and the photo names. Staff entered in the wizard have source `onboarding`.

HireCraft keeps the candidate pane for people hired after go-live. The Mitarbeiterkarte file is `teamcraft\employees.json`. TeamCraft does not show that page yet. Lohnverrechnung is a later `lohncraft`, which will read a complete card and a locked month.

CLI: `prepare`, `template`, `acknowledge`, `apply`, `demo-write --accept-demo`, `dry-run`, `fingerprint`.

Shared types live in `craft-biz::company`. The guide lives in `craft-biz::advice`. Spec: `docs/PRD.md`.

> Local-only until admission: no remote yet. See CRAFT_CONSOLIDATION_PLAN_2026-11 section 7.
