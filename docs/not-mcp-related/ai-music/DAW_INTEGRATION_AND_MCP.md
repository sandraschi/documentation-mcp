# AI Music — DAW Integration, Infinite Crate & MCP Plans

> Last updated: 2026-03-04

Bringing Lyria RealTime and ACE-Step v1.5 into the actual production workflow:
Reaper via the Infinite Crate VST, reaper-mcp new tools, and a planned
ACE-Step MCP server + webapp combo.

---

## Part 1: The Infinite Crate VST in Reaper

### What it is

A free experimental VST3/AU plugin from Google Magenta that pipes the
Lyria RealTime API directly into any VST3-capable DAW as a virtual
instrument. You get a continuously evolving AI music stream on a track —
steer it live with text prompts, BPM sync, key, density, brightness, and
mute controls (bass / drums / other).

### Download & install

- Page: https://magenta.withgoogle.com/infinite-crate
- Windows: VST3 installer (x86_64)
- Free Gemini API key: https://aistudio.google.com/apikey
  (Lyria RealTime usage is currently free, no billing needed)
- Install VST3 to `C:\Program Files\Common Files\VST3\`
  or your custom Reaper VST path

### Reaper setup

1. **Reaper → Options → Preferences → Plug-ins → VST**
   Add `C:\Program Files\Common Files\VST3\` if not already listed
2. Click **Re-scan** / **Clear cache and re-scan**
3. Create a new track → **Insert virtual instrument on new track**
4. Search for "Infinite Crate" → double-click to load
5. On first load: paste your Gemini API key into the key field
   (stored system-wide, not per-project)
6. Hit play on a Lyria prompt → audio starts streaming into the track

### Controls

| Control | What it does |
|---------|-------------|
| **Prompt sliders** | WeightedPrompts — blend up to ~6 text descriptors with relative intensity |
| **BPM** | `[DAW]` = sync to Reaper project tempo; manual = override |
| **Key** | Nudge the model toward a key (imprecise — no major/minor distinction) |
| **TopK** | Lower = more deterministic; higher = more surprising |
| **Temp** | Randomness of generation |
| **Density** | How busy/sparse the arrangement sounds |
| **Brightness** | High-frequency content amount |
| **Mute Bass / Drums / Other** | Drop instrument groups from the stream |
| **Guidance** | How strongly the prompt steers the next generated chunk |

### Practical workflow in Reaper

**Jam partner / inspiration source:**
- Load Infinite Crate on Track 1, armed for live monitoring
- Record-arm Track 2 (your instrument)
- Set BPM to [DAW], set a key, set a vibe prompt
- Reaper records both simultaneously — you playing + AI stream
- Later: use Reaper's dynamic split / item editing to keep the good bits

**Sampling the stream:**
- Load Infinite Crate on a track
- Hit record on that track while it plays
- Capture minutes of evolving material
- Use Reaper's **razor edit** or **dynamic split** to carve out loops
- Drag good loops to the media bay for reuse

**Layering / arrangement:**
- Multiple Infinite Crate instances = multiple parallel streams
  (note: server dropouts increase with multiple instances)
- Each instance can have different prompts — e.g., one sparse ambient,
  one rhythmic, blend them via faders

### Known limitations

- **10-minute session limit** — must click Reset after 10 minutes.
  For longer sessions: record in 8-minute chunks with a reset between.
- **Cloud-only** — requires internet. Not usable offline or on Goliath
  without network. Your 4090 is irrelevant here.
- **Instrumental only** — no vocals. Lyria 3 vocals are Gemini app only,
  not in the RealTime API.
- **Latency** — minimum ~1 second from control change to audible effect.
  Not suitable for tight live performance; fine for background/inspiration.
- **DaVinci Resolve Fairlight: NOT compatible** — Fairlight does not
  reliably support VST3. Use Reaper for Infinite Crate, then import
  rendered clips into Resolve for video sync/editing.

### Reaper → DaVinci Resolve workflow

1. Generate and record Infinite Crate output in Reaper
2. Export as WAV (Track → Render selected items)
3. Import WAV into DaVinci Resolve timeline as audio track
4. Sync to picture in Fairlight or Cut page

---

## Part 2: New reaper-mcp Tools for AI Music

The current reaper-mcp (v2.0, FastMCP, 4 portmanteau tools, port 10796)
controls Reaper via OSC. The existing tools cover transport, tracks,
project management, and system status. Missing: anything AI-music specific.

### Proposed new operations for `reaper_project` portmanteau

```
reaper_project("import_ai_clip", path=..., track=..., position=...)
```
Import a rendered ACE-Step or Lyria clip into the current project at
a specified track and timeline position.

```
reaper_project("render_selection", start=..., end=..., output_path=...)
```
Render a time selection to a file (feeds results back into ACE-Step
pipeline for audio repainting / extend workflows).

```
reaper_project("bounce_track", track_id=..., output_path=...)
```
Bounce a single track (e.g., a recorded Infinite Crate stream) to a
clean WAV for ACE-Step repainting.

### Proposed new portmanteau tool: `reaper_ai`

New 5th portmanteau tool focused on AI music workflows:

```python
reaper_ai(operation, **kwargs)
```

| Operation | Description |
|-----------|-------------|
| `insert_clip` | Import an AI-generated WAV to a new track at a position |
| `create_ai_track` | Add a labeled track designated for AI content |
| `region_to_file` | Export a named region to WAV (for ACE-Step repainting input) |
| `batch_import` | Import a folder of ACE-Step outputs as items on sequential tracks |
| `set_color_ai` | Color all AI-sourced tracks a distinct color (visual tagging) |
| `label_ai_items` | Tag imported AI items with source metadata in item notes |

### Webapp additions (port 10796)

The reaper-mcp webapp dashboard currently shows transport status,
track list, and project info. Proposed new page:

**AI Music Studio page** (`/ai-music`):
- Quick "generate with ACE-Step" button → fires generation, auto-imports result
- Infinite Crate connection status indicator (API key valid / model live)
- List of AI-tagged tracks in current project
- One-click bounce-to-file for any track
- Region list with "send to ACE-Step repainting" buttons

This page requires the ACE-Step MCP (see Part 3) to be running alongside.

---

## Part 3: ACE-Step MCP Server + Webapp (New Project)

### Project name: `acestep-mcp`

Repo: `D:\Dev\repos\acestep-mcp`
Glama target: yes (MIT license, clean training data = good fit)
Port allocation: needs entries in WEBAPP_PORTS.md (TBD)

### What it wraps

ACE-Step v1.5 Python API:
- GitHub: https://github.com/ace-step/ACE-Step-1.5
- Install: `pip install acestep` or `uv add acestep`
- Models: auto-downloaded to `~/.cache/acestep/` on first run
- Hardware: Goliath's RTX 4090 → ~2–5s per full song in turbo mode

### Core MCP tools (portmanteau design)

```python
acestep_generate(operation, **kwargs)
```

| Operation | Parameters | Description |
|-----------|-----------|-------------|
| `text_to_music` | tags, lyrics, duration, model, seed | Generate song from prompt |
| `extend` | audio_path, duration, tags | Extend an existing clip |
| `repaint` | audio_path, start, end, tags | Regenerate a time region |
| `cover` | audio_path, tags | Style-transfer cover version |
| `vocal_to_bgm` | vocal_path, tags | Generate backing track from vocal |
| `batch` | prompts_list, output_dir | Generate multiple songs in parallel |

```python
acestep_models(operation, **kwargs)
```

| Operation | Description |
|-----------|-------------|
| `list` | Available downloaded models |
| `download` | Download a specific model variant |
| `status` | GPU memory, current load |
| `set_default` | Set default model for generation |

```python
acestep_library(operation, **kwargs)
```

| Operation | Description |
|-----------|-------------|
| `list` | Browse generated songs in output dir |
| `get` | Get path/metadata for a specific song |
| `delete` | Remove a song from library |
| `tag` | Add tags to a generated song for search |
| `export_to_reaper` | Copy to Reaper project folder + trigger reaper_ai import |

### Webapp (acestep-webapp)

Standalone React frontend, separate from MCP server itself.
Runs alongside, calls the MCP server's REST endpoint (FastMCP HTTP mode).

**Pages:**

**Generate** (`/generate`)
- Text prompt area for tags + lyrics (separate fields)
- Duration slider (10s – 600s)
- Model selector (turbo variants / SFT / base)
- Seed control (random or fixed)
- BPM / key metadata hints
- Generate button → live progress indicator → audio player on completion
- Waveform display (wavesurfer.js)
- Save to library / Send to Reaper buttons

**Library** (`/library`)
- Grid of generated songs, sortable by date/tags/duration
- Inline audio player per card
- Bulk select for batch export
- Tag editor
- "Open in Reaper" button per song

**Repainting** (`/repaint`)
- Upload or pick from library
- Waveform with drag-select for repaint region
- Tags input for the repainting style
- Preview before/after
- Save repainted version

**Batch** (`/batch`)
- CSV import for bulk generation jobs
- Job queue with progress per item
- Useful for generating e.g. 20 variations of a theme

**Settings** (`/settings`)
- Model management (download / delete / set default)
- Output directory configuration
- GPU status widget
- Reaper integration: path to Reaper project folder for auto-import

### Integration with reaper-mcp

The `export_to_reaper` operation in `acestep_library` calls
reaper-mcp's `reaper_ai("insert_clip", ...)` operation:

```
Claude → "generate a lo-fi jazz track and put it in Reaper"
 → acestep_generate("text_to_music", tags="lo-fi, jazz, chill", duration=120)
 → wait for completion
 → acestep_library("export_to_reaper", song_id=..., track_name="AI LoFi Jazz")
 → reaper_ai("insert_clip", path=..., track=..., position="cursor")
 → reaper_project("save")
```

Full end-to-end from text prompt to Reaper project — one Claude instruction.

### loras (fine-tuning)

ACE-Step supports LoRA fine-tuning from ~5–10 reference songs. The webapp
could expose a LoRA training page:

**LoRA** (`/lora`)
- Upload 5–10 reference audio files
- Style name input
- Training duration estimate (Goliath: ~2h on 4090 for basic LoRA)
- Progress tracking
- Once trained: available in model selector as a style option

This is the "train on Sandra's Reaper projects" path — custom style
that ACE-Step learns from your own music.

---

## Part 4: Summary of Proposed New Work

| Item | Type | Priority | Est. time |
|------|------|----------|-----------|
| Install + test Infinite Crate in Reaper | Manual | Now | 30 min |
| Get Gemini API key for Lyria RealTime | Manual | Now | 5 min |
| Add `reaper_ai` portmanteau to reaper-mcp | Code | High | 1–2 days |
| Add `/ai-music` page to reaper-mcp webapp | Code | Medium | 1 day |
| Create `acestep-mcp` repo (FastMCP 3.0) | Code | High | 2–3 days |
| ACE-Step webapp (React, basic Generate + Library) | Code | Medium | 2–3 days |
| Repaint page | Code | Low | 1 day |
| LoRA training page | Code | Low | 1–2 days |
| Update FLEET_INDEX and WEBAPP_PORTS | Docs | With MCP | 15 min |

Total for core functionality (Infinite Crate working + reaper-mcp update +
basic acestep-mcp with Generate/Library): **~5–7 days**.

---

## Part 5: Quick Start — Right Now

If you want to experiment today before any new MCP work:

```powershell
# 1. Install ACE-Step standalone (no MCP yet)
pip install acestep --break-system-packages

# 2. Download default turbo model
uv run acestep-download

# 3. Launch Gradio UI at localhost:7860
uv run acestep --torch_compile true

# 4. Meanwhile: install Infinite Crate VST in Reaper
#    Download from https://magenta.withgoogle.com/infinite-crate
#    Get API key from https://aistudio.google.com/apikey
#    Load on a Reaper track, paste key, start streaming
```

Both can be running simultaneously: ACE-Step Gradio for batch generation,
Infinite Crate in Reaper for live jamming. No MCP required yet.
