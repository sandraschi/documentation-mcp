# Speech Integration — Fleet Template

Add TTS (read-aloud) and STT (voice input) to any fleet webapp chat page.

## Files

| File | Copy to | Purpose |
|------|---------|---------|
| `speech-service.ts` | `web_sota/src/common/speech-service.ts` | Core abstraction (auto-detects speech-mcp vs Web Speech API) |
| `SpeakButton.tsx` | `web_sota/src/components/SpeakButton.tsx` | "Read aloud" button per assistant message |
| `MicButton.tsx` | `web_sota/src/components/MicButton.tsx` | Voice input mic button next to chat input |

## Integration Steps

### 1. Copy files

```bash
cp templates/speech/speech-service.ts  repo/web_sota/src/common/speech-service.ts
cp templates/speech/SpeakButton.tsx    repo/web_sota/src/components/SpeakButton.tsx
cp templates/speech/MicButton.tsx      repo/web_sota/src/components/MicButton.tsx
```

### 2. Init at app root

In your `ChatPage.tsx` (or `Layout.tsx`), call `initSpeechService()` once on mount:

```typescript
import { initSpeechService } from "@/common/speech-service";

useEffect(() => { initSpeechService(); }, []);
```

### 3. Add SpeakButton to assistant messages

```tsx
import { SpeakButton } from "@/components/SpeakButton";

// Inside your message render loop, next to existing CopyButton:
<CopyButton text={msg.content} />
{msg.role === "assistant" && <SpeakButton text={msg.content} />}
```

### 4. Add MicButton to the input area

```tsx
import { MicButton } from "@/components/MicButton";

// Before the chat input, or next to it:
<MicButton input={input} setInput={setInput} />
```

## How It Works

```
initSpeechService() probes localhost:10909/api/v1/health
  ├── speech-mcp responds → Tier 2: WAV fetch + Audio playback
  └── speech-mcp missing  → Tier 1: window.speechSynthesis (Web Speech API)

SpeakButton reads text aloud. MicButton captures voice → inserts into input field.
Both auto-hide when their respective backend is unavailable.

Tier 1 (Web Speech API) requires Chrome or Edge.
Tier 2 (speech-mcp) works in any browser but requires speech-mcp running.
```

## speech-mcp Requirements (Tier 2)

- `speech-mcp` must be running (port 10909, backend)
- Default provider `windows` uses SAPI5 — zero config, free
- For better voices: set `GOOGLE_API_KEY`, `ELEVENLABS_API_KEY`, or `HUME_API_KEY` in speech-mcp's `.env`
- Speech is auto-detected — no config needed in the consumer webapp
