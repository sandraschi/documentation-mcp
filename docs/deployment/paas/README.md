# PaaS / Cloud Deploy Targets for the Fleet

**Last Updated:** 2026-10-22
**Status:** active
**Scope:** Railway + direct alternatives, evaluated for fleet use (FastMCP Python servers + React/Vite webapps, Tauri local-first, Goliath RTX 4090 local).

This section answers: where do we push a fleet repo when `localhost` is not enough (public demo, webhook ingress, always-on companion)?

## In this section

| File | What |
|------|------|
| [railway.md](railway.md) | Railway deep-dive: model, pricing/trial, agent workflow, limits |
| [alternatives.md](alternatives.md) | Render, Fly.io, Northflank, Coolify, DigitalOcean App Platform, Encore, Netlify/Vercel — head-to-head |
| [oct-2026-breach-runbook.md](oct-2026-breach-runbook.md) | Oct 21 2026 Railway env-var incident: what happened, who is affected, rotation runbook |
| [fleet-fit.md](fleet-fit.md) | Decision matrix for Sandra/Steve: what to host where, what stays on Goliath, cost rules |
| [coolify-goliath.md](coolify-goliath.md) | Coolify on Goliath Hyper-V VM: spec, direct-IP vs Tailscale vs Tunnel, fleet Dockerfile, test plan |

Parent: [../README.md](../README.md) (general deployment) + [../../operations/TailscaleFunnel.md](../../operations/TailscaleFunnel.md) (private ingress alternative).

## TL;DR for the fleet

- **Goliath stays primary.** Local NSSM, 10700-15000 ports, Ollama, LanceDB. No per-second billing beats free local watts for 187 repos.
- **Public share-a-link = PaaS.** 2-3 repos max warm at any time. Everything else sleeps or stays local.
- **2026-10-21 posture: DO NOT put real secrets on Railway** until post-mortem + rotation proof. Trial with dummy keys only.
- **Default pick post-breach:** Coolify self-hosted (Hetzner or Goliath VM) for control, Fly.io for Docker-native always-on, Render for closest Railway-like DX. Northflank if you want BYOC in your own VPC.

## Mental model

```
localhost (stdio, Tauri, MCPB) ── dev / joy
  └─> Tailscale Funnel ── private share to Steve / phone, no public internet
  └─> PaaS (this section) ── public URL, webhook ingress, demo for others
  └─> Hetzner + Coolify ── your own PaaS, fixed price, env vars stay yours
```

Related: `mcp-central-docs/operations/WEBAPP_PORTS.md` (port registry — claim before you expose), `deployment/security.md`, `deployment/monitoring.md`.
