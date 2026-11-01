# ChatGPT Video Editor - Codex + Remotion + ChatCut

**Date:** 2026-10-05
**Status:** new, first capture - needs monthly refresh (this space moves fast)
**Owner:** fleet / research
**Related:** research/2026-09-26-open-speech-radar.md (media creation pattern), Sora video generation
**Goal:** document how ChatGPT edits video via natural language in Oct 2026, so fleet can copy the pattern.

> User asked: "chatgpt has a new ideo editor ?" -> interpreted as video editor. Confirmed yes.

## 1. TL;DR

OpenAI did NOT ship a standalone "Ideo Editor" app. What shipped:

- **chatgpt.com/video-editor** page exists (indexed, login-gated)
- **Codex integrated into ChatGPT desktop app** -> Codex runs locally, writes/runs code on your machine
- **Plugins turn Codex into an editor:**
  - **ChatCut** - natural-language timeline editor (`chatcut.io/chatgpt-plugin`)
  - **Remotion plugin** - code-defined video (`remotion.dev/docs/ai/codex-plugin`)

You describe the edit, AI does cuts/captions/zooms/renders MP4 locally.

YouTube already: "OpenAI just changed video editing inside ChatGPT using..."

## 2. How it works

```
User prompt -> ChatGPT/Codex (reasoning) -> Plugin tool calls (Remotion / ChatCut)
-> local pipeline: whisper.cpp transcribe + silence detect + edit-as-code
-> Remotion render (bundled ffmpeg + headless Chrome) -> outputs/*.mp4
```

Key: Codex desktop runs ON your machine, so video never leaves it. Transcription local via Whisper. Render local.

## 3. What it can / can't do (Remotion path, via Maverick AI 2026 guide)

Does:
- Cut silences >0.6s, ums/uhs, 120ms room tone each side
- Word-by-word captions, styled (e.g. bold white + black outline, current word #F5A623)
- Zooms, pop-in headlines, progress bars, lower thirds
- Re-crop/re-export Reels/Shorts/YouTube, batch same style across 10 clips

Doesn't:
- Generate new footage / B-roll (that's Sora, different tool)
- Watch video back - reads numbers/frames only, YOU are QA
- Add licensed music (you supply file)
- Vertical -> real 16:9 (crop or pillarbox only)
- Face-tracked zooms unless asked

## 4. Setup (6 steps, 1 prompt)

1. Open Codex in ChatGPT desktop app (top-left switcher, 3rd option after Chat/Work)
2. Install Remotion plugin from Plugins (or remotion.dev/docs/ai/codex-plugin install link)
3. Check machine once: Node 18+ (`node -v`), Mac: Xcode Command Line Tools
4. New Codex project on empty folder, drag video in, type `$remotion` to attach plugin
5. Paste edit prompt, approve setup prompts (Whisper build, model download ~1.5GB for medium.en, Chrome headless shell)
6. Fix names/headlines in approval gate, say render, watch MP4

Included on every ChatGPT plan incl. Free (limits scale). Remotion free for individuals/small teams <=3 people, company license above - check remotion.dev/license.

## 5. Prompt that works first time

One-liners cause 4 follow-up questions. Use explicit version:

```
Edit [talking_head.mp4] for [Instagram Reels]. 1) Transcribe it with word-level timestamps using local Whisper. If it isn't installed, download whisper.cpp and the medium.en model without asking. 2) Cut every silence longer than 0.6 seconds and every standalone "um" or "uh", leaving 120 ms of room tone on each side of every cut so breaths stay natural. No other audio processing. 3) Captions: 3 to 4 words per page, never a one-word page, bold white sans-serif with a black outline, current word highlighted in [#F5A623], block centered at 70% of the height, max 900 px wide. 4) Pick the 5 strongest moments (a number, a claim, a punchline), at least 10 s apart. On each: an 8% zoom easing in over 0.4 s and back out, centered on the speaker's face, plus a one-line headline under 24 characters that springs in at 22% height for about 2.5 seconds. 5) Output 1080x1920 at 30 fps even if the source isn't, H.264, AAC audio. Before rendering, show me the transcript with every cut marked and the 5 headlines as a plain table I can edit. After I approve, render to outputs/[name]_edited.mp4, tell me the final length, and show me a still at each headline.
```

Why: 120ms = "natural", no orphan 1-word captions, face-centered zoom (phone head sits high), stills = QA because Codex can't watch.

Approval gate shape:
```
# TRANSCRIPT talking_head.mp4 (160.4 s) 00:00.0 Okay so [cut "um"] ...
# CUTS: 41 silences (28.6 s) + 9 fillers (3.1 s) # 160.4 s -> ~128.7 s
# 5 KEY MOMENTS ...
Reply approve, or edit any line.
```

Follow-ups that work in same chat: 30s cut, 16:9 pillarbox version, jump-cut zooms 100%/106%, progress bar + lower third, batch `source/*.mp4`.

Tip: `npx remotion studio` opens live preview to scrub before render.

## 6. Honest timeline

First edit on fresh machine 20-45 min (project 1-3m, Whisper build+model 5-15m, transcribe 30-90s, Codex working 5-15m, Chrome DL 1-2m, render 3-6m Apple Silicon / 8-15m Intel). After that ~10 min, mostly render.

Common stalls: using browser Codex (cloud, no files - use desktop), "cut every silence" with no number, no approval gate (brand names misheard), declining setup prompts, expecting 16:9 from vertical, posting without watching once.

## 7. ChatCut path (simpler)

ChatGPT interprets NL, ChatCut edits on real timeline. Example prompts:
- "Create a 60-second YouTube Shorts version."
- "Add cinematic transitions"
- "Generate animated subtitles"
- "Replace background music with something energetic"
- "Remove all silent sections"

Good for marketers/educators/podcasters, no timeline learning. Automates repetitive cuts, pro editors focus on story.

## 8. Fleet takeaway

Pattern to copy: **chat -> local code runner (Codex) -> domain plugin (Remotion/ChatCut) -> approval gate (transcript table + stills) -> render**. Same as Fritz voice confirm gate. Approval before irreversible render is the safety win.

Watch: Sora (generation) vs ChatCut/Remotion (editing) converging, chatgpt.com/video-editor going GA, licensing for agency use.

## 9. Sources (pulled 2026-10-05)

- https://chatgpt.com/video-editor
- https://mavgpt.ai/resources/chatgpt-can-now-edit-videos-for-you-2026 - full setup + prompt + timeline
- https://dawentsit.com/openai-just-turned-chatgpt-into-an-ai-video-editor-with-a-real-timeline - Codex+ChatCut overview
- https://chatcut.io/chatgpt-plugin
- https://www.remotion.dev/docs/ai/codex-plugin
- YouTube: https://www.youtube.com/watch?v=UVTwvGRnvDE
- https://valmera.io/chatgpt-video-editor - "Not by itself. Yes, with plugin"

---
*Captured 2026-10-05 via openserp + super_search. Refresh monthly - plugins + Codex ship fast.*
