import logging

from fastapi import APIRouter, HTTPException, Request

from docs_mcp.backend import llm_client, settings_store

logger = logging.getLogger("docs_mcp.api.settings")
router = APIRouter(prefix="/api")

@router.get("/settings")
async def api_settings_get():
    """Return current webapp settings. API key is masked."""
    try:
        s = settings_store.load_settings()
        key = s.get("local_llm_key") or ""
        if len(key) > 4:
            s = {**s, "local_llm_key": "****" + key[-4:]}
        else:
            s = {**s, "local_llm_key": "****" if key else ""}
        return s
    except Exception as e:
        logger.error(f"Error in api_settings_get: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/settings")
async def api_settings_put(request: Request):
    """Save webapp settings."""
    try:
        body = await request.json()
        current = settings_store.load_settings()

        # Masking logic
        if "local_llm_key" in body and (body["local_llm_key"] or "").strip() == "":
            body["local_llm_key"] = current.get("local_llm_key") or ""
        if (body.get("local_llm_key") or "").startswith("****"):
            body["local_llm_key"] = current.get("local_llm_key") or ""

        updates = {
            "ollama_url": (body.get("ollama_url") or "").strip(),
            "ollama_model": (body.get("ollama_model") or "").strip(),
            "local_llm_url": (body.get("local_llm_url") or "").strip(),
            "local_llm_key": (body.get("local_llm_key") or "").strip(),
            "lmstudio_url": (body.get("lmstudio_url") or "").strip(),
            "lmstudio_model": (body.get("lmstudio_model") or "").strip(),
            "provider": (body.get("provider") or "").strip().lower(),
        }

        if updates["provider"] not in ("ollama", "local", "lmstudio", ""):
            updates["provider"] = ""

        settings_store.save_settings({**current, **updates})
        return {"success": True}
    except Exception as e:
        logger.error(f"Error in api_settings_put: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/ollama")
async def api_ollama_models(url: str = ""):
    """List available Ollama models."""
    try:
        if not url:
            s = settings_store.load_settings()
            url = (s.get("ollama_url") or "").strip()
        if not url:
            return {"models": [], "message": "Ollama URL missing"}

        models, error = await llm_client.list_ollama_models(url)
        return {"models": models, "message": error}
    except Exception as e:
        logger.error(f"Error in api_ollama_models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/lmstudio")
async def api_lmstudio_models(url: str = ""):
    """List available LM Studio models."""
    try:
        if not url:
            s = settings_store.load_settings()
            url = (s.get("lmstudio_url") or "").strip()
        if not url:
            return {"models": [], "message": "LM Studio URL missing"}

        models = await llm_client.list_openai_models(url)
        return {"models": models}
    except Exception as e:
        logger.error(f"Error in api_lmstudio_models: {e}")
        raise HTTPException(status_code=500, detail=str(e))
