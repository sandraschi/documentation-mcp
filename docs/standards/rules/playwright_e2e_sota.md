# Playwright E2E Testing Standard (SOTA 2026)

Every fleet repo with a webapp MUST include Playwright end-to-end tests.

## Rationale

Backend unit tests verify that MCP tools return correct data. Playwright
tests verify that the actual React UI renders, navigates, and integrates
with the backend correctly. Without e2e tests, regressions in the frontend
go undetected until someone clicks through manually.

> **CUA-NSIS tests** (pywinauto) catch what Playwright cannot: NSIS install
> failures, backend unreachable, CSP/CORS config, timing races, and registry
> cleanup. See [CUA-NSIS Smoke Testing](cua_nsis_smoke_testing.md).
> **Both are required.** Playwright for dev loop; CUA for pre-release certification.

## Requirements

### 1. Install & Config

```bash
cd webapp/
npm install --save-dev @playwright/test
npx playwright install chromium
```

Create `webapp/playwright.config.ts`:

```ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
    testDir: './e2e',
    timeout: 60000,
    retries: 1,
    use: {
        baseURL: 'http://localhost:PORT',   // YOUR frontend port
        headless: true,
        screenshot: 'only-on-failure',
    },
    webServer: {
        command: 'uv run uvicorn YOUR_PACKAGE.server:app --host 127.0.0.1 --port BACKEND_PORT --log-level warning',
        port: BACKEND_PORT,
        cwd: '../',
        timeout: 30000,
        reuseExistingServer: false,
    },
});
```

### 2. Test Structure

Tests go in `webapp/e2e/*.spec.ts`. Two describe blocks:

- **Frontend** — page load, navigation, UI interactions via `{ page }`
- **REST API** — backend endpoints via `{ request }`

### 3. Screenshot Capture for README (developing)

Optional but **recommended** for wrapper MCPs (Blender, GIMP, KiCad, …):

- Add `webapp/e2e/screenshots.spec.ts` — stable viewport 1280×720, `data-testid` anchors
- Output to `docs/screenshots/*.png`
- Recipe: `just screenshots`

Full standard: [README_WEBAPP_SCREENSHOTS.md](../README_WEBAPP_SCREENSHOTS.md).

### 4. What Every Webapp MUST Test

| Test | What it catches |
|------|----------------|
| Dashboard loads with KPIs | React render, API fetch |
| Each page loads | Routing, component mount |
| Navigation sidebar works | Router links, all routes |
| Topbar health check | Backend connectivity |
| Compose / input forms | Conditional rendering, form state |
| Settings page | Provider discovery API |
| Help page tabs | Tab component rendering |
| REST: GET /api/status | Server alive |
| REST: POST invalid input → 422 | Validation |

### 5. Minimum Test Suite

Every fleet repo with a webapp MUST have Playwright E2E tests that validate:

- Backend health endpoint returns 200
- Frontend SPA loads (page does not crash)
- No console errors (zero tolerance — enforced by `../scripts/playwright-audit.ps1`)
- No 404s on page navigation
- No hydration failures

The minimal acceptable test suite is:
```typescript
import { test, expect } from '@playwright/test';
test.describe('Fleet Audit', () => {
    test('Backend health', async ({ request }) => {
        const resp = await request.get(BE + '/health');
        expect(resp.status()).toBe(200);
    });
    test('Frontend loads', async ({ page }) => {
        await page.goto(FE, { timeout: 15000 });
        await page.waitForTimeout(3000);
        await expect(page.locator('#root')).toBeAttached();
    });
});
```

Where BE and FE are set to the repo's backend/frontend ports.

### 6. CI Integration

Add to `.github/workflows/ci.yml`:

```yaml
- name: Install & test
  run: |
    cd webapp
    npm ci
    npx playwright install chromium
    npx playwright test
```

### 7. Auth Pattern

```ts
const AUTH = { Authorization: 'Basic ' + Buffer.from('user:pass').toString('base64') };
```

### 8. Referenced Implementation

- [email-mcp webapp e2e tests](https://github.com/sandraschi/email-mcp/tree/master/webapp/e2e) — 17 tests
- [email-mcp playwright.config.ts](https://github.com/sandraschi/email-mcp/blob/master/webapp/playwright.config.ts)

## Enforcement

- New repos: Playwright tests are REQUIRED before merging the webapp
- The `just e2e` recipe (runs `../scripts/playwright-audit.ps1`) must pass before SOTA certification
- CI MUST run `npx playwright test` on push
- Minimum: at least the Fleet Audit tests from §5 (backend health + frontend loads)
