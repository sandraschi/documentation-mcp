"""FastAPI route registration for speech_crossconnect.py.

HOW TO VENDOR: copy into <your_repo>/src/<your_pkg>/services/speech_routes.py
(same directory as speech_crossconnect.py), then in your app factory:

    from .services.speech_routes import register_speech_routes
    register_speech_routes(app)

Routes registered (adjust the "/api/speech" prefix if it collides with an
existing route in your repo):

    GET  /api/speech/voices              -> live provider/voice list
    GET  /api/speech/speak.wav?text=...  -> real audio bytes, for an <audio> tag
    POST /api/speech/speak               -> {text, provider, voice_id} JSON body,
                                             plays on speech-mcp's OWN speaker
    POST /api/speech/wake_word           -> {action, keyword, sleep_keyword,
                                             sensitivity} JSON body. action is
                                             start/stop/status of a MACHINE-WIDE
                                             background listener on whatever
                                             machine runs speech-mcp — not a
                                             per-browser-tab feature. See
                                             speech_crossconnect.py's wake_word()
                                             docstring before wiring a UI to it.
"""

from __future__ import annotations

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response

from .speech_crossconnect import speak, speak_wav_bytes, voices, wake_word


def register_speech_routes(app: FastAPI) -> None:
    @app.get("/api/speech/voices")
    def api_speech_voices() -> JSONResponse:
        return JSONResponse(voices())

    @app.post("/api/speech/wake_word")
    def api_speech_wake_word(payload: dict) -> JSONResponse:
        return JSONResponse(
            wake_word(
                str(payload.get("action", "status")),
                keyword=str(payload.get("keyword", "hey_jarvis")),
                sleep_keyword=payload.get("sleep_keyword"),
                sensitivity=float(payload.get("sensitivity", 0.5)),
            )
        )

    @app.get("/api/speech/speak.wav")
    def api_speech_speak_wav(text: str, provider: str = "gemini", voice_id: str = "default"):
        try:
            resp = speak_wav_bytes(text, provider=provider, voice_id=voice_id)
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=502, detail=f"speech-mcp unreachable: {exc}"
            ) from exc
        return Response(content=resp.content, media_type="audio/wav")

    @app.post("/api/speech/speak")
    def api_speech_speak(payload: dict) -> JSONResponse:
        return JSONResponse(
            speak(
                str(payload.get("text", "")),
                provider=str(payload.get("provider", "gemini")),
                voice_id=str(payload.get("voice_id", "default")),
            )
        )
