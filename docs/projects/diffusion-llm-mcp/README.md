# diffusion-llm-mcp — Fleet Project (MCD stub)

**Status:** Active (June 2026)  
**Repo:** https://github.com/sandraschi/diffusion-llm-mcp  
**Type:** MCP Server — discrete diffusion / dLLM inference  
**Ports:** Frontend **10834**, backend **10835**  
**FastMCP:** **3.2+** (planned sidecar)  
**Hardware:** Goliath (RTX 4090 24 GB)

---

## Role

Catch-the-all **dLLM slot** — complements [local-llm-mcp](./local-llm-mcp/README.md) (AR/Ollama). Routes batch/frontier-shaped work when HLE-weighted assessment favors diffusion over autoregression.

## Deep assessment (MCD)

| Doc | Purpose |
|-----|---------|
| [diffusiongemma/](./diffusiongemma/README.md) | Model assessment archive |
| [diffusiongemma/HLE_AND_CAIS.md](./diffusiongemma/HLE_AND_CAIS.md) | HLE, priesthood, Scotsman, Butlerian |

## Operational docs (fleet repo)

PRD, architecture, Windows scaffold, fleet integration — live in the **GitHub repo** `docs/` folder (not duplicated here until Phase 1 ships).

---

*MCD page — refresh when FastMCP sidecar lands.*
