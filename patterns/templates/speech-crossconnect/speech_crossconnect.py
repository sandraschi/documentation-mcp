"""Fleet crossconnect adapter: speech-mcp TTS, vendored from japanophile-mcp
(reference implementation, 2026-09-15 — see docs/TOOLS.md and
src/japanophile_mcp/services/crossconnects.py in that repo for the live
version this was extracted from).

Built on crossconnect_base.py's CrossconnectPeer — read
../../CROSSCONNECT_PATTERN.md (the general contract) before adding a second
peer integration to your repo. This file is short specifically because the
shared concerns (dialogic shape, timeout handling, graceful degradation) live
in the base, not here.

HOW TO VENDOR
--------------
1. Vendor crossconnect_base.py first (../crossconnect-base/crossconnect_base.py)
   into the SAME services/ directory as this file — it's peer-agnostic,
   shared by every adapter you add, not speech-specific.
2. Copy this file into <your_repo>/src/<your_pkg>/services/speech_crossconnect.py.
3. Adjust DEFAULT_PROVIDER below if you don't want Gemini as the default.
4. Register the FastAPI routes — see speech_routes.py in this same template dir.
5. Add the frontend pieces — see speech.ts + SpeechControls.tsx in this dir.

BUGS ALREADY FOUND (found the hard way, keep the workarounds)
-----------------------------------------------------------------------
- Gemini synthesis is much slower than Windows SAPI: ~14-22s for a 200-400
  character excerpt (measured live against a real speech-mcp instance,
  2026-09-15). speak() and tts_wav_url()'s consumers use a 45s timeout for
  exactly this reason — a typical 10-15s API timeout will misreport a
  slow-but-successful Gemini call as "speech-mcp not reachable."
- speech-mcp's POST /api/v1/tts does NOT normalize voice_id="default" for
  the gemini provider — it passes "default" straight through as a literal
  Gemini voice name, which 500s. Its sibling GET /api/v1/tts/wav already
  normalizes "default" -> "Kore" correctly; the POST path just doesn't.
  speak() below works around this by substituting "Kore" before sending.
  Check speech-mcp's CHANGELOG before removing this workaround — it may
  already be fixed upstream by the time you read this.
- Never hardcode a voice list. Providers and cloned voices (ElevenLabs
  clones especially) change independently of your repo — always call
  voices() live for any UI dropdown.
"""

from __future__ import annotations

import os
from urllib.parse import urlencode

import httpx

from .crossconnect_base import CrossconnectPeer

# Gemini sounds notably better than Windows SAPI but is ~10-20x slower per call.
# Change to "windows" here (or let callers override per-call) if latency matters
# more than voice quality for your use case.
DEFAULT_PROVIDER = "gemini"

_peer = CrossconnectPeer(
    name="speech-mcp",
    base_url=os.getenv("SPEECH_MCP_URL", "http://127.0.0.1:10909"),
)


def voices() -> dict:
    """GET speech-mcp /api/v1/voices — real, live provider/voice list for a UI
    dropdown. Shape: {"providers": [{"name", "status", "voices": [...]}, ...]}.
    """
    result = _peer.get_json("/api/v1/voices", timeout=10.0)
    if result["success"]:
        result["message"] = "Voices from speech-mcp."
    return result


def speak(text: str, provider: str = DEFAULT_PROVIDER, voice_id: str = "default") -> dict:
    """POST speech-mcp /api/v1/tts — plays on speech-mcp's OWN speaker (agent-side
    voice output, e.g. for an MCP tool). For audio your own caller can play back
    (a webapp), use speak_wav_bytes() or tts_wav_url() instead.
    """
    if not text.strip():
        return {"success": False, "message": "speak needs non-empty text.", "data": None}
    if provider == "gemini" and voice_id in ("", "default"):
        voice_id = "Kore"  # see module docstring: POST /api/v1/tts bug workaround
    result = _peer.post_json(
        "/api/v1/tts",
        {"text": text, "provider": provider, "voice_id": voice_id},
        timeout=45.0,  # Gemini is slow — see module docstring
    )
    if result["success"]:
        result["message"] = f"Spoken via speech-mcp ({provider})."
    return result


def speak_wav_bytes(
    text: str, provider: str = DEFAULT_PROVIDER, voice_id: str = "default"
) -> httpx.Response:
    """GET speech-mcp /api/v1/tts/wav and return the raw response — for your own
    FastAPI route to wrap in a Response(media_type="audio/wav"). Raises
    httpx.HTTPError on failure; catch it at your route boundary (see
    speech_routes.py's api_speech_speak_wav for the pattern).
    """
    return _peer.raw_get(
        "/api/v1/tts/wav",
        {"text": text, "provider": provider, "voice_id": voice_id},
        timeout=45.0,  # Gemini is slow — see module docstring
    )


def tts_wav_url(text: str, provider: str = DEFAULT_PROVIDER, voice_id: str = "default") -> str:
    """Direct speech-mcp WAV URL, as a plain string (no request made). Rarely
    needed directly — speak_wav_bytes() is what your FastAPI route should call.
    Do not point a browser <audio> tag at this URL unless speech-mcp's own CORS
    is configured for your webapp's origin; proxy through your backend instead.
    """
    qs = urlencode({"text": text, "provider": provider, "voice_id": voice_id})
    return f"{_peer.base_url}/api/v1/tts/wav?{qs}"


def wake_word(
    action: str,
    keyword: str = "hey_jarvis",
    sleep_keyword: str | None = None,
    sensitivity: float = 0.5,
) -> dict:
    """POST speech-mcp /api/v1/wake_word — start/stop/check a background
    wake-word listener (openWakeWord).

    IMPORTANT — this is NOT per-browser-tab STT like MicButton. It starts a
    listener thread on whatever MACHINE runs speech-mcp, using THAT machine's
    own microphone, running until stopped. It has no per-request lifetime and
    no built-in way to notify a specific browser tab when the keyword fires —
    on detection it either routes to the Fleet Voice Command Bus (if
    speech-mcp has FLEET_VOICE_DELEGATE=1) or just logs locally. Treat
    action="start" as flipping on a real always-listening microphone on that
    machine, not as starting a request-scoped voice session — surface that
    clearly in your UI (see WakeWordToggle.tsx's warning copy) rather than
    presenting it as a lightweight toggle.

    action: "start" | "stop" | "status".
    """
    if action not in ("start", "stop", "status"):
        return {
            "success": False,
            "message": f"Unknown wake_word action '{action}'. Valid: start, stop, status.",
            "data": None,
        }
    body: dict[str, object] = {"action": action, "keyword": keyword, "sensitivity": sensitivity}
    if sleep_keyword:
        body["sleep_keyword"] = sleep_keyword
    result = _peer.post_json("/api/v1/wake_word", body, timeout=15.0)
    # post_json only sees transport-level success (2xx) — speech-mcp itself
    # returns 200 with {"success": false, "error": ...} for a logical failure
    # (e.g. an action it doesn't recognize), so promote that too.
    peer_body = result.get("data")
    if result["success"] and isinstance(peer_body, dict) and not peer_body.get("success", True):
        return {
            "success": False,
            "message": peer_body.get("error", "wake_word action failed."),
            "data": peer_body,
        }
    return result
