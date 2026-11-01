# reversing-mcp — Next Steps

**Rewritten:** 2026-10-12 (Gym G1 shipped; product is the Gym now).

## Closed

- March 2026 plan: companion architecture (ReVa external), install modes, version gate.
- 2026-10-11: Tier 2 bridge, backend transplant, Next.js kill, chat standard, assfix
  0→86, fakefind 6/6, ghaudit first run, release v0.4.0, revops registration.
- 2026-10-11: Hopper CLOSED (unsupported on win32, verified). Tier 3 static half done.
- 2026-10-12: TEXT.DKI resolved (Opus+Ghidra; decoder in directmedia-mcp, reader live).
- 2026-10-12: **Gym G1 shipped** (job runner, stages 0/1/4, REST+MCP+`/gym` page, proven
  on Digibib5). PRD names the Gym as the product.

## Priority 1: Gym G1b + G2 (next)

- [ ] G1b elicitation: format-spec stubs, help-file mining, generated tour-YAML draft
  (spec: `docs/ELICITATION_AND_CLICKER.md` Part A; no VM needed).
- [ ] G2 oracle capture: Frida file-API trace + outputs + screenshots in VM (needs Frida
  tools installed here + virtualization-mcp handshake).
- [ ] Ghidra 12.0 → 12.1.x upgrade (unlocks REA-ghidra; own headless works on 12.0).
- [ ] Cold rescore to confirm 86 (same-context score is self-assessed by SOP rule).

## Priority 2: Gym G3-G5

- [ ] G3 clicker tour: live pywinauto driver (read GUITAR/AppAgent/UFO trio first).
- [ ] G4 UI build: Tauri template + codegen from capture bundle (gate: user approves).
- [ ] G5 round trip + compare: `--gym-roundtrip` hook, oracle re-open verdict.
- [ ] Expert-ready gap reports from failed compares (contributor funnel).

## Priority 3: Later

- [ ] UIA-to-IPC + file-write-to-offset correlations; version-diff maps.
- [ ] Webapp "Ask about this app" surface over `rea_investigate` + map viewer.
- [ ] IDA Free scope check only if a Free-based workflow is ever proposed.

## Priority 4: Shop window (demo the real thing, never vapor)

- [ ] `demo-vid-mcp` Gym run on camera: intake → triage → amber verdict → gate go
  (live `gym` calls, narrated). Then the webapp tour + first-map video as specced.
- [ ] README Preview screenshots once the Gym page has a real run to show.

## Reference Resources

- Upstream repo: https://github.com/sandraschi/reversing-mcp (PRD.md, docs/GYM_SPEC.md, docs/ELICITATION_AND_CLICKER.md)
- REA: https://rea.tools · https://github.com/morluto/rea
- Ghidra releases: https://github.com/NationalSecurityAgency/ghidra/releases
- Fleet CUA standard: `mcp-central-docs/standards/rules/cua_nsis_smoke_testing.md`
