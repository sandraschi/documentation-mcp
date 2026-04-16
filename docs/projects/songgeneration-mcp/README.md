# songgeneration-mcp (fleet index)

**GitHub:** [sandraschi/songgeneration-mcp](https://github.com/sandraschi/songgeneration-mcp)

**Local clone:** `D:\Dev\repos\songgeneration-mcp` (edit docs in the repo; this file is a fleet mirror).

## One-liner

**SongGeneration v2 (LeVo 2 / SG2)** MCP server: **local** open-weight music generation via SongGeneration-Studio—**dual-track** (`vocal.wav`, `inst.wav`), SG2 length tags, optional **~10 s** style prompt.

## vs Gemini Lyria 3 Pro (~Mar 2026)

- **Lyria 3 Pro**: Cloud, Gemini-integrated; often **~$0.08/track** in typical credit economics (**verify** pricing).
- **SG2 / LeVo 2**: **On-prem**; strong for **classical**, **rubato**, **instrumental** nuance; counterweight to **US-centric** commercial defaults—complements (not replaces) Google’s AI roadmap for many users.

Full PRD and comparison: repo `docs/PRD.md`, `docs/LYRIA_VS_SG2.md`; MCP resource `docs://lyria-vs-sg2`.

## Ports (fleet)

See `operations/WEBAPP_PORTS.md`: **10884** frontend, **10885** MCP HTTP (if used).
