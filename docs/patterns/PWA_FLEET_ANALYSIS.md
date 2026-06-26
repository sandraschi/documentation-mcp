# PWA (Progressive Web App) — Fleet Analysis

**Date:** 2026-05-02  
**Status:** Decision — not adopted as fleet standard  
**Tags:** webapp, frontend, pwa, vite, react, pattern, decision

---

## Summary

PWA is not recommended as a fleet-wide standard for MCP server webapps. The features it provides
do not align with the operational profile of local homelab tooling. It may be added selectively to
specific apps where the "installed app" UX is desirable.

---

## What PWA Actually Provides

Three pillars:

1. **Installability** — pin app to OS taskbar/desktop as a standalone window (no browser chrome)
2. **Offline support** — service worker caches assets; app loads without a network connection
3. **Web app manifest** — branded icon, display name, splash screen, theme colour

Secondary capabilities: push notifications, background sync, app store submission.

---

## Technical Implementation (Vite Stack)

Adding basic PWA to any Vite/React app is a one-liner:

```bash
npm install vite-plugin-pwa -D
```

```ts
// vite.config.ts
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({ registerType: 'autoUpdate' })
  ]
})
```

This generates a service worker and manifest at build time. For **manifest-only installability**
(no offline caching), a hand-written `public/manifest.json` is sufficient and avoids service
worker complexity entirely.

The real complexity cost comes from:
- Service worker lifecycle management (update prompts, stale cache handling)
- Defining a caching strategy per route/endpoint
- Debugging stale builds served from cache during development
- Cross-browser compatibility edge cases

---

## Why This Does Not Fit the Fleet

All fleet webapps share the same operational profile:

- **Local-only** — served on `localhost:XXXX`, LAN access only
- **Backend-dependent** — every app is a thin frontend over a running MCP/Starlette server
- **No mobile use case** — primary interface is Claude Desktop on Goliath

The killer PWA features are therefore useless:

| PWA Feature | Fleet Reality |
|---|---|
| Offline mode | App is useless if backend is down regardless |
| Push notifications | Covered by speechops + robofang |
| App store distribution | Irrelevant |
| Installability | Achievable without full PWA (see below) |

Additionally, service worker caching actively causes pain in local dev: stale JS/CSS is served
from cache after a `npm run build`, requiring manual cache clears. For a fleet of 135+ servers
that are iterated rapidly, this is net-negative.

---

## The One Case Where It Makes Sense

**Manifest-only installability** — no service worker, just a `manifest.json`. This gives:
- Standalone window (no browser address bar)
- Custom icon in taskbar
- Branded splash screen

Implementation cost: ~15 minutes per app.

Good candidates:
- `aiwatcher-mcp` dashboard (permanent monitor window)
- `arxiv-mcp` webapp (reference panel on secondary screen)
- Any app intended for "always-on" display use

To implement manifest-only:
1. Add `public/manifest.json` with `name`, `short_name`, `icons`, `start_url`, `display: "standalone"`
2. Link it in `index.html`: `<link rel="manifest" href="/manifest.json">`
3. Generate icons (192px and 512px minimum)

No `vite-plugin-pwa` needed. No service worker. Chrome/Edge will show the install button in the
address bar.

---

## Why DeepSeek Added It

Pattern-matching against "modern webapp checklist." DeepSeek (and similar code completion tools)
treat PWA as a default best practice for any Vite/React app because it is for public-facing
consumer apps. It does not reason about deployment context. The addition is not wrong per se —
it just solves problems that don't exist in a local homelab fleet.

---

## Decision

| Scenario | Recommendation |
|---|---|
| Fleet-wide standard | **No** — not in `WEBAPP_SOTA_STANDARDS.md` |
| Full PWA (service worker + offline) | **No** — maintenance cost exceeds value |
| Manifest-only (installability) | **Optional** — add if pinned-to-taskbar UX is wanted |
| AI-generated code adds `vite-plugin-pwa` | **Review** — remove if offline features not needed |

When reviewing AI-generated code that includes `vite-plugin-pwa`, check whether the service worker
configuration is actually doing anything useful. If it is just `registerType: 'autoUpdate'` with
no custom cache strategies, the offline benefit is marginal and the stale-cache risk is real.
Replacing it with a manifest-only approach is usually the right call.

---

## References

- `standards/WEBAPP_SOTA_STANDARDS.md` — current fleet frontend standard
- `patterns/webapp-integration-pattern.md` — MCP webapp integration pattern
- `patterns/WEBAPP_SETUP_GUIDE.md` — webapp setup guide
