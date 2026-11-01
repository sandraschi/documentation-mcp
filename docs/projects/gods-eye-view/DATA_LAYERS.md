# God's Eye View — Data Layers (all 20 + static sets)

Source: upstream `README.md` layer table + `docs/CURRENT-STATE.md` § Active Data Layers + `DATA_SOURCES.md` + `.env.example` at HEAD `8b8ccc9`.

Key: 🟢 no key · 🟡 free key · 🔴 metered. Intervals are upstream-stated poll/proxy-TTL figures.

## Movement

| Layer | Source | Proxy | Interval | Auth | Notes |
|-------|--------|-------|----------|------|-------|
| Live Flights | OpenSky Network; bounded adsb.lol regional fallback | `/api/flights` (OAuth + fallback) | 30 s | 🟢 anon works, 🟡 OAuth for credits | `OPENSKY_AUTH_MODE=oauth\|basic\|auto\|anon`. Non-commercial license; commercial deploy needs OpenSky agreement. adsb.lol fallback is 250 nm snapshot around camera subpoint, provenance shown |
| Military Flights | adsb.lol `/v2/mil` | `/api/military` | 15 s | 🟢 | Amber symbology; silent ~24 h trace backfill on select → stacked 3D loops |
| Live Vessels | AISStream websocket | `/api/vessels` | 60 s + 800 ms visibility pass | 🟡 free signup | `VITE_AIS_LIVE_MAX_ROWS=12000`, labels clustered to 900. Watchdog: stale at 120 s silence, recycle at 2.5x. Terrestrial AIS quiet mid-ocean; sat-AIS is $$$. Beta, no formal ToS |
| Satellites | CelesTrak TLE + SGP4 | `/api/celestrak` | 120 s | 🟢 | 838-object catalog, class colors + live legend, DENSE chip = full Starlink shell. TLEs disk-cached |
| Space Missions | Launch Library 2 + CelesTrak | `/api/launches` + `/api/celestrak/active` | 5 min | 🟢 (🟡 token raises allowance) | Rolling 30 d, 15 unauth calls/h. Ascent replay labeled RECONSTRUCTED ESTIMATE, scrub 0.25–4x |
| Transit | Operator GTFS-RT VehiclePositions (Boston, Austin, Minneapolis, Helsinki, NL, Norway, SEQ) | `/api/transit` | 15 s poll + delayed playback | 🟢 | Selected-vehicle trails, mode-colored DETECT labels. Courtesy attributions per operator |
| Bikeshare | GBFS (Lyft + BCycle) | `/api/gbfs` | 60 s | 🟢 | Per-feed attribution-only licenses |
| Traffic | TomTom flow + OSM roads / Hybrid | `/api/tomtom` flow; roads browser-direct OpenFreeMap tiles | viewport-driven, capped tile cache | 🟢 sim, 🟡 live flow | Without key: white-dot sim at hardcoded per-class speeds. With key: live speeds + congestion colors below ~8 km. Default 6,000 tiles/day cap |
| Directions | OSRM on FOSSGIS (`routing.openstreetmap.de`) | `/api/route?steps=1` | on placement/mode change | 🟢 | 1 req/s max, valid UA, no scraping/heavy use, commercial use restricted. Fix-the-map link required |

## Eyes

| Layer | Source | Proxy | Interval | Auth | Notes |
|-------|--------|-------|----------|------|-------|
| CCTV Mesh | Austin, TxDOT, Caltrans, TfL, Ontario 511, Fintraffic, DriveBC, Tallinn, Tarktee, Live Traffic NSW, Calgary, Statens vegvesen, Delaware DelDOT (+ more) | `/api/cctv` | 10 s active | 🟢 | ~3,900 cameras projected INTO 3D + VIEWSHED coverage volumes. Poses are estimated priors, gizmo-calibratable. Per-pack `CCTV_*_ENABLED/MAX_SOURCES`, catalog ceiling 4,000 round-robin. HLS via lazy hls.js (2 sessions, 12 seg/24 MiB, 4 MiB/10 s per fetch, no ffmpeg). RTMP-only unsupported |
| Street Level | Mapillary (first provider; Panoramax/KartaView/GSV planned) | `/api/mapillary/*` | camera-driven, 320 ms debounce, ≤9 tiles, 24 h cache | 🟡 client token | Coverage z0–5 points / z11–14 sequence lines; cones open MapillaryJS viewer (EXPAND/FIT/FILL/FOLLOW). Provider contract in `src/layers/streetLevel/registry.js`. CC BY-SA 4.0 credit on-globe |
| Mapped ALPR | OSM (incl. DeFlock mapping) | hourly extract, viewport-bounded | — | 🟢 | Locations + tags only. No plates, no video. SHOW NEAREST |

## Events + weather

| Layer | Source | Proxy | Interval | Auth | Notes |
|-------|--------|-------|----------|------|-------|
| Earthquakes | USGS | direct | 60 s | 🟢 | Last 24 h, public domain |
| Active Fires | NASA FIRMS (VIIRS x3 NRT + MODIS NRT, trailing 24 h) | `/api/firms` (`FIRMS_MAP_KEY`) | 10 min (proxy TTL 30 min) | 🟡 free | Click → dive + intensity + NEAREST camera |
| Fire Perimeters | NIFC WFIGS + InciWeb links | `/api/fire-perimeters` + `/api/fire-perimeters/inciweb/*` | 5 min (catalog 1 h, pubs 30 min) | 🟢 | Containment in legend; stale-on-error; per-client limits |
| Wind | NOAA GFS / ECMWF IFS 10 m (GRIB2 byte-range, eccodes-wasm) | `/api/wind` | 1 h forecast cycle | 🟢 | Animated particles + optional speed/temp/pressure field. GFS public domain; ECMWF CC BY 4.0 + terms |
| Observed Weather | NOAA nowCOAST: MRMS radar (CONUS ~4 min), GOES IR (~5 min / hourly global), lightning density (15 min accum, Americas+Pacific) | WMS via app | 2–10 min meta refresh, 24 h image cache | 🟢 | One WEATHER timeline (step back/Play/Latest). On Google 3D: translucent shells above city |
| Cyclones | NOAA NHC/CPHC `CurrentStorms.json` + tropical MapServer | `/api/cyclones` | 5 min cache | 🟢 | Positions + forecast tracks + cones (Atlantic + E/C Pacific) |
| Recent Imagery | NASA GIBS WMTS + Worldview snapshots + CMR HLS granules | browser-direct (CORS *) | per-box 30 d catalog query | 🟢 | No bulk: 1 catalog query/box, tiles bounded, 6 in flight |

## Infrastructure (bundled static)

| Set | Count | License warning |
|-----|-------|-----------------|
| Datacenters (OSM extract) | 4,351 | ODbL; incomplete by nature, labeled that way |
| Dams (OpenInfraMap/OSM) | 704 | ODbL |
| Submarine cables (TeleGeography) | 712 | **NonCommercial — commercial users must delete or license** |
| Mapped installations (OSM + Overture + optional Overpass/Google Places) | viewport-driven | Community mapping, incomplete by nature |
| Neighborhoods / Natural Earth regions | bundled | see per-folder provenance in `src/data/local_data/` |

Plus: Radio Browser (PDDL directory; broadcaster streams per-owner terms), cockpit Local Info weather (Open-Meteo CC BY 4.0), cockpit headlines (Google News RSS personal/noncommercial + GDELT fallback).

## Local receivers (the fleet-relevant bit)

`docs/LOCAL-RECEIVERS.md` + `server/providers/local-receivers.js`:

- **Local ADS-B:** `LOCAL_RECEIVER_FEEDS=1090=http://<lan-host>:8080/data/aircraft.json,...` — loopback/RFC1918/localhost/`*.local` only, path must end `aircraft.json`. Relayed server→browser with ~1 s in-memory cache. Selected local aircraft enriched via same adsbdb proxy (24 h disk cache). ADS-B unauthenticated: incomplete/delayed/spoofable — not for nav.
- **Broadcast FM:** USB RTL-SDR in-browser via WebUSB (`@jtarrio/webrtlsdr`). Samples/audio/optional location stay in browser. Nothing stored/redistributed.
