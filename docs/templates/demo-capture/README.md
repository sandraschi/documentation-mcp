# Demo Capture — fleet screenshot + video tool

Generates promotional materials for any fleet webapp: full-page screenshots and a Playwright-powered video walkthrough. No external recording software needed.

## Files

```
templates/demo-capture/
├── README.md            ← this file
├── demo-screenshots.ts   ← Playwright screenshot spec (copy to webapp/e2e/)
├── demo-video.ts         ← Playwright video walkthrough spec
├── capture.ps1           ← runner script (adapt per repo)
└── config.json           ← per-repo config (ports, pages, nav items)
```

## Usage

```powershell
# 1. Copy templates to your webapp
cp templates/demo-capture/demo-screenshots.ts webapp/e2e/
cp templates/demo-capture/demo-video.ts webapp/e2e/

# 2. Edit config.json with your ports and page list

# 3. Run
pwsh templates/demo-capture/capture.ps1 -Screenshots -Video

# 4. Output in docs/screenshots/
```

## How it works

Playwright's `video: "on"` config uses Chromium's built-in screencast API to record a `.webm` video of all page interactions — no OBS, no ShareX, no screen recording permissions. The tracing API also captures a full interaction trace (`trace.zip`) for debugging.

The screenshot spec navigates to each page, waits for content, and saves full-page PNGs.

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
