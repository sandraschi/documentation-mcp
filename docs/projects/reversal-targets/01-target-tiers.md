# 01 - Curated Target Tiers

Ranked by hittability for a small fleet: shallow math first, documented user
refusal second, legal exposure third. Every entry names the wedge (one refused
feature, never the whole app), the fleet holder, and the C&D temperature.

## Tier 0 - FOSS and orphaned commercial (hit freely)

No living owner with litigation incentive. Trackers are public recruitment grounds.

| Target | Wedge | Fleet holder | Notes |
|---|---|---|---|
| Mixxx | Video mixing the greybeards refused for years | mixx-dj-mcp + virtualdj-mcp + videogen | Flagship. Users document departure to VDJ/Serato in-tracker. Shallow math. |
| Audacity | Post-privacy-fiasco goodwill gap; modern UX, non-destructive basics | audiotool-nexus-mcp + reaper-mcp | Community distrust of the owner is a recruiting asset. |
| VLC gaps | Streaming, library, and remote-control UX around an unkillable engine | directmedia-mcp + obs-mcp | Never clone the decoders; clone the experience around them. |
| KeePassXC gaps | Browser + mobile UX polish | (none yet - candidate) | Trust-sensitive: must stay auditable, MIT, offline-first. |
| Thunderbird gaps | Calendar,.E2E mail UX | thunderbird-mcp | Mozilla-scale, but gaps are shallow and users vocal. |
| Darktable gaps | DAM workflow, culling speed | immich-mcp | Photographers file precise complaints; differential-testable against Lightroom. |
| Inkscape gaps | Performance, SVG2 features | inkscape-mcp | Slow-moving, expert users, vector math is public. |
| Calibre gaps | Reader UX, German corpus ingestion | calibre-mcp | See Digitale Bibliothek drill below. |
| foobar2000 | Effectively single-maintainer, Windows-only, no meaningful updates | audiotool-nexus-mcp | Abandonware-adjacent; a modern free player is months of work. |
| Paint.NET | Single dev, closed source but friendly; gaps in photo tools | gimp-mcp | Verify license posture before touching; author is reasonable. |
| Anki gaps | Sync, mobile, shared-deck UX | (none yet - candidate) | Medical/student users file excellent bug reports. |
| Scrivener gaps | Windows version lags Mac for years | libreoffice-mcp + pdf-mcp | Writers are loyal and loud; long-form UX is shallow math. |

## Tier 1 - Mid-tier commercial, shallow math, stagnant (hit with care)

Living owners, so diverge chrome and names from day one. Pick fights where the
math is public and the incumbent is visibly asleep.

| Target | Wedge | Notes |
|---|---|---|
| VirtualDJ/Serato video features | Specific effects routing and library gaps | Irony: the refuge Mixxx users fled to has its own refused corners. |
| Ableton arrangement UX | Session-to-arrangement bridging, UX polish | DSP underneath is standard; the moat is workflow taste, which is clonable by observation. Big but shallow. |
| Bandicam/Fraps-style capture UX | Modern overlay + instant-share flow | OBS does the engine; the wedge is the five-click experience. |
| Total Commander / Directory Opus | Twin-panel modernization, preview, tabs | File managers are pure UX; zero math moat. Unsexy, lucrative, grateful users. |
| Scrivener Windows parity | Already in Tier 0 list; commercial but slow | See above. |
| DJUCED / djay gaps | Mobile/desktop handoff | Small vendors, unlikely to litigate a free alternative. |

## Tier 2 - Heavy but swarmable (document, do not start)

Deep math that still falls to differential testing plus contributor swarms, as
photocraft proved. Only with a cause, a tracker, and merge velocity ready.

| Target | Math depth | Notes |
|---|---|---|
| Blender addon ecosystem | Varies; material/retopo/rigging tools | Contribute upstream first; clone only refused addons. |
| DaVinci gaps | Codecs, temporal, color science | Deep; needs the swarm, not a skunkworks. |
| KiCad gaps | EDA UX, library management | Engineers file perfect issues; math is standards. |
| LibreOffice fidelity gaps | OOXML round-trip edge cases | Decades deep, but every edge is a testable spec. |

## Tier 3 - Unattainable for us (study only)

| Target | Why not |
|---|---|
| Adobe suite | ArtCraft's war; also trade-dress minefield for a second mover |
| AutoCAD / Parasolid kernels | 40 years of computational geometry; no swarm available |
| Excel calc engine | Deceptively monstrous; compatibility surface is the product |
| Pro Tools DSP | Hardware-tied, litigious owner, niche pro lock-in |

## Drill candidate: Digitale Bibliothek 5 (UPDATED 2026-10-10: premises revised)

Directmedia Publishing's German classics library on disc (v5). Corrections to
the first draft of this entry, all verified live on Goliath:

- NOT absent: Digibib5.exe RUNS (PID 110836, window "Digitale Bibliothek").
  No install trace in registry/Program Files (portable or CD-launched).
- Format war already won by directmedia-mcp: TEXT.DKI cracked (structured
  records, 2-byte length headers), 101 volumes / ~14GB extracted to Python.
  The fleet holder EXISTS and holds the corpus. Drill is not acquisition.
- What never worked is reversing-mcp's Ghidra execution side (tools
  registered, ReVa/IDA docs written, decompiler loop unclosed).
- New finding: the app window is a ghost. It reports 0x0 at screen center,
  PrintWindow yields title-bar plus black client, and force-maximize claims
  fullscreen while the compositor shows underlying windows. Late-90s Delphi
  versus Win11 DWM. It collapses its own window within seconds of being
  maximized. UIA tree inspection (pywinauto-mcp) is the way in, not pixels:
  menus and controls exist regardless of paint.
- Publisher believed defunct (verify: Directmedia folded circa 2012 -
  confirm before any redistribution; local private use of owned media is
  the documented posture in directmedia-mcp).
- Revised drill: (a) UIA crawl of the live ghost via pywinauto missions,
  keyboard-first (Delphi apps answer Alt-key navigation when paint is
  broken); (b) route the already-extracted 101 volumes into calibre-mcp
  depot for German RAG evaluation; (c) compat-shim attempts (XP-SP3, 16-bit,
  admin) inside win11-automated glass box only if (a) stalls.
