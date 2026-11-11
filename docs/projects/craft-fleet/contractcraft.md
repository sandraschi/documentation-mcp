# ContractCraft - Assessment

**Repo:** `D:\Dev\repos\contractcraft` (local, not pushed) - **Date:** 2026-11-09 - **Grade: C+** (Tier 1 only, no GUI; synthetic data; risk rules not reviewed by a lawyer) - **Origin:** fleet-owned

## What it is

Contract templates, review workflow, redlines, clause risk scan, tamper-evident seals and notice deadlines.
Fifth app of the back-office suite (`craft-fleet-expansion/BACKOFFICE_CRAFT_SUITE.md`, section 4.5).

## Model / verbs

- **Crates:** `contractcraft-store` (versioned templates, contracts, immutable versions + seals, transitions, emitted log), `contractcraft-core` (`risk.rs`, `seal.rs`, `render.rs`, redline, deadlines, demo), `contractcraft-mcp` (`contractcraft` binary).
- **17 MCP tools / CLI verbs:** status, template add/list/show, draft, list, show, edit, terms, transition, seal, verify, redline, risk_scan, render, deadlines, demo_seed.

## Strengths

- Gemini-draft bugs fixed by design: no fake Typst/PDF (PDF only through the real Typst CLI, clear error otherwise); the Ed25519 seal is documented and labelled as tamper evidence, not a signature.
- Status machine enforced; text changes only in draft as new versions; versions and seals immutable by trigger; executing requires a seal of the current version.
- Template fill refuses typos, missing required values, leftover and injected placeholders.
- Risk scan: 9 default DE/EN rules (liability, indemnity, auto-renewal, foreign venue/law with Austrian exceptions, missing AVV/DPA, penalty, unilateral change, exclusivity), user TOML rules, always with disclaimer. Redline reports the risk delta of an edit.
- Live chain verified: `contractcraft deadlines --emit` -> bus -> `taskcraft inbox-drain` -> issue "Kündigungsfrist ..." due 30.11.2026. Exported md verified byte-identical to the seal; a one-character change is detected.

## Gaps / risks

- No egui window.
- Typst not installed on Goliath, so PDF is untested end to end (md and typ work).
- md -> Typst converter: headings, bullets, paragraphs only.
- Seal key is a plain file next to the DB (Credential Manager planned in craft-biz secrets).
- No LLM review, no word-level redline, no DOCX import, no QES.
- `contract.executed` goes to gaincraft, which does not exist yet.

## Next 3 steps

1. Install Typst, add a PDF render test that runs when the CLI is present.
2. egui app: contract list, side-by-side redline with risk panel, deadline calendar.
3. Lawyer review of the rule set; add rules for Gewährleistung waivers and payment terms.

## Verdict

Grade C+: honest, tested Tier 1 with the integrity guarantees enforced twice and a working deadline link to taskcraft; needs a GUI and a legal review of the rules before real use.
