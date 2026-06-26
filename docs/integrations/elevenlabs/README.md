# ElevenLabs Integration Guide

ElevenLabs provides state-of-the-art **Neural Voice Cloning** and **Multilingual TTS**.

## Overview

ElevenLabs is used in Speech-MCP for its superior Professional Voice Cloning (PVC) and its broad language support. While Hume AI leads in emotional prosody (EVI), ElevenLabs provides the "High Fidelity" benchmark for voice identity.

## Key Capabilities

- **Instant Voice Cloning**: Clone a voice in seconds with high accuracy.
- **Professional Voice Cloning**: Studio-quality identity replication.
- **Multilingual v2**: High-performance synthesis in 32+ languages.
- **Speech-to-Speech**: Transform voice identity while maintaining original performance.

## MCP Implementation

The `speech-mcp` gateway extends the TTS and Cloning tools to support ElevenLabs:

- Select `provider="elevenlabs"` in `text_to_speech`.
- Use `manage_voice_clones` for PVC management.

## Configuration

Requires an `ELEVENLABS_API_KEY` in your environment.
- **Base URL**: `https://api.elevenlabs.io/v1`
