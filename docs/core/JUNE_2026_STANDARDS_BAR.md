# June 2026 Standards Bar

**Status:** Canonical fleet snapshot  
**Effective:** 2026-06-17  
**Hub:** [AGENT_PROTOCOLS.md](./AGENT_PROTOCOLS.md) (SOTA v12.2)

---

## Non-negotiables (June 2026)

| Topic | Bar |
|-------|-----|
| **FastMCP** | **3.2+** minimum — `fastmcp>=3.2.0`, `prefab-ui>=0.14.0` core dep. Current SOTA: **3.4.x** (moves fast — pin with `<4` not exact version) |
| **Packaging** | **MCPB** (`mcpb pack`) — **no DXT** — [DXT_DEPRECATION.md](./DXT_DEPRECATION.md) |
| **Python** | **uv** + `pyproject.toml` + committed `uv.lock` |
| **Automation** | Root **justfile**; `uv run python` never naked `python` |
| **LLM manifests** | **`llms.txt` + `llms-full.txt`** pair |
| **Discovery** | **`glama.json`** at repo root |
| **Webapp ports** | **10700–10800** band + adjacent FE/BE — [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md) |
| **UI in chat** | Prefab for list / status / stats tools — [SOTA_REQUIREMENTS.md §2.2](./SOTA_REQUIREMENTS.md) |
| **Concurrency** | [fastmcp-3.2-concurrency.md](./fastmcp-3.2-concurrency.md) universal connect pattern |
| **JS package manager** | **Bun** replaces npm — [BUN_STANDARDS.md](./BUN_STANDARDS.md) |

---

## Retired (do not scaffold or cite as current)

- **FastMCP 2.12 / 2.14.x / any 2.x** as minimum version
- **DXT** packaging (`.dxt`, `dxt.json`, `@anthropic/dxt`)
- **Poetry** for new MCP repos
- **FastMCP 3.1.0** as fleet minimum (superseded by 3.2+)

---

## Public publish slice (`sandraschi-collected-docs`)

**Mandatory IN after update** (see [PUBLISH_UPDATE_CHECKLIST.md](../PUBLISH_UPDATE_CHECKLIST.md)):

| Shelf | Path |
|-------|------|
| **Projects** | `projects/` — entire fleet tree |
| **Integrations** | `integrations/` — refresh for new releases |
| **AI** | `not-mcp-related/general-ai/`, `not-mcp-related/development/`, `protoconsciousness/` |

Plus BUILD/SAGA: `standards/`, `fastmcp/`, `tools/`, `skills/`, `operations/`, `patterns/`, `ecosystem/`.

See [WEED_MANIFEST.md](../WEED_MANIFEST.md) for exclude/slim rules.

---

## Doc update checklist (June 2026 pass)

- [ ] README badges: FastMCP **3.2+**
- [ ] Remove DXT install options — [DXT_DEPRECATION.md](./DXT_DEPRECATION.md)
- [ ] `integrations/README.md` — service catalog current
- [ ] `skills/**` — no 2.14.3 minimums
- [ ] `projects/robofang/mcp-servers/*.md` — purge 2.12 references
- [ ] CHANGELOG new entries reference **3.2+** and MCPB only

---

**Version:** 2026-06-17 · Owner: Sandra Schipal
