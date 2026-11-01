# Fleet Fit — What Goes Where (Sandra/Steve, Goliath-first)

**Rule:** Goliath is home. PaaS is a window, not a house. Max 2-3 warm public services.

## 1. Decision matrix

| Need | Where | Why |
|------|-------|-----|
| Dev, MCPB, Tauri, Claude Desktop stdio | Goliath local | Zero bill, RTX 4090, instant |
| Private share to Steve/phone | Tailscale Funnel | No public internet, no secret sprawl. See `operations/TailscaleFunnel.md` |
| Public demo (week-long) | Railway trial / `ssh railway.new`, dummy keys | Cheapest ephemeral, tear down after |
| Always-on webhook ingress | Fly.io or Hetzner+Coolify | Fixed cost, sleeps never, Docker-native |
| Prod API+DB+frontend | Render or Northflank BYOC, or Coolify self-host | Predictable or owned |
| Static webapp | Netlify/Vercel free | Don't pay PaaS for static |
| GPU inference / embeddings | Goliath only | Cloud GPU $ kills you |
| Secrets of record | Password manager + Goliath, scoped relay tokens outward | Post-Oct-2026 non-negotiable |

## 2. Cost discipline

- Trial math: $5 / 30d ≈ $0.0069/h burn. One 1GB always-warm service + egress eats it in days. Plan teardown date at deploy time.
- Free $1/mo = one nano sleeper, nothing more.
- Hobby $5 / Pro $20 are floors, not caps. Set provider spend alerts on OpenAI/Anthropic/Hetzner AND Railway/Render/Fly.
- Prefer fixed (Hetzner CX22 ~€6, Fly shared) for 24/7; prefer usage (Railway) for bursty previews.

## 3. Recommended starter stack (if you want a public window this month)

1. **Hetzner CX22 + Coolify** (1 box): `api.yourdomain.at` + `app.yourdomain.at` + Postgres. All env on your disk. Back up to Hetzner Storage Box.
2. **Tailscale** for everything else.
3. **Railway trial** only for throwaway PR previews with dummy keys until breach post-mortem clears.

Domain: if you recover your old `.at` (see §4), point `*.yourdomain.at` at Hetzner/Coolify, Let's Encrypt via Coolify. No registrar move needed to start — just DNS A.

## 4. Your old Austrian domain + Hostinger / dark-app-factory lead (2026-10-22)

Fleet-wide grep for `hostinger` = 0 hits across 10k files. No Hostinger reference in `dark-app-factory/` code, docs, or `mcp-central-docs/projects/dark-app-factory/`.

What the repos DO say:
- `dark-app-factory/docs/FULL_AUTO_DEPLOYMENT.md` (2026-02-11): full-auto domain was planned as INWX API for .at + Hetzner for host, Phases 2-3. Never implemented. Phase 1 only outputs `deploy.sh` + `docker-compose.prod.yml` + `nginx.conf`. So the factory itself never registered anything.
- `dark-app-factory/docs/MONETIZATION_PLAN.md`: Product A EUR100 = you host on your Hetzner or deliver zip. Product B EUR300 = their problem. Line: Domain nic.at, INWX for .at. Or use your existing domain.
- `sandras-com/SPEC.md` 11.1 (2026-10-05): `sandras.com` was UNREGISTERED as of 2026-10-05 (no NS, Verisign RDAP 404). Status: Sandra buys it. So if you reserved something long ago, it is not this one unless bought after Oct 5.

Hostinger reality check: Hostinger is Lithuanian (Hostinger International, Kaunas) with German storefront `hostinger.de` — heavily used in DE/AT as cheap hoster, not an Austrian registrar. If Steve holds it, it lives in HIS hPanel under Domains → Portfolio, not in your mailbox. Your INBOX Graph search for `hostinger` returned only StackCommerce promo spam, no invoice — consistent with Steve-owned.

To close it (5 min with Steve):
1. Steve logs into `hpanel.hostinger.com` → Domains → check list + expiry + auto-renew. Note exact domain + registrar shown (often Tucows/Enom resold via Hostinger).
2. If domain found for a dark-factory demo: decide keep (point A-record to Hetzner/Coolify) or let expire + note date in `operations/session-log/`.
3. If nothing in hPanel: run `nic.at` Whois for any candidate you remember + check Steve's Hostinger billing emails for `domain registration / Verlängerung`.
4. Tell me the exact domain string and I file it in `fleet-registry.json` + this doc so we stop re-hunting.

Original recovery paths still stand: nic.at Whois if you remember the name, bank statements for easyname/world4you/domaintechnik/inwx yearly ~EUR15-30, Sent/Archive for nic.at Rechnung.

You said long ago you reserved a URL/small site on an Austrian registrar. Email search in INBOX for `easyname/world4you/domain` returned 0 registrar hits (only newsletters matched `domain` generically) — so it's either old, archived, or under a different mailbox.

Most likely Austrian hosts (Vienna/Linz reality):
- **Easyname** (Vienna, easyname.at) — #1 guess for "small site + .at long ago"
- **World4You** (Linz, world4you.com)
- **Domaintechnik** (Vienna, domaintechnik.at)
- **Internex / Innofield / checkdomain / INWX** (AT-compatible, INWX is German but common for .at)
- Also possible: **A1, Drei, UPC/Magenta** bundle, or **Hetzner/Netcup** (German, but many AT users).

Fastest jog, in order:
1. **nic.at lookup** — if you remember ANY candidate name: `https://www.nic.at/` → Whois → shows current registrar + holder (often you). Try variants you would have picked.
2. **Bank/credit-card history** — search for `easyname`, `world4you`, `domaintechnik`, `internex`, `inwx`, `nic.at` in statements (yearly ~€15-30 .at fee leaves a trail).
3. **Old mailbox / Sent** — search Sent + Archive for `nic.at`, `Rechnung Domain`, `Verlängerung`, `.at` renewal. Your INBOX Graph search above missed it, so check Sent/Archive explicitly.
4. **Password manager / browser** — search logins for those 5 host names.
5. Tell me any fragment (approx year, was it `name.at`? `wordpress` one-click? email included?) and I narrow to 1 registrar + recovery link.

If we recover it: keep registrar as-is, just set DNS A → Hetzner/Coolify or CNAME → Render/Fly. No need to transfer to Railway (they also sell domains but you don't need that now).
