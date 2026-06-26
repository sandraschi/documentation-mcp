# teleoperator-mcp — fleet index



**Source repo:** `D:\Dev\repos\teleoperator-mcp`  

**Status:** Active · Milestone 1 (Boomy + Pico/Quest WebXR) · **Virtual twins** (vBoomy / Resonite) in progress  

**Role:** First fleet project that makes the Pico 4 worth powering on — VR teleop to Yahboom Raspbot v2 **or Resonite vBot** via browser, no native headset app.



**Last updated:** 2026-06-04



---



## One-line summary



Thin gateway: **WebXR webapp on the headset** (pose @ 30 Hz over WebSocket) + **MCP on Goliath** (session config, status — not on the hot path) + **yahboom-mcp** downstream to Boomy + **LiveKit** video return (separate pipe, port 15580).



---



## Ports (Goliath)



| Port | Service |

|------|---------|

| **10900** | Vite webapp — SOTA Iron Shell (React) + WebXR entry |

| **10901** | FastAPI backend + WebSocket `/ws/teleop` + `/api/logs` |

| **10892** | yahboom-mcp (robot REST) |

| **15580** | myconf LiveKit SFU (headset WebRTC video) |



**Start (fleet standard):** `webapp\start.bat` or `webapp\start.bat -WithTailscaleServe`  

**Pico M1 detached:** `scripts\m1-up.ps1`



After backend up, start video publisher (once per session):



```powershell

Invoke-RestMethod -Method Post http://127.0.0.1:10901/api/v1/livekit/publisher/start

```



Or webapp **Tools → teleop_livekit_publisher_start → Dry run**.



---



## Webapp (SOTA 2026-06)



Fleet [WEBAPP_STANDARDS](../../standards/WEBAPP_STANDARDS.md) compliant:



| Route | Purpose |

|-------|---------|

| `/` (Home) | Health dashboard, Enter VR |

| `/tools` | MCP dry-run inspector |

| `/logs` | Event log tail + export |

| `/apps` | Fleet discovery |

| `/settings` | Local LLM glom-on |

| `/help` | Pico / teleop quick start |



API: `GET /api/capabilities`, `GET /api/logs*`. Launcher: `webapp/start.ps1` (Windows `cmd /c npm` fix).

**CI:** GitHub Actions on `windows-latest` — `pytest` + `npm run check` (see repo `.github/workflows/ci.yml`).



---



## Pico 4 path



1. Sideload **Tailscale** — [pico-tailscale-setup](../../pico-tailscale-setup/)

2. Goliath: `webapp\start.bat -WithTailscaleServe`

3. Sign in on Pico with **same Microsoft account as Goliath**

4. Pico Browser → `https://goliath.<tailnet>.ts.net/` → **Enter VR**



**MCD docs:** [pico/WEBXR.md](../pico/WEBXR.md) · [pico/REVIVE_CHECKLIST.md](../pico/REVIVE_CHECKLIST.md)



---



## Upstream documentation



| Doc | Topic |

|-----|-------|

| [CHANGELOG.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/CHANGELOG.md) | Release notes (2026-06-04 SOTA webapp) |

| [LIVEKIT.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/LIVEKIT.md) | Video pipe + STUN troubleshooting |

| [TAILSCALE_VIEWERS.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/TAILSCALE_VIEWERS.md) | Headset VPN pitfalls |

| [PRD.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/PRD.md) | Requirements |

| [ARCHITECTURE.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/ARCHITECTURE.md) | System design |

| [WEBXR.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/WEBXR.md) | Client stack (in-repo) |

| [HTTPS.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/HTTPS.md) | Tailscale Serve |

| [BRINGUP.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/BRINGUP.md) | M1 bench checklist |

| [DUAL_MODE_ARCHITECTURE.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/DUAL_MODE_ARCHITECTURE.md) | Long-term telesupervision |

| [TODO.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/TODO.md) | Milestones |

| [VIRTUAL_TWINS_FLEET.md](VIRTUAL_TWINS_FLEET.md) | **Cross-repo** vBot + LeRobot fleet index |

| [LEROBOT.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/LEROBOT.md) | JSONL capture + parquet export |

| [VIRTUAL_TWINS.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/VIRTUAL_TWINS.md) | vBoomy / Resonite loop |

| [VBOT_CREATIVE_TWINS.md](https://github.com/sandraschi/teleoperator-mcp/blob/main/docs/VBOT_CREATIVE_TWINS.md) | Mechazilla, kaiju, creative vBots |



Local paths mirror upstream under `teleoperator-mcp/docs/`.



---



## Fleet integrations



| Project | Link |

|---------|------|

| yahboom-mcp | [../yahboom-mcp/README.md](../yahboom-mcp/README.md) |

| robotics-mcp | [../robotics-mcp/README.md](../robotics-mcp/README.md) — vbot OSC gateway |

| resonite-mcp | [../resonite-mcp/README.md](../resonite-mcp/README.md) — ProtoFlux receiver |

| bumi-mcp | [../bumi-mcp/README.md](../bumi-mcp/README.md) |

| tailscale-mcp | [../tailscale-mcp/README.md](../tailscale-mcp/README.md) |

| Pico 4 hub | [../pico/README.md](../pico/README.md) |

| myconf LiveKit | `D:\Dev\repos\myconf` (port 15580) |

| Robotics standard | [../../standards/YAHBOOM_ROBOTICS_STANDARD.md](../../standards/YAHBOOM_ROBOTICS_STANDARD.md) |



---



## Live URL (Sandras lab)



`https://goliath.tailfab45.ts.net/` — confirm with `tailscale serve status` on Goliath.



**2026-06-04 bench:** LiveKit STUN config fixed in myconf; publisher verified on Goliath; Pico tailnet + first VR session in progress (drive pending Boomy ROS).

