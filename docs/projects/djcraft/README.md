# DJCraft

**Version**: v0.1.0 — Local-First 4-Deck Digital Mixing, Stem Isolation & Harmonic Studio.
**Repository**: [`d:\Dev\repos\djcraft`](file:///d:/Dev/repos/djcraft) | [GitHub: sandraschi/djcraft](https://github.com/sandraschi/djcraft)
**Control Port**: `14118` (`djcraft --control 14118`)
**Parent Suite**: Sovereign Craft Suite / Craft Bundlers

---

## Features & Architecture

```
djcraft-core (DSP Engine / Stem Extractor / BPM & Key Detector)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
  djcraft-mcp (L1/L2)                          djcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 4-Deck Mixer + Waveforms)
```

- **Consolidates Fleet Repos**: `virtualdj-mcp`, `stems-mcp`, `butterchurn-mcp`, `dj-media-hub`.
- **4-Deck Virtual Engine**: Direct fader control, pitch bends, transient-based BPM tracking, and master crossfader curves.
- **Real-Time Stem Isolation**: Vocal, bass, drums, and harmonic instrument separation.
- **Hardware MIDI Mapping**: Zero-latency mapping to Hercules DJ consoles and physical MIDI controllers.
