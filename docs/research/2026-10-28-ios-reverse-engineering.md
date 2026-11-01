# Reversing an iPhone app (October 2026 field guide)

**Private -- Sandra S. + collaborators only. Not for public distribution.**

**Status:** research note, filed 2026-10-28. Verified against live sources same day.
**Scope:** how to go from "great app on my iPhone" to understood/cloned behavior.
Learning and interop are the frame; republishing someone else's app is not covered here.

## 0. Decide what "reverse" means (three goals, three bars)

| Goal | What you need | Jailbreak? |
|------|--------------|------------|
| Understand how it works | Decrypted binary + disassembler | Only to obtain the binary (see 1) |
| Clone the behavior | Network API contract via proxy (see 3) | No, unless SSL pinning |
| Drive the UI automatically | Screenshots + scripted taps (see 4) | No (but needs a Mac + cert) |

## 1. Getting the decrypted binary (October 2026 status)

App Store IPAs are FairPlay-encrypted. Static tools cannot read them until
something on-device decrypts them. Verified state as of 2026-10-28:

- **No public jailbreak for iOS 27** (nor 26/17-18 on modern chips per status
  trackers). Dopamine cracked iOS 26 in Aug 2026 after 326 days -- rootless,
  limited (A12/A13, up to 26.0.1). An untethered 27.0.1 demo (Calif, Hexacon
  Oct 16) exists as a demo only, no public tool.
- **TrollStore + TrollDecrypt: no jailbreak required.** TrollDecrypt launches the
  app and reads the decrypted executable out of process memory, one tap back to
  an IPA ([donato-fiore/TrollDecrypt](https://github.com/donato-fiore/TrollDecrypt)).
  Catch: TrollStore installs only on specific iOS versions, so this needs a device
  sitting on a compatible one.
- **checkm8 bench device (iPhone X and older):** unpatchable bootrom flaw,
  jailbreakable forever. The eternal RE bench -- but it cannot install apps that
  require current iOS, so it only helps for apps that still support old systems.
- **House rule:** keep one spare iPhone/iPad on a vulnerable version and never
  update it. Every reverser learns this once.

Get the IPA onto your PC first if you like (ipatool with your own Apple ID, or
Apple Configurator) -- it arrives encrypted; decryption happens on-device or
not at all.

## 2. Static analysis (this part runs on Goliath)

Unzip the decrypted IPA, then: `strings`, Info.plist, asset catalogs (images,
storyboards, SwiftUI view structure), class-dump for Objective-C (selectors and
class names survive -- extremely readable), and Ghidra/Hopper/IDA for the rest
(Swift demangles fine). Fleet already owns this stage: hand the binary to
revops-mcp (Ghidra/ReVa) once you have it.

## 3. Network contract (often the whole clone)

Point the app at mitmproxy on Mac/PC, install its CA on the iPhone, watch the
API traffic, reimplement the client. No jailbreak needed -- unless the app does
SSL pinning, in which case you need SSL Kill Switch, which needs jailbreak or
TrollStore. Try the proxy first; it is ~80% of most clones.

## 4. Observation and automation: the "no remote control" niggle

Apple ships no remote-control channel for iOS (no ADB equivalent). But "no auto
clickthrough/screenshot possible" is only one-third true:

- **Watching is easy.** QuickTime over USB mirrors the screen; a Mac also works
  as an AirPlay receiver. No special state required.
- **Screenshots are solved without jailbreak.** `idevicescreenshot` (libimobiledevice,
  current master, packaged in Debian's libimobiledevice-utils as of Apr 2026)
  pulls screenshots over USB. Asterisk, from its own manpage: a mounted developer
  disk image is required -- i.e. an Xcode-paired, developer-mode device, not a
  jailbroken one. Alibaba's `tidevice` wraps the same protocols in Python.
- **Scripted taps are solved with a Mac + cert.** XCUITest/WebDriverAgent drives
  taps, swipes and text entry in third-party apps on stock, non-jailbroken
  devices (this is how every CI device farm automates iOS); Appium sits on top.
  Requirements: a Mac host, a signed WebDriverAgentRunner (paid developer
  account), USB or WiFi. There is no practical Windows-only, cert-free route --
  the Mac is the driver host.
- **Jailbreak VNC (Veency lineage)** exists where jailbreaks exist, i.e. under
  exactly the same version scarcity as the dumpers in section 1.

Practical combo for app mapping with zero jailbreak: proxy (section 3) for the
API contract + `idevicescreenshot` for state capture + WebDriverAgent for
scripted clickthrough. That covers observe, drive, and understand; only binary
decryption still demands a vulnerable device.

## 5. Rebuild rule

Reimplement from what you learned (clean, yours, shippable). Patching their
binary is fragile, theirs, and legally radioactive. Paid-feature gating in your
own apps goes server-side; the client is open reading material (see the moat
discussion that prompted this note).

---
*Filed 2026-10-28. Companion: [Apple hub](apple/README.md). Jailbreak trackers used:
jailbreakly.com (27: demo only; 26: Dopamine rootless), r/jailbreak TrollDecrypt threads.*
