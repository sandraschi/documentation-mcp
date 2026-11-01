# huggingface-mcp

Local-first Hugging Face Hub bridge: search models, datasets, and spaces;
download GGUF files into a local depot; register them in Ollama; preview and
download datasets; and run inference through your own hardware or HF
serverless. Not a clone of the official remote hf-mcp-server - the value here
is the local pipeline: search -> download -> register -> infer.

## What You Can Do

- **Search the Hub** - models, datasets, and spaces with pagination
  (`hf_hub` operation `search`)
- **Inspect repos** - downloads, likes, tags, file list with sizes, README
  excerpt (`get_model`, `list_files`)
- **Download to a local depot** - GGUF-first via glob patterns, revision-aware
  (`download`) into `HF_DEPOT_ROOT` (default `D:\Dev\models\huggingface`)
- **Register in Ollama** - one call from GGUF to a working local tag
  (`register_ollama`)
- **Work with datasets** - preview first rows via the datasets-server API,
  download snapshots for training jobs (`dataset_preview`, `dataset_download`)
- **Infer locally** - chat/text/embedding/image/TTS through local Ollama first
  (when the model is installed), HF serverless as fallback (`infer`)
- **Track favorites and downloads** - persisted in SQLite (`favorites`,
  `status`)
- **Rich in-chat cards** - Prefab surfaces for depot, favorites, and status

## Preview

| Dashboard | Models |
|-----------|--------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Models](docs/screenshots/models.png) |

*Screenshots pending - generate with `just screenshots` after first run.*

## Quick Install

Claude Desktop users: download `huggingface-mcp-0.1.0.mcpb` from
[Releases](https://github.com/sandraschi/huggingface-mcp/releases/latest) and
drag it onto the Claude Desktop window. Everything else lives in
[INSTALL.md](INSTALL.md).

## Example Prompts

- "Find the most-downloaded GGUF models for Qwen 2.5"
  -> `hf_hub(operation="search", query="Qwen2.5 GGUF", repo_type="model")`
- "Download FLUX.1-dev GGUF and register it in Ollama as flux1:q4"
  -> download -> `register_ollama`
- "Show me the first 10 rows of the SQuAD dataset"
  -> `hf_hub(operation="dataset_preview", repo_id="squad", split="train")`
- "Chat with my local qwen:q4 model"
  -> `hf_hub(operation="infer", task="chat", model="qwen:q4")`

## Documentation

| Doc | Contents |
|-----|----------|
| [Installation](INSTALL.md) | All install methods, prerequisites |
| [Onboarding](docs/ONBOARDING.md) | HF account + token setup, rate limits, money/CC |
| [Architecture](docs/ARCHITECTURE.md) | System architecture, data flow, ports |
| [Configuration](docs/CONFIGURATION.md) | Env vars, config options |
| [Tool Reference](docs/TOOLS.md) | All available tools and operations |
| [Development](docs/DEVELOPMENT.md) | Contributing, local setup |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues |

## Requirements

- Windows / macOS / Linux, Python 3.11+ (managed via uv)
- Claude Desktop (MCP host) or any MCP-compatible client
- Optional: Ollama (for `register_ollama` + local inference), HF account
  token (gated models + higher rate limits)

## License

Apache-2.0
