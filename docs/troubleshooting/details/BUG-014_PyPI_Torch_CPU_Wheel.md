# BUG-014: PyPI torch wheel is CPU-only - uv sync silently installs CPU torch

| | |
| :--- | :--- |
| **ID** | BUG-014 |
| **Severity** | P1 (silent performance regression: "CUDA out of nowhere gone") |
| **Date** | 2026-08-18 |
| **Component** | Any fleet repo declaring `torch` in `pyproject.toml` |
| **Status** | Fixed in midasheng-gen-mcp; 4 fleet repos at risk (see below) |

## Symptom

Fresh `uv sync --extra model` installs `torch 2.13.0+cpu`. `torch.cuda.is_available()`
returns False on a machine with a healthy RTX 4090. Generation/GPU features
silently run 10-50x slower on CPU. On Goliath this surfaced as
`model_state: not_installed` + `cuda: False` immediately after a successful
install.

## Root Cause

Since torch 2.13 (2026), the PyPI default `torch` wheel is **CPU-only**.
CUDA builds live on the PyTorch index (`https://download.pytorch.org/whl/cu126`).
`uv sync` / `pip install torch` from PyPI therefore installs the CPU wheel
with no error. torch 2.11 and earlier bundled CUDA on PyPI, so existing
lockfiles are unaffected until they re-resolve.

## Resolution (midasheng-gen-mcp)

Pin the CUDA source in `pyproject.toml`:

```toml
[tool.uv.sources]
torch = { index = "pytorch-cu126" }
torchaudio = { index = "pytorch-cu126" }

[[tool.uv.index]]
name = "pytorch-cu126"
url = "https://download.pytorch.org/whl/cu126"
explicit = true
```

Verify: `uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`
must print `2.13.0+cu126 True`.

## Second finding (same session): fp16 broken in MiDashengLM-Gen

`model.half()` loads fine but generation raises `mat1 and mat2 must have
the same dtype, but got Float and Half` even under `torch.autocast`.
Reference impl runs fp32. Fix: load fp32 (~12 GB VRAM on the 4090) with a
`MIDASHENG_DTYPE` env toggle (fp16 documented experimental). Verified:
10 s thunderstorm in 34 s, comedy club scene in ~2.5 min.

## Fleet audit (2026-08-18)

Repos declaring `torch` in pyproject WITHOUT a pytorch CUDA index:

| Repo | Status |
|------|--------|
| local-llm-mcp | FIXED 2026-08-18 (torch 2.6.0+cu126) |
| speech-mcp | FIXED 2026-08-18 (torch/torchaudio/torchcodec +cu126) |
| videogen-mcp | FIXED 2026-08-18 (torch 2.13.0+cu126) |
| songgeneration-mcp | FIXED 2026-08-18 (torch 2.13.0+cu126) |
| kyutai-mcp, ocr-mcp, splatmaker-mcp, midasheng-gen-mcp | OK (index present) |

Note: `mcpb/` staging pyproject twins were included in the scan; the
`mcpb/` copies are build artifacts and must not be edited.

## Log Snippet

```
torch 2.13.0+cpu
cuda available: False
device count: 0
```

## SOTA Impact

New repos with torch deps MUST pin the pytorch CUDA index in
`pyproject.toml` (see midasheng-gen-mcp as reference). The 4 at-risk repos
need the same `[tool.uv.sources]` block before their next `uv sync`.

