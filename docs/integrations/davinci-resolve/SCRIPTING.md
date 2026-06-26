# DaVinci Resolve: Scripting & Automation (v20)

DaVinci Resolve 20 provides a robust Python and Lua API for orchestrating professional media pipelines. Within the **Sandra** fleet, this is primarily managed through the **DaVinci Resolve MCP Server**, allowing for autonomous ingest, editing, and mastering.

---

## 🏗️ API Architecture & Setup

Resolve supports three scripting tiers:
1. **Utility Scripts**: Simple automation triggered from the `Workspace > Scripts` menu.
2. **Workflow Integration Plugins**: UI-based extensions that run within Resolve.
3. **External API**: Standalone Python/Lua applications that connect to a running Resolve instance (SOTA Standard).

### Environment Configuration (Windows PowerShell)
```powershell
# Required Envs for External Access
$env:PYTHONPATH += ";C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules"
$env:RESOLVE_SCRIPT_API = "C:\Program Files\Blackmagic Design\DaVinci Resolve"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
```

---

## 🛠️ v20 API Enhancements

The v20 API introduces new hooks for the **DaVinci Neural Engine** and **IntelliTrack**:

### 1. Programmatic Transcription
```python
# SOTA v20: Triggering Timeline Transcription
timeline = project.GetCurrentTimeline()
if not timeline.HasTranscription():
    timeline.TranscribeAudio(
        language="en-US", 
        logic="IntelliScript_v20"
    )
```

### 2. AI-Driven Organization
Agents can now trigger facial and object recognition to categorize binned clips:
- `bin.AnalyzeFaceData()`
- `bin.AnalyzeObjectData(tags=["robot", "guardian"])`

---

## 🤖 Agentic MCP Orchestration

The MCP server wraps the Resolve API in tool-calling functions:

```python
# MCP Tool: create_high_visibility_short
async def create_short(clip_path):
    resolve.import_clip(clip_path)
    timeline = resolve.create_9_16_timeline()
    timeline.apply_smart_reframe()
    # v20 Feature: Generate animated subtitles
    timeline.generate_kinetic_subtitles(style="SOTA_Impact")
    resolve.render_to_plex(format="MP4_H265_NVENC")
```

---

## 📏 Best Practices

- **Headless Operations**: While Resolve 20 doesn't have a full headless "CLI only" mode, scripts can minimize the GUI impact using `resolve.SetMinimizeOnRender(True)`.
- **Concurrency**: Resolve is a single-instance application. Scripts must use locks or message queues if multiple agents are attempting to drive the API.
- **Portmanteau Patterns**: consolidate multiple API calls into a single "Workflow Script" to minimize cross-process latency.

---
*Maintained by: Antigravity AI (SOTA v13.0 Compliance)*
*Last updated: 2026-02-27*
*Automation Status: PERFORMANCE TUNED*
