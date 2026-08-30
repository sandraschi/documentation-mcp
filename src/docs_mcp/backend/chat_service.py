"""Chat service with memory, streaming, personas, and multi-provider routing."""

import json
import logging
import uuid
from collections import defaultdict
from collections.abc import AsyncGenerator

from docs_mcp.backend import llm_client as lc

logger = logging.getLogger(__name__)

PERSONAS: dict[str, str] = {
    "default": "You are a helpful documentation assistant for the MCP ecosystem. Answer concisely based on the provided documentation context. If you don't know, say so.",
    "technical": "You are a precise technical documentation expert for the MCP fleet. Provide exact specifications, code examples, and file paths. Be accurate above all.",
    "concise": "You are a documentation assistant. Answer in the shortest complete way possible. One paragraph max unless the question requires more depth.",
    "educator": "You are a patient tutor explaining MCP ecosystem documentation. Break down complex topics step by step. Use analogies where helpful.",
}

CLOUD_PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "models": ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022"],
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "models": ["gemini-2.5-pro", "gemini-2.5-flash"],
    },
}

# In-memory conversation store: {conversation_id: [messages]}
_conversations: dict[str, list[dict]] = defaultdict(list)


async def auto_discover() -> dict[str, bool]:
    """Scan standard ports for running LLM engines."""
    result: dict[str, bool] = {"ollama": False, "lmstudio": False}
    try:
        models, _ = await lc.list_ollama_models("http://localhost:11434")
        result["ollama"] = len(models) > 0
    except Exception:
        logger.debug("Ollama not detected on port 11434")
    try:
        models, _ = await lc.list_openai_models("http://localhost:1234/v1")
        result["lmstudio"] = len(models) > 0
    except Exception:
        logger.debug("LM Studio not detected on port 1234")
    return result


def get_provider_info(provider_key: str) -> dict | None:
    for key, info in CLOUD_PROVIDERS.items():
        if key == provider_key:
            return info
    return {"base_url": "", "models": []}


async def stream_chat(
    message: str,
    conversation_id: str | None = None,
    persona: str = "default",
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
    api_url: str | None = None,
    system_prompt_override: str | None = None,
    search_fn=None,
    settings=None,
) -> AsyncGenerator[str, None]:
    if conversation_id is None:
        conversation_id = uuid.uuid4().hex[:12]

    conv = _conversations[conversation_id]

    # 1. Search docs for context
    sources: list[str] = []
    if search_fn:
        try:
            search_result = search_fn(message, limit=5) if callable(search_fn) else {"data": []}
            sources = [r["filename"] for r in (search_result.get("data") or [])]
        except Exception as e:
            logger.warning("Search failed: %s", e)

    # 2. Append user message
    conv.append({"role": "user", "content": message})

    # 3. Build system prompt
    system = system_prompt_override or PERSONAS.get(persona, PERSONAS["default"])
    doc_context = "\n\n".join(
        [f"SOURCE: {r['filename']}\n{r['content']}" for r in (search_result.get("data") or [])]
        if search_fn and callable(search_fn)
        else []
    )
    if doc_context:
        system += f"\n\nUse the following documentation context to answer:\n{doc_context}"

    # 4. Build messages array (last 20 for context window)
    messages = [{"role": "system", "content": system}]
    for m in conv[-20:]:
        messages.append(m)

    # 5. Route to provider
    provider_key = provider or (settings.get("provider", "") if settings else "")
    api_url_resolved = api_url
    api_key_resolved = api_key
    model_resolved = model

    if not provider_key and settings:
        provider_key = settings.get("provider", "")

    # 6. Stream
    full_response = ""
    try:
        if provider_key == "ollama":
            url = api_url_resolved or (
                settings.get("ollama_url", "http://localhost:11434") if settings else "http://localhost:11434"
            )
            m = model_resolved or (settings.get("ollama_model", "") if settings else "")
            async for chunk in lc.stream_ollama(url, m, messages):
                full_response += chunk
                yield json.dumps({"type": "token", "content": chunk}) + "\n"

        elif provider_key in CLOUD_PROVIDERS:
            info = CLOUD_PROVIDERS[provider_key]
            url = api_url_resolved or info["base_url"]
            m = model_resolved or info["models"][0]
            key = api_key_resolved or ""
            async for chunk in lc.stream_openai_compatible(url, key, m, messages):
                full_response += chunk
                yield json.dumps({"type": "token", "content": chunk}) + "\n"

        elif provider_key == "local" or provider_key == "lmstudio":
            url = api_url_resolved or (
                settings.get("lmstudio_url", "http://localhost:1234/v1") if settings else "http://localhost:1234/v1"
            )
            if not url or url == "http://localhost:1234/v1":
                url = api_url_resolved or (settings.get("local_llm_url", "") if settings else "")
            key = api_key_resolved or (settings.get("local_llm_key", "") if settings else "")
            m = model_resolved or (settings.get("lmstudio_model", "") if settings else "")
            async for chunk in lc.stream_openai_compatible(url, key, m, messages):
                full_response += chunk
                yield json.dumps({"type": "token", "content": chunk}) + "\n"

        else:
            # No provider configured - return RAG-only response
            fallback = f"Found {len(sources)} relevant documentation sources. Enable an LLM provider in Settings for AI-synthesized answers."
            yield json.dumps({"type": "token", "content": fallback}) + "\n"

    except Exception as e:
        logger.error("Chat stream error: %s", e)
        yield json.dumps({"type": "token", "content": f"Error: {e}"}) + "\n"

    # 7. Save assistant response with sources
    conv.append({"role": "assistant", "content": full_response})

    # 8. Yield sources + done
    yield json.dumps({"type": "sources", "content": sources}) + "\n"
    yield json.dumps({"type": "done", "conversation_id": conversation_id}) + "\n"
