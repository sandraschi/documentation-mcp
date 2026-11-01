---
title: "Standards Bar"
category: standard
status: review
audience: mcp-dev
last_updated: 2026-09-18
# status: review -- promoted from JUNE_2026_STANDARDS_BAR.md 2026-09-18.
# Change to active once someone has verified it against the current codebase.
---
# Standards Bar (living)

**Status:** Canonical fleet bar -- this file, not a dated snapshot
**Hub:** [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md)
**Source of truth for ports:** [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)

> Why no date in this filename: dated snapshots (`JUNE_2026_*`, `SEPT_2026_*`)
> rot the moment the month turns and force every referrer to guess which one is
> current. This file is the living bar. Dated files under `standards/` are
> frozen snapshots for archaeology only -- see
> [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md). New guidance lands
> here with a version line at the bottom, not in a new filename.

---

## 1. Pure-Rust ArtCraft Track (Primary for Bucket A & B Repos -- 2026-10-17+)

See **[RUST_ARTCRAFT_STANDARD.md](./RUST_ARTCRAFT_STANDARD.md)** for the full specification and invalidation matrix. For any repo with a root `Cargo.toml` (piloted by [`rust-devices-mcp`](../projects/rust-devices-mcp/README.md)):

| Topic | Pure-Rust ArtCraft Bar |
|-------|------------------------|
| **Architecture** | **3-Tier Cargo Workspace (`resolver = "2"`)**: L1 `<domain>-core` (`Command::dispatch`, protocols, zero UI/MCP deps) -> L2 `<domain>-mcp` (`clap` `--json` CLI + `mcp` stdio subcommand) -> L3 `<domain>-app` (Tauri v2 calling L1 directly in-process). |
| **Zero-Panic Lint Gate** | `clippy::unwrap_used`, `clippy::expect_used`, `clippy::panic`, `clippy::unimplemented`, `clippy::todo` all set to **`deny`** in workspace and crate headers. `cargo clippy --workspace --all-targets --all-features -- -D warnings` must be clean. |
| **MCP Transport** | **MCP `2024-11-05` over `stdio`** (`run_mcp_stdio`). **Stdout is 100% pure JSON-RPC**; all logs go to `stderr` (`eprintln!`). Zero `rmcp` dependency required. |
| **Desktop / Ports** | **Zero localhost HTTP sidecar ports.** L3 calls L1 in-process (`#[tauri::command]`). `WEBAPP_PORTS.md` and `STARLETTE_NO_PYDANTIC_STANDARD.md` do **not** apply to Pure-Rust repos. |
| **Crate Selection** | **Direct-Protocol Preference:** Use `reqwest`, `serde_json`, `tokio`, `rusqlite`, `tokio-serial`, `windows-sys` directly in L1 rather than pulling unmaintained `0.0.x` wrapper crates from `crates.io`. |
| **Automation & Locks** | Root `justfile` with explicit `$env:USERPROFILE\.cargo\bin` PATH prefix; **`Cargo.lock` committed**. |

---

## 2. Python / FastMCP Track (Bucket C & D Repos + Unconverted Legacy Fleet)

> **Scope note (2026-10-17):** The rules below apply **only** to Python-based MCP servers (`pyproject.toml` at root, e.g., Bucket D PyTorch/CUDA repos or unconverted legacy servers). Never enforce FastMCP, Ruff, Starlette, or port-claiming rules on a Pure-Rust repo.

| Topic | Bar |
|-------|-----|
| **FastMCP** | **3.4.4+** -- `fastmcp>=3.4.4,<5`, `prefab-ui>=0.14.0` core dep. Current SOTA: **4.0.5** (verified against PyPI 2026-09-18; 3.4.3 had Host/Origin guard regression -- skip it, 3.4.4 is the fix; 4.x is now the live major). **New repos MAY target 4.0.x** with MRTR awareness, or stay on 3.4.4+ -- both pass the gate. Existing repos on 3.2.x may stay until active work touches their deps. |
| **Sampling** | **Permitted through the grace window (~2027-07).** The MCP 2026-07-28 spec formally deprecates sampling/roots in favour of MRTR, with a ~12-month removal window. `ctx.sample()` keeps working, Claude still supports it, and fleet gates MUST NOT fail a repo merely for using it -- flag at most INFO. New work should know the MRTR replacement exists (see `fastmcp/2026-07-28-spec-migration.md`) but is not forced onto it while the window is open. |
| **Packaging** | **MCPB** (`mcpb pack`) -- **no DXT** -- [DXT_DEPRECATION.md](./DXT_DEPRECATION.md) |
| **Python** | **uv** + `pyproject.toml` + committed `uv.lock` |
| **Automation** | Root **justfile**; `uv run python` never naked `python` |
| **LLM manifests** | **`llms.txt` + `llms-full.txt`** pair |
| **Discovery** | **`glama.json`** at repo root |
| **Webapp ports** | Adjacent FE/BE pair from the reservoir -- **do not restate the range here**, it drifts as the fleet grows. Check the actual current range and register your pair in [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md), the sole source of truth (currently 10700-12000; widened 2026-09-10). |
| **UI in chat** | Prefab for list / status / stats tools -- [SOTA_REQUIREMENTS.md §2.2](./SOTA_REQUIREMENTS.md) |
| **Concurrency** | [fastmcp-3.2-concurrency.md](./fastmcp-3.2-concurrency.md) universal connect pattern |
| **JS package manager** | **Bun** replaces npm -- [BUN_STANDARDS.md](./BUN_STANDARDS.md) |
| **Linting** | **Ruff 0.16.x** (current 0.16.8, verified 2026-09-18) -- the pinned `ruff-pre-commit` rev in `.pre-commit-config.yaml` MUST equal the ruff version `uv run ruff` resolves from the venv (dev dependency), and both are updated together. Never run a bare global `ruff.exe` against a repo as the source of truth -- only the repo's own pinned version (`just lint` = `uv run ruff check .`, or the pre-commit hook) counts as the gate. |

---

## Retired / Superseded

- **Python/FastMCP/Starlette sidecars for Bucket A & B repos** (superseded 2026-10-17 by [RUST_ARTCRAFT_STANDARD.md](./RUST_ARTCRAFT_STANDARD.md))
- **FastMCP 2.12 / 2.14.x / any 2.x** as minimum version (superseded; do not use)
- **DXT** packaging (`.dxt`, `dxt.json`, `@anthropic/dxt`)
- **Poetry** for new MCP repos
- **FastMCP 3.1.0** as fleet minimum (superseded by 3.2+)

---

## Version

**Version:** 2026-10-17 (added Pure-Rust ArtCraft primary track + Python invalidation scope; pilot `rust-devices-mcp`) · Owner: Sandra Schipal
