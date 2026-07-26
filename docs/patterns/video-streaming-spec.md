# Video Streaming — mixxxxx → Webapp

**Problem**: mixxxxx plays companion video files on a secondary monitor/projector. The webapp (butterchurn-mcp or mixx-dj-mcp Cockpit) shows only generative MilkDrop visuals, not the actual video. DJs who project video want to see the same video feed in the webapp for preview.

## Architecture v1 (Simple — File Polling)

The simplest working approach, good enough for v1:

```
mixxxxx VideoDecoder → QImage → periodic JPEG save → file on disk
                                                          │
                                          mixx-dj-mcp HTTP server
                                                          │
                                          webapp <img src="/api/video/frame">
```

### mixxxxx side (C++)

Add a `VideoFrameExporter` class that runs alongside the decoder:

```cpp
// src/video/videoframeexporter.h
class VideoFrameExporter : public QObject {
    Q_OBJECT
  public:
    explicit VideoFrameExporter(QObject* parent = nullptr);
    void setFrame(const QImage& frame);
    void setOutputPath(const QString& path);
    void setActive(bool active);

  private:
    QImage m_latestFrame;
    QString m_outputPath;
    QTimer* m_saveTimer;
    bool m_active = false;
};
```

```cpp
// src/video/videoframeexporter.cpp
void VideoFrameExporter::setFrame(const QImage& frame) {
    m_latestFrame = frame;
}

void VideoFrameExporter::saveFrame() {
    if (!m_active || m_latestFrame.isNull()) return;
    m_latestFrame.save(m_outputPath, "JPEG", 85); // quality 85
}
```

The timer fires at ~5 fps (200ms interval) — enough for preview, low CPU.

Integrated into `VideoDecoder`: after each decoded frame, call `VideoMixer::instance().setFrame(deck, image)` which stores the latest frame per deck. The exporter reads from the mixer and writes to a file.

**Files**: ~80 lines C++

**Output path**: `%TEMP%\mixxxxx\frame_1.jpg`, `frame_2.jpg`, etc.

### mixx-dj-mcp side (Python)

New REST endpoint:

```python
@fastapi_app.get("/api/video/frame")
async def video_frame(deck: int = 1):
    """Serve the latest video frame for a deck."""
    path = Path(tempfile.gettempdir()) / "mixxxxx" / f"frame_{deck}.jpg"
    if not path.exists():
        return Response(status_code=404, content="No frame available")
    return FileResponse(path, media_type="image/jpeg")
```

With cache control:
```python
return FileResponse(path, media_type="image/jpeg",
    headers={"Cache-Control": "no-cache, must-revalidate"})
```

**Files**: ~20 lines Python

### Webapp side (React)

`<VideoPreview>` component:

```tsx
function VideoPreview({ deck }: { deck: number }) {
    const [frameUrl, setFrameUrl] = useState("");
    const [error, setError] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            const url = `${API_BASE}/api/video/frame?deck=${deck}&t=${Date.now()}`;
            setFrameUrl(url);
        }, 250); // 4 fps
        return () => clearInterval(interval);
    }, [deck]);

    if (error) return <div className="text-slate-500">No video frame</div>;

    return <img src={frameUrl} className="w-full rounded-lg"
        onError={() => setError(true)} />;
}
```

**Files**: ~40 lines TSX

### Limitations of v1

| Issue | Impact | Future fix |
|-------|--------|------------|
| File I/O per frame | ~5ms write, fine for 5fps | Shared memory |
| JPEG encode on main thread | Slight UI stutter | Background thread |
| Polling via <img> | 250ms latency, fine | WebSocket push |
| No audio sync | Visuals only | v2 |

## Architecture v2 (Low Latency — WebSocket)

Replace file I/O with a WebSocket push:

```
mixxxxx → UDP broadcast → mixx-dj-mcp WebSocket server → browser
```

1. VideoDecoder encodes frame as WebP (fast, smaller than JPEG)
2. Sends via UDP to localhost:11130
3. mixx-dj-mcp runs a UDP listener + WebSocket server
4. Webapp connects via `new WebSocket()` and renders on canvas

**Complexity increase**: ~3x v1. Only worth it if DJs complain about v1 latency.

## Implementation Plan

| Step | What | Where | Effort |
|------|------|-------|--------|
| 1 | VideoFrameExporter C++ class | mixxxxx | ~80 lines |
| 2 | Wire into VideoDecoder | mixxxxx | ~10 lines |
| 3 | `/api/video/frame` endpoint | mixx-dj-mcp | ~20 lines |
| 4 | VideoPreview component | webapp | ~40 lines |
| 5 | Test with actual video | — | ~30 min |
