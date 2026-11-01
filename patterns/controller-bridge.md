# Controller Bridge — VDJ/Serato → Mixxxxx

## The Gap

| | Serato | VirtualDJ | Mixxx |
|---|--------|-----------|-------|
| Certified mappings | 200+ (vendor-official) | 500+ (vendor + community) | ~200 (community only) |
| Auto-detection | Yes (vid/pid database) | Yes (built-in) | Partial |
| MIDI learn | No | Yes (full) | Yes (per-control) |
| Mapping format | Binary .dat files | XML + script | JavaScript |
| New controller support | Vendor ships it | Days after release | Months to years |

## The Files

**VirtualDJ** stores device mappings at:
```
%APPDATA%\VirtualDJ\Devices\*.xml
%APPDATA%\VirtualDJ\Devices\Default\*.xml
C:\Program Files\VirtualDJ\Devices\*.xml  (bundled)
```

Each XML describes MIDI/HID bindings, button names, LED feedback, and display mappings.

**Serato** stores at:
```
%APPDATA%\Serato\Hardware\*.dat
```

Binary format (already partially reverse-engineered in `src/library/serato/`).

## Strategy

### Phase 1: VDJ XML → Mixxx JS converter

VDJ's mapping XML is well-documented. A Python script reads it and outputs a Mixxx controller script:

```python
# Input: VDJ device XML
# Output: Mixxx controller.js

MIDI_ACTION_MAP = {
    "deck 1 play":       ('[Channel1]', 'play'),
    "deck 1 cue":        ('[Channel1]', 'cue_default'),
    "deck 1 sync":       ('[Channel1]', 'sync_enabled'),
    "deck 1 volume":     ('[Channel1]', 'volume'),
    "deck 1 filter":     ('[Channel1]', 'filterHigh'),
    "deck 1 browse":     ('[Library]', 'MoveVertical'),
    "deck 1 load":       ('[Channel1]', 'LoadSelectedTrack'),
    "master volume":     ('[Master]', 'volume'),
    "crossfader":        ('[Mixer]', 'crossfader'),
    # ... 200+ mappings
}
```

### Phase 2: Auto-detection via VID/PID database

Read USB device descriptors, match against a compiled database of known controllers, auto-load the correct mapping.

```python
USB_DEVICES = {
    (0x08E4, 0x0158): "Pioneer DDJ-1000",
    (0x08E4, 0x0149): "Pioneer DDJ-SB3",
    (0x2B73, 0x0001): "Denon DJ MC7000",
    # ... 1000+ entries
}
```

### Phase 3: Serato format exporter (read their mapping binary)

The existing `src/library/serato/` parsers understand Serato's binary crate/cue format. Extend to also read controller mapping `.dat` files.

## Implementation

Build a converter script at `D:\Dev\repos\mixxxxx\scripts\controller_bridge.py` that:
1. Scans for VDJ device XMLs
2. For each, generates a Mixxx controller `.js` file + `.xml` descriptor
3. Installs to `res/controllers/` for auto-detection

Also add a `mixx_controller` tool to `mixx-dj-mcp`:

| Operation | Description |
|-----------|-------------|
| `list_detected` | List detected USB MIDI controllers |
| `convert_vdj` | Convert a VDJ mapping to Mixxx format |
| `auto_map` | Auto-detect controller and suggest mapping |
| `learn` | Walk through MIDI learn for unmapped controls |
| `status` | Show current controller mapping status |

## Win

If this works for even the top 20 most common DJ controllers (Pioneer DDJ series, Numark Mixtrack series, Denon MC series), Mixxxxx instantly goes from "can I find a mapping for my controller?" to "plug and play" — parity with VDJ and Serato for hardware support.
