# Demo Capture — fleet screenshot + video tool

Generates promotional materials for any fleet webapp: full-page screenshots, a Playwright-powered video walkthrough, and (via **meta_mcp**) an optional Remotion MP4 with title overlay.

## MCP orchestration (recommended)

Use **meta_mcp** `demo_ops` for the full pipeline — start stack, record, render:

```python
# Plan → record → Remotion MP4 in one call
await demo_ops(operation="record", app_id="inkscape-mcp", render_mp4=True)
```

Detailed reference: **[meta_mcp/docs/tools/demo-capture.md](../../../meta_mcp/docs/tools/demo-capture.md)**

| Operation | What it does |
|-----------|--------------|
| `plan` | Scan routes + `data-testid` → `config.json` |
| `record` | Start/reuse webapp, Playwright → PNG + `.webm` |
| `render` | Remotion → `docs/screenshots/{repo}-demo.mp4` |
| `health` | Wait for manifest ports ready |

Templates are bundled in `meta_mcp/src/meta_mcp/demo_capture_templates/` (Playwright + Remotion).

---

## Manual / standalone usage

### Files in this template

```text
templates/demo-capture/
├── README.md                 ← this file
├── demo-screenshots.ts       ← Playwright screenshot spec (copy to webapp/e2e/)
├── demo-video.ts             ← Playwright video walkthrough spec
└── config.json               ← example per-repo config (ports, pages, nav items)
```

Remotion templates live in `meta_mcp/.../demo_capture_templates/remotion/` and are materialized to `{repo}/scripts/screencast/` on first render.

### Copy and run (Playwright only)

```powershell
# 1. Copy templates to your webapp
Copy-Item templates/demo-capture/demo-screenshots.ts webapp/e2e/
Copy-Item templates/demo-capture/demo-video.ts webapp/e2e/

# 2. Edit config.json with your ports and page list

# 3. Run (from webapp/e2e after copying playwright.demo.config.ts from meta_mcp template)
npx playwright test demo-screenshots.ts demo-video.ts --config playwright.demo.config.ts

# 4. Output in docs/screenshots/
```

Or use meta_mcp `demo_ops(operation="record", ...)` — no manual copy required.

---

## How it works

Playwright's `video: "on"` config uses Chromium's built-in screencast API to record a `.webm` video of all page interactions — no OBS, no ShareX, no screen recording permissions. The tracing API also captures a full interaction trace (`trace.zip`) for debugging.

The screenshot spec navigates to each page, waits for content, and saves full-page PNGs.

**Remotion layer (optional):** Playwright `.webm` is copied to `scripts/screencast/public/source.webm`, then Remotion renders an MP4 with a title card overlay. See meta_mcp demo-capture doc for details.

---

## Per-repo config

```json
{
  "backend_port": 11028,
  "frontend_port": 11029,
  "health_path": "/api/health",
  "pages": [
    { "route": "/", "selector": "[data-testid='dashboard']", "name": "Dashboard" },
    { "route": "/animation", "selector": "text=Animation Studio", "name": "Animation Studio" }
  ],
  "video_steps": [
    { "action": "goto", "url": "/" },
    { "action": "wait", "ms": 2000 },
    { "action": "goto", "url": "/settings" },
    { "action": "wait", "ms": 1000 }
  ]
}
```

Supported step actions: `goto`, `wait`, `wait_selector`, `click`, `fill`.

---

## Output artifacts

| Artifact | Location |
|----------|----------|
| PNG screenshots | `docs/screenshots/*.png` |
| Playwright video | `web_sota/e2e/demo-test-results/**/*.webm` |
| Playwright trace | `docs/screenshots/demo-trace.zip` |
| Remotion MP4 | `docs/screenshots/{repo}-demo.mp4` |

---

## Prerequisites

- Node.js 18+ (`npx` on PATH)
- `npx playwright install chromium` (once per machine)
- Fleet webapp with `start.ps1` and manifest entry (for MCP orchestration)
- Recommended: `data-testid` on key pages for stable selectors
