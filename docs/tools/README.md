# MCP Development Tools

**Private — Sandra S. + collaborators only. Not for public distribution.**

**Last Updated:** 2026-06-17  
**Standards:** FastMCP **3.2+** · [JUNE_2026_STANDARDS_BAR.md](../standards/JUNE_2026_STANDARDS_BAR.md)

Tools for developing, testing, and analyzing MCP servers.

---

## 🔍 MCP Zoo Analyzer

Tool for analyzing MCP server quality and compliance against fleet standards (3.2+, MCPB, no DXT).

→ See [zoo-analyzer.md](zoo-analyzer.md)

---

## 🤖 Agentic IDE & CLI tools

| Tool | Doc |
|------|-----|
| **OpenCode** | [OPENCODE.md](./OPENCODE.md) — model-agnostic agent CLI; verify FastMCP 3.2 patterns per model |
| **Cursor** | [integrations/cursor-ide/](../integrations/cursor-ide/) |
| **Zed** | [integrations/zed/](../integrations/zed/) |

---

## 🧪 Testing & Diagnostic Tools

### MCP Inspector

Debug MCP connections and inspect messages.

### FastMCP Dev Mode

```powershell
uv run fastmcp dev server.py
```

### Wrapture (Diagnostic Sidecar & Host Testing)

Call-site binding, determinism assertions, and zero-code ad-hoc tracing.
- **Fleet Policy**: Dev/test utility & diagnostic sidecar only (no production fleet rollout).
- **Primary Use**: Testing C-extensions/Win32 APIs (`windows-operations-mcp`), fault injection stubs (`email-mcp`), and local hang debugging.

→ See [WRAPTURE.md](WRAPTURE.md)

---

## Related

- [fastmcp/README.md](../fastmcp/README.md) — FastMCP framework docs
- [operations/MCP_SERVER_SAGA_INDEX.md](../operations/MCP_SERVER_SAGA_INDEX.md) — migration war stories
- [integrations/README.md](../integrations/README.md) — 59-service fleet catalog
