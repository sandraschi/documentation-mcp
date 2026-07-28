# Onboarding Standard — first-timer host / account setup

**Status:** ACTIVE — fleet mandatory when the repo needs external setup  
**Version:** 1.0 (2026-07-26)  
**Audience:** Agents scaffolding or raising new `*-mcp` repos; humans reading `docs/ONBOARDING.md`

**Related:** [AGENT_INSTALL_REFERENCE.md](./AGENT_INSTALL_REFERENCE.md), [LLM_AND_INSTALL_TIERS.md](./LLM_AND_INSTALL_TIERS.md), [NAKED_PC_INSTALL_STANDARD.md](./NAKED_PC_INSTALL_STANDARD.md), [README_STRUCTURE.md](./README_STRUCTURE.md), [TESTING_GUIDE.md](./TESTING_GUIDE.md) (declared doubles)

---

## Why this exists

INSTALL.md answers *how to get the MCP bridge running*.  
**Onboarding** answers *what world you are joining and what you must do before the bridge is useful*.

These often need a **human account, paid plan, or heavyweight host app** before any tool call works:

| Repo class | External dependency | Example |
|------------|---------------------|---------|
| Fediverse / social | Instance account + app token | `mastodon-mcp` |
| Cloud API product | Vendor signup + API key | `worldlabs-mcp` → worldlabs.ai |
| Host DCC / game engine | Desktop app install | `blender-mcp`, `unity3d-mcp`, `godot-mcp` |
| Media servers | Local service + token | `plex-mcp`, `jellyfin-mcp` |
| Hardware / robots | Device + SDK / firmware | `unitree-mcp`, `yahboom-mcp` |

Naked-PC `start.bat` can install uv/Node. It **cannot** create a Mastodon account or install Unity for you. That gap is onboarding.

---

## When ONBOARDING is mandatory

**Default: YES.** Almost every fleet MCP wraps something the user must install or log into before they get joy. Treat onboarding as required unless you can prove an exemption.

Ship `docs/ONBOARDING.md` (+ webapp first-run UX below) when **any** of these are true (nearly always):

1. A **wrappee / host application** must be installed and runnable — Blender, Unity, Godot, Notepad++, Mixxx, Plex, Resolve, KiCad, GIMP, …
2. A third-party **account** or **API token** is required for real use — Mastodon, Discord, World Labs, cloud LLMs, …
3. Use may require **money**, a **credit card**, a **paid tier**, or **usage credits**.
4. First useful action needs more than `uv sync` / `start.bat` (OAuth, developer app, addon enable, project path, firewall, GPU driver, …).

**Rule of thumb:** If the README names a product that is not this MCP process itself, that product needs onboarding. `notepadpp-mcp` without Notepad++ installed is a dead bridge — document install + detect + red CTA.

**Exempt (rare):** **No wrappee and no online account necessary** (pure in-process util, nothing to install or sign up for). Mark `Onboarding: N/A` plus a one-line rationale in `docs/DEVELOPMENT.md`. If **either** a wrappee **or** an online account exists, onboarding is mandatory. Do **not** use N/A to save time.

---

## Required artifact

```
docs/ONBOARDING.md          ← first-timer narrative (DEFAULT for wrappee/account repos)
INSTALL.md                  ← link to ONBOARDING near the top
README.md Documentation table ← row for Onboarding
webapp Dashboard            ← big red under-hero CTA + MOCK-until-onboarded (webapp repos)
webapp Settings / Help      ← secondary cue + docs pointer
```

Optional: dedicated route `/onboarding` for long wizards (Unity project path, Blender addon enable). The **big red under-hero button** is still mandatory on Dashboard.

---

## Required sections (exact order)

`docs/ONBOARDING.md` MUST use these headings:

### 1. What this is for

Two to five sentences: who benefits, what the MCP does, what it does **not** do.  
Example: “Human-approved Mastodon outbox for fleet promotion drafts — not an auto-poster, not Bluesky.”

### 2. Cost and accounts (money / CC)

Honest table. Never bury paid requirements.

| Question | Answer (fill honestly) |
|----------|------------------------|
| Do I need an account? | Yes/No + where |
| Free tier? | Yes / limited / No |
| Credit card required? | Yes / No / only for paid tier |
| Ongoing cost? | Free / subscription / usage metered |
| Who bills? | Vendor name (not sandraschi unless true) |

If free forever on a public Mastodon instance: say so. If World Labs needs credits: say so up front.

### 3. Prerequisites outside this repo

Bullet list of **host-world** needs (not uv/Node — those stay in INSTALL.md):

- Account URL / signup link
- App / editor version floor
- Hardware (GPU, robot, capture device)
- Network (local LAN, firewall ports)

### 4. First-timer setup steps

Numbered, clickable, Windows-first PowerShell where commands are needed.  
One path only for the happy case. Link INSTALL Options A–D for packaging variants.

### 5. Pitfalls (read before you click Publish)

Known foot-guns: dry-run defaults, rate limits, wrong store edition of an app, headless vs GUI, token scopes, “I posted to production by accident”, regional blocks, ToS.

### 6. Sanity check

How the user knows onboarding worked:

- Health endpoint field (`instance_configured: true`)
- Settings page green badge
- One dry-run tool call that returns `"dry_run": true` or a probe that returns `"success": true`
- Screenshot of host app showing the connection (optional)

### 7. Declared doubles (if any)

Cross-link: what works **without** finishing onboarding (dry-run, empty inbox). Must match [TESTING_GUIDE.md](./TESTING_GUIDE.md) § Declared doubles — no silent fake success that looks live.

---

## Webapp first-run cue (webapp repos)

When backend health shows “not configured” (no token, host offline, etc.):

### Required UX

1. **Big red onboarding button under the Dashboard hero** — full-width (or dominant), high contrast red, label like “Complete onboarding — connect {Host}”. Links to Settings / Onboarding wizard. `data-testid="onboarding-cue"`.
2. **Mock-until-onboarded sample content** — KPIs, inbox, recent lists MAY show **declared** sample data so the UI is not a blank desert. Rules:
   - Every mock surface carries a visible **MOCK** badge (`data-testid="mock-badge"`).
   - Sample actors use obviously fake names (e.g. **Joe Mocky**, **Sandra Mockinger**) — never real users.
   - Body text includes `[MOCK]` or equivalent.
   - Dashed rose/red borders preferred for mock cards.
   - Page banner: `data-testid="mock-data-banner"` explaining samples clear after setup.
3. **Clear on success** — when health reports configured / connected (`instance_configured`, host probe OK, etc.), **remove all mock content** and show live (or honestly empty) data only. No toggle to “keep mocks”.
4. **Settings** may keep a secondary onboarding panel; the **primary** CTA is the red under-hero button.

### Forbidden

- Fake KPIs **without** MOCK badges (that is undeclared gaslighting — fails FakeFind + gate).
- Mock content that remains after successful onboarding.
- Using real colleague names as sample actors.

Declared in code: e.g. `webapp/src/lib/mockOnboarding.ts` + `docs/ONBOARDING.md` § Declared doubles / Mock-until-onboarded.

`data-testid="onboarding-cue"` on the **big red** Dashboard button (primary).

---

## Host catalog (copy / adapt)

| Host / vendor | Typical onboarding burden | Money note |
|---------------|---------------------------|------------|
| Notepad++ / Win apps | Install host via winget or vendor site; probe path | Usually free |
| Mastodon / Akkoma / etc. | Instance account + Development app token | Usually free; some instances invite-only |
| World Labs / similar AI APIs | Signup + API key + maybe credits | Often CC for usage |
| Blender | Install Blender + enable addon / MCP bridge | Blender free; time cost |
| Unity | Editor install + project + package | Personal vs Pro licensing |
| Unreal / Godot | Editor install | Engine free; marketplace assets may cost |
| Plex / Jellyfin | Server URL + token | Plex may need Plex Pass for some APIs |
| Discord | Bot application + token + intents | Free; verify bot in Discord Dev Portal |
| Cloud LLM | API key | Almost always metered / CC |

Agents scaffolding a new wrappee: fill the catalog row into §2–§5 literally; do not invent “free and unlimited” if the vendor meters.

---

## Relationship to INSTALL.md

| Doc | Job |
|-----|-----|
| **ONBOARDING.md** | Human + vendor world: accounts, money, pitfalls, first useful call |
| **INSTALL.md** | Get MCP + webapp binaries running (winget, Options A–D) |
| **CONFIGURATION.md** | Env var reference table |
| **TROUBLESHOOTING.md** | Symptom → fix after setup |

INSTALL.md MUST include near the top:

```markdown
> **First time?** Complete [docs/ONBOARDING.md](docs/ONBOARDING.md) before expecting live host calls.
```

---

## New-repo gate

**Onboarding is on the hard ship checklist** in `standards/AGENTS.md` §4.1 item **8** (default yes).

Agents must ship, for wrappee/account repos:

1. `docs/ONBOARDING.md`
2. Big red under-hero `onboarding-cue`
3. MOCK-until-onboarded UI that clears when configured

Assess severity: missing onboarding / red CTA / MOCK pattern when a wrappee **or** online account exists = **HIGH** (`patterns/repo-assess-and-fix.md`). `Onboarding: N/A` is only valid for **rare: no wrappee and no online account necessary** — without that rationale = **HIGH**.

---

## Template stub

```markdown
# Onboarding — {repo-name}

## What this is for
…

## Cost and accounts (money / CC)
| Question | Answer |
|----------|--------|
| Do I need an account? | |
| Free tier? | |
| Credit card required? | |
| Ongoing cost? | |
| Who bills? | |

## Prerequisites outside this repo
- …

## First-timer setup steps
1. …
2. …

## Pitfalls
- …

## Sanity check
- …

## Declared doubles
- …
```

Copy to `docs/ONBOARDING.md` and fill every cell. Empty “Credit card required?” is a gate fail.
