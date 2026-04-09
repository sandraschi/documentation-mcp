---
title: "Webapp Port Reservoir"
category: reference
status: active
audience: mcp-dev
skill_candidate: false
related:
  - operations/SOTA_MASTER_INVENTORY.md
  - operations/webapp-registry.json
last_updated: 2026-03-27
---

# Webapp Port Reservoir

**Version**: 1.0  
**Last Updated**: 2025-02-10  
**Status**: MANDATORY

---

## Purpose

All MCP server webapps and dashboards MUST use ports from the reserved range **10700-11000**. This eliminates port conflicts with common dev defaults (3000, 5000, 5173, 8000, 8080) and provides a single predictable range for the entire ecosystem.

## Port Range

- **Reserved**: 10700-11000 (300 ports)
- **Spacing**: Use even-numbered ports with gaps (10700, 10702, 10704...) to absorb "port hopper" drift
- **No collision** with IANA well-known (0-1023) or common dev ports
- **Adjacency Rule (MANDATORY)**: Frontend and Backend ports for a single project MUST be kept together (e.g., 10792/10793). Do NOT "hop" into unused lower gaps if it breaks project adjacency.

## FORBIDDEN Ports

**NEVER** use these for new webapps:

- 3000 (Create React App, many Node dev servers)
- 5000 (Flask default, many Python dev servers)
- 5173 (Vite default)
- 8000, 8080 (common API/defaults)
- 5174, 5175 (Vite fallbacks)
- Any port below 1024 (privileged)

## Port Allocation Registry

| Port | Repo | Service |
|------|------|---------| 
| 10700 | virtualization-mcp | Web dashboard |
| 10702 | git-github-mcp | Backend (FastAPI + MCP HTTP) |
| 10703 | git-github-mcp | Frontend (Vite dev) |
| 10704 | advanced-memory-mcp | Webapp |
| 10705 | advanced-memory-mcp | Bridge server |
| 10706 | robotics-mcp | Web dashboard |
| 10708 | database-operations-mcp | Web dashboard |
| 10710 | unity3d-mcp | Web dashboard |
| 10712 | vrchat-mcp | Web dashboard |
| 10714 | resonite-mcp | Web dashboard |
| 10715 | devices-mcp | USB camera helper (Windows; optional) |
| 10716 | devices-mcp | Frontend (Vite dev; fleet default) |
| 10717 | devices-mcp | Backend (FastAPI web-sota API) |
| 10718 | meta_mcp | Backend |
| 10719 | meta_mcp | Frontend |
| 10720 | calibre-mcp | Backend |
| 10721 | calibre-mcp | Frontend |
| 10722 | mywienerlinien | Frontend |
| 10724 | mcp-studio | Backend |
| 10725 | mcp-studio | Frontend |
| 10728 | ring-mcp | Web dashboard |
| 10730 | moltbot-mcp | Webapp |
| 10732 | advanced-memory-mcp | MCP SSE transport |
| 10733 | advanced-memory-mcp | Startup service |
| 10734 | myai/calibre_plus | Frontend |
| 10735 | advanced-memory-mcp | Auto-start service |
| 10736 | myai/calibre_plus | Backend |
| 10738 | dark-app-factory | Web dashboard |
| 10739 | dark-app-factory | MCP streamable HTTP (`mcp-server/`, path `/mcp`) |
| 10740 | plex-mcp | Webapp backend |
| 10741 | plex-mcp | Webapp frontend |
| 10742 | filesystem-mcp | Backend |
| 10743 | filesystem-mcp | Frontend |
| 10744 | universal-actuator-mcp | Web dashboard frontend |
| 10745 | universal-actuator-mcp | Web dashboard backend (API) |
| 10748 | windows-operations-mcp | Backend |
| 10749 | windows-operations-mcp | Frontend |
| 10750 | reversing-mcp | Backend (API) |
| 10751 | reversing-mcp | Frontend |
| 10752 | nest-protect-mcp | Frontend |
| 10753 | nest-protect-mcp | Backend |
| 10756 | discord-mcp | Backend (MCP streamable HTTP `/mcp` + REST) |
| 10757 | discord-mcp | Frontend |
| 10762 | winrar-mcp | Backend |
| 10763 | winrar-mcp | Frontend |
| 10764 | openclaw-molt-mcp | Frontend |
| 10765 | openclaw-molt-mcp | Backend |
| 10766 | osc-mcp | Web dashboard frontend |
| 10767 | osc-mcp | Web dashboard backend |
| 10768 | openmanus-mcp | Backend (FastAPI) |
| 10769 | openmanus-mcp | Frontend (Vite) |
| 10770 | arxiv-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10771 | arxiv-mcp | Frontend (Vite) |
| 10772 | gimp-mcp | Frontend |
| 10773 | gimp-mcp | Backend |
| 10774 | bumi-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10775 | bumi-mcp | Frontend (Vite) |
| 10776 | glance-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10777 | glance-mcp | Frontend (Vite) |
| 10778 | xkcd-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10779 | xkcd-mcp | Frontend (Vite) |
| 10782 | home-assistant-mcp | MCP HTTP |
| 10788 | pywinauto-mcp | Web dashboard frontend |
| 10789 | pywinauto-mcp | Web dashboard backend |
| 10791 | documentation-mcp | Fleet Starts Launcher (ASGI UI) |
| 10792 | avatar-mcp | Web dashboard frontend |
| 10793 | avatar-mcp | Web dashboard backend (API) |
| 10794 | documentation-mcp | Fleet Dashboard |
| 10795 | documentation-mcp | Fleet Frontend |
| 10796 | reaper-mcp | Web dashboard frontend |
| 10797 | reaper-mcp | Web dashboard backend |
| 10798 | multi-backup-mcp | Frontend |
| 10799 | multi-backup-mcp | Backend |
| 10800 | alexa-mcp | Web dashboard frontend |
| 10801 | alexa-mcp | Web dashboard backend |
| 10802 | bookmarks-mcp | Web dashboard frontend |
| 10803 | bookmarks-mcp | Web dashboard backend |
| 10804 | rustdesk-mcp | Web dashboard frontend |
| 10805 | rustdesk-mcp | Web dashboard backend |
| 10806 | docker-mcp | Web dashboard frontend |
| 10807 | docker-mcp | Web dashboard backend |
| 10808 | iflow-mcp-catalog | Web dashboard frontend (Vite) |
| 10809 | iflow-mcp-catalog | Web dashboard backend (FastAPI `/api/*`) |
| 10810 | notion-mcp | Web dashboard frontend |
| 10811 | notion-mcp | Web dashboard backend |
| 10812 | email-mcp | Web dashboard frontend |
| 10813 | email-mcp | Web dashboard backend |
| 10814 | notepadpp-mcp | Web dashboard frontend |
| 10815 | notepadpp-mcp | Web dashboard backend |
| 10816 | toolbench-mcp | Web dashboard frontend (Vite) |
| 10817 | toolbench-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10818 | obs-mcp | Web dashboard frontend |
| 10819 | obs-mcp | Web dashboard backend |
| 10820 | tailscale-mcp | Web dashboard frontend |
| 10821 | tailscale-mcp | Web dashboard backend |
| 10822 | netatmo-weather-mcp | Web dashboard frontend |
| 10823 | netatmo-weather-mcp | Web dashboard backend |
| 10826 | directmedia-mcp | Web dashboard frontend |
| 10827 | directmedia-mcp | Web dashboard backend |
| 10828 | nest-protect-mcp | Web dashboard frontend |
| 10829 | nest-protect-mcp | Web dashboard backend |
| 10830 | unity3d-mcp | Web dashboard frontend |
| 10831 | unity3d-mcp | Web dashboard backend |
| 10832 | local-llm-mcp | Web dashboard frontend |
| 10833 | local-llm-mcp | Web dashboard backend |
| 10834 | home-assistant-mcp | Web dashboard frontend |
| 10835 | home-assistant-mcp | Web dashboard backend |
| 10836 | llm-txt-mcp | Web dashboard frontend |
| 10837 | llm-txt-mcp | Web dashboard backend |
| 10838 | immich-mcp | Web dashboard frontend |
| 10839 | immich-mcp | Web dashboard backend |
| 10840 | beyondcompare-mcp | Web dashboard frontend |
| 10841 | beyondcompare-mcp | Web dashboard backend |
| 10842 | davinci-resolve-mcp | Web dashboard frontend |
| 10843 | davinci-resolve-mcp | Web dashboard backend |
| 10844 | fastsearch-mcp | Web dashboard frontend |
| 10845 | fastsearch-mcp | Web dashboard backend |
| 10848 | blender-mcp | Web dashboard frontend |
| 10849 | blender-mcp | Web dashboard backend |
| 10850 | monitoring-mcp | Web dashboard frontend |
| 10851 | monitoring-mcp | Web dashboard backend |
| 10852 | web-development-mcp | Web dashboard frontend |
| 10853 | web-development-mcp | Web dashboard backend |
| 10854 | paperless-ngx | Web interface |
| 10858 | ocr-mcp | Web dashboard frontend |
| 10859 | ocr-mcp | Web dashboard backend |
| 10860 | system-admin-mcp | Web dashboard frontend |
| 10861 | system-admin-mcp | Web dashboard backend |
| 10862 | sakana-mcp | Web dashboard frontend (Vite) |
| 10863 | sakana-mcp | Web dashboard backend (FastAPI) |
| 10864 | worldlabs-mcp | Web dashboard frontend |
| 10865 | worldlabs-mcp | Web dashboard backend |
| 10870 | robofang | Web dashboard frontend |
| 10871 | robofang | Bridge server |
| 10872 | robofang | Supervisor |
| 10874 | handbrake-mcp | Web dashboard frontend |
| 10875 | handbrake-mcp | Web dashboard backend |
| 10876 | virtualdj-mcp | Web dashboard frontend |
| 10877 | virtualdj-mcp | Web dashboard backend |
| 10878 | vienna-live-mcp | Web dashboard frontend |
| 10879 | vienna-live-mcp | Web dashboard backend |
| 10880 | vroidstudio-mcp | Web dashboard frontend |
| 10881 | vroidstudio-mcp | Web dashboard backend |
| 10882 | suno-mcp | Web dashboard frontend |
| 10883 | suno-mcp | Web dashboard backend |
| 10884 | songgeneration-mcp | Web dashboard frontend |
| 10885 | songgeneration-mcp | Web dashboard backend |
| 10886 | myconf | Webapp frontend |
| 10887 | myconf | Webapp backend |
| 10888 | myai | Webapp frontend |
| 10889 | myai | webapp_api backend |
| 10892 | yahboom-mcp | Web dashboard backend (API) |
| 10893 | yahboom-mcp | Web dashboard frontend |
| 10894 | dreame-mcp | Backend (MCP SSE + REST API, DreameHome cloud); fleet map: `GET /api/v1/map` |
| 10895 | dreame-mcp | Frontend (Vite React dashboard; proxies `/api` → 10894) |
| 10896 | mywienerlinien | Webapp dashboard (Vite, proxies → 3079) |
| 10897 | magentart-mcp | Magenta RT (Docker Backend) |
| 10898 | magentart-mcp | Web dashboard frontend |
| 10899 | magentart-mcp | Web dashboard backend (FastAPI) |
| 10900 | audiotool-nexus-mcp | Webapp frontend (Vite / React) |
| 10901 | observability-mcp | Web dashboard frontend |
| 10902 | observability-mcp | Web dashboard backend (API) |
| 10922 | gtfs-mcp | MCP HTTP / Webapp (was incorrectly overlapping 10897 with magentart-mcp in JSON) |
| 10924 | kyutai-mcp | Web dashboard backend (FastAPI) |
| 10925 | kyutai-mcp | Web dashboard frontend (Vite) |
| 10926 | kyutai-mcp | MCP HTTP `/mcp` |
| 10927 | lewm-mcp | FastAPI + MCP HTTP `/mcp` (LeWorldModel bridge) |
| 10928 | lewm-mcp | Vite dashboard (glass UI) |
| 10930 | songgeneration-mcp | SongGeneration-Studio default local API/UI target |
| 10932 | openclaude-mcp | MCP SSE backend (FastMCP 3.2) + REST bridge (`/tools/{name}`) |
| 10933 | openclaude-mcp | React webapp (Vite) |
| 10940 | alsergrund-bridge | Backend (FastMCP) |
| 10941 | alsergrund-bridge | Frontend (Vite) |

## Port Allocation Registry (Live)

Source of truth in machine-readable JSON:
- [webapp-registry.json](./webapp-registry.json)
- [container-registry.json](./container-registry.json)

> **FORBIDDEN PORTS (3000, 5000, 5173, 8000, 8080)**: Strictly prohibited for production webapps. Any webapp found on these ports will be forcefully migrated.

## New Webapp Checklist

1. Pick next available port from registry (check for gaps)
2. Add entry to this document
3. Configure via env: `WEB_PORT=107xx` or `PORT=107xx`
4. Update vite.config.ts proxy if using Vite dev

## Cross-MCP Deck Handoff Convention

For DJ/media fleet interoperability, servers that expose deck control should keep a stable REST handoff surface:

- `POST /api/v1/deck/{deck_id}/load`
- `POST /api/v1/deck/{deck_id}/play_pause`
- `POST /api/v1/deck/{deck_id}/sync`
- `POST /api/v1/deck/{deck_id}/cue`

Current reference implementation: `virtualdj-mcp` (`10877` backend).  
Current upstream consumer: `songgeneration-mcp` Listen export flow (`10885` backend).

## Webapp Startup (MANDATORY)

Every start script MUST clear its port of zombies before binding. Required files: `start.ps1` + `start.bat`.

**Browser (recommended):** SOTA `start.ps1` scripts should **open the webapp in the default browser as the final step** after the frontend is reachable (either `Start-Process http://...` after a readiness poll, or an equivalent hidden poll + open). Many repos still only print a URL and rely on a manual click — that is allowed but not ideal for parity across the fleet.

```powershell
# start.ps1 pattern
$WebPort = 10700   # YOUR port from registry
npx --yes kill-port $WebPort 2>$null
# OR: Get-NetTCPConnection -LocalPort $WebPort -ErrorAction SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

```bat
@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
```
