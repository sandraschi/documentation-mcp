# ADN-2026-04-22-002 — Tailscale Funnel for remote MCP ingress

**Date:** 2026-04-22  
**Scope:** How this fleet should expose MCP HTTPS endpoints to Google-hosted agents.

## Decision

Prefer **Tailscale Funnel** (or equivalent Tailscale-approved HTTPS exposure) over **Cloudflare Tunnel** when a public URL is required for **remote MCP**, **unless** a project already standardizes on Cloudflare for compliance or DNS reasons.

## Rationale

- The fleet already standardizes on **Tailscale mesh** (`integrations/README.md` catalog).  
- Remote MCP needs **Google-reachable HTTPS**; the tunnel vendor is **not** prescribed by Google’s public blogs.  
- Centralizing on Tailscale reduces **secret sprawl** and keeps ingress policy next to **ACLs** operators already reason about.

## Constraints

- Funnel is a **public ingress surface**: apply **tool-level auth**, rate limits, and **least-privilege** MCP tool manifests.  
- Align MCP **transport** with whatever **Interactions API / remote MCP** requires on the day of deployment (see live docs; do not assume SSE-only servers work).

## Reference

- Tailscale Funnel KB: https://tailscale.com/kb/1223/funnel  
- Hub: `../integrations/gemini-deep-research-interactions-2026.md`
