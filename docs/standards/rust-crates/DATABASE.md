# Databases in Pure Rust (Embedded + Client SQL)

| Crate (version) | Use when |
|---|---|
| `rusqlite` 0.40 (verified 2026-10-17) | **Local-first default.** Ergonomic SQLite wrapper (bundled SQLite — no system dep). Device-state caches, telemetry logs, FTS5 search indexes, MCP server persistence. Sync API — wrap in `spawn_blocking` or use a dedicated thread with channels; never hold a connection across `.await`. |
| `sqlx` 0.9 (verified 2026-10-17) | Talking to **server** databases (Postgres/MySQL) from async Rust, with compile-time checked queries. Only when the data must live on a server (multi-machine fleet state). Heavier setup (database URL at build time for checked macros, or use unchecked `query!` alternatives). |
| `redb` 4.4 (verified 2026-10-17) | Pure-Rust embedded KV store (no C SQLite at all). Niche pick: content-addressed caches, dedup indexes, when SQLite's SQL is overkill and a typed key-value map is the whole need. |

Rules: data files live under `%LOCALAPPDATA%/<app>/` (Windows) or the repo
`data/` dir for dev — and `data/`, `*.sqlite3`, `*.db*` are always
gitignored (gate item). Migrations: numbered SQL files + a `user_version`
pragma check at startup (`rusqlite`), not ad-hoc ALTERs. Backups are just
file copies — say so in the README.
