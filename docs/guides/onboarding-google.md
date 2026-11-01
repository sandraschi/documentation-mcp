---
title: "Onboarding: Google (your Docs and Drive, Gemini keys, and the Agent Platform formerly called Vertex AI)"
category: guide
status: review
audience: mcp-dev, end-users
last_updated: 2026-10-07
last_verified: 2026-10-07
review_every_days: 30
sources:
  - https://developers.google.com/workspace/guides/configure-oauth-consent
  - https://developers.google.com/workspace/guides/create-credentials
  - https://developers.google.com/workspace/guides/enable-apis
  - https://developers.google.com/identity/protocols/oauth2
  - https://developers.google.com/identity/protocols/oauth2/native-app
  - https://developers.googleblog.com/en/usability-and-safety-updates-to-google-auth-platform/
  - https://support.google.com/cloud/answer/15549945
  - https://developers.google.com/workspace/drive/api/guides/api-specific-auth
  - https://developers.google.com/workspace/docs/api/auth
  - https://ai.google.dev/gemini-api/docs/api-key
  - https://ai.google.dev/gemini-api/docs/billing
  - https://ai.google.dev/gemini-api/docs/migrate-to-cloud
  - https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment
  - https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/authentication
  - https://developers.google.com/program/plans-and-pricing
# status: review -- written 2026-10-07 from Google's own documentation (see "Where this
# information comes from"). It has NOT yet been followed end to end on a fresh Google account;
# the open questions are listed at the bottom.
---
# Setting up Google access

This guide explains, in plain language, how to give programs in this collection access to Google
services. It exists because Google changed its web console and its key system in 2025 and 2026,
renamed one of its products, and offers **three quite different ways to obtain a credential** that
look similar and are easy to mix up. Most older tutorials, and most of what an AI assistant
remembers, describe the old screens.

Two programs use it today: **google-docs-mcp** (reads and edits your own Google Docs and Drive
files) and **google-ai-mcp** (uses Google's Gemini models for chat, images, speech, music and video).
The matching guide for Microsoft is [onboarding-microsoft.md](onboarding-microsoft.md).

## 1. Which of the three paths do you need?

Read this section first. It decides everything else.

**Path A: you want a program to read or edit your own Google Docs and your own Drive files.**
You need an *OAuth client of type Desktop app*, and then you sign in once with your Google account in
your web browser. This is what google-docs-mcp uses. It is the longest path, because Google's console
makes you describe your "app" before it will give you the credential.

**Path B: you want a program to talk to Google's Gemini artificial intelligence models for chat,
images, speech or text embeddings.** You need a *Gemini API key* from a website called Google AI Studio.
This is the short path. google-ai-mcp uses it for chat, images, speech and embeddings, through the
environment variable `GOOGLE_API_KEY`.

**Path C: you want a program to generate video with Veo or music with Lyria.** You need a *Google Cloud
project* on the platform that used to be called Vertex AI and is now called the Gemini Enterprise Agent
Platform, plus credentials for it. google-ai-mcp uses this for video and music, through the environment
variable `GOOGLE_CLOUD_PROJECT`. If neither credential is present, google-ai-mcp does not fail: it runs
in a clearly labelled mock mode that returns made-up sample answers.

These paths are independent. A key from path B cannot read your Docs, and an OAuth client from path A
cannot call Gemini.

## 2. Words you will meet (a short glossary)

Please read this once. The rest of the guide uses these words without repeating the explanation.

- **Google Cloud project.** A named folder inside Google Cloud that holds settings, switched-on
  services, credentials and billing. Everything below happens inside one project.
- **API** (application programming interface). The way a program talks to a service. "Enabling the
  Google Docs API" means switching on that service for your project.
- **Console.** Google's web page for managing a Google Cloud project, at console.cloud.google.com.
- **OAuth** (pronounced "oh-auth"). An industry standard that lets a program act on your behalf
  without ever learning your password. You sign in on Google's own page and Google hands the program
  a limited-permission token.
- **OAuth client.** The credential that identifies a program to Google during an OAuth sign-in. It
  consists of a **client ID** (a public identification string) and usually a **client secret**.
  "Desktop app" is the client type for programs that run on your own computer.
- **Google Auth platform.** The part of the console where you describe your app and create OAuth
  clients. It replaced the older "OAuth consent screen" page.
- **Audience.** The setting that says who may sign in to your app: **External** means any Google
  account holder (what a private individual needs), **Internal** means only members of your
  organization's Google Workspace.
- **Scope.** A named piece of access, for example "see and edit your Google Docs". Scopes are graded
  as non-sensitive, sensitive or restricted, and the grade decides how much review Google demands
  before the general public may use your app.
- **Consent screen.** The page, shown during your first sign-in, that lists the scopes and asks you to
  click Allow.
- **Access token and refresh token.** The access token is short-lived proof that you signed in. The
  refresh token lets the program obtain new access tokens without asking you again.
- **Loopback address.** An address that points back to your own computer, such as `http://127.0.0.1`
  or `http://localhost`. During sign-in Google sends your browser to such an address so that the
  program on your computer receives the result.
- **API key.** A single string that identifies your *project* to a service. It does not identify a
  person, so it cannot be used to read someone's private documents.
- **AI Studio.** A Google website (aistudio.google.com) where individuals create Gemini API keys.
- **Billing account.** A payment method attached to a project. Needed for anything beyond the free
  limits.
- **gcloud.** Google's command-line tool for Cloud, installed on your computer. A "CLI" is a
  command line interface: a program you type commands into.
- **Application Default Credentials**, abbreviated **ADC**. A convention in Google's software kits
  (called SDKs, short for software development kits) where a program automatically finds your
  credentials. For local development you create them with one command, `gcloud auth
  application-default login`.
- **Service account.** A robot identity belonging to a project rather than to a person.
- **Quota project.** The project that is charged and rate-limited when your own user credentials call
  a service.
- **IAM** (Identity and Access Management). Google Cloud's system of roles that decide who may do what
  in a project.
- **PKCE** (proof key for code exchange, pronounced "pixie"). An extra safeguard for sign-in
  programs that run on your own computer.
- **OOB** (out of band). The old sign-in style in which Google showed a code that you copied and
  pasted into a program. Google has switched it off.

## 3. Things people confuse (each of these has cost someone an afternoon)

**"I pay for Google AI Pro, so I already have API access."** You do not. The app subscription is not
an API key. What the subscriptions do include is a monthly allowance of developer credit: ten dollars
for AI Pro, forty dollars for AI Ultra with 20 terabytes, and one hundred dollars for AI Ultra with 30
terabytes. Google's page says the credit applies "in AI Studio, Gemini Enterprise Agent Platform or any
Google product". You still have to create a key or a project yourself, and the page does not say how
to activate the credit; that is an open question below.

**"An API key can read my Docs."** It cannot. Google's own wording is that a standard key "associates
requests with a Google Cloud project for billing and quota purposes" and "doesn't identify a caller".
Your private documents require OAuth, which is path A.

**"My AI Studio key and my Cloud Console key are the same thing."** Both belong to a Google Cloud
project, but since 28 May 2026 new AI Studio keys are a different kind of key (section 6).

**"Which environment variable do I use, `GEMINI_API_KEY` or `GOOGLE_API_KEY`?"** Google's software
kits read both. If both are set, `GOOGLE_API_KEY` wins. google-ai-mcp reads `GOOGLE_API_KEY`.

**"Vertex AI."** Google announced on 22 April 2026, at its Cloud Next conference, that Vertex AI is
now part of the **Gemini Enterprise Agent Platform**. That announcement date comes from news reports
rather than from Google's documentation; Google's documentation now uses both names side by side.

**"Which OAuth client type?"** It must be **Desktop app**. A client created as "Web application"
produces a "redirect URI mismatch" error with google-docs-mcp, because the program signs in through
your own computer, not through a public website.

**"Can a service account read my Docs?"** Not by default. A service account is a separate robot
identity with its own empty Drive, so it can only see documents that you explicitly share with its
email address. That is not how google-docs-mcp works, and we have not tested it.

**"Internal or External?"** Internal only works for people inside one Google Workspace organization;
anyone else is turned away with the error `org_internal`. A private person with a normal Gmail
address must choose **External**.

## 4. What it costs

- **Path A (Docs and Drive).** Free at personal volumes, and no credit card is needed to create the
  OAuth client. The google-docs-mcp documentation says the same.
- **Path B (Gemini key).** There is a **free tier**: access to certain models up to their free rate
  limits, with no billing account required. To go beyond it you link a Cloud Billing account. New
  users must prepay at least five dollars in credits; that prepaid model has been the default for new
  users since 23 March 2026. Spending caps depend on your payment history: 250 dollars a month at
  Tier 1, 2,000 dollars at Tier 2, and between 20,000 and 100,000 dollars or more at Tier 3. You can
  also set a cap per project. Google states that on paid usage "your prompts and responses are not used
  to improve Google products"; on the free tier you should read the data policy.
- **Path C (Agent Platform).** Needs a Google Cloud project and, in practice, a billing account,
  because video and music generation are billed usage. We have not confirmed this, and Google also
  offers an "express mode" for quick trials whose limits we could not read; see the open questions.

---

## 5. Path A in detail: reading and editing your Docs and Drive (google-docs-mcp)

### 5.1 The idea in one paragraph

You create a Google Cloud project and switch on two services, the Docs API and the Drive API. You then
tell Google about your "app" on the Google Auth platform pages, which only means entering a name and
an email address. You create an OAuth client of type Desktop app, and copy its client ID and client
secret into the program. The first time the program needs access it opens your browser, you sign in
and click Allow, and the program stores the resulting token.

### 5.2 The steps, using today's console wording

Older instructions mention "APIs and Services, then OAuth consent screen" and "Credentials, then Create
credentials". Those screens have been replaced. In the current console the relevant area is called
**Google Auth platform** and has four pages named **Branding**, **Audience**, **Data Access** and
**Clients** (Google's page, dated 3 September 2026).

1. **Create or choose a project.** Open https://console.cloud.google.com and create a project, or pick
   an existing one.
2. **Switch on the two services.** Open the menu, choose **APIs and Services**, then **Library**, then the
   **Google Workspace** category. Open **Google Docs API** and click **Enable**. Repeat for **Google
   Drive API**. (The same can be done from the command line with `gcloud services enable
   docs.googleapis.com drive.googleapis.com`; those two service names come from general knowledge and
   we have not re-checked them.)
3. **Describe your app.** Open the menu, choose **Google Auth platform**, then **Branding**. If the page
   says "Google Auth platform not configured yet", click **Get Started** and go through four short
   screens:
   1. *App information:* enter an app name and choose a user support email address, then click Next.
   2. *Audience:* choose **External** if you use an ordinary Gmail account, or Internal if you are
      inside a Workspace organization, then click Next.
   3. *Contact information:* enter an email address where Google may send project notices, then
      click Next.
   4. *Finish:* tick the box "I agree to the Google API Services: User Data Policy", then click
      **Continue** and **Create**.
4. **Add yourself as a test user.** Open **Audience**, find **Test users**, click **Add users**, enter
   your own Google address and click **Save**. A project in testing may have up to 100 test users.
5. **Choose the scopes.** Open **Data Access**, click **Add or Remove Scopes**, tick the scopes the
   program needs, and click **Save**. Section 5.3 explains which to pick.
6. **Create the OAuth client.** Open the menu, choose **Google Auth platform**, then **Clients**, click
   **Create Client**, set **Application type** to **Desktop app**, enter a **Name** (only you see it) and
   click **Create**. Desktop clients need no redirect address and no fingerprint.
7. **Save the client secret right now.** This is the step that surprises people. Google's
   announcement of 28 April 2025 says that since June 2025 the console masks client secrets: "Once
   the creation screen is closed, the client secret will not be shown again", and afterwards only the
   last few characters are visible. **Download the JSON file (a plain-text data format) offered on the creation screen** and store
   it safely. If you lose the secret you must create a new one with the console's secret rotation
   feature; Google's post does not describe the steps.
8. **Give the program the ID and secret.** google-docs-mcp reads them from the environment variables
   `GOOGLE_DOCS_MCP_CLIENT_ID` and `GOOGLE_DOCS_MCP_CLIENT_SECRET`, or from a file `data/oauth_client.json`.
9. **Sign in once.** Ask the program to run its `start_oauth` operation. Your browser opens Google's
   consent screen. You will probably see the warning "Google hasn't verified this app"; section 5.4
   explains why that is normal for your own app. Continue, click Allow, and the program writes your
   token to `data/token.json`. That file is plain text; see the security section.

### 5.3 Choosing scopes: take the narrowest one that works

Google grades every scope. The grade decides how much review would be needed to let the general
public use your app. From Google's Drive and Docs pages (both dated 3 September 2026):

- `drive.file` is **non-sensitive**: the program can only touch files it created or that you opened
  with it. Google's recommendation is "the most narrowly focused scope possible", and this is the
  scope it points to first.
- `documents` is **sensitive**: it lets the program see, edit, create and delete all your Google
  Docs. `documents.readonly` is the read-only version and is also sensitive.
- `drive` is **restricted**: all of your Drive files. Publishing an app to the general public with a
  restricted scope requires a special verification and possibly a security assessment. `drive.readonly`
  and `drive.metadata` are restricted as well.

google-docs-mcp currently asks for `documents` **and** `drive`, which is the most demanding combination.
For one person using their own client that is acceptable. It matters only if you ever want other people to
use your client. Narrowing it to `drive.file` would remove features such as browsing and backing up
arbitrary folders; we have not measured exactly which.

### 5.4 Testing mode, production mode, and why you get signed out after a week

Your project has a *publishing status*. It starts as **Testing**.

- In **Testing**, with the External audience, Google issues refresh tokens that **expire after seven
  days**, so you must sign in again weekly. (Google makes an exception when the app asks only for the
  name, email address and profile.) Only the people you listed as test users can sign in, and Google
  shows a warning screen before authorization.
- In **In production**, the app is open to any Google account. If it uses sensitive or restricted scopes
  and has not been verified, Google shows an "unverified app" warning and limits the app to **100 new
  users in total, for the whole lifetime of the project; the limit cannot be reset.** Verified apps are
  exempt.

For **one person using their own client** there are two sensible choices. You can stay in Testing and
accept the weekly re-login. Or you can press **Publish app** on the Audience page and live with the
unverified-app warning, clicking through "Advanced" and "continue to the app", because it is your own
app. We believe the seven-day expiry does not apply once the app is in production, because Google states the
rule only for Testing, but Google does not say so in as many words; it is an open question. Do not apply
for verification unless you plan to distribute the app to others.

Other rules about refresh tokens, from Google's page dated 26 May 2026: a refresh token that has not been
used for **six months** expires; each Google account may hold at most **100 refresh tokens per OAuth
client** (older ones are dropped); changing your password invalidates tokens that carry Gmail scopes; and
if a Workspace administrator restricts one of the services your app uses, the token stops working with the
error `admin_policy_enforced`.

A newer rule, from Google's announcement of 28 April 2025: **an OAuth client that has been inactive for
six months is deleted automatically.** You get a notice and can restore it within 30 days. If a program
stopped working after a long break, this may be the reason.

### 5.5 How the sign-in finds its way back to the program

From Google's page for programs on desktop computers, dated 14 September 2026: the supported method is
the **loopback address**, written `http://127.0.0.1:port` (or `http://[::1]:port` for the newer internet
address style), where the program briefly listens on a free port and Google sends your browser there. The
old copy-and-paste method (OOB) is "no longer supported", so tutorials that tell you to paste a code are
obsolete. The word `localhost` also works, but Google warns that it "may cause issues with client
firewalls", so the numeric form is preferred. PKCE is recommended but not required. A desktop client's
secret is not truly secret, because the program lives on your computer, but the console treats it as
confidential and so should you.

google-docs-mcp starts its local listener with the Google library's `run_local_server` function. Which
address form it uses has not been checked and is an open question below.

---

## 6. Path B in detail: a Gemini API key (google-ai-mcp: chat, images, speech, embeddings)

### 6.1 Getting a key

All of this comes from Google's page dated 6 October 2026.

1. Open https://aistudio.google.com/apikey (Google also links the key list at
   aistudio.google.com/api-keys) and accept the terms of service. **If you are a new user, Google creates
   a default project and a first key for you automatically.**
2. **If you already use Google Cloud**, AI Studio does not show your existing projects by default. Open
   **Dashboard**, then **Projects**, then **Import projects**, search for the project, import it, and then
   create the key on the **API Keys** page. Every key belongs to a project, and the project decides
   billing and quota.
3. Give the key to the program as the environment variable `GOOGLE_API_KEY`.

### 6.2 What changed in 2026 (read this if an old key stopped working)

- **7 May 2026.** The Gemini service started blocking *unrestricted* keys that had been dormant for a long
  time. AI Studio marks them with a **"Blocked"** label. The remedy is to create a new key or to restrict
  the old one so that it works only for the Gemini API.
- **28 May 2026.** All new keys created in AI Studio are **authorization keys** (Google calls them "auth
  keys"). An auth key is "bound directly to a Google Cloud service account", is **restricted to the Gemini
  API by default**, and gets faster enforcement if it leaks. For your program nothing changes: you pass it
  as the `api_key` setting, or as the `x-goog-api-key` web header, or through the environment variables
  `GEMINI_API_KEY` or `GOOGLE_API_KEY`, exactly as before.
- **Now.** A standard Cloud key with no restriction is rejected by the Gemini service. If you use such a
  key, restrict it to the Generative Language API (the Gemini API's technical name) in the console.

Treat the key like a password. Never commit it to version control and never put it in code that runs
in a web page. For production use, Google recommends storing it in its Secret Manager service and adding
restrictions by application or network address.

### 6.3 Free and paid use

The free tier needs no billing account. To pay for more, link a Cloud Billing account and prepay at
least five dollars. The tiers and spending caps are described in section 4 (Google's billing page, dated 28
September 2026).

---

## 7. Path C in detail: the Agent Platform project (video and music in google-ai-mcp)

google-ai-mcp uses a Google Cloud project for Veo 3.1 video and Lyria 3 music. It reads
`GOOGLE_CLOUD_PROJECT`, and `GOOGLE_CLOUD_LOCATION` (default `us-central1`), and some of its code
switches Google's software kit into the platform mode with a setting called `vertexai=True`.

### 7.1 When to use this instead of an AI Studio key

Google's own advice, from the page dated 30 September 2026, is: "Most developers should use the Gemini
Developer API unless there is a need for specific enterprise controls." Use the Agent Platform when a
feature exists only there, as with Veo and Lyria in this project, or when you need those enterprise
controls. The two services sign you in differently: the Developer API uses an API key, while the
Agent Platform uses Google Cloud credentials such as a service account or Application Default
Credentials.

### 7.2 How to authenticate

Google's documentation lists three options:

- **Application Default Credentials (ADC)**, the standard choice for working on your own computer. After
  installing the gcloud tool, run `gcloud auth application-default login`; a browser window asks you to
  sign in. (Google's page, dated 6 October 2026. The page does not say where on Windows the credentials
  file is written.)
- **An express-mode API key**, meant for quick prototypes. The console route starts at a "Start free"
  button and an "Express mode" section; we could not read the exact steps, and we do not know whether
  Veo and Lyria work with it. Both are open questions.
- **A service account key file**, for servers and automated jobs. You point the environment variable
  `GOOGLE_APPLICATION_CREDENTIALS` at the file.

Google's software kits honour these environment variables: `GOOGLE_APPLICATION_CREDENTIALS`,
`GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION` and `GOOGLE_GENAI_USE_VERTEXAI`. In Python the kit is
called google-genai. The classic way to select the platform is `genai.Client(vertexai=True,
project="...", location="us-central1")`. Newer documentation also shows `genai.Client(enterprise=True,
project="...", location="global")`, and says the newer "Interactions API" supports only the `global`
location during its preview.

### 7.3 A typical setup on your own computer

Google's setup page could not be read in full, so the commands below are the standard ones from general
Google Cloud practice and are marked where we have not re-checked them.

1. Create or choose a project and attach a billing account to it.
2. Switch on the service: `gcloud services enable aiplatform.googleapis.com` (the service name is from
   general knowledge).
3. Run `gcloud auth application-default login`. This one is confirmed by Google's page.
4. If a call fails with "no quota project available" or "the API is not enabled", that is a known
   limitation: Google says ADC with a user account "might not work for some APIs without extra
   configuration". The usual remedy is `gcloud auth application-default set-quota-project PROJECT_ID`
   (the command is from general knowledge; Google's page only points to a troubleshooting article).
5. Your account needs permission to call the service. The usual role is "Vertex AI User",
   `roles/aiplatform.user` (from general knowledge; the role may have been renamed with the platform).
6. Set `GOOGLE_CLOUD_PROJECT` (and `GOOGLE_CLOUD_LOCATION`) for google-ai-mcp.

---

## 8. When something goes wrong

Each entry says what you see, what it usually means, and what to do. "Confirmed" means we checked it
against Google's documentation; "from our code" means it is how our programs behave; "unchecked" means it
is general knowledge.

- **"Google hasn't verified this app."** This is normal for your own unverified OAuth client. Click
  Advanced and continue to the app. Only an app that you distribute to other people needs verification.
  (Confirmed.)
- **`redirect_uri_mismatch`.** The OAuth client was created as a Web application. Delete it and create a
  Desktop app client. (From our code and notes.)
- **You must sign in again after about a week.** Your project is in Testing, where refresh tokens last seven
  days. See section 5.4. (Confirmed.)
- **`invalid_grant` after months away.** The token was unused for six months, or the whole OAuth client was
  deleted for inactivity (restorable within 30 days). Sign in again, or recreate the client. (Confirmed.)
- **`org_internal`.** The audience is Internal but you are not in that organization. Change the audience to
  External. (Confirmed.)
- **`admin_policy_enforced`.** A Workspace administrator restricted a service your app uses. Ask the
  administrator. (Confirmed.)
- **"Access blocked" for a particular account.** That account is not on the Test users list. Add it on the
  Audience page. (Confirmed.)
- **A 403 error saying an API "has not been used in project" or "access not configured".** The Docs or Drive
  API is not switched on in that project. Enable it (section 5.2, step 2). (Unchecked.)
- **An AI Studio key shows "Blocked", or requests are rejected.** The key is unrestricted or dormant. See
  section 6.2. (Confirmed.)
- **Application Default Credentials work for some calls but you see "no quota project".** Set a quota project
  (section 7.3, step 4). (Confirmed that the limitation exists; the command is from general knowledge.)
- **google-ai-mcp reports "not configured" for video or music.** `GOOGLE_CLOUD_PROJECT` is not set. See
  section 7. (From our code.)
- **HTTP error 429 ("too many requests").** You hit the free tier's rate limit. Wait, or move to a paid tier
  (section 4). (Confirmed.)

## 9. Security in plain words

API keys and OAuth client secrets are credentials. Never commit them to version control, never paste them
into screenshots or chat messages, and never put them in code that is delivered to a web browser. Every
repository in this collection ignores `.env` files for that reason. In google-docs-mcp the token file
`data/token.json` is stored as plain text, with the same trust level as the Claude Desktop configuration
file; the project that stores tokens encrypted on Windows, onenote-mcp, shows how this could be improved
here (we propose it; nothing has been changed). Choose the narrowest scope that does the job. Do not share
one OAuth client between several people: the hundred-user limit for unverified apps and the verification
requirements make that a trap.

## 10. Observations about our own repositories (nothing has been changed yet)

- The existing `docs/ONBOARDING.md` of google-docs-mcp still uses the **pre-2025 console wording** ("OAuth
  consent screen", "Credentials, then Create credentials"). Its paragraph about the seven-day limit and about
  publishing to production is also muddled. It should be rewritten against section 5 of this guide.
- google-docs-mcp requests the restricted `drive` scope. The trade-off against `drive.file` deserves a
  paragraph in its documentation.
- google-ai-mcp has an **empty `docs/` folder**. Its `AGENTS.md` mentions only `GOOGLE_API_KEY` and
  `GOOGLE_CLOUD_PROJECT`. It needs a short `docs/ONBOARDING.md` that states the A, B and C split and links
  here.
- The sign-in listener in google-docs-mcp should preferably use `127.0.0.1` rather than `localhost`
  (section 5.5); this has not been checked in the code.

## 11. Ideas for the weekend: making Google onboarding easier

The console clicks cannot be automated away, but a person can be walked through them with the exact labels
used above. Possible improvements: an in-app checklist like the one in onenote-mcp ("1. create a project
and enable the two APIs, 2. fill in the Google Auth platform pages, 3. create a Desktop client, 4. paste the
ID and secret, 5. sign in") with copy buttons and links; a form field that explains "this secret is shown
only once, download the JSON now"; a banner that explains the seven-day Testing expiry and shows how to
publish the app; and a friendly "please sign in again" message when Google answers `invalid_grant`, rather
than a raw error. The `gcloud` tool can probably create a project and switch on APIs, but we believe it has
no first-class command for creating the consent configuration or the Desktop OAuth client; that belief is
unchecked.

## 12. Where this information comes from

All pages were read on 7 October 2026. The date shown is the date printed on the page, when it has one.

- Configure the OAuth consent (Google Auth platform), 3 September 2026:
  https://developers.google.com/workspace/guides/configure-oauth-consent
- Create credentials (Desktop client), shown with September 2026 pages:
  https://developers.google.com/workspace/guides/create-credentials
- Enable Google Workspace APIs, 3 September 2026:
  https://developers.google.com/workspace/guides/enable-apis
- OAuth 2.0 overview, token expiry rules, 26 May 2026:
  https://developers.google.com/identity/protocols/oauth2
- OAuth 2.0 for desktop apps, 14 September 2026:
  https://developers.google.com/identity/protocols/oauth2/native-app
- Google Developers Blog, "Usability and safety updates to Google Auth Platform", 28 April 2025:
  https://developers.googleblog.com/en/usability-and-safety-updates-to-google-auth-platform/
- Manage app audience (testing and production, user cap), no date shown:
  https://support.google.com/cloud/answer/15549945
- Drive scopes, 3 September 2026: https://developers.google.com/workspace/drive/api/guides/api-specific-auth
- Docs scopes, 3 September 2026: https://developers.google.com/workspace/docs/api/auth
- Gemini API keys, 6 October 2026: https://ai.google.dev/gemini-api/docs/api-key
- Gemini API billing, 28 September 2026: https://ai.google.dev/gemini-api/docs/billing
- Gemini Developer API compared with the Agent Platform, 30 September 2026:
  https://ai.google.dev/gemini-api/docs/migrate-to-cloud
- Application Default Credentials for local development, 6 October 2026:
  https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment
- Authentication options for the Agent Platform, formerly Vertex AI (no date shown; the page moved from the old Vertex AI address when the product was renamed):
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/machine-learning/authentication
- Google Developer Program credits for AI Pro and Ultra (no date shown):
  https://developers.google.com/program/plans-and-pricing
- News coverage of the 22 April 2026 rename (secondary sources): HPCwire, The Journal, Campus Technology.

## 13. Open questions for the first hands-on walkthrough

These could not be settled by reading and should be answered by someone following the guide on a fresh
Google account, with screenshots.

1. Walk through path A in the live console and capture every page.
2. Express mode: how is the key created, what are the free limits, and do Veo and Lyria work with it?
3. Agent Platform: confirm the service name, the required role, the quota-project command, and where
   Windows stores the ADC file.
4. How are the AI Pro and Ultra developer credits activated?
5. Does an unverified app in production keep refresh tokens beyond seven days?
6. Does google-docs-mcp's sign-in listener use `localhost` or `127.0.0.1`?
