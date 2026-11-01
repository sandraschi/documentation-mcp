# Changelog

## [0.1.0] - 2026-08-05

Initial release:

- `hf_hub` portmanteau (11 ops): search, get_model, list_files, download,
  register_ollama, dataset_preview, dataset_download, infer, favorites,
  status, help
- Model depot downloads (GGUF-first) into `HF_DEPOT_ROOT`
- Ollama registration with 600s timeout (fleet parity with unsloth-mcp)
- Dataset preview via datasets-server API, dataset snapshots
- Inference: local Ollama first, HF serverless fallback
- SQLite favorites + download history
- Prefab surfaces: depot, favorites, status cards
- SOTA webapp (11 pages) on 11152/11153
- Dual transport: stdio + HTTP `/mcp`, REST `/api/v1/*`
