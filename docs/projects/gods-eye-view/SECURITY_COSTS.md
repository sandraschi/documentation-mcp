# God's Eye View — Security, Costs, Licenses

Source: `SECURITY.md`, `DATA_SOURCES.md`, `.env.example`, README §§ Keys/Costs/Sharing at HEAD `8b8ccc9`. Paraphrased, not pasted.

## 1. Threat model (operator = you, localhost by default)

- **Bind:** `HOST=localhost`, `PORT=4173`. Only your machine reaches the key-brokering proxies. `GEV_ALLOWED_HOSTS` for LAN hostnames; `0.0.0.0` alone does NOT trust arbitrary Host headers.
- **Client-exposed by design (restrict at provider, don't try to hide):** `GOOGLE_MAPS_API_KEY` (HTTP-referrer + API restriction: Map Tiles + Geocoding), `CESIUM_ION_TOKEN` (public `assets:read` + URL restriction), `MAPILLARY_CLIENT_TOKEN` (public client token). Visible in devtools by design.
- **Server-only (never reach browser):** `GOOGLE_MAPS_SERVER_API_KEY` (split opt-in; IP-restricted; Places + Street View Static only), `OPENAI_API_KEY`, `AISSTREAM_API_KEY`, `FIRMS_MAP_KEY`, `TOMTOM_API_KEY`, `OPENSKY_*`, `LL2_API_TOKEN`. Browser gets OpenAI short-lived session token only.
- **Proxy hardening:** SSRF protection, response caps, sanitized errors, sanitized 429s. Google cost endpoints throttled per-IP default 120/min (`GEV_RATELIMIT_GOOGLE_PER_MIN`), OpenAI cost endpoints 30/min (`GEV_RATELIMIT_OPENAI_PER_MIN`). Typo → default, not unlimited. **Throttles are NOT billing caps.**
- **HLS:** 2 sessions, ≤12 segments/24 MiB retained, 4 MiB + 10 s per fetch, no segment files/ffmpeg, refuses redirects/off-origin/encrypted/non-TS. 8 client leases/session, 15 s abandoned-lease expiry.
- **Embed:** `?embed=1` framing denied unless `GEV_EMBED_FRAME_ANCESTORS` set. Other pages never frameable.
- **Provider Settings:** loopback-only; disabled when shared. Pinokio 8.0.40 native Configure panel does NOT save this app's nested file correctly AND logs values — use in-app POWER UP instead (8.2 fixes install, not confirmed for Configure).
- **Storage:** `.env` (terminal) or `pinokio/ENVIRONMENT` (Pinokio) made owner-only BEFORE secret write, gitignored. Shell/Keychain values shown as externally-configured, read-only, never touched.
- **Report:** see SECURITY.md reporting section upstream. Scope/expectations: exploratory viz, not hardened production service.

## 2. LAN sharing (explicit opt-in, eyes open)

`npm run dev -- --host 0.0.0.0 --port 4173` (or `HOST=0.0.0.0 ./scripts/dev-fresh.sh`). Anyone who can reach it can spend your quota through the proxies. Before sharing: provider quotas + usage limits + billing/budget alerts FIRST (budget alert alone doesn't stop spend). Tighten `GEV_RATELIMIT_*`. Pinokio LAN/Cloudflare sharing stays disabled; remote access = separately reviewed auth proxy.

## 3. What it costs (mid-2026 upstream figures — verify at providers)

| Tier | Reality |
|------|---------|
| 🟢 most layers | $0, no signup: OpenSky anon, USGS, CelesTrak, adsb.lol, city CCTV, Radio Browser, GBFS, LL2, transit, OSRM, NOAA/ECMWF, OSM ALPR, bundled sets |
| 🟡 free-key | $0 with signup + quotas/eligibility: AISStream, FIRMS, TomTom (200 k tiles/mo), OpenSky OAuth, Cesium ion Community (personal/non-commercial) |
| Google 3D | Free via eligible ion within quota; metered direct (billing on). ~1,000 free tile sessions/mo currently; ~3 h rendering per root request. Solo sparse explorer can stay free — still set alerts |
| 🔴 OpenAI voice | Metered. API-key path: spend readout + $2 warn + $5 hard cap. OAuth path: tracked, no dollar cap |

## 4. License carve-outs (MIT covers CODE, not DATA)

- **Remove-if-commercial:** TeleGeography cables (NonCommercial, self-contained folder), OpenSky (non-commercial + possible written-agreement requirement for operational live use), Google tiles/geocode/places (proprietary ToS; no caching/storing/rehosting — live-only is the compliant pattern; keep Google logo credit).
- **Attribute-required:** ECMWF (CC BY 4.0 + terms + disclaimer), Mapillary (CC BY-SA 4.0), OSM/Overture/adsb.lol (ODbL), TomTom, TfL, Ontario OGL, Fintraffic CC BY 4.0, DriveBC/Calgary OGL variants, Statens vegvesen NLOD 2.0, Live Traffic NSW CC BY 4.0, Open-Meteo (CC BY 4.0 + adjacent link), GDELT (cite + link), Re:Earth terrain (CC BY 4.0) + EGM2008 (NGA public domain).
- **Courtesy:** CelesTrak (cite Kelso), AISStream, USGS/NASA/NOAA/NIFC/InciWeb (public domain, credit courtesy), transit operators, CCTV cities, Radio Browser (PDDL) + broadcaster terms, adsbdb (no published quota; route data © Taylor/Mason — get permission; fan-out capped 4-in-flight ~5/s, 24 h disk cache, fail-silent).
- **Media:** README GIFs show Google 3D + live data promotionally with in-frame attribution; not licensed for standalone reuse (`docs/media/README.md`).
