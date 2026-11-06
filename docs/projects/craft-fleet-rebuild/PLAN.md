# Fleet Craft Rebuild — Grand Plan

**Status:** draft 2026-11-02
**Owner:** Sandra S. + fleet agents
**Scope:** 10 pilot crafts, not 200 repos. Prove verbs, then decide.
**Sources:** `D:\Dev\repos` (339 entries), `C:\Program Files\*Craft` (16 CLIs), `democraft-mcp` v0.3.0 (15 apps, 35 demos), `LEN-VL.pdf` extraction workflow (pdfcraft-cli text → reportlab → pdfcraft-cli info), `opencode.json` craft map 2026-11-02.

## 0. Executive summary

Do NOT rebuild ALL fleet repos as crafts. Rebuild 10 where the repo is already tool-shaped (document/model + headless verbs + files in/out). Leave daemons, bridges, observers alone.

Pilot order:
1. `virtucraft` (from `virtualization-mcp`) — VMs as documents.
2. `dbcraft` (finish `D:\Dev\repos\databasecraft`, consolidate `database-operations-mcp`) — DB as document.
3. Wave 1 (3-6): `revecraft`, `doccraft`, `filecraft`, `gitcraft`.
4. Wave 2 (7-11): `containercraft`, `bookcraft`, `meshcraft`, `benchcraft`, `splatcraft`.

Success = `just ci` green + 3 democraft recipes each with `run.json` + `*-report.md` + `data/craft_compat.json` baselines. No recipe, no craft.

## 1. Why craft pattern, when it fits, when it doesn't

### 1.1 The pattern (from Storytold ArtCraft + SolidCraft + Craft Anything)

- One binary: `*-cli.exe <verb>` for humans, `*-cli.exe mcp` on stdin/stdout for agents. Same engine.
- Confinement: `--automation-read-root DIR --automation-write-root DIR` (ArtCraft), `--allow-path DIR` (SolidCraft), `--root DIR` (pdfcraft compact mode). Agent file tools cannot escape.
- Headless first: every democraft demo is a real CLI run, not a mock. `src/democraft_mcp/recipes.py` dispatched via `RECIPES[(app,demo)]` with `RunCtx.do_with(exe, argv)`. Output: `outbox/<app>/<demo>/` with `run.json` + report.
- Registry: `democraft-mcp/src/democraft_mcp/crafts.py` — one entry per app (exe, verbs, HERO facts, family core/community). Webapp contact-sheet on 11245/11246 (`GET /api/gallery`, `GET /api/crafts`).
- MCP thin: FastMCP or Rust MCP wrapper, stdio, `MCP_TRANSPORT=stdio`, `FASTMCP_BANNER=0`. No ports except webapps.
- Compat: `data/craft_compat.json` (gitignored) pins 104 verbs across 13 core CLIs (Oct 31 builds). New craft must add its verbs without breaking existing.

### 1.2 Fit test (must answer YES to all 4)

1. Single model? (VM, DB, binary, document, book, mesh, capture, repo, container, file)
2. Verbs are headless? (no OAuth browser dance, no 2FA, no interactive pairing)
3. Files in/out? (can write `run.json` + artifact to `outbox/`)
4. 3 recipes obvious? (if you can't name 3 demos in 30 seconds, it's not a craft)

### 1.3 Explicit non-goals

- No rename churn for its own sake. `email-mcp` stays `email-mcp` even if it grows `cli` verbs. Craft name only when model+verbs fit.
- No Python→Rust rewrites unless Bucket A/B (see §2). Craft is about interface, not language.
- No 200-repo sweep. Max 10 files per commit, 3+ file edits need timestamped `.bak` (fleet rule).

## 2. Bucket triage (from RUST_ARTCRAFT_STANDARD.md §3)

- **Bucket A (REST/cloud/SQLite/CLI/system) + Bucket B (clean hardware/SCPI/LAN IoT):** Pure-Rust ArtCraft 3-tier (`L1 <domain>-core`, `L2 <domain>-mcp`, `L3 <domain>-app`). Default for `virtucraft`, `dbcraft`, `containercraft`, `benchcraft`.
- **Bucket C (embedded host-app Python) + Bucket D (PyTorch/CUDA ML):** Stay Python/FastMCP. Applies to `blender-mcp` (host-owned), `invokeai/comfy` (CUDA), `speech-mcp` (mic/STT routing).
- Dossier must name bucket + blocker in `docs/DEVELOPMENT.md` or `HANDOVER.md`. "Faster to write" is not a blocker.

## 3. Why calibre → bookcraft YES, plex → videocraft NO

### 3.1 Calibre is file-shaped

- `calibre-mcp` + `rust-calibre-mcp` operate on files: EPUB/PDF, metadata.db, covers, full-text index. Verbs map 1:1:
  - `query_books(search) / calibre_metadata_search / rag_retrieve` → `book search --query`
  - `manage_books(details) / manage_comments(read)` → `book info --id`
  - `manage_files(convert) / export_books(pandoc)` → `book convert --to epub`
  - `search_fulltext / rag_retrieve` → `book grep --query`
- No server login, no streaming, no transcode session. Can run headless on `D:\Dev\repos` with `--automation-read-root`. Democraft recipes obvious:
  1. `book/search-and-info` (find + dump metadata)
  2. `book/convert-roundtrip` (epub→pdf→txt, measure bytes)
  3. `book/fulltext-find` (fts query + snippet + location)
- Hence `bookcraft`. Short, matches `pdfcraft/solidcraft` convention.

### 3.2 Plex is server-shaped

- `plex-mcp` wraps a running Plex Media Server: auth token, library sections, watch state, transcode sessions, remote access, companions. 80% of calls need a live server + account, not a file.
- Hypothetical `videocraft` verbs (`transcode / thumbnail / probe`) already exist better in `handbrake-mcp` (files) + `FilmCraft/EffectCraft` apps (render). Plex adds server state on top.
- Forcing Plex into craft verbs would either (a) duplicate handbrake badly, or (b) leak server creds into headless recipes (token in `run.json` — no).
- Decision: **DO NOT make videocraft from plex-mcp.** If video files need a craft, derive from `handbrake-mcp` + `ffmpeg` + `qcad`? No — derive from file transformers:
  - `handbrake-mcp` (transcode) + `ffmpeg` (probe) + `resolume-mcp` (clips)? Still weak. Better: leave video to FilmCraft/EffectCraft apps via democraft, keep `plex-mcp` as bridge.
- Rule: library managers (Plex, Immich, Calibre-server mode) are NOT crafts. File transformers (epub→pdf, mp4→thumb, raw→jpg) ARE.

## 4. Why photocraft from immich + “one other” is a trap

User intuition: “photocraft would just derive from immich and one other photo tool.” Understandable, wrong shape.

- `immich-mcp` (+ `rust-photoprism-mcp`) are server-shaped like Plex: timelines, ML search, faces, albums, sharing, auth. Recipes would need a seeded server + API key, not files. That violates Fit Test #2 and #3.
- Photo *files* DO craft cleanly, but sources are different:
  - EXIF: `exiftool` via `pdf-mcp`? No — via `fileops` + `pillow` (already in democraft dev deps).
  - Convert/dedupe/thumb: `pillow`, `rawtherapee`? Actually `immich` thumbnails are server-side; file-side is `ImageMagickalleries.
- Correct split:
  - **Keep `immich-mcp` as bridge** (server). Do not craft.
  - **If photocraft needed**, derive from file tools: `exif read/write / convert / dedupe-by-hash / contact-sheet` using `pillow>=13` (democraft already depends). Recipes:
    1. `photo/exif-strip-and-thumb` (read exif → strip → 256px thumb, measure)
    2. `photo/dedupe-find` (hash dir, report dups)
    3. `photo/contact-sheet` (montage + html gallery)
  - “One other photo tool” should be `rust-photoprism-mcp` file-mode or `exiftool`, NOT immich-server mode.
- Decision: **No photocraft in Top 10.** Photo files covered by `filecraft` exif verbs + PhotoCraft the app (already installed). Revisit only if 3 file-recipes prove out. Do not fuse two servers into a fake craft.

Same logic kills `plex→videocraft`, `email→mailcraft`, `discord→chatcraft`, `aiwatcher→watchcraft`.

## 5. The 10 — detailed

Naming: short, lowercase, `*craft`, CLI `*craft-cli.exe`, MCP key same as dir. `virtucraft` > `virtualizationcraft`, `dbcraft` > `databasecraft` (but `databasecraft/` dir already exists — keep dir, publish as `dbcraft` alias or rename dir after pilot; do not keep both names long-term).

### #1 virtucraft (from virtualization-mcp) — PILOT, P0

- Source: `D:\Dev\repos\virtualization-mcp` (`virtops_*`: `vm_management`, `snapshot_management`, `network_management`, `storage_management`, `hyperv_management`, `libvirt_management`, `sandbox_management`, `system_management`)
- Model: VM = {name, os_type, memory_mb, disk_gb, snapshots[], nics[], disks[]}
- Verbs (CLI):
  - `virtucraft vm list --json`
  - `virtucraft vm info --vm NAME`
  - `virtucraft vm start|stop --vm NAME [--force]`
  - `virtucraft snapshot list|create|restore|delete --vm NAME [--snap NAME]`
  - `virtucraft network list|create --name NET [--ip IP --netmask MASK]`
  - `virtucraft storage list-disks|create-disk --name D.vdi --size-gb N`
- MCP: thin portmanteau `virtucraft(operation=...)` or 1:1 tools; stdio; no port.
- Democraft recipes:
  1. `virt/list-and-info` (list → info first VM, assert json keys)
  2. `virt/snapshot-roundtrip` (create test snap → list → delete, measure ms)
  3. `virt/network-create-delete` (host-only net create → list → remove)
- Effort: S (verbs exist). Bucket A → Rust candidate, but Python wrapper OK for pilot.
- Risk: Hyper-V needs admin; recipes must skip gracefully when no hypervisor. Gate with `crafts.py` capability `hyperv_present`.
- Success: 3 recipes green on Goliath (Windows 11, Hyper-V present).

### #2 dbcraft (finish databasecraft, consolidate database-operations-mcp) — PILOT, P0

- Sources: `D:\Dev\repos\databasecraft` (exists, Rust, Cargo.toml, crates/, justfile) + `D:\Dev\repos\database-operations-mcp` (Python)
- Model: DB connection + query + dump file
- Verbs:
  - `dbcraft query --db sqlite:///path.db "SELECT ..."` (also postgres/mysql via URL)
  - `dbcraft schema --db URL [--table T]`
  - `dbcraft backup --db URL --out dump.sql`
  - `dbcraft vacuum --db path.db`
  - `dbcraft diff --db1 A --db2 B` (schema diff)
- MCP: `dbcraft(operation=query|schema|backup|...)`
- Recipes:
  1. `db/queryardstick` (seed sqlite, run 3 queries, assert rows)
  2. `db/backup-restore-roundtrip` (backup → hash → restore to tmp → diff)
  3. `db/schema-diff` (v1 vs v2, assert added column)
- Effort: S-M (dir exists, need CLI surface + recipes). Decide: Rust `databasecraft` IS `dbcraft` — rename dir or keep dir + publish binary as `dbcraft-cli.exe`. Do not ship both names.
- Risk: credential handling (never log URL with password; use env). Portmanteau must redact.
- Success: works on sqlite file in `D:\Dev\repos` without creds.

### #3 revecraft (from reversing-mcp) — Wave 1, P1

- Source: `D:\Dev\repos\reversing-mcp` (`revops_*`: `analyze_binary`, `extract_strings`, `analyze_entropy`, `analyze_pe_file`, `engine die/capa/frida`, `ghidra`, `digibib`, `hercules*`)
- Model: binary file
- Verbs: `revecraft strings|entropy|pe-info|die|capa --file X [--json out.json]`, `revecraft dki-decode --file TEXT.DKI`, `revecraft snapshot --file X` (digibib bundle)
- Recipes: `rev/strings-entropy` (known exe, assert entropy + strings), `rev/die-capa-smoke` (skip if engines missing, report `down` not zero), `rev/dki-decode` (fixture DKI → txt, assert utf8)
- Effort: M (engines heavy: capa 42min on 4.7MB; gate with timeout + `down` receipts). SearchStudio pattern: dead pipes reported, not silent zeros.
- Risk: frida executes target — needs `confirm=True` + `accept_local=True`, logged VM opt-out. Never in `just ci` default.

### #4 doccraft (from libreoffice-mcp) — Wave 1, P1

- Source: `D:\Dev\repos\libreoffice-mcp`
- Model: office document
- Verbs: `doccraft convert --in docx --out pdf`, `doccraft text --in pdf`, `doccraft info --in file`, `doccraft combine a.pdf b.pdf --out c.pdf`
- Recipes: `doc/convert-roundtrip`, `doc/text-extract`, `doc/combine-split` (all with fixtures, measure bytes/pages)
- Effort: S. Overlaps pdfcraft verbs — that's OK, doccraft handles office in, pdfcraft handles pdf ops. Boundary documented.
- Risk: LibreOffice headless install drift. Pin version in `docs/`.

### #5 filecraft (from filesystem-mcp + disk-usage-mcp + sysinternals-mcp file verbs) — Wave 1, P1

- Sources: `filesystem-mcp`, `disk-usage-mcp`, file verbs of `system-admin-mcp`
- Model: file/dir/volume
- Verbs: `filecraft list|hash|grep|du|find-large --path DIR`, `filecraft strings --file BIN`
- Recipes: `file/hash-grep`, `file/du-top10`, `file/find-dups` (use `D:\Dev\repos` fixtures, never `C:\Windows`)
- Effort: S. Highest reuse (other crafts call it in `do_with`).
- Risk: path traversal — enforce `--automation-read-root`. Never allow `C:\` in recipes.

### #6 gitcraft (from git-github-mcp) — Wave 1, P1

- Source: `D:\Dev\repos\git-github-mcp` (`gitops_*`: `git_core`, `git_branch`, `git_admin`, `github_ops`, `fleet_*`)
- Model: repo + PR
- Verbs: `gitcraft status|log|diff --repo DIR`, `gitcraft pr-list|pr-view --repo owner/name`, `gitcraft fleet-dirty` (across `D:\Dev\repos`)
- Recipes: `git/status-clean-check` (assert clean or list dirty, never mutate), `git/log-recent` (parse 5 commits), `git/pr-list-fleet` (read-only, needs `gh auth`, skip if not logged in)
- Effort: M (GitHub needs auth; recipes must degrade to local-only). Never `force-push`, never `reset --hard` in recipes.
- Risk: mutation — recipes READ-ONLY. No commit/push in bench.

### #7 containercraft (fuse docker-mcp + podman-mcp + kubernetes-mcp) — Wave 2, P2

- Sources: 3 repos → 1 craft. Model: container/image/volume/network.
- Verbs: `containercraft ps|logs|exec --ctr NAME -- cmd`, `containercraft compose-ps|compose-logs --dir DIR`
- Recipes: `ctr/list`, `ctr/logs-tail`, `ctr/exec-echo` (hello-world image only; skip if daemon down, report `down`)
- Effort: M (3 repos to fuse, daemon flakiness). Use `fileops:container_ops` patterns, not new code.
- Risk: daemon not running on Goliath? Check first. Recipes skip, not fail, when daemon down.

### #8 bookcraft (from calibre-mcp + rust-calibre-mcp × readly-mcp) — Wave 2, P2

- Sources: `calibre-mcp` (Python), `rust-calibre-mcp` (Rust). Pick ONE (recommend Rust if ArtCraft, else Python). Do not ship both. Cross with `readly-mcp` for ingest (not storage).
- Model: book AND magazine issue AND comic/manga volume. Calibre already handles EPUB/PDF + CBZ/CBR (comics/manga), PDF magazines, metadata.db, covers, fulltext. Readly provides `search_magazines / list_library / open_latest_issue / list_articles / extract_article_text / read_all_articles / smart_scrape` (browser + `READLY_AUTH_TOKEN`, headless=False) — that is ingest, not library. Boundary: readly scrapes → markdown/PDF artifact → bookcraft stores/converts/greps.
- Verbs: `book search|info|convert|grep` (4 verbs, not 40 tools) + `book ingest-readly --mag NAME --out issue.md` (thin wrapper over readly `open_latest_issue + read_all_articles`, writes artifact to outbox, never mutates Calibre library in ci).
- Recipes: `book/search-and-info`, `book/convert-roundtrip` (epub→pdf→txt + cbz→pdf for comics, measure bytes/pages), `book/fulltext-find` (fixtures, no DRM books), `book/readly-ingest-sim` (fixture HTML → issue.md, no browser; live browser only with token, report `down` if absent).
- Effort: M (pick impl, thin CLI + readly ingest shim).
- Risk: Calibre library path config drift (`fleet-start.config.ps1` + env). Pin test library to fixtures. Readly needs login + non-headless browser — recipes default to sim fixture, live only with `READLY_AUTH_TOKEN` set, report `sim` otherwise. Never commit tokens.

### #9 meshcraft (ONE of blender-mcp / freecad-mcp / qcad-mcp / godot-mcp) — Wave 2, P2

- Pick ONE host: recommend `freecad-mcp` (headless CAD, STEP) OR `blender-mcp` (mesh). Do NOT craft all four. `CADCraft` app exists; `SolidCraft` already does parametric. Meshcraft fills import/export/render-thumb gap.
- Model: mesh/scene. Verbs: `mesh info|export --to stl|step|thumb --out png`
- Recipes: `mesh/info-cube` (primitive, assert bbox/volume), `mesh/export-roundtrip` (step→stl, measure), `mesh/thumb` (render 256px, assert png)
- Effort: L (host apps flaky headless). Gate: skip if host not installed, report `down`.
- Risk: Blender/FreeCAD headless on Windows is fragile. Timebox to 1 day; if no green recipe, drop from pilot.

### #10 benchcraft (fuse oscilloscope-mcp + logic-analyzer-mcp + multimeter-mcp + power-supply-mcp + spectrum-analyzer-mcp + function-generator-mcp) — Wave 2, P2

- Sources: 6 tiny instrument repos → 1 craft. Model: capture/trace.
- Verbs: `bench capture|decode|measure|export-csv --dev TYPE`
- Recipes: `bench/capture-sim` (simulated capture, no hardware), `bench/decode-uart` (fixture), `bench/export-csv` (assert rows)
- Effort: M (fuse + sim mode). Hardware-gated: all recipes run in `sim` when no device, report `sim` receipt.
- Risk: hardware absent on Goliath — sim must be first-class, not mock-to-pass. Declare `sim` in report.

### #11 albumcraft (from LightCraft album.* + catalog.query × immich-mcp + rust-photoprism-mcp) — Wave 2, P2
- Dossier: `albumcraft-DOSSIER.md` (this folder, 2026-11-02, 9.2 KB). Stub to wire in `democraft-mcp/src/democraft_mcp/crafts.py` + 3 sim-first recipes in `recipes.py` (see dossier §5-§6).

- Sources: LightCraft app (`album.create/list/addPhotos/removePhotos/smart`, `catalog.query/stats`, `activity.list`) for file/demo-library mode + `immich-mcp` (albums, ML search, faces, sharing, timelines) + `rust-photoprism-mcp` for server mode. Do NOT touch PhotoCraft (Photoshop clone, layers/retouch) or LightCraft develop sliders (exposure/color) — albumcraft is curation, not pixels, not light.
- Model: album = {id, name, smart?, rules, photos[], cover}. Photo = {id, library, rating, faces[], keywords[], date}.
- Why this seam works: photocraft=edit, lightcraft=develop, albumcraft=organize. No overlap. Immich alone fails Fit Test (needs seeded server + token in ci) — LightCraft `--demo` library gives headless fixtures, Immich gives AI (faces/search/share) gated behind token.
- Verbs:
  - `album list|create|add|remove --album NAME [--ids ...]` (from LightCraft `albums.list`, `album.create/addPhotos/removePhotos`)
  - `album smart-create --name X --rules '{match:all, rules:[...]}'` (from `album.createSmart`, `album.ruleFields`)
  - `catalog query --text QUERY --limit 20` (from `catalog.query`, Immich search fallback)
  - `faces cluster|list` (from Immich faces + LightCraft face-scan `activity.list`)
  - `share link --album NAME` (from Immich share; sim mode writes `share.json` with fake URL marked `sim`, never hits prod server in ci)
- Recipes (all against `--demo` library + sim Immich unless token present):
  1. `album/create-add-query` — create `ci-TIMESTAMP` → add 3 demo photos → `catalog.query --text` → assert 3 present → delete album. Measures ms, writes `run.json`.
  2. `album/smart-faces-sim` — `album smart-create --rules rating>=3` → `faces cluster` (sim: fixture faces) → assert smart count + report `sim` receipt if no Immich token.
  3. `album/share-sim` — `share link --album` → assert `share.json` with `sim:true`, no network. Live share only with `IMMICH_TOKEN` set, never in default `just ci`.
- Effort: M (fuse 3 sources, sim-first). LightCraft CLI already does `run/start`, `mcp --demo/--library`, `snapshot`, `merge` — reuse, don't reimplement.
- Risk: server creds in bench (never log tokens, redact in `run.json`), LightCraft library locking (use tmp `--library` per recipe), Immich absent → `down`/`sim` receipt, not fail. Faces PII — fixtures only, no real photos in repo.
- Success: 3 recipes green on `--demo`, gallery tile in democraft with contact-sheet.

## 6. Naming + CLI + MCP conventions (normative)

- Dir: `D:\Dev\repos\<name>craft` or `D:\Dev\repos\<name>-mcp` during migration, ONE name at ship. Binary: `<name>craft-cli.exe`. MCP key: `<name>craft`. Example: `virtucraft-cli.exe`, key `virtucraft`.
- Short wins: `virtucraft` not `virtualizationcraft`, `dbcraft` not `databasecraft` (alias; see §5 #2), `revecraft` not `reversingcraft`, `doccraft` not `libreofficecraft`, `containercraft` (no shorter unambiguous; `dockcraft` collides with Docker brand — avoid), `benchcraft` not `instrumentcraft`.
- CLI: `<cli> info|text|render|edit|combine|extract|split|check|audit|batch|tools|run|mcp|ui` subset as fits. `--help` must work. `mcp` subcommand: stdin/stdout, `--automation-read-root D:\Dev\repos --automation-write-root D:\Dev\repos` (ArtCraft) or `--allow-path D:\Dev\repos` (SolidCraft-style) or `--root DIR`.
- MCP: `type: local`, `command: [exe, mcp, ...roots]`, `enabled: true/false`, `timeout: 60000` (120000 for heavy: ghidra, capa, solid). See `opencode.json` 2026-11-02 for `pdfcraft/solidcraft/craft-anything/texturecraft/democraft/gamecraft` examples.
- Ports: backend+1 frontend pairs from `mcp-central-docs/operations/WEBAPP_PORTS.md` (10700-15000, never 3000/5000/5173/8000/8080). Claim via `fleet-gate/claim_ports.py` before allocating. democraft uses 11246/11245.

## 7. Democraft integration (required, not optional)

- Registry: `democraft-mcp/src/democraft_mcp/crafts.py` — add entry (exe, verbs, HERO, family, maker, capabilities). Family `core` for Storytold-owned, `community` for Tanganyika/others (SolidCraft precedent).
- Recipes: `src/democraft_mcp/recipes.py` — 3 per craft minimum, dispatched via `RECIPES[(app,demo)]` + `RunCtx.do_with`. Each writes `outbox/<app>/<demo>/run.json` + `*-report.md` with measured numbers (bytes, pages, ms, bbox, volume).
- Compat: `data/craft_compat.json` (gitignored) — bump baselines after `just ci` green on Oct 31 builds. Never commit baselines.
- Gallery: `webapp/src/lib/appMeta.ts` (hue/icon), `components/ContactSheet.tsx`, `components/ArtifactGrid.tsx`. `GET /api/gallery`, `GET /api/crafts`. Ctrl+K palette. Biome must parse Tailwind.
- Gates: `just ci` (ruff, pyright, pytest --cov-fail-under=55, biome). Screenshots: `node webapp/scripts/shots.mjs docs/screenshots` (Node, not Bun — Playwright hangs under Bun on Windows).

## 8. Phases + gates

- **Phase 0 (done 2026-11-02):** pdfcraft enabled, solidcraft verified, craft-anything + texturecraft + democraft + gamecraft wired in `opencode.json`. `len-120-territory.pdf` built via reportlab, verified via `pdfcraft-cli info` (2pp, A4). Restart opencode to load.
- **Phase 1 (pilot, done 2026-11-04):** virtucraft + dbcraft. 3 recipes each. `just ci` green. democraft gallery shows 2 new tiles. Decision gate: if no green recipes in 2 days per craft, cut scope (fewer verbs), not quality.
- **Phase 2 (Wave 1, done 2026-11-04):** revecraft, doccraft, filecraft, gitcraft (read-only recipes for git). 3 recipes each (12 new recipes total). All 4 crafts functional with CLI binaries and FastMCP stdio servers. Full test suite passing (113 passed, 57.80% coverage in `democraft-mcp`). All repos pushed to GitHub.
- **Phase 3 (Wave 2, 4-8 weeks):** containercraft (fuse 3), bookcraft (pick 1 impl), meshcraft (pick 1 host), benchcraft (fuse 6, sim-first).
  - Progress 2026-11-05: `bookcraft` L1/L2 shipped (v0.1.0) and registered in `democraft-mcp` as `book` with 4 green recipes; the `rust-calibre-mcp` cutover decision is still open.
- **Phase 4 (decommission):** old `-mcp` dirs become shims or archive to `_archives/` after 2 green releases. Never delete without `HANDOVER.md` + `fleet.lock.json` update + session-log entry (`mcp-central-docs/operations/session-log/YYYY-MM-DD.md`).

## 9. Risks + mitigations

- **Rename churn breaks fleet scripts/starts:** Mitigate with shims (`start.ps1` forwards), `fleet-start.config.ps1` kept, `WEBAPP_PORTS.md` single source.
- **Hypervisor/CUDA/host-app absent:** Recipes skip with `down`/`sim` receipt, never fake green. SearchStudio precedent: dead pipes reported, not silent zeros.
- **Creds in bench:** Never log tokens/URLs. Redact in `run.json`. No frida/exec in default `just ci`.
- **Goliath stale python.exe (HANDOVER 2026-11-02 notes hundreds):** Ram weeder scan before bench runs; do not kill prod NSSM children (use `sc.exe stop/start`, verify new PID owns port).
- **License/patent traps (LEN lesson):** Territory lists live in PDFs (50pp). Always extract via `pdfcraft-cli text --page N` (cleaner than pypdf), store CSV + PDF in `reports/`, ingest to AIWatcher (`inbox_add` with guid). Today's proof: `inbox:52a23df8...` + `len-120-territory.pdf`.

## 10. Open questions

1. `databasecraft/` dir vs `dbcraft` name — rename dir or alias binary? (Recommend: keep dir, ship `dbcraft-cli.exe`.)
2. `meshcraft` host pick: FreeCAD (STEP, headless-friendly) vs Blender (mesh, fragile)? Timebox spike 1 day.
3. `containercraft` vs keeping `docker-mcp` name for Docker Desktop users? (Recommend: craft name, keep `docker-mcp` as shim.)
4. Enable remaining 10 ArtCraft apps (cad/deck/effect/film/grid/light/photo/sound/vector/word) in `opencode.json`? Currently off to save startup. Enable on demand.
5. `craft-anything` project dir (`*.cany`) location? Default to `D:/Dev/repos/_sandbox_runs/` or per-craft `data/`? Decide before first `craft-anything chat` run.

## Appendix A. Current opencode.json craft map (2026-11-02)

on: designcraft, figcraft, pdfcraft, solidcraft, gamecraft, democraft, craft-anything, texturecraft
off (installed): cadcraft, deckcraft, effectcraft, filmcraft, gridcraft, lightcraft, photocraft, soundcraft, vectorcraft, wordcraft
bins verified: all 16 `*-cli.exe` in `C:\Program Files\*Craft` exist.

## Appendix B. Serve / Connect / MCP matrix (measured 2026-11-02 via `--help` + `commands`)

How to read: `run` = one shot, `serve`/`--connect`/`app --port` = many shots, one session, `mcp` = many shots, agent protocol. Democraft uses `run` + `mcp --demo` for CI (clean room per recipe), `serve`/`--connect` only for interactive/perf/watch.

| App | serve? | connect? | port? | mcp? | watch path |
|---|---|---|---|---|---|
| CADCraft | no | no | no | yes | `run` only (no session) |
| Craft Anything | no | no | no | yes | web/terminal output, `*.cany` project |
| DeckCraft | YES (`serve`) | no | no | yes | serve stdio/TCP for batch decks |
| DesignCraft | no (`app [--port]` + `mcp [--connect]` + `script [--connect]`) | YES (`--connect PORT`) | YES (`app --port`) | yes | `app --port` exposes control, `mcp --connect` bridges to open window |
| EffectCraft | no | no | no | yes | `run` only |
| FigCraft | YES (`serve` equiv — check `figcraft-cli --help` for `serve`) | no | no | yes | serve session for multi-select/edit loops |
| FilmCraft | no | no | no | yes | `run` only |
| GridCraft | no | YES (`--connect`?) | no | yes | bridge to open grid |
| LightCraft | YES (`snapshot`, `merge` are session-like; `serve` flag present in matrix) | YES (`--connect [ADDR]`, default 127.0.0.1:7980, `lightcraft --control 7980`) | no (control port, not serve) | yes (`--demo/--library/--connect/--compact`) | `snapshot -o OUT.png --size WxH` (CPU-rasterized headless UI), `render` single file, `mcp --demo` for agents |
| PdfCraft | no | no | no | yes (`--root/--compact`) | `render --page --dpi --out png`, `run --script --report` (one JSON doc) — stateless, no session needed |
| PhotoCraft | YES (`serve [--port] [--control-token]`) | no | YES (`--port`, `PHOTOCRAFT_CONTROL_PORT`, JSON-lines `{"id","method","params"}`) | yes | `serve` stdio or 127.0.0.1:PORT, token-gated; `run` for one-shots |
| SolidCraft | no (auto-bridge) | YES (implicit — next call bridges if app started) | no | yes | headless in-process, bridges to open app automatically |
| SoundCraft | YES | no | no | yes | serve session for render loops |
| TextureCraft | YES | no | YES | yes | serve + port for bake loops |
| VectorCraft | no | YES | no | yes | bridge to open doc |
| WordCraft | no | YES | YES (`app --port` equiv) | yes | bridge to open doc |

Measured via: `Get-ChildItem "C:\Program Files" *Craftcli --help | Select HasServe/HasConnect/HasPort/HasMcp` 2026-11-02 — CAD False/False/False/True, Deck True/False/False/True, Design False/True/True/True, Effect False/False/False/True, Fig True/False/False/True, Film False/False/False/True, Grid False/True/False/True, Light True/True/False/True, Pdf False/False/False/True, Photo True/False/False/True, Solid False/True/False/True, Sound True/False/False/True, Texture True/False/True/True, Vector False/True/False/True, Word False/True/True/True.

### Our crafts — do they have --serve? Should they?

- `gamecraft-cli` (ours, `D:\Dev\repos\gamecraft/target/debug/gamecraft-cli.exe`): NO serve, NO mcp (mcp is separate `gamecraft-mcp.exe` stdio). Verbs: `lint/query/uid/forge/new/list/report/verify/gltf/commands/describe/run/export`. `verify` = headless self-play (web) / headless boot to win marker (Godot). To WATCH: use `gamecraft-desktop.exe` (window) or web three.js player + `report` (gate record, cheat sheet) + `export` glTF. SHOULD it have serve? YES — want `gamecraft-cli serve --port 9000` keeping one Bevy/Godot headless session open, streaming `verify` ticks + `snapshot --out png` per 500ms for democraft gallery. Currently each `verify` cold-boots. File as `gamecraft#serve` issue.
- `democraft-mcp` (ours, Python FastMCP, `python -m democraft_mcp`): NO serve (MCP stdio + FastAPI 11246 + Vite 11245). To WATCH: `GET /api/gallery`, `GET /api/crafts`, `outbox/<app>/<demo>/run.json + *-report.md + contact-sheet`, Ctrl+K palette. Webapp IS the serve. SHOULD it have CLI serve? No — add `democraft watch --port 11245` = static file watcher on `outbox/` + live-reload gallery (tiny, no engine). Don't duplicate Craft Anything `serve`.
- `databasecraft-cli` (ours, Rust, `target/debug/databasecraft-cli.exe`): NO serve. Verbs: `status/query/schema-inspect/record-insert/export-merge/seed-demo/embed/semantic-search/commands/describe/mcp`. `mcp` = stdio Plane1 headless or Plane2 `--attach` (that's its serve equiv — attach to live DB). SHOULD it have serve? NO for queries (stateless, <10ms). YES only as `--watch` for `seed-demo` progress + `status` control port (already reports “registered control port” in `status` — surface it).
- `virtucraft` (proposed): YES, needs `serve --port` from day 1. `vm start` + `snapshot` + `sandbox run` are long-lived; gallery wants `shot --out png` polling. Spec in `virtucraft-DOSSIER.md` §3-§4: `serve` keeps one VBox/Hyper-V session open, `run --script` for recipes.
- `albumcraft` (proposed): NO serve (LightCraft `--demo` + sim Immich are one-shots). Watch via `export sheet --out jpg` + democraft gallery, same as democraft. Add `watch` only if `ingest --dir` gets slow (poll `activity.list`).

Rule: serve when session startup >200ms or you need screenshots mid-run (games, VM boot, photo merge). Otherwise `run --script --report` + gallery is enough. Ours: gamecraft YES (watch play), virtucraft YES (watch boot), democraft NO (gallery IS watch), dbcraft NO (queries are instant).

See §5 per-craft verbs. Full `tool_search` output per CLI via `<cli> tools` (pdfcraft precedent: `pdfcraft-cli tools`). Paste into `docs/TOOLS.md` per repo (fleet standard).

## Appendix C. What NOT to craft (with reasons)

- plex-mcp → keep bridge (server state, §3.2)
- immich-mcp / photoprism-mcp → keep bridges (server state, §4)
- email-mcp, discord-mcp → bridges (OAuth, polling, webhooks)
- aiwatcher-mcp, searchstudio-mcp, fleetwatcher-mcp → observers/pipelines
- speech-mcp, alexa-mcp, yahboom-mcp → voice bus members (see `VOICE_COMMAND_BUS.md`, ingress via `fleet-agent-mcp POST /api/voice/intent`)
- unsloth-mcp, triton-mcp → Bucket D (CUDA)

---

*Generated 2026-11-02 from live `D:\Dev\repos` listing (339 entries), `C:\Program Files` craft inventory (16 CLIs), `democraft-mcp` HANDOVER v0.3.0, `opencode.json` (1309 lines). Next: restart opencode, run `just ci` in democraft-mcp, scaffold virtucraft dossier.*
