# Webapp Screenshot Content Standard (v2)

**Status:** DRAFT — proposed amendment to `README_WEBAPP_SCREENSHOTS.md`
**Date:** 2026-07-29
**Trigger:** ai-games-collection screenshots show page headers instead of game boards; chitchat shows welcome hero + topbar

## Problem

The existing screenshot standard (`README_WEBAPP_SCREENSHOTS.md`) specifies *where* to capture (dashboard, feature page) and *how* (1280px, PNG, Playwright). It does not specify *what must be visible*. The result across the fleet:

| Repo | What the screenshot shows | What it should show |
|------|--------------------------|---------------------|
| ai-games-collection | Topbar + "Select a game" page header | A rendered Go/chess/othello board with pieces |
| chitchat | Welcome hero + "Hey! Ready for a chitchat?" | The Topics tab with category pills + full topic list |
| Most dashboards | Skeleton: topbar, sidebar, hero text, zero KPIs | KPIs populated, backend connected, actual tool count |

The root cause: Playwright captures the page at its **empty default state**. No data has been loaded, no interaction has occurred. The screenshot captures a shell, not the product.

## The rule

> Every README screenshot MUST show the webapp in a **populated state** — real data, real content, real result. A screenshot of an empty dashboard, unstyled skeleton, or "nothing here yet" placeholder is a **self-own** and fails review.

## Per-page capture requirements

| Page type | Must show | Never show |
|-----------|-----------|------------|
| **Dashboard** | KPIs with real numbers, **backend status green** (not red/offline/probing), at least one populated stat card | Empty hero with "Welcome to X" only; error states ("500 error", "invalid JSON", "Failed to fetch", red badge); offline indicator |
| **Content page** (topics, books, media, archive) | A populated list/grid with real items, not the empty state | "Nothing here yet," zero results |
| **Tool/demo page** | An actual tool result: rendered board, exported file list, pipeline output | Parameter form with no execution |
| **Chat** | A conversation with messages, not the blank input | Empty chat with "send a message" |
| **Settings** | Detected providers, model selected | "No LLM detected" on most repos |

## How to achieve populated state

### Option 0: Wait for backend connectivity (MANDATORY, always)

Before any screenshot, wait for the backend to be reachable and the dashboard status indicator to go green. A screenshot showing "500 error," "Offline," or a red badge is **worse than no screenshot** — it advertises failure.

```typescript
// Wait for backend health + green status badge in the UI
await page.waitForResponse(r => r.url().includes('/api/health') && r.status() === 200, { timeout: 60000 });
await page.waitForSelector('[data-testid="backend-dot"].bg-green-500, [data-testid="backend-dot"][class*="green"]', { timeout: 30000 });
// Poll if the app uses exponential backoff (1s, 2s, 4s, 8s, 16s = up to 31s)
await page.waitForTimeout(5000);  // let KPIs populate
```

Every fleet webapp MUST have `data-testid="backend-dot"` on its connection indicator per `tauri_nsis_building.md`. The green class varies (`bg-green-500`, `text-green-500`, `[class*="green"]`), so match broadly.

After the backend-health gate passes, do a final sanity check — if the page text contains any error keyword, **fail the script**:

```typescript
const body = await page.textContent('body');
const poison = ['500 error', 'invalid JSON', 'Failed to fetch', 'Internal Server Error', 'Connection refused'];
if (poison.some(p => body?.includes(p))) {
  throw new Error(`Screenshot aborted: page contains error text`);
}
```

If the backend never comes up or the page shows an error, **fail the screenshot script** — do not capture a broken page.

### Option A: Seed data before capture (preferred)

The Playwright capture script inserts test data via the app's own API before taking the screenshot:

```typescript
// BEFORE screenshot — seed content
await page.request.post(`${API}/api/archive`, {
  data: { topic: "Best coffee in Vienna?", response: "Kaffee Alt Wien, no contest.", tags: ["vienna"] }
});
// ...seed 3-4 entries...

// NOW take the screenshot
await page.goto('/app/archive');
await page.waitForSelector('[data-testid="archive-list"]');
await page.screenshot({ path: '../docs/screenshots/archive.png' });
```

### Option B: Navigate to a deep-linked state

Some pages have content by default (e.g., `/app/games/go` shows a board immediately). Capture those routes, not the landing page.

### Option C: Demo mode endpoint

Add a backend endpoint `POST /api/demo/seed` that pre-loads the database with showcase data. The Playwright script calls it before capture, then resets after. This gives reproducible, good-looking screenshots without polluting real user data.

### Anti-example: ai-games-collection

The current Playwright spec navigates to `/` (game selection page) and captures the header. Fix: seed a game, navigate to `/game/{id}`, capture the rendered board.

## Update to standard

Amend `README_WEBAPP_SCREENSHOTS.md` §"What to show":

1. Add a **Content gate** rule before the Hero section: "Every screenshot MUST show populated state."
2. Add the per-page requirements table above.
3. Add §"How to achieve populated state" with the three options.
4. Update the Playwright capture example to include API seeding before `page.screenshot()`.
5. Add to the checklist: `[ ] Screenshot shows populated data, not empty shell`

## Video (future)

Same standard applies to demo videos: don't record 30 seconds of clicking through empty pages. Seed content first, then walk through the populated experience. The `meta_mcp demo_ops` pipeline already supports `video_steps` — these should include seed interactions.

## Fleet audit (quick scan)

| Repo | Screenshots exist? | Shows content or shell? |
|------|-------------------|------------------------|
| ai-games-collection | Yes (Phase 2) | Shell — game selection page, no board renders |
| chitchat | No | Would show welcome hero only |
| kicad-mcp | No | — |
| blender-mcp | No | — |

Full audit deferred to `FLEET_WEBAPP_README_SCREENSHOTS_SWEEP.md`.
