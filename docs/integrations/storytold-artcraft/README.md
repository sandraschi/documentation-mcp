# Storytold ArtCraft: The Pure-Rust Multi-Agent Benchmark

**Source**: Brandon Thomas & team · **GitHub**: [github.com/storytold](https://github.com/storytold)

## Overview
ArtCraft is a suite of professional creative desktop tools (FilmCraft, PhotoCraft, SoundCraft, VectorCraft, CadCraft, DeckCraft) written in pure Rust. Its landmark engineering significance: **it was written almost entirely by parallel Claude Opus agent loops operating under a deterministic test harness.**

## Key Principles Borrowed for Fleet Rustification (`r11n`)
The `sandraschi` fleet adopted the ArtCraft methodology for its pure-Rust rewrite track:
1. **Never Let LLMs Invent Architecture**: Treat agents as bounded compilers against typed command buses.
2. **`clippy::deny(clippy::unwrap_used)`**: Zero-panic tolerance across crates. All errors are typed `Result<T, E>`.
3. **The Universal Command Bus (`Command::dispatch`)**: GUI (`egui`), CLI (`clap`), and MCP JSON-RPC handlers dispatch through the same enum, preventing drift.
4. **Oracle Testing**: External ground truth (FFmpeg, PSD round-trips) determines verification rather than model self-grading.
