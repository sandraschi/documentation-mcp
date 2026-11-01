# BUG-051 - Stale Vite dev server silently serves CSS without Tailwind (no error anywhere)

- **ID**: BUG-051
- **Severity**: P2 (dev-only, but completely invisible: unstyled page, zero errors)
- **Date**: 2026-09-26
- **Component**: Any web_sota where Tailwind/PostCSS setup lands AFTER the dev server started
- **Status**: Fixed here (restarted frontend, verified 24 KB CSS + headless screenshot)

## Symptom

Dashboard renders all content and live data, but with NO styling at all: serif
font, blue links, no layout. Looks like "no tailwind, no css". `tsc`, `biome`,
`vite build` all green. Dev transforms return HTTP 200. Browser console shows
nothing. The served `/src/index.css` module contains ONLY hand-written custom
CSS (845 bytes) - the `@tailwind` directives produce zero output, silently.

## Root Cause

The Vite dev process (started 19:45) predated the Tailwind setup files
(`tailwind.config.js`, `postcss.config.js`, `src/index.css`, tailwind dep -
all created ~20:15). Vite does not pick up a newly-added PostCSS/Tailwind
pipeline without a restart: every file - including brand-new ones - is
transformed through the stale, PostCSS-less pipeline. Unprocessed `@tailwind`
at-rules are ignored silently by browsers, so there is no error on either side.
`vite build` uses a fresh process every time, which is why build was green
while dev was broken - the two can disagree indefinitely.

Contributing confusion: `npm ls` tree healthy, configs load standalone,
`postcss` direct run emits 22 KB with preflight - everything EXCEPT the
running process was correct.

## Resolution

Restarted the frontend dev server (fresh `npm run dev` in its own console, same
as the fleet engine spawns). Served CSS went 845 B -> 23,929 B with preflight.
Verified with a real headless Edge screenshot (sidebar, KPIs, onboarding cue
all styled) - screenshots don't lie, `tsc` doesn't see this class of failure.

## Detection command (the 10-second check, use before any CSS debugging)

```powershell
$t = (Invoke-WebRequest http://127.0.0.1:<PORT>/src/index.css).Content
$t.Length; $t -match 'box-sizing'   # False = Tailwind not processing, restart dev server
```

Also compare process start time against setup-file mtimes:
`Get-CimInstance Win32_Process -Filter "ProcessId=<vite pid>" | select CreationDate`.

## SOTA Impact

- New-repo / assfix flow: after ADDING Tailwind/PostCSS deps or configs to a
  repo whose dev server is already running, the dev server MUST be restarted.
  `start.ps1` port-clear + fresh spawn covers this on relaunch, but a running
  session never self-heals.
- Verification gap: no gate (`tsc`/`biome`/`vite build`) exercises the RUNNING
  dev server's CSS pipeline. Headless-browser screenshot
  (`msedge --headless=new --screenshot`) is the ground truth for "does the
  webapp look right" - used here, recommend for webapp assfix passes.
- Headless Edge recipe (no installs, Edge ships with Windows):
  `msedge --headless=new --disable-gpu --no-sandbox --user-data-dir=<tmp> \
--screenshot=<out>.png --window-size=1280,900 --virtual-time-budget=20000 <url>`
  Note: `--dump-dom` to stdout came back empty in this environment; `--screenshot`
  worked. Detached GUI launches from a pipe-less session die silently - spawn via
  `Start-Process powershell.exe -NoExit -Command ...` like the fleet engine does.
