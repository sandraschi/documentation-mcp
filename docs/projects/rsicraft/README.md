# RSICraft

**Version**: v0.1.0 — Recursive Self-Improvement & Model Fine-Tuning Studio.
**Repository**: [`d:\Dev\repos\rsicraft`](file:///d:/Dev/repos/rsicraft) | [GitHub: sandraschi/rsicraft](https://github.com/sandraschi/rsicraft)
**Parent Suite**: Sovereign Craft Suite / AI

---

## Features & Architecture

```
rsicraft-core (Transactional Store / Card Recompute / Sandbox Runner)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
  rsicraft-mcp (L1/L2)                         rsicraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 GPU Training Studio)
```

- **ArtCraft 3-Crate Standard**: Strict Rust 1.85+, zero-panic containment, and Docker execution sandbox.
- **Card-Based Evolution**: Iterative prompt and model parameter optimization cards with transactional history in SQLite.
- **MCP 2024-11-05 Stdio Server**: Direct tool-call integration for autonomous self-improving agents.
