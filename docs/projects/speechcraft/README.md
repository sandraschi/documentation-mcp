# SpeechCraft

**Version**: v0.1.0 — Text-to-Speech, Voice Design & Audio Synthesis Studio.
**Repository**: [`d:\Dev\repos\speechcraft`](file:///d:/Dev/repos/speechcraft) | [GitHub: sandraschi/speechcraft](https://github.com/sandraschi/speechcraft)
**Control Port**: `14132` (`speechcraft --control 14132`)
**Parent Suite**: Sovereign Craft Suite / Audio

---

## Features & Architecture

```
speechcraft-core (ONNX Kokoro/Piper Runner / Phonemizer / Audio Normalizer)
                               ^
        ┌──────────────────────┴──────────────────────┐
        │                                             │
 speechcraft-mcp (L1/L2)                       speechcraft-app (L3 GUI)
(FastMCP Stdio Server & CLI)              (egui 0.37 Waveform & Voice Designer)
```

- **Consolidates Fleet Repos**: `speech-mcp`, `audio-studio-mcp`.
- Offline neural TTS with sub-100ms latency via Kokoro ONNX.
- Phoneme-level pitch, duration, and cadence fine-tuning.
