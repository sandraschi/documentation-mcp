# Craft Brochure Asset Standard (`docs/brochure/`)

**Status:** Normative (2026-11-09)
**Owner:** Sandra S. + Fleet Agents
**Toolchain:** `bookcraft-cli` (`D:\Dev\repos\bookcraft`) + Calibre `ebook-convert.exe`
**Reference Implementation:** `D:\Dev\repos\wincraft\docs\brochure\`

---

## 1. Purpose

Every Pure-Rust ArtCraft studio (`*craft`) in the fleet MUST ship a self-contained, magazine-grade **Technical Brochure & Operator Handbook** inside its repository at `docs/brochure/`.

Instead of scattering ad-hoc marketing slides or relying on external cloud tools, we dogfood our own **BookCraft** (`bookcraft-cli`, Grade A, 30 MCP tools) to ingest a print-and-e-reader-styled HTML5 + inline-SVG source document and compile deterministic **EPUB** and **PDF** brochures.

---

## 2. Standard File Layout

Every `*craft` repository MUST provide the following three files under `docs/brochure/`:

```text
<repo>/
└── docs/
    └── brochure/
        ├── <repo>-brochure.html   # Canonical HTML5 + inline SVG source (print & e-reader styled)
        ├── <repo>-brochure.epub   # Compiled via `bookcraft-cli convert --to epub`
        └── <repo>-brochure.pdf    # Compiled via `bookcraft-cli convert --to pdf`
```

---

## 3. Mandatory 5-Section Brochure Structure

Each `<repo>-brochure.html` MUST include:

1. **Cover Page (`.cover`):**
   - Series badge (`ArtCraft Fleet Technical Brochure · Series #N`)
   - Craft title, semantic version (`vX.Y.Z`), and one-sentence value proposition
   - **Inline vector SVG Architecture Diagram** showing L3 (`<name>-app`), L2 (`<name>-mcp`), and L1 (`<name>-core`) dataflow
   - 4-card KPI grid (Tool count, Crates/ Consolidation ratio, Idle daemon tax `0 MB`, Output formats)
2. **Section 1 — Executive Summary & Consolidation Scope:**
   - Which legacy Python/Node MCP servers or fragmented scripts this Craft app subsumes, and why it passes the ArtCraft fit test.
3. **Section 2 — Flagship Subsystems:**
   - 2x2 capability cards explaining the core engines, FFI bridges, or deterministic pipelines.
4. **Section 3 — Interactive Views, CLI & Export Engine:**
   - Documentation of the **Cards (Default) / List / JSON** switcher, live filtering, numeric-aware sorting, pagination, and `CSV` / `MD` / `TXT` / `JSON` export examples.
5. **Section 4 & 5 — Complete Tool Reference Matrix & Safety Invariants:**
   - Full table of all MCP tools / CLI verbs (`Read-Only` vs `Mutating`, `confirm=true` gates) and the repository's non-bypassable safety guards (`.bak` backups, `--read-only`, `--root` confinement).

---

## 4. Standard Build Pipeline (`bookcraft-cli`)

All Craft brochures are compiled through `bookcraft-cli` (`D:\Dev\repos\bookcraft`) using the fleet script `D:\Dev\repos\mcp-central-docs\scripts\build-craft-brochure.ps1`:

```powershell
# Compile or refresh docs/brochure/<repo>-brochure.{html,epub,pdf} for any craft repo:
pwsh -File D:\Dev\repos\mcp-central-docs\scripts\build-craft-brochure.ps1 -RepoPath D:\Dev\repos\wincraft
```

Under the hood, the script executes:
1. `bookcraft-cli --library <fleet-brochure-lib> init` (if not yet initialized)
2. `bookcraft-cli --library <fleet-brochure-lib> add-book --file <repo>-brochure.html --title "<repo>-brochure" --authors "Sandra S." --series "ArtCraft Fleet Brochures"`
3. `bookcraft-cli --library <fleet-brochure-lib> convert --id <id> --to epub --out-dir <repo>/docs/brochure`
4. `bookcraft-cli --library <fleet-brochure-lib> convert --id <id> --to pdf --out-dir <repo>/docs/brochure`

---

## 5. L3 Desktop App Integration

Every L3 `eframe`/`egui` desktop studio (`<name>-app`) SHOULD expose one-click **`📖 PDF Brochure`** and **`📚 EPUB Brochure`** buttons in its top header bar and Doctor/Help view that launch `docs/brochure/<repo>-brochure.pdf` and `docs/brochure/<repo>-brochure.epub` via the system viewer.
