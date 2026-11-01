# AI mass-decompilation wave (Oct 2026)

Short-lived context note for reversing-mcp roadmap work. Source: chat
between Sandra and Muse Spark on 2026-10-16 plus the blog post below.
Full session narrative: `operations/session-log/2026-10-16.md`.

## The blog

- popcar, 2026-10-14: "AI is mass-decompiling games - thats both awesome
  and scary"
  (https://popcar.bearblog.dev/ai-is-mass-decompiling-games-thats-both-awesome-and-scary/)
- Opens with an anti-AI figleaf (slop/bots, firings, hardware prices,
  shoved into everything, pride in hand work), then spends the rest
  documenting AI recomp ports with open enthusiasm.
- Hand-decomp baseline: years of community effort (OpenGOAL for Jak and
  Daxter, Ship of Harkinian for Zelda). AI baseline now: days, messy but
  working and stable.
- Examples cited: IsaacRecomp (Flash original to 1440p/165fps),
  OpenCMR2, FFTA any-aspect-ratio, Metroid Prime port, Ratchet and Clank
  nearly done, Skate 3 and Black Ops Zombies in a browser, Mario 64 to
  Scratch, AnyPS5 as a Proton-style PS5-to-PC layer (Animal Well already
  ported).
- Scary half: anyone can liberate any app, theft is unprovable, clean-room
  claims become a joke (malus.sh), licenses possibly unenforceable, more
  invasive DRM likely. Preservation half: abandoned games playable and
  moddable on modern systems.
- Only that one post is relevant; the 2025 back catalog is noise. Already
  pushed to the aiwatcher pipeline (feed 18) on 2026-10-16.

## The tsunami framing

From pro Craft/Artcraft apps through game recomp cloners down to every
Tom, Dick and Sandra with a chat app - AI-driven reversing is now a
mass activity, not a specialist one. Per Sandra 2026-10-16, Artcraft's
Brandon Thomas has not written a line of Rust since February: the new
reality. Hand-mashing `.py` by hand is the donkey on the autobahn -
noble, knows every bend, arrives three weeks late.

### The Hardware Parallel: The Behringer Phenomenon (Oct 2026)

The same wave has crossed from pure software into physical electronics.
Behringer (Music Tribe) represents the industrial extreme of this shift:
- **From Coolaudio silicon to ROM/DSP reversing**: Moving beyond Curtis analog IC clones
  (V3340/V3320) into extracting vintage digital ROMs (Roland JP-8000 supersaw, Prophet VS
  vector wavetables, Casio CZ Phase Distortion).
- **Agentic RE tooling**: Leveraging agent-native MCP disassembler bridges like
  [REA](https://rea.tools/) (300k+ GitHub stars) to ingest firmware dumps and reconstruct DSP
  math directly into clean C/C++ or Rust targeting sub-\$1.50 ARM Cortex-M and RISC-V chips.
- **Vertical PRC Manufacturing Moat**: Music Tribe City in Zhongshan produces custom
  tooling, high-speed SMT boards, and rigid plastic/aluminum enclosures for \$49–\$99 retail.
- **The Next Frontier — Dual-Platter DJ Gear**: Legacy club standards (AlphaTheta/Pioneer
  CDJ-3000 at \$3,000+) run on commoditized ARM SoCs and simple faders/encoders. With
  Rekordbox databases (`export.pdb`) and Pro DJ Link protocols already reversed by open
  source, high-end standalone dual-platter DJ hardware is ripe for a sub-\$500 disruption.
- Full reference architecture (hardware): `reversing-mcp/docs/BEHRINGER_PLAYBOOK.md`.
- Strategic manifesto on the death of emulation & console recompilation: `reversing-mcp/docs/MASS_RECOMP_AND_CONSOLE_LIBERATION.md`.

## Implications for reversing-mcp (open, not decided)

1. Fast messy-but-working recomp beats slow perfect decomp for
   preservation throughput. Gym stages should reward "runs and is
   moddable", not just "matches source".
2. Auto-port layers (Proton/AnyPS5 style) and auto-generated mod hooks
   are the output users actually want - decompilation is the means.
3. Provenance problem: if theft is unprovable, gym/ClickerLab runs need
   to record *how* an artifact was produced (engine, model, inputs),
   because the license story is getting murkier, not clearer.
4. Ingest UX matters as much as engine power: today's Gemini reversing
   firehose arrived as a leporello of Docs exports. Consolidate-first
   pipelines (merge by date, then distill) beat per-file handling.

## Related

- iPad-Gemini-to-Docs pipeline + `google-docs-mcp` wiring in opencode:
  session log 2026-10-16, `opencode/MCP_SETUP.md`.
- Merge-and-distill prompt for the pending Gemini firehose: session log
  2026-10-16 (run in a fresh opencode session with Docs + revops live).
