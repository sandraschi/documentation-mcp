# CraftDeck — Handover Document

**Last Updated**: 2026-11-10
**Current State**: v0.2.0 Active Launcher
**Primary Artifact**: [sandraschi/craft-deck](https://github.com/sandraschi/craft-deck)

---

## 1. What Was Done
- Forked and extended from `storytold/craft-launcher` in 100% native Rust.
- Multi-platform packaging: Windows, macOS, Linux.
- Added cards for Sandra's bespoke Craft apps.

---

## 2. Immediate Next Steps
1. Add new launcher cards for `DevCraft` (`devcraft-start.bat`) and `AICraft` (`aicraft-start.bat`).
2. Add real-time socket detection on card badges (e.g. green indicator when port `11258` or `11260` is active).
