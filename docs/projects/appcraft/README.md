# AppCraft

**Version**: v0.1.0 — Sovereign Desktop Application Builder & Web Container.
**Repository**: [`d:\Dev\repos\appcraft`](file:///d:/Dev/repos/appcraft) | [GitHub: sandraschi/appcraft](https://github.com/sandraschi/appcraft)
**Control Port**: `14115` (`appcraft --control 14115`)
**Parent Suite**: Sovereign Craft Suite

---

## Features & Architecture

```
appcraft-core (Application Manifest / Window Harness / IPC Bridge)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
  appcraft-mcp (L1/L2)                         appcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (Native Application Shell / Multi-Window)
```

- Local-first application packaging and zero-latency window management.
- Standardized IPC event bus shared across all sovereign suite tools.
