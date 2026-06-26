"""LLM client: Ollama (list models + chat), OpenAI-compatible (chat + list models / LM Studio).
No hardcoded model lists; supports auto-discovery and resilient fallback.
"""

import json
import logging
from typing import Any, AsyncGenerator

import aiohttp

logger = logging.getLogger(__name__)

OLLAMA_LIST_URL = "/api/tags"
OLLAMA_CHAT_URL = "/api/chat"
OPENAI_MODELS_URL = "/v1/models"
OPENAI_CHAT_SUFFIX = "/v1/chat/completions"


async def list_ollama_models(base_url: str) -> tuple[list[str], str | None]:
    """Fetch model names from Ollama API. Returns (model_list, error_message)."""
    if not base_url or not base_url.strip():
        return ([], "Ollama URL is empty.")

    url = base_url.rstrip("/") + OLLAMA_LIST_URL
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                if resp.status != 200:
                    return ([], f"Ollama HTTP {resp.status} at {base_url}")
                data = await resp.json()
                models = data.get("models") or []
                names = [
                    (m.get("name") or m.get("model") or "").strip() for m in models if (m.get("name") or m.get("model"))
                ]
                if not names:
                    return ([], "Ollama has no models pulled.")
                return (names, None)
    except Exception as e:
        logger.warning("Ollama connection failed at %s: %s", base_url, e)
        return ([], f"Connection failed at {base_url}")


async def list_openai_models(base_url: str) -> tuple[list[str], str | None]:
    """Fetch model ids from OpenAI-compatible models endpoint (e.g. LM Studio)."""
    if not base_url or not base_url.strip():
        return ([], "Local LLM URL is empty.")

    url = base_url.rstrip("/")
    if not url.endswith("/models"):
        url = url + ("/models" if url.endswith("/v1") else OPENAI_MODELS_URL)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                if resp.status != 200:
                    return ([], f"Local LLM HTTP {resp.status} at {base_url}")
                data = await resp.json()
                items = data.get("data") or []
                names = [str(m.get("id", "")).strip() for m in items if m.get("id")]
                if not names:
                    return ([], "No models found on local LLM server.")
                return (names, None)
    except Exception as e:
        logger.warning("Local LLM connection failed at %s: %s", base_url, e)
        return ([], f"Connection failed at {base_url}")


async def chat_ollama(base_url: str, model: str, messages: list[dict[str, str]]) -> str:
    """Send chat to Ollama /api/chat. Returns assistant reply text or raises."""
    if not base_url or not model:
        raise ValueError("ollama_url and ollama_model required")

    url = base_url.rstrip("/") + OLLAMA_CHAT_URL
    payload = {"model": model, "messages": messages, "stream": False}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(f"Ollama chat failed {resp.status}: {text[:200]}")
                data = await resp.json()
                msg = data.get("message")
                if isinstance(msg, dict) and "content" in msg:
                    return (msg["content"] or "").strip()
                return (data.get("response") or "").strip()
    except aiohttp.ClientConnectorError as e:
        raise RuntimeError(f"Could not connect to Ollama at {base_url}") from e


async def chat_openai_compatible(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
) -> str:
    """OpenAI-compatible chat completion. model optional for some servers (LM Studio)."""
    if not base_url:
        raise ValueError("local_llm_url required")

    url = base_url.rstrip("/")
    if not url.endswith("chat/completions"):
        url = url + ("/chat/completions" if url.endswith("/v1") else OPENAI_CHAT_SUFFIX)

    headers = {"Content-Type": "application/json"}
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"

    payload: dict[str, Any] = {"messages": messages, "stream": False}
    if model and model.strip():
        payload["model"] = model.strip()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=120)
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(f"Local LLM chat failed {resp.status}: {text[:200]}")
                data = await resp.json()
                choices = data.get("choices") or []
                if not choices:
                    return ""
                content = (choices[0].get("message") or {}).get("content") or ""
                return content.strip()
    except aiohttp.ClientConnectorError as e:
        raise RuntimeError(f"Could not connect to Local LLM at {base_url}") from e


# -- Streaming helpers --

async def stream_ollama(base_url: str, model: str, messages: list[dict[str, str]]) -> AsyncGenerator[str, None]:
    """Stream chat from Ollama. Yields content tokens as they arrive."""
    if not base_url or not model:
        yield "Error: ollama_url and ollama_model required"
        return

    url = base_url.rstrip("/") + OLLAMA_CHAT_URL
    payload = {"model": model, "messages": messages, "stream": True}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=300)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    yield f"Error: Ollama returned {resp.status}"
                    return
                async for line in resp.content:
                    text = line.decode("utf-8", errors="replace").strip()
                    if not text:
                        continue
                    if text == "data: [DONE]":
                        return
                    try:
                        if text.startswith("data: "):
                            text = text[6:]
                        chunk = json.loads(text)
                        content = chunk.get("message", {}).get("content", "") or chunk.get("response", "")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        pass
    except aiohttp.ClientConnectorError as e:
        yield f"Error: Could not connect to Ollama at {base_url}"


async def stream_openai_compatible(
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
) -> AsyncGenerator[str, None]:
    """Stream chat from OpenAI-compatible endpoint. Yields content tokens."""
    if not base_url:
        yield "Error: local_llm_url required"
        return

    url = base_url.rstrip("/")
    if not url.endswith("chat/completions"):
        url = url + ("/chat/completions" if url.endswith("/v1") else OPENAI_CHAT_SUFFIX)

    headers = {"Content-Type": "application/json"}
    if api_key and api_key.strip():
        headers["Authorization"] = f"Bearer {api_key.strip()}"

    payload: dict[str, Any] = {"messages": messages, "stream": True}
    if model and model.strip():
        payload["model"] = model.strip()

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=300)) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    yield f"Error: LLM returned {resp.status}"
                    return
                async for line in resp.content:
                    text = line.decode("utf-8", errors="replace").strip()
                    if not text:
                        continue
                    if text == "data: [DONE]":
                        return
                    try:
                        if text.startswith("data: "):
                            text = text[6:]
                        chunk = json.loads(text)
                        choices = chunk.get("choices") or []
                        if choices:
                            delta = choices[0].get("delta") or {}
                            content = delta.get("content") or ""
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        pass
    except aiohttp.ClientConnectorError as e:
        yield f"Error: Could not connect to LLM at {base_url}"
