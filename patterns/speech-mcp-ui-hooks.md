# Speech-MCP UI hooks (fleet pattern)

**Goal:** One voice gateway (`speech-mcp`, ports **10908/10909**) for read-aloud and dictation across fleet webapps, without each repo spawning its own STT/TTS stack.

## When to use speech-mcp

| Need | Use |
|------|-----|
| Read assistant reply or email body aloud | `GET /api/v1/tts/wav?text=...&provider=windows` (browser `<audio>`) |
| Speak on server speakers | `POST /api/v1/tts` |
| Mic → text in a form field | `POST /api/v1/transcribe` or `/ws/stt` |
| Hands-free cross-app commands | [VOICE_COMMAND_BUS.md](../standards/VOICE_COMMAND_BUS.md) → fleet-agent **10996** |

**Do not** embed pyttsx3, faster-whisper, or ElevenLabs SDKs in every repo unless speech-mcp is down and you need a offline fallback.

## Integration surfaces (good candidates)

| Repo | Read aloud | Voice input |
|------|------------|-------------|
| **email-mcp** | Chat replies, email detail body, compose proofread | Dictation into compose; "read unread" |
| **libreoffice-mcp** | Chat responses, job summaries | Chat command dictation |
| **ednaficator** | News digest (Phase 3), email summaries (Phase 2) | Telegram voice notes (local whisper OK on hot path) |
| **aiwatcher-mcp** | Digest cards | Low priority |

**Exclude** from family concierge TTS routing: dev-only repos (KiCad, winops, git).

## Recommended integration (2026-09-15 — supersedes the direct-fetch snippet below)

**Use the vendorable template:** [templates/speech-crossconnect/](templates/speech-crossconnect/)
— a backend proxy (Python) + frontend client + drop-in `<SpeechControls>`
React component (provider + voice dropdowns, not just a fixed "windows"
call), extracted from **japanophile-mcp**'s live 2026-09-15 integration.
Its README documents three real bugs already found (Gemini voice_id="default"
500s on the POST endpoint, Gemini's 10-20x latency vs SAPI needing a 45s not
15s timeout, and why you must never hardcode a voice list) so the next repo
doesn't rediscover them from scratch.

Key difference from the old snippet below: **proxy through your own backend**
(`register_speech_routes(app)`), don't `fetch()` speech-mcp directly from the
browser — one CORS story, one place for graceful degradation, and a slow
Gemini call doesn't misreport as "unreachable" the way a browser-side 15s
default fetch timeout would.

### Old snippet (kept for history — has the timeout and hardcoded-provider issues above)

```typescript
const SPEECH = import.meta.env.VITE_SPEECH_MCP_URL ?? 'http://127.0.0.1:10909'

export async function speakText(text: string) {
  const q = new URLSearchParams({ text, provider: 'windows' })
  const res = await fetch(`${SPEECH}/api/v1/tts/wav?${q}`)
  if (!res.ok) throw new Error('TTS failed')
  const blob = await res.blob()
  await new Audio(URL.createObjectURL(blob)).play()
}
```

**Implemented (2026-07-28):** `lib/speech.ts` + 🔊 on assistant bubbles in **email-mcp** `/chat` and **libreoffice-mcp** `/chat` (predates the template above — consider migrating when touched next, not urgently).
**Implemented via template (2026-09-15):** japanophile-mcp `Know.tsx` — Listen button with live provider/voice dropdowns.

## Backend / concierge adapters

For family paths (Edna), use a **thin HTTP wrapper** like `ednaficator/concierge/email_tools.py`, not MCP stdio — or better, vendor
[templates/speech-crossconnect/speech_crossconnect.py](templates/speech-crossconnect/speech_crossconnect.py)
directly, which already has the 45s timeout and gemini voice_id workaround baked in:

```python
httpx.get(f"{SPEECH_URL}/api/v1/tts/wav", params={"text": summary, "provider": "windows"}, timeout=45.0)
```

## Auth and ops

- Optional `SPEECH_MCP_AUTH_TOKEN` + `X-Speech-MCP-Auth` on WebSocket streams
- REST TTS often works without token on localhost
- Only one wake-word listener should hold the default mic (see speech-mcp wake docs)

## Migration note

email-mcp Mail Watcher currently webhooks **robofang-mcp** for TTS alerts. Consolidate on speech-mcp when you want one voice and one provider config fleet-wide.

## Related

- [templates/speech-crossconnect/](templates/speech-crossconnect/) — the vendorable code for everything above
- [VOICE_COMMAND_BUS.md](../standards/VOICE_COMMAND_BUS.md)
- `speech-mcp/docs/tools-reference.md`
- `ednaficator/docs/CONCIERGE_PLAN.md` (Phase 3 news + TTS)
