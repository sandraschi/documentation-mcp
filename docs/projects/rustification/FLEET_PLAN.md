# Fleet Rustification Plan — topology, order, and cutover

**Status:** plan, 2026-10-20. **Scope:** how the fleet converts, in what order,
and what happens to repo names. **Not** a replacement for the triage docs.

## Source of truth

- **What to convert:** [`standards/rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md`](../../standards/rust-artcraft/FLEET_TRIAGE_AND_PYPI_TRANSPILATION.md)
  — 4-bucket matrix, Top 35 candidates, wave-0 pilots, per-group crates.
- **How to convert:** [`standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md`](../../standards/rust-artcraft/FLEET_CONVERSION_STANDARD.md)
  and [`patterns/REPCONV_SOP.md`](../../patterns/REPCONV_SOP.md) — Mode A/B,
  70% kernel, `repconv`, cutover checklist.
- **What "done" means:** the 6-Gate Definition of Done in
  [`standards/rust-artcraft/CONTAINMENT_AND_CRATES.md`](../../standards/rust-artcraft/CONTAINMENT_AND_CRATES.md).

This plan only adds the two things those docs leave open: **repo topology at
fleet scale** and **the naming decision**.

## Measured inputs (2026-10-20)

- 203 directories carry a `fleet-start.config.ps1`.
- **12** mention NSSM: `advanced-memory-mcp`, `aiwatcher-mcp`,
  `arxiv-mcp`, `devices-mcp`, `discord-mcp`, `email-mcp`, `fastsearch-mcp`,
  `fleet-agent-mcp`, `mcp-federation-hub`, `ms-graph-mcp`, `pywinauto-mcp`,
  `tvtropes-mcp`.
- 8 `rust-*` directories exist: `rust-arr-mcp`, `rust-calibre-mcp`,
  `rust-devices-mcp`, `rust-plex-mcp`, `rust-sdr-mcp`, `rust-yahboom-mcp`, plus
  `rust-test-b` / `rust-test-c` (experiments).
- Bucket split from the triage doc: ~55% A (~100 repos), ~15% B (~30), ~15% C
  (~25), ~15% D (~30).

## Decision: do not create a sibling repo per repo

A permanent `rust-` twin for every repo would double the fleet's CI, MCPB,
ports, AGENTS.md, issue trackers and agent confusion. The conversion standard
already rejects that: a shadow repo is a **temporary harness for live services**,
archived away after cutover.

| Repo kind | Mode | Repo count effect |
|---|---|---|
| NSSM / client-wired daily driver (the 12 above, plus any client-wired repo verified case by case) | **Mode A** shadow | +1 during the port, -1 when the Python repo is archived |
| Standalone, stateless, dormant (the bulk of Buckets A/B) | **Mode B** in-place branch | 0 |
| Hybrid Bucket C (host-app bridges) | In-place Rust L1/L2/L3 + thin Python listener | 0 |
| Bucket D (PyTorch/CUDA) | Stay Python, optional Rust front door | 0 |
| Hubs (`democraft`, craft wrappers) | **One** 3-tier workspace, not one per wrapped app | 0 |

Expected temporary growth: at most the Mode A set (12-25 repos). Net growth
after cutover: zero. The fleet ends with one repo per domain, not two.

## Naming (recommended, needs sign-off)

- The Rust repo keeps the name `rust-<domain>-mcp` **permanently** (matches the
  pilot and the existing 8).
- The Python repo is archived as `_archives/<domain>-mcp-python`, not deleted.
- The **MCP registration alias stays `<domain>`**. Claude Desktop, Cursor and
  chat see `devices`, `plex`, `arr` — never `rust-devices`. This is the part
  that stops config churn.
- If the fleet later prefers the original repo name, rename the Rust repo after
  the archive; GitHub redirects git URLs, but every client config and doc must
  be updated once, deliberately.

Open question: confirm "rust- is permanent" or schedule the rename. Do not leave
it implicit; agents will guess differently.

## Mode B in practice (what the tree and the release look like)

Mode B is a **branch inside the same repo**, not a second repo:

```
<domain>-mcp/                 (branch feat/rust-artcraft)
  Cargo.toml                  workspace root
  Cargo.lock                  committed
  crates/
    <domain>-core/            L1: domain logic, Command::dispatch
    <domain>-store/           L1: SQLite/history (if needed)
    <domain>-mcp/             L2: clap CLI + stdio MCP (--json + `mcp`)
    <domain>-app/             L3: egui desktop (if the repo has a UI)
  _legacy_py/                 old src/, pyproject.toml, tests/, webapp/
  README.md                   rewritten at merge
```

`main` stays Python until the merge. The branch carries both trees; at merge
`_legacy_py/` is **deleted**, so `main` ends up Rust-only with the same history,
issues, stars and clone URL. The old code is not lost: it remains at the last
Python tag, which is also the oracle for parity checks.

**Release assets at cutover** (pilot convention, `rust-devices-mcp` v0.4.0):

| Asset | When |
|---|---|
| `<domain>-mcp.exe` | always: CLI (`--json`) + stdio MCP (`mcp`) |
| `<domain>-app.exe` | only if the repo has an L3 desktop app |
| `<Domain>-Rust-X.Y.Z-setup.exe` | NSIS installer, if there is an app or a service |
| `SHA256SUMS.txt` | always |

No `.mcpb` in the pilot: MCPB is the Python/Node bundle format, and Rust ships a
binary plus installer. A binary MCPB can be added later if the client supports
it, but it is not the convention yet. Old Python releases keep their assets on
their own tags; tags are immutable history, do not delete them.

Client config changes once, at cutover: `command` becomes the `.exe`, `args`
become `["mcp"]`. The registration alias stays `<domain>`, so nothing else in
chat or configs changes. If the repo had a webapp, the L3 egui app must reach
UI parity before merge, or the webapp stays and the cutover slips; the 6 gates
do not allow a half-state on `main`.

## Waves

**Wave 0 — done.** `rust-devices-mcp` is the reference implementation (4 crates,
24 tools, 58 tests). Do not re-pilot; copy it.

**Wave 1 — live daily drivers (Mode A), one at a time.** Start with the 12 NSSM
repos, beginning with the ones already partially ported: `devices`, `arr`,
`plex`, `calibre`. Each cutover: parity to v0.4+, `import.rs` reads the legacy
`.env`/config, switch the client to the Rust binary, archive Python, update
`WEBAPP_PORTS.md` and the MCP config. No two cutovers in one day.

**Wave 2 — standalone Bucket A/B (Mode B), in place.** Bench instruments first
(`multimeter`, `oscilloscope`, `power-supply`, `function-generator`,
`spectrum-analyzer`) because the win is measurable (500 MB pyvisa replaced by
raw SCPI). Then REST/SQLite wrappers (`rss`, `bookmarks`, `fastsearch`). Branch
`feat/rust-artcraft`, `_legacy_py/` during the port, merge on 6 gates.

**Wave 3 — hubs and hybrids.** `democraft` becomes **one** workspace:
`craft-core` (process adapters + job engine + provenance), `craft-mcp` (L2), and
`craft-app` (L3: axum + the existing React build, or egui if the webapp is
retired). The 13 Craft apps are already Rust; this is adapters, not a rewrite.
Bucket C host bridges (Blender, FreeCAD, KiCad) keep a ~100-line Python listener
inside the host and Rust outside it.

**Wave 4 — defer and refuse.** Bucket C2 (Xiaomi/Amazon reverse-engineered auth)
stays Python until the protocol is stable. Bucket D stays Python; a Rust front
door is allowed only as a thin client to a Python GPU worker.

## Per-repo checklist

1. Bucket it (A/B/C/D) from the triage doc. If D, stop here.
2. Is it live (NSSM, client-wired, LAN)? Mode A; else Mode B.
3. Copy the 70% kernel from `rust-devices-mcp`; write only the domain driver.
4. Tool names must match 1:1 with the Python repo before cutover.
5. Pass the 6 gates; `repconv` checklist; MCPB if distributable.
6. Cut over, archive Python, update ports/registry/AGENTS.md/MCP config.
7. Record the cutover in `operations/session-log/` and the repo's HANDOVER.

## Guardrails

- One repo at a time; no fleet-wide sweeps. Max 5 files per commit; 3+ file
  edits get timestamped `.bak` first.
- Never scaffold a runt "rust-" repo to reserve a name. A repo exists when it
  passes gates.
- Dual maintenance is a budgeted window, not a lifestyle: if the Python repo
  needs a fix during the port, fix it and port the fix the same day.
- Archive, don't delete. The oracle loop needs the original to compare against.

## Metrics

- Mode A cutovers completed / 12 NSSM repos.
- Tool parity: tools matching 1:1 per converted repo.
- Python repos archived vs converted.
- Fleet repo count (should not grow net).
- Gate pass rate: first-run green, no waived HIGH.

## First five actions

1. Sign off the naming rule (rust- permanent, alias unchanged).
2. Verify `rust-arr`, `rust-plex`, `rust-calibre`, `rust-yahboom` parity status
   against their Python siblings; close the gap or archive them.
3. Convert `multimeter-mcp` in place as the first Mode B proof.
4. Cut over `devices-mcp` (Mode A) using the already-built pilot.
5. Write the `democraft` workspace plan (L1/L2/L3) and start `craft-core` with
   the job engine, since that is Python code we already own and understand.
