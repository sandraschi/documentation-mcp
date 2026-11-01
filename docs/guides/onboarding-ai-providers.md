---
title: "Onboarding: AI model providers (OpenAI, Anthropic, Meta)"
category: guide
status: review
audience: mcp-dev, end-users
last_updated: 2026-10-07
last_verified: 2026-10-07
review_every_days: 14
sources:
  - https://platform.claude.com/docs/en/get-started
  - https://platform.claude.com/docs/en/get-api-key
  - https://platform.claude.com/docs/en/manage-claude/authentication
  - https://support.claude.com/en/articles/11145838
  - https://developers.openai.com/api/docs/quickstart
  - https://developers.openai.com/api/docs/guides/production-best-practices
  - https://dev.meta.ai/
  - https://www.spheron.network/blog/meta-shut-down-the-llama-api-self-hosting-llama-is-now-offic/
# status: review -- written 2026-10-07 from the providers' own documentation where it could be
# read, and from secondary sources where it could not (each statement says which).
# Deliberately contains NO model names, prices, plan names or limits: those change weekly.
---
# Getting access to AI model providers (OpenAI, Anthropic, Meta)

This page explains how a program in this collection gets permission to use a commercial AI model:
what you sign up for, where the key comes from, how it is billed, and the few traps that catch
people. It covers **OpenAI**, **Anthropic** (the company that makes Claude) and **Meta**. The matching
guides for services that need a more involved setup are
[onboarding-microsoft.md](onboarding-microsoft.md) and [onboarding-google.md](onboarding-google.md).

## 1. What this page leaves out on purpose

These three companies change their model lineups, subscription plans, prices, usage limits and
branded products every few weeks. Any list of them written here would be wrong within a month, and a
wrong list that looks authoritative is worse than none. So this page contains only the things that have
stayed true for a long time: *where* you get a key, *how* you pay, and *how* to avoid the usual
mistakes. For anything that changes, each section ends with the provider's own page to check.

The same rule applies to our programs: **a program should never have a model name written into its
code or its documentation.** It should read the model from a setting, or ask the provider which
models exist. Then a model being retired is a settings change, not a bug.

If the product names themselves are what confuse you (for example the several different things Meta
calls "Muse", or the difference between a model, a chat app and an "agent"), read
[ai-names-explained.md](ai-names-explained.md) first. It explains the seven kinds of thing that AI names
usually refer to and gives a dated snapshot of who calls what by which name.

## 2. Four things that are true for all three

**A chat subscription is not API access.** Paying for a chat product (a ChatGPT plan, a Claude Pro or
Max plan, the Meta AI app) gives you the company's own app. A program of ours talks to the company's
*API* (application programming interface, the way programs talk to a service), and that is a separate
account with separate billing. Anthropic states it directly in its support article of 19 August 2026:
"these are separate systems", and subscriptions "do not include automatic API access". The same
separation applies to the other two companies; we have confirmed it only for Anthropic.

**You pay the API per use, usually in advance.** The API is billed by how much text is processed, not
by a monthly fee. Details of how you top up differ per company and are given below.

**The key is shown once.** When you create an API key (a long secret string that identifies you to
the service) the website shows it a single time. Copy it into a password manager immediately. If you
lose it you create a new one; nobody can show it to you again.

**Keys go in environment variables, never in files that are shared.** An environment variable is a
named setting of your computer that programs can read. Each company's official software kit (called an
SDK, a software development kit) looks for one particular variable name automatically, which is listed
below. Never put a key in source code, a screenshot, a chat message or a file that is committed to
version control.

## 3. OpenAI

**What you need.** An account at https://platform.openai.com and an *organization* (the account's
container; one is created for you). Inside it, every API key belongs to a *project*. You can use the
default project or create separate ones, for example one per program, so that you can see and cap each
program's spending separately.

**Getting a key.** OpenAI's documentation sends you to the page *Settings, Organization, API keys*
(https://platform.openai.com/settings/organization/api-keys), where you create a new secret key, give it a
name, and choose its project. OpenAI's quick-start says its software kits read the variable
**`OPENAI_API_KEY`**, and gives `setx OPENAI_API_KEY "your_key"` as the Windows way to set it. A detail
that trips people up on Windows: `setx` saves the value for programs started *afterwards*; the terminal
window you typed it in does not see it until you open a new one (general knowledge, not from the page).

**Good key habits (from OpenAI's production guidance).** Set an *expiration date* when you create a
project key and rotate it on a schedule: create the replacement, update the program, check it works, then
revoke the old key. Administrators can enforce a maximum key lifetime for the whole organization, and
can restrict which kinds of keys may be created at all.

**How you pay.** OpenAI's help center describes *prepaid billing* for new accounts: you buy credit in
advance, and the API works while a balance remains. A search summary of that article gives a minimum
purchase of five dollars, credits that expire after a year, and a required bank-backed credit or debit
card (no gift cards or virtual cards). We could not read the article itself (the site refused the
request), so check the amounts and rules on the billing page before relying on them. New accounts also
start with low rate limits that rise with usage and payment history.

**Check that your key works.** Listing the models your key may use is a harmless request that needs no
credit: `curl https://api.openai.com/v1/models -H "Authorization: Bearer %OPENAI_API_KEY%"`
(on Windows PowerShell use `$env:OPENAI_API_KEY`). A list means the key is good; an authentication error
means it is wrong or expired (general knowledge, not re-checked today).

**Look up, do not memorize:** current models and prices at https://developers.openai.com/api/docs
(the documentation moved from platform.openai.com/docs to this address, which redirects).

## 4. Anthropic (Claude)

A note of honesty: the author of this page is itself an Anthropic model, so every Anthropic statement
below was checked against Anthropic's current documentation instead of being written from memory.

**What you need.** A *Claude Console* account at https://platform.claude.com. The Console is the
developer site, separate from the consumer chat app at claude.ai. An organization is created with the
account, and inside it *workspaces* group keys and spending.

**Getting a key.** Open *Settings, API keys* (https://platform.claude.com/settings/keys) and click
**Create key**. You name the key, choose how long it lives, and set the **Linked account**. Three kinds of
key exist:

- A **personal key** acts as you and stops working if you leave the organization. Use it for your own
  development.
- A **service account key** belongs to a robot identity and is the right choice for anything shared or
  automated.
- A **workspace key** belongs to no person. Anthropic now calls it legacy and prefers the other two.

The expiration choices are three hours, one day, seven days, thirty days, a custom duration, or
**Never** (for keys you keep in a secrets manager and rotate yourself). An organization can forbid
"Never". Anthropic emails you before a key expires, and an expired key answers with a 401 error and
cannot be revived; you create a new one. The full key, which begins with `sk-ant-`, is shown **only once**
at creation.

**Using it.** The official software kits read the variable **`ANTHROPIC_API_KEY`** automatically. Anthropic's
new command-line tool also offers a browser login (`ant auth login`); if the environment variable is set,
the variable wins over the login. One trap: if a key is not tied to a single workspace, **every request
must also name the workspace** in a header called `anthropic-workspace-id`, otherwise the API answers with
a 400 error. Creating the key for one specific workspace avoids that.

**Subscription versus API.** Confirmed by Anthropic (support article, 19 August 2026): a Claude Pro or Max
plan covers the Claude apps and Claude Code within shared usage limits; **API use is separate, needs
Console credentials, and is charged at standard API rates.** Claude Code can be set to continue on API
credits when a plan's limit is reached, but only if you choose that. How you buy API credits and the
minimum amount are not covered in the pages we read; check the Console's billing page.

**Check that your key works.** `curl https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY"
-H "anthropic-version: 2023-06-01"` should list models; a 401 means the key is wrong or expired (the
models-list request is general knowledge; the two headers are confirmed by Anthropic's pages).

**Look up, do not memorize:** current models at https://platform.claude.com/docs/en/models/overview and the
authentication options at https://platform.claude.com/docs/en/manage-claude/authentication. (The docs
moved from docs.anthropic.com to platform.claude.com.)

## 5. Meta

Meta is the case that shows why this page is short: **the product itself was replaced in the summer of
2026.** Older tutorials (and most AI assistants' memory) describe a hosted "Llama API" at
llama.developer.meta.com and api.llama.com. According to several secondary sources, that hosted service
was shut down on **6 July 2026**, and requests to it now return a "sunset" answer. We could not find an
official shutdown notice to quote; Meta's developer site now redirects visitors to a different address
(https://dev.meta.ai).

**What exists today.**

1. **The Meta Model API.** Meta's own page (https://dev.meta.ai) describes "direct, self-serve" access to
   its **Muse Spark** family of models and to a few image, speech and vision models, and says it is
   compatible with the OpenAI software kit. "Compatible with the OpenAI SDK" means you can use OpenAI's
   own client library and simply point it at Meta's web address instead (secondary sources give that
   address as `api.meta.ai`). You get in through a **Start building** button and a login; the page does not
   state prices, a free tier, or a waiting list, and secondary sources describe it as a public preview that
   opened on 9 July 2026. Because it is a preview, expect it to change.
2. **The open model files.** The older Llama models are still downloadable from Hugging Face under Meta's
   community licence (a licence with conditions; read it before commercial use), so you can run them on
   your own computer or rent them from a third-party hosting company. Those hosts change their offerings
   too: one secondary source reports that a host Meta had recommended dropped the relevant models within
   weeks.

**What it is not.** The **Meta AI** chat app and website are consumer products; like the others they are not
API access.

**Our advice.** Do not build a new program around Meta's hosted API until its pricing and terms are
published, and never hard-code its web address or model names. If a program needs a Meta model today, the
safer route is to run an open model locally or through a host you already trust, behind a setting that
names the model.

**Look up, do not memorize:** https://dev.meta.ai for the current Meta Model API; the Llama GitHub
repository, linked from that page, for the open models.

## 6. When this page is wrong

It will be. The check takes five minutes: open the "look up" page named in the provider's section, compare
its key-creation steps with what is written here, and correct this page. Please change the date at the top
when you do. Anything marked "general knowledge" or "secondary source" above is the first thing to
re-check.

## 7. Where this information comes from

All pages were read on 7 October 2026.

- Anthropic: Get started with Claude (https://platform.claude.com/docs/en/get-started), Get your Claude API
  key (https://platform.claude.com/docs/en/get-api-key), Authentication
  (https://platform.claude.com/docs/en/manage-claude/authentication), and the support article "Use Claude
  Code with your Pro or Max plan", dated 19 August 2026 (https://support.claude.com/en/articles/11145838).
  None of these pages shows its own date except the support article.
- OpenAI: API quick-start (https://developers.openai.com/api/docs/quickstart, no date shown) and
  Production best practices (https://developers.openai.com/api/docs/guides/production-best-practices, no
  date shown). OpenAI's help-center pages on prepaid billing could not be fetched (access refused); the
  billing details come from a search summary of them and from community forum posts.
- Meta: https://dev.meta.ai (no date shown). The shutdown date of the Llama API and the Meta Model API
  preview date come from secondary sources: the Spheron blog post "Meta shut down the Llama API", and
  summaries in Towards AI, Ecorpit and AIWiki.

## 8. Open questions

1. Meta: is there an official notice of the Llama API shutdown and of the Meta Model API's price and terms?
2. OpenAI: confirm the prepaid-billing amounts and card rules from OpenAI's own help center.
3. Anthropic: how are API credits bought, and what is the minimum amount?
4. Whether a chat subscription is separate from the API at OpenAI and Meta exactly as it is at Anthropic
   (we believe so; only Anthropic's statement was read).
