# Retro Gaming Research Hub - Emulators, Batocera Linux, Preloaded-Drive Grey Market

**Status:** active research + build log
**Created:** 2026-10-15
**Scope:** Game emulation as software (emulators, Batocera/EmuELEC/RetroPie/Lakka/Recalbox), the preloaded-ROM drive market (Kinhank et al.), and how to run a clean legal setup on fleet hardware. Explicitly NOT a source for ROMs, BIOS files, or download locations.
**Question it answers:** what is legal, why is Amazon full of 120,000-game drives anyway, and how do I play old games without buying contraband?

## Map

| # | Doc | What |
|---|-----|------|
| 0 | This README | Index + TL;DR + decisions |
| 1 | `01-EMULATOR-ECOSYSTEM.md` | Legal split (emulators vs ROMs vs BIOS), distro comparison, myth busting |
| 2 | `02-KINHANK-PRELOADED-DRIVES.md` | Amazon case study (ASIN B09P36912T): what it is, why it infringes 3x over, why it stays listed |
| 3 | `03-CLEAN-BATOCERA-VM-GUIDE.md` | Build log: clean Batocera 43.1 in VirtualBox (`batocera-clean`) via virtualization-mcp, quirks + fixes |

## TL;DR (Oct 2026 research)

* **Emulators are legal, preloaded ROMs are not.** Selling a drive with 120,000 commercial games is mass copyright infringement, full stop. No "abandonware" or "24-hour" exception exists in US law.
* **Kinhank drives also violate Batocera's own license**, which explicitly forbids selling Batocera pre-installed on any commercial medium (`wiki.batocera.org/license`).
* **Amazon listings persist because of marketplace mechanics**, not legality: 3rd-party seller (`yunsheng store`) + Fulfilled by Amazon + vague "Built-in 120000+ Games" wording + DMCA safe harbor (reactive takedowns only) + whack-a-mole re-listing.
* **The clean path is easy and cheap:** official Batocera image (free) + empty drive/VM + your own cartridge dumps + homebrew. Proven on Goliath 2026-10-15, see doc 03. Gameboy/Pong-era systems run perfectly virtualized; PS2-era and up wants bare metal for GPU reasons.
* **Buyer risk is low but real:** buyers are essentially never prosecuted, but the goods are infringing, can be seized in transit, and ship with zero warranty, frequent fake-capacity drives, and occasional malware in the boot partition.

## Decisions log

* 2026-10-15: Created hub after Amazon listing B09P36912T analysis. Verified Batocera 43.1 zen3 image (`batocera-zen3-x86-64-v3-43.1-20260529.img.gz`, 4.03 GiB) boots clean in VirtualBox on Goliath; snapshot `clean-booted-43.1` kept. No ROMs or BIOS files touched at any point.

## Sources (top)

* Batocera license: `wiki.batocera.org/license` (sale of pre-installed media forbidden)
* Batocera downloads: `batocera.org/download` (current stable 43.1, 2026-05-29 builds)
* Amazon listing: `amazon.com/dp/B09P36912T` (Kinhank 2TB, 120000+ games, Batocera 33, seller yunsheng store)
* Kinhank official: `kinhank-retrogame.com` (advertises 120,000+ preloaded titles, 80+ emulators)
* Lire encore: Nintendo v RomUniverse ($2.1M), Nintendo/Yuzu settlement ($2.4M) - enforcement precedent
