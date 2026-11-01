# Fleet repo scorecard — usability / popularity / realism / completion

**Status:** Seed planted 2026-10-04 · 6 rows scored · 290 to go in waves
**Tags:** [fleet, audit, tiering, scorecard]
**Signals (point-in-time):** [operations/fleet-repo-signals.csv](../operations/fleet-repo-signals.csv) — regenerable via `C:\Users\<user>\AppData\Local\Temp\opencode\fleet_repo_probe.ps1` (read-only, no launches)
**Parent plan:** [daemon-tiering-plan](daemon-tiering-plan.md)

## Fleet snapshot (2026-10-04, 296 repos scanned)

- **171 without `.venv`** (58% never installed), **211 without `data/`**, **249 without `logs/`**, 68 with zero Python.
- **24 backend ports alive.** That is the entire living fleet at noon on a Sunday.
- Conclusion: most of the fleet is early-days or blue-moon by *evidence*, not opinion. The tiering plan is downsizing to reality, not ambition.

## Criteria (score in waves, evidence first)

- **Usability:** verified-live (touched it this month, works) / working (daemon answers, unused) / untested / broken (known failure).
- **Popularity:** GH stars + external users if any; default is internal-only — say so, don't inflate.
- **Realism:** real wrappee (installed software millions use) / niche (pro hardware, small user base) / fantasy (hardware/persona with no users yet).
- **Completion:** assfix-zero complete / scaffold (runs, gaps) / runt (scaffold only) / unassessed.
- **Tier:** 0 stdio / 1 on-demand / 2 service — proposed until implemented.

## Seed rows (audited 2026-10-04, GH stars via gitops 2026-10-04)

| repo | usage | usability | popularity (★) | realism | completion | tier | evidence |
|---|---|---|---|---|---|---|---|
| calibre-mcp | daily grind | verified-live | 45 ★ (fleet #3) | real (Calibre 9.14, 13,184 books live) | complete-ish | 2 | port alive, data+logs, details fix verified |
| aiwatcher-mcp | daily grind | working | 2 ★ | real (fleet's own watcher) | scaffold+ | 2 | port alive, 60MB data, 04:55Z job |
| speech-mcp | daily grind (voice periods) | working | 2 ★ | niche (mic/VRAM hardware) | scaffold+ | 1 | port alive, 82MB data/models, lazy extras |
| notepadpp-mcp | blue moon | untested | 5 ★ | real (Notepad++) | unassessed | 0 | venv, no data/logs, port dead |
| handbrake-mcp | blue moon (~1 job/mo) | untested | 2 ★ (as handbrakemcp) | real (HandBrakeCLI) | unassessed | 0 | no venv/data/logs, in-mem jobs need sqlite fix |
| openbci-mcp | fantasy | untested | 2 ★ | fantasy (EEG skullcap, ~0 users) | scaffold | 0 | no venv/data/logs, port dead, full scaffold idle |

## GH star ranking (gitops `repo_list` + gh CLI, 297 repos, 2026-10-04)

Leaders: inkscape-mcp 82 · blender-mcp 53 · calibremcp 45 · windows-computer-use-mcp 40 · freecad-mcp 32 · worldlabs-mcp 24 · ocr-mcp 23 · advanced-memory-mcp 19 · qcad/virtualization 16. **109 repos at 0 ★.** Notables for other threads: bumi-mcp 7 ★, learnbot-mcp 1 ★, classroom-mcp 1 ★, japanophile-mcp 0 ★. Pattern: real creative tools (inkscape/blender/freecad) earn stars; wrappers earn dust. Popularity column in waves = stars + external-issue/PR activity, both via gitops, never vibes.

## How waves fill the rest

1. Take 10 repos sharing a signal cluster (e.g. next 10 no-venv-with-scaffold).
2. 5-minute check each: does the wrappee exist? does it start? who would use it?
3. One table row each + tier proposal; contentious ones get a note, not a meeting.
4. Downgrades follow the tiering plan (boot only, webapps untouched, single-repo reverts).
