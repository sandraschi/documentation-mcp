# bumi-mcp — Structure

**Authoritative tree:** clone [sandraschi/bumi-mcp](https://github.com/sandraschi/bumi-mcp).

```
bumi-mcp/
  src/bumi_mcp/
    __main__.py        # CLI --serve | --stdio
    app.py             # FastAPI + /mcp mount
    server.py          # FastMCP, tools, prompt, skills provider
    portmanteau.py     # bumi(operation=...)
    agentic.py         # bumi_agentic_workflow (sampling)
    knowledge.py       # BUMI_HERO, OSS links, virtual_twin map
    config.py          # pydantic-settings BUMI_MCP_*
    tools_manifest.py  # dashboard /api/tools
    data/fleet_default.json
    skills/bumi-operator/SKILL.md
  web_sota/            # Vite 10775 → proxy 10774
  tests/
  justfile
  llms.txt
  glama.json
```

This folder (`mcp-central-docs/projects/bumi-mcp/`) is the **central index**; behavior changes land in **GitHub bumi-mcp**.
