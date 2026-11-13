# BookCraft

**Version**: v0.1.0 — Pure-Rust Calibre Library Manager, Ingestion & Conversion Engine.
**Repository**: [`d:\Dev\repos\bookcraft`](file:///d:/Dev/repos/bookcraft) | [GitHub: sandraschi/bookcraft](https://github.com/sandraschi/bookcraft)
**Parent Suite**: Sovereign Craft Suite / Literature & Media

---

## Features & Architecture

```
bookcraft-core (Calibre metadata.db Parser / EPUB Engine / Format Converter)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
  bookcraft-mcp (L1/L2)                        bookcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 Reader & Library Manager)
```

- **Consolidates Fleet Repos**: `calibre-mcp`, `calibops`, `buchcraft`.
- **Pure-Rust Calibre Engine**: Direct parsing and manipulation of `metadata.db` SQLite files without Calibre daemon dependencies.
- **Three Unified Surfaces**: `bookcraft-cli` for shell scripts, FastMCP server for agents, and native desktop studio for reading and shelf management.
