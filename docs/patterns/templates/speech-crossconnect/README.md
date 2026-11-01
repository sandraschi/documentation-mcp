# speech-crossconnect template

Drop-in speech-mcp integration: TTS with a real provider/voice picker,
extracted from **japanophile-mcp** (reference implementation, wired
2026-09-15) so the next repo doesn't have to rediscover the same three bugs.
Also includes `MicButton.tsx` for voice input (STT), adapted from the fleet's
earlier `templates/speech/MicButton.tsx` — not from japanophile-mcp, which
never had voice input. See its own section below; it's deliberately NOT a
crossconnect (no speech-mcp call at all, see the file's header for why).

This is the **reference adapter** for the fleet-wide
[CROSSCONNECT_PATTERN.md](../../CROSSCONNECT_PATTERN.md) — read that first if
you're integrating a *different* sibling MCP server (calibre-mcp, plex-mcp,
discord-mcp, ...); it's the general contract this template implements, kept
separately so it doesn't have to be rediscovered per peer the way the speech
integration itself was rediscovered three times before anyone noticed the
overlap (see that doc's "Why this exists").

Full speech-mcp-specific context and the fleet-wide "when to use speech-mcp"
table: [../speech-mcp-ui-hooks.md](../speech-mcp-ui-hooks.md).

## Files

| File | Copy to | Purpose |
|---|---|---|
| `../crossconnect-base/crossconnect_base.py` | `src/<pkg>/services/crossconnect_base.py` | **Vendor this first.** Peer-agnostic `CrossconnectPeer` base — shared by every adapter you add, not speech-specific |
| `../crossconnect-base/crossconnect.ts` | `webapp/src/lib/crossconnect.ts` | **Vendor this first.** Peer-agnostic frontend counterpart |
| `speech_crossconnect.py` | `src/<pkg>/services/speech_crossconnect.py` | Speech-specific adapter: `voices()`, `speak()`, `speak_wav_bytes()`, `tts_wav_url()` |
| `speech_routes.py` | `src/<pkg>/services/speech_routes.py` | FastAPI routes: `/api/speech/voices`, `/speak.wav`, `/speak` |
| `speech.ts` | `webapp/src/lib/speech.ts` | Frontend fetch client (`speechApi(apiBase)`) |
| `SpeechControls.tsx` | `webapp/src/components/SpeechControls.tsx` | Listen button + provider/voice dropdowns, ready to drop into any page |
| `MicButton.tsx` | `webapp/src/components/MicButton.tsx` | Voice input (STT) — browser Web Speech API only, no backend/crossconnect involved |
| `WakeWordToggle.tsx` | `webapp/src/components/WakeWordToggle.tsx` | Start/stop/status of speech-mcp's machine-wide wake-word listener — **not** per-tab STT, see its warning copy |

## Quick integration

**Backend** (in your FastAPI app factory):

```python
from .services.speech_routes import register_speech_routes
register_speech_routes(app)
```

**Frontend** (anywhere you have text to read aloud):

```tsx
import { SpeechControls } from "@/components/SpeechControls";

<SpeechControls apiBase={API_BASE} getText={() => articleText} />
```

`getText` can be sync or async — call your own API inside it if the text
isn't already loaded (see japanophile-mcp's `Know.tsx` for a real example:
it calls `api.knowledgeGet(page)` inside `getText`, not before).

**Voice input** (anywhere you have a text input the user might want to speak into):

```tsx
import { MicButton } from "@/components/MicButton";

<input value={input} onChange={(e) => setInput(e.target.value)} />
<MicButton onResult={(transcript) => setInput(transcript)} />
```

`MicButton` renders nothing in browsers without `SpeechRecognition` (Safari,
Firefox) — check `isSttAvailable()` yourself first if you want different
fallback UI (e.g. a disabled button with a tooltip) instead of nothing. It
never calls speech-mcp or your backend at all; see the file's own header
comment for why (speech-mcp's STT is a batch/websocket flow, not a drop-in
mic button — different shape of problem) and the Chrome-sends-audio-to-Google
privacy tradeoff worth knowing before you ship it.

**Wake word** (speech-mcp's other STT mode — genuinely different from both
of the above, read before wiring it up):

```tsx
import { WakeWordToggle } from "@/components/WakeWordToggle";

<WakeWordToggle apiBase={API_BASE} defaultKeyword="hey_jarvis" />
```

`WakeWordToggle` is **not** per-browser-tab voice input. `action="start"`
spins up a background thread on whatever **machine** runs speech-mcp,
listening on that machine's own microphone via openWakeWord, until stopped —
closer to "turn on Hey Siri on that computer" than a webapp control. There's
no built-in way for a specific browser tab to be notified when the keyword
fires; on detection speech-mcp either routes to its Fleet Voice Command Bus
(if it has `FLEET_VOICE_DELEGATE=1` set) or just logs server-side. Don't
present this next to `MicButton` as if they're two flavors of the same
toggle — they aren't, and the component's own warning copy says so; keep
that copy when you adapt it.

## Bugs already found so you don't have to (as of 2026-09-15)

These are real, verified against a live speech-mcp instance — check its
CHANGELOG before assuming they're still true, and delete the workaround if
they've been fixed upstream:

1. **POST `/api/v1/tts` + `provider=gemini` + default voice_id 500s.** The
   endpoint passes the literal string `"default"` through as a Gemini voice
   name. Its sibling `GET /api/v1/tts/wav` already normalizes `"default"` to
   `"Kore"` — the POST path just doesn't. `speak()` in this template works
   around it by substituting `"Kore"` before sending.
2. **Gemini is 10-20x slower than Windows SAPI.** ~14-22s measured for a
   200-400 character excerpt, against near-instant SAPI. A typical 10-15s
   HTTP client timeout will misreport a slow-but-successful Gemini call as
   "not reachable". Both `speech_crossconnect.py` and `speech_routes.py` use
   a 45s timeout for exactly this reason — don't shrink it without checking
   real latency first.
3. **Never hardcode a voice list.** Providers and cloned voices (especially
   ElevenLabs) change independently of any consuming repo. `voices()` always
   calls speech-mcp live; the dropdown in `SpeechControls.tsx` renders
   whatever comes back, nothing baked in.

## Design decisions worth keeping when you adapt this

- **Proxy through your own backend, never call speech-mcp from the browser
  directly.** One CORS story, one place for graceful degradation, and the
  browser never needs to know speech-mcp's port.
- **Default provider is Gemini, not Windows SAPI** (`DEFAULT_PROVIDER` in
  `speech_crossconnect.py`) — voice quality is noticeably better, at the
  cost of the latency in bug #2 above. Change the default per-repo if
  latency matters more than quality for your use case; the provider is
  still user-switchable either way via the dropdown.
- **Trim the text before sending.** `SpeechControls`'s `maxChars` (default
  200) exists because Gemini's latency scales with text length — an
  unbounded "read the whole article" button will feel broken, not just
  slow. Bump it if your repo's use case tolerates a longer wait.
- **`success`/`message`/`data` dialogic shape everywhere**, matching the
  fleet's [DIALOGIC_RETURNS.md](../../../standards/DIALOGIC_RETURNS.md) standard — an
  unreachable peer is `success: false` with an actionable `message`, never
  a raw exception surfaced to the UI.

## Reference implementation

`japanophile-mcp`: `src/japanophile_mcp/services/crossconnects.py` (the
`speak`/`voices`/`tts_wav_url` functions this template was extracted from —
that file also has `library_search`/`media_search` for calibre-mcp/plex-mcp,
which aren't part of this speech-only template), `src/japanophile_mcp/http.py`
(`/api/crossconnect/*` routes), `webapp/src/pages/Know.tsx` (live usage with
persisted provider/voice selection).
