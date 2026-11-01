# BUG-042 — Vite Dev Serves Stale Transform, New Route Silently 404s

- **ID**: `BUG-042`
- **Severity**: `P2` (non-blocking, but burns debug hours mimicking a code bug)
- **Date**: 2026-09-20
- **Repo/Component**: `resonite-mcp` `web_sota` vite dev server (:10978) —
  applies to any long-lived vite dev server on this Windows host
- **Status**: Worked around (dev server restarted, PID 53704); root watcher
  flakiness not fixed, detection documented below

## Symptom

New route `/world-builder` added to `src/App.tsx` (import + `<Route>`,
`tsc` + `biome` clean, route confirmed on disk) redirected to `/` via the
catch-all `<Navigate>` on every load — fresh browser profiles included.
Zero errors anywhere: no console/pageerror output, no failed requests, all
static gates green. Indistinguishable from a wrong path or a typo in the
route table. Sibling edits made in the same session (sidebar link to the
same route) rendered fine, which deepened the misdirection.

## Root Cause

The dev server's in-memory transform cache went stale for exactly one file:
the served transform of `src/App.tsx` did **not** contain the new route
while the file on disk did. Verified, not inferred:

```powershell
# disk: route present (App.tsx line 82)
Select-String -Path src\App.tsx -Pattern 'world-builder'
# served transform: NO match before restart, match after restart
(Invoke-WebRequest -Uri 'http://127.0.0.1:10978/src/App.tsx' -UseBasicParsing).Content |
  Select-String -Pattern 'world-builder'
```

Fresh browser profiles kept failing, which rules out client cache and HMR
client state — the staleness was server-side. The file watcher missed the
change event for `App.tsx` while catching `sidebar.tsx`, so no
re-transform was ever triggered. Likely contributors (not proven at kernel
level): Windows watcher flakiness under load combined with atomic-save file
replacement. The dev server had been running ~1.5h with dozens of node
processes on the box.

## Resolution

Restarted the vite dev server (old node PID 63868 → new PID 53704 via
`node node_modules/vite/bin/vite.js --port 10978 --host 127.0.0.1`);
fresh transform cache served the route immediately, page works.

## Detection Next Time

A new page/route/component "doesn't exist" at runtime despite correct code
on disk, with all linters green and no console errors: **compare disk vs
served transform before touching code**:

```powershell
Select-String -Path src\App.tsx -Pattern '<your-new-thing>'
(Invoke-WebRequest -Uri 'http://127.0.0.1:<port>/src/App.tsx' -UseBasicParsing).Content |
  Select-String -Pattern '<your-new-thing>'
```

Disk yes + served no = stale dev server, restart vite. Do not debug the
router, do not rewrite the route.

## Fleet Audit Note (protocol)

This cannot be found by grepping repos — it is environmental, not a code
antipattern. Blast radius is every long-lived vite dev server on Goliath
(~190 webapps). No per-repo sweep is meaningful; the served-vs-disk check
above is the screen. If it recurs on one box repeatedly, suspect AV/indexer
interference with the file watcher rather than any repo's code.

## Related

- Same misdirection class as BUG-007 (correct structure, wrong layer —
  hours burnable on React/backend/CORS while the fix is 3 lines / one
  restart).
- Inverse of BUG-026 (false green): here the tests are green and the code
  is correct, but the *server* lies about what it serves.
