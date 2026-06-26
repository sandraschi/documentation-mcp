# MCPB package for Docs MCP

Build from **repo root**:

```powershell
npx mcpb pack . dist/docs-mcp.mcpb
```

Or with npm-installed CLI:

```powershell
mcpb pack . dist/docs-mcp.mcpb --no-sign
```

- **manifest.json** – MCPB manifest (server entry: `python -m docs_mcp.stdio_main`, PYTHONPATH=src).
- **assets/prompts/** – system.md, user.md, examples.json for Claude Desktop.

Source is in `../src/docs_mcp/`. The pack tool should include `src/` and `mcpb/` (or merge assets to bundle root per your CLI). Exclusions: see root `.mcpbignore`.
