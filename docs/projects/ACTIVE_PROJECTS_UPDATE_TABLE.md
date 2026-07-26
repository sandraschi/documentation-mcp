# Active Projects — Doc Update Priority Table

**Purpose:** Scoped refresh list for public `sandraschi-collected-docs` — **active** fleet repos, **advanced/innovative** first.  
**Not in scope yet:** `meta_mcp` `update_doc_repository` agentic tool — manual/table-driven pass.  
**Bar:** [JUNE_2026_STANDARDS_BAR.md](../standards/JUNE_2026_STANDARDS_BAR.md) · [PUBLISH_UPDATE_CHECKLIST.md](../PUBLISH_UPDATE_CHECKLIST.md)  
**Last updated:** 2026-06-17

---

## Priority key

| Priority | Meaning |
|----------|---------|
| **P0** | Active + innovative — publish showcase; update before public cut |
| **P1** | Active production — refresh ports, 3.2+, MCPB; no DXT |
| **P2** | Active but stable / lower churn — header + cross-links only |
| **Defer** | Planned, scaffold, or design-only — honest STATUS, not full rewrite |

## Freshness key

| Tag | Meaning |
|-----|---------|
| 🟢 | Touched June 2026 or repo-synced ≤30d |
| 🟡 | Exists but stale (3.1 min, old model names, DXT refs) |
| 🔴 | Stub, missing, or mirror doc wrong |

---

## P0 — Advanced & innovative (update first)

| Project | Innovation / why active | MCD path | Ports | Fresh | Gaps | Update actions |
|---------|-------------------------|----------|-------|-------|------|----------------|
| **diffusion-llm-mcp** | dLLM paradigm slot; HLE routing; Goliath | `projects/diffusion-llm-mcp/` | 10834/10835 | 🔴 | Stub only | Expand from fleet repo `docs/`; link `diffusiongemma/` |
| **diffusiongemma** | Anti-saturation eval; catch-them-all assessment | `projects/diffusiongemma/` | — | 🟢 | No code repo section | Add Phase 1 smoke status when run |
| **local-llm-mcp** | AR incumbent; pairs with dLLM | `projects/local-llm-mcp/` | 10832/10833 | 🟢 | — | Updated June 2026: VLLMv1Provider fix, dashboard rewrite, fresh docs |
| **meta_mcp** | Fleet orchestrator, probes, repo inspiration | `projects/meta_mcp/` | 10718/10719 | 🟢 | `update_doc_repository` not built | Sync from repo CHANGELOG; ports verified |
| **fleet-agent-mcp** | Self-evolving agent; Fritz coworker | `projects/fleet-agent-mcp.md` | 10996/10997, Intel 11027 | 🟡 | Single `.md` not folder | Folder + STATUS; link fritz-coworker |
| **fritz-coworker** | Poor Man's Viktor; pulses, Intel Hub | `projects/fritz-coworker/` | 11027 | 🟡 | Pilot vs prod unclear in index | June 2026 pilot status; device watch flows |
| **federation-mcp** | MCP mesh hub; encrypted peer links | `projects/federation-mcp/` | 10856/10857 | 🟡 | Verify vs `mcp-federation-hub` repo | PEERS_AND_MESH summary; 3.2+ |
| **robotics-mcp** | Physical + virtual robotics composite | `projects/robotics-mcp/` | (composite) | 🟡 | "XMas 2025" hardware note aged | Yahboom/teleoperator cross-links; 3.2+ |
| **yahboom-mcp** | ROS2 Pi5 embodied baseline | `projects/yahboom-mcp/` | 10892/10893 | 🟡 | — | Align [YAHBOOM_ROBOTICS_STANDARD](../standards/YAHBOOM_ROBOTICS_STANDARD.md) |
| **teleoperator-mcp** | WebXR → physical robot bridge | `projects/teleoperator-mcp/` | 10900/10901 | 🟡 | M1 status | Pico/Quest path; safety preflight |
| **bumi-mcp** | Humanoid virtual twin | `projects/bumi-mcp/` | 10774/10775 | 🟡 | 3.1 badge | 3.2+; Noetix integration current |
| **uitars-mcp** | VLM desktop agent; 4090-sized | `projects/uitars-mcp/` | 10976/10977 | 🟢 | — | vs windows-computer-use comparison table |
| **windows-computer-use-mcp** | CUA / UIA automation; certified | `projects/windows-computer-use-mcp/` | 10789 area | 🟢 | Safety stack verbose | CUA parity roadmap one-pager; no DXT |
| **tauri-cua-nsis** | Certified desktop ship path | `projects/tauri-cua-nsis/` | — | 🟢 | Screenshot bloat | Slim cert artifacts per WEED_MANIFEST |
| **openmanus-mcp** | FOSS Manus-class; local LLM | `projects/openmanus-mcp/` | 10768/10769 | 🟡 | 3.1; safety essay long | 3.2+; sampling + pywinauto risk summary |
| **reversing-mcp** | Ghidra bridge; DKI mission | `projects/reversing-mcp/` | 10750/10751 | 🟡 | — | ReVa separation; Frida link |
| **chip-design-mcp** | RTL→GDSII open ASIC pipeline | `projects/chip-design-mcp/` | 11022/11023 | 🟢 | Private GH link | Public-safe description; standard link |
| **lewm-mcp** | JEPA world model bridge | `projects/lewm-mcp/` | 10927/10928 | 🟡 | — | Sync `integrations/lewm-mcp.md`; arxiv ingest |
| **cursor-mcp** | Cloud agent spend guardrails | `projects/cursor-mcp/` | 11000 | 🟡 | — | Cursor 3.x / cloud agents Jun 2026 |
| **robofang** | Fleet control plane supervisor | `projects/robofang/` | 10870–10872 | 🟡 | Mirror `mcp-servers/*.md` stale | Refresh mirror docs or mark secondary |
| **aiwatcher-mcp** | AI news → Intel Hub ingest | `projects/aiwatcher-mcp/` | 10946/10947 | 🟡 | — | Digest publish flow; meta_mcp handoff |
| **discord-mcp** | Agentic Discord bridge 2026 | `projects/discord-mcp/` | 10756/10757 | 🟡 | — | 3.2+ confirmed; skills list |
| **ittybitty** (videogen-mcp) | AI narrated video MVP | `projects/ittybitty/` | 11054/11055 | 🟢 | — | Tauri ship status |
| **dark-app-factory** | Generative software factory | `projects/dark-app-factory/` | 8001/8002 | 🟡 | — | DTU + council; 2026 standards |

---

## P1 — Active production (second wave)

| Project | Role | MCD path | Ports | Fresh | Update actions |
|---------|------|----------|-------|-------|----------------|
| **calibre-mcp** | Library RAG + FTS + Tauri NSIS | `projects/calibre-mcp/` | 10720/10721 | 🟢 | NSIS production-ready Jun 2026 |
| **plex-mcp** / **plexmcp** | Media server MCP | `projects/plex-mcp/`, `plexmcp/` | 10740/10741 | 🟡 | Dedupe two folders? 3.2+ |
| **devices-mcp** | IoT + Fritz priority API | `projects/devices-mcp/` | 10717 | 🟢 | Tauri desktop note |
| **virtualization-mcp** | Sandbox isolation | `projects/virtualization-mcp/` | 10700/10701 | 🟡 | 3.2+; naked-install |
| **arxiv-mcp** | Research MCP + dashboard | `projects/arxiv-mcp/` or index link | 10770/10771 | 🟡 | lewm paper ingest cross-link |
| **notebooklm-fleet-mcp** | NotebookLM wrapper | `projects/notebooklm-fleet-mcp/` | 10783/10784 | 🟡 | `nlm` CLI version |
| **tailscale-mcp** | Tailnet admin | `projects/tailscale-mcp/` | (see PRD) | 🟡 | Partner tailnets |
| **dreame-mcp** | LIDAR vacuum map | `projects/dreame-mcp/` | 10894/10895 | 🟡 | — |
| **autohotkey-mcp** | Scriptlets MCP | `projects/autohotkey-mcp/` | 10747 | 🟡 | 3.2+ |
| **godot-mcp** | Indie game ship | `projects/godot-mcp/` | +9080 bridge | 🟡 | itch/steam cross-links |
| **steam-mcp** | Steam portmanteau | `projects/steam-mcp/` | 11020/11021 | 🟡 | — |
| **games-app** | Tauri games + AI engines | `projects/games-app/` | (see repo) | 🟡 | 3.2+ badge |
| **mcp-studio** | Mission control UI | `projects/mcp-studio/` | — | 🟡 | vs meta_mcp roles |
| **openclaw** | Personal assistant gateway | `projects/openclaw/` | — | 🟡 | Feb 2026 security audit ref |
| **agy-fleet-mcp** | Antigravity config sync | `projects/agy-fleet-mcp/` | 10825 | 🟡 | Tool budget ~50 |
| **glance-mcp** | RSS + fleet probes | `projects/glance-mcp/` | 10776/10777 | 🟡 | 3.2+ |
| **chitchat** | Conversation archive MCP | `projects/chitchat/` | 10974/10975 | 🟡 | — |
| **libreoffice-mcp** | Headless office for Fritz | `projects/libreoffice-mcp/` | 10981/10983 | 🟡 | CUA verification path |
| **reaper-mcp** / **virtualdj-mcp** | DJ/media composite inputs | `projects/*/` | — | 🟡 | ai-producer-hub links |
| **unity3d-mcp** / **resonite-mcp** / **vrchat-mcp** | Social VR stack | `projects/*/` | — | 🟡 | robotics-webapp mesh |
| **ring-mcp** / **home-assistant-mcp** | Home IoT | `projects/*/` | 10728+, 10796+ | 🟡 | WebRTC notes |

---

## P2 — Light touch (header + links)

Stable production MCPs with infrequent churn: **obs-mcp**, **nest-protect-mcp**, **nest-***, **notion-mcp**, **obsidian-mcp**, **xkcd-mcp**, **mywienerlinien**, **veogen**, **myai**, **dj-media-hub**, **ai-producer-hub**, **getbooks-mcp** (planned banner only).

**Action:** `Last Updated: 2026-06-17`, ports, 3.2+ if cited, remove any DXT install blocks.

---

## Defer (honest stub only)

| Project | Why defer | MCD action |
|---------|-----------|------------|
| **antigravity-cli-mcp** | Design only | Keep planned banner |
| **getbooks-mcp** | Design only | — |
| **fleet-cold-install** | Scaffold program | TODO honest |
| **apple/CalFolio** | Pre-scaffold | — |
| **directmedia-mcp** | No folder; index row only | Create minimal README or fix index |
| **arxiv-mcp** | If no `projects/arxiv-mcp/` folder | Add stub from index |

---

## Integration pages tied to P0 (update with projects)

| Integration doc | Tied P0 project |
|-----------------|-----------------|
| [integrations/lewm-mcp.md](../integrations/lewm-mcp.md) | lewm-mcp |
| [integrations/openmanus.md](../integrations/openmanus.md) | openmanus-mcp |
| [integrations/cursor-ide/](../integrations/cursor-ide/) | cursor-mcp |
| [integrations/local-llm/](../integrations/local-llm/) | local-llm-mcp, diffusion-llm-mcp |
| [integrations/zed/](../integrations/zed/) | Dev toolchain |
| [integrations/gemini-deep-research-interactions-2026.md](../integrations/gemini-deep-research-interactions-2026.md) | aiwatcher, google-ai-mcp |
| [integrations/agentmemory.md](../integrations/agentmemory.md) | fleet-agent, openmanus |
| [integrations/blender-mcp.md](../integrations/blender-mcp.md) | robotics / media |
| [integrations/yahboom/](../integrations/yahboom/) | yahboom-mcp, teleoperator |

---

## Suggested work order (no meta_mcp automation)

1. **P0 inference pair:** diffusion-llm-mcp + local-llm-mcp + `integrations/local-llm/`
2. **P0 control plane:** meta_mcp + robofang + federation-mcp
3. **P0 embodied:** robotics-mcp → yahboom → teleoperator → bumi
4. **P0 agentic risk:** openmanus-mcp + windows-computer-use-mcp + uitars-mcp
5. **P0 deep tech:** reversing-mcp + chip-design-mcp + lewm-mcp
6. **P0 narrative:** diffusiongemma (already 🟢) + AI section models addendum
7. **P1 wave** in portfolio clusters (media, home, research)

---

## Future: `meta_mcp` `update_doc_repository`

Tempting — **not yet.** When added, point it at this table's P0 rows + live repo `CHANGELOG`/`README`/`glama.json` — not the full ~155 tree.

---

*Full fleet index:* [projects/README.md](./README.md)
