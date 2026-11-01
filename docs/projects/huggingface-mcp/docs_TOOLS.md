# Tools

One portmanteau tool `hf_hub` with an operation enum, plus three Prefab card
tools. All parameters are `Annotated` + `Field`; docstrings carry
`## Return Format` and `## Examples`.

## hf_hub

| Operation | Purpose | Key params |
|-----------|---------|------------|
| `search` | Search models/datasets/spaces (paginated) | `query`, `repo_type` (model/dataset/space), `limit` (1-100, default 10), `cursor` |
| `get_model` | Repo metadata + README excerpt | `repo_id`, `repo_type` |
| `list_files` | File list with sizes | `repo_id`, `path` (subdir filter) |
| `download` | snapshot_download into depot | `repo_id`, `pattern` (default `*.gguf`), `revision` |
| `register_ollama` | Create Ollama tag from a GGUF | `local_path`, `ollama_tag` |
| `dataset_preview` | First rows of a dataset split | `repo_id`, `split` (default train), `rows` (1-100) |
| `dataset_download` | Dataset snapshot into depot | `repo_id`, `revision` |
| `infer` | chat/text/embedding/image/tts | `task`, `inputs`, `model` |
| `favorites` | list/add/remove saved repos | `favorites_op`, `repo_id`, `repo_type`, `note` |
| `status` | Token, depot, Ollama, recent downloads | - |
| `help` | Operation map with descriptions | - |

### Pagination contract (search)

Returns `{items, has_more, next_cursor}`. Pass `next_cursor` as `cursor` to
fetch the next page; `has_more: false` ends iteration.

### Errors

Every op returns `{success: false, error, error_type, message}` on failure
with actionable suggestions where applicable (auth, validation, upstream,
not_implemented).

## Prefab tools

| Tool | Content |
|------|---------|
| `show_depot_app` | Depot file count, size, recent downloads |
| `show_favorites_app` | Saved favorites list |
| `show_status_app` | HF token, Ollama reachability + models |

## Examples

```
hf_hub(operation="search", query="flux", repo_type="model", limit=5)
hf_hub(operation="get_model", repo_id="black-forest-labs/FLUX.1-dev")
hf_hub(operation="download", repo_id="Qwen/Qwen2.5-1.5B-Instruct-GGUF", pattern="*.gguf")
hf_hub(operation="register_ollama", local_path="D:\\models\\hf\\Qwen--Qwen2.5-1.5B-Instruct-GGUF\\qwen2.5-1.5b-instruct-q4_k_m.gguf", ollama_tag="qwen2.5:q4")
hf_hub(operation="infer", task="chat", inputs=[{"role":"user","content":"hi"}], model="qwen2.5:q4")
hf_hub(operation="dataset_preview", repo_id="squad", split="train", rows=5)
hf_hub(operation="favorites", favorites_op="add", repo_id="org/foo", note="interesting")
hf_hub(operation="status")
```
