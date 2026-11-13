# CraftDeck

**Version**: v0.2.0 — Sovereign Universal Launcher & Package Manager for All Craft Apps.
**Repository**: [`d:\Dev\repos\craft-deck`](file:///d:/Dev/repos/craft-deck) | [GitHub: sandraschi/craft-deck](https://github.com/sandraschi/craft-deck)
**Parent Suite**: Sovereign Craft Suite

---

## What is CraftDeck?

CraftDeck is the universal desktop launcher for Sandra's sovereign software ecosystem. Rebuilt in pure Rust (`eframe` / `egui`), it provides one central tactile cockpit to install, launch, update, and monitor every app in the Craft App Suite.

```
                                 CraftDeck
      (One-Click Desktop Launch / Version Verification / Process Watchdog)
                                     │
    ┌──────────────┬──────────────┬──┴───────────┬──────────────┬──────────────┐
DevCraft        AICraft        CoderCraft     DatabaseCraft   DJCraft     RobotCraft
(11258/11259) (11260/11261)    (14128)        (14113)        (14118)        (14116)
```

- Replaces SaaS app launchers and cloud subscriptions with a 100% offline, local-first application dashboard.
- Monitors running Craft processes, their listening ports, and status.
