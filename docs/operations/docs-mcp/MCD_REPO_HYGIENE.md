# MCD repository git hygiene

**Priority:** P2  
**Repo:** mcp-central-docs

---

Decide on untracked working-tree items:

| Path | Decision needed |
|------|-----------------|
| `data/` | `.gitignore` (host-specific) or commit |
| `scratch/` | `.gitignore` |
| `src/docs_mcp/data/webapp_settings.json` | commit if shared config, else document override path |

`webapp_settings.json` was edited in the Ollama pass — ensure tracked or documented as local-only.
