# 17 - LookCraft North Star: reverse Outlook, artcraft playbook, Rust endpoint

Date: 2026-10-14. Status: research complete, repo not yet scaffolded.
Prompt: "reverse outlook into lookcraft". Precedent: gridcraft-for-Excel.

## 1. The bet

Single Rust app (`rmcp` MCP server + `clap` CLI, Tauri shell later): perfect
UI/UX copy of Outlook, backend power increasing per release. GH repo with
issue/PR automation harness from day one. AI used heavily throughout —
teardown, spec-annotated codegen, round-trip corpus, review triage.

## 2. The contributor asymmetry (answered honestly)

ArtCraft has thousands of contributors including domain specialists (the Bezier
guru from Tsinghua fills a gap in days that would take us months). Joe Schmoe
and sandraschi do not. Consequences, accepted up front:

- **Longer, thinner.** Expect ~5-15x solo-dev throughput from 2 people + AI,
  not 1000x. Coverage arrives release by release, never all at once.
- **The substitute for specialists is threefold:** (a) public specs instead of
  lore (MS-PST/MS-OX*/Graph/JMAP — mail is standards-heavy, taste-light, which
  is genuinely good news vs cloning Illustrator); (b) existing libs as
  crystallized specialist knowledge — depend on melib/libpst, don't re-derive;
  (c) the automation harness as the contributor funnel: AI agents are the first
  contributors, Joe + Sandra are reviewers, not authors (`11-contributor-funnel.md`
  pattern, machines first).
- **The asymmetric advantage ArtCraft doesn't have:** MCP-native distribution.
  Their contributors are humans; an MCP mail server gets AI agents as *users*.
  Every agent that reads mail through LookCraft is adoption ArtCraft can't see.
- **Win condition is not parity.** Win = (1) best-in-class PST round-trip +
  MCP server agents actually use; (2) UI copy good enough that switching cost
  is near zero; (3) the harness that lets 2 people absorb AI output safely
  (spec-first, corpus-gated, honest gaps). Parity with Outlook is never the goal;
  the wedge + the moat (corpus) is.

## 3. Timing

EWS dies on Exchange Online **2026-10-01** (13 days). Every third-party client
is mid-migration to Graph. A Graph-native clone launches into forced movement —
the same kind of protocol window gridcraft exploits with PSD specs.

## 4. Spec corpus (preliminary research, 2026-10-14)

- **MS-PST** (`learn.microsoft.com/.../ms-pst`, public since 2010) — round-trip
  corpus foundation. Method precedent: `grokify/outlook-pst-go` (spec-section
  refs inline + porting case-study; copy the habit).
- **MS-OXMSG + MS-OX\*** (`/openspecs/exchange_server_protocols/`) — MSG +
  ~100 MAPI/Exchange wire docs.
- **Microsoft Graph** mail/calendar (`/graph/api/resources/message|event|contact`)
  — the post-EWS backend. Requires app registration + OAuth: ToS gate, legal
  pass required before promising "works with your 365 account".
- **JMAP** RFC 8621 family (`jmap.io`) — open-protocol escape hatch; melib
  already speaks it.
- iCalendar RFC 5545, vCard RFC 6350, MIME RFC 5322/2045-49 — Outlook is ~40%
  calendar; non-negotiable.
- **rmcp** + Tauri v2 clap-CLI — endpoint stack is solved (~250-line MCP server,
  single binary).

## 5. Format ladder (round-trip corpus order)

PST/OST → MSG → EML/MIME → ICS → VCF → OAB. Parser precedent: libpst (C,
PST→mbox/Maildir), libpff (PST+OST+PAB), MS pstsdk (2010 C++ SDK).

## 6. Teardown list (artcraft `12` method each)

Thunderbird (+Betterbird) — reference clone. Mailspring — design reference,
closest open "perfect copy" target. **meli/melib** — Rust precedent AND
candidate backend dependency (IMAP/JMAP/Maildir/mbox/notmuch/NNTP). Evolution,
KMail — enterprise/Exchange tradition, watch their Graph ports for pitfalls.
Superhuman/Spark/eM Client/new-Outlook-PWA — proprietary, teardown only.
Rust libs: melib (sync), lettre (send), rust-imap (narrow alt).
Fleet-internal: `projects/email-mcp`, `projects/ms-graph-mcp` — backend starts
as their consolidation, not from zero.

## 7. Release train (backend power per release)

- **R1**: EML/local + IMAP working client, Outlook-look shell. No Microsoft account needed.
- **R2**: PST import (MS-PST round-trip corpus green).
- **R3**: Graph (after legal pass) — the migration-window release.
- **R4**: calendar (ICS + Graph calendar) — the actual Outlook parity wedge.

## 8. Failure modes, named

Taste gap (interaction feel without a designer — mitigate: mechanical teardown
+ tokens + CUA verification harness). Long tail (weird PSTs, Exchange edges —
mitigate: corpus + honest-gaps labeling). Burnout (mitigate: narrow scope +
harness). Graph rug-pull (mitigate: local-first + IMAP/JMAP need no permission).

## 9. Next actions

1. File this doc (done). 2. UX teardown of new-Outlook + Mailspring. 3. New
   Repo Gate scaffold (Rust `rmcp`+`clap`, GH repo + issue/PR harness) on go-ahead.
