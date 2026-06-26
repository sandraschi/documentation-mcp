---
title: "Webapp Port Reservoir"
category: reference
status: active
audience: mcp-dev
skill_candidate: false
related:
  - operations/SOTA_MASTER_INVENTORY.md
  - operations/webapp-registry.json
last_updated: 2026-05-25
---

# Webapp Port Reservoir

**Version**: 1.0  
**Last Updated**: 2026-06-16  
**Status**: MANDATORY

---

## Purpose

All MCP server webapps and dashboards MUST use ports from the reserved range **10700-11500**. This eliminates port conflicts with common dev defaults (3000, 5000, 5173, 8000, 8080) and provides a single predictable range for the entire ecosystem.

## Port Range

- **Reserved**: 10700-11500 (800 ports)
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
| 10700 | virtualization-mcp | Frontend (Vite dev) |
| 10701 | virtualization-mcp | Backend (FastAPI REST) |
| 10702 | virtualization-mcp | MCP HTTP/SSE (streamable) |
| 10702 | git-github-mcp | Backend (FastAPI + MCP HTTP) |
| 10703 | git-github-mcp | Frontend (Vite dev) |
| 10704 | advanced-memory-mcp | Webapp |
| 10705 | advanced-memory-mcp | Bridge server |
| 10706 | robotics-mcp | Web dashboard |
| 10708 | database-operations-mcp | Web dashboard |
| 10710 | unity3d-mcp | Web dashboard |
| 10712 | vrchat-mcp | Web dashboard |
| 10715 | devices-mcp | USB camera helper (Windows; optional) |
| 10716 | devices-mcp | Frontend (Vite dev; fleet default) |
| 10717 | devices-mcp | Backend (FastAPI web-sota API); Fritz probe `GET /api/fleet/priority` |
| 10718 | meta_mcp | Backend |
| 10719 | meta_mcp | Frontend |
| 10720 | calibre-mcp | Backend |
| 10721 | calibre-mcp | Frontend |
| 10722 | mywienerlinien | Frontend |
| 10724 | mcp-studio | Backend |
| 10725 | mcp-studio | Frontend |
| 10726 | depot-mcp | Frontend (Vite dev; SOTA dashboard) |
| 10727 | depot-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`) |
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
| 10744 | autohotkey-test | ScriptletCOMBridge HTTP server (AHK depot bridge: /scriptlets, /run, /stop, /dashboard) |
| 10745 | autohotkey-test | (reserved — future AHK dashboard backend) |
| 10746 | autohotkey-mcp | Backend (FastAPI + MCP HTTP, dual transport) |
| 10747 | autohotkey-mcp | Frontend (Vite React SPA: Overview, Help, Chat, Scriptlets, Running, Status, Tools) |
| 10748 | windows-operations-mcp | Backend |
| 10749 | windows-operations-mcp | Frontend |
| 10750 | reversing-mcp | Backend (API) |
| 10751 | reversing-mcp | Frontend |
| 10752 | nest-protect-mcp | Frontend |
| 10753 | nest-protect-mcp | Backend |
| 10756 | discord-mcp | Backend (MCP streamable HTTP `/mcp` + REST) |
| 10757 | discord-mcp | Frontend |
| 10758 | openbci-mcp | Web dashboard frontend (Vite) |
| 10759 | openbci-mcp | Backend (REST + MCP HTTP `/mcp` + WebSocket EEG) |
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
| 10824 | gimp-mcp | GIMP Live Bridge (TCP to GIMP plugin) |
| 10825 | agy-fleet-mcp | MCP HTTP only (`/mcp` + `/health`; no dashboard) |
| 10774 | bumi-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10775 | bumi-mcp | Frontend (Vite) |
| 10776 | glance-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10777 | glance-mcp | Frontend (Vite) |
| 10778 | xkcd-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10779 | xkcd-mcp | Frontend (Vite) |
| 10780 | browser-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10781 | browser-mcp | Frontend (Vite; browser control + bookmarks dashboard) |
| 10782 | home-assistant-mcp | MCP HTTP |
| 10783 | notebooklm-fleet-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10784 | notebooklm-fleet-mcp | Frontend (Vite glass) |
| 10788 | windows-computer-use-mcp | Web dashboard frontend |
| 10789 | windows-computer-use-mcp | Web dashboard backend |
| 10790 | avatar-mcp | Prometheus metrics (METRICS_PORT; not the MCP HTTP surface) |
| 10791 | mcp-central-docs | Fleet Starts Launcher (starts-ui ASGI) |
| 10792 | avatar-mcp | Web dashboard frontend |
| 10793 | avatar-mcp | Web dashboard backend (API) |
| 10794 | mcp-central-docs | Docs MCP webapp frontend (Vite) |
| 10795 | mcp-central-docs | Docs MCP backend (REST `/api/*` + MCP streamable HTTP `/mcp`) |
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
| 10840 | beyondcompare-mcp | Vite dashboard (`web_sota`; dev proxy `/api` + `/mcp` → 10841) |
| 10841 | beyondcompare-mcp | Unified FastAPI + FastMCP gateway (REST + MCP default `/mcp`) |
| 10842 | davinci-resolve-mcp | Web dashboard frontend |
| 10843 | davinci-resolve-mcp | Web dashboard backend |
| 10844 | fastsearch-mcp | Web dashboard frontend |
| 10845 | fastsearch-mcp | Web dashboard backend |
| 10846 | readly-mcp | Web dashboard (Vite; proxies to readly-mcp REST) |
| 10848 | blender-mcp | Web dashboard frontend |
| 10849 | blender-mcp | Web dashboard backend |
| 10850 | monitoring-mcp | Web dashboard frontend |
| 10851 | monitoring-mcp | Web dashboard backend |
| 10852 | web-development-mcp | Web dashboard frontend |
| 10853 | web-development-mcp | Web dashboard backend |
| 10854 | paperless-ngx | Web interface |
| 10855 | leanforge-mcp | Web dashboard backend (FastAPI + SSE live updates) |
| 10856 | leanforge-mcp | Web dashboard frontend (Vite React) |
| 10858 | ocr-mcp | Web dashboard frontend |
| 10859 | ocr-mcp | Web dashboard backend |
| 10860 | system-admin-mcp | Web dashboard frontend |
| 10861 | system-admin-mcp | Web dashboard backend |
| 10862 | sakana-mcp | Web dashboard frontend (Vite) |
| 10863 | sakana-mcp | Web dashboard backend (FastAPI) |
| 10864 | worldlabs-mcp | Web dashboard frontend |
| 10865 | worldlabs-mcp | Web dashboard backend |
| 10866 | repomix-mcp | Web dashboard (Vite dev) |
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
| 10890 | obsidian-mcp | Web dashboard frontend (Vite) |
| 10915 | obsidian-mcp | Backend (FastAPI `obsidian_mcp.gateway`; deduped from myai **10889**) |
| 10892 | yahboom-mcp | Web dashboard backend (API) |
| 10893 | yahboom-mcp | Web dashboard frontend |
| 10894 | dreame-mcp | Backend (MCP SSE + REST API, DreameHome cloud); fleet map: `GET /api/v1/map` |
| 10895 | dreame-mcp | Frontend (Vite React dashboard; proxies `/api` → 10894) |
| 10896 | mywienerlinien | Webapp dashboard (Vite, proxies → 3079) |
| 10897 | magentart-mcp | Magenta RT (Docker Backend) |
| 10898 | magentart-mcp | Web dashboard frontend |
| 10899 | magentart-mcp | Web dashboard backend (FastAPI) |
| 10900 | teleoperator-mcp | WebXR client frontend (Vite; Pico browser) |
| 10901 | teleoperator-mcp | Backend (FastAPI + WebSocket + MCP HTTP `/mcp`) |
| 10900 | audiotool-nexus-mcp | Webapp frontend (Vite / React) |
| 12007 | observability-mcp | Web dashboard backend (MCP HTTP `/mcp`) |
| 12008 | observability-mcp | Web dashboard frontend (Vite) |
| 12009 | observability-mcp | Process Prometheus `/metrics` exporter |
| 10903 | myai/document_viewer | document-viewer container (Flask/FastAPI, internal :5192) |
| 10904 | myai/future_you | future-you container (uvicorn, internal :5194) |
| 10905 | myai/stablediff_gradio | stablediff-gradio container (gpu profile, internal :5196) |
| 10906 | onenote-mcp | Web dashboard frontend (Vite) |
| 10907 | onenote-mcp | Backend (FastMCP HTTP; path `/mcp`) |
| 10908 | speech-mcp | Web dashboard frontend (Vite) |
| 10909 | speech-mcp | Backend (FastAPI + FastMCP SSE; path `/mcp`) |
| 10910 | rtorrent-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`) |
| 10911 | rtorrent-mcp | Frontend (Vite dev; proxies `/api` + `/mcp` → 10910) |
| 10912 | gtfs-mcp | Web dashboard frontend (Vite) |
| 10913 | gtfs-mcp | Backend (FastAPI + MCP HTTP `/mcp`) |
| 10922 | vienna-life-assistant | ViLife backend + MCP HTTP `/mcp` (carrier — do not assign to gtfs-mcp) |
| 10924 | kyutai-mcp | Web dashboard backend (FastAPI) |
| 10925 | kyutai-mcp | Web dashboard frontend (Vite) |
| 10926 | kyutai-mcp | MCP HTTP `/mcp` |
| 10927 | lewm-mcp | FastAPI + MCP HTTP `/mcp` (LeWorldModel bridge) |
| 10928 | lewm-mcp | Vite dashboard (glass UI) |
| 10930 | songgeneration-mcp | SongGeneration-Studio default local API/UI target |
| 10932 | openclaude-mcp | MCP SSE backend (FastMCP 3.2) + REST bridge (`/tools/{name}`) |
| 10933 | openclaude-mcp | React webapp (Vite) |
| 10934 | jellyfin-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + WebSocket `/ws`) |
| 10935 | jellyfin-mcp | Frontend (Vite / Next.js dev; proxies `/api` → 10934) |
| 10936 | oscilloscope-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; USB scope bridge) |
| 10937 | oscilloscope-mcp | Frontend (Vite React; waveform viewer; proxies `/api` → 10936) |
| 10938 | arr-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; Sonarr/Radarr/Lidarr/Readarr/Prowlarr/Overseerr/Bazarr) |
| 10939 | arr-mcp | Frontend (Vite React dashboard; cross-arr stats + search) |
| 10940 | alsergrund-bridge | Backend (FastMCP) |
| 10941 | alsergrund-bridge | Frontend (Vite) |
| 10942 | ednaficator | Backend (Starlette + uvicorn) |
| 10943 | ednaficator | Frontend (Vite / React) |
| 10946 | aiwatcher-mcp | Backend (Starlette + FastMCP ASGI, `/mcp`) |
| 10947 | aiwatcher-mcp | Frontend (Vite / React) |
| 10944 | freecad-mcp | Backend (FastAPI + FastMCP ASGI, REST + MCP `/sse`) |
| 10945 | freecad-mcp | Frontend (Vite / React) |
| 10948 | goose-mcp | Backend (Starlette + FastMCP ASGI, `/mcp`) |
| 10949 | goose-mcp | Frontend (Vite / React) |
| 10950 | opencode-cli-mcp | Frontend (Vite, proxies /api → 10951) |
| 10951 | opencode-cli-mcp | Backend (FastAPI + REST bridge) |
| 10952 | telephony-mcp | Web dashboard backend (Starlette, audit log API) |
| 10953 | telephony-mcp | Web dashboard frontend (Vite React) |
| 10956 | deepfang | Supervisor API + MCP SSE (FastMCP 3.2) |
| 10957 | deepfang | React dashboard |
| 10958 | deepfang | Sanitizer shim (custom Python/FastAPI) |
| 10959 | deepfang | DeepSeek adjudicator bridge |
| 10960 | deepfang | Air-gapped worker (Docker internal network) |
| 10961 | deepfang | Prometheus metrics |
| 10962 | deepfang | Loki log aggregation |
| 10963 | deepfang | Grafana observability |
| 10964 | tvtropes-mcp | MCP SSE + REST API (FastMCP 3.2) |
| 10965 | tvtropes-mcp | React dashboard (scraper status + trope search) |
| 10966 | qcad-mcp | Backend (FastAPI + FastMCP ASGI, REST + MCP `/sse`) |
| 10967 | qcad-mcp | Frontend (Vite / React) |
| 10968 | kick-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 10969 | kick-mcp | Frontend (Vite; future dashboard) |
| 10970 | colony-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 10971 | colony-mcp | Frontend (Vite / React glass dashboard) |
| 10954 | copy-fail-mcp | Web dashboard frontend (Vite) |
| 10955 | copy-fail-mcp | Backend (FastMCP MCP HTTP) |
| 10972 | hermes-agent | Hermes WebUI (fleet conductor agent dashboard) |
| 10973 | hermes-agent | (reserved — future Hermes service) |
| 10974 | chitchat | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 10975 | chitchat | Frontend (Vite / React) |
| 10976 | uitars-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 10977 | uitars-mcp | Frontend (Vite dev; proxies `/api` + `/mcp` → 10976) |
| 10978 | resonite-mcp | Web dashboard frontend (Vite) |
| 10979 | resonite-mcp | Backend (FastAPI + MCP HTTP) |
| 10980 | nuki-mcp | Web dashboard |
| 10981 | libreoffice-mcp | Backend (FastMCP 3.2 HTTP `/mcp`; headless convert + extension bridge). **Host:** LibreOffice `soffice` — fleet-tested **26.2.3.2** at `C:\Program Files\LibreOffice\program\soffice.exe` |
| 10982 | universal-actuator-mcp | Web dashboard (Vite) |
| 10983 | libreoffice-mcp | Frontend (Vite webapp — template gallery, job queue, PDF preview) |
| 10984 | wall-flower | Web dashboard (Vite) |
| 10985 | logic-analyzer-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; sigrok + simulator LA bridge) |
| 10986 | games-app | Web dashboard (Vite) |
| 10987 | games-app | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`) |
| 10988 | logic-analyzer-mcp | Frontend (Vite React; trace + decode viewers; proxies `/api` → 10985) |
| 10989 | vienna-life-assistant | Web dashboard (Vite) |
| 10990 | gazebo-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 10991) |
| 10991 | gazebo-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; general-purpose Gazebo sim server) |
| 10992 | godot-mcp | Web dashboard frontend (Vite) |
| 10993 | godot-mcp | Backend (FastAPI + FastMCP TCP bridge) |
| 10994 | streamfog-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`) |
| 10995 | streamfog-mcp | Frontend (Vite React dashboard; proxies `/api` → 10994) |
| 10996 | fleet-agent-mcp | Backend (FastMCP 3.2 HTTP `/mcp`) |
| 10997 | fleet-agent-mcp | Frontend (reserved for future React dashboard) |
| 11027 | fleet-intel-reports | Intel Reports Hub — Fritz + AIWatcher HTML (`fleet-agent-mcp/scripts/start-intel-hub.ps1`; iPad / Tailscale). Pattern: `patterns/intel-reports-hub.md` |
| 10998 | scraper-mcp | Backend (FastAPI + FastMCP 3.2, REST `/api/*` + MCP `/mcp`; includes toolbench-mcp archiver) |
| 10999 | scraper-mcp | Frontend (Vite React dashboard; proxies `/api` → 10998) |
| 11000 | cursor-mcp | Backend (FastMCP 3.2 HTTP `/mcp`; Cursor platform API — usage/spend guardrails, cloud agents) |
| 11010 | grandorgue-mcp | Backend (FastMCP 3.2 + FastAPI, REST `/api/*` + MCP `/mcp` + WebSocket `/ws`) |
| 11011 | grandorgue-mcp | Frontend (Vite React console; proxies `/api` + `/health` + `/ws` → 11010) |
| 11012 | tahoma2d-mcp | Frontend (Vite dev; proxies `/api` + `/mcp` → 11013) |
| 11013 | tahoma2d-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; Tahoma2D bridge) |
| 11014 | google-ai-mcp | Backend (FastAPI + FastMCP 3.2 HTTP `/mcp` + REST `/api/*`; Gemini Chat, Nano Banana image, Veo video, Lyria music, TTS, Embeddings) |
| 11015 | google-ai-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11014) |
| 11016 | kicad-mcp | Backend (FastAPI + FastMCP HTTP/SSE `/mcp` + REST `/api/*`; hybrid stable CLI + IPC CRUD) |
| 11017 | kicad-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11016) |
| 11018 | kicad-mcp | KiCad TCP bridge (legacy; kc_bridge.py ↔ pcbnew GUI) — fallback when 11 nightly IPC unavailable |
| 11020 | steam-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`; Steam Web API bridge) |
| 11021 | steam-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11020) |
| 11022 | chip-design-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`; EDA orchestration) |
| 11023 | chip-design-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11022) |
| 11024 | vla-mcp | Backend (FastAPI + FastMCP HTTP `/mcp` + REST `/api/*`; VLA / wall-x bridge) |
| 11025 | vla-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11024) |
| 11028 | inkscape-mcp | Backend (FastAPI `/api/health`; moved off **10900** audiotool conflict) |
| 11029 | inkscape-mcp | Frontend (Vite; proxies `/api` + `/mcp` → 11028) |
| 11030 | fleet | Per-repo **just** recipe UI (`mcp-central-docs/scripts/just-dashboard.ps1`; `just just-ui`) |
| 11031 | mcp-central-docs | Fleet **just** dashboard (`scripts/fleet-dashboard.ps1`; `just dashboard`) |
| 11032 | documentation-mcp | Public docs hub frontend (Vite; proxies `/api` → 11033) |
| 11033 | documentation-mcp | Public docs hub backend (REST `/api/*` + MCP streamable HTTP `/mcp`) |
| 11001 | function-generator-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; AWG bridge) |
| 11002 | function-generator-mcp | Frontend (Vite; planned) |
| 11003 | power-supply-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; bench PSU) |
| 11004 | power-supply-mcp | Frontend (Vite; planned) |
| 11005 | multimeter-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; DMM bridge) |
| 11006 | multimeter-mcp | Frontend (Vite; planned) |
| 11007 | spectrum-analyzer-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; RTL-SDR/TinySA) |
| 11008 | spectrum-analyzer-mcp | Frontend (Vite; planned) |
| 11009 | jtag-swd-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; OpenOCD) |
| 11019 | jtag-swd-mcp | Frontend (Vite; planned) |
| 11034 | bus-pirate-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`) |
| 11035 | bus-pirate-mcp | Frontend (Vite; planned) |
| 11036 | bench-orchestrator-mcp | Backend (workflow glue across bench MCPs) |
| 11037 | bench-orchestrator-mcp | Frontend (Vite; planned) |
| 11038 | test-fixture-mcp | Backend (YAML test sequences) |
| 11039 | test-fixture-mcp | Frontend (Vite; planned) |
| 11040 | smoke-detector-mcp | Backend (Nest/bench safety alerts) |
| 11041 | smoke-detector-mcp | Frontend (Vite; planned) |
| 11042 | bench-camera-mcp | Backend (USB webcam snapshots) |
| 11043 | bench-camera-mcp | Frontend (Vite; planned) |
| 11044 | limx-robotics-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; MuJoCo sim lifecycle + VLA bridge) |
| 11045 | limx-robotics-mcp | Frontend (Vite React dashboard; sim jobs, robot variants, fleet export) |
| 11046 | mujoco-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; general-purpose MuJoCo sim server) |
| 11047 | mujoco-mcp | Frontend (Vite React dashboard; model depot, sim control, state browser) |
| 11048 | isaac-mcp | Frontend (Vite React dashboard; proxies `/api` + `/mcp` → 11049) |
| 11049 | isaac-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; NVIDIA Isaac Sim/Lab simulation server) |
| 11050 | ros-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; ROS 2 bridge — topics, services, params, bags, launch) |
| 11051 | ros-mcp | Frontend (Vite React dashboard; topic browser, service caller, node graph) |
| 11052 | unitree-mcp | Backend (FastAPI + FastMCP HTTP `/mcp`; MuJoCo sim lifecycle + ROS 2 bridge) |
| 11053 | unitree-mcp | Frontend (Vite React dashboard; robot models, sim control, fleet export) |
| 11054 | ittybitty (videogen-mcp) | Backend (FastAPI + FastMCP HTTP `/mcp`; topic → narrated video pipeline) |
| 11055 | ittybitty (videogen-mcp) | Frontend (Vite dev; static dist placeholder until storyboard editor) |
| 11056 | giskard-mcp | Backend (Starlette + FastMCP HTTP `/mcp`; Giskard red-team scanning) |
| 11057 | giskard-mcp | Frontend (Vite React dashboard; scan history + report viewer) |
| 11060 | tailscale-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11061 | worldlabs-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11062 | inkscape-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11063 | fastsearch-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11064 | davinci-resolve-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11065 | beyondcompare-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11066 | system-admin-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11067 | winrar-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11068 | rustdesk-mcp | Logging backend (FastAPI; ring-buffer log query, stats, export, clear) |
| 11700 | myai | dashboard container (Starlette/Flask, internal :11700) |
| 11701 | myai | traefik reverse proxy (HTTP, internal :80) |
| 11702 | myai | traefik dashboard (internal :8080) |
| 11703 | myai | weaviate vector DB (internal :8080) |

## Unified observability stack (Docker)

**mcp-central-docs/monitoring** — one Grafana/Loki/Prometheus for the fleet. Host bindings use **12000–12010** so they do not collide with per-repo stacks on 3000/9090/3100 or the webapp reservoir.

| Port | Service |
|------|---------|
| 12000 | unified-grafana (container :3000) |
| 12001 | unified-prometheus (container :9090) |
| 12002 | unified-loki (container :3100) |
| 12003 | unified-promtail (container :9080) |
| 12004 | unified-node-exporter (container :9100) |
| 12005 | unified-cadvisor (container :8080) |
| 12006 | unified-blackbox (container :9115) |
| 12007 | observability-mcp | MCP HTTP backend (`/mcp`) |
| 12008 | observability-mcp | Web dashboard frontend (Vite) |
| 12009 | observability-mcp | Process `/metrics` exporter (`PROMETHEUS_PORT`) |
| 12010 | mcp-central-docs | RebootX On-Prem (mobile monitoring, Go build from source) |
| 12011 | mcp-central-docs | RebootX Swagger UI (API explorer) |

Override via `monitoring/.env` (see `monitoring/.env.example`). Fleet scrape targets: `monitoring/prometheus.fleet.yml` + `CONNECT_TO_UNIFIED_MONITORING.md`.

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
# start.ps1 pattern — SOTA 2026
param([switch]$Headless, [switch]$BackendOnly, [switch]$NoBrowser)
$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $PSCommandPath
$BackendPort = 10700   # YOUR port from registry (backend)
$FrontendPort = 10701  # YOUR port from registry (frontend)

# Port zombie clearing
Get-NetTCPConnection -LocalPort $BackendPort -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
Get-NetTCPConnection -LocalPort $FrontendPort -ErrorAction SilentlyContinue |
    ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }

# Start backend via Start-Job with proper working directory
$BackendJob = Start-Job -Name "backend" -ScriptBlock {
    param($Root, $Port)
    Set-Location $Root
    uv run python -m my_package.server --port $Port
} -ArgumentList $ScriptRoot, $BackendPort

# Readiness poll
for ($i = 0; $i -lt 60; $i++) {
    try { $r = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/health" -TimeoutSec 2 -UseBasicParsing -ErrorAction SilentlyContinue
          if ($r.StatusCode -eq 200) { break } } catch {}
    Start-Sleep 1
}

# Start frontend via Start-Process with -WorkingDirectory
$WebRoot = Join-Path $ScriptRoot "webapp"
Start-Process -NoNewWindow -FilePath "npx" -ArgumentList "vite --port $FrontendPort --host" -WorkingDirectory $WebRoot

# Auto-open browser
Start-Process "http://127.0.0.1:$FrontendPort"

# Keep-alive
while ($true) {
    if ($BackendJob.State -eq "Completed" -or $BackendJob.State -eq "Failed") {
        Receive-Job $BackendJob; break
    }
    Start-Sleep 2
}
```

```bat
@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0start.ps1"
```
