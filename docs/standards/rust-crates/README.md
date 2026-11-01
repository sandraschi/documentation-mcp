# Rust Crates — Fleet Field Guide

Short, opinionated notes on the most important Rust crates for the
rustification rollout. ("Crates" is the correct term: a crate is what
`Cargo.toml` depends on and what `cargo build` compiles. A *library* is a
crate with a lib target; a *module* is a `mod` inside a crate.)

| Doc | Covers | Fleet rule of thumb |
|---|---|---|
| [BEVY.md](BEVY.md) | Bevy game engine (ECS, 3D, audio, UI) | Full-engine needs only, with written justification |
| [3D.md](3D.md) | Viewers + dynamic viewing (`three-d`, `rend3`, `kiss3d`) | `three-d` for viewer/clone jobs |
| [GRAPHS.md](GRAPHS.md) | Charts (`egui_plot`, `plotters`) + graph structures (`petgraph`) | `egui_plot` inside egui, `plotters` for files, `petgraph` for relations |
| [COMMS.md](COMMS.md) | HTTP/WS/MQTT/serial (`reqwest`, `tokio-tungstenite`, `rumqttc`, `serialport`) | Match the wire protocol, nothing bigger |
| [DATABASE.md](DATABASE.md) | Embedded + client SQL (`rusqlite`, `sqlx`, `redb`) | `rusqlite` local-first, `sqlx` for servers |
| [TOOLCHAIN.md](TOOLCHAIN.md) | PyPI/npm/bun → cargo table (registries, runners, linters, bundlers) | Half these rows *delete* tooling — no runtime |
| [ECOSYSTEM.md](ECOSYSTEM.md) | Maturity map, real gaps, key sites (official + community) | Read before planning any rustification |

Versions below were verified against crates.io on 2026-10-17. Pin exact
versions per repo; bump deliberately, never blindly. Pre-1.0 crates
(everything here except `rusqlite`/`plotters`/`petgraph`) may break API
between minors — read the changelog before upgrading.
