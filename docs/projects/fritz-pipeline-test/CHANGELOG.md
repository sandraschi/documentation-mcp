# Changelog

## [0.1.0] — 2026-08-02

### Fixed
- **Greeter crash** — `greet()` referenced undefined `grt`; now uses `name`. Test passes.

### Added
- `__main__.py` CLI entry point (`fritz-pipeline-test` prints "Hello, World!")
- `INSTALL.md`, `llms.txt`, `llms-full.txt`, `glama.json`, CHANGELOG
- `uv.lock` (committed), ruff/pytest dev deps, hatchling build system
