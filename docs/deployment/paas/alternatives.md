# PaaS Alternatives — Head-to-Head (2026-10-22)

Evaluated for: Python FastMCP + React/Vite, Dockerfile-first, env-var config, preview URLs, fixed vs usage billing, who holds secrets.

## 1. At-a-glance

| Platform | Model | Billing | Free/trial | Best for fleet | Watch out |
|----------|-------|---------|------------|----------------|-----------|
| **Render** | Managed PaaS, closest Railway twin | Fixed per-service + usage | Free static + limited free web service, then from ~$7/mo | Production backends/workers, predictable bills | Cold sleeps on free; Disk/DB extra |
| **Fly.io** | Docker-native micro-VMs global | Usage (VM-s + egress) | Small free allowance | Always-on MCP servers, global edge, `fly.toml` | Egress + always-on cost; Postgres you operate |
| **Northflank** | App delivery + BYOC | Per-service + BYOC infra | Trial, then paid | Post-breach pick if you want managed but secrets in your VPC | Overkill for single demo; pricing complexity |
| **Coolify** | Self-hosted Heroku-clone (OSS) | Free software, you pay VPS | Free | **Default for control**: Goliath VM or Hetzner €5-10 box, env stays yours | You are ops (updates, backups, certs) |
| **DigitalOcean App Platform** | Managed PaaS on DO | Fixed + usage | $5/mo floor | If already on DO, simple | Same lock-in as others, fewer AI templates |
| **Encore.dev** | Backend PaaS w/ type-safe infra | Usage | Free tier | API-heavy repos | Frontend story thinner |
| **Vercel / Netlify** | Frontend + serverless | Usage/seats | Generous free frontend | Static webapps only | Backend/MCP server = wrong tool |
| **Hetzner (raw) + Caddy/Docker** | VPS | Fixed €4-12/mo | No free, cheap fixed | Cheapest warm 24/7, pairs with Coolify | Manual, but scriptable via `start.ps1` pattern |

Sources: Northflank `railway-alternatives` (2026-10-07), Render `best-railway-alternatives`, Encore, DeployHype, Ownkube, Kuberns roundups; cross-checked 2026-10-22 via search receipts.

## 2. Why people leave Railway (2026 pattern)

1. **Always-warm bill shock** — per vCPU-s/GB-s is great bursty, brutal for never-sleep.
2. **Uptime/deploy pauses** — Oct 2026 incident froze deploys 16h+.
3. **Secret trust** — env-var store is now a blast radius (see breach runbook).
4. **Predictability** — fixed-size VM (Fly, Hetzner) beats meter for companions.

## 3. Picks by job

- **One public demo for a week:** Railway trial ($5) or `ssh railway.new` box, dummy keys. Tear down after.
- **Always-on companion (fleet-agent, digest sender):** Fly.io micro-VM or Hetzner CX22 + Coolify. Fixed cost, sleeps never.
- **Private share to Steve/phone:** Don't use PaaS — Tailscale Funnel (`operations/TailscaleFunnel.md`).
- **Prod webapp + API + DB:** Render (managed) or Northflank BYOC (VPC). Coolify if you want to own it.
- **Static webapp only:** Netlify/Vercel free tier, backend stays on Goliath/Fly.

## 4. Coolify note (fleet favourite)

Runs on your metal: `Hetzner → Docker → Coolify → git push → HTTPS`. Supports nixpacks/Dockerfile, Postgres/Redis one-click, preview envs, backups to S3.

```bash
# Hetzner CX22 example (approx €6/mo, 2 vCPU/4GB)
# - Ubuntu 24.04, Docker, Coolify install script
# - A record *.yourdomain.at → IP, Coolify handles Let's Encrypt
# - env vars live on your disk, not a third-party store
```

Good fit because fleet already does NSSM + `start.ps1` + adjacent ports — Coolify is the same mental model, just on a VPS with public IP.

## 5. Migration checklist (Railway → X)

- [ ] Export service list + env names (NOT values) + volumes + domains + cron
- [ ] Re-create secrets at destination from source-of-truth (password manager), rotate any that lived on Railway pre-2026-10-21
- [ ] Dockerfile/nixpacks builds green locally (`docker build`)
- [ ] Healthcheck `/health` + `/ready`, private networking, persistent volume for SQLite/LanceDB
- [ ] Preview URL + custom domain + HTTPS, webhook re-registration
- [ ] Old Railway project → sleep, then delete volumes after retention window

## 6. What NOT to do

- Don't mirror 187 repos to any PaaS. 2-3 warm max.
- Don't store long-lived OpenAI/Anthropic keys as plain env on any PaaS post-breach — use short-lived / workload identity where supported, or proxy via Goliath.
- Don't use Vercel/Netlify for the MCP server half — split frontend (static) from backend (Fly/Render/Coolify).
