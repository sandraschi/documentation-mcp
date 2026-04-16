# worldlabs-mcp - Status

**Repository**: [worldlabs-mcp](https://github.com/sandraschi/worldlabs-mcp)
**FastMCP Version**: v1.2.0 (Stable Simulation)
**Status**: 🟢 PRODUCTION
**Last Updated**: 2026-02-23

## Overview

MCP server wrapping the [World Labs Marble API](https://docs.worldlabs.ai/api). Generates navigable 3D worlds (Gaussian splats, collision mesh, panorama) from text prompts, images, multi-image sets with azimuth angles, and video. Includes end-to-end local file upload flow.

## Tool Summary

| Tools | Pattern |
|-------|---------|
| 11 | Direct (no portmanteau — API is already flat) |

## Tools

| Tool | Description |
|------|-------------|
| `generate_world_from_text` | Text prompt → async Operation |
| `generate_world_from_image` | Public image URL → Operation (panorama flag) |
| `generate_world_from_multi_image` | Multiple images + azimuth angles → Operation |
| `generate_world_from_video` | Public video URL → Operation |
| `upload_and_generate` | Local file → GCS upload → Operation (end-to-end) |
| `prepare_media_upload` | Get signed GCS upload URL (manual flow) |
| `generate_world_from_media_asset` | Uploaded asset ID → Operation |
| `get_operation` | Single status poll |
| `wait_for_world` | Blocking poll — raises RuntimeError on failure, TimeoutError |
| `list_worlds` | Paginated world listing |
| `get_world` | Fetch world details + asset URLs by ID |

## Models

| Model | Speed | Quality | Use case |
|-------|-------|---------|----------|
| `Marble 0.1-mini` | ~30-45s | Good | **Default** — iteration, testing |
| `Marble 0.1-plus` | ~5min | Best | Final quality output |

## Output Assets

Each generated world provides:
- **Gaussian splats** (SPZ) at 100k, 500k, full resolution
- **Collision mesh** (GLB) for physics/game engines
- **360 panorama** (JPEG)
- **Thumbnail** (JPEG)
- **AI caption** — auto-generated scene description
- **Marble viewer URL** — direct browser preview

## Structure

```
worldlabs-mcp/
├── src/worldlabs_mcp/
│   ├── __init__.py
│   ├── __main__.py
│   └── server.py          # All 11 tools
├── tests/
│   ├── conftest.py        # Fixtures (fake operations, worlds)
│   └── test_server.py     # 20+ tests, pytest-httpx mocks
├── scripts/
│   ├── run_server.py      # stdio + HTTP modes
│   └── run_tests.py
├── .github/workflows/ci.yml
├── glama.json
├── mcp_config.json
├── pyproject.toml
├── CHANGELOG.md
├── CONTRIBUTING.md
└── SECURITY.md
```

## CI/CD

- ✅ GitHub Actions (Python 3.10 / 3.11 / 3.12 matrix)
- ✅ Ruff linting
- ✅ pytest + pytest-httpx (all HTTP mocked)
- ⬜ Glama publication (pending)
- ⬜ mcpb packaging (pending)

## Installation

```json
{
  "mcpServers": {
    "worldlabs-mcp": {
      "command": "uvx",
      "args": ["worldlabs-mcp"],
      "env": {
        "WORLDLABS_API_KEY": "your-key-here"
      }
    }
  }
}
```

Local dev:
```json
{
  "mcpServers": {
    "worldlabs-mcp": {
      "command": "python",
      "args": ["D:/Dev/repos/worldlabs-mcp/scripts/run_server.py"],
      "env": {
        "WORLDLABS_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Requirements

- Python 3.10+
- World Labs account + API key: https://platform.worldlabs.ai/api-keys
- Credits consumed per generation

## Known Limitations

- Generation is async — operations can take 30s–5min depending on model
- No streaming progress; `wait_for_world` polls every 15s by default
- `upload_and_generate` requires local file to be readable by the MCP server process
- Multi-image azimuth support not yet confirmed against live API (spec-based implementation)
