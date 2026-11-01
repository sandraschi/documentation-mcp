# 01 - ArtCraft / Ars Analysis: What Actually Happened

> ERRATUM 2026-10-11: core artcraft relicensed Fair Source -> MIT OR Apache-2.0 on
> 2026-10-10 (PR #2043). Fair Source statements below are historical. See 13.

Date: 2026-10-08. Sources: getartcraft.com/apps, storytold/artcraft README/ROADMAP/LICENSE/dev_setup, GitHub releases/issues, Ars Technica 2026-10-07 by Kyle Orland, Reddit r/SaaS 1wwnhbt, HN 49934228 / 49958850 / 49959605 / 49960138.

## Timeline

- 2025: ArtCraft starts as "controllable AI for artists". Tauri + Rust + React/TS/Nx/Vite. SQLite + SQLx migrations. Compose in 2D, stage in 3D, then generate. 62-model catalog.
- 2026-01 to 2026-09: 20 releases (v0.5.0 to v0.41.0 on 2026-09-26). 7304 stars, 983 forks. Rapid velocity.
- 2026-02 onward: founder Brandon Thomas (LinkedIn possibilistic, decade Rust) codes exclusively with AI tools, settles on Claude Opus 5.5.
- 2026-10-04 weekend: pivot goes live at getartcraft.com/apps. Seven apps, all Pure Rust, native macOS/Windows/Linux installers + WASM web (FilmCraft has no web build yet).
- 2026-10-07: Reddit announce "open source 100 percent Rust cleanroom", HN + Bluesky pile-on about bugs, Ars publishes.
- 2026-10-08: issue tracker at #2005, roughly 20 new issues per day. MSI silent-crash, signup failure, canvas flicker, PSD vectors, AEP/HEIC requests, MCP-server proposal #2003.

## The seven crafts

| Craft | Adobe target | Status on site | Notes |
|---|---|---|---|
| PhotoCraft | Photoshop | Early alpha, installers ready, Mac/Win/Linux/Web | Hero shows Great Wave + Curves + type layers. Closest to "one-shotted Photoshop" claim. |
| VectorCraft | Illustrator | In development, installers ready | Neon Drive poster, Appearance panel, outer glow. |
| FilmCraft | Premiere | In development, no web | Charade 1963 timeline, scopes, program monitor. Screenshot mimics Premiere closely - trade dress risk. |
| LightCraft | Lightroom | In development | Ansel Adams Tetons, sliders. Photo library + RAW developer, local files. |
| PdfCraft | Acrobat Pro | Early alpha | Cover + All tools panel + threaded comments. Read/organize/combine/split/secure. |
| EffectCraft | After Effects | In development | Animated title comp, project panel, text/shape/solid layers. |
| DesignCraft | InDesign | In development | Magazine spread, threaded 3-column story, pull quote, text frame options. |

Shared principles (from site): Open source / Native not wrapped (no Electron, no webviews) / Familiar from day one (Adobe layouts, tools, shortcuts) / Your files your machine (no cloud round-trip) / Agent-ready (CLI + JSON control channel + MCP server) / Also in browser (WASM except FilmCraft).

## Tech behind core ArtCraft (the money engine)

- Rust 9.3 MB + TypeScript 6.5 MB. Tauri 2.10, Node v24.13.0, Nx + Vite locally, no global Nx.
- Custom unix_dev.sh launcher: binds 127.0.0.1:5193, scans upward for free port, passes exact devUrl to Tauri in memory, normalizes loopback origins for auth/media. node --test harness with fake Cargo tree. Best Tauri dev-loop pattern seen this year.
- Model catalog (62): Images 16 (Nano Banana 1/2/Pro, GPT Image 1.5/2/2.5 Flare/Sunburst, FLUX.1 dev/schnell/1.1 pro/ultra, Seedream 4/4.5/5), Video 25 (Seedance, Kling, Veo, Sora, Vidu, MiniMax H3, Flux 3), Sound 5 (Suno x4, Seed Audio), 3D meshes 11 (Hunyuan 3D 2.0/2.1/3/3.1, Tripo H3.1, Meshy 6, Rodin 2.5), Worlds 5 (Marble, TripoSplat). Providers: ArtCraft hosted + Grok + Midjourney + Sora + World Labs. Planned: Kling, Google, Runway, Luma, OpenArt, Freepik.
- Crafting ops (differentiator): Image-to-Location, 3D compositing, 2D compositing + bg removal, Image-to-3D-mesh, Character Posing, Kitbash blocking, Identity Transfer, Mixed-asset scenes. Prompting ops (table stakes): T2I, prompted edit, canvas/mask inpaint, I2V.
- Backend services live in separate closed artcraft-services repo. Desktop task DB in _database/sql/artcraft_migrations + .sqlx cache. SQLX_OFFLINE=true for check.
- Roadmap 2026: beat aggregators, tangible clay-like surfaces, every model, purpose-built relight/repose models, content studio + AI feature film, festivals, remove hosted dependence, more Rust, tests/CI. Loftier: Open OpenAI/Google/Anthropic, open models/platforms/hardware, Dont Be Evil.

## Funding and license split - critical

- Core artcraft repo LICENSE.md: Fair Source (WIP, not OSI). Free to use/copy/modify for private personal use, outputs yours. Cannot sell software, cannot use code for competing business, cannot strip community/donation/paid links, cannot use brand. Promise: no rug pull, transition to OSI if business ends. Inspiration: Fair Source, Fair Code, Defold, Obsidian. Reason given: OSI makes hyperscaler cherry-picking too easy, Stability.ai died with no money, training future models needs capital.
- New 7 crafts: Ars quotes Thomas saying MIT/Apache, site says "Every line is on GitHub under permissive licenses. Read it, fork it, build on it." Revenue per Reddit pe799hc: token-based access to pre-existing ArtCraft visual AI model + IDE bundled inside apps alongside third-party models. Team building popular filmmaker software funds the rest. Motive per HN: Adobe cancellation-fee dark pattern.
- Action: treat as TWO regimes until verified per repo. Core = do not copy into competing product. Crafts = verify LICENSE file exists and is really MIT/Apache before reuse.

## Claims vs reality

- "One-shotted Photoshop. The whole thing." / "Software is over." / "100 percent parity within a month" (Reddit) amended to "99 percent will take a while, measured in months not years" (HN 49961661). "Now you can just create 1:1 functional equivalents, clean room, highly performant and cross-platform. Nothing is stopping you. Replace Search, build smartphones, remove ads, de-enshittify tech."
- Commenters (HN 49960138, Bluesky chinnyvision, whatabouttheken) list real gaps: PSD vectors, feather/density parity, AEP/HEIC/Pixelmator, .ecproj suffix, motion blur codecs, font collapse, copy/paste, localStorage mount failure, flicker, website scroll.
- Ars deck is correct: ambitious, free, nowhere near finished. Super early alpha per Thomas himself (HN 49959605).
- Why bug-counting is myopic: scaffolding is now instant with Opus, discovery parallelizes to users (2000 issues = free specs), fixing parallelizes to agents, fixes compound across shared Rust core + WASM + agent contract. Judge by 90-day burn-down slope, not day-3 screenshots. 80 percent + free + local + scriptable beats 99 percent for everyone except finishing houses.

## Legal

- Functional clean-room reverse engineering is generally legal (EFF FAQ, N64 precedent, Ars 2020 beyond-emulation piece).
- Trade dress is the risk (Ars cites 2012 Tetris clone test). FilmCraft mimicking Premiere layout/fonts/colors closely could draw Adobe letter even if code is clean. Mitigation: diverge chrome, names, icons, keep behavior parity.
- Do not copy Adobe UI pixel-for-pixel in fleet work. Document behavior, reimplement with fleet SOTA styling (Slate-950/Zinc-950, Lucide, no light theme per WEBAPP_SOTA_STANDARDS).

## What to watch next

- Per-repo LICENSE verification for all 7 crafts.
- FilmCraft web build absence - why (performance, codecs, or legal).
- Issue burn-down rate + MSI/auth fixes (#1990, #2004, #1984, #1983).
- MCP-server proposal #2003 - if he ships CLI/JSON/MCP uniformly, his mesh thesis is real.
- Any Adobe contact, plus rename/restyle commits that signal trade-dress caution.
