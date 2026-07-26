# Wispr Flow — Voice Dictation for the Fleet

**Website**: https://wisprflow.ai  
**Platform**: Mac, Windows, iOS, Android  
**Pricing**: ~$20/mo Pro (14-day free trial)  
**Funding**: $81M (Wispr AI)

---

## What it is

Wispr Flow is a **system-level voice dictation overlay**, not an API or SDK. It listens at the OS level and types into any input field in any app — VS Code, Cursor, Claude, ChatGPT, terminals, webapps. The fleet's React `<input>` / `<textarea>` elements work with it automatically with zero integration code.

## Why it matters for the fleet

| Aspect | Browser Web Speech API | Wispr Flow |
|--------|----------------------|------------|
| Cost | Free | ~$20/mo Pro |
| Browser | Chrome/Edge only | Any app, any browser |
| Latency | Server-side (slow) | On-device (fast) |
| Accuracy for code | Poor | Good (developer-focused) |
| Filler-word removal | No | Yes (AI auto-edits) |
| Personal dictionary | No | Yes |
| Voice snippets | No | Yes |
| Languages | ~30 | 100+ |

## Fleet recommendation

**Tier 1 — Free** (browser Web Speech API, always available):
- Use `useSpeech()` hook (see `standards/rules/chat_speech_sota.md`)
- Works in Chrome/Edge for basic dictation
- ~40 lines of code, no API keys

**Tier 2 — Premium** (Wispr Flow, user-purchased):
- Works automatically — no code changes needed
- `<input data-testid="chat-input">` elements already work
- Recommend for developers doing heavy code work via chat

## Tags

`[wispr-flow, voice, dictation, speech, accessibility]`
