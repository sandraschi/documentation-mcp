# FastMCP 3.2 — Fleet Capability Map

**Last updated:** 2026-06-06  
**Standard:** FastMCP 3.4.2 (fleet target); 3.2.0 GA baseline documented in [3.2-features.md](3.2-features.md)  
**New in 3.4:** [3.4-features.md](3.4-features.md) — remote bridge, fail-loud proxies, returnable errors  
**Audience:** MCP server authors, fleet maintainers, architects  

The FastMCP 3.2 GA stack introduces declarative **providers**, **transforms**, **prompts**, **bundled skills**, **CodeMode**, and high-fidelity **Generative UI** through Prefabs. This document maps these capabilities to practical use cases, pointing to the authoritative 3.2 SOTA guides.

---

## 1. Complexity Ladder (April 2026)

From **baseline** to **fully autonomous orchestration**:

```
  Easy Wins ──────────────────────────────────────────────► Advanced / Agentic
  
  Decorator Tools + 3-4-100 docstrings
       → Prompts (@mcp.prompt) + Bundled Skills (skill://)
       → Generative UI / Prefab (Rich in-chat dashboards)
       → Transforms (Namespace, Rename, Visibility)
       → Providers (FileSystem, OpenAPI, Proxy)
       → Agentic Sampling (ctx.sample() — borrow client LLM)
       → CodeMode (Semantic Discovery for 50+ tool catalogs)
```

**Fleet Default**: Most `*-mcp` repos should use **Namespaced Tools** + **3-4-100 docstrings** + **Vanishing Args**. Add **Prompts/Skills** for expert guidance. Reach for **CodeMode** or **Sampling** only when solving specific scaling or autonomous reasoning problems.

---

## 2. Master Table — Capability → Use Case → Doc

| Capability | Use when... | Avoid when... | Complexity | Primary SOTA Doc |
|------------|--------------|--------------|------------|--------------|
| **`@mcp.tool()`** | Core tool surface for the server. | — | Baseline | [tool-documentation.md](tool-documentation.md) |
| **Namespaces** | Grouping sub-services (Portmanteau V2). | Tiny servers (<5 tools). | Low | [portmanteau-v2-managed-namespaces.md](portmanteau-v2-managed-namespaces.md) |
| **`@mcp.prompt()`** | You need discoverable "System Blueprints". | README instructions suffice. | Low | [skills-and-prompts.md](skills-and-prompts.md) |
| **Skills Provider** | Exposing portable `.md` checklists/expertise. | A single prompt suffices. | Low–Medium | [skills-and-prompts.md](skills-and-prompts.md) |
| **Prefab UI** | In-conversation cards/tables/dashboards. | Heavy forms or multi-tab UIs. | Medium | [generative-ui-prefabs.md](generative-ui-prefabs.md) |
| **Transforms** | Federated prefixing (`NamespaceTransform`). | Single flat server. | Medium | [providers-and-transforms.md](providers-and-transforms.md) |
| **Providers** | Sourcing from Filesystem or OpenAPI specs. | Manual registration is faster. | Medium | [providers-and-transforms.md](providers-and-transforms.md) |
| **Agentic Sampling** | Autonomous orchestration of multi-step tools. | Deterministic tasks only. | **High** | [agentic-sampling.md](agentic-sampling.md) |
| **CodeMode** | Very large (50+) tool catalogs. | Metadata proliferation is low. | **High** | [codemode-discovery.md](codemode-discovery.md) |
| **LifeSpan/Probes** | Verifying DB connectivity on startup. | Purely local stateless tools. | Low | [persistent-storage.md](persistent-storage.md) |

---

## 3. Recommended Combinations

### 3.1 The Industrial Standard (`*-mcp`)
- **V3 Docstrings**: 3-4-100 rule + **Vanishing Args** (`Annotated`).
- **Managed Namespaces**: `mcp.mount(subapp, namespace='...')`.
- **Prefab UI**: Mandatory for any `list` or `status` tool.

### 3.2 The Autonomous Agent
- **Sampling Meta-Tools**: `agentic_` prefix tool calling `ctx.sample()`.
- **CodeMode**: Enabled to manage discovery if wrapping external proxies.
- **Prompts**: `database_expert`-style guidance for the orchestrated LLM.

---

## 4. Study Order for Maintainers

1.  **[tool-documentation.md](tool-documentation.md)** — Foundations (Rules of 3-4-100).
2.  **[portmanteau-v2-managed-namespaces.md](portmanteau-v2-managed-namespaces.md)** — Architectural grouping.
3.  **[skills-and-prompts.md](skills-and-prompts.md)** — Knowledge distribution.
4.  **[generative-ui-prefabs.md](generative-ui-prefabs.md)** — Visualization.
5.  **[providers-and-transforms.md](providers-and-transforms.md)** — Composition.
6.  **[agentic-sampling.md](agentic-sampling.md)** — Autonomy.
7.  **[codemode-discovery.md](codemode-discovery.md)** — Scaling.

---

## References
- [SOTA_REQUIREMENTS.md](../standards/SOTA_REQUIREMENTS.md)
- [TOOL_DESIGN_STANDARDS.md](../standards/TOOL_DESIGN_STANDARDS.md)
- [3.2-features.md](3.2-features.md)
eration-hub**, **robofang** vs FastMCP **`ProxyProvider`** only; leaf servers (e.g. **calibre-mcp**) stay domain-focused. |
| 2026-03-28 | Initial fleet capability map: complexity ladder, master table, patterns, study order, cross-links. |
