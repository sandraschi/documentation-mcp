# HANDOVER - adobe-offensive

## What was done (2026-10-08)

- Created projects/adobe-offensive section with 7 files: README, 01-analysis, 02-copy,
  03-inventory, 04-targets, 05-pywinauto, 06-roadmap, plus this HANDOVER.
- Sources: storytold/artcraft README/ROADMAP/LICENSE/dev_setup, releases (v0.41.0 2026-09-26),
  issues (#2005 latest), getartcraft.com/apps (7 crafts), Ars 2026-10-07 Orland.
- Batch discipline: batch1 5 files (README+01-04), batch2 3 files (05+06+HANDOVER). No commits yet.

## Last concrete action

- Wrote 06-plans-roadmap.md with Phase 0-4 + Opus handoff prompt + license table TODO.

## Next step for Opus or next agent

1. Execute Phase 0.1: verify LICENSE per Craft repo, fill appendix table in 06.
2. VM snapshot + PhotoCraft/PdfCraft smoke via pywinauto-mcp.
3. Weekly issue burn-down note here.

## Blockers

- Craft repo URLs not yet enumerated (only hub getartcraft.com/apps known). Need per-repo links.
- FilmCraft web absence reason unknown.
- No ports claimed yet for any new harness work - run claim_ports.py before code.

## Deliberately NOT done

- No code copied from ArtCraft core (Fair Source). Specs only.
- No Adobe UI pixel copy. Behavior specs + fleet restyle rule stands.
- No new fleet repo scaffolded. Mesh first, per 03.
- No git commit - leave files uncommitted for Sandra review, then commit max 5 per commit.

## Session 2026-10-08 (late) - Phase 0 execution

### 0.1 License table - DONE
- Appendix in 06 filled. All 7 Craft repos are dual MIT OR Apache-2.0 (LICENSE files read, Cargo.toml checked).
  Brand assets (docs/brand/, ArtCraft name) excluded by NOTICE. None marked DO NOT REUSE. Core artcraft stays Fair Source.

### 0.3 Baseline - day 0 snapshot (2026-10-08T21:02Z, gh api)
This is the FIRST data point, not a one-week series. Re-run on 2026-10-15 for the first weekly delta.

| repo | stars | forks | open issues | open PRs | releases | latest release |
|---|---|---|---|---|---|---|
| storytold/artcraft | 7464 | 1014 | 62 | 10 | 28 | artcraft-v0.41.0 2026-09-26 |
| storytold/photocraft | 25798 | 3482 | 295 | 151 | 7 | v0.5.0 2026-10-08 |
| storytold/vectorcraft | 3593 | 1382 | 21 | 3 | 9 | v0.7.0 2026-10-08 |
| storytold/filmcraft | 5045 | 1672 | 103 | 45 | 5 | v0.4.0 2026-10-08 |
| storytold/lightcraft | 5214 | 1492 | 64 | 22 | 5 | v0.4.0 2026-10-08 |
| storytold/pdfcraft | 4228 | 1420 | 104 | 19 | 5 | v0.4.0 2026-10-08 |
| storytold/effectcraft | 2605 | 1104 | 37 | 24 | 7 | v0.6.0 2026-10-08 |
| storytold/designcraft | 1557 | 846 | 53 | 46 | 5 | v0.4.0 2026-10-08 |

Notes: open issue/PR counts from GitHub search API (is:open). artcraft open issues = 62, which is far below the
"#2005" issue number in 01. The #2005 is the issue+PR number sequence, not the open count. Stars are now
concentrated on photocraft (25.8k), 3.5x the core repo. All 7 crafts shipped a release today (2026-10-08).
Command to reproduce: see the gh api loop in this session; per repo: repos/storytold/<r>, search/issues
is:issue/is:pr is:open, releases (paginated), releases/latest.

### 0.2 VM smoke - NOT DONE (blocked, nothing installed, no evidence files written)
Looked (read-only):
- virtualization-mcp backend :10701 up; pywinauto-mcp backend :10789 up (NSSM service mcp-pywinauto-mcp, LocalSystem).
- VBoxManage (user context) lists 5 VMs incl. win11-automated (Win11 x64, 8 GB, 4 CPU, poweroff, 0 snapshots).
- virtualization-mcp GET /api/v1/vms returns [] and hyperv_management list returns 0. BUG CANDIDATE: the service
  does not see the user's VirtualBox VMs (likely VBox per-user registry vs service account). Not investigated further.
- Installers: photocraft-0.5.0-windows-x64.msi (55.8 MB), pdfcraft-0.4.0-windows-x64.msi (44.3 MB) on GitHub releases.
Blockers:
1. Downloading + installing third-party alpha MSIs needs Sandra's explicit go.
2. Architecture gap: the host pywinauto-mcp (LocalSystem service, session 0) cannot inspect windows inside a VM guest.
   UIA dumps need pywinauto running inside the guest (or inside Windows Sandbox). Needs a decision before 0.2 can run.
3. virtualization-mcp cannot see win11-automated (see bug candidate above), so "snapshot via virtualization-mcp" is not
   possible today without fixing that or using VBoxManage directly.

## How to continue

- Read README then 01-06 in order. Keep ASCII prose. Update this file at session end.
- If older than a week, treat as stale, re-verify releases/issues/licenses.

## Session 2026-10-11 - UX teardown, business model, legal, trajectories

### Done
- New: 12-artcraft-ux-teardown.md, 13-business-model.md, 14-legal-deep-dive.md,
  15-trajectories.md. README index + erratum; erratum headers in 01, 02, 06.
- Verified via gh api 2026-10-11 10:11 UTC: core artcraft relicensed to
  MIT OR Apache-2.0 on 2026-10-10 (PR #2043). Org storytold: 56 repos,
  114,580 stars, 33,089 forks. photocraft 44,167 (+18.4k since 2026-10-08).
  The "300k stars" figure did not verify. New Microsoft/Autodesk/Avid targets
  in org: wordcraft, gridcraft, deckcraft, cadcraft, soundcraft.
- Verified: no Adobe legal action reported; no 2026 SCOTUS ruling on UI
  reimplementation (Cox v. Sony and Thaler cert denial are the 2026 items).
- Comps verified: InterPositive $587M, Canva-Affinity (~$380M reported, free
  since 2025-10-30), Anthropic-Bun (2025-12), Steinberger to OpenAI (2026-02),
  Google-Windsurf ($2.4B license, 2025-07).

### Open
- Two-agent clean-room design for reversing-mcp (observer vs implementer
  separation, recorded purpose per session) is NOT written. Tier 3
  CUA+disassembly maps upstream conflict with clean-room reimplementation use;
  needs a design decision before anyone uses Tier 3 output for a rebuild.
- Mirror insurance (15 section 7.1) needs Sandra's go.
- photocraft-cli MCP wrapper: run wrappee-drift first.
- Re-score 15 trajectory odds monthly.
- .bak files from this session in adobe-offensive/ and reversing-mcp/
  (NEXT_STEPS .bak is unused; NEXT_STEPS itself untouched).
- Nothing committed.

### Addendum 2026-10-14 - LookCraft north star + PRD
- New: `17-lookcraft-northstar.md` (research bundle: MS-PST/OX*/Graph/JMAP
  corpus, format ladder, teardown list, R1-R4 train, contributor-asymmetry
  answer) and `18-lookcraft-prd.md` (objective, users incl. agents-first,
  weak-fit override of 16 §3, architecture, harness, legal gates, R1 checklist).
- `16-portfolio-expansion.md`: Outlook weak-fit rating appealed with dated
  override (re-score monthly). No other ratings touched.
- Next, in order: teardown (new-Outlook + Mailspring, `12` method), then Rust
  scaffold under the New Repo Gate (rmcp + clap + GH harness).

### Addendum 2026-10-14 - teardown done (`19-lookcraft-teardown.md`)
- Mailspring source-read: mailsync shape stolen (per-account CLI process,
  JSONL tasks/changes over stdio, local-op-first, kill-safe sqlite), sync
  algorithm (bg sweep + fg IDLE), fat-row regret noted; component inventory
  maps 1:1 to Outlook copy; plugin points = harness-era mechanism.
- New Outlook: WebView2 shell + Outlook-web + Fluent vocabulary (docs/reporting,
  inference marked); M365 rail = two-tier nav, copy order/icons/collapse.
- Verb split: TRIAGE vs FILE vs SEND. Settled: melib sync, sqlite+indexes,
  Tauri webview, CLI-first, corpus from R1. Do-not-copy list filed.
- Next: Rust scaffold under the New Repo Gate. Needs Sandra's go (new repo).

### Addendum same day - 16-portfolio-expansion.md
- Office batch (wordcraft/gridcraft/deckcraft + cadcraft/soundcraft) all
  created 2026-10-07; batch-2 stars ~1/10 of batch 1. Baseline numbers for the
  2026-10-15 delta are in 16 section 1.
- cadcraft ships its own MCP (`cadcraft-cli mcp`). Decision recorded: compose
  cadcraft -> qcad-mcp -> freecad-mcp via DXF, do not build a fleet clone.
  Steps 1-6 in 16 section 6, none started (alpha install needs Sandra's go).
- Doc drift: projects/CAD_FLEET_COMPETITIVE.md qcad ports 10966/10967 vs
  qcad-mcp README 11966/11967. Not fixed.
- Trademark collisions (Soundcraft, Lightcraft, Minecraft/Warcraft) are
  VERIFY items, from memory.
