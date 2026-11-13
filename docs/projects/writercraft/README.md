# WriterCraft

**Version**: v0.1.0 — Distraction-Free Prose & Long-Form Literary Studio.
**Repository**: [`d:\Dev\repos\writercraft`](file:///d:/Dev/repos/writercraft) | [GitHub: sandraschi/writercraft](https://github.com/sandraschi/writercraft)
**Control Port**: `14121` (`writercraft --control 14121`)
**Parent Suite**: Sovereign Craft Suite / Literature

---

## Features & Architecture

```
writercraft-core (Markdown AST / Prose Linter / Word Statistics / Outliner)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
writercraft-mcp (L1/L2)                       writercraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 Minimalist Prose Canvas)
```

- **Consolidates Fleet Repos**: `notion-mcp`, `obsidian-mcp`.
- Typewriter mode, automated word count goals, chapter reordering.
- Prose quality linter (passive voice detection, readability indexes).
