# Cua Driver (external) — fleet integration notes

**Product:** [Cua Driver](https://cua.ai/docs/cua-driver/guide/getting-started/introduction) · **Repo:** [trycua/cua](https://github.com/trycua/cua)  
**Fleet counterpart:** [pywinauto-mcp](../projects/pywinauto-mcp/README.md)

## Fleet stance

- **Not** a fleet-maintained MCP repo today.
- **pywinauto-mcp** is the integration point for host desktop automation (HTTP **10789**, bridge alias **`pywinauto`** in fleet-agent-mcp).
- Full comparison and Excel/Cursor/fleet-agent answers: **[CUA_DRIVER_AND_PYWINAUTO.md](../patterns/CUA_DRIVER_AND_PYWINAUTO.md)**.

## Quick install (reference)

```powershell
# Example — verify current install docs on cua.ai before production use
claude mcp add --transport stdio cua-driver -- cua-driver mcp
```

## Do not confuse with

| Name | What it is |
|------|------------|
| **Cua Driver** | Host background computer-use (this doc) |
| **cua-sandbox / Lume** | VM / isolation products from same org |
| **Claude Cowork** | Sandbox-first Claude desktop (different shape) |
