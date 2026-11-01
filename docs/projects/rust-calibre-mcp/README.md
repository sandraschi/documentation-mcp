# Project Hub -- `rust-calibre-mcp`

**Repo:** `D:\Dev\repos\rust-calibre-mcp`
**Legacy Oracle:** `D:\Dev\repos\calibre-mcp` (`master@5abaad6`, untouched read-only)
**Status:** Production Ready -- Wave-0 `repconv` Reference Pilot (Completed 2026-10-18)

## Overview

`rust-calibre-mcp` is the first end-to-end fleet conversion built with the hardened **`repconv` Belt-and-Suspenders Standard** (`mcp-central-docs/patterns/REPCONV_SOP.md` + `scripts/New-RustArtcraftRepo.ps1`).

- **L1 (`crates/calibre-core`)**: Pure-Rust read-only SQLite engine (`rusqlite` `bundled`, `SQLITE_OPEN_READ_ONLY | SQLITE_OPEN_NO_MUTEX` + `5000 ms` `busy_timeout`), direct `full-text-search.db:books_text` scanner bypassing Calibre's custom `calibre` FTS5 C tokenizer, zero-config `import.rs` discovering local Calibre libraries via `%APPDATA%\calibre`, `bridge.rs`, and `llm.rs` (`gemma4:12b`).
- **L2 (`crates/calibre-mcp`)**: `clap` CLI (`--json`) + `MCP 2024-11-05` stdio server with 23 canonical `calibre.*` tools and dual-aliased routing for legacy FastMCP portmanteau tool names.
- **L3 (`crates/calibre-app`)**: Native `eframe`/`egui` 0.37 desktop application with 9 tabs (`Libraries`, `Books`, `Fulltext`, `Analytics`, `Chat`, `Crossconnect`, `Settings`, `Help`, `RawJson`), `Ctrl+Wheel` zoom, Sun/Moon theme toggle, and `--smoke` headless mode.

## Key Documents in Repo

- [`docs/CONVERSION_DOSSIER.md`](../../../rust-calibre-mcp/docs/CONVERSION_DOSSIER.md)
- [`docs/ASSESSMENT_2026_10_18.md`](../../../rust-calibre-mcp/docs/ASSESSMENT_2026_10_18.md)
- [`docs/CONVERSION_LOG.md`](../../../rust-calibre-mcp/docs/CONVERSION_LOG.md)
- [`HANDOVER.md`](../../../rust-calibre-mcp/HANDOVER.md)
