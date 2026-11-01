# MCP Server Saga — Index

**The fleet's war stories, migrations, and standards evolution** — June 2026 edition.

This is the narrative layer behind [AGENT_PROTOCOLS.md](../standards/AGENT_PROTOCOLS.md). Standards say what to do; saga docs say what broke when we didn't.

---

## Canonical entry points

| Saga | Doc | Era |
|------|-----|-----|
| **GitHub CI/CD marathon** | [THE_GITHUB_SAGA.md](../not-mcp-related/git-github/github/THE_GITHUB_SAGA.md) | Advanced Memory MCP — 6.5h session, 20 bugs, quiet CI |
| **FastMCP 2.x → 3.2+** | [FASTMCP3_UPGRADE_STRATEGY.md](../standards/FASTMCP3_UPGRADE_STRATEGY.md) | Fleet rollout playbook |
| **FastMCP history** | [HISTORY_OF_FASTMCP.md](../standards/HISTORY_OF_FASTMCP.md) | 1.x through 3.x timeline |
| **DXT → MCPB purge** | [DXT_DEPRECATION.md](../standards/DXT_DEPRECATION.md) | June 2026 — DXT retired |
| **First-connection guarantee** | [MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md](../standards/MCP_SERVER_FIRST_TIME_SUCCESS_GUARANTEE.md) | STALE — ideas valid, verify against 3.2+ |
| **3.2 upgrade status** | [fastmcp-3.2-upgrade-status.md](../status/fastmcp-3.2-upgrade-status.md) | Repo-by-repo upgrade log |
| **Chip-design wipe incident** | [GIT_REPOSITORY_SAFETY.md](../standards/GIT_REPOSITORY_SAFETY.md) | Git before batch edits |
| **June 2026 bar** | [JUNE_2026_STANDARDS_BAR.md](../standards/JUNE_2026_STANDARDS_BAR.md) | Current snapshot |
| **FastMCP 4 / MRTR probe** | [MCP4_MRTR_PROBE_CASE_REPORT.md](./MCP4_MRTR_PROBE_CASE_REPORT.md) | 2026-08-02 — CD does NOT implement MRTR; fleet stays on 3.x |
| **CUA-NSIS smoke test learns to walk** | [CUA_NSIS_SAGA.md](./CUA_NSIS_SAGA.md) | 2026-08-02 — 6-phase fake pass → 162-repo title-matching nav sweep |

---

## Packaging saga (DXT is over)

| Phase | Format | Status |
|-------|--------|--------|
| 2024–2025 | DXT (`.dxt`) | **Retired** — do not document |
| 2025–2026 | MCPB (`.mcpb`) | **Current** — [MCPB_PACKAGING_STANDARDS.md](../standards/MCPB_PACKAGING_STANDARDS.md) |
| Fleet discovery | `glama.json` + `llms.txt` pair | **Current** |

Project CHANGELOGs that say "Complete DXT Purge" or "Migrated DXT → MCPB" are historical receipts — not instructions to ship DXT.

---

## Integration & tools shelf

| Shelf | Index |
|-------|-------|
| **59-service integration catalog** | [integrations/README.md](../integrations/README.md) |
| **Dev tools** (OpenCode, zoo analyzer) | [tools/README.md](../tools/README.md) |
| **AI tool assessments** | `integrations/*.md`, `tools/OPENCODE.md` |
| **Zed / Cursor / Windsurf** | `integrations/zed/`, `ecosystem/cursor/` |

---

## Project-level migration receipts

Search `projects/*/CHANGELOG.md` for:

- `DXT` — historical purge lines only
- `FastMCP 3.1` / `FastMCP 3.2` — upgrade receipts
- `MCPB` — current packaging

**Robofang mirror docs** (`projects/robofang/mcp-servers/`) — being updated to 3.2+; treat as secondary to live repo READMEs.

---

## Public publish

MCP saga + standards + integrations + tools **stay in** [sandraschi-collected-docs](https://github.com/sandraschi/sandraschi-collected-docs) (planned public). See [WEED_MANIFEST.md](../WEED_MANIFEST.md).

---

*Standards are the map. Saga is the blood on the trail.*
