# libreoffice-mcp — Fleet LibreOffice Automation



> **Status: 0.1.0** — Phase 0–3 complete: headless convert, ODT merge, batch pack, webapp with PDF preview.



**Source repo:** `D:\Dev\repos\libreoffice-mcp`

**Ports:** **10981** (FastMCP HTTP `/mcp` + REST) · **10983** (Vite webapp)

**Stack:** FastMCP 3.2 · headless `soffice` **26.2.3.2+** · optional bridge to extension MCP on **8765**

**Changelog:** repo [CHANGELOG.md](https://github.com/sandraschi/libreoffice-mcp/blob/main/CHANGELOG.md) · [MCD mirror](./CHANGELOG.md)

---

## Host prerequisite — LibreOffice

libreoffice-mcp shells out to **`soffice --headless`**. Install LibreOffice on the host before starting convert/merge jobs.

| Platform | Default path | Fleet-tested |
|----------|--------------|--------------|
| Windows | `C:\Program Files\LibreOffice\program\soffice.exe` | **26.2.3.2** (2026-05-30) |
| Override | `LIBREOFFICE_MCP_SOFFICE_PATH` | Custom install path |

Verify: `libreoffice(operation='status')` or `GET http://127.0.0.1:10981/api/health`.

### GUI verification (pywinauto-mcp)

Headless convert does not exercise the Calc/Writer UI tree. For **Cua-shaped** live-window loops (`get_window_state`, `snapshot_id`, `element_index`), use **[pywinauto-mcp](../pywinauto-mcp/README.md)** e2e: `pytest -m e2e` in that repo (launches `--calc`, requires the same `soffice` install). See [CUA_DRIVER_AND_PYWINAUTO.md](../../patterns/CUA_DRIVER_AND_PYWINAUTO.md).

---

## Start (MCD launchers)

| Launcher | What |
|----------|------|
| [starts/libreoffice-mcp-start.bat](../../starts/libreoffice-mcp-start.bat) | `webapp/start.bat` — backend **10981** + dashboard **10983** + browser |
| [just-starts/libreoffice-mcp-just.bat](../../just-starts/libreoffice-mcp-just.bat) | Same |
| Repo | `webapp\start.bat` or root `start.bat` (delegates to webapp) |

Included in [just-starts/start-all.ps1](../../just-starts/start-all.ps1) (after `fleet-agent-mcp`).

---



## Phase plan



| Phase | Deliverable | Status |

|-------|-------------|--------|

| **0** | `convert`, `bridge_*`, fleet_bridge alias | **Done** |

| **1** | REST job queue + SOTA webapp :10983 (Tailwind, sidebar, Tools/Status/Help) | **Done** |

| **2** | ODT template merge (`merge`, bundled templates v2) | **Done** |

| **3** | Fritz coworker PDF flows (weekly, board, artifact) | **Done** |



---



## MCP surface



Portmanteau tool: **`libreoffice`**



| Operation | Description |

|-----------|-------------|

| `status` | `soffice` path + extension bridge online |

| `convert` | Headless convert; `.md` → HTML → PDF |

| `merge` | ODT `{{PLACEHOLDER}}` merge → pdf/odt |

| `list_templates` | Bundled + custom templates |

| `batch_pack` | Multi-file artifact pack → single PDF |

| `bridge_discover` | List tools on extension MCP (:8765) |

| `bridge_call` | Proxy to extension (live Writer/Calc edit) |

| `help` | Ops list + REST routes |



### Bundled templates (v2 styles)



Writer styles: DocTitle, DocMeta, SectionHeading, BodyText; A4 margins. Version tracked in `~/.libreoffice-mcp/templates/.builtin-version`.



| Template | Placeholders | Coworker flow |

|----------|--------------|---------------|

| `fleet-report.odt` | TITLE, DATE, SUMMARY, BODY | `coworker_weekly_report_pdf` (Fri 17:00) |

| `fleet-board-pack.odt` | TITLE, DATE, KPI_TABLE, NARRATIVE, ACTION_ITEMS | `coworker_board_pack` (monthly `d1:09:00`) |

| `fleet-artifact-pack.odt` | TITLE, DATE, FILE_LIST, SUMMARY | `coworker_artifact_pack` (Sun 18:00) |



Stored in `~/.libreoffice-mcp/templates/` (seeded on first run).



---



## REST API (webapp)



| Endpoint | Purpose |

|----------|---------|

| `GET /api/templates` | Template gallery |

| `POST /api/merge` | Merge + convert |

| `POST /api/pack` | Batch artifact pack |

| `POST /api/convert` | Headless convert job |

| `GET /api/output/file/{name}` | PDF/HTML preview |

| `GET /api/jobs` | Convert job queue |



Registry: [webapp-registry.json](../../operations/webapp-registry.json) · [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — `libreoffice-mcp-backend` / `libreoffice-mcp-frontend`.



---



## Fritz coworker integration



| Flow | MCP tool | libreoffice op |

|------|----------|----------------|

| Weekly report PDF | `coworker_weekly_report_pdf` | `merge` → `fleet-report.odt` |

| Monthly board pack | `coworker_board_pack` | `merge` → `fleet-board-pack.odt` |

| Weekly artifact pack | `coworker_artifact_pack` | `batch_pack` + `fleet-artifact-pack.odt` |



Delivery: Fritz `notify_email` with PDF attachment via fleet_bridge alias `libreoffice` (:10981).



See [fritz-coworker](../fritz-coworker/README.md) · [fleet-agent-mcp](../fleet-agent-mcp.md).



---



*Tags: #libreoffice #office #foss #mcp #fleet #fritz #coworker*

