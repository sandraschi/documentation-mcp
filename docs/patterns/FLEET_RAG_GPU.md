# Fleet GPU RAG (LanceDB + FastEmbed + CUDA)

Standard for repos that embed into LanceDB with **fastembed** + **BAAI/bge-small-en-v1.5**.

## Repos

| Repo | Index command | Notes |
|------|---------------|--------|
| **mcp-central-docs** | `just rag-gpu` | Reference implementation |
| **documentation-mcp** | `just rag-gpu` | Public docs fork |
| **calibre-mcp** | `just rag-gpu-metadata` | Metadata LanceDB index |
| **plex-mcp** | `just rag-gpu-sync` | Plex metadata sync |
| **advanced-memory-mcp** | `just rag-gpu` | POST `/search/reindex` (API must be running) |
| **arxiv-mcp** | `just rag-gpu` | Paper chunk reindex |
| **depot-mcp** | `just rag-gpu` / `just rag` | Re-embed indexed depot files |
| **speech-mcp** | `just rag-gpu` | Docs LanceDB reindex |
| **robofang** | `just rag-gpu` | Index `docs/` markdown |

## One-time install (per repo venv)

```powershell
just rag-gpu-install   # ~1.5 GB NVIDIA pip CUDA 12 runtimes + onnxruntime-gpu
```

## Run GPU embed

```powershell
just rag-gpu           # or repo-specific recipe above
```

**Do not** use `uv run` for embed jobs while GPU mode is active — it reinstalls CPU `onnxruntime` from `pyproject.toml`.

Revert: `just rag-cpu-install`

## Python

Copy `standards/patterns/fleet_fastembed_gpu.py` into the repo and call `create_text_embedding()` from vector store / ingest code.

Env flags (either works):

- `RAG_GPU=1` — fleet generic
- `MCD_RAG_GPU=1` — legacy alias
- `.venv/rag-gpu-mode` — written by `rag-gpu-install`

Batch sizes: CPU 64, GPU 256.

## PowerShell scripts (copy set)

| Script | Role |
|--------|------|
| `scripts/rag-gpu-env.ps1` | CUDA DLL PATH + mode detection |
| `scripts/rag-python.ps1` | Venv python + PATH (not `uv run`) |
| `scripts/enable-rag-gpu.ps1` | Install + verify CUDA session |
| `scripts/enable-rag-cpu.ps1` | Restore CPU stack |
| `scripts/run-rag-gpu*.ps1` | Repo-specific reindex entry |
| `scripts/just/rag-gpu*.ps1` | Thin justfile delegates |

## Justfile rule

Never inline `$env:VAR=...` in justfile bodies — `just` eats `$` on Windows. Always `-File scripts/just/...ps1`.

See also: [ai-rag-2026.md](../core/ai-rag-2026.md), mcp-central-docs `scripts/just/README.md`.
