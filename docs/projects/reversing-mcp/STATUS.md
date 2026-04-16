# Reversing MCP — status (fleet)

**Source of truth:** [sandraschi/reversing-mcp](https://github.com/sandraschi/reversing-mcp) · local `D:\Dev\repos\reversing-mcp`

## Snapshot

- **MCP:** FastMCP 3.1+; static analysis, heuristic DKI helpers, LLM config. **Does not ship ReVa tools** — ReVa is another server.
- **Ghidra:** Interactive work via **ReVa** MCP; optional headless `analyze_binary(..., ['ghidra'])` from the clone.
- **Digibib5 / DKI:** **Example test case** for small/medium apps — not a Word-sized decompile goal. Faithful `text.dki` decode: see upstream **DIGIBIB_DECOMPILE_PLAN.md**.
- **Webapp:** Ports **10750** / **10751** — [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md).

## Fleet docs in this folder

| File | Role |
|------|------|
| [README.md](./README.md) | Hub and upstream links |
| [CHANGELOG.md](./CHANGELOG.md) | Doc sync log for central-docs only |
| [DIGIBIB_STATUS.md](./DIGIBIB_STATUS.md) | **Mirror** of `reversing-mcp/docs/status.md` — Digibib5 / `Text.dki` ReVa notes + on-disk hex samples |

Older copies of marketing-style status text were removed in favor of the upstream **README.md** and **docs/** in the clone.
