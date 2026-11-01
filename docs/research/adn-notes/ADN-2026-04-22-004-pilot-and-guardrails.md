# ADN-2026-04-22-004 — Pilot order and guardrails (Deep Research + MCP fleet)

**Date:** 2026-04-22  
**Scope:** Safe rollout before pointing “many” MCP servers at a hosted research agent.

## Pilot order

1. **Read-only** MCP with **no PII** (e.g. public docs mirror, static capability catalog).  
2. **Single** HTTPS endpoint via **Tailscale Funnel**; measure **cold start**, **request timeout**, and **retry** behavior on the agent side.  
3. Add **one** authenticated data source (still non-destructive tools).  
4. Only then attach **high-power** tools (filesystem, shell, finance, robotics).

## Guardrails

- **Tool manifests:** narrow descriptions; avoid dumping 50-server manifests into one interaction until **context caching / pruning** strategy is defined (see pricing page when implementing).  
- **Logging:** never log raw API keys or OAuth tokens in MCP access logs.  
- **Kill switch:** DNS or Funnel policy off switch for a misbehaving server without redeploying Gemini.

## Success criteria

- Repeatable **completed** interaction with **citations** preserved in downstream storage.  
- Documented **cost envelope** per run class (pilot vs production) from **official pricing**, not forum posts.

## Link

Hub: `../integrations/gemini-deep-research-interactions-2026.md`
