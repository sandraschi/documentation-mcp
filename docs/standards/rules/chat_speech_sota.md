# Fleet Chat Speech Standard (SOTA 2026)

**Established**: 2026-07-05  
**Updated**: 2026-07-06  
**Reference impl**: `local-llm-mcp` — `web_sota/src/common/speech.ts`, `web_sota/src/pages/chat.tsx`  
**Template files**: `mcp-central-docs/templates/speech/` — `speech-service.ts`, `SpeakButton.tsx`, `MicButton.tsx`, `INTEGRATION.md`

---

## Problem

Developers using fleet chat pages for coding questions or long prompts benefit from voice input (STT) and having responses read aloud (TTS). The browser Web Speech API provides both, but the integration pattern is not standardised across the fleet — only `local-llm-mcp` has it.

## Standard

### TTS (Text-to-Speech) — SpeakButton

Every chat page that renders assistant messages SHOULD include a "Speak" button on each assistant message. It reads the message aloud using `window.speechSynthesis`.

**Pattern** (extracted from `local-llm-mcp`):

```tsx
// components/SpeakButton.tsx — add to any fleet chat page
import { useState } from "react";
import { Volume2 } from "lucide-react";
import { isTTSSupported, speak } from "@/common/speech";

export function SpeakButton({ text }: { text: string }) {
  const [speaking, setSpeaking] = useState(false);
  if (!isTTSSupported()) return null;
  return (
    <button
      onClick={() => {
        if (speaking) { window.speechSynthesis.cancel(); setSpeaking(false); return; }
        setSpeaking(true);
        speak(text, () => setSpeaking(false));
      }}
      className="p-1.5 rounded transition-colors text-slate-400 hover:text-white"
      title={speaking ? "Stop" : "Speak"}
    >
      <Volume2 className="h-3.5 w-3.5" />
    </button>
  );
}
```

### STT (Speech-to-Text) — MicButton

Every chat page SHOULD include a microphone button next to the input field. It captures speech via the Web Speech API and inserts the transcript into the input.

**Pattern** (extracted from `local-llm-mcp`):

```tsx
// Inside ChatPage component
const [listening, setListening] = useState(false);
const [interimTranscript, setInterimTranscript] = useState("");
const recognitionRef = useRef<ReturnType<typeof createSpeechRecognition> | null>(null);

useEffect(() => {
  if (!isSTTSupported()) return;
  recognitionRef.current = createSpeechRecognition(
    (transcript, isFinal) => {
      if (isFinal) {
        setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
        setInterimTranscript("");
      } else {
        setInterimTranscript(transcript);
      }
    },
    () => setListening(false),
  );
  return () => { recognitionRef.current?.stop(); };
}, []);

function toggleMic() {
  if (!recognitionRef.current) return;
  if (listening) { recognitionRef.current.stop(); }
  else { recognitionRef.current.start(); setListening(true); }
}

// In JSX, next to the input:
{isSTTSupported() && (
  <button onClick={toggleMic} title={listening ? "Stop" : "Voice input"}>
    {listening ? <MicOff /> : <Mic />}
  </button>
)}
```

### Shared `speech.ts` module

Place this in `web_sota/src/common/speech.ts` (or `webapp/src/common/`):

```typescript
/** Strip markdown to plain text for TTS. */
export function stripMarkdown(md: string): string {
  return md
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[*_`#~]/g, "")
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/\n+/g, " ")
    .trim();
}

export function speak(text: string, onEnd?: () => void): () => void {
  if (typeof window === "undefined" || !window.speechSynthesis) return () => {};
  const plain = stripMarkdown(text);
  if (!plain) return () => {};
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(plain);
  u.rate = 1; u.pitch = 1;
  if (onEnd) u.onend = onEnd;
  window.speechSynthesis.speak(u);
  return () => window.speechSynthesis.cancel();
}

export function isTTSSupported(): boolean {
  return typeof window !== "undefined" && !!window.speechSynthesis;
}

interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}
interface SpeechRecognition extends EventTarget {
  continuous: boolean; interimResults: boolean; lang: string;
  onresult: (event: SpeechRecognitionEvent) => void;
  onend: () => void; onerror: (event: Event) => void;
  start: () => void; stop: () => void; abort: () => void;
}
interface SpeechRecognitionConstructor { new (): SpeechRecognition }
declare global {
  interface Window {
    SpeechRecognition?: SpeechRecognitionConstructor;
    webkitSpeechRecognition?: SpeechRecognitionConstructor;
  }
}

const SpeechRecognitionAPI =
  typeof window !== "undefined" &&
  (window.SpeechRecognition || window.webkitSpeechRecognition);

export function isSTTSupported(): boolean {
  return !!SpeechRecognitionAPI;
}

export function createSpeechRecognition(
  onResult: (transcript: string, isFinal: boolean) => void,
  onEnd: () => void,
): { start: () => void; stop: () => void } {
  if (!SpeechRecognitionAPI) return { start: () => {}, stop: () => {} };
  const recognition = new SpeechRecognitionAPI() as SpeechRecognition;
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = navigator.language || "en-US";
  recognition.onresult = (e: SpeechRecognitionEvent) => {
    let transcript = "";
    for (let i = e.resultIndex; i < e.results.length; i++) {
      transcript += e.results[i][0].transcript;
    }
    onResult(transcript, e.results[e.results.length - 1].isFinal);
  };
  recognition.onend = onEnd;
  recognition.onerror = () => onEnd();
  return {
    start: () => { try { recognition.start(); } catch { onEnd(); } },
    stop: () => { try { recognition.abort(); } catch {} onEnd(); },
  };
}
```

## Template files

Ready-to-copy code lives at `mcp-central-docs/templates/speech/`:

| File | Purpose |
|------|---------|
| `speech-service.ts` | Core abstraction — auto-detects speech-mcp (Tier 2) vs Web Speech API (Tier 1) vs none |
| `SpeakButton.tsx` | Extracted read-aloud component per assistant message |
| `MicButton.tsx` | Extracted voice input button with interim transcript preview |
| `INTEGRATION.md` | Step-by-step per-repo guide |

## Integration tiers

| Tier | Source | Cost | Browser | Integration effort |
|------|--------|------|---------|-------------------|
| **1 — Web Speech** | Browser API | Free | Chrome/Edge only | 3 files, ~20 lines per chat page |
| **2 — speech-mcp** | Fleet voice gateway (port 10909) | Free (SAPI5) to cloud-keyed | Any browser | Auto-detected — zero config in consumer |
| **3 — Wispr Flow** | OS-level overlay | ~$20/mo | All apps | Zero — works automatically on `<input>` |

## Rollout

| Phase | Scope | Repos | Method |
|-------|-------|-------|--------|
| 1 — Canary | `local-llm-mcp` | Already shipped | Reference impl |
| 2 — Template published | `mcp-central-docs/templates/speech/` | ✅ **Done** | 3 files + INTEGRATION.md |
| 3 — Pilot 1 | `local-llm-mcp` (refactor to template), `arxiv-mcp` (fresh) | 2 repos | Replace inline code with template imports |
| 4 — SOTA chat roll | All repos with SOTA chat (35 repos) | Mechanical: copy 3 files, 2 imports, 2 JSX insertions |
| 5 — Basic chat roll | All remaining chat pages (22 repos) | Bundled with SOTA chat upgrade |

## Repo-Aware Voice

## Repo-Aware Voice (SOTA pattern)

Wispr Flow and basic Web Speech STT both transcribe voice to raw text with **zero repo context** — they dump words into an `<input>` and the server treats them like typed text. The fleet chat can do better because the webapp has access to the skill preprompt, personality, and tool surface.

**Pattern:** When the mic button is used, append the transcribed text to the current skill preprompt + personality instructions before sending. This makes voice input aware of what tools the server exposes and how it should behave.

```tsx
// Inside ChatPage — repo-aware voice send
// On mic transcript finalisation:
const repoAwarePrompt = `${buildSystemPrompt(personalityId, customPrompt)}\n\n${transcribedText}`;

// Then use repoAwarePrompt as the user message instead of raw text.
// The LLM receives both the skill context and the voice input,
// so it understands which repo/tools the user is talking about.
```

**Implementation in the fleet chat flow:**

```
Voice input  ──→  Web Speech STT  ──→  raw text
                                          │
                    skill preprompt ──────┤  (buildSystemPrompt result)
                    personality role  ────┤
                                          ▼
                              enriched prompt sent to /api/llm/chat
```

The `sendMessage()` function already calls `buildSystemPrompt()` to construct the system message. The repo-aware upgrade is to also inject that context as a prefix to the user's transcribed message:

```tsx
async function handleVoiceSubmit() {
  if (!finalTranscript.trim()) return;
  const fullContext = `${buildSystemPrompt(personalityId, customPrompt)}
  
---  
Voice input: ${finalTranscript}`;
  // Send fullContext as the user message
  await sendMessage(fullContext);
}
```

This is a one-line change in the `sendMessage` call path — the mic handler just constructs a richer message instead of the raw transcript. Wispr Flow cannot do this because it operates outside the browser.

### Anti-patterns

- **No fallback**: If `isSTTSupported()` is false, hide the mic button entirely (don't show a disabled button).
- **Markdown in TTS**: Always strip markdown before passing to `speechSynthesis.speak()` — raw `**bold**` or `[link](url)` sounds terrible when spoken.
- **Multiple utterances**: Call `window.speechSynthesis.cancel()` before starting a new utterance to prevent overlapping speech.
- **Wispr Flow duplication**: Don't try to "integrate" Wispr Flow via API — it's an OS overlay. Just make sure `<input>` elements exist (they already do).
