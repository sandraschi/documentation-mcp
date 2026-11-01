---
title: "Onboarding: Microsoft (your own app registration, sign-in, OneNote)"
category: guide
status: review
audience: mcp-dev, end-users
last_updated: 2026-10-07
last_verified: 2026-10-07
review_every_days: 30
sources:
  - https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app
  - https://learn.microsoft.com/en-us/graph/auth-register-app-v2
  - https://learn.microsoft.com/en-us/entra/identity-platform/reply-url
  - https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview
  - https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account
# status: review -- written 2026-10-07 from Microsoft's own documentation (see "Where this
# information comes from"). It has NOT yet been followed end to end on a fresh account; the
# open questions are listed at the bottom.
---
# Setting up Microsoft access (for OneNote and other Microsoft services)

This guide explains, in plain language, everything you have to do once so that a program on your
computer can read and write your OneNote notebooks. The program that needs it today is
**onenote-mcp**. The same steps apply to any other tool in this collection that signs you in to a
Microsoft service on your own behalf, for example Outlook mail or OneDrive files. The matching
guide for Google is [onboarding-google.md](onboarding-google.md).

You do not need to be a developer to follow this guide. You do need about ten minutes, a web
browser, and a Microsoft account.

## 1. Why you have to do this yourself

Microsoft does not let a program sign a person in unless the program has been **registered**
with Microsoft first. Registering means filling in a short form in Microsoft's web portal, and the
result is a record that says "an application with this name and this identification number exists,
and it is allowed to ask people to sign in."

In this collection every person registers their own application. There are two reasons. First, the
number Microsoft hands back (the client ID, explained below) is tied to the person who created it, and
we do not want one shared number that thousands of people depend on. Second, there is no
usable shared alternative: the number that Microsoft's own "Graph Explorer" demonstration tool uses
looks like it works, but OneNote refuses the sign-in tokens it produces and answers with the error
code 40001. That is why onenote-mcp no longer ships with any built-in number.

Registering is free. The only awkward part is that Microsoft's portal sometimes wants you to have
an Azure account first, which asks for a credit card (see section 4).

## 2. Words you will meet (a short glossary)

Please read this once. The rest of the guide uses these words without repeating the explanation.

- **Microsoft account.** The email address and password you use for Outlook.com, Hotmail, Xbox or a
  work or school Microsoft 365 login. A *personal* Microsoft account ends in outlook.com,
  hotmail.com, live.com or similar. A *work or school* account belongs to an organization.
- **Entra ID** (pronounced "enter-uh"). Microsoft's identity service. It used to be called Azure
  Active Directory. It is the part of Microsoft that keeps the list of registered applications.
  The web page where you manage it is called the **Microsoft Entra admin center**.
- **Tenant**, also called a **directory**. A private container inside Entra ID that holds the users
  and registered applications of one person or organization. If you are an individual, Microsoft
  creates a tenant for you called "Default Directory".
- **App registration.** The record described in section 1. It lives inside your tenant. Once it is
  created it cannot be moved to a different tenant.
- **Application (client) ID.** A long identification number made of letters and digits in the
  pattern `12345678-abcd-1234-abcd-1234567890ab`. Technically this kind of number is called a GUID
  (globally unique identifier). It tells Microsoft which registered application is asking. It is
  not a password: this kind of application has no secret, and a person still has to sign in. We
  nevertheless keep it private and store it encrypted.
- **Public client.** An application that runs on the user's own computer and therefore cannot keep a
  secret. Microsoft handles it differently from a web service. onenote-mcp is a public client, which
  is why you must never create a "client secret" for it.
- **Supported account types.** The setting that says who may sign in to your application: only
  people with personal Microsoft accounts, only people from organizations, or both.
- **Authority.** The Microsoft web address the application sends people to for signing in. The
  address ends in `consumers`, `organizations` or `common` depending on the supported account
  types. The application picks it for you from the account type you choose in its settings.
- **Redirect address** (Microsoft also calls it a "redirect URI" or "reply URL"; URI is short for
  uniform resource identifier, which means a web address). After you have signed in, Microsoft sends
  your browser back to this address so the program learns that sign-in succeeded. For a program on
  your own computer, this address points at your own computer and begins with `http://localhost`.
- **Permission**, also called a **scope**. A named piece of access, for example "read my OneNote
  notebooks" (`Notes.Read`) or "read and change my OneNote notebooks" (`Notes.ReadWrite`).
- **Consent.** The moment, during your first sign-in, when Microsoft shows you the list of
  permissions and you click Accept.
- **Access token and refresh token.** After sign-in the program receives an access token, a short
  lived proof that you are signed in (about an hour). It also receives a refresh token, a longer
  lived item that lets it quietly obtain new access tokens without bothering you again.
- **Microsoft Graph** (usually just "Graph"). Microsoft's single web service that gives programs
  access to your Microsoft data, including OneNote.
- **DPAPI** (Data Protection API). A feature of Windows that encrypts data so that only your own
  Windows user account on this computer can read it. onenote-mcp uses it to store your tokens and
  your client ID.

## 3. The big picture in one story

You open the dashboard of onenote-mcp and paste in the Application (client) ID of the registration
you created. You click "Sign in". The program opens your web browser at a Microsoft address and
includes that ID, the permissions it wants, and the redirect address. You sign in with your Microsoft
account and click Accept. Microsoft sends the browser back to the redirect address on your own
computer, and the program receives a one-time code, exchanges it for the tokens described above,
and stores them encrypted. From then on the program can read and write your OneNote notebooks
until you revoke access or the refresh token expires from long disuse.

Everything you do in the Microsoft portal exists only to make that story possible.

## 4. What you need before you start, and what it costs

You need a Microsoft account. Registering an application costs no money.

There is one possible obstacle. Microsoft's own quick-start guide (page dated 14 May 2026) lists
"an Azure account that has an active subscription" as a prerequisite, and says you can create one
for free. Azure is Microsoft's cloud service. Creating even a *free* Azure account requires a phone
number and a credit or debit card that is not a prepaid card. Microsoft's FAQ explains that the card is used "for identity
verification to validate that account holders are real people and not bots", and that a one-dollar
temporary authorization charge may appear on the card and is then removed. You can sign up with a
Microsoft account or a GitHub account. If you do not later switch to pay-as-you-go pricing, Microsoft
says your Azure account and services will be disabled when the free period ends.

We do not yet know two things, and they are listed as open questions at the end of this guide.
First, whether a personal Microsoft account can reach the Entra admin center and register an
application *without* any Azure subscription. Some people report that it works and a "Default
Directory" appears on its own, but Microsoft's page still lists the subscription as a prerequisite.
The simple advice is: try https://entra.microsoft.com first, and only create a free Azure account if the
portal refuses you. Second, whether your registration keeps working after a free Azure account has
lapsed. Microsoft's pages do not say.

The role you need inside your tenant is "Application Developer" or higher. If you are using your own
personal directory you are its owner and already have it.

## 5. Choose the right "supported account type" first

When you register the application you must say who may sign in. Pick by looking at where your OneNote
notebooks live.

- If your notebooks are on a **personal** Microsoft account (stored on consumer OneDrive), choose the
  option for **personal Microsoft accounts only**. The application will then use the `consumers`
  sign-in address. This combination is strict: if the registration says "personal only" but the
  program sends people to the `common` address, Microsoft stops at the start of sign-in with the
  error code AADSTS9002346 (the letters are Microsoft's prefix for "Azure Active Directory Security
  Token Service" errors). onenote-mcp prevents this by asking you which account type you chose and
  choosing the address itself.
- If your notebooks are on a **work or school** account, choose the option for your organization
  only (called "single tenant"), or the option for any organization. The sign-in address is then
  `organizations`.
- If you use **both**, choose the option for any organization **plus** personal accounts. The sign-in
  address is then `common`. This is also the setting onenote-mcp assumes when you have not told it
  otherwise.

A warning about Microsoft's own advice: the quick-start guide recommends "Single tenant only" for most
applications. That is correct for a company's internal program and wrong for you if your OneNote is
a personal one. Do not follow that recommendation blindly.

## 6. Step by step: registering your application

The wording below comes from two Microsoft pages that were last updated in January and May 2026.
Microsoft's two pages describe the same menu with slightly different names, so where the names
differ both are given. Look for the entry with the closest meaning.

### 6.1 Open the Entra admin center

1. Open https://entra.microsoft.com in your web browser and sign in with your Microsoft account.
   (The older Azure portal at https://portal.azure.com reaches the same registration page. The
   in-app guide in onenote-mcp links to the Azure portal.)
2. If your account belongs to more than one directory, click the gear-shaped **Settings** icon in the
   top menu and choose the directory in which the registration should live. Individuals normally
   only have one.
3. In the left-hand menu open **App registrations**. In the quick-start guide the path is written
   "Entra ID, then App registrations". In the Graph guide it is written "Identity, then
   Applications, then App registrations". Click **New registration**.

### 6.2 Fill in the registration form

1. **Name.** Choose anything you will recognize, for example `onenote-mcp-local`. The name is shown to
   you on the permission screen later.
2. **Supported account types.** Choose according to section 5. The four choices are worded
   differently in Microsoft's two guides:

   - "Single tenant only" (quick-start) or "Accounts in this organizational directory only" (Graph
     guide): only people in your own organization.
   - "Multiple Entra ID tenants" or "Accounts in any organizational directory": people in any
     organization.
   - "Any Entra ID Tenant + Personal Microsoft accounts" or "Accounts in any organizational
     directory and personal Microsoft accounts": organizations and personal accounts.
   - "Personal accounts only" or "Personal Microsoft accounts": only personal accounts.
3. **Redirect URI (optional).** Leave this empty. Microsoft's Graph guide says to configure it in a
   separate step, which is section 6.3 below.
4. Click **Register**. Microsoft shows the **Overview** page of your new registration. Copy the
   **Application (client) ID** from that page. You do not need the "Object ID" and you do not need
   any secret.

### 6.3 Add the redirect address (the step people most often get wrong)

1. In the left-hand menu of your registration, under **Manage**, click **Authentication**.
2. Under **Platform configurations** click **Add a platform**.
3. Choose the tile named **Mobile and desktop applications**. This is the correct choice for a
   program that runs on your own computer and signs you in through the system web browser.
4. In the list of redirect addresses, add two custom addresses, then click **Configure**:
   - `http://localhost`. Microsoft recommends exactly this address for desktop programs that use the
     system browser.
   - `http://localhost/api/auth/callback`. This is the address, apart from the port number, that
     onenote-mcp actually sends. The reason for adding both is explained next.

Microsoft's rules for redirect addresses, from the page dated 14 May 2025 and updated June 2026, in
plain words:

- The insecure `http` form is allowed only for localhost, meaning your own computer.
- For localhost, Microsoft **ignores the port number** when comparing addresses. A registered
  `http://localhost/x` therefore also matches `http://localhost:10907/x`. The program does not need
  to know a free port in advance.
- Microsoft does **not** ignore the part after the port, called the *path*. For example,
  `http://localhost/MyWebApp` does not match `http://localhost/MyNativeApp`. Whether the bare
  address `http://localhost` alone is enough for onenote-mcp, which sends the longer address ending
  in `/api/auth/callback`, we could not test, because Microsoft only checks the redirect address
  after you have signed in. Registering both costs nothing and removes the doubt.
- Microsoft says it would be better to use the numeric form `127.0.0.1` instead of the word
  `localhost`, because a misconfigured firewall can break the word form. However, the portal's text
  box refuses to accept `http://127.0.0.1`. Adding that form requires editing the registration's
  manifest (an advanced settings file written in JSON, a plain-text data format). For ordinary use, stay with `http://localhost`.
- The newer-style (IPv6) address of your own computer, `[::1]`, is not supported at all.
- Never register several localhost addresses that differ only in the port number.
- A registration that allows personal accounts may not use query strings (the part of a web address
  after a question mark) or wildcard characters in redirect addresses.

If sign-in later fails with the message **AADSTS50011** ("The reply URL specified in the request does not
match the reply URLs configured for the application"), the message names the address it received.
Register exactly that address, without the port number, under the same platform.

### 6.4 Turn on "Allow public client flows"

Still on the **Authentication** page, look for a switch called **Allow public client flows** (older
versions of the portal put it under a heading called "Advanced settings"). Set it to **Yes** and click
**Save**. Microsoft's page says that an application that has redirect addresses needs a public client
configuration. Our own notes add that without this setting, the backup sign-in method (the "device
code" method, where you type a short code on a Microsoft web page) fails with the message
`unauthorized_client`. We have not yet confirmed the exact current label and position of this switch
on a freshly created registration; see the open questions.

### 6.5 Add the permissions

1. In the left-hand menu click **API permissions** (API means application programming interface, the
   way programs talk to a service), then **Add a permission**, then **Microsoft Graph**, then
   **Delegated permissions**. "Delegated" means "the program acts on behalf of the person who is
   signed in."
2. Add exactly these three, which are what onenote-mcp asks for: **Notes.Read**, **Notes.ReadWrite**
   and **User.Read**. User.Read is normally added automatically when the registration is created.
3. Do **not** add anything under "Application permissions". Microsoft's OneNote documentation states
   plainly that the Graph OneNote service "doesn't support app-only authentication". A background
   service cannot read your notes without you; a signed-in person is always required.
4. If you work in an organization and want to reach notebooks that colleagues have shared with you,
   Microsoft also offers the broader permissions `Notes.Read.All` and `Notes.ReadWrite.All`. They are
   not needed for a personal OneNote and we have not tested them.
5. You normally do **not** click "Grant admin consent". You give consent yourself, once, when you first
   sign in. According to a community reference site (not Microsoft itself), personal accounts do not
   require administrator consent for the delegated Notes permissions. Organizations can configure a
   rule that requires an administrator's approval first; if you see a "need admin approval" screen,
   ask your administrator.
6. Never create a **client secret** or a certificate for this registration. It is a public client, so a
   secret would protect nothing and could leak.

## 7. Giving the ID to the program, and signing in

**With onenote-mcp 1.3.0 or newer.** Open the dashboard. The red "Complete setup" banner shows three
steps. In step 1, paste the Application (client) ID into the box, choose the account type that
matches what you picked in section 5, and click Save. The program stores the number encrypted with
Windows DPAPI and never shows it again, only its last four characters so that you can recognize
which one is saved. In step 2, click Sign in; your browser opens at Microsoft; sign in and click
Accept. Step 3 is about connecting your AI tools and is described in the onenote-mcp
documentation.

**For developers.** The environment variables `ONENOTE_CLIENT_ID` and `ONENOTE_AUTHORITY` override
the stored values. The authority is one of `https://login.microsoftonline.com/consumers`,
`https://login.microsoftonline.com/organizations` or `https://login.microsoftonline.com/common`.

**How long does sign-in last?** The program keeps the refresh token and quietly renews the access
token about once an hour. onenote-mcp's own documentation says the refresh token stays valid for
roughly ninety days of non-use, after which you sign in again. We have not independently confirmed
the ninety-day figure against Microsoft's documentation.

**Taking access away.** For a personal account you can review and remove applications on the
Microsoft account privacy pages (account.live.com). For a work account use the "My Apps" page or
your administrator. Both statements come from experience rather than from a page we fetched.

## 8. What the OneNote service can and cannot do

Everything in this section comes from Microsoft's OneNote overview page dated 30 June 2025, except
the last point. Through Microsoft Graph a program that you have signed in can read and write the
notebooks, sections, section groups and pages that you own or that were shared with you. This
includes personal notebooks stored on consumer OneDrive and notebooks on OneDrive for Business, and
also notebooks owned by a Microsoft 365 group or by a SharePoint team site. The service address
begins `https://graph.microsoft.com/v1.0/me/onenote/`. There is no sign-in-free access: every call
needs a signed-in person.

The last point is from our own experience: the shared demonstration number of the Graph Explorer
tool produces tokens that work for basic profile calls but are rejected by OneNote with the error
code 40001. This is the reason every person needs their own registration.

## 9. When something goes wrong

Each entry below says what you see, what it usually means, and what to do. "Confirmed" means we
checked it against Microsoft's documentation; "from our notes" means it is recorded in the
onenote-mcp project from earlier experience; "unchecked" means it is from general knowledge.

- **You see AADSTS50011 (reply URL does not match).** The redirect address is not registered the way
  the program sent it. Register the address named in the message, without the port, under "Mobile and
  desktop applications". (Confirmed.)
- **You see AADSTS9002346 when starting sign-in.** The registration allows personal accounts only, but
  the program used the `common` sign-in address. Choose "personal accounts" as the account type in the
  program's settings so that it uses the `consumers` address. (From our notes.)
- **You see unauthorized_client.** "Allow public client flows" is switched off. Turn it on
  (section 6.4). (From our notes.)
- **Sign-in works, but OneNote answers with 40001 or "not a valid authentication token".** The program
  is using someone else's ID, usually the Graph Explorer demonstration number, or the account type does
  not match your account. Use your own registration and sign in again. (From our notes.)
- **OneNote answers with error 401.** The sign-in has expired or been revoked. Sign in again. The
  program's address `/api/auth/debug` shows whether a token is present and how old it is. (From our
  notes.)
- **You see AADSTS65001 (consent required).** A permission was not accepted. Sign in again and click
  Accept; in an organization, ask an administrator. (Unchecked.)
- **You see AADSTS700016 (application not found in the directory).** Either the client ID was copied
  incorrectly, or the registration's account type does not include the account you are signing in
  with. Copy the ID again and compare with section 5. (Unchecked.)
- **Everything worked and now you see invalid_grant.** The refresh token has expired or been revoked,
  for example after a long break or a password change. Sign in again. (Unchecked.)

## 10. Security in plain words

The client ID of a public client is not a password: nobody can pretend to be you with it alone,
because the real person must still sign in. We keep it private anyway, so that strangers cannot
send people to a sign-in screen that carries your registration's name. onenote-mcp therefore stores
the ID, the refresh token and the access token encrypted with Windows DPAPI, readable only by your own
Windows user account, and its web interface never displays the full ID. Never put the ID or any
token in a public file, an issue report, a screenshot or a chat. Each person should have their own
registration, and the files that hold tokens are never committed to version control.

## 11. Where this information comes from

All pages were read on 7 October 2026. The date shown is the date printed on the page, when it has
one.

- Microsoft Learn, "How to register an app in Microsoft Entra ID", dated 14 May 2026:
  https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app
  (prerequisites, registration steps, account-type names).
- Microsoft Learn, "Register an application with the Microsoft identity platform" (Graph guide),
  dated 22 January 2026: https://learn.microsoft.com/en-us/graph/auth-register-app-v2
  (alternative menu names, platform configuration).
- Microsoft Learn, "Redirect URI (reply URL) best practices and limitations", dated 14 May 2025,
  updated June 2026: https://learn.microsoft.com/en-us/entra/identity-platform/reply-url
  (localhost rules, the 127.0.0.1 limitation).
- Microsoft Learn, "Use the OneNote REST API", dated 30 June 2025:
  https://learn.microsoft.com/en-us/graph/api/resources/onenote-api-overview
  (what OneNote offers, no app-only access).
- Microsoft Azure free account page (no date shown; it replaced the older FAQ page at the same site):
  https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account (card and phone verification).
- Community reference site for Graph permissions (not by Microsoft, so treat as a hint):
  https://graphpermissions.merill.net/permission/Notes.ReadWrite.html

## 12. Open questions for the first hands-on walkthrough

These could not be settled by reading and should be answered by someone following the guide on a
fresh personal Microsoft account, with screenshots.

1. Can a personal account without any Azure subscription register an application today, and does
   the registration survive after a free Azure account lapses?
2. What is the current exact label and position of "Allow public client flows"?
3. Is the bare address `http://localhost` enough for onenote-mcp, or must the path
   `/api/auth/callback` also be registered?
4. What does the consent screen say for Notes.Read and Notes.ReadWrite, and does any administrator
   step appear for a personal account?
5. Update the guide inside onenote-mcp (`web_sota/src/components/ms-app-registration.tsx`) so that it
   tells people to register both redirect addresses, and add screenshots to this guide.
