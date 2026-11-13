# DatabaseCraft — Project Overview & Architecture Hub

**Version**: v0.7.0 — Production-Ready Relational Canvas, In-Place Cell Editing, Column Resizing & Reordering, Compact Joins & CTO Watchdog
**Repository**: [`d:\Dev\repos\databasecraft`](file:///d:/Dev/repos/databasecraft) | [GitHub: sandraschi/databasecraft](https://github.com/sandraschi/databasecraft)
**Parent Suite**: Storytold ArtCraft Creative Suite
**Registered Control Port**: **`14113`** ([`operations/WEBAPP_PORTS.md`](../../operations/WEBAPP_PORTS.md))
**Parent Standard**: [`standards/RUST_ARTCRAFT_STANDARD.md`](../../standards/RUST_ARTCRAFT_STANDARD.md)
**Menu Bar Standard**: [`standards/rust-artcraft/CRAFT_MENU_BAR_STANDARD.md`](../../standards/rust-artcraft/CRAFT_MENU_BAR_STANDARD.md)
**Test Suite**: 34 unit & integration tests (100% green, 0 warnings)
**Safety Guarantee**: 100% Safe Rust • Zero Unsafe Blocks • Zero Panics (`clippy::unwrap_used` denied)

---

## 1. Executive Summary

**DatabaseCraft** is the pure-Rust relational database engine, Non-1NF spreadsheet perspective canvas, and dynamic data-merge platform built specifically for the **Storytold ArtCraft** creative desktop suite (PhotoCraft, VectorCraft, FilmCraft, DesignCraft, WordCraft, GridCraft, DeckCraft, CadCraft, FigCraft, LightCraft, PdfCraft, SoundCraft, EffectCraft).

DatabaseCraft bridges the chasm between **spreadsheets** (which cannot handle plural $1:N$ relations without VLOOKUP formula spaghetti) and **traditional SQL tools** (which duplicate parent rows via Cartesian join explosion).

Inspired by the MIT CSAIL *Relational Canvas* research (*SIEUFERD*) and commercialized by tools like Ultorg ($35/mo), DatabaseCraft brings **Non-1NF hierarchical perspectives** directly to desktop Rust:
1. **Nested Subqueries Without Row Duplication**: View Parent Entities, nested Invoices, and nested Line Items in a continuous spanned matrix grid.
2. **1-Click Relation Sprouting**: Discover forward ($N:1$) and reverse ($1:N$) foreign keys and sprout them into child tables with zero Cartesian explosion.
3. **Contextual Inline Rollups**: Real-time atomic aggregations (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`) calculated directly within parent headers.
4. **24/7 Executive CFO Cockpit**: Ultra-lightweight (sub-30MB RAM), zero-panic Rust engine running continuously on an executive's second monitor.
5. **CTO Resident Watchdog & Notification Bus**: Autonomous monitoring of database health, disk starvation, and quiescent table churn (e.g. unexpected mutations on static `employees` or `roles` tables) with 1-click remediation.
6. **Cross-Craft Dynamic Publishing**: Stream verified hierarchical data directly into **DesignCraft** catalogs, **DeckCraft** board slides, and **WordCraft** contracts over Plane 2 TCP on registered control port `14113`.

---

## 2. Ports & Control Plane

| Port | Service | Transport | Standard / Scope |
|:---|:---|:---|:---|
| **`14113`** | Control & Plane 2 Live Channel (`databasecraft --control 14113`) | Localhost TCP Loopback | Registered in `WEBAPP_PORTS.md` |
| **`stdio`** | Model Context Protocol (`MCP 2024-11-05`) | Line-delimited JSON-RPC 2.0 | Agent tool catalog (29 tools) |

---

## 3. Four-Crate System Architecture

Following the **ArtCraft Containment Harness** ([`standards/rust-artcraft/CONTAINMENT_AND_CRATES.md`](../../standards/rust-artcraft/CONTAINMENT_AND_CRATES.md)):

```
                                databasecraft-store (L1)
             (Zero-Panic rusqlite WAL / Vector Math / FTS5 Hybrid Search)
                                           ^
                                           │
                                databasecraft-core (L1)
             (Non-1NF Canvas Compiler, Relation Sprouter, Watchdog, Bus)
                                           ^
                     ┌─────────────────────┴─────────────────────┐
                     │                                           │
           databasecraft-mcp (L2)                      databasecraft-app (L3 GUI)
         (FastMCP Stdio Server & CLI)                   (egui 0.37 Native Studio)
```

### Layer Specifications
* **`crates/databasecraft-store` (L1)**: Local-first relational storage wrapping `rusqlite` in WAL mode with foreign keys and busy timeouts. Pure-Rust SIMD-friendly dense vectors (`Cosine`, `DotProduct`, `L2`), FTS5 BM25 text search, and zero-panic error handling.
* **`crates/databasecraft-core` (L1)**: Non-1NF Relational Canvas perspective AST (`CanvasSpec`), SQLite 3.38+ `json_group_array(json_object(...))` query compiler, schema adjacency resolver (`SchemaRelationsResolver`), quiescent mutation tracker, bounded ring-buffer notification bus, and cross-craft merge export generators.
* **`crates/databasecraft-mcp` (L2)**: Single binary providing 29 typed MCP tools over line-delimited stdio JSON-RPC 2.0 (`MCP 2024-11-05`) and human-friendly CLI subcommands (`--json`).
* **`crates/databasecraft-app` (L3)**: Native GPU desktop workstation (`egui 0.37` / `wgpu`) with 11 integrated workspaces, top 8-menu bar, 5-dialog Help suite, continuous spreadsheet matrix, and live control socket.

---

## 4. Key Capabilities & Delivery Matrix

| Capability | Description | Status |
|:---|:---|:---|
| **Non-1NF Relational Canvas** | Compiles nested visual perspective ASTs into high-performance SQLite 3.38+ JSON queries without Cartesian row inflation. | ✅ Complete |
| **Interactive Column Resizing** | Dynamic drag-to-resize divider handles (6px hit zone) on column headers, synchronized column widths from headers down all data rows, and double-click reset. | ✅ Complete |
| **Drag-and-Drop Column Reordering** | Intuitive header drag-and-drop with floating drag badges, animated electric cyan drop guidelines, and instant AST column permutation. | ✅ Complete |
| **In-Place Cell Editing & Undo/Redo** | Double-click cell mutation with atomic primary key write-back, multi-step Undo/Redo stack, and quiescent table audit logging. | ✅ Complete |
| **Compact Joins (FK Inlining)** | Inlines referenced display labels (e.g. `customers.company_name` for `orders.customer_id`) via scalar subqueries without sprouting child table hierarchies. | ✅ Complete |
| **Interactive Tri-State Sorting** | Header click sorting (`ASC` -> `DESC` -> `None`) with visual glyphs (`▲`, `▼`), recompiling perspective AST in sub-milliseconds. | ✅ Complete |
| **Typographic Smart Cell Formatter** | Type-aware in-cell formatting: currency commas (`$1,850.00`), delivery/order status pill badges (`[DELIVERED]`, `[PROCESSING]`), and monospace dates. | ✅ Complete |
| **CTO Resident Watchdog** | Proactive monitoring of disk starvation, WAL growth envelopes, and quiescent table mutation churn (>10 mut/min) with 1-click remediation. | ✅ Complete |
| **Craft Notification Bus** | Thread-safe bounded ring buffer with severity classifications (`info`, `warning`, `critical`, `disaster`) and dynamic top-bar alert badge. | ✅ Complete |
| **Universal Craft 8-Menu Bar** | Top menu bar (`File`, `Edit`, `View`, `Insert`, `Modify`, `Commands`, `Window`, `Help`) strictly adhering to `CRAFT_MENU_BAR_STANDARD.md`. | ✅ Complete |
| **Mandatory 5-Dialog Help Suite** | Modal overlays for Command Palette (`Ctrl+K`/`Ctrl+Shift+P`), Keyboard Shortcuts (`F1`/`Ctrl+/`), Project Docs, Licenses & Notices, and About DatabaseCraft. | ✅ Complete |
| **Reference Commercial Datasets** | Turnkey seeds: Northwind Traders 3-tier deep relations (`customers -> orders -> order_items`), Ecommerce Catalog, Film Production, and Executive KPIs. | ✅ Complete |
| **29 FastMCP Tools & CLI** | Complete tool catalog mirroring `Command::dispatch` operations over stdio and command-line subcommands. | ✅ Complete |
| **Cross-Craft Merges** | Formats verified relational data slices for DesignCraft catalogs, DeckCraft slides, WordCraft letters, GridCraft sheets, and PdfCraft ledgers. | ✅ Complete |

---

## 5. Verification Commands

```powershell
# Run all 34 automated unit & integration tests
cargo test --manifest-path "d:\Dev\repos\databasecraft\Cargo.toml"

# Run clippy across all workspace crates and targets (0 warnings required)
cargo clippy --manifest-path "d:\Dev\repos\databasecraft\Cargo.toml" --all-targets

# Run headless smoke verification without GPU window
cargo run --manifest-path "d:\Dev\repos\databasecraft\Cargo.toml" -p databasecraft-app -- --smoke

# Launch native desktop application on registered control port 14113
cargo run --manifest-path "d:\Dev\repos\databasecraft\Cargo.toml" -p databasecraft-app -- --control 14113
```

---

## 6. Multi-App Production Flows

Registered in [`patterns/CRAFT_MULTI_APP_FLOWS.md`](../../patterns/CRAFT_MULTI_APP_FLOWS.md):

* **Flow 13: Product Catalog Factory**
  `db:product-query (14113)` -> `photo:plate-grade (14109)` -> `design:print-spread (14102)` -> `pdf:portfolio (14108)`
* **Flow 14: Film Production Asset Logger**
  `db:call-sheet-query (14113)` -> `sound:ident-jingle (14110)` -> `film:timeline-cut (14105)` -> `pdf:portfolio (14108)`
* **Flow 15: Executive Board Metric Deck**
  `db:revenue-kpis (14113)` -> `grid:homepage-grid (14106)` -> `deck:pitch-deck (14101)` -> `pdf:portfolio (14108)`
