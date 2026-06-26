# bumi-mcp — Status

**Last updated:** 2026-03-20  
**Source repo:** [sandraschi/bumi-mcp](https://github.com/sandraschi/bumi-mcp)  
**Local path:** `D:/Dev/repos/bumi-mcp`

---

## Release channel

| Field | Value |
|-------|--------|
| **Version** | **0.1.0** |
| **PyPI** | *publish when ready* |
| **Ports** | **10774** backend · **10775** frontend |

---

## What works today

- **stdio MCP** — `bumi`, `bumi_agentic_workflow`, prompt `bumi_quick_start`, skill `bumi-operator`.
- **HTTP** — FastAPI `/api/*`, MCP streamable **`/mcp`**.
- **Web** — Vite glass dashboard (hero, virtual twin, fleet JSON, tools manifest).
- **CI** — Ruff + pytest (GitHub Actions).

---

## Honest gaps

| Area | State |
|------|--------|
| **Vendor motion API** | Not integrated — add when Noetix documents a stable local interface. |
| **PyPI** | Install from repo / path until published. |

---

## See also

- [README.md](./README.md)  
- [INTEGRATION.md](./INTEGRATION.md)  
- [RoboFang bumi-mcp.md](https://github.com/sandraschi/robofang/blob/main/docs/integrations/bumi-mcp.md)
