# Mixxxxx — Video-Enabled Mixxx Fork

**Status**: Spec v0.1
**Repository**: `https://github.com/sandraschi/mixxxxx`
**Parent**: Mixxx 2.5.6 (tag `2.5.6`)
**MCP companion**: `mixx-dj-mcp` (ports 11116/11117, OSC 11118/11119)

## Why a Fork

Mixxx upstream has explicitly declined video (complexity, maintenance surface, audio-only philosophy). Meanwhile FFmpeg is already in their dependency tree (`avcodec-60.dll`, `avutil-58.dll`, `swresample-4.dll` — shipped in every Windows installer). The GPU pipeline is Qt6 + OpenGL, already proven by the GL waveform/spinny widgets. The delta to add video playback is ~350 lines of C++ and a skin widget.

Video DJs are not a niche — Serato Video, VDJ, Traktor all ship it. "Audio-only" is a self-imposed limitation, not a technical boundary.

## What This Is Not

This is NOT a video mixer. No video effects, no transitions, no chroma key, no karaoke. **v1 is a video frame slapped on top of a playing deck**, synced to the audio engine. You get a second window (or in-deck widget) showing the video file that matches the loaded track. That's it. v2 adds crossfader-aware video blending.

## File Manifest

All new files, no existing file modified outside CMakeLists.txt:

```
src/
├── video/
│   ├── videodecoder.h          # FFmpeg decoder wrapper
│   ├── videodecoder.cpp        # avcodec_send_packet → avframe → QImage
│   ├── videowidget.h           # QOpenGLWidget for rendering
│   ├── videowidget.cpp         # paintGL with texture upload, play/pause/resize
│   ├── videocontrolobject.h    # ControlObject definitions
│   └── videocontrolobject.cpp  # /deck[N]/video_enabled, /deck[N]/video_fullscreen
├── library/
│   ├── video_dao.h             # (add 5 lines to track DAO for video mime types)
│   └── video_dao.cpp           # (add 5 lines)
└── skins/
    └── video_skin.xml          # <VideoWidget> LateNight/Deere insertion
```

**Total**: 10 new files, ~350 lines of C++/Qt6.

## New Control Objects (COs)

| Address | Range | Default | Description |
|---------|-------|---------|-------------|
| `/deck[N]/video_enabled` | 0/1 | 0 | Toggle video playback for deck |
| `/deck[N]/video_fullscreen` | 0/1 | 0 | Pop video to separate fullscreen window |
| `/deck[N]/video_position` | float | — | Current video position (read-only, normalized) |
| `/mixer/video_crossfader` | 0/1 | 0 | Enable video crossfader blending (v2) |

These COs are immediately usable by `mixx-dj-mcp` via the same OSC protocol — no MCP server changes for basic control, just add `video_enable`, `video_fullscreen` ops to the existing `mixx_deck` portmanteau.

## Decoder Architecture

```
Mixxx engine loop → Track loaded → Check for companion video file
    │ (same directory, same basename, .mp4/.mkv/.mov)
    ▼
videodecoder.cpp opens FFmpeg (avformat_open_input)
    │
    ├── Audio: NOT decoded here — engine handles it
    └── Video: avcodec_send_packet → avframe → sws_scale → QImage → OpenGL texture
         │
         ▼
videowidget.cpp paintGL → bind texture → draw quad → swap
```

Video is decoded on a background thread and frame-synced to the engine's audio clock (`track_samples` / `track_samplerate` → `av_seek_frame` on mismatch). No attempt at A/V sync beyond this — FFmpeg's native timing is reliable enough for DJ use where millisecond precision isn't expected.

**Companion video file discovery**: When a track is loaded, look for `{track_basename}.mp4`, `.mkv`, `.mov` in the same directory. If found, autoload. This mirrors the Serato Video `.svd` convention without requiring a database change.

## CMake Changes

In the existing `CMakeLists.txt`:

```cmake
# Add to existing find_package for FFmpeg (already present for audio codecs)
find_package(PkgConfig)
pkg_check_modules(AVCODEC libavcodec>=60)
pkg_check_modules(AVFORMAT libavformat)
pkg_check_modules(SWSCALE libswscale)

# Add to mixxx-lib target
target_sources(mixxx-lib PRIVATE
    src/video/videodecoder.cpp
    src/video/videowidget.cpp
    src/video/videocontrolobject.cpp
)
target_link_libraries(mixxx-lib PRIVATE
    ${AVCODEC_LIBRARIES}
    ${AVFORMAT_LIBRARIES}
    ${SWSCALE_LIBRARIES}
)
```

No new external dependencies. The FFmpeg DLLs are already shipped.

## Skin Integration

Add to LateNight or Deere skin XML:

```xml
<WidgetGroup>
    <Size>200,150</Size>
    <Children>
        <VideoWidget>
            <Name>Deck1Video</Name>
            <Size>200,150</Size>
            <VideoEnabledControl>/deck/1/video_enabled</VideoEnabledControl>
        </VideoWidget>
    </Children>
</WidgetGroup>
```

On first launch, a `<VideoWidget>` appears in the default skin showing "No video" text. When `/deck/1/video_enabled` toggles on, it opens the companion file and renders.

## Fullscreen Window

When `/deck[N]/video_fullscreen` is set to 1, the videowidget detaches from the skin and opens a standalone `QWindow` with no chrome on the secondary monitor (detected via `QGuiApplication::screens()`). Closing the window resets the CO to 0. This is the primary use case for actual DJing — video on a projector, skin on the laptop.

## Build Pipeline

```powershell
# Same as upstream Mixxx Windows build:
cd mixxxxx
mkdir build && cd build
cmake -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release
cpack -G NSIS
```

Output: `Mixxxxx-2.5.6-video-win64.exe`

The existing build.ps1 in `mixx-dj-mcp/native/` needs no changes — it builds the MCP server's backend, not Mixxx.

## Installation

1. Uninstall Mixxx (keep library database at `%LOCALAPPDATA%\Mixxx\mixxxdb.sqlite`)
2. Install Mixxxxx — reads the same database path
3. Enable OSC: Preferences → MIDI/OSC → port 11118/11119
4. Start mixx-dj-mcp server
5. Open webapp or connect AI assistant

No migration needed. The fork uses the same database schema, same controller mappings, same skins (plus the new VideoWidget).

## MCP Server Integration

In `mixx-dj-mcp`, add to `mixx_deck` operations:

| Operation | Params | OSC address |
|-----------|--------|-------------|
| `video_enable` | `deck`, `enable` | `/deck/{deck}/video_enabled` |
| `video_fullscreen` | `deck`, `enable` | `/deck/{deck}/video_fullscreen` |

That's two additions to `deck_control.py`'s `Literal` enum and two `if/elif` branches. OSC protocol is unchanged — the new COs are just new addresses the server sends to port 11119.

## Build & Release

```powershell
# Create fork from tag
cd D:\Dev\repos
gh repo fork mixxxdj/mixxx --clone --fork-name mixxxxx
cd mixxxxx
git checkout 2.5.6
git checkout -b video

# Apply patch files
copy D:\Dev\repos\mixx-dj-mcp\patches\mixxxxx\* src\video\
# Apply CMake changes manually (~5 lines)

# Build
cd build
cmake -G "Visual Studio 17 2022" -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release

# Ship
cpack -G NSIS
# Upload to GitHub Releases
```

First release tag: `v2.5.6-video.1`

## Non-Goals (v1)

- Video transitions / effects / chroma key
- Video library browsing (use filesystem, mirror existing track)
- Video recording
- Streaming video input
- MIDI mapping for video controls (COs suffice)
- Video mixing (crossfader-aware blending is v2)
- DRM / stream-ripped video content

## v2 Considerations

- Crossfader-aware blending: route crossfader to video opacity on the widget
- AlphaMask video transition (template from VDJ's video crossfader)
- Deck 3-4 video support
- Skins with embedded video thumbnails in library browser
- Performance: hardware decode via `cuvid`/`dxva2` if available, fallback to swscale
