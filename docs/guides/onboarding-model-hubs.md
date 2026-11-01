---
title: "Onboarding: model hubs (Hugging Face and Civitai)"
category: guide
status: review
audience: mcp-dev, end-users
last_updated: 2026-10-07
last_verified: 2026-10-07
review_every_days: 30
sources:
  - https://huggingface.co/docs/hub/security-tokens
  - https://huggingface.co/docs/hub/models-gated
  - https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables
  - https://huggingface.co/docs/huggingface_hub/guides/cli
  - https://developer.civitai.com/site/guide/getting-started
  - https://developer.civitai.com/orchestration/guide/authentication
# status: review -- written 2026-10-07 from the sites' own documentation where it could be read.
# The Civitai domain split comes from secondary sources and is labelled as such.
---
# Getting access to model hubs: Hugging Face and Civitai

A **model hub** is a website that hosts downloadable AI models (the large files of learned numbers,
usually called *weights*) together with descriptions, licences and sometimes sample images. Many programs
in this collection download a model from a hub the first time they run: speech recognition, document
reading, image generation and local chat models all do. A search of our repositories found about two dozen
that mention Hugging Face, including a dedicated one (`huggingface-mcp`), and a handful that mention
Civitai, including a dedicated one (`civitai-mcp`).

Often you need no account at all, because many models are public. This guide explains when you *do* need
one, how to get the credentials, and the traps. The matching guides for other services are listed in
[onboarding-ai-providers.md](onboarding-ai-providers.md). Names of models and products are deliberately
left out here; see [ai-names-explained.md](ai-names-explained.md) for the dated snapshot of those.

## Part 1. Hugging Face

### 1.1 When you need an account and a token

Public models can be downloaded without signing in. You need an account, and a program needs a *token*
(a secret string that proves who you are), in three situations: the model is **private**, the model is
**gated** (explained below), or you want to **upload** something. A token is also useful against rate limits,
because signed-in requests are treated more generously (general knowledge, not checked today).

### 1.2 Tokens: three kinds, and which to choose

Create tokens in your account settings on the **Access Tokens** tab
(https://huggingface.co/settings/tokens) with the **New token** button. You choose a role and a name. Hugging
Face's documentation describes three roles:

- A **read** token can only read repositories you could read yourself, public or private. Use it to download
  models.
- A **write** token can also change repositories you have write access to. Use it only when a program must
  upload, for example when training and publishing a model.
- A **fine-grained** token is limited to specific resources, for example one model or one organization. This
  is the safest kind and the one Hugging Face recommends for anything in production, because if it leaks
  the damage is limited.

Hugging Face's own advice is to create **one token per application or use**, such as one for your laptop and
another for a notebook, so that you can cancel one without breaking the others. If a token leaks, delete or
refresh it on the same settings page. Organizations on paid plans can require administrator approval for
tokens or allow only fine-grained ones; a token that is rejected for that reason answers with a 403 error.

### 1.3 Gated models: what they are and how you get in

A **gated** model is one whose author has switched on *access requests*: before you may download the files you
must agree to share your username and email address with the author, and sometimes answer extra questions or
accept a licence. Gating is common for early research releases and for models with special licences. Some
facts that surprise people:

- **You request access in a web browser, while signed in.** It cannot be done from a script. On the model's
  page you click the button to agree and send the request.
- **Approval can be instant or manual.** With automatic approval you get access immediately. With manual
  approval an author reviews each request, which can take days.
- **Access belongs to you personally**, not to your organization.
- **The author keeps control.** Hugging Face states that authors "can decide at any time to block your access
  to the model without prior notice", even after approving you. A rejected request cannot be repeated.
- **Some gated models exclude the European Union**, decided by your internet address.
- **Your program then needs a token** belonging to the account that has access. Without it the download
  fails with an access error even though the model page opens fine in your browser.

### 1.4 Signing in on your computer

Hugging Face's command-line tool is now called **`hf`**, not `huggingface-cli` as in older tutorials. A
command-line tool, or CLI, is a program you use by typing commands. Install it with the one-line installer
from the documentation, with `pip install -U huggingface_hub`, or run it on demand with `uvx hf`. Then:

- `hf auth login` opens your browser to sign in, or lets you paste a token. The token is saved in a file under
  `.cache\huggingface` in your user folder.
- `hf auth whoami` shows which account and organizations the computer is signed in as. Use it to check a
  setup.
- `hf auth logout` deletes the stored tokens (it does not affect a token set through the environment).

A program can instead receive the token through the **environment variable `HF_TOKEN`**. An environment
variable is a named setting of your computer that programs can read. If it is set, it overrides the token
stored on the machine. The older name `HUGGING_FACE_HUB_TOKEN` is deprecated. Hugging Face's libraries read
these variables when they start, so a change made afterwards has no effect until the program restarts.

The documentation does not say that the stored token file is encrypted, so treat it like the plain secret it
is. For programs of ours that need a token, the safest design is to ask for it once, store it with the same
care as the other secrets in this collection, and hand it to the library through `HF_TOKEN`.

### 1.5 Where the downloads go (the cache)

Downloaded models are kept in a **cache** folder so that they are fetched only once. By default it is
`.cache\huggingface` in your user folder, and models are under its `hub` subfolder. Models are large, so
move the cache to a bigger drive if the system drive is small. Two variables control this: `HF_HOME`
(the base folder, which also holds the token) and `HF_HUB_CACHE` (only the model files; defaults to
`HF_HOME\hub`).

**A Windows detail.** The cache saves space by using *symbolic links* (shortcut-like entries). Windows only
allows ordinary programs to create them if **Developer Mode** is switched on (or the program runs as
administrator). Without it everything still works, but large files may be stored twice, and Hugging Face prints
a warning. You can silence it with `HF_HUB_DISABLE_SYMLINKS_WARNING=1`, or switch Developer Mode on in
Windows settings. A cache on a shared network drive used by different operating systems can fail on links; set
`HF_HUB_DISABLE_SYMLINKS=1` there.

### 1.6 Useful switches

- `HF_HUB_OFFLINE=1` stops the library from contacting the Hub at all; only already-cached files are used, and
  it also speeds up loading, since it skips the check for newer versions. If a file is not cached you get an
  error.
- `HF_HUB_DISABLE_TELEMETRY=1` (or the general `DO_NOT_TRACK=1`) turns off the usage statistics that
  Hugging Face's libraries send.
- `HF_HUB_DOWNLOAD_TIMEOUT` (default 10 seconds) can be raised on slow connections.
- Downloads now use a storage system called **Xet**, which is automatic. An older speed-up switch,
  `HF_HUB_ENABLE_HF_TRANSFER`, is deprecated and no longer works; the replacement for faster transfers is
  `HF_XET_HIGH_PERFORMANCE`.

### 1.7 When something goes wrong

- **"Cannot access gated repo" or a 401 or 403 error on a download.** You have not been granted access, or the
  program has no token, or the token belongs to a different account. Check the model page in the browser while
  signed in, then run `hf auth whoami` on the computer.
- **A 403 on an organization's models with a token that works elsewhere.** The organization may allow only
  fine-grained tokens, or your token may still await administrator approval.
- **A model loads online but not offline.** It was never fully cached; run once online.
- **Disk full.** Check the size of the cache and move it with `HF_HOME`.
- **Token exposed by accident.** Delete or refresh it at once on the Access Tokens page. Hugging Face also lets
  anyone report a token they find, and it is then invalidated and the owner is emailed.

### 1.8 Look up, do not memorize

Hugging Face's documentation at https://huggingface.co/docs/hub and https://huggingface.co/docs/huggingface_hub.
Rate limits and the paid plans change; neither is covered here.

## Part 2. Civitai

### 2.1 What it is and why it is different

Civitai is a community site for **image-generation models and add-ons** (checkpoints and the small "LoRA"
add-ons that adjust a style or subject). Programs such as civitai-mcp, invokeai-mcp and comfyops-mcp use it
to search and download them. Unlike Hugging Face, Civitai has no stable account tiers to document: **its rules
about content, regions and payments have changed repeatedly in 2025 and 2026**, so this section stays short.

### 2.2 Getting an API key (Civitai's documentation)

1. Sign in at https://civitai.com (create a free account first if needed).
2. Open **Account settings**, scroll to the **API Keys** section and click **Add API key**.
3. Give the key a name and copy the token. **It is shown only once.** Treat it like a password.
4. A program sends it in an HTTP header, which is a labelled extra line in a web request, written
   `Authorization: Bearer <token>`.

Some of the public endpoints work without a key; others need one so that Civitai knows who is asking. Civitai's
page does not say whether model downloads in particular require a key; in practice many do, so expect to
supply one (not checked today).

### 2.3 Two different interfaces

Civitai has the **public models interface** (searching and downloading models) and a separate
**orchestration interface** (running image generation on Civitai's computers), at
`orchestration.civitai.com`. Both use the same kind of key. The orchestration page of the documentation is
marked as an unfinished stub (token scopes, rate limits and rotation rules are "to be expanded"), so do not
build on it yet.

### 2.4 The two websites (reported, not from Civitai's documentation)

According to news and community sources, Civitai **split in April 2026 into two websites**: **civitai.com**, the
version suitable for the general public and for ordinary payment providers, and **civitai.red**, which can show
the broader catalogue including adult content and requires an 18-plus setting to be switched on in the account.
The same account, models and stats are reported to work on both, and the programming interface is reported to
stay on civitai.com and be reachable through civitai.red as well. Civitai's own developer pages that we read
mention only civitai.com. Memberships and payment options differ between the two. Because all of this is
second-hand and changes quickly, a program should never hard-code either domain, and anyone relying on adult
content should read the current terms of service on the site itself.

### 2.5 Look up, do not memorize

https://developer.civitai.com for the interface; the site's own terms of service for content rules.

## Where this information comes from

All pages were read on 7 October 2026. None of the Hugging Face pages showed a date.

- Hugging Face: User access tokens (https://huggingface.co/docs/hub/security-tokens); Gated models
  (https://huggingface.co/docs/hub/models-gated); environment variables of the `huggingface_hub` library
  (https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables); the command-line
  tool (https://huggingface.co/docs/huggingface_hub/guides/cli).
- Civitai: Getting started (https://developer.civitai.com/site/guide/getting-started) and the
  orchestration authentication page (https://developer.civitai.com/orchestration/guide/authentication), neither
  with a date. The domain split comes from secondary sources: Kombitz (12 April 2026), AI IDE List, and
  summaries of Civitai's own announcements.
- The "about two dozen repositories" figure is from a text search of the local repositories on 7 October 2026,
  excluding vendored copies.

## Open questions

1. Hugging Face: rate limits for signed-in versus anonymous downloads, and the current paid plans.
2. Civitai: whether model downloads need a key, the official statement on the two domains, and the final rules
   for the orchestration interface.
3. Whether our programs handle a missing or rejected token with a clear message instead of a stack trace.
