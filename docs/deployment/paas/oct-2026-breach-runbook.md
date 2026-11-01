# Railway Oct 21 2026 Incident — Env-Variable Exposure Runbook

**Incident date:** 2026-10-21 (disclosed Oct 21, dark ~16h+)
**Fleet status 2026-10-22:** DO NOT place real secrets on Railway. Dummy keys only for trials.
**Applies to:** anyone who ever stored secrets as Railway env vars (API keys, DB passwords, registry creds).

## 1. What happened (verified 2026-10-22)

- Railway detected anomalous activity in systems storing customer configuration / environment variables.
- Unauthorized third party **may have accessed encrypted variables and, for a subset, obtained decrypted contents.**
- Deployments paused during response. Multiple trackers (GitGuardian, Safeguard, CyberSec press, class-action watch) list: API keys, DB passwords, registry credentials, AI inference provider keys (Anthropic/OpenAI specifically named in secondary reporting).
- Railway notice advised: revoke/rotate credentials stored as env vars, check provider usage logs.
- What Railway has NOT fully detailed (as of receipts): exact subset size, sealed-variable scope, per-project blast list. Treat as unknown → assume exposure.

Do not copy secret VALUES into tickets, chats, or docs during response. Inventory NAMES only.

## 2. Who is affected

- Any Railway account with non-dummy env vars before 2026-10-21, even if project later deleted (retention unknown).
- Highest blast radius: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`, `DOCKER_*`, `AWS_*`, `DATABASE_URL`, `REDIS_URL`, `REGISTRY_PASSWORD`, webhook signing secrets.
- Fleet-specific: if you trialled Railway with a real key for convenience — you are in scope.

## 3. Rotation runbook (do in this order)

### Step 0 — Stop the bleed
- Pause auto-deploys that inject old secrets. Do not trigger rebuilds that re-use compromised env.

### Step 1 — Inventory (names only)
```bash
# per Railway project: list variable NAMES, never echo values
railway variables --service <svc>  # names
# write down: which providers, which environments (prod/preview), who else holds copies
```

### Step 2 — Rank by blast radius
1. Money-movable: cloud (AWS/GCP), registry push, DB write, OpenAI/Anthropic with spend limits
2. Identity: GitHub, OAuth client secrets, webhook signers
3. Low: public feature flags, non-secret config

### Step 3 — Rotate at SOURCE, then update Railway, then redeploy
- Source first (OpenAI dashboard → new key, Neon/Supabase → reset password, GH → revoke token), verify new credential works locally.
- Update Railway env to new value, redeploy once builds return.
- Revoke old credential AFTER new path is live (avoid self-DoS). Confirm revocation in provider audit log.

### Step 4 — Look for misuse
- OpenAI/Anthropic usage graphs + activity since 2026-10-20, unknown keys/IPs/risky model spikes.
- DB: new users, new connections, pg_stat / audit log, backups exfiltrated?
- GitHub: new deploy keys, actions runs, package pushes.
- Registry: new pulls from unknown IPs.
- Stripe/AWS: spend alerts.

### Step 5 — Write it down
One line per secret: `provider / key-name / rotated YYYY-MM-DD / old revoked Y/N / misuse seen Y/N`. Keep in private ops log, not in git.

## 4. Fleet hardening after

- No long-lived keys as plain PaaS env. Prefer: short-lived tokens, workload identity/OIDC where supported, or proxy via Goliath (PaaS holds a scoped relay token, real key stays home).
- `.env.example` with NAMES only; real `.env` never committed (already fleet rule, re-affirm).
- Separate preview vs prod keys with spend caps (OpenAI limits, Anthropic spend alerts).
- Backup rotation log to `operations/session-log/` (no values).
- Re-evaluate: Coolify/Hetzner or Northflank BYOC keeps env on disk you control.

## 5. Sources (receipts 2026-10-22)

- Safeguard: `safeguard.sh/resources/blog/railway-environment-variables-breach-october-2026`
- GitGuardian: `blog.gitguardian.com/railway-october-2026-incident-environment-variables`
- OpenClassActions, TheCyberSecGuru, Hall Attorneys investigation pages (all dated Oct 21 2026).
- Search coverage: openserp-local + duckduckgo ok(10 each), fleet-local clean, Tavily/Exa unconfigured.

Update this file when Railway publishes post-mortem (root cause, scope, sealed-var verdict, build-resume proof).
