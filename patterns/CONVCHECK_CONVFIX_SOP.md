---
title: "ConvCheck / ConvFix SOP (post-repconv audit and repair for rust-* repos)"
category: pattern
status: active
audience: mcp-dev
skill_candidate: true
related:
  - patterns/REPCONV_SOP.md
  - standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md
  - standards/RUST_ARTCRAFT_STANDARD.md
  - standards/rules/agentic_macros.md
last_updated: 2026-10-18
---

# ConvCheck / ConvFix SOP

**Triggers:** `convcheck <rust-repo>` (read-only audit) / `convfix <rust-repo>` (mutating repair)
**Applies to:** `D:\Dev\repos\rust-*-mcp` workspaces that already exist (shadow-built by `repconv`).
**Never applies to:** `D:\Dev\repos\<name>-mcp` Python originals — those take `repconv`, never `convcheck`.

## Why this exists

`repconv <repo>` converts `D:\Dev\repos\<name>-mcp` into `D:\Dev\repos\rust-<name>-mcp` in phases 0-5.
In practice the shadow stalls mid-flight (phase-1 scaffold committed, parity claimed but unverified,
6 gates half-green, `HANDOVER.md` stale). Re-running `repconv` on `rust-*` is nonsense — it would
treat the Rust output as a Python input and re-stamp the kernel over real work.

`convcheck` is the read-only gate that answers "how converted is this, really?"
`convfix` closes exactly what `convcheck` found, tier by tier. Same split as
`gapfind` (report) vs fix pass, `fakefind` (report) vs fix pass.

| Macro | Input | Mutates? | Question |
|---|---|---|---|
| `repconv <name>-mcp` | Python original | Creates `rust-<name>-mcp` | How do I convert this? |
| `convcheck <rust-name>-mcp` | Rust shadow | **No** | How converted is this, really? |
| `convfix <rust-name>-mcp` | Rust shadow + convcheck report | **Yes, Rust side only** | Fix exactly the gaps, nothing else |

## Hard rules

1. **convcheck is read-only.** Report, propose, wait. No `.rs`, no `.toml`, no `git commit`. Same rule as gapfind/fakefind.
2. **Legacy fence holds both ways.** `D:\Dev\repos\<name>-mcp` stays untouched during convcheck *and* convfix. Verify with `git -C D:\Dev\repos\<name>-mcp status --porcelain` + `rev-parse --short HEAD` before and after; any drift aborts the pass.
3. **Enumerate from code truth, never memory.** Tool mapping from `llms-full.txt` / `src/<pkg>/` (Python) vs `crates/<domain>-core/src/lib.rs` `Command` enum + `crates/<domain>-mcp` CLI/MCP list (Rust). Gate status from commands actually run (`cargo clippy`, `cargo test`, `cargo fmt --check`, stdio probe), not from `README.md` badges.
4. **Batch safety:** max 10 files per commit; 3+ file edits need timestamped `.bak` per file first. Checkpoint commit per tier closed.
5. **No new scope.** convfix closes convcheck items only. New features, renames, or webapp redesigns are a separate task.

## convcheck procedure (read-only)

Given `D:\Dev\repos\rust-<domain>-mcp` + sibling `D:\Dev\repos\<domain>-mcp`:

1. **Baseline:** record both SHAs (`git rev-parse --short HEAD`), branch, `git status --porcelain` (both must be clean to start; if dirty, report and stop).
2. **Dossier freshness:** does `docs/CONVERSION_DOSSIER.md` exist with the 7-point recon + 1:1 tool table? Is `docs/CONVERSION_LOG.md` + `HANDOVER.md` newer than the last code commit? Stale docs = finding.
3. **1:1 tool mapping:** build `Legacy Tool & Operation -> Rust Command -> CLI subcommand -> MCP name + legacy alias`. Every legacy `@mcp.tool` / portmanteau `operation` must have a row; mark `covered / missing / intentionally-excluded (with rationale)`.
4. **6-gate probe (run, don't skim):**
   - `cargo clippy --workspace --all-targets --all-features -- -D warnings`
   - `cargo test --workspace`
   - `cargo fmt --all --check`
   - stdio probe: `initialize -> tools/list -> tools/call` (stdout pure JSON-RPC, logs on stderr only)
   - `Cargo.lock` committed, no `target/`, `*.bak`, `*.exe` in `git status`
   - `CHANGELOG.md` has a checkpoint line for the current tier
5. **Write report:** `docs/ASSESSMENT_<YYYY-MM-DD>.md` is written by *convfix*, not convcheck — convcheck reports in-chat (table + gate red/green + fix list ordered by tier). No files written.

## convfix procedure (mutating, Rust side only)

1. **Gate:** a convcheck report less than 7 days old, or re-run convcheck first.
2. **Order:** dossi er gaps (missing tool rows) -> compile gates (clippy/test/fmt) -> parity gaps (missing commands) -> polish (snapshots, CHANGELOG, HANDOVER). One tier per commit.
3. **Prove each fix by running it:** paste the exact `cargo` command + counts, plus the stdio probe transcript for MCP changes.
4. **Close the loop:** append to `docs/CONVERSION_LOG.md`, update `HANDOVER.md` (last action, next step, blockers, deliberately-not-done), write `docs/ASSESSMENT_<YYYY-MM-DD>.md`, commit.

## Done criteria

- convcheck: in-chat table with every legacy op mapped + 6 gates red/green + ordered fix list. Zero files touched (`git status` identical before/after).
- convfix: all convcheck reds green (or explicitly deferred with rationale in `ASSESSMENT`), `CONVERSION_LOG.md` + `HANDOVER.md` current, checkpoint commits pushed (or left local with explicit instruction).
