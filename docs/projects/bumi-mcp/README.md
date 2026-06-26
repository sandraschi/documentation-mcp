# bumi-mcp — Noetix Bumi humanoid (fleet MCP)

**Central project documentation** for **bumi-mcp**.

**Canonical source repo:** [github.com/sandraschi/bumi-mcp](https://github.com/sandraschi/bumi-mcp) · **Local clone:** `D:/Dev/repos/bumi-mcp`

**Ports:** **10774** (FastAPI + MCP `/mcp`) · **10775** (Vite dashboard)

---

## What it does

- **FastMCP 3.1+**: `bumi(operation=...)`, `bumi_agentic_workflow`, prompt `bumi_quick_start`, skills provider.
- **Hero product data** for **Noetix Bumi** + pointers to **Noetix-Robotics** OSS repos.
- **Optional** `BUMI_ROBOT_URL` — `robot_status` probes `/health`, `/api/health`, `/status`.
- **Virtual twin map** — documents composition with **resonite-mcp**, **robotics-mcp**, **worldlabs-mcp** (no duplicate Resonite client here).
- **`bumi(operation="market")`** — Noetix story, **China humbot** landscape, **[JD.com](https://www.jd.com)** + **Shenzhen / Shanghai / Beijing** walk-up retail context (see upstream README).

**Hardware honesty (upstream README):** Maintainers do **not** have a physical Bumi yet; Noetix is **oversubscribed** → expect **months** for units. **Bumi vbot** prep uses the existing **vbot MCP fleet** (**robotics-mcp**, **resonite-mcp**, **unity3d-mcp**, **blender-mcp**, **worldlabs-mcp**, etc.) — see upstream README.

---

## Naming

Repo **`bumi-mcp`**; vendor **Noetix Robotics** in descriptions and Glama keywords.

---

## Docs in this folder

| File | Purpose |
|------|---------|
| [STATUS.md](./STATUS.md) | Release state |
| [INTEGRATION.md](./INTEGRATION.md) | Mesh wiring |
| [STRUCTURE.md](./STRUCTURE.md) | Repo layout |

---

## Fleet

| Related | Role |
|---------|------|
| [robotics-mcp](../robotics-mcp/) | Orchestration, `noetix_info`, vbot + Resonite |
| [yahboom-mcp](../yahboom-mcp/) | ROS 2 car pattern |
| [dreame-mcp](../dreame-mcp/) | Appliance pattern |
| [resonite-mcp](../resonite-mcp/) | In-world tooling |
| [robofang](../robofang/) | Hub, federation |

---

*Tags: #bumi-mcp #noetix #humanoid #robotics #mcp #fleet*
