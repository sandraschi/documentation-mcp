# [BUG-005] MCP Server Startup Failure (Race/Dependencies)

- **ID**: `BUG-005`
- **Severity**: `P3`
- **Date**: 2026-03-18
- **Repo/Component**: MCP Config / External Servers (Cursor/AG)

## Symptom
MCP server fails to start or crashes immediately upon initialization in Antigravity or Cursor.

## Root Cause
- **Missing Dependencies**: Python/Node packages not installed in the target environment.
- **Race Condition**: Server attempts to bind to a port or access a resource before it is ready.
- **Path Misconfiguration**: Relative paths used in config files that fail when launched from different IDE contexts.

## Resolution
1. **Dependency Audit**: Run `pip install` or `npm install` explicitly in the server directory.
2. **Absolute Paths**: Mandatory use of absolute paths in all `mcp_config.json` entries.
3. **Port Culling**: Added port culling logic to `start.ps1`.

## Log Snippet (Example)
```text
[SOTA-ERROR] MCP Server 'robotics-mcp' failed to start.
Error: Cannot find module 'fastmcp'
at Function.Module._resolveFilename (node:internal/modules/cjs/loader:1144:15)
at Function.Module._load (node:internal/modules/cjs/loader:1222:23)
```

## SOTA Impact
Updated [SOTA_REQUIREMENTS.md](../../standards/SOTA_REQUIREMENTS.md) to mandate absolute paths and pre-start dependency checks.
