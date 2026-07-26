# External reference repos (not submodules)

Vendored clones for comparison and selective porting. Do not treat as fleet dependencies.

| Path | Upstream | Purpose |
|------|----------|---------|
| [mcp-libre](./mcp-libre/) | [jwingnut/mcp-libre](https://github.com/jwingnut/mcp-libre) | UNO extension MCP on `:8765`; spreadsheet read pattern ported to `spreadsheet_read.py` |

Update clone:

```powershell
Set-Location D:\Dev\repos\external\mcp-libre
git pull
```

License: check upstream `LICENSE` before copying code into libreoffice-mcp.
