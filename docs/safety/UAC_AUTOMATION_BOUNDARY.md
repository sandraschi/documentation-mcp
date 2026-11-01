# UAC prompts cannot (and should not) be automated

**Last Updated**: 2026-10-20

## The rule

**No agent, script or CUA loop may approve a UAC prompt.** Prefer installs that
need no elevation; when elevation is unavoidable, a human clicks once (or a
standing, reviewed elevation helper is installed with consent). Never leave a
machine in a no-prompt UAC configuration to make automation easier.

## Why the prompt resists automation

The consent prompt runs on the **secure desktop** — a separate desktop that
user-mode processes cannot see or send input to. `SendInput`, pywinauto,
AutoHotkey and CUA all fail there, because there is no input path from the
interactive session. That isolation is the feature, not an implementation gap.

Two related facts:

- **UAC is not a security boundary** in Microsoft's model (it is a consent
  mechanism). That is why UAC bypasses are treated as bugs to patch, not as an
  API to call.
- **Elevation state is per-process.** A process that is already elevated
  (service, scheduled task, SYSTEM context) needs no prompt; a normal agent
  process cannot acquire that state without consent or policy.

## What "automating UAC" actually means

| Pattern | What it really does | Verdict |
|---|---|---|
| `ConsentPromptBehaviorAdmin=0` | Elevates admins without asking | **Forbidden** — disables the boundary |
| `PromptOnSecureDesktop=0` | Moves the prompt to the normal desktop, where automation *can* click it | **Forbidden** — direct attack vector |
| UAC bypass (fodhelper, computerdefaults, …) | Abuses a trusted auto-elevating binary | **Forbidden** — malware technique |
| Standing elevation (scheduled task / service, installed once with consent) | Runs installers at high integrity thereafter | **Allowed** — one reviewed install, then policy |
| Per-user / portable installs | No elevation at all | **Preferred** |

## Fleet practice

1. **Avoid elevation first.** Per-user VST3 (`%LOCALAPPDATA%\Programs\Common\VST3`),
   portable zips, `winget --scope user`, user-scope Python/Node tooling.
2. **When an installer insists** (machine-wide VST3, drivers, services), a human
   approves the prompt. Document what was installed and where.
3. **If repeated elevation is genuinely needed**, install one reviewed
   scheduled task or service that runs the specific reviewed installer, and log
   every invocation. Do not generalise it into "run anything elevated".
4. **Verify afterwards** by observable effect (file present, service running,
   plugin scanned), not by trusting the installer's exit code.
5. **Never** set `PromptOnSecureDesktop=0` or `ConsentPromptBehaviorAdmin=0` on a
   fleet machine. If a tool "requires" it, the tool is the problem.

## CUA vs UAC (the confusion is common)

- **CUA** (computer-use automation) drives a visible GUI: clicks, keys, drags.
- **UAC** is the elevation consent prompt, deliberately outside the visible
  desktop that CUA can reach.

CUA cannot click UAC. Anything claiming it can has either disabled the secure
desktop or is not actually crossing the elevation boundary.

## Worked example (2026-10-20, free VST3 set)

- Surge XT, Dexed, Dragonfly, Valhalla: portable zips extracted to the per-user
  VST3 folder — **no UAC**.
- Valhalla's download turned out to be an installer, run with `/S` via
  `Start-Process -Verb RunAs`: **one human approval**.
- Cardinal (1.1 GB) via winget: **one human approval**.
- Verification was effect-based: SoundCraft's `engine.vst3_plugins` listed 11
  plugins; Surge, Valhalla and Cardinal each loaded on a track and bounced
  audio.

## Related

- [powershell-recycle-bin-workaround.md](powershell-recycle-bin-workaround.md)
- [../standards/AGENTS.md](../standards/AGENTS.md) — tool paths and shell rules
- [../troubleshooting/TRAPS_AND_PITFALLS.md](../troubleshooting/TRAPS_AND_PITFALLS.md)
