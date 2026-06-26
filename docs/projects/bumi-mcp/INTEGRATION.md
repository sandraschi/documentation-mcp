# bumi-mcp — Integration

How **bumi-mcp** connects to the **sandraschi MCP fleet** and **RoboFang**.

**Repo:** [sandraschi/bumi-mcp](https://github.com/sandraschi/bumi-mcp) · **Ports:** **10774** / **10775**

---

## Composition (do not duplicate)

| Capability | Delegate to |
|------------|-------------|
| Resonite sessions, avatars, worlds | **resonite-mcp** |
| Gaussian splat / WorldLabs ingest → Resonite | **worldlabs-mcp** + **robotics-mcp** workflows |
| Fleet-wide vbot / OSC | **robotics-mcp** |

**bumi-mcp** owns **Noetix Bumi narrative + OSS pointers + optional HTTP health** (`BUMI_ROBOT_URL`). Motion control arrives only with a documented vendor bridge.

---

## Registry

- [operations/WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) — **10774**, **10775**
- [operations/webapp-registry.json](../../operations/webapp-registry.json) — `bumi-mcp-backend`, `bumi-mcp-frontend`
- [operations/MASTER_MCP_CONFIG.json](../../operations/MASTER_MCP_CONFIG.json) — `bumi-mcp` stdio (disabled default)

---

## RoboFang

- [docs/integrations/bumi-mcp.md](https://github.com/sandraschi/robofang/blob/main/docs/integrations/bumi-mcp.md)
- [docs/MCP_SERVERS.md](https://github.com/sandraschi/robofang/blob/main/docs/MCP_SERVERS.md) §3.4
