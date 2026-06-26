# Reaper Workflows: Automated Audio production

These workflows define the automated audio patterns in the Sandra ecosystem.

## 🔊 Workflow: "Robot Vocal Signature Generation"

Creating unique auditory identities for robot chassis.

1.  **Selection**: Agent selects a base "Industrial" flavor from the sample vault.
2.  **Processing**: `reaper_mcp` applies a Granular Synthesizer FX and modulates parameters.
3.  **Variant Generation**: Agent triggers 10 different iterations with slightly randomized pitch.
4.  **Rendering**: `trigger_render` saves the files to the **Unitree Robotics** assets folder.

## 🎞️ Workflow: "Post-Production Master"

Final audio polish for documentary walkthroughs.

1.  **Assembly**: Import the audio track from a **Davinci Resolve** render.
2.  **EQ/Compression**: Agent applies a "Sandra-Standard" voice-over chain.
3.  **Loudness Normalization**: Agent ensures the final output hits -14 LUFS (Integrated).
4.  **Export**: The finalized track is sent back to Resolve for the final encode.

---
*Last updated: 2026-02-14*
