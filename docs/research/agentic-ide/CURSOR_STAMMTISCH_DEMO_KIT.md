---
title: "Cursor Stammtisch — demo kit (Vienna / any meetup)"
category: research
status: notes
audience: builders
last_updated: 2026-03-24
---

# Cursor Stammtisch — what actually lands

**Claiming “I made 100 repos with Cursor”** sounds like vapor. **Proof beats brag.** Optimize for **one tight story + one live or recorded demo** (60–120 seconds).

---

## The pitch (one sentence)

> “I run a **local MCP fleet**: each server is a small product (FastAPI + tools + optional Vite UI). The agent doesn’t ‘guess’ my stack — it **calls tools** with schemas I own.”

That reframes volume into **systems design**.

---

## iPad + RustDesk → home box (4090) — **light bag, heavy iron**

Solid Stammtisch move: **no 3 kg NVIDIA laptop**; carry **iPad** (or phone), connect over **RustDesk** to a **home server / workstation** that has the GPU and the real MCP fleet.

**Story in one line:** “Compute and MCP stay **at home** on my network; I’m just the **glass** — privacy + no schlepping.”

**Prep (do before you leave):**

| Check | Why |
|--------|-----|
| Home PC **awake** or reliable **Wake-on-LAN** path | RustDesk can’t wake a dead machine |
| RustDesk **ready** (client running, ID known) | iPad RustDesk app or browser flow per your setup |
| **Test from cellular** once | Venue Wi‑Fi ≠ your LAN — catch NAT/firewall surprises early |
| **Low-latency demo path** | Prefer a flow that tolerates 80–200 ms (dashboard, static catalog, short tool output) — not buttery local video editing |
| **Sanitized screen** | No tokens, no `fleet_manifest` secrets, no embarrassing notifications |

**Optional tie-in:** fleet already treats **RustDesk** as a hand (see RoboFang **`docs/MCP_FLEET.md`**); you can mention **remote substrate** without live-driving it on spotty Wi‑Fi.

**Risk:** conference uplink sucks → have a **15 s screen recording** of the same RustDesk session as backup (Tier B).

---

## Demo tiers (pick one)

### A) **Live** (best if Wi‑Fi behaves)

1. Open **one** MCP-backed webapp on a **fleet port** (e.g. `107xx`–`108xx`, not 5173).
2. Show **Cursor** connected to **one** MCP server (stdio): run a **single tool** with a visible result (e.g. refresh catalog, fetch status, list tools).
3. One sentence: “Same server: stdio for the IDE, HTTP for the dashboard.”

**Prep:** laptop charged, token in env if needed, **offline fallback** = screen recording on phone.

### B) **Recorded** (most reliable)

- 90-second screen capture: IDE → tool call → JSON result → optional browser tab.
- Narrate **one** concrete outcome (e.g. “indexed 100 public forks, sorted by stars, filtered by category”).
- **Baseline (nth Stammtisch):** keep a **pocket proof pack** offline on phone/tablet — **still + Short (or Veo clip)** of the same story (RustDesk → 4090 box, fleet port UI, one MCP tool). Live demo when the room cooperates; **premade when it doesn’t**. Same assets can seed YT Shorts later; no need to ship all of that for week one.

### C) **Artifact** (no runtime)

- Print or phone: QR to a **public README** or **30-second GIF** in a repo.
- Handout: **one diagram** (agent → MCP → your API / hardware). See `operations/FLEET_CONTROL_PLANE.md` for a simple box diagram you can reuse.

---

## Props checklist

| Item | Why |
|------|-----|
| **Laptop + HDMI/USB‑C adapter** | Projector roulette (or **iPad + RustDesk** to home 4090 — see § above) |
| **Offline recording** | Venue Wi‑Fi dies |
| **Second screen or phone** | Show README / ports table while IDE is full-screen |
| **Business card or QR** | Repo + LinkedIn — conversation continues |

---

## What *not* to do

- Don’t open 100 repos in a file tree — **boring and unbelievable**.
- Don’t deep-dive RAG unless the room asked for it.
- Don’t argue “AI will replace devs” — Stammtisch wants **craft**, not manifestos.

---

## Vienna-specific (light touch)

- Mention **local-first** and **privacy** (MCP on `127.0.0.1`) — plays well in EU crowds.
- If waitlist clears: **arrive early**, sit power-side, **introduce with the one-liner** above.

---

## Optional “wow” micro-demos (low effort)

- **Port discipline:** show `mcp-central-docs/operations/WEBAPP_PORTS.md` — “we reserved **10700–10800** so nothing fights Vite defaults.”
- **One weird hand:** robot, OBS, Resolve — **physical or creative** beats generic CRUD.
- **iflow-mcp-catalog:** “Here’s **live data** from GitHub API — stars, categories — not slides.” (Requires `GITHUB_TOKEN` + prior `refresh` if network is flaky.)

---

## Related internal docs

- Fleet architecture (no duping servers into RoboFang): [FLEET_CONTROL_PLANE.md](../../operations/FLEET_CONTROL_PLANE.md).
