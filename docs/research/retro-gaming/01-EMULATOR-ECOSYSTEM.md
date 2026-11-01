# 01 - Game Emulator Ecosystem: What Is Legal and What Is Not

**Purpose:** The one-page legal/technical split everyone in retro gaming needs. Status of knowledge Oct 2026, US law focus (Sandra/Steve context: EU/AT law is directionally the same on the points below).

## 1. The three layers (only one of them is the problem)

| Layer | Examples | Legal status |
|-------|----------|--------------|
| **Emulator software** | RetroArch, Dolphin, PCSX2, mGBA, MAME (emulator itself) | **Legal.** Clean-room reimplementation precedent (Sony v Connectix, Sony v Bleem!, 1999-2000). Open source, freely distributable. |
| **Game ROMs** | Any commercial game dump you did not make from your own cartridge/disc | **Infringing to distribute, infringing to download.** Copyright stays with the publisher for 70+ years; "abandonware" has no legal meaning. |
| **Console BIOS/firmware** | Sony PS1/PS2 BIOS, Sega CD BIOS | **Separately copyrighted software.** Shipping a BIOS you did not dump yourself is its own infringement, independent of games. |

Rule of thumb: the *player* is legal, the *content* is licensed. A device/app that plays games is fine. A device/app that *comes with* games it has no license for is contraband.

## 2. Retro Linux distros compared

All free, all open source, all ship with (at most) a handful of homebrew demo games. You add your own dumps.

| Distro | Base | Best for | Notes |
|--------|------|----------|-------|
| **Batocera.linux** | Buildroot, EmulationStation | x86 PCs, Raspberry Pi, handhelds, bare-metal USB boot | Largest device matrix (x86_64, zen3-optimized x86-64-v3, RPi 0-5, Odroid, Anbernic...). v43.1 current Oct 2026. License **forbids commercial pre-installed sale**. Fleet-verified, see doc 03. |
| **EmuELEC** | LibreELEC fork | Amlogic TV boxes | The Kinhank-box stack (Super Console X etc. run EmuELEC/EmuELEC+Android). Same ROM rules. |
| **RetroPie** | Raspberry Pi OS + EmulationStation | Raspberry Pi tinkerers | Oldest community, Pi-focused, manual setup. |
| **Lakka** | LibreELEC + RetroArch | Minimal RetroArch appliance | Lightest, RetroArch-only UI, no EmulationStation. |
| **Recalbox** | Buildroot, EmulationStation | Plug-and-play Pi/PC | Closest to Batocera in spirit, smaller device matrix. |

Underneath most of them: **libretro cores + RetroArch** (the shared emulator API/runner), plus standalone emulators (Dolphin, PCSX2, RPCS3...) for systems libretro does not cover well.

## 3. Myths, killed

* **"Abandonware is legal."** No. Copyright does not lapse because a game is old or unprofitable. Only the rights holder (or expiry, ~70 years after author's death in US/EU) frees a work.
* **"I can download it if I own the cartridge / delete after 24h."** No such rule in US law. Personal backup-from-your-own-media is the defensible zone (and even that is contested for circumvented DRM under DMCA 1201); downloading someone else's rip is not it.
* **"Emulators themselves are grey area."** Outdated framing from the 90s lawsuits, which the emulator makers won. The emulator is settled law; the ROM bundle is the infringement.
* **"If it's on Amazon it must be licensed."** See doc 02. Amazon is a marketplace with reactive enforcement, not a licensor.

## 4. The legal ways to fill a Batocera install

1. **Dump your own cartridges/discs** (defensible personal-backup zone; needs a dumper/adapter per system).
2. **Homebrew ROMs** (free, legal, many excellent - Batocera-adjacent communities curate lists).
3. **Licensed re-releases** (Nintendo Switch Online, PS Plus Classics, official Mini consoles, Antstream, GOG retro catalog) - not Batocera, but the zero-friction legal shelf.
4. **Public domain / rights-released games** (small but real catalog).

What is never on this list: a 2TB drive with 120,000 games for EUR 115. That is doc 02.
