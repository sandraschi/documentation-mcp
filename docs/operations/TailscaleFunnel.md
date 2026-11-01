# Tailscale Funnel - Fleet Public Hub (canonical)

**Status**: active · **Owner**: mcp-central-docs (canonical)
**Copies**: `tailscale-mcp/docs/FLEET_FUNNEL.md` mirrors this file.
**Rule**: repos that support funneling LINK here - do not duplicate funnel
docs in per-repo READMEs or AGENTS files beyond a one-line pointer.

---

## 1. What this is

Tailscale Funnel exposes local services on `goliath` to the public internet
on `https://goliath.<tailnet>.ts.net` - no port forwarding, no domain, TLS
auto-provisioned. The fleet uses it as a **low-usage public site for a few
buddies**: docs, reports, and experiments. Everything is a subpage under one
hostname; the root is a landing page.

## 2. Route map (live config)

Source of truth: `tailscale serve status` on goliath.

| Mount | Local target | Service | Auth |
| --- | --- | --- | --- |
| `/` | 127.0.0.1:11157 | Funnel landing page (`mcp-central-docs/funnel-landing/`) | none (public directory) |
| `/multigpu/` | 127.0.0.1:11136 | Multi-GPU Cluster Recipes playbook (Docusaurus) | none (public docs) |
| `/games/` | 127.0.0.1:11158 (strip proxy) -> 10987 | AI games dashboard (ai-games-collection; SPA + API on one port) | none (demo UI; engines are local, bursty) |
| `/intel/` | 127.0.0.1:11027 | Intel Reports Hub | Basic auth except `/intel/public` + `/intel/health` |
| `:11027` (port) | 127.0.0.1:11027 | Intel Reports Hub | tailnet-only (iPads, fleet probes) |
| `:10443` (port) | 127.0.0.1:10900 | (legacy tailnet-only route) | tailnet-only |

## 5b. Path-strip proxy pattern (for non-prefix-aware apps)

**CORRECTION 2026-10-25 (measured, supersedes the original wording below):**
`tailscale serve` DOES strip the mount prefix before forwarding. Proof: on the
`/games/` mount (funnel -> :11158 proxy -> :10987 backend), the path
`/games/games/games/board-games/chess.html` returned **200 through the funnel**
while the same path requested **direct on the proxy** returned 404 — i.e.
exactly one strip happened at tailscaled, one at the proxy, landing on the real
backend path. Consequence: a proxy mounted behind `serve --set-path` must run
with **no strip of its own** (`--prefix ""`), or every request is double-stripped
and 404s. `start-funnel-path-proxy.ps1 -NoStrip` is the correct mode here.

The other half of the problem is the browser side: an app that was written for
root mounting mixes relative and root-absolute links, and under a subpath mount
both break in different ways:
- relative `games/x.html` from page `/games/` resolves to `/games/games/x.html`
  — which, with the single strip, lands on the real path -> works untouched.
- root-absolute `/js/x.js` resolves OUTSIDE the mount -> hits the funnel root ->
  wrong app. These must be prefixed.
- root-level relative assets (`styles.css`, `icon-192.png`, `manifest.webmanifest`)
  on a nested page resolve relative to the page and miss -> must be prefixed.
- sibling relative assets (`css/chess.css`, `../board-games/x.html`) must NOT be
  prefixed or they break.

`funnel-path-proxy.py --rewrite-prefix /games` handles that with two rule sets
split by content type (`html` attributes vs `code` string/call literals) —
applying both to the same HTML double-prefixes (`/games/games/js/x`), which is
exactly the bug that cost an hour on 2026-10-25.

Known remaining gap on `/games/`: the game pages talk to AI engines on
`:11211`/`:11212`/`:11213` directly (`js/api-config.js` builds
`protocol//host:port`), and the funnel exposes nothing on those ports, so pages
LOAD but AI moves fail from the iPad. Fix requires an engine proxy route in the
gateway (`/api/engine/<name>/*` -> localhost:112NN) plus api-config using it
when `!isLocal`. Not yet done.

**Original (now corrected) wording:**

Tailscale serve does NOT strip the mount path - `/games/foo` arrives at the
target as `/games/foo`. Apps that are not prefix-aware need one of:

1. **uvicorn `root_path`** (Python ASGI) - strips the prefix before routing.
   Used by the Intel Reports Hub (`INTEL_REPORTS_HUB_ROOT_PATH=/intel`).
2. **Rebuild with `BASE_URL`** - for static site generators (Docusaurus
   playbook uses this: `BASE_URL=/` funnel build).
3. **Path-strip reverse proxy** - for everything else:
   `scripts/funnel-path-proxy.py` (stdlib only) + `scripts/start-funnel-path-proxy.ps1`.
   `--prefix /games --target http://127.0.0.1:10987`, served on 11158.
   The proxied app must use **same-origin relative** API URLs (see the
   ai-games-collection frontend: relative base outside Tauri) so `/api/*`
   resolves through the mount; the target's own proxy/dev server handles it.

Rule: absolute `http://127.0.0.1:PORT` URLs in frontend code only work when
the browser runs ON the host - never on the funnel. Any app being exposed
needs relative API bases.

## 6. Friend Joe exposure plan

The funnel address goes to a few people, and transitive creep means assume
girlfriend/boyfriend-grade traffic: curious, non-technical, unpredictable.
Everything below stays **cheap for goliath** (static or seconds-scale bursts).

| Candidate | Status | Usage profile | Notes |
| --- | --- | --- | --- |
| Landing page + static subpages (vibecoding, tooling-cost, architecting, fleet, sage) | live | near-zero (static HTML) | The joke card stays honestly tagged |
| `/multigpu/` playbook | live | static site | Docusaurus build, no backend |
| `/games/` AI games dashboard | live | UI is light; ENGINE MOVES are the only bursts (seconds each) | Engines run local (native or docker); one game = a few seconds of CPU per move. If this ever becomes a problem, cap engine CPUs (docker `--cpus`) or point the dashboard at an idle mode |
| `/intel/public` | live | static-ish digest page | open subtree for iPad chatbot webviews |
| Future: papers/arXiv digest, screenshots gallery, aiwatcher HTML digest | planned | static, regenerated hourly | Same pattern as the intel hub |

**Never expose:** email, secrets, DB/windows ops, LLM chat endpoints (GPU
burn + open endpoint), monitoring dashboards with host internals. Those stay
tailnet-only or behind the Basic auth challenge.

**Creep guardrails:** no unauthenticated personal data anywhere on the
funnel; the only burst source is the games engines (seconds-scale); static
content scales to dozens of curious friends without measurable load.

## 3. Auth model (important)

- **Main funnel addresses challenge with HTTP Basic auth (401 + WWW-Authenticate).**
  No redirects to a login page - a 302 would break the browser's auth dialog
  and lock out outside users who DO have credentials.
- **The `/public` subtree is open** (the intel hub's `/public` + `/health`).
  Anything meant for unauthenticated visitors (iPads, chatbot webviews,
  buddies without credentials) lives under a `/public` path.
- iPad chatbots / webview agents **cannot answer Basic auth prompts** - if a
  page is for them, it must be unauthenticated. That is why intel reports
  have a public page and everything else stays behind the challenge.

## 4. ACL

Funnel is an explicit node attribute. Current policy grants it to goliath:

```json
"nodeAttrs": [
  { "target": ["100.118.171.110"], "attr": ["funnel"] }
]
```

(goliath = 100.118.171.110; check with `tailscale status`.) No ACL change is
needed to add funnel paths on goliath - the attribute covers the node. Adding
funnel on a DIFFERENT node requires an ACL edit (admin console) + this doc.

## 5. Adding a public subpage (checklist)

1. **Register the port** in `operations/WEBAPP_PORTS.md` + `webapp-registry.json`.
2. **Run the service** on goliath with a start script (fleet standard;
   zombie-clear + readiness poll). Long-running services should survive via
   scheduled task or start script re-run.
3. **Serve route**: `tailscale serve --bg --set-path /x/ http://127.0.0.1:PORT`
   (no `--set-path` for `/`).
4. **Publish**: `tailscale funnel --bg --set-path /x/ http://127.0.0.1:PORT`.
   There is no `tailscale funnel on` - funnel is per-target. Re-run the
   funnel commands after ANY serve change (serve edits drop the funnel flag).
5. **Path-prefix-aware apps**: if the app does not natively serve under the
   mount path, use uvicorn `root_path` (uvicorn strips the prefix before
   routing; paths not starting with it pass through unchanged - tailnet
   direct access on the port keeps working). Absolute redirects break under
   a prefix; use relative `Location` headers or 401 challenges.
6. **Link it from the landing page** (`funnel-landing/index.html`).
7. **Verify publicly**: `Invoke-WebRequest https://goliath.<tailnet>.ts.net/x/`
   from a non-tailnet context (or `tailscale funnel status`).

Idempotent helper: `mcp-central-docs/scripts/setup-funnel-routes.ps1`.
Landing server: `mcp-central-docs/scripts/start-funnel-landing.ps1`.

## 6. What is allowed on the funnel

| Content | Rule |
| --- | --- |
| Docs, playbooks, reports | Yes, unauthenticated or with app-level auth |
| Demos (games dashboards, experiments) | Yes, ideally with auth or on /public |
| Personal data (email, secrets, DB ops, windows ops) | **No** - tailnet-only. App-level auth is not enough for secrets-class services |
| Anything long-running | Yes - funnel proxies to whatever listens locally; the service must be RUNNING (funnel does not start it). 502 = service down |

## 7. Doc-link rule

- `mcp-central-docs/operations/TailscaleFunnel.md` - canonical (this file).
- `tailscale-mcp/docs/FLEET_FUNNEL.md` - mirror copy.
- Other repos (multi-gpu-cluster-recipes, fleet-agent-mcp, ...): one-line
  pointer to the canonical file in AGENTS.md / relevant doc. No duplication.
- Fleet-wide funnel news: `mcp-central-docs/CHANGELOG.md`.
