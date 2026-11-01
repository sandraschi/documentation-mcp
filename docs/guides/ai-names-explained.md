---
title: "Which AI name is which? A plain-language map (snapshot of 7 October 2026)"
category: guide
status: review
audience: end-users, mcp-dev
last_updated: 2026-10-07
last_verified: 2026-10-07
review_every_days: 7
sources:
  - https://dev.meta.ai/
  - https://platform.claude.com/docs/en/intro
  - https://docs.x.ai/
  - https://hermes-agent.nousresearch.com/
  - https://datanorth.ai/news/meta-releases-muse-spark-1-2-and-muse-code
  - https://openai.com/index/introducing-dots/
# status: review -- the snapshot half of this page is deliberately short-lived (weeks). The
# "decoder" half is meant to last. Where a company's own page could not be read, the text says so.
---
# Which AI name is which?

Nobody could be blamed for being confused. One company now sells a model family, a model inside that
family, a cheaper copy of the same model, a chat assistant, a coding program for the terminal, and a
developer service, and several of those share a single name. Other companies add "agents" and "bots" of
their own. This page sorts them out in plain language.

The page has two halves. **Part 1 is a decoder** that works for any new name, today or next year, and
should stay correct. **Part 2 is a snapshot** of what the names meant on 7 October 2026, and it will
age within weeks: treat it as a convenience, not as a reference.

## Part 1. The decoder

Almost every AI name you meet is one of the following seven kinds of thing. Working out which kind it is
usually answers most of your questions.

1. **A model.** The "brain": a very large program that has learned from text, images and so on. It does
   nothing by itself; some other program has to send it a request. Names usually carry a version number,
   which is why they change so often.
2. **A model family or brand.** A set of related models under one name, for example a small fast one and a
   large careful one. The family name stays while the models inside it are replaced.
3. **A chat assistant (an app or website).** A product for people: you type, it answers. It uses a model
   inside, and you usually pay a monthly subscription for it.
4. **A coding agent.** A program, usually run in a terminal window, that uses a model to read and change
   the files of a software project, run commands, and keep going until a goal is reached. The model is
   the brain; the agent is the body that acts.
5. **An always-on or personal agent.** A program that keeps working for you in the background, often on a
   computer in the vendor's cloud or on a server you own, and reports back. Many companies call these
   "bots", which is the word that causes the most confusion.
6. **A developer service or API** (application programming interface, the way programs talk to a
   service). This is how *other programs*, such as ours, use a model. It is billed separately from any
   chat subscription.
7. **A pricing or data tier.** A variant of one of the above with different cost, limits or privacy terms.
   Some tiers are cheaper because you agree that the company may learn from what you send.

### Five questions to ask about any new name

1. **Which of the seven kinds is it?** If the answer is "a model", ask which program uses it. If it is a
   "bot" or "assistant", ask whether it is kind 3, 4 or 5.
2. **Where does it run?** On your own computer, on a server you control, or in the vendor's cloud. This
   decides what the vendor can see.
3. **How do I pay?** A subscription (kind 3 and some of kind 5), pay-per-use through an API (kind 6), or free.
   A subscription never includes API access, and API use never includes the subscription's app.
4. **Does it learn from my data?** Free tiers and "contributor" or "research" tiers often do. Paid API
   tiers usually do not. Read the data terms before sending private material.
5. **Do our programs need it?** Our programs (the MCP servers in this collection) need kind 6: an API key.
   They do not need the assistants and agents. Those are *clients* that might one day use our tools.

---

## Part 2. Snapshot, 7 October 2026

Each paragraph says what the names are, then whether our programs need it. "Reported" means the claim
comes from news coverage or summaries rather than from a page of the company itself that we could read.

### Meta

Meta's names are the most tangled, because **"Muse" is used for several different things.**

- **Muse** is the name of Meta's *model family*, which Meta's new Superintelligence Labs started
  releasing in April 2026 (reported). It replaced the Llama family as Meta's main line.
- **Muse Spark** is the first and main *model* in that family. It has version numbers: Meta's developer
  page lists Muse Spark 1.3 as the main version and 1.2 and 1.1 as earlier ones. Besides Muse Spark, the
  same page lists an image model (Muse Image), a speech-to-text model (Muse Voice Transcribe) and a
  vision model (SAM 3.1).
- **Muse Spark "contributor"** is not a different model. It is the *same model sold at a much lower
  price on a different tier*, and the catch is stated openly: Meta "may use prompts and completions sent
  to that tier to train future models". It also has a much lower request limit than the standard tier
  (reported: 60 requests per minute per team against 3,000). The name appears in the model identifier
  `muse-spark-1.2-contributor`. This is kind 7 in the decoder.
- **Muse Code**, called simply **"Muse"** on Meta's developer page, is a *coding agent* for the terminal
  ("multi-agent coding in your terminal"), in beta, announced on 5 August 2026 together with Muse Spark 1.2
  (reported). It runs from a command line and has no desktop app. The coverage we read mentions macOS and
  Linux only; whether it works on Windows is unconfirmed.
- **Meta AI** (the app and the website meta.ai) is the *consumer chat assistant* that uses Muse Spark
  inside. This is the "bot" most people mean when they say "Muse". In the app you choose between a fast
  "Instant" mode and a slower "Thinking" mode (reported).
- **The Meta Model API** is the *developer service* (kind 6) that lets programs call the Muse models. It
  replaced the older **Llama API**, which was reportedly shut down on 6 July 2026. It is compatible with
  OpenAI's software library. See [onboarding-ai-providers.md](onboarding-ai-providers.md).
- **Llama** is the older model family. Its model files can still be downloaded and run yourself.

Do our programs need it? Only the Meta Model API, and only if you want a Meta model.

### OpenAI

- **ChatGPT** is the *chat assistant* (kind 3), sold as subscription plans.
- **GPT-6 Astra** is reported as the newest *model*, announced at OpenAI's developer day on 29 September
  2026. Model names change with every release.
- **Codex** is OpenAI's *coding agent* (kind 4).
- **dots** are OpenAI's new *always-on agents* (kind 5), introduced at the same developer day. According to
  reports quoting OpenAI, each dot gets a goal from you, has "its own cloud computer", connects to the
  apps you allow, works between your conversations and brings results back for your review. You reach it
  from ChatGPT, text messages, Slack, Teams or a phone call. The first dot is included with the Pro and
  Business Premium plans, rolled out gradually to adults in supported markets (at launch Pro excluded the
  European Economic Area, Switzerland and the United Kingdom). OpenAI's own announcement pages refused our
  requests, so every dots detail is second-hand.
- **The OpenAI API** is the developer service (kind 6).

Do our programs need it? Only the API. A dot is a different kind of thing: a possible *user* of tools, not
something our programs call.

### Anthropic

- **Claude** is the *model family*. Anthropic's documentation currently names four current models in it
  (called Fable, Opus, Sonnet and Haiku, each with a version number). Pick by reading the models page, not
  from memory.
- **claude.ai** and the **Claude desktop and phone apps** are the *chat assistant* (kind 3).
- **Claude Code** is the *coding agent* (kind 4), used in a terminal, in an editor, or inside the desktop app.
- **The Claude Console** (platform.claude.com) is where developers create API keys and manage billing. **The
  Messages API** is the developer service (kind 6). **Claude Managed Agents** is Anthropic's documented
  way to run a pre-built agent on Anthropic's own computers (kind 5 as a service).

Do our programs need it? Only the API key from the Console. A Claude subscription is separate.

### xAI

- **Grok** is both the *model family* and the *chat assistant* made by xAI; in practice people say "Grok"
  for either. It is built into the social network **X**, has its own website grok.com and phone apps, and
  is reported to be free with limits to X users.
- **SuperGrok** and **X Premium+** are *subscription plans* (kind 7) for heavier use (reported).
- xAI also offers code-focused models; its developer page mentions a coding model with a version number.
  The names are changing fast and we do not list them.
- **The xAI API** (base address `https://api.x.ai/v1`, from xAI's documentation) is the developer service
  (kind 6). We could not read how API keys are issued; check xAI's site.

Do our programs need it? Only the API, if you want a Grok model.

### Nous Research

- **Hermes models** (for example the family called Hermes 4) are open *language models*: files you can
  download and run. They are tuned for conversation and reasoning.
- **Hermes Agent** is a different thing with the same first name: an open-source (MIT licence)
  *personal agent* (kind 5) that you install on your own computer or server and talk to through your
  terminal or chat apps such as Telegram, Discord and Slack. It launched in February 2026 and is described
  as the successor of an earlier open-source agent called OpenClaw (reported). Its documentation warns
  that the Hermes 4 *models* are not recommended for use inside Hermes Agent, because they are tuned for
  chat and reasoning rather than for the rapid tool-calling the agent depends on. That is exactly the
  "model versus agent" trap.
- **Nous Portal** is Nous Research's hosted service for running Hermes Agent.

Do our programs need it? No. Hermes Agent is a possible *client*; see the open questions.

### Google and Microsoft

Covered in their own guides: [onboarding-google.md](onboarding-google.md) (Gemini models and app, AI Studio,
the Agent Platform) and [onboarding-microsoft.md](onboarding-microsoft.md) (Microsoft Graph).

---

## Why "bot" is the word to distrust

"Bot" has been used in this snapshot's sources for a chat assistant (Meta AI, ChatGPT), for an account
that answers you inside a social network (Grok on X), for an always-on agent (dots, Hermes Agent) and for
a coding program (Muse Code, Codex, Claude Code). Those are four different kinds of thing with four different
price models. When you read "bot", stop and ask question 1 of the decoder.

## Where this information comes from

All pages were read on 7 October 2026.

- Meta: https://dev.meta.ai (Meta's own page: model list, "Muse" terminal agent, Meta Model API); coverage
  of Muse Spark and Muse Code from Fortune (8 April 2026), 9to5Mac (5 August 2026) and Datanorth
  (https://datanorth.ai/news/meta-releases-muse-spark-1-2-and-muse-code), which is also the source of the
  "contributor" tier terms. Those are secondary sources.
- OpenAI: search summaries quoting OpenAI's page "Introducing dots" and its "DevDay 2026 Recap" (the pages
  themselves returned "access refused"), plus trade press (The Next Web, Digit).
- Anthropic: https://platform.claude.com/docs/en/intro (names of the current models and the two ways to
  build).
- xAI: https://docs.x.ai (base address and model naming excerpt); products and plans from trade
  summaries (Voiceflow, Verdent), which are secondary sources.
- Nous Research: the official site and documentation at https://hermes-agent.nousresearch.com, as
  summarized by search; the OpenClaw lineage comes from a secondary source.

## Open questions

1. Which of these agents (Muse Code, Codex, dots, Hermes Agent, Claude Code) can use the MCP servers in this
   collection, and how? That decides which of them matter for our documentation.
2. Meta: does Muse Code run on Windows, and is there an official statement on the "contributor" tier terms
   beyond the coverage cited here?
3. OpenAI: confirm the dots details and the model name from OpenAI's own pages.
4. xAI: how API keys are issued and what the plan names currently are.
