# Resolume Arena & resolume-mcp

Fleet integration for **live VJ / video**: the host application is **Resolume Arena** (or **Avenue**); the MCP bridge is **[resolume-mcp](../../projects/resolume-mcp/README.md)** (OSC-based control from agents).

---

## Host software: Resolume (demo vs license)

Resolume is commercial software from [resolume.com](https://resolume.com/). There is **no** separate long-term “free tier” like a SaaS plan.

**Official demo:** Both **Avenue** and **Arena** are available as **fully functional demos** from the [download page](https://resolume.com/download/). You can use the demo **as long as you like**; **everything works**, including saving projects. The **only** limitations (per Resolume manuals and [Avenue vs Arena — Demo](https://resolume.com/support/en/avenue-arena-difference)) are:

| Limitation | What DJs/VJs see |
|------------|------------------|
| **Logo watermark** | Resolume branding appears on the **program output** from time to time (unacceptable on a big LED wall). |
| **Robotic voice** | A deep/robotic voice says **“Resolume Avenue”** or **“Resolume Arena”** on the output **every minute or so** — intentional nag, not a bug. |

There is **no** feature cripple in the demo. **Registration** (purchased serial under **File → Preferences → Registration**) removes **both** the watermark and the voice. Offline registration is supported if the show machine has no Internet.

**Avenue vs Arena:** Arena is the superset (projection mapping, edge blending, DMX, SMPTE, Pioneer/Denon sync, etc.); Avenue is the VJ core without those Arena-only features. Same demo rules apply.

**Club vs home lab**

- **Not gig-safe on demo** if Resolume audio is routed to the house PA — the voice will blast the room.
- **Dev / integration OK on demo:** develop **resolume-mcp**, test NDI input, and OSC from **mixx-dj-mcp** (`mixx_daw` `resolume_sync`) without paying first.
- **Licensed Avenue (~€299)** is the straightforward fix when Resolume is part of the paid rig.

### mixxxxx stack: video in Resolume, audio from Mixxx

In the fleet **mixxxxx + mixx-dj-mcp** rig, **mixxxxx (or Mixxx) is the audio source of truth** — decks, crossfader, and FOH come from the DJ app. Resolume is a **visual layer** on top:

```
mixxxxx (audio + crossfader video) --NDI--> Resolume layer 1 (base mix)
mixx-dj-mcp --OSC 11119--> mixxxxx
mixx-dj-mcp / resolume-mcp --OSC 7000--> Resolume (tempo, layers, clips)
FOH / booth monitors <-- audio from mixxxxx only
```

**Practical demo workaround:** Do **not** route Resolume’s **audio** to speakers or stream mix (disable or mute Resolume audio outputs; use **NDI or Spout for video only**). The periodic demo voice is on Resolume’s **program output**; if nothing listens to Resolume for sound, the nag does not hit the dancefloor. You still get the **video watermark** on screen until licensed — plan for that on projection, or buy Avenue.

With **mixxxxx providing all sound**, you typically **do not need** Resolume audio at all (no clip audio to FOH, no Resolume sync to CDJs via audio). That matches how many AV rigs work: DJ software = music, VJ software = pictures.

**Canonical fork docs:** [mixxxxx `docs/RESOLUME-FLEET-CROSSCONNECT.md`](https://github.com/sandraschi/mixxxxx/blob/video/docs/RESOLUME-FLEET-CROSSCONNECT.md), [ORCHESTRATOR.md](https://github.com/sandraschi/mixxxxx/blob/video/docs/ORCHESTRATOR.md).

---

## Fleet MCP server: resolume-mcp

| Item | Detail |
|------|--------|
| **Purpose** | OSC control of clips, layers, effects, performance (BPM, batch updates) |
| **Repo** | [projects/resolume-mcp](../../projects/resolume-mcp/README.md) — also `D:/Dev/repos/resolume-mcp` |
| **Transport** | OSC — send **commands to Resolume incoming port 7000** (Preferences → OSC); Resolume may **send** feedback on outgoing **7001** |
| **Webapp** | React/Vite dashboard; see [fleet-registry.json](../../operations/fleet-registry.json) and [WEBAPP_PORTS.md](../../operations/WEBAPP_PORTS.md) |

**Operator doc (copy-paste friendly):**  
[resolume-mcp: Resolume demo & licensing](https://github.com/sandr/resolume-mcp/blob/main/docs/user-guide/RESOLUME_ARENA_DEMO_AND_LICENSING.md) (same content as in-repo path `docs/user-guide/RESOLUME_ARENA_DEMO_AND_LICENSING.md`).

---

## Related fleet entries

- **[mixxxxx](https://github.com/sandraschi/mixxxxx)** (`video` branch) + **[mixx-dj-mcp](https://github.com/sandraschi/mixx-dj-mcp)** — DJ + deck video; NDI into Resolume; OSC bridge on **11118/11119**.
- **[VirtualDJ](virtualdj/README.md)** — DJ / audio performance (different product family).
- **[osc-mcp](../../projects/fleet.md)** — Generic OSC (`resolume_manager`); **resolume-mcp** uses Resolume’s composition address list; see osc-mcp `resolume-expert` skill.

---

## References (Resolume)

- [Download](https://resolume.com/download/)  
- [Avenue vs Arena](https://resolume.com/support/en/avenue-arena-difference) — includes **Demo** section  
