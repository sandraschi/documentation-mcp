---
title: "Port Occupancy: who can take a port, and how we find out"
category: reference
status: active
audience: all
last_updated: 2026-10-13
---

# Port Occupancy

Why allocating a port in this fleet is harder than reading one table, what actually
occupies the 10700-15000 reservoir, and which tool answers which question.

This exists because on 2026-09-18 the allocator built to *prevent* port collisions
**created four of them in a single afternoon**. Every one came from the same mistake:
consulting a source that did not know the whole truth.

## The reservoir is not reserved

`WEBAPP_PORTS.md` calls 10700-15000 "reserved". It is reserved **from us**, by
convention, and from nobody else. Nothing stops a third-party installer, a container
image or a colleague's side project from binding 11191.

That is not hypothetical. `open-webui` holds 11191 on this machine. Its maintainer picked
a high, odd-looking port on the same reasoning we did -- *nobody else will want this one*
-- and we then allocated it to `repomix-mcp`. There is no public registry that would have
prevented this; IANA and the Wikipedia port list cover well-known services, not the
"weird port" band that everyone reaches into precisely because it looks empty.

**The authoritative list of what is taken is this machine, not any document.**

## Five ways a port gets occupied

| # | Occupant | Visible in | Caught by |
|---|---|---|---|
| 1 | A fleet repo's backend/frontend | `fleet-start.config.ps1` | `fleet_lock.py` |
| 2 | A fleet repo's **extra** port (health, metrics, sidecar) | **nowhere** | nothing yet -- see Gaps |
| 3 | A compose file publishing a host port | `docker-compose.yml` | `compose_ports.py` |
| 4 | A running container (`docker run -p`, or a clone under `external/`) | `docker ps` | `compose_ports.py --running` |
| 5 | A native process (service, installed app) | the OS listener table | `compose_ports.py` listener scan |

Classes 3-5 were all invisible until 2026-09-18, which is why four bad allocations
happened in a row.

### Class 2 is still open

`teleconference-mcp` binds **10891** as `HEALTH_PORT`, a health/diagnostics/metrics
server separate from its MCP server on 10887. Its config declares only 10886/10887, so
the lock never knew 10891 was taken and `sdr-mcp` sat on it. The config schema models
exactly two ports; reality routinely has three or more.

## Static vs runtime: why both

A **compose file with a reserved-range port whose container is never started** is the
nastiest case in the fleet. Nothing is listening, so no runtime probe sees it. The
collision surfaces months later, on whatever machine finally runs that stack, with no
obvious link to the file that caused it. Only a static scan catches the *declaration*.

Conversely, a static scan cannot see `docker run -p 11191:8080`, a clone under
`_upstream/`, or a native app. Only the runtime checks catch those.

Neither is sufficient. Both are cheap.

## Ghosts

On 2026-09-18 five containers -- `games-gateway`, `games-stockfish`, `games-go`,
`games-shogi`, `games-collection-web` -- were found running from compose project
`games-app`, whose working directory `D:\Dev\repos\games-app` **no longer existed**.
They held seven fleet ports and no surviving repo explained why. `ai-games-collection`
is the successor and its compose defines the same services plus four more engines, so
the ghosts were also blocking it from starting its own stack.

Removed (no volumes, so no data at risk). The lesson: **deleting or renaming a repo does
not stop its containers.** Check `docker ps -a --filter label=com.docker.compose.project=<name>`
after retiring anything containerised.

## How to take a port

Never pick by hand. Never read one table and conclude.

```bash
python mcp-central-docs/fleet-gate/claim_ports.py --repo my-new-mcp --apply --emit-config
```

It considers registry rows, every `fleet-start.config.ps1`, every compose file, and every
running container before offering a pair. `new-mcp-server.ps1` calls it automatically, so
a scaffolded repo cannot be born on an occupied port.

## How to find out what is taken

```bash
# everything occupying the reservoir, and what collides with the lock
python fleet-gate/compose_ports.py --conflicts --running

# refresh the "Non-fleet occupants" table in WEBAPP_PORTS.md
python fleet-gate/compose_ports.py --running --write-registry

# who else in the fleet references a port before you move it
python fleet-gate/find_hardcoded_ports.py <repo>:<port>
```

The nightly gate runs the first and second.

## Moving a port is not a one-line change

Repos name their own ports in **10-24 places**: `vite.config.ts`, `src/lib/api.ts`,
`server.py`, `mcpb/manifest.json`, `stop.ps1`, `playwright.config.ts`, `.env.example`,
`native/src/backend.rs`, docs. Changing only the config leaves the frontend proxying to a
backend that is no longer there -- which presents as *exactly* the bug being fixed.

Use `migrate_port.py` (dry run by default, `.bak` per file), and check two things first:

1. **Who else points at this port?** `readly-mcp` had live consumers in `robofang`,
   `arxiv-mcp` and `aiwatcher-mcp`.
2. **Does this port actually belong to this repo?** `ai-producer-hub` declared
   `BackendPort = 10885`, but 10885 is **songgeneration-mcp's** backend, which it merely
   *consumes*. Renumbering would have broken a working integration.

## Gaps, stated plainly

- **Class 2 (undeclared extra ports) is undetected.** Needs an `ExtraPorts` schema field
  *and* a code scanner, because declaration alone relies on memory.
- The ownership heuristic in the runtime check still misfires where a container's name
  shares no stem with its repo.
- A native listener that starts *after* a nightly run is invisible until the next one.
