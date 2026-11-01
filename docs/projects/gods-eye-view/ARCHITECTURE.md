# God's Eye View — Architecture (deep pass at `8b8ccc9`)

Source: local clone `D:\Dev\repos\_upstream\gods-eye-view`, plus `docs/CURRENT-STATE.md`, `docs/CODE-BOUNDARIES.md`, `docs/UI-OWNERSHIP.md`, `package.json`, `vite.config.js`, `server/`, `src/`.

## 1. Runtime shape

```
browser (CesiumJS scene, vanilla JS UI)
  -> same-origin /api/* (Vite dev proxy -> server/providers/*)
    -> public upstreams (OpenSky, adsb.lol, AISStream WS, CelesTrak, USGS, NOAA, ...)
```

- **No framework.** `src/main.js` (~650 lines bootstrap), `src/ui.js` facade, `src/hud.js` intel HUD + AI summary, `src/mapStackController.js` basemap switching, `src/app/*` application composition, `src/ui/*` panels.
- **Build:** Vite 6 + `vite-plugin-cesium` 1.2.23. `vite.config.js` re-exports `server/standalone/vite.config.js` — the dev server IS the proxy. `npm run build:panel` builds the in-conversation MCP globe; rerun after app changes.
- **Deps (runtime, small):** `cesium`, `satellite.js` (SGP4), `hls.js` (DelDOT/Norway live video), `mapillary-js`, `@meri-imperiumi/eccodes-wasm` (GRIB2 wind), `egm96-universal`, `mgrs`, `@mapbox/vector-tile`+`pbf`, `@jtarrio/webrtlsdr`+`@jtarrio/signals` (local RTL-SDR).
- **DevDeps:** `vite`, `puppeteer` (QA harnesses), `sharp`, `ws`, `prettier` 3.9.6.

## 2. Directory map (what lives where)

| Path | Role |
|------|------|
| `src/app/` | Application composition: `application.js`, `viewer.js`, `scene.js`, `controls.js`, `data.js`, `tools.js`, `catalog.js`, `operations.js`, `sources.js` |
| `src/ui/` | Panels, HUD, styles, control facade; `panelRails.js`, `panelDisclosure.js`, `surfaceKeyboard.js`, `visualInput.js`, `displayControls.js`, `effects.js`, `mapSource.js`, `layers.js`, `location.js`, `radio.js`, `cctv.js`, `context.js`, `cockpit.js`, `scenes.js`, `applicationShell.js`, `navigationController.js`, `shareRestoration.js`, `visualSettings.js` |
| `src/maps/` | `controller.js`, `catalog.js`, `imagery.js`, `terrain.js`, `google3d.js`, `defaultSources.js` — the basemap ladder |
| `src/layers/` (25 dirs) | `flights`, `military`, `aircraft`, `vessels`, `earthquakes`, `satellites`, `launches`, `installations`, `traffic`, `transit`, `bikeshare`, `directions`, `cctv`, `alpr`, `radio`, `weather`, `wind`, `cyclones`, `firms`, `perimeters`, `recentImagery`, `streetLevel`, `submarineCables`, `awareness`, `localAdsb` |
| `src/data/` | One module per layer + `manager.js` orchestration + `contextStore.js` + `lifecycle.js` + `local_data/` bundled sets |
| `src/sources/` | Portable fetch contracts: `live/index.js`, `radioBrowser.js`, `cctvTypes.js`, `regional.js`, `overpass.js`, `nominatim.js`, `transitService.js`, `httpBody.js` |
| `src/voice/` | Realtime session + tools (see VOICE_AND_MCP). `realtimeController.js`, `realtimeSession.js`, `realtimeBackend.js`, `realtimeConnection.js`, `realtimeTurns.js` (40 KB), `gevActions.js` (166 KB), `actionSchemas.js`, `layerManifest.js`, `pointerContext.js`, `speech.js`, `voiceCost.js` |
| `src/annotations/` | Voice + manual whiteboard (areas, lines, pins, routes, distance arrows) |
| `src/director/`, `src/scenes/` | Cinematic scene director, playback, shareable scene bundles |
| `src/search/` | Keyless geocoder, Nominatim, bundled cities/landmarks |
| `src/tools/` | Portable tool catalog (`defineTool` + `composeCatalog`), `queries/` per domain, `mcp/` adapter, `functions.js` adapter, `services.js`, `surfaces.js` |
| `src/sdr/` | Browser WebUSB RTL-SDR (FM broadcast receiver, local ADS-B via decoder `aircraft.json`) |
| `server/providers/` | `cctv.js`, `cyclones.js`, `firePerimeters.js`, `firms.js`, `gbfs.js`, `live.js`, `local-receivers.js` (18 KB), `local.js`, `mapillary.js`, `military-installations.js`, `openai.js`, `overpass.js`, `places.js`, `radio.js`, `regional.js`, `space.js`, `terrain.js` (heights), `traffic.js`, `transit.js`, `weather.js` (21 KB), `wind.js` |
| `server/mcp/` | `stdio.js` — MCP server reading a running app's `/api` routes |
| `server/standalone/` | `vite.config.js`, `key-setup.js` (POWER UP backend), `voiceTools.js` |
| `config/` | e.g. `cctv_sources.*.json` source packs; `CCTV_SOURCES_FILE` / `CCTV_SOURCES_JSON` overrides |
| `scripts/` | ~40+ QA/build scripts: `qa-*.mjs` per surface, `check-package-boundaries.mjs`, `check-import-directions.mjs`, `setup-doctor.mjs`, `dev-fresh.sh`, Pinokio `pinokio-*.mjs` |
| `public/models/` | Shipped 3D aircraft + `README.md` provenance per model |

## 3. Map stacks (the basemap ladder)

`src/mapStackController.js` + `src/maps/*`. Order matters:

1. **Esri World Imagery + OSM** — keyless default. OSM auto-fallback if Esri unreachable; globe continues without terrain if heights unavailable.
2. **Cesium ion** — free Community token (eligible personal/non-commercial): ion-hosted Google Photorealistic 3D + world terrain + extra imagery stacks.
3. **Direct Google** — metered Map Tiles API + place search. Same 3D, direct billing.

Traffic/cables/cloud shells behave differently per stack (draped vs terrain vs floating shells — see DATA_LAYERS).

## 4. Motion & symbology correctness (the hard parts, done right)

- **One interval behind + interpolate + dead reckon.** Feeds arrive 15–60 s; render reads last two fixes, interpolates, projects forward on gaps. Choppy input, smooth globe.
- **World-stable headings** (`src/data/iconOrientation.js`): per-frame screen-space course projection. Aircraft/ships point true heading at every camera angle, tracked or not, nadir or horizon. No viewport-lock spin.
- **Locked orbit rings** (`satellite.js` SGP4 + GMST realignment): rings stay glued, no drift/flicker.
- **Ground floor** (`groundCast.js`, `meshSampler.js`): at street zoom on Google 3D, surface mode flips draped→terrain; lines/cones/markers sit 2 m over bare earth from `/api/terrain/heights`; within 900 m, `scene.sampleHeight` (~11 m cells, 6 ms idle budget) follows trenches/steep streets; failed probes keep last-good + cooldown retry.
- **Governors:** `src/renderGovernor.js`, OpenSky credit governor, TomTom daily tile budget (default 6,000/day ≈ 186 k/31 d, inside 200 k/mo free), disk-cached TLEs, Mapillary tile strip (12 MB → ~80 KB by dropping unused `image` layer), one shared upstream fetch per tile.

## 5. Boundaries (enforced, not aspirational)

- `npm run check:boundaries` enforces `scripts/package-boundaries.json`: `gods-eye-view/tools` and `gods-eye-view/tools/mcp` are portable — no app/rendering/Node/Cesium/browser-global imports. Only voice reaches them (`withToolCatalog` in `src/voice/gevRealtime.js`).
- `npm run check:boundaries` also runs `check-import-directions.mjs`: dependencies point downward only.
- `UI-OWNERSHIP.md` / `VOICE-OWNERSHIP.md`: per-panel/component owners (scene, HUD, cockpit, camera, radio, location, layer panel, map source, effects, display, shortcuts/shaders, rails, disclosure, keyboard). Useful template for our own ownership docs.
- Tests colocated (`*.test.mjs` next to source) + `scripts/run-unit-tests.mjs`; Puppeteer QA per surface; fixture-mode QA (e.g. `qa:street-level:fixtures`) so CI needs no network.

## 6. State & sharing

- Layer state tokens (`scripts/next-layer-state-token.mjs`, `check-layer-state-tokens.mjs`): share-link v2 serializes camera + style + layers + one tracked target (`0.m.0` Mapillary off, `0.p.p` panos-only, `0.s.365` last year, etc.).
- `src/sharelink.js` (27 KB) + celestial tests (35 KB). A live target is a handoff, not a bookmark.
- Annotations persist until `clear the map`; Director scenes import/export as files/bundles with anchors + moves + data packs.
