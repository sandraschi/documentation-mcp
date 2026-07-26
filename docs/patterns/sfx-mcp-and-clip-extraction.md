# SFX-MCP & Plex Clip Extraction — Bridge Specs

## 1. sfx-mcp: Sound Effects Library

New MCP server wrapping the [FreeSound API](https://freesound.org/docs/api/) (CC0-licensed SFX, 600k+ sounds). Also optional local index for Soundly/Audionetwork collections.

### Repo: `sfx-mcp`
**Ports**: 11120 (backend), 11121 (frontend)
**Stack**: FastMCP 3.4+, FastAPI, httpx (FreeSound), SQLite (local cache)

### Tools

Portmanteau `sfx_search`:

| Operation | Params | Description |
|-----------|--------|-------------|
| `search` | `query`, `duration_max`, `tags`, `page` | Search FreeSound CC0 sounds |
| `download` | `sound_id`, `destination` | Download sound file to local path |
| `tag` | `sound_id`, `tag` | Tag a local sound for later recall |
| `list_local` | `tag` | List locally cached sounds by tag |
| `describe` | `sound_id` | Get metadata: duration, samplerate, tags, description |

Returns: `{"success": true, "sounds": [{"id": 123, "name": "fire-01.wav", "duration": 3.2, "tags": ["fire", "ambient"], "preview_url": "...", "download_url": "..."}]}`

### Config

```env
FREESOUND_API_KEY=your_key_here  # FreeSound API token (free registration)
SFX_LOCAL_PATH=C:/Users/sandr/Music/SFX  # local sound library path
```

### Why CC0?

FreeSound allows filtering by license. CC0 means no attribution required — sounds can be mixed, mashed, and distributed freely. The MCP server filters to CC0 by default.

### Webapp

Single page: search bar + results grid with play buttons and tag chips. Port 11121.

---

## 2. plex-mcp: `extract_clip` Tool

Add to existing `plex-mcp` repo (backend 10856, frontend 10857). Requires FFmpeg on PATH (already on Goliath).

### Tool: `plex_extract`

Portmanteau addition to plex-mcp:

| Operation | Params | Description |
|-----------|--------|-------------|
| `extract_clip` | `media_id`, `start_seconds`, `duration_seconds`, `output_path`, `video_codec` | Extract segment from media file |
| `extract_audio` | `media_id`, `start_seconds`, `duration_seconds`, `output_path` | Extract audio-only segment (no re-encode) |

```python
@mcp.tool()
async def plex_extract(
    operation: Literal["extract_clip", "extract_audio"],
    media_id: str,
    start_seconds: float = 0,
    duration_seconds: float = 30,
    output_path: str | None = None,
    video_codec: str = "copy",
) -> dict:
    """Extract a clip from a Plex media file using FFmpeg.
    
    ## Return Format
    {"success": bool, "file_path": str, "duration": float}
    """
```

### Implementation

```python
import subprocess
ffmpeg_cmd = [
    "ffmpeg", "-ss", str(start_seconds), "-i", media_path,
    "-t", str(duration_seconds),
    "-c", video_codec, "-c:a", "copy",
    "-avoid_negative_ts", "make_zero",
    output_path, "-y"
]
subprocess.run(ffmpeg_cmd, capture_output=True, timeout=300)
```

### Use Case

"Extract the first soliloquy of Richard III" → `plex_extract("extract_clip", media_id="richard-iii-1995", start_seconds=120, duration_seconds=45, output_path="C:/tmp/richard-soliloquy.mp4")`

---

## 3. mixx-dj-mcp: REST Deck Handoff Endpoints

Add to `mixx-dj-mcp/src/mixx_dj_mcp/server.py`:

```python
from pydantic import BaseModel

class DeckLoadRequest(BaseModel):
    track_path: str

@fastapi_app.post("/api/v1/deck/{deck_id}/load")
async def deck_load(deck_id: int, req: DeckLoadRequest):
    bridge = get_osc_bridge()
    bridge.send(f"/deck/{deck_id}/LoadTrack", req.track_path)
    return {"success": True, "deck": deck_id, "track": req.track_path}

@fastapi_app.post("/api/v1/deck/{deck_id}/play_pause")
async def deck_play_pause(deck_id: int, action: str = "toggle"):
    if action == "play":
        bridge.send(f"/deck/{deck_id}/play", 1.0)
    elif action == "pause":
        bridge.send(f"/deck/{deck_id}/play", 0.0)
    else:
        bridge.send(f"/deck/{deck_id}/play", 1.0)  # toggle
    return {"success": True, "deck": deck_id, "action": action}

@fastapi_app.post("/api/v1/deck/{deck_id}/sync")
async def deck_sync(deck_id: int):
    bridge.send(f"/deck/{deck_id}/sync_enabled", 1.0)
    return {"success": True, "deck": deck_id}

@fastapi_app.post("/api/v1/deck/{deck_id}/cue")
async def deck_cue(deck_id: int, mode: str = "cue"):
    bridge.send(f"/deck/{deck_id}/cue_play", 1.0)
    return {"success": True, "deck": deck_id, "mode": mode}
```

These endpoints match the fleet convention from WEBAPP_PORTS.md. Other MCP servers (songgeneration-mcp, plex-mcp via a future handoff) can call them directly via HTTP without needing the MCP tool layer.

---

## 4. End-to-End: Richard III Prompt

```python
# 1. Search Plex for Richard III
result = await plex_search(query="Richard III 1995", type="video")
media_id = result["media"][0]["id"]

# 2. Extract soliloquy clip
clip = await plex_extract(operation="extract_clip",
    media_id=media_id, start_seconds=120, duration_seconds=45)

# 3. Load to mixx deck 1
httpx.post("http://127.0.0.1:11116/api/v1/deck/1/load",
    json={"track_path": clip["file_path"]})

# 4. Separate stems
await mixx_stems(operation="separate", deck=1)
# ... wait for stem_status == 2 ...

# 5. Mute all stems except vocals on sampler 1
await mixx_stems(operation="mute_bass", sampler=1, enable=True)
await mixx_stems(operation="mute_drums", sampler=1, enable=True)
await mixx_stems(operation="mute_other", sampler=1, enable=True)

# 6. Search FreeSound for conflagration
sfx = await sfx_search(operation="search", query="conflagration fire large")
sfx_path = await sfx_search(operation="download",
    sound_id=sfx["sounds"][0]["id"], destination="C:/tmp/sfx/")

# 7. Load SFX to deck 2
httpx.post("http://127.0.0.1:11116/api/v1/deck/2/load",
    json={"track_path": sfx_path})

# 8. Generate Motörhead backing via songgeneration-mcp
gen = await songgen_generate(prompt="Motörhead fast rock riff, 140 BPM, distorted bass",
    duration=60, output_path="C:/tmp/motorhead.wav")

# 9. Load to deck 3
httpx.post("http://127.0.0.1:11116/api/v1/deck/3/load",
    json={"track_path": gen["file_path"]})

# 10. Mix: bring in Motörhead, fade SFX under vocals
await mixx_mixer(operation="crossfader_set", value=0.3)
```


## Implementation Plan

| Step | What | Repo | Effort |
|------|------|------|--------|
| 1 | sfx-mcp: scaffold FastMCP server, FreeSound search/download | new | ~1 session |
| 2 | plex-mcp: add `extract_clip` tool | plex-mcp | ~30 min |
| 3 | mixx-dj-mcp: add REST deck handoff endpoints | mixx-dj-mcp | ~15 min |
| 4 | songgeneration-mcp: verify REST handoff works with mixx-dj-mcp | songgeneration-mcp | ~30 min |
| 5 | E2E test: run the Richard III script with real Plex library | all | ~1 session |
