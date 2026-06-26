# Handbrake High-Efficiency Video Transcoding

The Handbrake MCP integration provides a specialized CLI-driven service for standardized video transcoding across the media fleet. It ensures that all recorded walkthroughs, research clips, and plex media are optimized for bandwidth and compatibility.

## 🚀 Deployment & Pipeline

### Engine Configuration
- **Binary**: `HandBrakeCLI.exe` (Windows SOTA).
- **Core Strategy**: Hardware-accelerated encoding via **NVIDIA NVENC** (RTX 4090).
- **Format Standard**: `.mp4` (H.264/H.265) for universal fleet compatibility.

### MCP Registration
```json
{
  "handbrake": {
    "command": "python",
    "args": ["-m", "handbrake_mcp.server"],
    "cwd": "D:/Dev/repos/handbrake-mcp",
    "env": {
      "HANDBRAKE_CLI_PATH": "C:/Program Files/HandBrake/HandBrakeCLI.exe"
    }
  }
}
```

## 📼 Batch Processing Tools

### Transcode Presets
| Preset | Capability | Description |
| :--- | :--- | :--- |
| `SOTA_WALKTHROUGH` | 1080p60 NVENC | Optimized for low file size with high text legibility. |
| `PLEX_OPTIMIZED` | 4K HDR | Maximum fidelity for the home cinema fleet. |
| `MOBILE_FAST` | 720p30 | Low-bitrate preview for iOS/iPad remote access. |

### Operational CLI
- **`transcode_video`**: Primary entry point for converting files in the `D:/Dev/repos` scratch space.
- **`get_preset_list`**: Query available SOTA-compliant encoding configurations.
- **`abort_job`**: Immediate termination of active transcoding tasks to reclaim GPU resources.

## 🛠️ Advanced Fleet Integration

### Automated Ingestion Workflow
Agents use the Handbrake MCP to automatically process OBS recordings:
1. **OBS** captures a 10GB raw MKV.
2. **Handbrake** transcodes it into a 500MB MP4 using the `SOTA_WALKTHROUGH` preset.
3. **Immich** indexes the final file for archival.

## 📊 Performance Governance
- **GPU Utilization**: Ensure NVENC cores are available. Handbrake takes priority over background tasks but yields to real-time rendering (Blender).
- **Temp Storage**: Use the NVMe drive for temporary cache to prevent I/O bottlenecks.

---
*Maintained by: Antigravity AI (SOTA v12.1 Compliance)*
*Last updated: 2026-02-14*
*Fleet Status: Active*
