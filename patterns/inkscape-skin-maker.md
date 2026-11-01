# Mixxx Skin Maker — Inkscape-MCP Pipeline

**Concept**: An AI agent designs Mixxx skins via natural language. The pipeline uses `inkscape-mcp` to generate SVG assets and `mixx_skin` to assemble the XML, producing a valid Mixxx skin in minutes.

## How Mixxx Skins Work

A Mixxx skin is a directory containing:

```
skin.xml           — Layout XML (widgets, positions, connections)
style/             — SVGs for knobs, faders, buttons, backgrounds
  knob_bg.svg
  knob_indicator.svg
  fader.svg
  btn_play.svg
  ...
waveform/          — Waveform renderer SVGs (optional)
```

The XML references SVGs by path. Every knob, fader, button, and background is an SVG file. The XML defines layout containers (`<WidgetGroup>`, `<Stack>`) and wires them to ControlObjects.

## The Maker Flow

```
User: "Make me a purple neon skin with large waveforms"
    │
    ├── 1. mixx_skin("create_skin", name="NeonPurple", prompt="purple neon, large waveforms")
    │
    ├── 2. LLM generates skin.xml structure (references LateNight skeleton)
    │
    ├── 3. LLM designs color palette → SVG color schemes
    │
    ├── 4. inkscape-mcp generates SVGs:
    │       - Background: gradient purple (#1a0033 → #0d001a)
    │       - Knobs: neon cyan indicator on dark bg
    │       - Faders: purple track + cyan handle
    │       - Buttons: rounded rects with glow
    │       - Waveform: cyan trace on dark background
    │
    ├── 5. Skin assembled into directory, written to Mixxx skins path
    │
    └── 6. User selects in Preferences → Interface → Skin
```

## Inkscape-MCP Tools Required

The existing `inkscape-mcp` (port 11028) can execute Inkscape commands. We need:

| Operation | What it does |
|-----------|-------------|
| `export_svg` | Run Inkscape to export SVG with given geometry, colors, layers |
| `convert_to_png` | Render SVG to PNG for preview |
| `batch_recolor` | Recolor an entire skin's SVG set with new palette |

## Skin XML Template Engine

Mixxx skin XML follows a consistent structure. Rather than generating from scratch, we clone LateNight (the most flexible base) and modify:

```python
SKIN_TEMPLATE = "LateNight"
PALETTE = {
    "bg_dark": "#0d001a",
    "bg_medium": "#1a0033",
    "accent": "#00ffff",
    "text": "#ffffff",
    "text_dim": "#888899",
    "waveform_low": "#00ffff",
    "waveform_mid": "#ff00ff",
    "waveform_high": "#ffffff",
}
```

Changes:
1. `skin.xml` — update style scheme reference
2. `style/{scheme}/` — generate new SVG files with palette colors
3. `waveform/` — recolor waveform renderers

## Current Limitations

| Issue | Workaround |
|-------|-----------|
| Inkscape must be installed locally | inkscape-mcp already assumes this |
| Full skin generation takes ~60 SVGs | Start with 1 style scheme + 4 deck layouts, reuse LateNight's structure |
| SVG-to-skin mapping is undocumented | We reverse-engineer it from existing skins (the `<PathBackground>`, `<PathForeground>` etc. tags are well-defined in mixxx.org manual) |

## Implementation Plan

| Step | What | Effort |
|------|------|--------|
| 1 | Add `create_skin` operation to `mixx_skin` tool | ~1 hour |
| 2 | Design SVG template set (knob, fader, button, background) | ~2 hours |
| 3 | Wire inkscape-mcp calls into the pipeline | ~1 hour |
| 4 | Test: generate a skin, load in Mixxxxx, verify | ~1 hour |
