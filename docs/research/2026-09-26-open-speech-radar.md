# Open Speech Radar - Fritz Must Talk and Understand

**Date:** 2026-09-26
**Status:** living doc, update monthly (this space moves fast)
**Owner:** speech-mcp + fleet-agent-mcp (fritz)
**Related:** NEXT_AI_WAVE_ENDUSERS.md, research/2026-09-26-rabbit-os3-analysis.md
**Goal:** fritz talks to Sandra and understands the response, fully local-first, cloud-optional. No token meter, no ads.

## 1. Required loop (hoi-polloi bar)

wake -> VAD -> streaming STT -> intent (fritz Voice Bus) -> action -> streaming TTS with barge-in -> confirm in voice for irreversible/external.

Latency budget: wake <300ms, first STT partial <500ms, TTS first packet <400ms. Anything slower feels broken to endusers. Text fallback always, voice primary.

Current fleet baseline (speech-mcp 0.6.5, live pyproject):
- STT local: FunASR (optional funasr extra, modelscope) + sherpa-onnx 1.12.40 + onnxruntime. Sidecar :10914 noted in earlier survey.
- Streaming: sherpa-onnx + openwakeword 0.4.0.
- Cloud: google-genai (Gemini Live), hume, elevenlabs. Local free: pyttsx3 + Windows SAPI5.
- Memory: LanceDB + fastembed transcripts.
- Bus: FLEET_VOICE_DELEGATE=1, fritz POST /api/voice/intent.

That covers the loop. What is stale is model choice, not plumbing.

## 2. STT to watch (open weights, local runnable)

- **FunASR family (Alibaba)** - incumbent in our stack. Track FunASR-nano / SenseVoice / firered-asr2 comparisons (Douyin July 2026 shootout lists v2.5-asr, firered-asr2, glm-asr-nano, cohere-transcribe, sense-voice, fun-asr-nano for Mandarin + dialect + meeting + song). Action: keep FunASR sidecar, add SenseVoice variant for Mandarin/dialect test.
- **Qwen3-ASR / Qwen-Audio-3.x** - Alibaba Qwen audio line is sweeping 2026: Qwen-Audio-3.0-TTS topped Speech Arena (WAIC July 2026), Qwen-Audio-3.1 leads ASR+TTS+Realtime per Yunqi Sept 22 2026 notes. ASR side same lineage. Action: eval Qwen3-ASR vs FunASR on German + English + Mandarin (Sandra trilingual).
- **NVIDIA Parakeet / Canary / Granite Speech** - Feb 2026 open LLM roundup still lists Whisper Large V3, Canary, Qwen 2.5B-era, Granite Speech 3.3 as RAG-relevant STT. Parakeet fast conformer path matters for 4090 throughput. Action: keep Whisper Large V3 as reference, bench Parakeet for speed.
- **Vosk vs Whisper vs FunASR** - July 2026 CSDN offline shootout (edge + privacy angle). Vosk small, Whisper accurate, FunASR balanced. Action: Vosk only for tiny nodes, not Goliath.
- **GLM-ASR-Nano (Zhipu)** - in same shootout. Watch only, residency flag (same as Z.ai rule).

## 3. TTS to watch (open weights, local runnable)

- **Qwen3-TTS 0.6B 12Hz** - key one. 0.6B, first-packet fast, local real-time viable. Qwen3-TTS-Tokenizer PESQ 3.21 wide / 3.68 narrow (Jan 2026 guide). Flash = realtime, Plus = quality. Action: P0 candidate to replace pyttsx3 default for Fritz voice.
- **Qwen-Audio-3.0-TTS-Plus / 3.1-TTS-Next** - Plus topped Artificial Analysis Speech Arena. Next (Yunqi Sept 22 2026) is audiogen: one shot generates voice + SFX + ambience + music, multi-speaker podcast. Action: Plus for quality voice, Next for creations/podcast jobs.
- **Kokoro** - 82M, Apache, still the small-local king. Keep as fallback when VRAM tight.
- **Chatterbox / Orpheus / MOSS-TTS v1.5 / Supertonic** - June 2026 reshuffle notes: MOSS v1.5 MOS 4.0 for ZH/EN mix, Nano/Supertonic 20+ langs but weaker cloning. Orpheus fine-tunes (e.g. Bangla paper) show cloning path. Action: Chatterbox for expressive, MOSS for ZH/EN mix.
- **Hume / ElevenLabs** - keep as cloud quality option only, never default. Cost trap.

## 4. Full-duplex / speech-to-speech to watch

- **Kyutai Moshi (+ Moshiko)** - still the open full-duplex reference. Interrupt handling done right. Action: track Moshi 2.x, borrow barge-in logic even if we keep pipeline ASR->LLM->TTS.
- **Qwen2.5-Omni / Mini-Omni / Llama-Omni class** - end-to-end speech models. Latency win, control loss. Action: eval one omni path for r1-style push-to-talk, keep pipeline for tool calls.
- **Pipecat / LiveKit Agents** - not models, but the plumbing everyone uses for transport + VAD + turn-taking. Action: copy their VAD + turn-taking thresholds, do not adopt framework wholesale.
- **soniqo/speech-swift** - Apple Silicon STT/TTS/speech-to-speech toolkit listing Qwen3-ASR among 52 langs. Useful as Mac Studio target reference.

## 5. Wake / VAD / diarization

- Keep openwakeword + Silero/WebRTC VAD. Picovoice Porcupine only if custom wake accuracy fails (commercial).
- Diarization + speaker ID: needed for family mode (who said it). See Google CC pattern - per-member memory split requires knowing who spoke.

## 6. What Fritz needs next (ordered)

1. **Default local voice pair:** FunASR (or Qwen3-ASR if bench wins) + Qwen3-TTS-0.6B-Flash, streaming, barge-in on. Cloud TTS behind flag only.
2. **Trilingual bench:** German + English + Mandarin WER/MOS on Goliath 4090. Sandra speaks all three; most evals do not.
3. **Voice confirm gate:** spoken readback for irreversible/external sends (`send email to X, correct?`), same POLICIES.yaml as text confirm queue.
4. **Speaker tag:** who spoke -> memory_user:<id> routing (ties to family work).
5. **Monthly refresh job:** aiwatcher watches HF trending + Qwen/Kyutai/NVIDIA releases, files update PR to this doc. No silent drift.

## 7. Google - very active, mostly cloud + one open gift

Search retry 2026-09-26 via mega (google/bing/duckduckgo all responded):

- **Gemini-TTS GA Dec 11 2025** - 30 voices, 70+ locales, single + multi-speaker, style/accent/pace/tone via natural-language prompt. Docs: docs.cloud.google.com/text-to-speech/docs/gemini-tts.
- **Gemini 3.1 Flash TTS (Q2 2026)** - 70+ langs, 30+ voices, streaming, bracket tags for non-speech sounds, multi-speaker dialogue. In AI Studio.
- **Gemini 3.8 Flash TTS + Flash-Lite TTS (Sept 23 2026, 3 days ago)** - most expressive yet. Flagship = studio fidelity across 130+ langs, Lite = low-latency throughput. Voice Design from text (describe accent/tone/age), line-by-line direction (pacing, emotion, turn-taking, conversational sounds), custom voice from scratch or replicate with verbal consent, SynthID watermark. Announced by Logan Kilpatrick, benchmark-topping per SiliconANGLE. Action: cloud quality reference for Fritz, never default (cost + watermark + consent flow).
- **Chirp 3 STT** - multilingual ASR, 24 GA langs + 77 preview, auto lang detect, punctuation, denoising, diarization, streaming, V2 API. Coval benches daily (last 2026-09-25). Action: accuracy/latency reference to beat locally.
- **Chirp 3 HD voices + Instant Custom Voice** - Cloud TTS tier, SSML pause/pace, cloning. Versus Gemini TTS: Chirp = controlled/enterprise, Gemini = expressive/creative.
- **Gemini 3.5 Transcribe (Aug 26 2026)** - context-aware dictation in Gboard, Antigravity, Gemini app, Chrome. Interesting pattern: transcription with app context, not bare ASR. Copy for ViLife/fritz inbox.
- **Gemini Audio / Live API (Sept 15 2026)** - realtime conversational models, Gemini 3.8 Live topped Speech-to-Speech Index 82.6. Live API $1/1M input. Pricing refs: 3.5 Flash TTS $6/1M out, 3.1 Flash TTS $20/1M. Action: keep google-genai Live path in speech-mcp as cloud full-duplex option.
- **Gemma 4 (Apr 2 2026, Apache 2.0)** - first fully OSI-open Gemma. Dense + MoE 2.3B-31B (E2B/E4B/26B MoE/31B), 256K ctx, native text+image+audio, improved audio encoders, ONNX checkpoints for edge/browser, day-0 transformers support. Audio understanding guide June 5 2026 (ASR/translation). MedGemma 1.5 4B + MedASR free Jan 2026. Action: only open gift in this list - eval Gemma 4 audio encoder for on-device ASR/understanding, especially Mac Studio target.

Rule: use Google as benchmark + cloud fallback, not base. Local pair stays Qwen/FunASR + Qwen-TTS/Kokoro. Re-check quarterly, they ship monthly.

## 8. Watch list (sources that actually move)

- Hugging Face trending (Qwen/DeepSeek families dominate Apr 2026 radar).
- Alibaba Qwen Audio releases (WAIC, Yunqi).
- Kyutai releases.
- NVIDIA NeMo / Parakeet.
- CSDN/smzdm 2026 TTS reshuffle threads (surprisingly current for ZH open TTS).
- AssemblyAI free STT roundup 2026 (good baseline table).

---
*Baseline from speech-mcp pyproject 0.6.5 live 2026-09-26. Model notes from Baidu/CSDN pulls same day (Google/Yandex captcha-blocked, treat ZH press as lead not gospel). Refresh monthly.*
