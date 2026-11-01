# World Labs — Browser vs API billing (Marble vs Platform)

> **One-line take:** `marble.worldlabs.ai` (browser) and `platform.worldlabs.ai` (API) are two **separate** accounts/balances/credit pools, even with the same email. Credits do not transfer (\u201cMarble credits cannot be spent on API, API credits cannot be spent in Marble\u201d \u2014 `docs.worldlabs.ai/marble/support/account-billing`). Sandra\u2019s wodlabs workflow is API-only, so the ~30\u20ac/mo Standard browser sub is redundant. Gallery browsing is public.

## 1. What the browser subscription (~30\u202f\u20ac/mo = Standard) actually unlocks

Source: `docs.worldlabs.ai` llms.txt/index, `marble/export/gaussian-splat`, `marble/support/account-billing`, `marble.worldlabs.ai/pricing` (dynamic table).

### Tiers & gates

| Plan | Worlds/mo | What it gates |
|------|-----------|---------------|
| **Free** | 4 | Text, single image, 360\u00b0 panorama only. No multi-image / video / Chisel (3D blockout), no editing, no export, no community downloads |
| **Standard** (~30/mo) | 12 | + multi-image (2\u20138, azimuth Front/Back/Left/Right or Auto Layout), video (<100\u202fMB), **Chisel** coarse-3D \u2192 detail, **reuse prompt**, **editing** (pano-edit: brush area + NL fix), **download community worlds**, **exports** (SPZ/PLY 3 LoDs, panorama JPG, collider GLB) \u2014 \u201cStandard covers splat exports \u2026 what you need for Unreal/Unity/Blender/Houdini\u201d |
| **Pro** | 25 | + **expand** (click beyond bounds \u2192 2k-credit seamless growth), **variation** (alt takes), **HQ textured mesh (GLB)**, enhanced video output, **commercial rights** |
| **Max** | 75 | High-volume |
| **Enterprise** | custom | `marble.worldlabs.ai/enterprise` |

Top-up credits roll over 1y; subscription credits don\u2019t (used first). \u201cPurchase credits\u201d button is disabled on Free.

### Browser-only creative loop (no API equivalent)

* **Create:** presets / roll-for-marbles, reuse-prompt iterator
* **Edit:** pano-edit (~20\u202fs), expand (~5\u202fmin), variation
* **Studio:** **Compose** (stitch N worlds into a seamless larger map — game-level builder, `marble/create/studio-tools/compose`), **Record** (keyframed cinematic camera \u2192 mp4 flythrough, `marble/create/studio-tools/record`)
* **Chisel** in-browser coarse 3D blockout (`marble/create/chisel-tools/chisel-basics`) as generation scaffold
* **Web/VR sharing:** one-click share link + VR link (hosted viewer)
* **Gallery** tabbed by `curated/stylized/realism/interior/hq/fantasy/sci-fi/all` with likes, owners, prompts, seeds, minimaps — browse free, download gated to Standard+
* Gen times: draft 20\u202fs, pano 30\u202fs, multi/vid 2\u202fmin, world/expand 5\u202fmin, mesh 1\u202fh (docs.worldlabs.ai index)

### Export note (trap)

`marble/export/gaussian-splat` note: *\u201cExporting requires a paid plan. Standard covers splat exports (SPZ and PLY), 360 panoramas, and collider meshes \u2026 HQ textured mesh export and commercial rights come with Pro. The Free plan can generate worlds but not export them.\u201d* This is the browser gate \u2014 it does **not** apply to API `worlds:export`.

## 2. What the API billing (Platform) is

`docs.worldlabs.ai/api/pricing` — **per usage-event** credits at `platform.worldlabs.ai/billing`:

* Base + input credits + per-edit charges (edit pano ~150, expand 2\u202f000), auto-refill threshold + overage. Named totals: `marble-1.0-draft`, `marble-1.0/1.1` (~1500 base), `marble-1.1-plus` (1500 + 300 per dynamic cube). Draft is cheapest for iteration.
* API exposes only `worlds:generate/get/list/export/delete`, `media-assets:prepare-upload/get`, `operations:get`, `credits:get`, `pano:depth_to_rgb`. **No** pano-edit, expand, variation, compose, record, VR-link \u2014 browser-only.
* Same email \u2260 same balance. You can be on Free in Marble and still get a Platform invoice.

## 3. Gallery \u2014 free or gated?

| Surface | Auth | Gated? |
|---------|------|--------|
| `marble.worldlabs.ai` \u2192 Gallery \u2192 **Download** button | Marble session | **Standard+** |
| `api.worldlabs.ai/api/v1/worlds:by-tag` (`tag=curated/\u2026`, `page_size`, `page_token`, `Referer: marble.worldlabs.ai`) | **none** | **public** |
| `worldlabs-mcp` \u2192 `gallery_explore(operation=browse|world|prompts|search)` + `GET /api/gallery` / `GET /api/gallery/search` + `scripts/gallery_scrape.py` | none | public; returns `{prompt, seed, owner, like_count, spz_urls[], minimap_url, marble_url}` |
| Your own worlds via `get_world(world_id)` | `WORLDLABS_API_KEY` | Platform (your gens only) |

Asset URLs inside are temporary signed GCS (`spz_urls` expire ~1h, GLB collider persists); `downloadAssetUrl(\u2026?asset_type=splat_500k)` and `proxy_splat_asset` bypass CORS while the MCP bridge runs.

## 4. Recommendation for an API-only shop (today)

* **Cancel Standard, keep Platform auto-refill.** `WORLDLABS_API_KEY` + `worldlabs-mcp` (22 tools: 20 server + 2 prefab) covers text/image/multi/video \u2192 `get_operation`/`wait_for_world` \u2192 `get_world` \u2192 SPZ/GLB/pano. The dashboard \u201conboarding cue\u201d now correctly hides once `GET /system` reports `api_key_set:true` (dismissible via `localStorage:worldlabs-onboarding-dismissed`).
* Gallery as mood-board is still free unauthenticated \u2014 reuse owners\u2019 prompts/seeds (credit owners).
* Re-subscribe to Standard **only** if you want the browser loop (pano-edit typos, expand horizons, compose game maps, record flythroughs) or hosted share/VR links without self-hosting Spark/`.RAD`.

## 5. Links

* `docs.worldlabs.ai` \u2192 `marble/support/account-billing` (the \u201cMarble credits cannot be used with World API\u201d callout), `api/pricing`, `marble/export/gaussian-splat`, `marble/export/specs` (SPZ/GLB/pano specs), `api/reference/*` (OpenAPI)
* In-repo: `worldlabs-mcp/docs/CONFIGURATION.md` (env table), `docs/FEATURES.md` (21\u219222 tools, now includes `worldlabs_shutdown`), `web_sota/src/pages/dashboard.tsx:ONBOARDING_DISMISS_KEY` (reminder fix), `src/worldlabs_mcp/server.py:GALLERY_API`
* Memops: `projects/world-labs-browser-vs-api-billing-and-gallery-access-2026-09-01`
