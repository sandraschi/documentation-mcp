# ADN-2026-04-22-005 — MetaMCP vs a new Gemini / Deep Research bridge

**Date:** 2026-04-22  
**Scope:** Where fleet-local Gemini Interactions + Deep Research orchestration should live.

## Decision

- **Keep using `meta_mcp` (MetaMCP)** for what it already owns: **fleet catalog**, health probes, **MASTER_MCP_CONFIG** alignment, scaffolding, **Tool Lab** execution against **registered** MCP nodes, and cross-repo diagnostics.  
- **Do not** fold Deep Research **client** logic (start interaction, stream or poll for 10–60 minutes, parse artifacts, map MCP URL tool configs) into MetaMCP’s core server as a default feature set. That couples two lifecycles: **Google API schema churn** and **fleet orchestration**.  
- **Add a separate, small artifact** when automation is needed: e.g. **`gemini-fleet-research`** (new repo) or **`meta_mcp/contrib/` scripts** that call the Interactions API and optionally **read** MetaMCP’s catalog export for MCP base URLs—without extending MetaMCP’s shipped tool surface until the API stabilizes.

## Rationale

MetaMCP is an **industrial control plane** for **your** MCP processes. A hosted Deep Research job is an **external orchestrator** with different auth, quotas, timeouts, and transport rules. Merging them in one binary increases regression risk and complicates security review (API keys, egress allowlists).

A **thin bridge** (few tools: `research_start`, `research_status`, `research_cancel`, optional `list_funnel_endpoints` from config) keeps blast radius small and lets you version the Google SDK independently of MetaMCP **3.2.x**.

## When MetaMCP alone is enough

If humans drive research from **AI Studio** or a **notebook**, and the fleet only needs **documentation** of URLs and patterns, **no new MCP** is required—use **mcp-central-docs** + **Advanced Memory** seed notes.

## Links

- MetaMCP hub: `../projects/meta_mcp/README.md`  
- Gemini hub doc: `../integrations/gemini-deep-research-interactions-2026.md`
