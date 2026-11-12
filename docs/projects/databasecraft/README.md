# DatabaseCraft

**Version**: v0.5.0 — L1 SQLite & Relational Storage Engine with Vector Embeddings.
**Repository**: [`d:\Dev\repos\databasecraft`](file:///d:/Dev/repos/databasecraft) | [GitHub: sandraschi/databasecraft](https://github.com/sandraschi/databasecraft)
**Parent Suite**: Sovereign Craft Suite

---

## Ports

| Port | Service | Assigned Date |
|------|---------|---------------|
| `14113` | Control & UI Port (`databasecraft --control 14113`) | 2026-10 |

---

## Architecture

```
                              databasecraft-store
             (Zero-Panic rusqlite WAL / Vector Math / FTS5 Hybrid Search)
                                       ^
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
       databasecraft-mcp (L1/L2)                   databasecraft-app (L3 GUI)
     (FastMCP Stdio Server & CLI)                   (egui 0.37 Native Studio)
```

- **`crates/databasecraft-store`**: Shared L1 SQLite storage engine powering CoderCraft, DevCraft, and AICraft. Provides zero-panic wrappers, vector similarity metrics (cosine, dot, L2), and FTS5 hybrid search.
- **`crates/databasecraft-core`**: Schema migration, query builder, and relational modeling abstractions.
- **`crates/databasecraft-mcp`**: FastMCP stdio server and CLI.
- **`crates/databasecraft-app`**: Native immediate-mode egui desktop studio with table inspector and SQL console.
