# secrets-mcp

**P1 minesweeper** — fleet credential vault bridge. Bitwarden CLI, static audit, fingerprint-only resolve.

## Quick start

```powershell
Set-Location D:\Dev\repos\secrets-mcp
uv sync
Copy-Item secrets-registry.example.yaml secrets-registry.yaml
uv run secrets-mcp
```

## Tool

`secrets_ops(operation=health|list_refs|resolve|audit_repo|audit_fleet|help)`

**Security:** `resolve` returns fingerprint only, never the raw value.

## Ports (planned web_sota)

Backend **11026**, frontend **11027** — Phase 2 (11024/11025 reserved by vla-mcp).

## Spec

[mcp-central-docs operations/planning/specs/P1-secrets-mcp.md](https://github.com/sandraschi/mcp-central-docs/blob/main/operations/planning/specs/P1-secrets-mcp.md)
