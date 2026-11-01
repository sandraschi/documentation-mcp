# Primer mandate — Nell's Primer, built properly (mandate first, code second)

**Status:** Mandate adopted 2026-10-04 · not yet built · builds toward it start here
**Tags:** [primer, education, child-safety, local-first, anti-doomster, mandate]
**Research base:** [research/2026-10-04-ai-agents-dots-grokbot-muse-primer-trajectory.md](../research/2026-10-04-ai-agents-dots-grokbot-muse-primer-trajectory.md) (Parts 1-5)

## Thesis (one paragraph)

The short-to-medium-term anti-doomster trajectory is a **non-extractive, locally-runnable, curriculum-owned tutor-companion** after Stephenson's *Young Lady's Illustrated Primer*: story-driven, Socratic, teachable, auditable. The tech exists now (Socratic ITS lineage, small local models, edge compute), the existing Primer skeleton proves the architecture, and the US companion-casino path (ads-as-advice, $500/mo meters, parasocial hooks, political drift) is the thing we explicitly refuse to clone. Paternalism here means **published curriculum + file-owned memory + deterministic validation**, not hidden steering. *Quis custodiet?* The validator's lists, the curriculum diff, and the adult progress view — all versioned, all exportable.

## What we copy from illustrated-primer (ahb-sjsu, MIT)

Assessment 2026-10-04: **2 stars, 0 forks, 0 issues, 2 watchers, ~76 KB, single push July 26 2026** — unknown, unpopular, one-shot student project. But **substantial skeleton, not a runt**: real three-box split (Director → Ractor → deterministic Validator), YAML prerequisite DAG with per-skill human fallbacks, 143 unit tests, live-verified July 25 2026 against NRP gateway + local Atlas fallback (fixed 2 real validator bugs from live runs), honest PRIVACY/ARCHITECTURE docs stating home-network-only, no auth, no child has used it, voice/illustrations/adult-UI unbuilt.

Verdict: **fork the architecture, not the repo.** Rebuild in fleet style (FastMCP portmanteau, start.ps1, Prefab, assfix-zero) with the invariant intact: *nothing model-written reaches a child unvalidated.*

## Honest feasibility

| Part | Reality |
|---|---|
| Socratic + teachable pedagogy | Proven on arXiv (LFTutor, AITEE, Sakshm 1170 learners, PACE, Socratic Playground, HypoCompass +12% debugging) — prompts + misconception ledger, not new science |
| Local small models | Llama-class 7-13B runs on commodity hardware for story beats (Favero et al.); gateway cascade only for hard generation; `nothing-leaves-LAN` flag is a config line |
| Deterministic validator | Reading band + banned topics + PII/outside-world + character-break + hint-leak; conservative wordlists, versioned, teacher-editable (their "die vs dice" fix is the template) |
| Curriculum DAG | YAML per subject, prerequisites, teach_notes, fallback beats; load-time errors on cycles/dupes/missing fallbacks; teacher-diffable |
| Guardian model | Child sees story; adult sees reasons + full logs; provider sees nothing by default; crisis path flags to human, auto-reports only at published imminent-harm threshold |
| Hard parts | Authoring 20+ quality fallbacks per subject; age-band calibration; false-positive tuning on crisis flags; earning teacher trust after Character.AI/Replika grief cases |

## v0 scope (when picked up)

1. Director → Ractor → Validator skeleton against a local model; `reason` string per decision; adult progress view
2. Seed DAG: 20 math + 10 logic skills with age bands, teach_notes, tested fallbacks
3. Local-first cascade (local default, gateway optional, LAN-only flag); per-learner local JSON only
4. Home-network pilot: 2-3 families, pre/post + cognitive-load surveys; no school rollout before that reads clean
5. Published curriculum diff + validator version log from day one (the anti-custody guarantee)

## Later / maybe

School pilot with teacher co-read; "you-teach-Dojo" fallible-bot beats; voice read-aloud; generated illustrations (allowlisted); Bumi-class body as optional peripheral — brain stays the Primer, body stays dumb without it; EU July 2027 child-safety assessment kit as built-in report.

## Non-goals

No subscriptions metered by the week · no ads or ranked "advice" · no lover/persona layer · no streaks/gems/leaderboards · no opaque cloud memory · no auto-reporting dragnet · no "totally suppressed" promises (friction + no-amplification + no-transaction-authority while flagged instead) · no school rollout before home pilot.

## Fleet components to reuse (not reinvent)

- **learnbot-mcp (:11101)** — personas with backstory/voice/skills + safety-guarded chat (topic block, rate limit, PII redaction, audit log) + SM-2 vocab quizzes + grammar check + graded readers + lesson CRUD/generation + VRM avatar + TTS. Primer takes: lesson/quiz/reader engine, safety + audit pattern, persona-as-shifu (not persona-as-girlfriend).
- **classroom-mcp (:11105)** — courses/modules/courseware, assignments, progress (scores, time-spent, vocab mastery), teaching-agent roles (lecturer/tutor/grader/designer), CEFR/JLPT/HSK-aware generation, learnbot bridge. Primer takes: roster + assignment + progress spine, so the tutor's `reason` strings land in a real gradebook instead of a JSON file.
- **japanophile-mcp (:11193)** — vendored kanji (13k), JLPT bank (600 Q), 400k vocab + 278k examples, kana/era utils, streak/due queue, culture/language knowledge pages. Primer takes: proof that vendored-local corpora + honest no-fake-data discipline works; language-learning vertical as first pilot subject.
- Rule: Primer orchestrates, fleet serves. No forked copies of kanji DBs or quiz engines — crossconnect over REST, same as classroom→learnbot bridge.

## Against AI-addling: Bildung by design (European/Swedish paternalist endpoint)

Starting point is openly paternalist — European/Swedish variant: universal, capped, curriculum-bound, audit-positive — aimed at the "good sci-fi endpoint" (Star Trek post-scarcity competence, Culture mild utopia with teeth, not candy). Reference on shelf: **Joe P. L. Davidson, *Saving Utopia* (MIT Press, Mar 2026)** — utopia as endangered species, postdystopian method (start from the grim trajectory, then build resilient hope through concrete institutions). Calibre lookup timed out during drafting — confirm author/edition from library when back.

Bildung guardrails (how Nell stays a thinker, not a prompter):

1. **No-answer default.** Socratic hint ladder first (LFTutor/AITEE/PACE), direct answer only after documented struggle or explicit teacher override. Every direct answer logged as pedagogical debt.
2. **Teach-back beats.** Per unit, the child must teach Dojo (fallible bot) — HypoCompass pattern. No teach-back, no advance. Grades weight explanation, not output.
3. **Allgemeinbildung floor.** DAG spans math, logic, language, history, science, music, crafts — no early specialization funnel. Review scheduler keeps stale mastery alive; streaks/gems banned, Rescue-rule handles motivation.
4. **Real-world acts.** Stanford Smart Primer pattern: every unit ends in a physical act (measure, draw, build, interview, walk). Screen time capped; embodiment via cheap sensors/Bumi-class body later, never as chat extension.
5. **Teacher-in-loop + peer room.** Classroom-mcp assignments + human marketplace referrals; group story rooms (Mouse Army ending, supervised) so Nell learns *with* peers, not *from* a plush.
6. **Evaluate thinking, not throughput.** Pre/post + transfer + debugging (+12% style) + load surveys. DAU/streaks are anti-metrics; report them only to prove we didn't optimize them.

## Why second wins (copy + fleet power + eastern take)

First-mover doesn't decide (OpenClaw proved it: 390k stars from execution + timing + ecosystem, not from being first to say "agent"). The SJSU skeleton sits at 2 stars because it's one dev, no distribution, no pilots, no philosophy. We copy the load-bearing parts (three boxes, deterministic validator, YAML DAG + fallbacks, local cascade, Rescue-first pedagogy) and add what it structurally can't:

- **Fleet power:** FastMCP portmanteau server + start.ps1/start.bat + Prefab adult progress UI + voice-command-bus read-aloud + Calibre-backed story library + .mcpb/NSIS packaging + CI + onboarding. A tutor nobody can install is a thesis; a tutor Sandra can double-click is infrastructure.
- **Eastern take:** shifu over mascot (duty to the student, not retention of the user); wu-wei tutoring (minimal intervention, maximal self-discovery — Socratic withholding as virtue, not trick); koan beats (a "you-teach-Dojo" paradox per unit: *what is the sound of one agent clapping?* — the answer is the child explaining it back); Nell defended, not delighted — the Primer routes *around* skullguns (abusive household, junk curriculum, engagement casino) instead of negotiating with them.
- **Distribution that matters:** home pilots first, teacher-editable curriculum diffs, published validator log. OpenClaw won on registry + skills + word of mouth. We win on classrooms + parents who can read the diff.

## Shifu mechanics (rotation, camouflaged quizzes, shifting presentation)

- **Teacher rotation against unhealthy bonding.** No single persona/voice owns a child. Shifu roster rotates per subject or per term (calligraphy master, garden auntie, ship's engineer) — same Director pedagogy underneath, different Ractor voice/face. Continuity lives in the story ledger, not in one "friend." Explicitly an anti-parasocial device: grief-proof by design (nobody to lose), favoritism-proof (no pretty voice gets more trust).
- **Strength/weakness elicitation via camouflaged quizzes.** Diagnostics never announce themselves. Young kids get games (plum-counting with Dojo, karuta-style cards from the japanophile deck, spot-the-odd-one-out); older kids get teach-back challenges and debugging quests. Every game writes to the same misconception ledger as a formal quiz. Gamified *format*, never gamified *retention* — no streaks, no loot, session ends when the ledger is fed.
- **Illuminated-manuscript presentation: the medium shifts, the message holds.** Reference: *Les Tres Riches Heures* (Limbourg brothers) and medieval books of hours — text, illumination, calendar, and prayer in one object; plus our Plex photo-library page scans as art source. The Primer presents per age/mood/subject: talking picture book (early), bestiary margin-doodles (mid), star charts and hour-tables (timetables as Books of Hours), cute puppy companion (young, warmth without lover-talk), Mechazilla engineer mode (older, systems and building). Same validator, same DAG — presentation is a skin the Director chooses, auditable in the `reason` string. McLuhan with guardrails: the medium teaches, never traps.
