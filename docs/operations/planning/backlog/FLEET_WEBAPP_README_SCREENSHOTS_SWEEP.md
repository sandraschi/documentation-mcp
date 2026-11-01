# Fleet webapp README screenshots sweep

**Priority:** P2  
**Standard:** `standards/playwright_e2e_sota.md` §3

## Problem

Fleet webapp READMEs describe UI but rarely show it. One 1280×720 screenshot beats 50 lines of prose — especially wrapper MCPs (Blender, GIMP, KiCad).

## Per webapp

- `webapp/e2e/screenshots.spec.ts` — dashboard KPIs, full-page PNG
- Output: `docs/screenshots/dashboard.png`
- README: `![Dashboard](docs/screenshots/dashboard.png)`
- Viewport 1280×720, dark theme, `data-testid` anchors

## Screenshot set

| Capture | Notes |
|---------|-------|
| Dashboard | Sidebar collapsed; stitch if tall |
| Sidebar | Expanded, standalone PNG |
| Tool/Lab pages | Every page that shows what the app *does* |
| Skip | Logs, Settings, Help, About |

~15 min per webapp. Screencast/video pipeline is separate — see [meta_mcp demo capture](../../meta_mcp/docs/tools/demo-capture.md).
