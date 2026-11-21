# Brief: Claude (round 2, when token allowance permits)

Read first: `standards/CRAFT_FLEET_RULES.md`, then `projects/CRAFT_CONSOLIDATION_PLAN_2026-11.md`,
then session-log entries `craft-*` since the last Claude entry.

Role: review and independent verification. Never verify a lane Claude executed.
Token frugality: max 10 repos per session; read README + entry points, not whole crates.

Log file: `operations/session-log/craft-claude-<date>.md`.

## Tasks, in order

### K1. Status check (cheap, every session start)
- Compare plan ticks against reality: archived flags on GitHub, test counts from a fresh
  `cargo test --workspace` on 2 sampled repos, uncommitted state in mcp-central-docs.
- Report discrepancies to Sandra in chat and in the log.

### K2. Phase 3 README honesty audit
- Order: repos with releases first (celcraft, writercraft, robotcraft, databasecraft,
  gamecraft, rsicraft, devcraft, taskcraft, wikicraft, teamcraft, gaincraft, buchcraft,
  deskcraft, contractcraft, assetcraft, billcraft, spendcraft, hirecraft, helmcraft,
  formcraft, splatcraft, aicraft), then T2 repos without releases.
- For every README feature claim: find the code path, or mark it `Planned`. Write the
  proposed README diff into the log per repo; the owning agent applies it (or Claude applies
  it if no lane owns the repo, after claiming).
- Flag `[ALPHA]` prefixes that no longer match the tier.

### K3. Phase-exit verification
- After agy's A2 and Cursor's C2: fresh clone, build, test, compare README vs behaviour on
  each repo they claim done. Tick the plan's phase exit only if it holds.
- Phase 5 sample: 5 random active crafts, same checks, plus egui contrast and Ctrl + wheel
  zoom (screenshot via the app if available).

### K4. Governance wiring (after Phase 4)
- Add the admission gate and release gate to `RUST_ARTCRAFT_STANDARD.md`.
- Add the craft rules to `standards/AGENT_READING_ORDER.md` and regenerate the FLEET-CONTEXT
  block in `D:\Dev\repos\AGENTS.md` with `fleet-gate/agent_context.py` (do not hand-edit it).
- Propose a weekly scheduled run of the scorecard; Sandra approves.

## Not yours
Bulk mechanical rollouts (opencode), stub implementation (agy, Cursor).
