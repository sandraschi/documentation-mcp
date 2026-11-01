# Railway — Deep Dive (fleet-evaluated 2026-10-22)

> Railway is an infra platform that collapses build → deploy → network → observe into one UX.
> Tagline-proof: Heroku-like DX, usage-based billing, agent-native (CLI + remote MCP).

Sources: `railway.com/llms.txt`, `railway.com/agents.md`, `docs.railway.com/pricing/free-trial`, pricing page, `railway.com/.well-known/*`.

## 1. What it is / isn't

- **Is:** managed PaaS for full-stack apps, DBs (Postgres/Redis), buckets/volumes, functions, cron, preview envs per PR.
- **Is not:** GPU cloud for local LLM (no RTX 4090 economics), not a Tauri/MCPB replacement, not a secret manager (see breach).
- **Interface:** Dashboard + CLI (`railway up -y`) + GraphQL `https://backboard.railway.com/graphql/v2` + remote MCP `mcp.railway.com` + OAuth/Login-with-Railway.

Agent setup (from `agents.md`):
```bash
bash <(curl -fsSL cli.new) --agents -y   # preferred CLI agent path
ssh railway.new                          # free Linux VM, no account (see §3)
```

## 2. How a fleet repo maps

Typical fleet repo = FastMCP Python backend (port N) + Vite React frontend (port N+1), Dockerfile or nixpacks.

```
repo/
  railway.json  # or railway.toml — services, build, start, healthcheck
  backend/Dockerfile
  webapp/Dockerfile
```

Adjacent-port convention collapses to 2 Railway services with private networking + one public domain. Env vars per service, shared volume if needed.

Minimal `railway.json` pattern:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": { "builder": "NIXPACKS" },
  "deploy": { "startCommand": "uv run python server.py", "healthcheckPath": "/health" }
}
```

Webapp static: build with `bun run build`, serve `dist/` via Caddy/nginx or Railway static.

## 3. Pricing / trial (checked 2026-10-22)

> Always re-check `railway.com/pricing` — numbers move.

| Tier | Price | What you get |
|------|-------|--------------|
| **Trial** | $0, one-time **$5 credit, 30 days** | Hobby features, capped: 1 GB RAM, shared vCPU, 5 services/project. Full vs Limited network depends on GitHub verification (age/activity). Limited = restricted egress + few ports. |
| **Free (post-trial)** | **$1/mo recurring credit, no rollover** | Keeps tiny service warm. Volumes from trial deleted 30 days after credits expire unless you upgrade. |
| **Hobby** | **$5/mo minimum → credit** | Light workloads pay just the floor. Metered after. |
| **Pro** | **$20/mo minimum → credit** | Team/prod. Same metering. |
| **Enterprise** | Custom | SSO, audit, committed spend. |
| **ssh railway.new** | Free, no account | 2 vCPU / 2 GB VM, 60 min build, claim link 24h, 3 boxes/IP/day. Unclaimed boxes deleted. Keyed by SSH key. Region-capped when busy. |

Metering (usage-based, per-second): Memory ~$0.00000386/GB-s + CPU vCPU-s + disk + egress. Bursty = cheap. Always-warm = expensive. That is the #1 reason people leave.

Carry-over rule: trial remainder carries to first paid plan but may skip first invoice (fraud check) and apply as discount after first successful payment.

## 4. Limits that bite fleet repos

- 1 GB RAM on trial → Ollama / embeddings OOM. Keep trial to API + static frontend, no local LLM.
- Shared vCPU → cold starts, noisy tail latency. Healthcheck accordingly.
- 5 services/project on trial → one backend + one webapp + one DB = already 3.
- Limited-trial egress → outbound webhooks / MCP sampling / OAuth callbacks can fail silently. Verify at `railway.com/verify` or upgrade to Hobby.
- 10 MB export-style limits do not apply here, but build logs + ephemeral disk do — persist in volumes/buckets, not container FS.

## 5. When to use / when not

**Use for:** public demo URL, webhook ingress (GitHub/Discord/Stripe), always-on companion (fleet-agent inbox, aiwatcher digest sender), PR previews.

**Do not use for:** local-LLM inference, LanceDB bulk ingest, 24/7 x 187 repos, secret storage as system-of-record (post-Oct-2026).

## 6. Fleet ops notes

- Claim ports first (`operations/WEBAPP_PORTS.md` + `fleet-gate/claim_ports.py`) even for cloud — avoids collision when you pull back local.
- `railway up -y` deploys linked service; `railway run` for one-off commands; `railway logs` tails.
- Keep `railway.json` in repo, secrets in Railway dashboard only (never in git), mirror required keys in `.env.example`.
- Post-breach (§ breach-runbook): pin to dummy keys on any new trial until incident cleared.

## 7. Links

- Docs: `https://docs.railway.com/llms.txt`
- Agents: `https://railway.com/agents.md`
- Pricing: `https://railway.com/pricing.md`, trial: `https://docs.railway.com/pricing/free-trial`
- Catalogs: `/.well-known/ai-catalog.json`, `/api-catalog`, `/mcp/server-card.json`, deploy manifests `/deploy/llms.txt`
