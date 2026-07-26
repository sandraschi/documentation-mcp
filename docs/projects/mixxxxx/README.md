# Mixxxxx — Video-Enabled Mixxx Fork

**Version**: v0.4

Fork of Mixxx 2.5.6 that adds video playback via bundled FFmpeg. Companion to mixx-dj-mcp (OSC control).

## Features

### v1 (shipped)
- Video decoding via FFmpeg (avcodec/avformat/swscale)
- Companion video file autoload (same basename, .mp4/.mkv/.mov/.webm)
- QPainter-based rendering with aspect-ratio letterbox
- Fullscreen output to secondary monitor
- ControlObjects: video_enabled, video_fullscreen
- Skin element: \<VideoWidget\> in LateNight/Deere
- Library scanner: .mkv/.webm added to format whitelist

### v2 (shipped)
- **VideoMixer**: Singleton compositing all deck video streams with crossfader blending
- **VFX**: Per-deck brightness/contrast/saturation COs (video_brightness, video_contrast, video_saturation)
- **VideoThumbnail**: FFmpeg keyframe extraction, 500-entry LRU cache
- **Hardware decode**: D3D11VA + CUDA via av_hwdevice_ctx_create with software fallback
- **Video output panel**: Detachable fullscreen window for secondary monitor/projector
- **Skin attributes**: show_video_preview (per-deck), show_video_output (output panel)
- **6 new COs**: video_crossfader, video_brightness, video_contrast, video_saturation, video_enabled, video_fullscreen

### Sprint 1 / v3 (shipped)
- **Phase indicator**: PhaseControl reads beat_distance → `[Channel{N}],phase` (0-360). WPhaseIndicator: QPainter arc ring with green→yellow→orange→red color gradient, pulsing when > 180° out of phase. `<PhaseIndicator>` skin element in LateNight.
- **Rekordbox export**: RekordboxExporter reads Mixxx SQLite, writes Pioneer .pdb via libdjinterop. COs: `[Export],rekordbox_usb_path` (string), `[Export],export_crate` (push), `[Channel{N}],export_rekordbox` (push per-deck).

## Build

```powershell
tools\windows_release_buildenv.bat
cd build
cmake -DCMAKE_TOOLCHAIN_FILE="..\buildenv\mixxx-deps-2.5-x64-windows-release-40c29ff\scripts\buildsystems\vcpkg.cmake" -DVCPKG_TARGET_TRIPLET=x64-windows-release -G Ninja ..
ninja
```

## OSC Control (via mixx-dj-mcp)

| CO | Address | Description |
|-----|---------|-------------|
| video_enabled | /deck/[N]/video_enabled | Toggle video on/off |
| video_fullscreen | /deck/[N]/video_fullscreen | Toggle fullscreen window |
| video_brightness | /deck/[N]/video_brightness | Brightness adjustment (0.0–1.0) |
| video_contrast | /deck/[N]/video_contrast | Contrast adjustment (0.0–1.0) |
| video_saturation | /deck/[N]/video_saturation | Saturation adjustment (0.0–1.0) |
| video_crossfader | /video_crossfader | Crossfader video blend (0.0–1.0) |
| phase | /deck/[N]/phase | Beat phase alignment (0–360°) |
| rekordbox_usb_path | /export/rekordbox_usb_path | USB path for Pioneer export |
| export_crate | /export/export_crate | Trigger crate export |
| export_rekordbox | /deck/[N]/export_rekordbox | Trigger per-deck track export |

## Status

- v2 — Build succeeds, exe verified. Hardware decode, VideoMixer, VFX, thumbnails all working.
- v3 (Sprint 1) — Phase indicator and Rekordbox export shipped. COs verified in source.
- v0.4 — All three exporters (Rekordbox, Serato, VDJ) wired to trigger COs via ExportController. Legacy setAudioClock() removed.

## Repository

https://github.com/sandraschi/mixxxxx (branch: video)
