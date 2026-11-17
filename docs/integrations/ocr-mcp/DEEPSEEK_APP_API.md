# DeepSeek app API, and the ocr-mcp cloud backend

**Date:** 2026-11-14
**Repos:** `ocr-mcp`, `craft-ai`, `codercraft`, `writercraft`, `travelcraft`, `aicraft`
**Official guide:** https://api-docs.deepseek.com/guides/build_a_chatbot/
**OCR reference:** https://api-docs.deepseek.com/guides/ocr/
**Pricing:** https://api-docs.deepseek.com/quick_start/pricing

DeepSeek opened the consumer app to API callers on 2026-11-14. One key now covers web search, page reading, file input, a basic safety check, conversation titles, and three standalone tools: OCR, speech-to-text, and text-to-speech. The model id for the chat features is `deepseek-flash` (weights `DeepSeek-V4.1-Flash-1017`).

This note is the fleet record of what that API actually is, which call belongs in which app, and how `ocr-mcp` exposes the OCR half.

## Two DeepSeek OCR products

These names get mixed up. They are different programs.

| Name in this fleet | What it is | Where it runs | What you get back |
| --- | --- | --- | --- |
| `deepseek-ocr2` | Local DeepSeek-OCR-2 weights (about 3B parameters, about 6 GB) | The GPU, inside `ocr-mcp` | Layout-capable local OCR. The alias `deepseek` still means this backend |
| `deepseek-api` | `POST https://api.deepseek.com/v1/tools/ocr` | DeepSeek's cloud | Raw page text. No boxes, no tables, no form fields |
| `deepseek-flash` | Chat model | DeepSeek's cloud | A completion. Search and URL reading are tools on this call. OCR is not one of them |

Asking the chat model a question about a document is a third path, File Parsing. Upload with `POST /files` and a purpose, then pass the returned `file_id` on a later chat request. That path is not wired. OCR and File Parsing both accept PDF, Word, PowerPoint, and images, and they bill the same page rate, but only File Parsing puts the document into a conversation.

## What the standalone tools are

The chat request does not transcribe audio, speak, or OCR. Those are separate endpoints. A client that wants all three makes three calls.

| Tool | Method and URL | Body | Reply |
| --- | --- | --- | --- |
| OCR | `POST https://api.deepseek.com/v1/tools/ocr` | `multipart/form-data` with `purpose` and `file` | One JSON object, page by page |
| Speech to text | `POST https://api.deepseek.com/v1/tools/asr` | `multipart/form-data` with `file` | JSON: `text`, `duration_ms` |
| Text to speech | `POST https://api.deepseek.com/v1/tools/tts` | JSON: `text`, optional `voice_id`, `format` | The audio bytes themselves (`audio/wav` or raw PCM) |
| Web search and page read | `POST https://api.deepseek.com/chat/completions` (also Messages and Responses) | JSON tools `deepseek_web_search` and `deepseek_read_url` | Content blocks: thinking, search, page reads, text, citations |

Auth for all of them is `Authorization: Bearer $DEEPSEEK_API_KEY`.

### OCR request

Both form fields are required. Any other field is a 400.

| Field | Values |
| --- | --- |
| `file` | PDF, DOC, DOCX, PPT, PPTX, PNG, JPEG, WebP, GIF, BMP, TIFF. The format is detected from the bytes, not the extension |
| `purpose` | `text_recognition` (default here) or `rich_layout_recognition` |

`text_recognition` extracts Word and PowerPoint text directly when the file has no pictures. Everything else is recognized page by page. `rich_layout_recognition` recognizes every file page by page. The OCR endpoint still returns text. It does not return cropped figures. Figures in a chat context are a File Parsing feature (`rich_layout_recognition` on `POST /files`), not this call.

Limits:

| Limit | Value | HTTP status when exceeded |
| --- | --- | --- |
| File size | 100 MiB | 413 |
| Pages | 1,000 | (request rejected) |
| Upload | Must finish within 120 seconds, with no pause longer than 30 seconds | 408 |
| Total time | 180 seconds from the start of the upload, including recognition | 408 |

While recognition runs, the service writes newline bytes to keep the connection open, then writes one JSON object. Those newlines are leading whitespace. `json.loads` after a left-strip is the right parse. A client that does `response.json()` on a body that starts with newlines can fail.

Example body, shortened:

```json
{
  "id": "ocr-9b2f4c1e",
  "object": "ocr.result",
  "purpose": "text_recognition",
  "page_count": 2,
  "pages": [
    {"index": 0, "text": "...", "finish_reason": "stop"},
    {"index": 1, "text": "...", "finish_reason": "length"}
  ],
  "usage": {"input_tokens": 1536, "output_tokens": 412, "total_tokens": 1948}
}
```

`pages[].text` is the raw model output. There is no cleanup pass. `finish_reason: "length"` means that page hit the output cap and the text is incomplete. `ocr-mcp` appends `[page truncated]` on that page. `usage` is reported for reference and is not the billing meter. Billing is per page.

The file is not stored in the Files API and cannot be downloaded later. A failed call is not billed.

### Speech to text

One audio file in, one transcript out. Streaming recognition is not supported.

| Limit | Value |
| --- | --- |
| Format | 16-bit PCM WAV, or Ogg Opus, detected from the bytes |
| WAV sample rates | 8000, 16000, 22050, 24000, 32000, 44100, 48000 Hz |
| Channels | Mono or stereo. Stereo uses the left channel only |
| Size | 8 MiB, and the upload must finish within 10 minutes |
| Duration | 120 seconds |

```json
{"request_id": "...", "text": "...", "duration_ms": 3200}
```

### Text to speech

| Field | Required | Notes |
| --- | --- | --- |
| `text` | yes | At most 10,000 billed characters. Body at most 64 KiB |
| `voice_id` | no | `stella` (default) or `tide` |
| `format` | no | `wav` (default) or `pcm` |
| `filter_markdown` | no | Default true. Markdown markers are stripped before reading |

`wav` is `audio/wav`. `pcm` is raw 16-bit mono PCM at 24 kHz. Audio is streamed as it is synthesized. One request returns at most 30 minutes. A JSON body that starts with `{` is an error, not a wav.

There is also a WebSocket at `wss://api.deepseek.com/v1/tools/tts` for sending text in chunks while a model is still generating. The fleet calls the full-text POST only.

### Chat tools, and the settings they erase

A streaming or non-streaming chat call opts in with:

```json
{
  "model": "deepseek-flash",
  "thinking": {"type": "enabled"},
  "tools": [
    {"type": "deepseek_web_search"},
    {"type": "deepseek_read_url"}
  ],
  "messages": [{"role": "user", "content": "..."}]
}
```

The same features exist on three endpoints:

| Protocol | URL |
| --- | --- |
| Messages | `POST https://api.deepseek.com/anthropic/v1/messages` |
| Responses | `POST https://api.deepseek.com/responses` |
| Chat Completions | `POST https://api.deepseek.com/chat/completions` |

The service runs search and page reads. The client draws the blocks and sends them back unchanged on the next turn. Block types are `thinking`, `server_tool_use` plus `web_search_tool_result` or `web_fetch_tool_result`, and `text` with citations. `stop_reason: "refusal"` means the safety check rejected the turn.

When the request declares `deepseek_web_search` or `deepseek_read_url`, sets `safety_check` to `high`, or enables `title`, DeepSeek ignores the caller's sampling. On Chat Completions that list is `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`, `stop`, `seed`, `n`, `preserve_thinking`, and `parallel_tool_calls`. `max_tokens` still applies, and it caps each inference step inside the round, not the whole round.

That is why a code loop that needs a fixed temperature must not turn those switches on. A research call that wants citations should turn them on and accept that temperature is no longer yours.

The safety check is described by DeepSeek as basic risk control. A public service still has to do its own review, registration, and labeling. The open-source chat demo keeps the API key in the browser and is for demonstration only.

## Price, checked 2026-11-14

Off-peak `deepseek-flash` token rates. Peak hours are double, and they are weekday 01:00-04:00 and 06:00-10:00 UTC. Weekends and Chinese public holidays are off-peak all day.

| Meter | Off-peak |
| --- | --- |
| Input, cache miss | $0.15 / 1M tokens |
| Input, cache hit | $0.003 / 1M tokens |
| Output | $0.60 / 1M tokens |
| Search (text or image) | $0.75 / 1,000 searches |
| Web fetch | $0.75 / 1,000 fetches |
| File parsing and the OCR API | $0.225 / 1,000 pages |
| Text to speech, list / sale | $0.45 / $0.225 per 10,000 characters |
| Speech to text, list / sale | $0.116 / $0.058 per hour |

A 40-page OCR job is under a cent. The cost is not the reason to hesitate. The document leaves the machine.

US labs already sell the server-side search shape. Their search call fees, on the same date, are higher. Fetch and file handling are not the same product, so this table is only the search line and the file shape.

| Vendor | Search call | Page read | Attached files |
| --- | --- | --- | --- |
| DeepSeek `deepseek-flash` | $0.75 / 1,000 | $0.75 / 1,000 | OCR or File Parsing at $0.225 / 1,000 pages, inside the turn for File Parsing |
| OpenAI Responses `web_search` | $10 / 1,000, plus result tokens | `open_page` on the same tool | File search is a stored vector index at $2.50 / 1,000 calls, plus storage |
| Anthropic `web_search` | $10 / 1,000, plus result tokens | `web_fetch` has no tool fee. The page is billed as input tokens | PDF on the message |
| Gemini 3 Google Search grounding | $14 / 1,000 after 5,000 free searches a month | URL context, billed as input tokens | Native PDF and image tokens |

DeepSeek's search fee is about 13 times below OpenAI and Anthropic, and about 19 times below Gemini 3. A fetched page can still cost more in tokens than the $0.00075 fetch fee. Anthropic charges no fetch fee and then bills the page as input. Those are not the same bill.

## Where the fleet calls it

The key is `DEEPSEEK_API_KEY`, or the `deepseek_api_key` field in `%USERPROFILE%\.craft\ai_config.json` for the Rust apps. `ocr-mcp` reads `DEEPSEEK_API_KEY` or `OCRConfig.deepseek_api_key`. It does not read the craft-ai JSON file.

### ocr-mcp

Backend id: `deepseek-api`.
Class: `DeepSeekApiOcrBackend` in `src/ocr_mcp/backends/deepseek_api_backend.py`.

Select it by name:

```text
process_document(source_path="C:/scans/contract.pdf", backend="deepseek-api")
```

Aliases `deepseek-cloud` and `deepseek-ocr-api` map to it. The alias `deepseek` still maps to `deepseek-ocr2`. That split is deliberate. A caller who says "deepseek" keeps the local weights.

Auto selection does not prefer this backend. The fallback order reaches it only after Indra, Tesseract, the small local engines, PaddleOCR-VL, and Mistral, and only when a key is present. A machine with Tesseract installed will not send a scan to DeepSeek just because the key is in the environment.

The tool result is the usual OCR dict: `success`, `text`, a heuristic `confidence` that is explicitly not a model score, and `metadata` with `pages`, `truncated_pages`, `purpose`, `ocr_id`, and `estimated_usd` at $0.000225 per page. Language hints and crop regions are ignored and recorded as ignored. The API has no place to put them.

`DEEPSEEK_OCR_PURPOSE` overrides the purpose. Allowed values are `text_recognition` and `rich_layout_recognition`. Anything else falls back to `text_recognition`.

What this backend will not do:

- Bounding boxes, reading order, tables, or form fields. Form reconstruction stays on the local engines.
- Offline OCR. No key, no call.
- A chat answer about the document. Paste the page text into a later chat call if you need that, or use File Parsing, which is not implemented here.
- The local `deepseek-ocr2` path. That backend is unchanged.

### Craft apps

These call `craft-ai-core` (`crates/craft-ai-core/src/deepseek.rs`), not `ocr-mcp`.

| App | Control | Call |
| --- | --- | --- |
| CoderCraft | LLM settings provider `deepseek`, then Send | `complete_flash`. No search tools, so temperature stays 0.2. Other providers still get the local stub |
| WriterCraft | Companion: "Search and cite", and "Read file (OCR)" | `research` (search plus URL reading) and `ocr_file`. The chapter draft stays the local template |
| TravelCraft | Sight Chat: "live web", "Transcribe", "Read aloud" | `research`, `transcribe_file` (WAV or Ogg Opus into the Ask box), `speak_to_file` (wav in the temp directory, voice `stella`) |
| AICraft | Model card | `deepseek-flash` listed at the off-peak token rates. The route button still prints an estimate and does not place the call |

CoderCraft must not enable search on a code edit. WriterCraft and the TravelCraft live-web checkbox are the calls that want citations and therefore give up temperature.

ContractCraft, HireCraft, and DeskCraft do not call this API. A cheap page is still a contract, a resume, or a customer ticket leaving the machine.

## When to pick which OCR

| Situation | Use |
| --- | --- |
| Scan on the flatbed, forms, tables, boxes, no network | `indra-ocr`, `tesseract`, or `deepseek-ocr2` |
| Academic PDF, local GPU, layout matters | `deepseek-ocr2`, `olmocr-2`, `paddleocr-vl` |
| No GPU, or the file is DOC, DOCX, PPT, or PPTX, and page text is enough | `deepseek-api` |
| Cloud OCR that returns markdown and structured layout, and the Mistral price is acceptable | `mistral-ocr` |
| You need the model to answer a question about a chart inside the file | File Parsing on `deepseek-flash`, not `deepseek-api` |

Mistral OCR in this repo is the other cloud engine. It posts a base64 image to `https://api.mistral.ai/v1/ocr` and joins per-page markdown. It is aimed at layout. DeepSeek's OCR tool is aimed at cheap page text, including Office files the local engines do not open. Keep both. Do not collapse them into one "cloud" switch.

## Operator notes

1. Set `DEEPSEEK_API_KEY` in the environment of the `ocr-mcp` process. The web app and the MCP server share `OCRConfig`, so a key present at process start is enough. Changing the key later needs a process restart unless a settings endpoint is added later. Mistral has one. DeepSeek does not, yet.
2. Call `backend="deepseek-api"` on purpose. Do not rename the local backend.
3. Expect raw text. If a page ends with `[page truncated]`, that page hit `finish_reason: "length"` and the rest of that page is missing.
4. Budget 180 seconds. The client timeout in `ocr-mcp` is 180 seconds, matching the service limit.
5. Treat the heuristic confidence as a text-density hint. Do not threshold a workflow on it the way you would threshold Tesseract word confidence.
6. For speech, use TravelCraft or `craft_ai_core::deepseek`. `ocr-mcp` does not transcribe or speak.
