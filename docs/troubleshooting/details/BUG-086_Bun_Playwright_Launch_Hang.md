# BUG-086 — playwright-core hangs on browser launch under Bun (Windows)

**Date:** 2026-10-23 | **Severity:** P2 | **Component:** `web_sota/e2e` (any Bun-run Playwright script)
**Status:** Workaround in place — run e2e under `node`, not `bun`

## Symptom

`bun e2e/smoke.mjs` with `playwright-core@1.64.1` hangs forever in
`chromium.launch()`: the browser process spawns (visible pid) but the
CDP handshake never completes — even with `--no-sandbox`,
`--disable-dev-shm-usage`, system Chrome channel, and headless shells
1161/1169/1248. Same script under `node v24.4.1` passes 11/11 in seconds.

## Root cause (suspected)

Bun's stdio/pipe transport for the Chrome DevTools remote-debugging pipe
does not complete the handshake on Windows. Not version-specific to the
browser: system Chrome, full Chromium 1248, and three headless-shell builds
all hang identically under Bun and all work under node.

## Workaround applied

`just e2e` and `package.json` e2e script invoke `node`, never `bun`:
`& "C:\Program Files\nodejs\node.exe" web_sota/e2e/smoke.mjs`.
`playwright-core` stays a devDependency (installed via bun, resolved fine
under node from `node_modules/`).

## Proper fix (open)

- Retest with newer Bun (1.3.14 observed) — may already be fixed upstream.
- Fleet rule candidate: Playwright scripts always run under node even in
  bun-managed webapps; document in e2e/cua testing standards.
