# Troubleshooting

## Server doesn't appear in Claude Desktop
**Cause**: Config JSON is malformed or server crashed at import
**Fix**: Validate the JSON at jsonlint.com; run `uv run python -m huggingface_mcp.server` in a terminal and check for import errors.

## "command not found: uv"
**Cause**: uv not installed or not in PATH
**Fix**: `winget install astral-sh.uv` then restart the terminal.

## Gated model download fails with auth error
**Cause**: Model requires a Hugging Face account + license acceptance; HF_TOKEN not set
**Fix**: Create a read token at https://huggingface.co/settings/tokens, set `HF_TOKEN`, accept the model license on its Hub page, restart.

## register_ollama fails with HTTP 4xx/5xx from Ollama
**Cause**: Ollama not running, wrong OLLAMA_URL, or tag conflict
**Fix**: Start Ollama; verify `curl http://127.0.0.1:11434/api/tags`; use a unique `ollama_tag`.

## register_ollama seems to hang
**Cause**: Large GGUFs take minutes to import; the timeout is 600s
**Fix**: Wait. If it fails after 10 minutes, check Ollama logs.

## dataset_preview returns "not found"
**Cause**: The dataset uses a non-default config/split
**Fix**: Check the dataset's Hub page for config/split names; try `split="validation"` or the documented config.

## Search returns empty results
**Cause**: Query too narrow, or anonymous rate limit hit
**Fix**: Widen the query; add HF_TOKEN for higher rate limits.

## Webapp shows MOCK badges / red "HF token" KPI
**Cause**: Backend runs without HF_TOKEN - the declared MOCK-until-onboarded state
**Fix**: Follow docs/ONBOARDING.md; badges clear when the token is detected.

## Webapp can't reach the backend
**Cause**: Backend not running, or wrong port
**Fix**: `start.bat` boots both; verify `curl http://127.0.0.1:11152/api/health`.

## Infer falls back to HF serverless unexpectedly
**Cause**: `model` not found in local Ollama (HF_INFER_PREFER_LOCAL=1)
**Fix**: `ollama pull <tag>` first, or pass an existing tag as `model`.
