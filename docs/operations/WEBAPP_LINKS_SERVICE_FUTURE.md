# Webapp & Container Links Service (Future)

**Version**: 1.0  
**Last Updated**: 2025-02-10  
**Status**: PLANNED

---

## Current State

- **Calibre MCP** and **Plex MCP** topbars hardcode two lists in `topbar.tsx`:
  - **WEBAPP_ZOO**: webapp label, URL, port; click checks if up, and if not calls backend `/api/webapp-launch` to run the repo start script, then opens the tab.
  - **CONTAINER_LINKS**: naive list of container UIs (Portainer, Traefik, Grafana, MyAI services, etc.); click opens URL only (no start).
- Backend **webapp-launch** in each repo has its own hardcoded port-to-(repo, script) map and uses `REPOS_ROOT` to run start scripts.

This is acceptable for now. Hardcoding in `topbar.tsx` is the intended short-term approach.

---

## Future: Single Source of Truth + Links Service

Later, the following should be implemented:

1. **Single source of truth**  
   All webapp and container port/link data lives in **mcp-central-docs** (e.g. [WEBAPP_PORTS.md](./WEBAPP_PORTS.md) and a machine-readable derivative, or a dedicated `webapp-registry.json` / `container-registry.json` that is generated from or kept in sync with the docs).

2. **Links service**  
   A dedicated service (API or MCP server) that:
   - **Reads** the registry from mcp-central-docs (file path, URL, or packaged artifact).
   - **Exposes**:
     - List of webapps: label, url, port, repo, start script path (for launch).
     - List of container UIs: label, url, port; optionally tagged as frontend vs infra so only frontends are shown in “open in browser” dropdowns.
   - **Performs starts**: given a port or app id, runs the correct start script (using the same registry), so launch logic lives in one place instead of each webapp backend.

3. **Consumers**  
   Calibre MCP, Plex MCP, and any other dashboard:
   - Call the **links service** for the webapp and container lists (and optionally for “start this app”) instead of using hardcoded lists and local `/api/webapp-launch`.
   - No duplicate port maps or script paths; everything derives from the central registry.

4. **Container registry**  
   Extend the source of truth to distinguish:
   - **Frontend** (openable in browser: Portainer, Traefik UI, Grafana, MyAI frontends, etc.).
   - **Infra** (databases, APIs, internal services) so they can be listed separately or hidden from the “Containers” dropdown.

---

## Summary

| Aspect              | Now                         | Later                                                                 |
|---------------------|-----------------------------|-----------------------------------------------------------------------|
| Webapp list         | Hardcoded in topbar.tsx     | From links service → mcp-central-docs registry                       |
| Container list      | Hardcoded in topbar.tsx     | From links service → mcp-central-docs (frontend vs infra)            |
| Start / launch      | Per-repo webapp-launch API  | Centralized in links service using same registry                      |
| Port allocation     | WEBAPP_PORTS.md             | Same; registry is the single source of truth for ports and scripts    |
