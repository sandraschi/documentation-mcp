# Fleet naming — disambiguation guide

**Last updated:** 2026-06-05  
**Rule:** Never use bare `vla` in fleet_bridge, workflows, or agent prompts without context.

---

## The collision

| Token | Meaning | Repo | fleet_bridge alias |
|-------|---------|------|-------------------|
| **ViLife** / **vienna-life** | Vienna Life Assistant — calendar, todos, expenses, meta dashboard | `vienna-life-assistant` | `vienna-life` |
| **vla-robotics** | Video-Language-Action — X Square Wall-OSS / robot agentic tools | `vla-mcp` | `vla-robotics` |

**Deprecated:** alias `vla` → resolves to `vla-robotics` only. It must **never** mean Vienna Life Assistant.

---

## Preferred terms in docs and code

| Context | Use | Avoid |
|---------|-----|-------|
| Life admin app | `vienna-life-assistant`, `vienna-life`, **ViLife** | `VLA` alone |
| Robotics MCP | `vla-mcp`, `vla-robotics`, **X-VLA** | `VLA` alone |
| UI sidebar badge | `Vienna Life` or `ViLife` | `VLA` (ambiguous) |
| MCP tool | `vienna_life` | `vla_*` |
| Ports | ViLife backend **10922**, frontend **10988** | — |
| Ports | vla-mcp backend **11024**, frontend **11025** | — |

---

## Ship class (naval doctrine)

- **vienna-life-assistant** = aircraft carrier (human flag bridge)
- **vla-mcp** = destroyer (robotics battlespace)

See [FLEET_PHILOSOPHY.md](FLEET_PHILOSOPHY.md).

---

## Deprecated repos

| Repo | Status | Replacement |
|------|--------|-------------|
| `vienna-live-mcp` | **quarantined** | `vienna-life-assistant` — same domain, one carrier |


---

## Agent prompt snippet

```
Life admin → fleet_call_tool(server="vienna-life", tool="vienna_life", ...)
Robotics VLA → fleet_call_tool(server="vla-robotics", tool="vla_pipeline", ...)
Never use server="vla" in new workflows; legacy alias maps to vla-robotics only.
```
