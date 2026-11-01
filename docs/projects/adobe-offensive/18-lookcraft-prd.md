# 18 - LookCraft PRD: Rust Outlook clone, artcraft playbook, agent-native

Date: 2026-10-14. Status: PRD, repo not yet scaffolded. Parent: `17-lookcraft-northstar.md`.
Method precedent: `12-artcraft-ux-teardown.md`. Endpoint template: cadcraft
(`cadcraft-cli mcp`, single Rust workspace, CLI + MCP + UI shell — see 16 §6).

## 1. Objective

A Rust mail/PIM client that looks and feels like Outlook, works without a
Microsoft account on day one, and is usable by AI agents through a built-in
MCP server. Two humans (Joe Schmoe, sandraschi) + AI contributors via an
issue/PR automation harness. Backend power increases per release (R1→R4);
no release ships a backend it cannot prove on a corpus.

Non-goals: Exchange-server reimplementation, Outlook parity, mobile apps,
collaboration server features (shared mailboxes v1, Teams interop).

## 2. Users, in order

1. **AI agents** — the MCP server is the primary interface. An agent triaging,
   filing, and drafting mail through LookCraft tools is adoption no human
   marketing buys. Every tool must be agent-callable with zero GUI.
2. **Sandra** — daily driver for IMAP + local archives by R2.
3. **Joe Schmoe** — the switching-cost test: if Joe can't move in an afternoon,
   the UX copy failed.

## 3. The weak-fit override (16 §3 rated Outlook-as-client WEAK fit)

16 is right that the value of Outlook has historically lived in
Exchange-the-server. The override is three dated facts:

- **EWS dies 2026-10-01.** The server tie is being cut by Microsoft itself;
  every client is being thrown back onto Graph (permissioned, ToS-gated) or
  open protocols. Client-side value (fast triage, local archives, agent
  access) is suddenly the differentiator.
- **PST lock-in is client-side.** Millions of orphaned PSTs behave like the
  orphaned Access DBs 16 already rates as good fit — "millions of orphaned
  business DBs, underrated" applies verbatim to PSTs.
- **Mail is standards-heavy, taste-light.** MS-PST/MS-OX*/Graph/JMAP/RFC
  5322/5545/6350 are public. The specialist gap that hurts against Illustrator
  hurts least here; the teardown gap is mechanical (layout, tokens, IA).

If any of the three stops being true, re-score (15-trajectories monthly cadence).

## 4. Scope: release train with gates

- **R1 — Look, local, IMAP.** Outlook-look shell (teardown-driven), EML/local
  folders, IMAP sync (melib), send (lettre). Gate: Joe-afternoon switch test
  on 2 IMAP accounts; `lookcraft-cli` parity for every GUI action.
- **R2 — PST import.** MS-PST reader, PST→local import, round-trip corpus
  (`lookcraft-corpus`, gridcraft-corpus pattern: N real-world PSTs, zero-diff
  bar). Gate: corpus green, import of a 1 GB PST without loss (losses listed,
  never silent).
- **R3 — Graph.** After legal pass (app registration, ToS, verified-publisher
  decision). Gate: 365 mail+calendar read/send against a test tenant.
- **R4 — Calendar.** ICS + Graph calendar; the actual Outlook wedge.
  Gate: invite round-trip with Thunderbird and Outlook (the corpus idea applied
  to interop).

No release widens scope without its gate green. Honest-gaps file ships in-repo
from R1 (fleet honesty rule).

## 5. Architecture (endpoint)

Rust workspace (cadcraft layout precedent):

- `lookcraft-cli` — full CLI (every feature), `mcp` subcommand (stdio like
  `cadcraft-cli mcp`), `--connect` to a running UI later.
- `lookcraft-core` — account/store/sync/search crates. Engines reused, not
  written: **imap crate + lettre** (sync/send now — both compile; `async-imap`
  0.9.7 rejected, does not build on current Tokio), rusqlite FTS5 (search,
  verified live), system webview or egui shell per teardown verdict (decision
  during scaffold, recorded with reasons). **melib deferred to R2 with cause**:
  its IMAP stream is `smol::Async`, which cannot run under the tokio runtime
  without a dual-runtime bridge — the trait wall makes that substitution safe
  later. No copyleft in the tree (revisit if melib returns: EUPL/GPL).
- UI shell (R1: thin, perfect-copy chrome over core; backend power is the
  release train, chrome is the constant).
- `lookcraft-corpus` — fixtures + round-trip harness, CI-gated.

## 6. UX copy spec (from teardown, to be executed)

Teardown targets: new-Outlook (PWA baseline to beat) + Mailspring (open design
reference), `12` method: DOM/CSS/tokens, verb-split IA (applied to mail:
TRIAGE vs FILE vs SEND?), two-tier nav (global rail moves between
Mail/Calendar/People; each tool owns its menus), maturity badges, mono-for-chrome.
Corpus idea applied to UI: screenshot-diff suite against reference layouts
(CUA harness does the looking).

## 7. Harness (the contributor funnel for 2 humans)

GH repo from day one: issue templates (bug/corpus-case/teardown-note),
PR automation (corpus CI must-pass, spec-ref check for parser code,
screenshot-diff for UI), AI-triage labels, weekly release train. Humans review;
machines author. Mirror insurance decision (15 §7.1) applies here too —
needs Sandra's go before public launch.

## 8. AI usage (heavy, gated)

Teardown-via-CUA (DOM + screenshots + token extraction), spec-annotated
parser codegen (MS-PST section refs, grokify/outlook-pst-go habit), corpus
case generation (synthetic PST/EML edge cases), review triage (first-pass PR
summaries + risk flags). Every AI output lands through the harness; nothing
lands on reputation. B4-style LLM guidance stays out of the product (mail is
not the place for improvisation), inside the factory only.

## 9. Legal gates (14 method, before R3 at latest)

Graph API ToS + app registration + publisher verification; "LookCraft" mark
search per jurisdiction/class (note 16 §5 method; Craft Docs/CMS collisions
are remote but VERIFY); UI trade-dress pass for the Outlook chrome copy;
Open Specification Promise scope check for MS-PST/MS-OX* (like 16 §2 did for
OOXML).

## 10. Risks (from 17 §8, kept live)

Taste gap, long tail, burnout, Graph rug-pull — mitigations in 17. Add:
melib-dependence risk (upstream direction changes — mitigate: trait-wall the
sync engine so rust-imap can substitute); single-maintainer bus factor
(mitigate: harness + docs written for strangers from day one).

## 11. R1 acceptance checklist (definition of done)

- [ ] `lookcraft-cli` sends/receives/lists/searches on 2 IMAP providers.
- [ ] GUI shell opens, triages, replies; Joe-afternoon test passed, notes filed.
- [ ] MCP server: agent triages 50-message fixture mailbox end-to-end.
- [ ] Honest-gaps file exists and is non-empty (a zero-gap R1 is a lie).
- [ ] Corpus harness runs in CI (fixtures + zero-diff bar, even if small).

## 12. Open questions

egui vs webview shell (teardown decides); tantivy vs sqlite-FTS (measure);
shared-engine candidacy (does lookcraft-core yield a `craft-mail` engine for
the portfolio? propose after R2); tour corpus location (in-repo vs fleet
library, cf. Tier 3 §8).
