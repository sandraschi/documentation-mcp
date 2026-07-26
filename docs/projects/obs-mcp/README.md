# OBS Studio MCP Server

<p align="center">
  <a href="https://github.com/casey/just"><img src="https://img.shields.io/badge/just-ready_to_go-7c5cfc?style=flat-square&logo=just&logoColor=white" alt="Just"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/PrefectHQ/fastmcp"><img src="https://img.shields.io/badge/FastMCP-3.4-7c5cfc?style=flat-square" alt="FastMCP"></a>
</p>

> 📖 **[Installation Guide](INSTALL.md)** — quick start, manual setup, and troubleshooting

**FastMCP server for OBS Studio automation** — streaming, recording, scenes, audio, multi-target OSC orchestration, and AI media integrations (Streamfog AR lenses, TTS, WorldLabs 3D backgrounds, image/video generation).

**Version 1.6.0** · Python 3.12+ · FastMCP >=3.4 · MIT

## Quick Start

```powershell
git clone https://github.com/sandraschi/obsmcp obs-mcp
cd obs-mcp
just
```

This lists all available recipes. Run `just bootstrap` to install dependencies, then `just serve` or `just dev` to start. See [INSTALL.md](INSTALL.md) for setup without `just`.

### Claude Desktop Integration

Add to `claude_desktop_config.json`:

```json
"mcpServers": {
  "obs-studio-mcp": {
    "command": "uv",
    "args": ["--directory", "D:/Dev/repos/obs-mcp", "run", "obs-studio-mcp"]
  }
}
```

Or build and drag-and-drop the MCPB package (see [Building & Packaging](#building--packaging)).

## Prerequisites

- **Python 3.12+** and [uv](https://docs.astral.sh/uv/)
- **OBS Studio 28.0+** with the WebSocket server enabled
  (OBS → Tools → WebSocket Server Settings → Enable server)
- Optional, for the integration tools: `streamfog-mcp`, `speech-mcp`, `worldlabs-mcp`, and the myAI media backends (see [Configuration](#configuration))

## Tools (36)

All tools are `obs_`-prefixed. Call `obs_help` at runtime for the live, always-accurate registry.

### Core OBS control

| Tool | Description |
|------|-------------|
| `obs_stream_start` / `obs_stream_stop` / `obs_stream_status` | Streaming lifecycle and status (timecode, bytes sent, reconnect state) |
| `obs_recording_start` / `obs_recording_stop` / `obs_recording_status` | Recording lifecycle and status |
| `obs_scenes_list` / `obs_scene_switch` | Scene enumeration and switching |
| `obs_replay_start` / `obs_replay_stop` / `obs_replay_save` | Replay buffer control and highlight capture |
| `obs_virtualcam_start` / `obs_virtualcam_stop` | Virtual camera output |
| `obs_audio_sources` / `obs_audio_mute` | Audio source enumeration and mute control |
| `obs_transition_set` | Scene transition type and duration |
| `obs_status` | Overall OBS status (versions, streaming, recording) |
| `obs_help` | Live tool registry introspection |

### OSC orchestration

| Tool | Description |
|------|-------------|
| `obs_send_osc` | Send OSC messages to configured targets (VRChat, stage gear, other nodes) |
| `obs_list_targets` | Enumerate connection targets from `config/targets.yaml` |

### AI media integrations

| Tool | Description |
|------|-------------|
| `obs_streamfog_status` / `obs_streamfog_set_lens` / `obs_streamfog_clear` / `obs_streamfog_toggle_avatar` | Streamfog AR lens orchestration (via streamfog-mcp) |
| `obs_scene_with_lens` | Atomic scene switch + AR lens activation |
| `obs_speech_list_voices` / `obs_speech_tts` | TTS voiceovers and narration (via speech-mcp) |
| `obs_worldlabs_generate_background` / `obs_worldlabs_list_backgrounds` | AI-generated 3D virtual backgrounds (via worldlabs-mcp) |
| `obs_generate_image` / `obs_generate_video` | Gemini Imagen / Veo 3 media generation (via myAI) |
| `obs_sd_generate` / `obs_sd_img2img` | Local Stable Diffusion / FLUX on the resident GPU |

### Workflows

| Tool | Description |
|------|-------------|
| `obs_list_workflows` | List Arazzo workflow descriptors bundled with the server |
| `obs_agentic_workflow` / `obs_production_assistant` | Multi-step agentic automation (under active development) |

## Configuration

Set environment variables or create `.env`:

```ini
OBS_WS_HOST=localhost
OBS_WS_PORT=4455
OBS_WS_PASSWORD=your_password
LOG_LEVEL=INFO
```

Integration endpoints (Streamfog, speech, WorldLabs, myAI) and their enable flags are configured the same way — see `src/obs_studio_mcp/config.py` for the full list of settings and defaults. OSC targets live in `config/targets.yaml` and can be managed from the webapp Targets page.

## Webapp Dashboard

The repo ships a React dashboard for monitoring and control.

- Frontend (Vite): port **10818**
- Backend (FastAPI REST): port **10819**

```powershell
cd web_sota
.\start.ps1
```

Then open `http://localhost:10818`.

## Building & Packaging

MCPB packaging uses the Anthropic mcpb CLI via Bun (fleet standard):

```powershell
bunx @anthropic-ai/mcpb validate manifest.json
bunx @anthropic-ai/mcpb pack . dist/obs-studio-mcp-v1.6.0.mcpb
```

Or use the repo scripts: `.\build-mcpb.ps1` / `scripts\mcpb-pack.ps1`. Release flow is the fleet triple-play (`just release`).

## Development

```powershell
uv sync --all-extras     # install everything
just lint                # ruff + biome
just fix                 # auto-fix + format
uv run pytest tests/ -v  # tests
```

Quality stack: [Ruff](https://astral.sh/ruff) for Python, [Biome](https://biomejs.dev/) for the webapp, `bandit`/`safety` audits via `just check-sec` / `just audit-deps`, justfile recipes for all fleet operations.

## Usage Examples

```
"Start streaming"
"Switch to the Gameplay scene with the beauty_smooth lens"
"Mute the microphone"
"Save that replay!"
"Generate a cyberpunk city background and list my scenes"
"Send /avatar/parameters/Mute to the VRChat OSC target"
```

## Documentation

- [INSTALL.md](INSTALL.md) — installation and troubleshooting
- [CHANGELOG.md](CHANGELOG.md) — release history
- [ASSESSMENT.md](ASSESSMENT.md) — current project audit
- [docs/adn-notes/](docs/adn-notes/) — technical deep-dives on the server and OBS Studio

## License

MIT
