# Boomy (Yahboom Raspbot v2) — Voice & Audio

**Project:** `yahboom-mcp`  
**Date:** 2026-04-14  
**Tags:** `[yahboom-mcp, robotics, voice, audio, CSK4002, espeak-ng, vosk, chatrobot]`  
**Full reference:** `D:\Dev\repos\yahboom-mcp\docs\hardware\VOICE_AUDIO.md`

---

## Summary

Boomy has three independent audio-related hardware components:

| Component | Purpose | Interface |
|---|---|---|
| CSK4002 voice module | Preset ASR (85 phrases) + preset playback | USB serial, 115200 baud |
| Pi 5 ALSA audio out | Arbitrary TTS via espeak-ng, file playback | ALSA / 3.5mm / USB audio |
| USB microphone | STT input for chatrobot loop | ALSA capture |

---

## Critical: The Module Is Not a TTS Chip

The CSK4002 is an **ASR (speech recognition) + preset playback** module. It cannot synthesise arbitrary text. The old `voice.py` was sending SYN6288 ASCII protocol (`$say,text#`) which the CSK4002 ignores entirely.

**Correct protocol — binary 3-byte packet:**
```
[0xA5, phrase_id, ~phrase_id & 0xFF]
```

Arbitrary TTS is handled by `espeak-ng` on the Pi over ALSA — completely separate from the module.

---

## Device Conflict Warning

Both the Rosmaster UART (sensors/IMU) and the voice module are USB-serial devices. Without udev rules, `ttyUSB0` assignment is non-deterministic. Fix with `/etc/udev/rules.d/99-boomy.rules`:

```udev
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
    SYMLINK+="ttyVOICE", MODE="0666", GROUP="dialout"
```

`voice.py` uses `/dev/ttyVOICE` as the primary device path.

---

## MCP Operations

All via `yahboom(operation=...)`:

| Operation | What it does |
|---|---|
| `get_status` | Probe device, pyserial, espeak-ng |
| `play` (param1=1–85) | Trigger preset phrase via binary packet |
| `play_beep` | Play phrase #1 (beep/greeting) |
| `listen` (param1=timeout) | Block and read one recognition event |
| `say` (param1=text) | espeak-ng TTS via ALSA |
| `say_file` (param1=path) | Upload + play MP3/WAV on Pi |
| `chat_and_say` (param1=prompt) | Ollama → espeak-ng pipeline |
| `volume` (param1=0–100) | Set ALSA master volume |

---

## Chatrobot Architecture

Full offline voice chatbot loop on Pi 5:

```
Wake word → CSK4002 → 0xA5 packet → Pi
                                      → Capture audio (ALSA)
                                      → Vosk STT → text
                                      → Ollama gemma3:1b → response
                                      → espeak-ng → speech
                                      → (optional) motion intent → cmd_vel
```

**Latency budget:** ~8 seconds end-to-end (Vosk + gemma3:1b).

**Planned implementation:** `operations/chatbot.py` — operations `chatbot_start`, `chatbot_stop`, `chatbot_status`.

---

## Pi Setup Checklist

```bash
sudo apt-get install espeak-ng          # TTS
pip3 install pyserial vosk              # serial + STT
# Download Vosk model:
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d ~/vosk-models/
```

---

## Env Vars (set on MCP host / Goliath)

| Variable | Default | Notes |
|---|---|---|
| `YAHBOOM_VOICE_DEVICE` | auto | Force path e.g. `/dev/ttyVOICE` |
| `YAHBOOM_VOICE_BAUD` | `115200` | Do not change for CSK4002 |
| `YAHBOOM_ESPEAK_VOICE` | `en` | Voice code for espeak-ng |
| `YAHBOOM_ESPEAK_SPEED` | `150` | WPM |
| `YAHBOOM_ESPEAK_PITCH` | `50` | 0–99 |

---

## Upgrade Plan

**[VOICE_AUDIO_UPGRADE.md](VOICE_AUDIO_UPGRADE.md)** — ReSpeaker Lite (XU316, ~€24) + Piper TTS.  
Adds hardware AEC, beamforming, noise suppression, and natural neural voice. Fixes chatrobot loop stability. CSK4002 kept as wake word detector.
