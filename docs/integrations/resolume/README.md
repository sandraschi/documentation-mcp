# Resolume Arena & resolume-mcp

Fleet integration for **live VJ / video**: the host application is **Resolume Arena** (or **Avenue**); the MCP bridge is **[resolume-mcp](../../projects/resolume-mcp/README.md)** (OSC-based control from agents).

---

## Host software: Resolume (demo vs license)

Resolume is commercial software from [resolume.com](https://resolume.com/). There is **no** separate long-term “free tier” like a SaaS plan.

**Official demo:** Both **Avenue** and **Arena** are available as **fully functional demos** from the [download page](https://resolume.com/download/). You can use the demo **as long as you like**; **everything works**, including saving projects. The **limitations** are:

- A **visual watermark** on the output  
- A **robotic voice** periodically reminding you which product you are using  

See Resolume’s article: **[Difference between Avenue and Arena](https://resolume.com/support/en/avenue-arena-difference)** (section **Demo**).

**Avenue vs Arena:** Arena is the superset (projection mapping, edge blending, DMX, SMPTE, Pioneer/Denon sync, etc.); Avenue is the VJ core without those Arena-only features. Same demo rules apply.

**Purchased license:** Removes watermark and voice reminders for that edition.

---

## Fleet MCP server: resolume-mcp

| Item | Detail |
|------|--------|
| **Purpose** | OSC control of clips, layers, effects, performance (BPM, batch updates) |
| **Repo** | [projects/resolume-mcp](../../projects/resolume-mcp/README.md) — also `D:/Dev/repos/resolume-mcp` |
| **Transport** | OSC (typical incoming/outgoing **7000 / 7001**; align with Resolume preferences) |
| **Webapp** | React/Vite dashboard; see [fleet-registry.json](../../operations/fleet-registry.json) and [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |

**Operator doc (copy-paste friendly):**  
[resolume-mcp: Resolume demo & licensing](https://github.com/sandr/resolume-mcp/blob/main/docs/user-guide/RESOLUME_ARENA_DEMO_AND_LICENSING.md) (same content as in-repo path `docs/user-guide/RESOLUME_ARENA_DEMO_AND_LICENSING.md`).

---

## Related fleet entries

- **[VirtualDJ](virtualdj/README.md)** — DJ / audio performance (different product family).
- **[osc-mcp](../../projects/fleet.md)** — Generic OSC; **resolume-mcp** is deeper for Arena-specific workflows (see fleet notes).

---

## References (Resolume)

- [Download](https://resolume.com/download/)  
- [Avenue vs Arena](https://resolume.com/support/en/avenue-arena-difference) — includes **Demo** section  
