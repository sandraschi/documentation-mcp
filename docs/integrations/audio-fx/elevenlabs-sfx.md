# ElevenLabs SFX Integration

**Category**: Audio FX / Text-to-SFX  
**Status**: SOTA API (v2.1.0)  
**API Endpoint**: `https://api.elevenlabs.io/v1/sound-generation`

## Overview
**ElevenLabs SFX** is a premier generative model for creating short, high-fidelity sound effects from text descriptions. It is optimized for "one-shot" transients and environmental loops, making it the primary choice for real-time app notifications, game sounds, and UI interactions.

## 🛠️ Key Features
- **Prompt Fidelity**: Exceptional understanding of material properties (e.g., "brushed aluminum," "cracked glass").
- **Automatic Looping**: Capability to generate seamless background loops (e.g., "gentle rain on a tin roof").
- **Variable Duration**: Support for samples ranging from 0.5s to 20s.

## 📝 Prompting Strategy
To get the best results from ElevenLabs, use descriptive, texture-heavy language:

- **Good**: *"Cinematic bass drop with a mechanical metallic trailing echo, high intensity."*
- **Bad**: *"Loud noise."*

## 🎬 Example MCP Tool Usage
```json
{
  "name": "generate_sfx",
  "arguments": {
    "prompt": "Cybernetic eyelid motor whir, high pitch",
    "duration_seconds": 1.5,
    "prompt_influence": 0.8
  }
}
```

---
> [!TIP]
> Use the `prompt_influence` parameter to control how closely the model sticks to your text vs. its generative "creativity."
