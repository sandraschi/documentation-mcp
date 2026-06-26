# Boomy Audio Upgrade — ReSpeaker Lite + Piper TTS

**Project:** `yahboom-mcp`  
**Date:** 2026-04-14  
**Tags:** `[yahboom-mcp, robotics, voice, audio, respeaker, piper-tts, upgrade, planned]`  
**Status:** Planned — hardware not yet purchased  
**Full reference:** `D:\Dev\repos\yahboom-mcp\docs\hardware\VOICE_AUDIO_UPGRADE.md`

---

## Why

The CSK4002 bundled voice module has a hard ceiling: 85 fixed preset responses, no AEC, and no arbitrary TTS. The chatrobot concept requires open-vocabulary STT and natural TTS. Without AEC, the chatrobot loop is also fundamentally broken — the mic hears its own speaker output and feeds back.

## Hardware: Seeed ReSpeaker Lite (XMOS XU316)

**~€24, Seeed DE warehouse, zero-driver USB UAC 2.0**

Key advantages over the CSK4002 on the capture side:
- **Hardware AEC** (Acoustic Echo Cancellation) on the XU316 DSP — cancels Piper output before Vosk sees it
- **Beamforming + noise suppression** — motor noise from mecanum wheels is removed at the DSP level
- 3 m far-field pickup with DSP active vs ~1 m raw
- 3.5mm audio output for speaker playback

**What the CSK4002 is kept for:** hardware wake word detection. When someone says "Hi, Yahboom", the module fires a `0xA5` binary packet in ~100 ms — fast, offloaded, zero Pi CPU. The chatrobot uses this as its wake trigger, then captures from the ReSpeaker Lite.

## Software: Piper TTS replaces espeak-ng

**Free, Apache 2.0. rhasspy/piper on GitHub.**

FastSpeech2 + HiFiGAN, quantised for Pi 5 CPU. Real-time or faster for most voice models. English (`en_US-lessac-medium`) and German (`de_DE-thorsten-medium`) voices available at ~60–90 MB each.

Quality comparison: espeak-ng = robotic GPS voice. Piper = natural neural voice. Night and day.

## Updated Latency Budget

| Stage | Old | New |
|---|---|---|
| Vosk STT | ~800 ms | ~500 ms (clean AEC input) |
| Piper TTS | ~500 ms espeak | ~200 ms Piper |
| **Total to first word** | **~6.4 s** | **~5.8 s** |
| **Loop stability** | Broken (no AEC) | Stable |

With sentence-streaming (Piper starts playing sentence 1 while generating sentence 2): perceived latency drops to ~3.5 s.

## Shopping List

| Item | Price |
|---|---|
| Seeed ReSpeaker Lite (XU316) | ~€24 |
| Small speaker (if needed) | ~€5–8 |
| **Total** | **~€24–32** |

## Integration Points

- `operations/voice.py` `say` operation: add `YAHBOOM_TTS_ENGINE=piper` path alongside espeak-ng
- `operations/chatbot.py` (planned): uses ReSpeaker Lite ALSA device for capture, Piper for output
- CSK4002 `listen` operation: unchanged, still used as wake trigger
- udev: add ReSpeaker Lite ALSA rule to `99-boomy.rules`

## Reference Links

- Full doc: `D:\Dev\repos\yahboom-mcp\docs\hardware\VOICE_AUDIO_UPGRADE.md`
- ReSpeaker Lite: https://wiki.seeedstudio.com/reSpeaker_usb_v3/
- Piper TTS: https://github.com/rhasspy/piper
- Working reference implementation (Pi 5 + Vosk + Piper + Ollama): https://github.com/m15-ai/TrooperAI
