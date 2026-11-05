# albumcraft — Dossier (draft 2026-11-02)

Source: LightCraft app (`album.*`, `catalog.query/stats`, `activity.list`) × `immich-mcp` (`list_albums/create_album/add_to_album/share_album`, `search_photos` CLIP+OCR, people/faces) × `rust-photoprism-mcp` (server fallback)
Target: `D:\Dev\repos\albumcraft` (Bucket A candidate, but Python pilot first — server + demo-library mix)
MCP key: `albumcraft` — binary `albumcraft-cli.exe` — `albumcraft-cli mcp --demo` / `--library DIR`
Democraft family: `core`. Webapp: reuse democraft gallery, no new webapp in pilot.

## 1. Why albumcraft, why not photocraft / lightcraft

You asked: aren't both photo editors? No — three different jobs:

**PhotoCraft = Photoshop clone (pixels, layers)**
- `photocraft-cli convert|info|run|batch|droplet|commands|mcp|serve`
- Engine: `file.new/close`, `select.*`, `layer.new.layer/group/duplicate/delete/select/setProps/arrange/*`, `layer.createClippingMask`, `layerMask.*`, `mergeDown/mergeGroup/flattenImage`, `newFillLayer.solidColor/gradient`, `newAdjustmentLayer.brightnessContrast/levels/curves/exposure/vibrance/hueSaturation/colorBalance/blackWhite/photoFilter/channelMixer/invert/posterize/threshold/gradientMap/selectiveColor/colorLookup`, `layerStyle.dropShadow/innerShadow/outerGlow/.../bevelEmboss`, `filter.blur.* / sharpen.* / noise.* / pixelate.*`, `paint.stroke`, `tools.setColors`, `image.imageRotation.*`, `document.inspect/pixel`, `layer.list`
- Model: layered document (`.pcraft/.psd`), selection + layers + masks + styles. Destructive pixel work, brush strokes.
- Use when: retouch, composite, “cut this out, put that behind.”

**LightCraft = Lightroom clone (library + raw developer, parametric)**
- `lightcraft-cli run|mcp|render|snapshot|merge hdr|panorama|...|commands`
- `run --demo / --library DIR / --import PATH / --connect ADDR`, `mcp --demo/--library`, `render IN -o OUT --set light.exposure=0.5 --preset ID --size --quality + --opt colorSpace/bitDepth/...`, `snapshot --demo/--library --script`, `merge hdr-batch` etc.
- Commands: `album.create/list/addPhotos/removePhotos/smart/ruleFields/setRules/setCover/sort`, `catalog.query/stats`, `activity.list/cancel` (imports, preview builds, face scan), `crop.*`, `curve.presets/applyPreset`, `develop.*` sliders (exposure, color), `app.export` (jpeg/png/tiff/webp/avif/jxl/psd/dng + watermark + colorspace + ppi + sharpen + metadata), `app.gpu/memoryBudget`, `beforeAfter.*`, `presets.list`
- Model: catalog + raw + non-destructive develop settings + albums. No layers, no brush strokes. Edits are slider values, re-rendered on export.
- Use when: ingest 1000 raws, cull, develop, export. “Make all these look right.”

**albumcraft = curator/organizer (albums, faces, search, share)**
- Model: album = {id, name, smart?, rules, photos[], cover}. Photo ref = {id, rating, faces[], keywords[], date}.
- No pixels, no sliders. Verbs: organize, find, share.
- Use when: “find all birthdays with Anna, make an album, share a link.” That is neither Photoshop nor Lightroom-develop — it is Immich + LightCraft-albums fused.
- Hence: `photocraft` taken (correctly), `lightcraft` installed (correctly), `albumcraft` missing (this dossier).

## 2. Fit test

1. Single model? YES — album.
2. Headless verbs? YES with `--demo` library + sim Immich. LightCraft `--demo` gives procedural demo library with no server. Immich needs token — gate behind sim.
3. Files in/out? YES — `run.json` + `album.json` + contact-sheet JPG + `share.json` (sim).
4. 3 recipes obvious? YES — see §5.

## 3. Verb map

| albumcraft CLI | from | params | notes |
|---|---|---|---|
| `albumcraft album list` | LightCraft `albums.list` / immich `list_albums(shared,include_stats)` | shared?, stats? | read-only, always runs. Unify: LightCraft local + Immich server both listed, source tagged `local|immich`. |
| `albumcraft album create --name X [--smart --rules JSON]` | LightCraft `album.create/createSmart/ruleFields` / immich `create_album` | name, rules? | Mutating, tmp `ci-TIMESTAMP` only in ci. Smart rules: rating/ratingOp/flag/keywords/camera/lens/dateFrom/dateTo/text (from `album.ruleFields`). |
| `albumcraft album add|remove --album ID --ids a,b,c` | LightCraft `album.addPhotos/removePhotos/toggleTarget` / immich `add_to_album` | albumId, photoIds[] | Mutating, tmp only. Local photos skipped (albums hold library photos) — report `skipped`. |
| `albumcraft catalog query --text Q [--limit 20]` | LightCraft `catalog.query(filter,sort,offset,limit)` / immich `search_photos` (CLIP semantic + OCR text-in-image) | query, limit | read-only. LightCraft filter → text search; Immich CLIP → semantic. Tag source in `run.json`. |
| `albumcraft faces list|cluster` | Immich people/faces (`tag_person`, faces) + LightCraft face-scan `activity.list` | — | read-only. Fixtures only (no real PII in repo). Sim faces when no token. |
| `albumcraft share link --album ID` | Immich `share_album` | albumId | Mutating (creates link). Sim default: write `share.json` with `sim:true`, fake URL marked sim. Live only with `IMMICH_TOKEN`, never in default ci. |
| `albumcraft ingest --dir DIR` | LightCraft `--import PATH` + `activity.list` | dir | Headless import into tmp `--library`, poll `activity.list` until done. Asserts counts. |
| `albumcraft export sheet --album ID --out sheet.jpg` | LightCraft `app.export` + `snapshot` | albumId, out | Writes contact-sheet for democraft gallery. |

Out of scope pilot: LightCraft `develop.*` sliders, `merge hdr/panorama`, `curve.*`, PhotoCraft `layer.*`/`filter.*` (different crafts), Immich `upload_photos` prod upload, `server_health/storage_info` except as `down` probe.

## 4. CLI spec

```
albumcraft-cli album list [--shared true|false] [--json]
albumcraft-cli album create --name ci-20261102-1200 [--smart --rules '{match:all,rules:[...]}']
albumcraft-cli album add --album ID --ids a,b,c
albumcraft-cli catalog query --text "birthday Anna" --limit 20
albumcraft-cli faces cluster
albumcraft-cli share link --album ID [--live]
albumcraft-cli ingest --dir ./fixtures/photos --library ./tmp/lib
albumcraft-cli export sheet --album ID --out outbox/album/sheet.jpg
albumcraft-cli mcp [--demo] [--library DIR] [--immich-url URL]  # stdio
albumcraft-cli tools
```

- `--help` works. `--json` one doc to stdout. Exit non-zero on fail.
- Roots: `--allow-path D:\Dev\repos` (or ArtCraft roots). Never write outside tmp/outbox in recipes.
- Live gates: `--live` required for real Immich share/upload; without it, sim. Env `IMMICH_TOKEN` never logged, redacted in `run.json`.

## 5. MCP spec (thin)

- `type: local`, `command: [albumcraft-cli.exe, mcp, --demo]`, `enabled: true`, `timeout: 60000`.
- Tools: `album_list`, `album_create`, `catalog_query`, `faces_list`, `share_link_sim` (safe subset). Mutating live tools behind separate `albumcraft_live` toolset (democraft `capabilities` lists `live:false` in ci).
- No ports. No new webapp (use democraft gallery).

## 6. Democraft recipes (required 3)

Fixtures: `fixtures/photos/` (3-5 CC0 JPGs, no real faces; synthetic face labels in sidecar JSON).

1. `album/create-add-query` — `ingest --dir fixtures` into tmp `--library` → `album create --name ci-TIMESTAMP` → `album add --ids` (3) → `catalog query --text` → assert 3 present → `album delete` (or leave tmp, nuke library dir). `run.json` + report with counts + ms. Always runs (`--demo` or tmp library, no token).
2. `album/smart-faces-sim` — `album smart-create --rules rating>=3` → `faces cluster` (sim fixtures) → assert smart count + faces JSON. Report `sim:true` when no `IMMICH_TOKEN`, `live:true` + redacted URL when token present (never in default ci). Always runs.
3. `album/share-sim` — `share link --album` (sim) → assert `share.json` with `sim:true`, fake URL clearly marked. Live share skipped unless `--live` + token. Writes contact-sheet via `export sheet` for gallery. Always runs.

Each writes `outbox/album/<demo>/run.json` + `*-report.md` with measured numbers (album ids, counts, ms, source `local|immich|sim`).

## 7. Gates

- `just ci` green. `crafts.py` entry (exe, verbs, HERO, family=core, capabilities `demo:true,live:false` in ci). `appMeta.ts` hue/icon, ContactSheet tile, Ctrl+K.
- `data/craft_compat.json` baselines (gitignored). `opencode.json` entry validated via `ConvertFrom-Json`.
- Max 10 files per commit, `.bak` for 3+ edits. `HANDOVER.md` + session-log on ship.

## 8. Risks

- Server creds in bench → redact, sim default, `--live` explicit, never in default ci.
- Real PII (faces) → fixtures only, synthetic labels, no real photos in repo.
- LightCraft library locking → tmp `--library` per recipe, nuke after.
- Immich absent → `down`/`sim` receipt, not fail (SearchStudio rule).
- Confusion with photocraft/lightcraft → docs must state: pixels vs light vs curation (see §1). Gallery grouping by family helps.

## 9. Effort

M (3-5 days). LightCraft verbs exist, Immich verbs exist, fuse + sim + 3 recipes + gallery tile. No engine work.

## 10. Next

Approve → scaffold `D:\Dev\repos\albumcraft` (Python FastMCP thin over `lightcraft-cli --demo` + `immich-mcp` client, or Rust if Bucket A dossier names blocker), add `crafts.py` entry, write fixtures + 3 recipes, `just ci`, shots via `node webapp/scripts/shots.mjs`.
