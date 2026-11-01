# 02 - What We Can Copy (Patterns, Not Code)

> ERRATUM 2026-10-11: core artcraft relicensed Fair Source -> MIT OR Apache-2.0 on
> 2026-10-10 (PR #2043). Fair Source statements below are historical. See 13.

Rule: inspire clean-room, never paste. Core artcraft = Fair Source clause 2 forbids
competing use. New crafts = claimed MIT/Apache, verify per repo first.

## A. Copyable architecture patterns

1. Free-port Tauri launcher (highest value).
   What: bind 127.0.0.1:5193, scan upward until free, pass exact devUrl to Tauri
   in memory without mutating checked-in config, normalize loopback origins for
   auth/media, never kill by port/name, propagate exit codes, node --test harness
   with real Vite listeners + fake Cargo tree covering occupied ports, simultaneous
   launches, React edits, shutdown, Rust watcher failure.
   Fleet action: lift into START_SCRIPT_STANDARD + TAURI_PRODUCTION_PITFALLS Phase 1.
   Fixes our repeated port-squat bugs (claim_ports.py checks both WEBAPP_PORTS.md
   and fleet-start.config.ps1 for same reason).

2. Model catalog router.
   What: Provider -> Family -> Model table with enabled/disabled/restricted flags
   (his dagger/double-dagger convention). 62 models across image/video/sound/3D/worlds.
   Paid ArtCraft hosted sits alongside BYO third-party + local.
   Fleet action: add to comfyops-mcp as `comfy_catalog` op. Local-first (FLUX.2 klein 4B,
   SD1.5 verified, Wan 2.2 LocalGen) with cloud-optional (Veo/Omni, Pexels/Pixabay/Coverr,
   Mixkit/NASA no-key). Same seed + same workflow = identical output stays mandatory.

3. Crafting pipeline vocabulary.
   What: named ops, not free prompt: image-to-location, 2D-composite, 3D-composite,
   image-to-mesh, pose, kitbash-block, identity-transfer, bg-remove, mixed-asset,
   canvas-mask-inpaint, prompted-edit, image-to-video.
   Fleet action: implement as crossconnect chain (see 03), not monolith. Keep names
   stable so Opus can plan over them.

4. SQLite task DB + SQLx pattern.
   What: _database/sql/artcraft_migrations + .sqlx cache, SQLX_OFFLINE=true check,
   Rust watcher rebuild-and-restart (state loss explicit), Vite HMR/Fast Refresh
   for frontend only.
   Fleet action: canonical for any Rust work; document restart-vs-reload semantics
   in DEVELOPMENT.md every time.

5. Desktop session regression doc.
   What: explicit checklist for ports/launcher/auth when changing any of the three.
   Fleet action: create docs/desktop-session-regression.md in every Tauri repo.
   Covers his live bugs (#1990 MSI silent exit, #2004 signup, #1984 localStorage mount,
   #1983 flicker) before they ship.

6. Agent-ready contract from day one.
   What: every Craft promises CLI + JSON control channel + MCP server + WASM web.
   Fleet action: already our portmanteau + Prefab + sampling pattern. Make it uniform:
   `help, status, mission` on every server, skill:// resources, prompts for plans
   (edit_plan, color_recipe, render_checklist pattern from davinci-resolve-mcp).

7. Rust + WASM dual target.
   What: pure Rust core compiled to desktop + browser. No Electron, no webviews.
   Fleet action: do not rewrite Python fleet in Rust. Instead: keep Python MCP servers
   as agent bridge, add thin Rust core only where hot (canvas, scopes, codecs).
   Pair with Tauri NSIS pitfalls checklist A-J before any installer build + BUILD_LOG.md.

## B. What NOT to copy

- Hosted auth/media/login + token subsidy. His roadmap admits removing hosted dependence
  is unfinished. Copying the phone-home creates single point of failure + bill risk.
- Pixel-identical Adobe chrome. Copy behavior + shortcuts + file round-trip, restyle
  with fleet SOTA (dark Slate/Zinc, Lucide, Radix, Zustand). Avoids Tetris trade-dress trap.
- 62-model sprawl on day one. Many entries already disabled (†/‡). Start with 5 verified
  local + 3 free-stock, expand behind flags.
- "100 percent in a month" messaging. Promise burn-down slope + regression suite, not date.

## C. Clean-room procedure for Opus (to stay legal)

1. Black-box only: observe running Adobe app via screenshots + UIA tree + files + docs.
   Never decompile, never paste Adobe or Fair-Source code.
2. Spec first: SPEC.md per dialog/panel with inputs, outputs, shortcuts, file effects.
3. Reimplement from spec in Rust/Python fresh. Log sources (doc URL, video timestamp,
   screenshot hash) not code origins.
4. Prove with two diffs: visual diff (screenshot before/after) + file diff (PSD/SVG/PDF
   round-trip byte or parsed comparison).
5. Diverge trade dress: different names, icons, spacing, theme. Keep shortcuts familiar
   where functional (Ctrl+Z) but not logo/fonts/layout copy.
6. Keep LICENSE hygiene: .gitignore before first add, .mcpbignore with wipe+recopy
   src -> mcpb/src before pack, prompts 3-4-100 rule per MCPB_PACKAGING_STANDARDS.

## D. Quick win list (copy this week)

- [ ] Port free-port launcher idea into one fleet Tauri repo as pilot, with node --test.
- [ ] Add desktop-session-regression.md to blender-mcp + videogen-mcp.
- [ ] Draft comfy_catalog table (5 local + 3 stock) behind flags.
- [ ] Add uniform `mission` + `snapshot` ops naming across gimp/blender/davinci/pywinauto.
- [ ] Verify all 7 Craft repo LICENSE files, record in 06-plans-roadmap appendix.
