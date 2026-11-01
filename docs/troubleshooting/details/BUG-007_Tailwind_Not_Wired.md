# BUG-007: Tailwind CSS Not Wired (Leporello Webapp)

**Severity**: P2 (Medium)
**Discovered**: 2026-07-30
**Repo**: overte-mcp (fleet-wide pattern)
**Status**: Fixed

## Symptom

Webapp renders as completely unstyled HTML — colloquially a "leporello" (accordion-fold of raw content). React components mount correctly (sidebar nav items, dashboard content all present in DOM), but every Tailwind utility class (`flex`, `bg-slate-950`, `gap-3`, `text-sm`, etc.) has zero effect. The app looks like a 1990s HTML page.

Agent debugging incorrectly focuses on:
- React rendering / hydration failures
- Backend connectivity / CORS
- Zombie processes / port conflicts
- PowerShell version mismatches
- Console errors

**None of these are the cause.** The app works perfectly — it just has no stylesheet.

## Root Cause

Tailwind CSS was never wired into the project. Three things must all be present:

1. **`package.json`** — `tailwindcss` and `@tailwindcss/vite` in `devDependencies`
2. **`vite.config.ts`** — `import tailwindcss from '@tailwindcss/vite'` and `plugins: [react(), tailwindcss()]`
3. **`src/index.css`** — `@import "tailwindcss";` at the very top (before all custom styles)

If any one of the three is missing, Tailwind classes silently do nothing. No warning, no error — just unstyled output.

## Why Agents Miss It

- The `glass-panel` and `glass-card` CSS classes are defined in `index.css` and render fine, giving a false sense that CSS works.
- Tailwind utility classes don't cause broken layout — they just don't apply. The HTML structure is correct, so accessibility snapshots show the right content.
- Console has zero errors. The app "works" — it just looks broken.
- Agents instinctively debug JavaScript, not CSS.

## Prevention

When a webapp renders as unstyled HTML, **always check the three Tailwind wiring points first** before touching anything else. This check takes 30 seconds and rules out a common cause that can waste hours. Add it to any webapp debugging checklist:

```
1. Is tailwindcss in package.json devDependencies?
2. Is @tailwindcss/vite imported and added to plugins in vite.config.ts?
3. Is @import "tailwindcss" at the top of index.css?
```

## Fix

Add the three missing pieces. Then `bun install` and `bun run build` — CSS size should jump from ~1.4 kB (custom styles only) to ~25 kB (Tailwind + custom).

```bash
bun add -d tailwindcss @tailwindcss/vite
```

Then edit `vite.config.ts`:
```ts
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Then edit `src/index.css` — add `@import "tailwindcss";` as the first line.
