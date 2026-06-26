---
title: "Bun Adoption Standard (package manager + runner)"
category: standard
status: active
audience: mcp-dev
skill_candidate: true
related:
  - standards/WEBAPP_SOTA_STANDARDS.md
  - standards/NAKED_PC_INSTALL_STANDARD.md
  - standards/CODE_QUALITY_STANDARDS.md
  - integrations/bun.md
last_updated: 2026-05-31
---

# Bun Adoption Standard (v1.0)

**Bun replaces npm as the JS package manager and script runner. Vite stays.**

Reference companion (what Bun is, command cheatsheet, Windows specifics,
gotchas): [integrations/bun.md](../integrations/bun.md).

---

## 1. Scope — what Bun does and does not do here

| Layer | Tool | Change |
|---|---|---|
| JS package manager | npm → **bun** | **Adopt.** `bun install`, `bun add`, `bun remove`. |
| JS script runner | npm → **bun** | **Adopt.** `bun run <script>`, `bunx <bin>`. |
| Lockfile | `package-lock.json` → **`bun.lock`** | **Adopt.** Text, committed. |
| Dev server + bundler | **Vite** | **Keep.** Do NOT replace with `Bun.build`. |
| Lint / format | **Biome** | **Keep** (unchanged; pairs cleanly with Bun). |
| UI test | **Playwright** (headless) | **Keep** (unchanged; see VERIFICATION_STANDARDS). |
| Unit test | vitest | **Optional later.** `bun test` only where it earns it. |
| Python | **uv** | **Untouched.** `uv run python` stays mandatory. |

Rationale for keeping Vite: Vite 8's Rolldown (Rust) bundler closed most of
Bun's bundler speed gap, and the Vite plugin/HMR ecosystem is mature and
load-bearing. Swapping it out buys little and risks a lot.

> [!IMPORTANT]
> This is a **package-manager + runner** standard, not a runtime migration.
> The runtime move (Vite executing on Bun instead of Node) is the optional,
> per-repo Phase 2 below — never fleet-wide by default.

---

## 2. The `--bun` boundary (read before migrating)

- `bun run dev` → runs the script; node-based CLIs like `vite` **still execute
  on Node** (Node stays installed). This is Phase 1. Zero runtime risk.
- `bun run --bun dev` → forces Vite onto the **Bun runtime**. This is Phase 2,
  where Bun-on-Windows / plugin rough edges can appear.

If you do not understand which form you are running, you are running Phase 1.

---

## 3. Naked-PC integration

The naked-PC standard's `start.ps1` `Require-Command` block currently
winget-installs **uv + Node.js**. Add Bun; **keep Node.js as the fallback**
throughout the transition (Vite officially needs Node 20.19+/22.12+, and Phase 1
executes Vite on Node).

```powershell
# In Require-Command (start.ps1) — add alongside existing uv + Node.js checks
if (-not (Get-Command bun -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Bun..."
    winget install --id Oven-sh.Bun -e --accept-source-agreements --accept-package-agreements
    # Fallback if winget unavailable:
    # powershell -c "irm bun.sh/install.ps1 | iex"
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH","User")
}
```

The local Vite guard and import smoke-test in `start.ps1` are unchanged.

---

## 4. Per-repo migration checklist (Phase 1 — the safe one)

Validate on **one** non-critical webapp repo first (suggest: a small dashboard
with a plain Vite/React/Tailwind frontend, no native deps). AI-assisted, a
single-repo Phase 1 migration is minutes, not hours.

1. [ ] `bun --version` resolves (install via §3 if not). Record version.
2. [ ] From the frontend dir: `bun install` (reads existing `package.json`).
3. [ ] Confirm `bun.lock` (text) generated. **Delete `package-lock.json`.**
4. [ ] `bun run dev` — Vite dev server boots, HMR works, no console errors
       (Playwright headless check per VERIFICATION_STANDARDS §2.4).
5. [ ] `bun run build` — production build succeeds; diff `dist/` against the
       npm baseline for unexpected size/asset changes.
6. [ ] `bun run check` / Biome lint+format still pass.
7. [ ] Update `start.ps1` to use `bun install` + `bun run` (keep Node present).
8. [ ] `.gitignore`: ensure `node_modules/` ignored (per GITIGNORE_STANDARDS);
       **commit `bun.lock`**.
9. [ ] CI (if any): `bun install --frozen-lockfile`; cache `~/.bun/install/cache`.
10. [ ] README/INSTALL.md: note Bun as package manager; Node still required.
11. [ ] gitops commit (NEVER fileops for git): scope `chore(frontend): migrate to bun`.

If steps 4–6 fail and the cause is an npm-compat edge case
(integrations/bun.md §"npm-compat reality"), fall back to npm for that repo and
log it in BUGS_DEPOT.md. No shame, no shortcut — Phase 1 must not break a build.

### Phase 2 (optional, per-repo, only after Phase 1 is stable)

12. [ ] Try `bun run --bun dev` and `bun run --bun build`.
13. [ ] Full Playwright pass + visual diff. Any regression → stay on Phase 1
        for that repo. Phase 2 is opportunistic, never mandatory.

---

## 5. Fleet rollout

Do **not** mass-migrate. Order:

1. One pilot repo, full Phase 1 checklist, soak for a few days.
2. Roll Phase 1 across new repos by default (scaffold templates use Bun).
3. Backfill existing repos opportunistically when already touching their
   frontend — not as a dedicated 135-repo sweep.
4. Phase 2 only per-repo, only where someone validates it.

Realistic timeline: pilot + validation ~1 day; "new repos default to Bun" is a
template edit (minutes); fleet backfill is ambient over weeks as repos get
touched, not a scheduled sprint.

---

**Owner:** Sandra Schipal
**Last Updated:** 2026-05-31
