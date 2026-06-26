# Hume AI Integration Guide

Hume AI provides the **Empathic Voice Interface (EVI)** and **Octave TTS**, enabling emotionally intelligent interactions through AI.

## Overview

Hume AI's technology is designed to measure nuanced vocal modulations and respond with emotionally appropriate prosody. This integration allows the MCP fleet to synthesize speech that isn't just natural-sounding, but contextually aware of human emotion.

## Key Capabilities

- **EVI 2/3**: Real-time, low-latency conversational voice AI with built-in emotional intelligence.
- **Octave TTS**: High-fidelity text-to-speech with granular control over emotional tones and prosody.
- **Voice Cloning**: Create faithful clones of voices from minimal source audio (5+ seconds).
- **Expression Measurement**: Dynamic analysis of vocal bursts, rhythm, and timbre.

## MCP Implementation

The `speech-mcp` server provides a SOTA bridge to these APIs, now expanded to a **Multi-Provider Gateway** supporting both Hume AI and ElevenLabs.

### Tools
- `text_to_speech`: Synthesize audio with emotional instructions.
- `start_evi_session`: Initialize a WebSocket-based real-time session.
- `manage_voice_clones`: Create and list custom voice clones.

## Configuration

Requires a `HUME_API_KEY` in your environment.
- **API Base**: `https://api.hume.ai/v0`
- **WebSocket**: `wss://api.hume.ai/v0/evi/chat`

## SOTA Aesthetics

The `speech-mcp` webapp uses the **Midnight Empathy** design system, featuring glassmorphism and emotion-reactive visualizers.
