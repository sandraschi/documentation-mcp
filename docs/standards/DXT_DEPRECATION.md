# DXT Packaging — Deprecated (June 2026)

**Status:** RETIRED fleet-wide  
**Effective:** 2026-06-17  
**Replaces:** All DXT (`.dxt`) distribution guidance

---

## Rule

**Do not document, scaffold, or ship DXT packages.** DXT is legacy Anthropic Desktop extension packaging. The fleet standard is **MCPB** only.

| Legacy | Current (June 2026) |
|--------|---------------------|
| `dxt pack` / `package_dxt.ps1` | **`mcpb pack`** per [MCPB_PACKAGING_STANDARDS.md](./MCPB_PACKAGING_STANDARDS.md) |
| `@anthropic/dxt` CLI | **MCPB CLI** (`npx @anthropic-ai/mcpb`) |
| `dxt.json` manifest | **`mcpb/manifest.json`** |
| `*.dxt` artifacts in `dist/` | **`.mcpb`** bundles; add `*.dxt` to `.gitignore` |

---

## Doc hygiene

When editing project READMEs or CHANGELOGs:

1. **Remove** "Option 4: DXT Package" install sections — replace with MCPB or `uvx` / stdio.
2. **Historical CHANGELOG lines** may mention DXT purge — keep as history, do not reintroduce instructions.
3. **Badges** `DXT Compatible` → remove or replace with MCPB.
4. **Grep before publish:** `\bDXT\b`, `\.dxt`, `@anthropic/dxt`, `package_dxt`

---

## FastMCP version (paired rule)

**Minimum FastMCP: 3.2+** for all new and updated server docs. **Do not cite FastMCP 2.12, 2.14.x, or 2.x** as current — see [JUNE_2026_STANDARDS_BAR.md](./JUNE_2026_STANDARDS_BAR.md).

FastMCP 2.x references belong only in [HISTORY_OF_FASTMCP.md](./HISTORY_OF_FASTMCP.md) (historical) or [FASTMCP3_UPGRADE_STRATEGY.md](./FASTMCP3_UPGRADE_STRATEGY.md) (migration).

---

## Related

- [PACKAGING_STANDARDS.md §5](./PACKAGING_STANDARDS.md)
- [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md)
- [operations/MCP_SERVER_SAGA_INDEX.md](../operations/MCP_SERVER_SAGA_INDEX.md) — DXT → MCPB migration war stories
