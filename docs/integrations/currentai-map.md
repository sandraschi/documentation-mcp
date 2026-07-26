# Current AI Open Source Stack Gap Map

**Website**: https://map.currentai.org  
**Repo**: https://github.com/currentai-org/os-ai-map  
**License**: MIT  
**Fleet consumer**: `aiwatcher-mcp` (`currentai` tool, port **10946**)

---

## Description

A living map of the open-source AI stack — what exists, how open each piece is, how widely it's used, and where the gaps are. Maintained by Current AI, funded by Patrick Collison and others. Data is curated YAML in `sources/` with a deterministic validation → serialize → render pipeline.

## Dataset structure

| Path | Contains | Records |
|------|----------|---------|
| `sources/products/` | Product metadata (name, display_name, type, description, URLs) | ~458 |
| `sources/scores/` | Per-product openness (0-5 + class), adoption (0-5), capability (0-5) | ~458 |
| `sources/categories/` | Category definitions + ordered product rosters | 15 |
| `sources/organizations/` | Org metadata + product rosters | ~249 |
| `sources/taxonomy.yaml` | 3 arcs × 15 categories (Columbia openness ontology) | 1 |

### Internal normalized schema

```json
{"product": "vLLM", "slug": "vllm", "type": "software",
 "stack_layer": "model_components / inference_code", "category": "inference_code",
 "openness_class": "open_source", "openness_bucket": "open",
 "openness_score": 5, "adoption_level": 4, "capability_score": 5,
 "source_commit": "abc123de", "fetched_at": "2026-07-05T..."}
```

### Stack layers (arcs)

| Arc | Layer | Categories |
|-----|-------|------------|
| **Product / UX** | `product_ux` | orchestration_agents, ui_api, telemetry_observability, safeguards, agent_tools_protocols |
| **Model components** | `model_components` | base_pretrained, finetuned_chat, inference_code, finetuning_code, evaluation_code, benchmark_eval_data, training_synthetic_datasets |
| **Infrastructure** | `infrastructure` | ml_frameworks, deployment, edge_hardware |

### Openness classes

| Class | Bucket | Meaning |
|-------|--------|---------|
| `open_source` | open | OSI-approved license or equivalent |
| `open_weights` | openish | Weights open, no training data or recipe |
| `closed_api` | closed | API-only, no weights or code |
| `open_dataset` | open | Dataset released under open terms |
| `restricted` | closed | Restricted license or access |

## Fleet integration

The dataset is consumed by `aiwatcher-mcp` via its `currentai` portmanteau tool:

| Operation | What it does |
|-----------|-------------|
| `refresh` | Fetch upstream YAML via raw.githubusercontent.com pinned to a commit hash. Store snapshot. |
| `diff` | Compare two snapshots — detect added, removed, openness-reclassified, maturity-changed, adoption-changed products |
| `query` | Lookup products by name or stack layer |
| `gap_report` | Per-layer counts of open / open-ish / closed products |
| `check_dependency` | 11-item fleet watchlist; flags concentration risk (<3 fully-open in a layer) and status changes |

### Watchlist

The [fleet watchlist](https://github.com/sandraschi/aiwatcher-mcp/blob/main/data/currentai/watchlist.json) monitors: vllm, sglang, llama.cpp, fastmcp, qwen, deepseek, starlette, bun, biome, ollama, lm studio.

### Data flow

```
currentai-org/os-ai-map (GitHub, daily commits)
  └── raw.githubusercontent.com/{commit}/sources/*.yaml
        └── aiwatcher-mcp fetcher (async httpx + yaml)
              └── Normalised product records
                    └── data/currentai/snapshots/{date}_{commit}.json
                          └── currentai(operation="diff") → briefing note to advanced-memory
```

## Refresh cadence

The upstream repo sees multiple commits per day (bot auto-regenerates on merge + feature PRs). The `currentai(operation="refresh")` fetches once on demand. Recommended: run daily via aiwatcher scheduler or a manual `just currentai-refresh` recipe.

## Tools

See the [aiwatcher-mcp project page](../projects/aiwatcher-mcp/README.md) and [`docs/CURRENTAI_RECON.md`](https://github.com/sandraschi/aiwatcher-mcp/blob/main/docs/CURRENTAI_RECON.md) for full schema and implementation details.

---

## Tags

`[currentai, os-ai-map, ai-stack, openness, gap-analysis, datasource]`
