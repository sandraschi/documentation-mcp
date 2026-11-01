# 04 - Other Windows App Targets Wide Open to the Same Reversal

Thesis: any Windows desktop app with visible UI/UX, local files, and public docs
is reversible by AI crawling screens + menus + configs + workflows + docs.
No Ghidra needed. SaaS hides logic server-side. Win32/Qt/Electron exposes it.

Ranked by value x feasibility x fleet leverage. All should use black-box clean-room
method from 02-C.

## Tier 1 - same shape as Adobe, immediate

1. Microsoft Office (Word/Excel/PowerPoint) -> LibreOffice is partial, but AI-rebuilt
   lightweight native Rust suite with OOXML round-trip + MCP control would obsolete
   rental for 80 percent. Fleet holder: libreoffice-mcp + pdf-mcp + onenote-mcp +
   ms-graph-mcp. Crawl: ribbon tabs, styles, track changes, pivot tables, master slides.
   Files: .docx/.xlsx/.pptx are ZIP XML - perfect diff target.
2. AutoCAD / SolidWorks -> freecad-mcp + qcad-mcp + codecad-mcp + blender-mcp already
   bridge DXF/STEP/GLB. Crawl: draw/modify/dimension, constraints, layouts, sheet sets.
  DWG is the moat, same as PSD. Start with DXF-SVG exchange + 2D-to-3D-scene.
3. Ableton / FL Studio / Pro Tools -> reaper-mcp + audiotool-nexus + stems + mixx/virtualdj
   + songgeneration/suno + kyutai-mcp. Crawl: piano roll, mixer, warp, stems, export.
   Audio is highly scriptable, low trade-dress risk (knobs are generic).
4. OBS + Streamlabs -> obs-mcp + streamfog-mcp + демократи. Crawl: scenes/sources,
   filters, transitions, replay buffer. Already agent-driven in fleet. Smallest lift.

## Tier 2 - high value, medium lift

5. Notion / Obsidian / Evernote -> obsidian-mcp + notion-mcp + quicknotes-mcp.
   Local-first Markdown + canvas + sync. Crawl: blocks, backlinks, embeds.
6. Lightroom already covered, but Capture One / DxO same pattern via immich-mcp +
   darktable bridge (new). RAW profiles are the long tail.
7. DaVinci vs Premiere is already Tier 1 in 03, but Vegas / Edius / Camtasia are
   easier small targets for ittybitty-style assemble/concat + karaoke subs + beat snap.
8. Blender addons panel itself: Substance Painter / Quixel / ZBrush mini-tools.
   Crawl brush/layer/material UI, reimplement as blender-mcp ops + webapp tabs.

## Tier 3 - wide net (pick one vertical, do not boil ocean)

- Accounting: QuickBooks / DATEV -> local SQLite ledger + PDF invoices + MCP.
  Highly regulated, avoid unless vertical sponsor appears.
- CAD/CAM/PCB: KiCad (kicad-mcp exists), Eagle, Altium. Crawl: schematic -> footprint ->
  Gerber. Fleet has jtag-swd, logic-analyzer, multimeter, power-supply, oscilloscope,
  sdr, triton - hardware bench already meshes.
- Video security: Milestone / dedicated NVR UIs -> bench-camera + lidar + open-drone.
- Ebook/reader: Calibre (calibre-mcp is strong) vs Kindle app. Low legal risk.
- Browsers-as-apps: Chrome/Firefox dialogs -> browser-mcp (Playwright) already covers.

## How to rank a new target (scorecard for Opus)

- Visible? 100 percent of features reachable via UIA + screenshots (pywinauto probe week).
- Files? Open or reverse-documented format on disk for diff testing (ZIP XML, JSON, SQLite best).
- Docs? Manuals + tutorials + forums ingestible for spec mining.
- Fleet holder? Existing wrappee MCP to bridge while rewriting (1-hop rule).
- Legal? Functional clone OK, trade dress must diverge. Fonts/logos/names replaced.
- Paid pain? Cancellation fee / rental / ads / de-enshittify angle for distribution.
- If score 5/6, add to 06 roadmap Phase 4 backlog. Max 1 new vertical per quarter.

## Explicit non-targets

- Cloud-gated SaaS with server-side inference (Figma multiplayer, Google Search).
  Crawl sees only thin client. Different game.
- Kernel DRM / games anti-cheat. Legal + technical trap. Do not touch.
- Anything requiring pasted Fair-Source or proprietary code. Reimplement, do not lift.
