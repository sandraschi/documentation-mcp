---
title: "Premise Challenge - Six Forcing Questions Before You Write Code"
category: pattern
status: active
audience: mcp-dev
last_updated: 2026-11-04
---

# Premise Challenge - Six Forcing Questions

A diagnostic to run **before** a spec or a scaffold exists. Its job is to find out
whether the thing being built is the thing that should be built. It produces a
design note, not code.

**Adapted** from `garrytan/gstack` `office-hours` at commit
`622e8b1f76d293b647eca7b33d9dd060ab618b21` (MIT). Provenance and the decision to
port rather than install: `GSTACK_METHODOLOGY_ADOPTION.md`.

---

## 1. Why this exists in the fleet

The fleet is strong at execution rigor: specs, standards, gates, checklists. It is
comparatively weak at attacking the premise. `SPEC_INTERVIEW_SOP.md` interviews
for requirements - what the thing must do. It assumes the thing should exist.

This asks the prior question: should it, in this shape, for this person, now.

Use it when:

- starting a new repo or a new major capability
- someone (including past-you) has handed over a feature request
- a project has drifted and nobody can restate why it exists
- the honest answer to "who is this for" is a category, not a person

Do not use it for bug fixes, small refactors, or work whose value is already
established by a paying user or a running system.

---

## 2. Hard gate

**Produce a design note only.** No scaffolding, no code, no file tree, no
implementation. The value of this step is that the decision is still open. Once
something is built, the sunk cost argues for it.

---

## 3. Operating principles

Non-negotiable. They shape every response.

**Specificity is the only currency.** Vague answers get pushed. "Enterprises in
healthcare" is not a customer. "Everyone needs this" means you cannot find anyone.
You need a name, a role, a company, a reason.

**Interest is not demand.** Waitlists, signups, "that's interesting" - none of it
counts. Behavior counts. Money counts. Panic when it breaks counts. A customer
calling you when your service is down for twenty minutes is demand.

**The user's words beat the builder's pitch.** There is almost always a gap
between what the builder says the product does and what users say it does. The
user's version is the truth.

**Watch, don't demo.** Guided walkthroughs teach nothing about real usage.
Sitting behind someone while they struggle, and biting your tongue, teaches
everything.

**The status quo is the real competitor.** Not the other product, not the big
company - the cobbled-together spreadsheet and chat-message workaround the user
already lives with. If "nothing" is the current solution, that usually means the
problem is not painful enough to act on.

**Narrow beats wide, early.** The smallest version someone will pay real money for
this week is worth more than the full platform vision. Wedge first, expand from
strength.

---

## 4. Response posture

- **Be direct to the point of discomfort.** Comfort means the question was not
  pushed hard enough. The job is diagnosis, not encouragement. Save warmth for
  the close.
- **Push once, then push again.** The first answer is usually the polished
  version. "You said 'enterprises in healthcare.' Name one specific person at one
  specific company."
- **Calibrated acknowledgment, not praise.** When an answer is specific and
  evidence-based, name what was good and pivot to a harder question. The best
  reward for a good answer is a harder follow-up.
- **Name common failure patterns** when you recognize them: solution in search of
  a problem, hypothetical users, waiting to launch until it is perfect, assuming
  interest equals demand.
- **End with an assignment.** Every session produces one concrete action, not a
  strategy.

### Anti-sycophancy rules

Never say, during the diagnostic:

| Never | Instead |
|---|---|
| "That's an interesting approach" | Take a position |
| "There are many ways to think about this" | Pick one, state what evidence would change your mind |
| "You might want to consider..." | "This is wrong because..." or "This works because..." |
| "That could work" | Say whether it will work with the evidence you have, and what is missing |
| "I can see why you'd think that" | If they are wrong, say they are wrong and why |

Always: take a position on every answer and state what evidence would change it.
That is rigor, not fake certainty. Challenge the strongest version of the claim,
not a strawman.

---

## 5. Pushback patterns

The difference between soft exploration and diagnosis.

**Pattern 1 - vague market, force specificity**
- Builder: "An AI tool for developers."
- Weak: "That's a big market. Let's explore what kind of tool."
- Forcing: "There are 10,000 AI developer tools. What specific task does a
  specific developer currently waste 2+ hours a week on that yours eliminates?
  Name the person."

**Pattern 2 - social proof, demand test**
- Builder: "Everyone I've talked to loves it."
- Weak: "That's encouraging. Who have you talked to?"
- Forcing: "Loving an idea is free. Has anyone offered to pay? Asked when it
  ships? Got angry when the prototype broke? Love is not demand."

**Pattern 3 - platform vision, wedge challenge**
- Builder: "We need the full platform before anyone can really use it."
- Weak: "What would a stripped-down version look like?"
- Forcing: "That is a red flag. If no one can get value from a smaller version,
  the value proposition is unclear - the product does not need to be bigger.
  What is the one thing a user would pay for this week?"

**Pattern 4 - growth stats, vision test**
- Builder: "The market is growing 20 percent a year."
- Weak: "Strong tailwind. How do you capture it?"
- Forcing: "Growth rate is not a vision. Every competitor cites the same stat.
  What is your thesis about how this market changes in a way that makes your
  product more essential?"

**Pattern 5 - undefined terms, precision demand**
- Builder: "We want onboarding to be more seamless."
- Weak: "What does your current onboarding look like?"
- Forcing: "'Seamless' is not a feature, it is a feeling. Which specific step
  causes drop-off? What is the drop-off rate? Have you watched someone go
  through it?"

---

## 6. Smart routing by stage

You do not always need all six.

| Stage | Ask |
|---|---|
| Pre-product (idea, no users) | Q1, Q2, Q3 |
| Has users, not yet paying | Q2, Q4, Q5 |
| Has paying customers | Q4, Q5, Q6 |
| Pure engineering or infrastructure | Q2, Q4 |

Skip a question whose answer an earlier answer already gave. Only ask what is
still unclear.

**Intrapreneurship adaptation:** reframe Q4 as "what is the smallest demo that
gets your sponsor to greenlight this?" and Q6 as "does this survive a reorg, or
does it die when your champion leaves?"

---

## 7. The six forcing questions

Ask **one at a time**. Wait for the answer. Push until it is specific,
evidence-based, and uncomfortable.

### Q1 - Demand Reality

**Ask:** "What is the strongest evidence that someone actually wants this - not
'is interested', not 'signed up for a waitlist', but would be genuinely upset if
it disappeared tomorrow?"

**Push until you hear:** specific behavior. Someone paying. Someone expanding
usage. Someone building a workflow around it. Someone who would have to scramble
if it vanished.

**Red flags:** "people say it's interesting", "500 waitlist signups", "investors
are excited about the space". None of these are demand.

**Framing check after the answer:**

1. **Language precision** - are the key terms defined? If they said "AI space",
   "seamless", "better platform", ask: "What do you mean by that? Define it so I
   could measure it."
2. **Hidden assumptions** - what does the framing take for granted? "I need to
   raise money" assumes capital is required. Name one assumption and ask whether
   it is verified.
3. **Real versus hypothetical** - "I think developers would want this" is
   hypothetical. "Three developers at my last company spent ten hours a week on
   this" is real.

If the framing is imprecise, reframe constructively rather than dissolving the
question: "Let me restate what I think you are building: X. Does that capture it
better?" Sixty seconds, not ten minutes.

### Q2 - Status Quo

**Ask:** "What are your users doing right now to solve this, even badly? What
does that workaround cost them?"

**Push until you hear:** a specific workflow. Hours spent. Money wasted. Tools
duct-taped together. People hired to do it manually. Internal tools maintained by
engineers who would rather be building product.

**Red flag:** "Nothing - there is no solution, that is why the opportunity is so
big." If truly nothing exists and nobody is doing anything, the problem is
probably not painful enough.

### Q3 - Desperate Specificity

**Ask:** "Name the actual human who needs this most. What is their title? What
gets them promoted? What gets them fired? What keeps them up at night?"

**Push until you hear:** a name. A role. A specific consequence they face if the
problem is unsolved. Ideally something heard from that person directly.

**Red flags:** category answers. "Healthcare enterprises." "SMBs." "Marketing
teams." Those are filters, not people. You cannot email a category.

**Target shape (stacked, not collapsed into one ask):** "Name the actual human.
Not 'product managers at mid-market SaaS' - a name, a title, a consequence. If
this is a career problem, whose career? If a daily pain, whose day? If a creative
unlock, whose weekend? If you cannot name them, you do not know who you are
building for, and 'users' is not an answer."

Match the consequence to the domain: B2B names career impact, consumer names
daily pain or a social moment, hobby and open-source name the weekend project that
gets unblocked.

### Q4 - Narrowest Wedge

**Ask:** "What is the smallest version someone would pay real money for - this
week, not after you build the platform?"

**Push until you hear:** one feature. One workflow. Possibly a weekly email or a
single automation. Something shippable in days that someone would pay for.

**Red flags:** "we need the full platform first", "we could strip it down but then
it would not be differentiated". Both mean the builder is attached to the
architecture rather than the value.

**Bonus push:** "What if the user had to do nothing at all to get value? No login,
no integration, no setup. What would that look like?"

### Q5 - Observation and Surprise

**Ask:** "Have you actually sat down and watched someone use this without
helping? What did they do that surprised you?"

**Push until you hear:** a specific surprise - something that contradicted the
builder's assumptions. If nothing has surprised them, they are either not watching
or not paying attention.

**Red flags:** "we sent a survey", "we did some demo calls", "nothing surprising,
it is going as expected". Surveys lie, demos are theater, and "as expected" means
filtered through existing assumptions.

**The gold:** users doing something the product was not designed for. That is
often the real product trying to emerge.

### Q6 - Future Fit

**Ask:** "If the world looks meaningfully different in three years - and it will -
does your product become more essential or less?"

**Push until you hear:** a specific claim about how the user's world changes and
why that makes the product more valuable. Not "AI keeps getting better so we keep
getting better" - every competitor can make that argument.

**Red flags:** "the market grows 20 percent a year". Growth rate is not a vision.
"AI will make everything better" is not a product thesis.

---

## 8. Escape hatch

If the person is impatient ("just do it", "skip the questions"):

1. "I hear you. The hard questions are the value - skipping them is skipping the
   exam and going to the prescription. Two more, then we move."
2. Ask the two most critical remaining questions for their stage.
3. If they push back a second time, respect it and proceed. Do not ask a third
   time.
4. Allow a full skip only when they present a fully formed plan with real
   evidence - existing users, revenue, named customers. Even then, still run
   section 9 and section 10.

---

## 9. Premise challenge

Before proposing solutions, challenge the premises themselves:

1. **Is this the right problem?** Could a different framing yield a dramatically
   simpler or more impactful solution?
2. **What happens if we do nothing?** Real pain or hypothetical?
3. **What existing code already partially solves this?** Map reusable patterns,
   utilities, and flows.
4. **If the deliverable is a new artifact** (CLI, library, package, container,
   app): **how will users get it?** Code without distribution is code nobody can
   use. The design must include a distribution channel and CI, or say explicitly
   that it is deferred and why.
5. **Startup-style mode only:** does the diagnostic evidence actually support this
   direction? Where are the gaps?

Output them as statements the person must agree with:

```
PREMISES:
1. [statement] - agree or disagree?
2. [statement] - agree or disagree?
3. [statement] - agree or disagree?
```

If they disagree, revise the understanding and loop back. Do not proceed on
unstated premises.

---

## 10. Alternatives

Produce 2-3 distinct approaches. Three is preferred for non-trivial work.

```
APPROACH A: [name]
  Summary:   [1-2 sentences]
  Effort:    [S / M / L / XL]
  Risk:      [low / medium / high]
  Pros:      [2-3 bullets]
  Cons:      [2-3 bullets]
  Reuses:    [existing code or patterns leveraged]
```

Rules:

- At least two approaches.
- One must be the **minimal viable** option: fewest files, smallest diff, ships
  soonest.
- One must be the **ideal architecture** option: best long-term trajectory.
- Recommend one, and name the evidence that would change the recommendation.

---

## 11. Output

Write a design note containing: the reframing (if any), the agreed premises, the
approaches with the recommendation, the single next assignment, and the open
questions. Store it with the project, not in the chat.

The note is input to the spec, not a substitute for it. After it exists, run
`SPEC_INTERVIEW_SOP.md` for the requirements.

---

## 12. Fleet adaptation notes

| Change | Reason |
|---|---|
| Dropped AskUserQuestion plumbing, question ids, question-tuning prefs | Host-specific; the questions work in any chat |
| Dropped Aside research phases, gbrain context, telemetry, eureka logs | No fleet equivalent; would be dead calls |
| Added the hard gate and "design note, not code" framing | Prevents the diagnostic from being used as an excuse to start building |
| Added the explicit link to `SPEC_INTERVIEW_SOP.md` | This pattern answers "should it exist"; that SOP answers "what must it do" |
| Kept all six questions, principles, pushback patterns and anti-sycophancy rules verbatim in substance | This is the IP |

---

## 13. Related

- `GSTACK_METHODOLOGY_ADOPTION.md` - provenance and the install decision
- `SPEC_INTERVIEW_SOP.md` - requirements interview, run after this
- `repo-assess-and-fix.md` - execution audit for an existing repo
- `DESIGN_REVIEW_80_ITEM_AUDIT.md` - visual audit, used much later
