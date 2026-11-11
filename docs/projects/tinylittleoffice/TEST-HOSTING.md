# Test-hosting TinyLittleOffice (3 tiers, pick one)

Upstream docs: `docs/self-host.md` in the read-only mirror
`D:\Dev\repos\_upstream\tinylittleoffice`. Rule: **never develop in `_upstream/`**
— fork or copy to a writable path first. Running servers is fine; editing the
mirror is not (refresh hard-resets it).

## Tier 0 — No install (try the games in 30 seconds)

1. Open https://tinylittleoffice.com/deck/ or `/write/`.
2. Drag `games/night-bakery.tlo` / `games/starfreight.tlo` (or any `ideas/*.tlo`)
   onto the page. It opens.
3. Edit → the address bar is your save. Copy it = your copy.

Agent path, same zero-install: `npx tinylittleoffice try deck draft.tlo`
(lint + measure + JSON, no browser), `npx tinylittleoffice link deck draft.tlo`.

## Tier 1 — Local dev (edit + instant reload, port 4178)

```powershell
# one-time: fork to a WRITABLE path (not _upstream)
git clone https://github.com/aboard-io/tinylittleoffice.git D:\Dev\scratch\tinylittleoffice-test
Set-Location D:\Dev\scratch\tinylittleoffice-test
npm ci
npm run dev      # http://localhost:4178, hot reload
npm test         # unit + browser (needs Playwright browsers once)
npm run build    # shippable static site in dist/
```

What you get: every app, Share, QR, Display Link, offline service worker.
What you don't: short links + cards (they need tinier, below) — Share still copies
long/present links, which is all games need.

Point links at your copy: `npx tinylittleoffice link deck draft.tlo --site http://localhost:4178/`.

## Tier 2 — Full self-host (site + short links, 2 ports, 1 SQLite file)

Same code the two Cloudflare Workers run, over `node:http` + `node:sqlite`:

```powershell
Set-Location D:\Dev\scratch\tinylittleoffice-test
VITE_SITE_URL=http://localhost:8000/ VITE_TINIER=http://localhost:8001/ npm run build
"BRAKE_KEY=$(openssl rand -base64 32)" | Out-File .env -Append -Encoding utf8
npm run selfhost   # site :8000, tinier :8001, data/tinier.sqlite
# Docker instead: npm run selfhost:build; npm run selfhost:up
```

`.env` keys (`.env.example` lists all): `BRAKE_KEY` (required),
`SITE`/`TINIER` (public addresses, baked into the build — rebuild after changing),
`PORT`/`TINIER_PORT` (8000/8001), `DB` (SQLite file), `IP_HEADER` (behind a proxy).
Browsers keep short links/passwords/offline only on `https://` or `http://localhost`
— off-machine testing needs TLS (tunnel or terminating proxy).

Cloudflare path (30 min, mostly DNS): same repo, `npx wrangler login`, set the 6
names in `wrangler.jsonc`/`tinier/wrangler.jsonc`/`.env.production`/D1/`BRAKE_KEY`,
`npm run deploy` (checks, migrations, both Workers, npm publish, verify). Tag path:
push `v*` → GitHub Actions Deploy → provenance + `verify-deploy` file-by-file.

## Testing OUR files against a tier

```powershell
# from the scratch clone (has node_modules), point at our mcd files:
node packages/doc/tinyoffice.ts try deck D:\Dev\repos\mcp-central-docs\projects\tinylittleoffice\games\night-bakery.tlo
node packages/doc/tinyoffice.ts try write D:\Dev\repos\mcp-central-docs\projects\tinylittleoffice\games\starfreight.tlo
node packages/doc/tinyoffice.ts link deck D:\Dev\repos\mcp-central-docs\projects\tinylittleoffice\games\night-bakery.tlo --site http://localhost:8000/
```

Clean = empty lint + sensible measure + link under the 2048 meter. If lint names a
slide/block, fix the `.tlo` (ours, writable) — never the mirror.

## Which tier for what

| Goal | Tier |
|------|------|
| Play/review a `.tlo` | 0 |
| Remix a game, try an 11th-app template | 1 |
| Share short links, test expiry/rate-limit/cards | 2 (selfhost or Cloudflare) |
| Prove prod parity | `npm run verify-deploy -- <url>` + `gh attestation verify` |

Mail/chat preview caveat (all tiers): long links use `~` + `+`-every-300 so
iMessage/Signal linkify them whole; some clients still wrap — sealed docs report
"wrong password or link was cut" for exactly this reason.
