# Gradio — Framework, Not Engine (Fleet Stance)

**Status**: Active (dependency of `myai/stablediff_gradio` only) · **License**:
Apache-2.0 · **Language**: Python · **GitHub**:
[gradio-app/gradio](https://github.com/gradio-app/gradio)
**Docs**: <https://gradio.app>
**Fleet decision**: no new Gradio-based projects; consume hosted Gradio apps
via the [HF MCP server](huggingface/README.md); ComfyUI (comfyops-mcp) is the
generative engine of record.

## What Gradio Is

Gradio is a **Python web-UI framework** for wrapping ML models into browser
demos: a few components (`gr.Image`, `gr.Slider`, `gr.Textbox`), ~100 lines,
working demo. It is a *presentation layer*, not an inference engine - the
model/diffusers/ComfyUI backend does the actual work.

This is why it was (and remains) popular for Stable Diffusion / Flux:
AUTOMATIC1111's webui (the SD default UI for years), Forge, and SD.Next all
shipped as Gradio shells, and Hugging Face **Spaces** (community-hosted
demos) are Gradio-first. The framework's simplicity is its superpower: it
lowered the cost of sharing a model demo to near zero.

## The Extension Ecosystem (the actual value add)

Gradio itself stayed minimal; the elaborate apps were built by **extension
systems layered on top**:

- A1111 extensions: ControlNet, LoRA stacks, Tiled VAE, face restore,
  Regional Prompter, upscalers, training UIs - hundreds of community
  extensions.
- The extensions, not the UI shell, carried the capability. The UI was
  interchangeable; the pipeline control was the asset.

**Key historical insight**: by 2026 that extension model is largely legacy.
The A1111/Forge ecosystem stalled, and the power-user crowd (plus model
releases: Flux, Wan, Hunyuan video) migrated to ComfyUI, where custom nodes
fill the same role with a stable, graph-native API.

## Capability Matrix: Gradio + Extensions vs ComfyUI

| Capability | Gradio + A1111/Forge ecosystem | ComfyUI (comfyops-mcp) |
|---|---|---|
| ControlNet | Extension | Native node |
| LoRA stacking / merging | Extension | Native node |
| Upscaling / face restore | Extensions | Native nodes |
| Regional prompting | Extension | Native (regional/conditioning nodes) |
| Video gen (AnimateDiff, Wan, Hunyuan) | Partial, fragile | Native, first-class |
| Batch / queue / jobs | Weak | Native (QueueManager, workflows as API) |
| Reproducibility | Checkpoints, loose | Deterministic graphs, versioned |
| Automation API | Poor (browser-first) | First-class (comfyops-mcp automates it) |
| Custom capabilities | Extension ABI (fragile) | Custom nodes (stable ABI) |
| Time to a working demo | Minutes | Minutes for nodes, steeper for complex graphs |
| Hosting / sharing | Spaces, instant | Self-hosted only |

## Where ComfyUI Wins (fleet default)

- **Automation**: workflows are the API contract. comfyops-mcp drives
  ComfyUI headlessly: curated workflow -> PNG/MP4, job queue, model depot
  (with civitai-mcp for catalog/download). None of that exists for Gradio.
- **Reproducibility**: a saved graph is a deterministic recipe; a Gradio app
  is a loose collection of UI state.
- **Breadth**: image, video, audio, control, custom nodes - one engine.

## Where Gradio Genuinely Still Applies

| Use case | Fleet position |
|---|---|
| Human-facing SD wrapper | **Exists**: `myai/stablediff_gradio` (internal :5196, GPU; host 10905) - keep, do not duplicate |
| Hosted demos we want to *call* | **Consume** via hf-mcp-server bouquet (any Space = a tool), pay nothing |
| Niche model shipped **only** as Gradio/Space | Self-host that wrapper behind `PROXY_TOOLS_CSV` (hf-mcp-server), do not rebuild it |
| New automation / gen capability | ComfyUI via comfyops-mcp; no new Gradio+extensions projects |
| New user-facing surfaces | React/Vite/Tailwind (WEBAPP SOTA), not Gradio |

### Fleet inventory: the existing app (`myai/stablediff_gradio`)

The app is a container inside the myai Docker stack (one of eight services
there), not a standalone repo - and it is **MCP-reachable today**:

| Fact | Value |
|---|---|
| Web UI | Internal :5196 (GPU profile), exposed on host port **10905** (see [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)) |
| MCP tool | `generate_image_gradio` (via myai toolset) |
| Lifecycle tools | `start_ai_service`, `stop_ai_service`, `list_ai_services`, `get_service_status` (myai) |
| Stack | Gradio + Diffusers; needs NVIDIA GPU |
| Status | Running, `[x]` GPU (myai STATUS.md, 2026-07) |

**How an agent uses it**: via the **myai platform MCP server** (wired into the
opencode config 2026-08-05 as `myai`, stdio, 20 tools) - `start_platform` /
`start_ai_service`, ensure the service is up (`list_ai_services` /
`get_service_status`), then call `generate_image_gradio` with the prompt. For
humans, browse to `http://127.0.0.1:10905`.

**Note**: the app is reachable through the platform server, not as a
standalone MCP server - the tool surface is one tool, and the platform server
already exposes it together with service lifecycle. Discovery for the Gradio
app itself lives in this doc.

## Fleet Stance (decision 2026-08-05)

1. **No new Gradio-based projects.** The A1111-style extension ecosystem is
   legacy; ComfyUI custom nodes cover the same ground with a stable API that
   automation can drive.
2. **Existing Gradio surfaces stay.** `myai/stablediff_gradio` remains the
   human-facing SD demo inside myai; migration to ComfyUI is only worth it if
   myai ever needs automation or video.
3. **Hosted Gradio apps are consumed, not hosted.** The HF MCP server bouquet
   turns any Space into an MCP tool; authors pay the hosting bill, we pay
   cold starts and rate limits.
4. **Gradio-only niche models**: self-host the wrapper (cheapest option that
   keeps the model's own UI semantics) behind `PROXY_TOOLS_CSV`; do not
   re-implement the model in ComfyUI unless we need it in automated
   pipelines.
5. **ComfyUI is the engine of record** for image/video/audio generation:
   comfyops-mcp (sidecar 11086, backend 11087, dashboard 11088) + civitai-mcp
   for model supply.

## Cross-references

- [HF MCP server (consuming hosted Gradio apps)](huggingface/README.md)
- [comfyops-mcp project pack](../projects/comfyops-mcp/README.md)
- [myai project (stablediff_gradio)](../projects/myai/README.md)
- [civitai-mcp (model depot supply)](../projects/civitai-mcp/README.md)
- [WEBAPP SOTA (fleet surface standard)](../standards/WEBAPP_SOTA_STANDARDS.md)

## Background

- [Gradio docs](https://gradio.app)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [AUTOMATIC1111 stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [Spaces overview (HF)](https://huggingface.co/docs/hub/spaces-overview)
