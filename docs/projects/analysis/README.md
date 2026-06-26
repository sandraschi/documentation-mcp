# Fleet repository analysis (MetaMCP)

Published snapshots from **MetaMCP** analysis tools — not hand-edited.

| Artifact | Description |
|----------|-------------|
| [INDEX.md](./INDEX.md) | Run history (regenerated on export) |
| [FLEET_RUNTS_LATEST.md](./FLEET_RUNTS_LATEST.md) | Latest MCP runt / SOTA scan (`analyze_mcp_runts`) |
| [FLEET_MULTIDIM_LATEST.md](./FLEET_MULTIDIM_LATEST.md) | Latest multi-dimensional fleet scan (`analyze_fleet`) |
| [latest.json](./latest.json) | Pointer to latest exported run |
| [runs/](./runs/) | Archived runs by UTC id |
| [repos/](./repos/) | Per-repo markdown copies |

## Refresh

From MetaMCP (stdio or Tool Lab):

1. `analyze_mcp_runts` with optional `scan_path` (default `REPOS_DIR` / `D:/Dev/repos`)
2. `publish_analysis_to_mcd` — or `analyze_mcp_runts` with `export_mcd=true`

Local depot (full history): `%USERPROFILE%\.meta_mcp\analysis\`

Override central docs root: `MCP_CENTRAL_DOCS_ROOT`.
