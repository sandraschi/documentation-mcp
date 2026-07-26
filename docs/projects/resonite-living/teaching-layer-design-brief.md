# learnbot-mcp + classroom-mcp — Teaching Layer Design Session

*Brief v2, 2026-07-20. Reordered: correction problem promoted to deliverable #1
(it determines everything downstream). Tool inventories extracted from live
repos on Goliath, 2026-07-20.*

## Who / context
I'm Sandra, Vienna. I maintain 50+ FastMCP servers (Python, FastMCP 2.10.1+,
dxt-packaged, GitHub user sandraschi, repos at D:\Dev\repos). Always-on
Windows workstation "Goliath" (RTX 4090 24GB, WSL2). AI-assisted dev,
timelines in days.

## The consuming project (why these two servers matter now)
"Nekomimi-chan": a conversational NPC in Resonite (VR platform), interacted
with from desktop now, via Pico 4 HMD later. Primary use case: advanced
Japanese language practice through natural conversation with her in-world.
Her "cybermind" runs on a LOCAL LLM — jackrong distilled models on the 4090 —
for zero running cost. She hears speech, converses, and should TEACH:
correct my Japanese, adapt difficulty, remember my progress across sessions,
run structured practice when asked, freeform conversation otherwise.

The teaching intelligence must live in two existing fleet servers, chained
into her pipeline alongside resonite-mcp and mcp-central-docs.

## Current state of the two servers (extracted 2026-07-20)

### learnbot-mcp — mature, 35 MCP tools, dxt + Tauri/NSIS packaged, tested
Per STATUS.md (2026-07-16) all areas ✅. Tool inventory from server.py:

- **Persona**: persona_create / persona_get / persona_list / persona_delete
- **Conversation lifecycle**: chat_start, chat_send, chat_hibernate,
  chat_resume, chat_destroy, chat_list
  — chat_send is the fat path (~160 lines): LLM call → emotion-tag
  inference → TTS via speech-mcp → robot orchestration (yahboom-mcp).
  Latency profile of this chain is UNMEASURED. That measurement is a
  prerequisite for any real-time design claims.
- **Lessons**: lesson_create / lesson_get / lesson_list / lesson_update /
  lesson_delete / lesson_generate / lesson_differentiate / lesson_run
  (framework-aware: JLPT, CEFR, HSK, DELF, …)
- **Learning tools**: vocab_quiz + vocab_submit — **SM-2 spaced repetition
  already implemented**, per-user_id, SQLite; grammar_check — single LLM
  pass, prompt-and-parse-JSON, quality = quality of backing model;
  reading_passage; graded_reader
- **Japanese reference data (local, bundled)**: kanji_search, vocab_lookup,
  jlpt_vocab_by_level, example_sentences, jlpt_quiz — backed by
  data/kanji.db and data/jlpt_questions.db, no external service
- **Ops/safety**: safety_rule_create/list/delete, audit_query,
  chat_proactive_tick, platform_send, chatbot_help; compliance module
- **LLM bridge**: llm_client.py → Ollama, **default llama3.2:3b**, falls
  back to any OpenAI-compatible endpoint. NOTE THE DISCREPANCY: the
  nekomimi plan says jackrong distilled on the 4090; the server currently
  defaults to a 3B model. grammar_check's usefulness at N2/N1 was never
  validated against either. The session must treat "what model actually
  backs grammar_check" as an open variable, not solved.
- REST API on :11101 + React SPA (9 pages) + VRM viewer + desktop mascot.

### classroom-mcp — thin CRUD layer, ~41 tools, NOT packaged, effectively untested
Per STATUS.md (2026-07-16): "No tests — two bugs (email upsert collision,
learnbot bridge port/path) shipped undetected." No README, no dxt manifest,
no Tauri native dir. Tool inventory from tools.py:

- **Students / classes**: student_create/get/list/update/delete,
  class_create/get/list/update/delete, class_add_student,
  class_remove_student
- **Assignments / progress**: assignment_create, assignment_list,
  assignment_delete, **progress_record, progress_list** (scores, time
  spent, vocab mastery per student/assignment)
- **Courses / modules / courseware**: full CRUD on all three
- **Teaching agents**: agent_create/list/delete (lecturer/tutor/grader
  roles per course)
- **Human teacher marketplace**: human_teacher_create/get/list/delete,
  referral_create/list/update_status
- **AI generation**: syllabus_generate, courseware_generate_ai,
  syllabus_list, assignment_create_with_lesson (bridge → learnbot-mcp
  lesson_generate over LEARNBOT_URL, :11105 → :11101)

Honest reading: learnbot-mcp already contains ~80% of a teaching layer
(SRS, grammar check, lessons, JLPT data). classroom-mcp is a multi-student
LMS skeleton whose only obviously nekomimi-relevant pieces are
progress_record/progress_list and maybe assignment scaffolding. What is
MISSING everywhere: a learner model beyond per-word SM-2 (no error
tracking, no register habits, no collocations, no pitch accent), any async
/ fire-and-forget path, and any mechanism for review-through-conversation.

## Hard constraints
- Real-time conversation: the teaching layer sits inside a speech loop.
  Any tool call that blocks the NPC's reply for >~1–2s kills immersion.
  Design for async/background where possible (error logging and
  learner-model updates must not block the response). First step of any
  latency claim: MEASURE the existing chat_send chain.
- VRAM budget (assumptions — correct me if wrong): 24GB total; assume
  jackrong distilled model ~8–14GB at usable quant, STT (whisper-class)
  ~1–3GB, TTS ~1–2GB, Resonite + desktop rendering pressure 2–4GB.
  Conclusion to test, not assume: there is NO room for a second
  concurrently-loaded correction model. Designs requiring one must say so
  and propose sequencing (model swap, CPU offload, or cloud).
- Cloud is EXPLICITLY AUTHORIZED for batch/post-session analysis if the
  local-only math doesn't work — but quantify it: calls per session ×
  tokens × price, monthly total at ~1 session/day, against a €100/month
  all-in AI budget that is already partly spoken for.
- FastMCP 2.10.1+, Python, Windows host. Persistence on local disk is fine.
  SQLite is the incumbent (both servers use it); don't introduce a new
  store without a reason.
- Learner: one primary user (me), advanced Japanese — JLPT N2-ish
  conversation with N1 aspirations, not beginner flashcards. Learner model
  must cover: nuance, register (keigo vs casual), collocations, pitch
  accent — not hiragana drills. (Pitch accent note: text-normalizing STT
  destroys the signal; be honest about whether it's detectable at all in
  this pipeline, or belongs on the cut list.)
- Must also remain useful as standalone MCP servers in Claude Desktop
  (fleet standard), not become nekomimi-only appendages. Known tension:
  truly async fire-and-forget tools are awkward in Claude Desktop's
  request/response world. Sync-with-fast-path compromises are acceptable
  if named as compromises.

## What I want from this session (deliverables, in order)

1. **The correction problem** (moved to #1 — it shapes everything below):
   how does the pipeline detect N2/N1-level Japanese errors when the
   listener is a distilled local model that may itself be shaky at nuance —
   and whose current default is literally llama3.2:3b? Options: in-line
   self-monitoring, dedicated correction pass, batch post-session analysis
   (local or cloud), hybrid. For each: what error classes it can actually
   catch (particle errors vs register slips vs unnatural collocations),
   latency cost, VRAM cost, money cost. Recommendation with numbers.
   "In-line correction limited to what the conversational model catches
   for free; everything else async/batch" is an acceptable answer if the
   analysis supports it.

2. **Responsibility split**: what belongs in learnbot-mcp vs classroom-mcp
   vs the LLM prompt vs nekomimi's orchestration glue — given the actual
   inventories above. Explicitly answer: does classroom-mcp belong in this
   pipeline AT ALL, or does the learner model land in learnbot-mcp with
   classroom-mcp as an optional progress ledger? "Drop classroom-mcp from
   the pipeline" is an acceptable answer. Be opinionated; a blurry
   boundary here means duplicated logic later.

3. **Learner-model design**: schema for persistent learner state (errors,
   mastered patterns, register habits, review queue), extending — not
   duplicating — the existing SM-2 vocab tables. Where it lives, how it's
   updated mid-conversation without blocking, and how spaced repetition
   works when "review" happens through conversation. Expectation setting:
   conversational review = the server injecting "try to elicit usage of
   X, Y, Z" into the system prompt and DETECTING whether elicitation
   happened — not guaranteeing it. No fantasy schedulers.

4. **Tool API design**: concrete FastMCP tool signatures for whichever
   server(s) survive deliverable #2 — names, params, return shapes —
   covering: correction/feedback, difficulty adaptation, session/lesson
   orchestration, progress queries. Reuse/extend existing tools where they
   fit (grammar_check, vocab_submit, lesson_run) rather than inventing
   parallel ones. Design for a mid-tier local LLM caller: simple,
   forgiving schemas; no 12-parameter tools.

5. **Phased build plan**: days-scale phases, each demoable. Phase 0 is
   measurement: instrument chat_send, get real latency numbers for the
   current chain with the jackrong model actually loaded. Phase 1 must
   work in the CURRENT desktop setup (nekomimi spawned in her Home
   session, ResoniteLink on :21789). Mark MVP explicitly.

6. **What NOT to build**: scope traps — full LMS features, multi-user
   classrooms, gamification, conversation memory beyond the learner model,
   and (pending #1) possibly pitch-accent detection. Cut list with reasons.

## Rules for this session
- State assumptions explicitly instead of asking clarifying questions;
  I'll correct wrong ones.
- Brutally honest about what a distilled local model can and cannot do
  in this loop. No hype. If a deliverable needs a cloud model to work
  acceptably, say so and quantify the cost implication.
- No stubs presented as solutions.
- Concrete: real tool signatures, real schema fields, real library names.
- Output as one continuous markdown document (it will live in
  D:\Dev\repos\mcp-central-docs\projects\resonite-living).
